#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2024, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers


#####################################################################
# WDings (the collective ESC term for Wingdings and Webdings)

webdings = [None] * 256
wingdings1 = [None] * 256
wingdings2 = [None] * 256
wingdings3 = [None] * 256
wdings = (webdings, wingdings1, wingdings2, wingdings3)

with open(os.path.join(parsers.directory, "UTCDocs", "WDingsSources.txt"), "r") as _f:
    for _line in _f:
        if not _line.strip() or _line[0] == "#":
            continue
        _splits = _line.strip().split(";")
        _ucs = int(_splits[0], 16)
        _dings = _splits[1:]
        for _ding in _dings:
            _dingno = int(_ding[0], 10)
            _dingcode = int(_ding[1:], 10)
            wdings[_dingno][_dingcode] = (_ucs,)

wingdings1[-1] = (0x1CC2F,)

graphdata.gsets["webdings_g0"] = (94, 1, tuple(webdings[33:127]))
graphdata.gsets["wingdings1_g0"] = (94, 1, tuple(wingdings1[33:127]))
graphdata.gsets["wingdings2_g0"] = (94, 1, tuple(wingdings2[33:127]))
graphdata.gsets["wingdings3_g0"] = (94, 1, tuple(wingdings3[33:127]))

# I'm basically treating all DECSPPCS code page numbers above 65535 as fair game. Shoot me (don't).
graphdata.rhses["999000"] = tuple(webdings[128:])
graphdata.defgsets["999000"] = ("webdings_g0", "nil", "nil", "nil")
graphdata.rhses["999001"] = tuple(wingdings1[128:])
graphdata.defgsets["999001"] = ("wingdings1_g0", "nil", "nil", "nil")
graphdata.rhses["999002"] = tuple(wingdings2[128:])
graphdata.defgsets["999002"] = ("wingdings2_g0", "nil", "nil", "nil")
graphdata.rhses["999003"] = tuple(wingdings3[128:])
graphdata.defgsets["999003"] = ("wingdings3_g0", "nil", "nil", "nil")


#####################################################################
# Marlett (does this rhyme with Charlotte?)

# Many of the following mappings, arrows especially, might be questioned.
# Not knowing any actual implementation trying to assign Unicode mappings
#   to Marlett, my main concern is preserving "legibility" in a manner of
#   speaking.
# The twelve Marlett characters which were added to Webdings in the same
#   locations retain their Webdings mappings, at any rate.
graphdata.gsets["marlett"] = (94, 1, (
            None,       None,       None,       None,       None,       None,       None,
None,       None,       None,       None,       None,       None,       None,       None,
(0x1F5D5,), (0x1F5D6,), (0x1F5D7,), (0x23F4,),  (0x23F5,),  (0x23F6, ), (0x23F7,),  (0x2B73, 0xF87F),
(0x1F782,), (0x1F783,), None,       None,       None,       None,       None,       None,
None,       None,       None,       None,       None,       None,       None,       None,
None,       None,       None,       None,       None,       None,       None,       None,
None,       None,       None,       None,       None,       None,       None,       None,
None,       None,       None,       None,       None,       None,       None,       None,
None,       (0x2714,),  (0x2713,),  (0x1FB7D,), (0x1FB7F,), (0x23BE,),  (0x23CC,),  (0x2B1B,),
(0x2022,),         (0x25CF,),         (0x25DC, 0xF879), (0x25DE, 0xF879), 
(0x25DC,  0xF87F), (0x25DE, 0xF87F),  (0x2B24,),        (0x1FB9E,), 
(0x1FB9E, 0xF87C), (0x2500,),         (0x1F5D9,),       (0x2753,), 
(0x2BC5,),         (0x2BC6,),         (0x2B0D, 0xF87F), (0x1F780,), 
(0x1FB9F,),        (0x1FB9F, 0xF87C), None, None, None, None, None))


#####################################################################
# Zapf Dingbats

graphdata.gsets["zdings_g0"] = zdg0 = (94, 1, parsers.read_single_byte("UTC/zdingbat.txt", typ="GL94"))
_zapf_gr = list(parsers.read_single_byte("UTC/zdingbat.txt", typ="GR94"))
_zapf_gr[79] = (0x1CEBD,)
graphdata.gsets["zdings_g1"] = zdg1 = (94, 1, tuple(_zapf_gr))
graphdata.rhses["998000"] = (tuple((i,) for i in range(0x2768, 0x2776)) + ((None,) * 19) + 
                             zdg1[2] + (None,))
graphdata.defgsets["998000"] = ("zdings_g0", "zdings_g1", "nil", "nil")


#####################################################################
# WordPerfect Iconic Symbols (not ECMA-35 structured)

# This is the original source of U+231A and U+231B emoji (and U+2319).
# 0x00–0x22 were defined in WordPerfect 5.
# WordPerfect 6 changed it so 0x21–0x7E, 0xA1–0xEF and 0xF1–0xFE
#   ranges are Zapf Dingbats, while 0x00–0x20 are similar (not identical).
#   0x7F–0xA0 and 0xF0 do not follow Zapf (or Mac OS) Dingbats.
# 0xF0 is basically an outlined version of U+27A7 (0xE7) afaict.
# 0xF1 is noted in wp6.enc as west-pointing but otherwise description
#   matches Zapf Dingbats so I'm assuming this to be an error.

