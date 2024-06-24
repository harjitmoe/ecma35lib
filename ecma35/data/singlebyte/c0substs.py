#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2024.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

graphdata.c0graphics["437"] = (None, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022, 0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C, 0x25BA, 0x25C4, 0x2195, 0x203C, 0xB6, 0xA7, 0x25AC, 0x21A8, 0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC, 0x2302)
graphdata.c0graphics["897"] = (None, 0x2554, 0x2557, 0x255A, 0x255D, 0x2551, 0x2550, 0xFFEC, None, 0xFFEE, None, 0x303F, None, None, 0xFFED, 0x263C, 0x256C, None, 0x2195, None, 0x2593, 0x2569, 0x2566, 0x2563, None, 0x2560, 0x2591, 0x21B5, 0xFFEA, 0xFFE8, 0xFFEB, 0xFFE9, None)
graphdata.c0graphics["903"] = graphdata.c0graphics["897"]
graphdata.c0graphics["904"] = graphdata.c0graphics["897"]

graphdata.c0graphics["1051"] = graphdata.c0graphics["1052"] = graphdata.c0graphics["1054"] = graphdata.c0graphics["437"][:-1] + (9618,)

graphdata.c0graphics["1056"] = graphdata.c0graphics["437"][:-1] + (9617,)

# 0xabad1dea's C0 graphics for Windows-1252 on the Famicom
# See: https://github.com/0xabad1dea/0xabad1dea.github.com/blob/master/img/nes-ansi.png
graphdata.c0graphics["1252"] = (None, 0x1F7E5, 0x1F7E9, 0x2588, 0x1CD2A, 0x1FB97, 0x2592, 0x2661, 0x2662, 0x2667, 0x2664, 0x263A, 0x2639, 0x1D15E, 0x266B, 0x266A, 0x2640, 0x2642, 0x23FB, 0x24B6, 0x24B7, 0x2191, 0x2193, 0x2190, 0x2192, 0x254B, 0x2503, 0x2501, 0x2595, 0x2594, 0x2581, 0x258F, None)

# Macintosh compatibility C0 graphics
# The common C0 replacements are the device controls. Others seem to vary with version.
# Version attested in Chicago bitmaps from Mac OS 8.0 and also in KEYBOARD.TXT. Note that the 
#   assignment of the escape key symbol to the escape character will not be accessible in 
#   ecma35lib as it currently works.
# Note that KEYBOARD.TXT includes several mappings which differ, due to predating the addition of
#   the WDings repertoires (and with it, more closely matching characters) to Unicode:
#     U+21E5 (⇥) where we have U+2B72 (⭲)
#     U+21E4 (⇤) where we have U+2B70 (⭰)
#     U+21A9 (↩) where we have U+2B90 (⮐)
#     U+21AA (↪) where we have U+2B91 (⮑)
#     U+F802 (PUA) where we have U+1F589 (🖉)
#     U+21E3 (⇣) where we have U+2B6D (⭭)
#     U+21E0 (⇠) where we have U+2B6A (⭪)
#     U+21E1 (⇡) where we have U+2B6B (⭫)
#     U+21E2 (⇢) where we have U+2B6C (⭬)
# Also, note well that some treatments of the character mapped here to U+25C6 (◆) per KEYBOARD.TXT
#   closer match U+2666 (♦), see for example IBM's CPGID-1275 code chart.
graphdata.c0graphics["1275"] = graphdata.c0graphics["1280"] = graphdata.c0graphics["1281"] = \
graphdata.c0graphics["1282"] = graphdata.c0graphics["1283"] = graphdata.c0graphics["1284"] = \
graphdata.c0graphics["1285"] = graphdata.c0graphics["1286"] = \
  (None,      None,      (0x2B72,), (0x2B70,), (0x2324,), (0x21E7,), (0x2303,), (0x2325,),
   None,      (0x2423,), (0x2326,), (0x2B90,), (0x2B91,), None,      None,      (0x1F589,),
   (0x2B6D,), (0x2318,), (0x2713,), (0x25C6,), (0xF8FF,), None,      None,      (0x232B,),
   (0x2B6A,), (0x2B6B,), (0x2B6C,), (0x238B,), (0x2327,),) + ((None,) * 4)
# Version attested in Chicago.ttf (not ChicagoFLF.ttf). Though U+2398 is an approximate mapping.
graphdata.c0graphics["10000"] = graphdata.c0graphics["10004"] = graphdata.c0graphics["10005"] = \
graphdata.c0graphics["10006"] = graphdata.c0graphics["10081"] = graphdata.c0graphics["10029"] = \
graphdata.c0graphics["10017"] = graphdata.c0graphics["10007"] = graphdata.c0graphics["10082"] = \
graphdata.c0graphics["10010"] = graphdata.c0graphics["10079"] = graphdata.c0graphics["10021"] = \
  (None,             (0x2325,), (0x2303,), (0x2324,), (0x21E7,), (0x21EA,), (0x238B,), (0x2423,),
   (0x232B,),        None,      (0x2B72,), (0x2B92,), (0x2398,), None,      (0x2B90,), (0x237D,),
   (0xF8FF, 0xF87A), (0x2318,), (0x2713,), (0x2666,), (0xF8FF,), (0x2326,), (0x2B70,), (0x2B91,),
   (0x2B93,)) + ((None,) * 8)





