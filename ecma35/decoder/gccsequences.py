#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2022.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.controldata import rformats
from ecma35.data.gccdata import gcc_tuples
from ecma35.data.names import namedata
from ecma35.data.multibyte import korea
import itertools

def gcc_lookup(tupl):
    if tupl in gcc_tuples:
        return gcc_tuples[tupl]
    chartuple = tuple(chr(i) for i in tupl)
    if chartuple and all(i in korea.combjamo for i in chartuple):
        hangultuple = tuple(itertools.dropwhile(lambda c: c == "\u3164", chartuple))[::-1]
        hangultuple = tuple(itertools.dropwhile(lambda c: c == "\u3164", hangultuple))[::-1]
        unic = None
        # Note: the filler is in all three, but we've stripped side fillers so it's a vowel here
        if any(i in korea.vowels for i in hangultuple):
            inits = tuple(itertools.takewhile(lambda c: c not in korea.vowels, hangultuple))
            notinits = tuple(itertools.dropwhile(lambda c: c not in korea.vowels, hangultuple))
            vowels = tuple(itertools.takewhile(lambda c: c in korea.vowels, notinits))
            finals = tuple(itertools.dropwhile(lambda c: c in korea.vowels, notinits))
            if len(inits) == 0:
                i = "\u115F"
            elif len(inits) == 1:
                i = korea.initials.get(inits[0], None)
            else:
                i = korea.compinitials.get(inits, None)
            if len(vowels) == 1:
                v = korea.vowels.get(vowels[0], None)
            else:
                v = korea.compvowels.get(vowels, None)
            if len(finals) == 0:
                f = ""
            elif len(finals) == 1:
                f = korea.finals.get(finals[0], None)
            else:
                f = korea.compfinals.get(finals, None)
            if f is not None and i and v:
                unic = i + v + f
        else:
            if hangultuple in korea.compsimple:
                unic = korea.compsimple[hangultuple]
            elif hangultuple in korea.compinitials:
                unic = korea.compinitials[hangultuple] + "\u1160"
            elif hangultuple in korea.compfinals:
                unic = "\u115F\u1160" + korea.compfinals[hangultuple]
            else:
                for split in range(1, len(hangultuple)):
                    if (inits := hangultuple[:split]) in korea.compinitials:
                        if (finals := hangultuple[split:]) in korea.compfinals:
                            unic = korea.compinitials[inits] + "\u1160" + korea.compfinals[finals]
                            break
        if unic: # NOT elif
            return tuple(ord(i) for i in namedata.canonical_recomp.get(unic, unic))  
    return tupl

okay_controls = {"SP": 0x20}
okay_controls.update(rformats)

def proc_gcc_sequences(stream, state):
    mode = "normal"
    bytesleft = 0
    reconsume = None
    series = []
    chars = []
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if mode == "normal":
            if token[:3] in (("CSISEQ", "GCC", (0x30,)), ("CSISEQ", "GCC", ())):
                mode = "firstbyte"
                bytesleft = 2
                series = [token]
                chars = []
            elif token[:3] == ("CSISEQ", "GCC", (0x31,)):
                mode = "variable"
                series = [token]
                chars = []
            # Transcoding hints for composition used in Apple mappings
            elif token[:2] in (("CHAR", 0xF860), ("CHAR", 0xF86A)):
                mode = "firstbyte"
                bytesleft = 2
                series = [token]
                chars = []
            elif token[:2] == ("CHAR", 0xF861):
                mode = "firstbyte"
                bytesleft = 3
                series = [token]
                chars = []
            elif token[:2] in (("CHAR", 0xF862), ("CHAR", 0xF86B)):
                mode = "firstbyte"
                bytesleft = 4
                series = [token]
                chars = []
            else:
                yield token
        elif mode == "firstbyte":
            if token[0] == "CHAR":
                series.append(token)
                chars.append(token[1])
                bytesleft -= 1
                mode = "secondbyte" if bytesleft <= 1 else "firstbyte"
            elif token[0] == "COMPCHAR":
                series.extend(token[2])
                chars.extend(token[1])
                bytesleft -= 1
                mode = "secondbyte" if bytesleft <= 1 else "firstbyte"
            elif token[0] == "CTRL" and token[1] in okay_controls:
                series.append(token)
                chars.append(okay_controls[token[1]])
                bytesleft -= 1
                mode = "secondbyte" if bytesleft <= 1 else "firstbyte"
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
                yield ("COMPCHAR", gcc_lookup(tuple(chars)), tuple(series))
                mode = "normal"
            elif token[0] == "COMPCHAR":
                series.extend(token[2])
                chars.extend(token[1])
                yield ("COMPCHAR", gcc_lookup(tuple(chars)), tuple(series))
                mode = "normal"
            elif token[0] == "CTRL" and token[1] in okay_controls:
                series.append(token)
                chars.append(okay_controls[token[1]])
                yield ("COMPCHAR", gcc_lookup(tuple(chars)), tuple(series))
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
            elif token[0] == "CTRL" and token[1] in okay_controls:
                series.append(token)
                chars.append(okay_controls[token[1]])
            elif token[:3] == ("CSISEQ", "GCC", (0x32,)):
                series.append(token)
                yield ("COMPCHAR", gcc_lookup(tuple(chars)), tuple(series))
                mode = "normal"
            elif token[:2] == ("CSISEQ", "GCC"): # i.e. chaining them without express terminator
                series.append(token)
                yield ("COMPCHAR", gcc_lookup(tuple(chars)), tuple(series))
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




