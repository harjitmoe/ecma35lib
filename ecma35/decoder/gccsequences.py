#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd
from ecma35.data.gccdata import gcc_tuples

def proc_gcc_sequences(stream, state):
    mode = "normal"
    reconsume = None
    series = []
    chars = []
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if mode == "normal":
            if token[:3] in (("CSISEQ", "GCC", (0x30,)), ("CSISEQ", "GCC", ())):
                mode = "firstbyte"
                series = [token]
                chars = []
            elif token[:3] == ("CSISEQ", "GCC", (0x31,)):
                mode = "variable"
                series = [token]
                chars = []
            else:
                yield token
        elif mode == "firstbyte":
            if token[0] == "CHAR":
                series.append(token)
                chars.append(token[1])
                mode = "secondbyte"
            elif token[0] == "COMPCHAR":
                series.extend(token[2])
                chars.extend(token[1])
                mode = "secondbyte"
            elif token[:2] == ("CTRL", "SP"):
                series.append(token)
                chars.append(0x20)
                mode = "secondbyte"
            else:
                yield ("ERROR", "TRUNCGCC")
                yield from series
                mode = "normal"
                reconsume = token
                continue
        elif mode == "secondbyte":
            if token[0] == "CHAR":
                series.append(token)
                chars.append(token[1])
                yield ("COMPCHAR", gcc_tuples.get(tuple(chars), tuple(chars)), tuple(series))
                mode = "normal"
            elif token[0] == "COMPCHAR":
                series.extend(token[2])
                chars.extend(token[1])
                yield ("COMPCHAR", gcc_tuples.get(tuple(chars), tuple(chars)), tuple(series))
                mode = "normal"
            elif token[:2] == ("CTRL", "SP"):
                series.append(token)
                chars.append(0x20)
                yield ("COMPCHAR", gcc_tuples.get(tuple(chars), tuple(chars)), tuple(series))
                mode = "normal"
            else:
                yield ("ERROR", "TRUNCGCC")
                yield from series
                mode = "normal"
                reconsume = token
                continue
        elif mode == "variable":
            if token[0] == "CHAR":
                series.append(token)
                chars.append(token[1])
            elif token[0] == "COMPCHAR":
                series.extend(token[2])
                chars.extend(token[1])
            elif token[:2] == ("CTRL", "SP"):
                series.append(token)
                chars.append(0x20)
            elif token[:3] == ("CSISEQ", "GCC", (0x32,)):
                series.append(token)
                yield ("COMPCHAR", gcc_tuples.get(tuple(chars), tuple(chars)), tuple(series))
                mode = "normal"
            elif token[:2] == ("CSISEQ", "GCC"): # i.e. chaining them without express terminator
                series.append(token)
                yield ("COMPCHAR", gcc_tuples.get(tuple(chars), tuple(chars)), tuple(series))
                mode = "normal"
                reconsume = token
                continue
            else:
                yield ("ERROR", "TRUNCGCC")
                yield from series
                mode = "normal"
                reconsume = token
                continue
        else:
            raise AssertionError("unrecognised mode: {!r}".format(mode))



