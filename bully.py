#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Exhaustively runs through a mapping file in a random order, testing
# a given mode.

import random, io
from ecma35.decoder import tokenfeed, simplecomparer

def bully(fn, statesequence):
    stringdat = []
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                a, b = line.split(None, 3)[:2]
                assert a[:2] == "0x"
                assert b[:2] in ("0x", "U+")
                stuff1 = int(a[2:], 16)
                unic = int(b[2:], 16)
                stuff2 = bytes([stuff1]) if stuff1 < 256 else bytes([stuff1 >> 8, stuff1 & 0xFF])
                stringdat.append((stuff2, chr(unic)))
    random.shuffle(stringdat)
    codestringdat, ucsstringdat = tuple(zip(*stringdat))
    codestring = statesequence + b"".join(codestringdat)
    ucsstring = "".join(ucsstringdat)
    simple_logger = simplecomparer.simple_logger_maker(ucsstring)
    x = io.BytesIO(codestring)
    x = tokenfeed.process_stream(x, lastfilter=simple_logger)
    for n, i in enumerate(x):
        if i[1] != "SUCCESS":
            print(ascii(i))
            print()

bully("ecma35/data/multibyte/mbmaps/Other/AppendixA_KPS9566-2011-to-Unicode.txt", b"\x1B%1\x1B$)N")