wordperfect5_page5 = ((0x2665,), (0x2666,), (0x2663,), (0x2660,), (0x2642,), 
                      (0x2640,), (0x263C,), (0x263A,), (0x263B,), (0x266A,),
                      (0x266C,), (0x25AC,), (0x2302,), (0x203C,), (0x221A,),
                      (0x21A8,), (0x2310,), (0x2319,), (0x25D8,), (0x25D9,),
                      (0x21B5,), (0x261E,), (0x261C,), (0x2713,), (0x2610,),
                      (0x2612,), (0x2639,), (0x266F,), (0x266D,), (0x266E,),
                      (0x260E,), (0x231A,), (0x231B,), (0x2104,), (0x2423,))

wordperfect6_page5_init = ((0x2661,), (0x2662,), (0x2667,), (0x2664,), (0x2642,), 
                      (0x2640,), (0x263C,), (0x263A,), (0x263B,), (0x266A,),
                      (0x266C,), (0x25AC,), (0x2302,), (0x203C,), (0x221A,),
                      (0x21A8,), (0x2310,), (0x2319,), (0x25D8,), (0x25D9,),
                      (0x21B5,), (0x2104,), (0x261C,), (0x2423,), (0x2610,),
                      (0x2612,), (0x2639,), (0x266F,), (0x266D,), (0x266E,),
                      (0x260F,), (0x231A,), (0x231B,))

# Characters 0x7F thru 0xA1 in WordPerfect 6 page 5. For now, I'm not even *trying* to round
#   trip the arrow styles given that I have only textual descriptions to work from.
wp6p5fill = ((0x1F676,),
(0x1F677,), (0x2774,), (0x2775,), (0x276A,), (0x276B,), (0x276C,), (0x276D,), (0x2772,),
(0x2773,), (0x1F589, 0xF87F), (0x1F58B, 0xF87F), (0x1F58A, 0xF87F), (0x06DE,), (0x1F5F6,), (0x1F5F8,), (0x2192,),
(0x2190,), (0x2190,), (0x2190,), (0x2190,), (0x2190,), (0x2190,), (0x2192,), (0x2190,), 
(0x2192,), (0x2190,), (0x2192,), (0x2190,), (0x2192,), (0x2190,), (0x25D6,), (0x1F48B,),
(0x00B6,),)

wordperfect6_page5 = wordperfect6_page5_init + zdg0[2] + wp6p5fill + zdg1[2] + (None,)

graphdata.rhses["998001"] = wordperfect6_page5[128:]
graphdata.defgsets["998001"] = ("zdings_g0", "zdings_g1", "nil", "nil")
graphdata.c0graphics["998001"] = (*wordperfect6_page5[:32], wordperfect6_page5[127])

graphdata.rhses["998002"] = wordperfect5_page5 + (None,) * 93

def fill():
    for hi in range(16):
        for lo in range(16):
            no = (hi << 4) | lo
            bit = wordperfect6_page5[no]
            print("".join(chr(i) for i in bit) if bit else "\uFFFD", end = " ")
        print()


#####################################################################
# LaTeX "wasy10" symbol set

graphdata.rhses["998100"] = (
  (0x2206,),  (0x22B2,), (0x22B4,),  (0x22B3,), (0x22B5,),  (0x2234,),  (0x2315,),  (0x260E,),
  (0x2713,),  (0x21E8,), (0x1FBFA,), (0x266A,), (0x2669,),  (0x1D15E,), (0x1D15D,), (0x266B,),
  (0x25C0,),  (0x25B6,), (0x21AF,),  (0x264C,), (0x260B,),  (0x29B0,),  (0x235F,),  (0x2648,),
  (0x2310,),  (0x2640,), (0x2642,),  (0x00A4,), (0x1F552,), (0x221D,),  (0x2222,),  (0x2205,),
  (0x25CF,),  (0x2941,), (0x2940,),  (0x25CB,), (0x263E,),  (0x263D,),  (0x2641,),  (0x263F,),
  (0x2039,),  (0x203A,), (0xFE3F,),  (0xFE40,), (0x263A,),  (0x263B,),  (0x263C,),  (0x2639,),
  (0x2127,),  (0x22C8,), (0x25A1,),  (0x25C7,), (0x26DD,),  (0x2311,),  (0x29FE,),  (0x2394,),
  (0x1F6D1,), (0x2B21,), (0x223F,),  (0x219D,), (0x228F,),  (0x2290,),  (0x2272,),  (0x2273,),
  (0x224B,),  (0x26B9,), (0x1F7B5,), (0x2721,), (0x2B20,),  (0x1F7AF,), (0x2207,),  (0x25D6,),
  (0x25D7,),  (0x25D1,), (0x25D0,),  (0x25B2,), (0x25BC,),  (0x00A7,),  (0x20AC,),  (0x0292,),
  (0x27B0,),  (0x2E59,), (0x2E5A,),  (0x2318,), (0x017F,),  (0x0259,),  (0x260C,),  (0x260D,),
  (0x2643,),  (0x2644,), (0x26E2,),  (0x2646,), (0x2647,),  (0x2649,),  (0x264A,),  (0x264B,),
  (0x264D,),  (0x264E,), (0x264F,),  (0x2650,), (0x2651,),  (0x2652,),  (0x2653,),  (0x00A2,),
  (0x2030,),  (0x00FE,), (0x00DE,),  (0x00F0,), (0x0254,),  (0x1FBBF,), (0x2350,),  (0x2357,),
  (0x2347,),  (0x2348,), (0x222B,),  (0x222C,), (0x222D,),  (0x222E,),  (0x222F,),  (0x222B,),
  (0x222C,),  (0x222D,), (0x222E,),  (0x222F,), (0x00A6,),  (0x235E,),  (0x2395,),  (0x235D,))
graphdata.defgsets["998100"] = ("alt646/knuth", "nil", "nil", "nil")


