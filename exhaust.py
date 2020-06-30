#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Exhaustively runs through a mapping file in a random order, testing
#   a given state of the decoder.
# The idea being to test all codes, not just the handful tested by
#   test.py, as well as properly testing the ones which Python doesn't
#   have codecs for without tedious manual encoding of test strings.

import random, io
from ecma35.decoder import tokenfeed, simplecomparer

def bully(fn, statesequence):
    stringdat = []
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() and not line.startswith("#") and (len(line.split(None, 1)) == 2):
                a, b = line.split(None, 2)[:2]
                if b[0] == "#": # i.e. "#UNDEFINED"
                    continue
                assert a[:2] == "0x", (a, b)
                assert b[:2] in ("0x", "U+"), (a, b)
                stuff1 = int(a[2:], 16)
                unic = "".join(chr(int(j, 16)) for j in b[2:].replace("0x", "").split("+"))
                if stuff1 in (0x1B, 0x0E, 0x0F, 0x8E, 0x8F, 0x90, 0x98, 0x9B, 0x9D, 0x9E, 0x9F):
                    # Don't insert shifts, escape sequences or other control sequences
                    continue
                elif unic == "\u3164":
                    # Don't insert truncated Hangul fillers
                    continue
                elif len(unic) > 1:
                    continue # Nukes test efficacy, but just can't compare reliably otherwise.
                else:
                    if stuff1 < 256:
                        stuff2 = bytes([stuff1])
                    elif stuff1 < 65536:
                        stuff2 = bytes([stuff1 >> 8, stuff1 & 0xFF])
                    else:
                        stuff2 = bytes([stuff1 >> 16, (stuff1 >> 8) & 0xFF, stuff1 & 0xFF])
                    stringdat.append((stuff2, unic))
    random.shuffle(stringdat)
    codestringdat, ucsstringdat = tuple(zip(*stringdat))
    codestring = statesequence + b"".join(codestringdat)
    ucsstring = "".join(ucsstringdat)
    simple_comparator = simplecomparer.simple_comparator_maker(ucsstring)
    x = io.BytesIO(codestring)
    x = tokenfeed.process_stream(x, lastfilter=simple_comparator)
    for n, i in enumerate(x):
        if i[1] != "SUCCESS":
            print(ascii(i))
            print()

print("===", "KPS 9566:2011", "===")
bully("ecma35/data/multibyte/mbmaps/Other/AppendixA_KPS9566-2011-to-Unicode.txt", b"\x1B%1\x1B$)N")
print("===", "KPS 9566:2003", "===")
bully("ecma35/data/multibyte/mbmaps/UTC/KPS9566.TXT", b"\x1B%1\x1B&0\x1B$)N")
print("===", "Unified Hangul Code", "===")
bully("ecma35/data/multibyte/mbmaps/UTC/KSC5601.TXT", b"\x1B%1")
print("===", "Microsoft Big5", "===")
bully("attic/CP950.TXT", b"\x1B%4\x1B&?\x1B$+!2")
print("===", "KanjiTalk 7", "===")
bully("ecma35/data/multibyte/mbmaps/Vendor/JAPANESE.TXT", b"\x1B%0\x1B&0\x1B(J\x1B&1\x1B$)B\x1B&1\x1B*I")
print("===", "HangulTalk", "===")
bully("ecma35/data/multibyte/mbmaps/Vendor/KOREAN.TXT", b"\x1B%6\x1B&?\x1B$+!:")








