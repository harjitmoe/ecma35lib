#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte.korea import initials, vowels, finals, combjamo
from ecma35.data.names import namedata

def proc_hangul_fillers(stream, state):
    first = second = third = fourth = None
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if first is not None:
            assert fourth is None # Shouldn't remain non-None across iterations.
            if (token[0] != "CHAR" or chr(token[1]) not in combjamo) and (
                    token[0] != "CTRL" or token[1] not in ("HF", "HWHF")):
                yield("ERROR", "TRUNCHANGUL", None)
                yield first
                if second is not None:
                    yield second
                if third is not None:
                    yield third
                first = second = third = None
                reconsume = token
                continue
            elif third is not None:
                fourth = token
                try:
                    if first[:2] not in {("CTRL", "HF"), ("CTRL", "HWHF")}:
                        raise KeyError
                    # KeyError may also be raised by the following statement:
                    unic = (initials[chr(second[1])] + vowels[chr(third[1])] +
                            finals[chr(fourth[1])])
                except KeyError:
                    yield("ERROR", "BADHANGUL", None)
                    yield first
                    first, second, third, fourth = second, third, fourth, None
                else:
                    cunic = namedata.canonical_recomp.get(unic, unic)
                    sources = (first, second, third, fourth)
                    yield ("COMPCHAR", tuple(ord(i) for i in cunic), sources)
                    first = second = third = fourth = None
            elif second is not None:
                third = token
            else:
                second = token
        elif token[0] == "CTRL" and token[1] in ("HF", "HWHF"):
            first = token
        else:
            yield token





