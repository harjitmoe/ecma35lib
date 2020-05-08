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
                if b[0] == "#": # i.e. "#UNDEFINED"
                    continue
                assert a[:2] == "0x", (a, b)
                assert b[:2] in ("0x", "U+"), (a, b)
                stuff1 = int(a[2:], 16)
                if stuff1 in (0x1B, 0x0E, 0x0F, 0x8E, 0x8F, 0x90, 0x98, 0x9B, 0x9D, 0x9E, 0x9F):
                    # Don't insert shifts, escape sequences or other control sequences
                    continue
                unic = int(b[2:], 16)
                if stuff1 < 256:
                    stuff2 = bytes([stuff1])
                elif stuff1 < 65536:
                    stuff2 = bytes([stuff1 >> 8, stuff1 & 0xFF])
                else:
                    stuff2 = bytes([stuff1 >> 16, (stuff1 >> 8) & 0xFF, stuff1 & 0xFF])
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

print("===", "KPS 9566:2011", "===")
bully("ecma35/data/multibyte/mbmaps/Other/AppendixA_KPS9566-2011-to-Unicode.txt", b"\x1B%1\x1B$)N")
print("===", "KPS 9566:2003", "===")
bully("ecma35/data/multibyte/mbmaps/UTC/KPS9566.TXT", b"\x1B%1\x1B&0\x1B$)N")
#print("===", "Microsoft Big5", "===")
#bully("ecma35/data/multibyte/mbmaps/Vendor/CP950.TXT", b"\x1B%4")








