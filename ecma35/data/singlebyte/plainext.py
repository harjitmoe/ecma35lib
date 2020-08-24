#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

graphdata.c0graphics["437"] = (None, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022, 0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C, 0x25BA, 0x25C4, 0x2195, 0x203C, 0xB6, 0xA7, 0x25AC, 0x21A8, 0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC, 0x2302)
graphdata.c0graphics["897"] = (None, 0x2554, 0x2557, 0x255A, 0x255D, 0x2551, 0x2550, 0xFFEC, None, 0xFFEE, None, 0x303F, None, None, 0xFFED, 0x263C, 0x256C, None, 0x2195, None, 0x2593, 0x2569, 0x2566, 0x2563, None, 0x2560, 0x2591, 0x21B5, 0xFFEA, 0xFFE8, 0xFFEB, 0xFFE9, None)
graphdata.c0graphics["903"] = graphdata.c0graphics["897"]
graphdata.c0graphics["904"] = graphdata.c0graphics["897"]

# Windows-125x pages, excluding Windows-1258 which is with the rest of the quo^'c ngu*~ encodings
graphdata.rhses["1250"] = parsers.read_single_byte("WHATWG/index-windows-1250.txt")
graphdata.rhses["1251"] = parsers.read_single_byte("WHATWG/index-windows-1251.txt")
graphdata.rhses["1252"] = parsers.read_single_byte("WHATWG/index-windows-1252.txt") # ISO-8859-1 ext.
graphdata.defgsets["1252"] = ("ir006", "ir100", "nil", "nil")
graphdata.rhses["1253"] = parsers.read_single_byte("WHATWG/index-windows-1253.txt")
graphdata.rhses["1254"] = parsers.read_single_byte("WHATWG/index-windows-1254.txt") # ISO-8859-9 ext.
graphdata.defgsets["1254"] = ("ir006", "ir148", "nil", "nil")
graphdata.rhses["1255"] = parsers.read_single_byte("WHATWG/index-windows-1255.txt")
graphdata.rhses["1256"] = parsers.read_single_byte("WHATWG/index-windows-1256.txt")
graphdata.rhses["1257"] = parsers.read_single_byte("WHATWG/index-windows-1257.txt")

# OEM pages (TODO: 210 Greek and 220 Spanish are both listed by DEC in the very definition of the
#   DECSPPCS CSI control, alongside some of the below. I do not have a source for their layout.)
graphdata.rhses["437"] = parsers.read_single_byte("ICU/ibm-437_P100-1995.ucm")
graphdata.defgsets["437"] = ("ir006", "nil", "nil", "nil") # Note: gets used as default.
graphdata.rhses["720"] = parsers.read_single_byte("ICU/ibm-720_P100-1997.ucm")
graphdata.rhses["737"] = parsers.read_single_byte("ICU/ibm-737_P100-1997.ucm")
graphdata.rhses["775"] = parsers.read_single_byte("ICU/ibm-775_P100-1996.ucm")
graphdata.rhses["850"] = parsers.read_single_byte("ICU/ibm-850_P100-1995.ucm")
graphdata.rhses["852"] = parsers.read_single_byte("ICU/ibm-852_P100-1995.ucm")
graphdata.rhses["855"] = parsers.read_single_byte("ICU/ibm-855_P100-1995.ucm")
graphdata.rhses["857"] = parsers.read_single_byte("ICU/ibm-857_P100-1995.ucm")
graphdata.rhses["858"] = parsers.read_single_byte("ICU/ibm-858_P100-1997.ucm")
graphdata.rhses["860"] = parsers.read_single_byte("ICU/ibm-860_P100-1995.ucm")
graphdata.rhses["861"] = parsers.read_single_byte("ICU/ibm-861_P100-1995.ucm")
graphdata.rhses["862"] = parsers.read_single_byte("ICU/ibm-862_P100-1995.ucm")
graphdata.rhses["863"] = parsers.read_single_byte("ICU/ibm-863_P100-1995.ucm")
graphdata.rhses["864"] = parsers.read_single_byte("ICU/ibm-864_X110-1999.ucm")
graphdata.rhses["865"] = parsers.read_single_byte("ICU/ibm-865_P100-1995.ucm")
graphdata.rhses["866"] = parsers.read_single_byte("WHATWG/index-ibm866.txt")
graphdata.rhses["869"] = parsers.read_single_byte("ICU/ibm-869_P100-1995.ucm")
graphdata.rhses["897"] = ((None,) * 33) + tuple(range(0xFF61, 0xFFA0)) + ((None,) * 32)
graphdata.defgsets["897"] = ("ir014", "ir013", "nil", "nil")
graphdata.rhses["903"] = (None,) * 128
graphdata.defgsets["903"] = ("ir014", "nil", "nil", "nil")
graphdata.rhses["904"] = (None,) * 128
graphdata.defgsets["904"] = ("ir006", "nil", "nil", "nil")
graphdata.rhses["1125"] = parsers.read_single_byte("ICU/ibm-1125_P100-1997.ucm")
graphdata.rhses["1131"] = parsers.read_single_byte("ICU/ibm-1131_P100-1997.ucm")

# Code pages 874 (TIS-620 exts)
# Per alias comments in ICU's convrtrs.txt, IBM's 874 is identical to IBM's 9066.
# Microsoft's 874, on the other hand, matches the layout of IBM's 1162.
graphdata.rhses["1162"] = parsers.read_single_byte("WHATWG/index-windows-874.txt")
graphdata.rhses["9066"] = parsers.read_single_byte("ICU/ibm-874_P100-1995.ucm")
# The two only collide at 0xA0, which IBM uses for an alternate U+0E48 and which Microsoft
#   uses for an NBSP. Favour the more-deployed Microsoft / ISO-8859-11 NBSP for "874".
graphdata.rhses["874"] = tuple(a or b for a, b in zip(graphdata.rhses["1162"],
                                                      graphdata.rhses["9066"]))
graphdata.defgsets["874"] = graphdata.defgsets["1162"] = ("ir006", "ir166", "nil", "nil")

# Macintosh pages
graphdata.rhses["10000"] = graphdata.rhses["1275"] = parsers.read_single_byte("WHATWG/index-macintosh.txt")
graphdata.rhses["10004"] = parsers.read_mozilla_ut_file("Mozilla/macarabic.ut")
graphdata.rhses["10005"] = parsers.read_mozilla_ut_file("Mozilla/machebrew.ut")
graphdata.rhses["10006"] = graphdata.rhses["1280"] = parsers.read_mozilla_ut_file("Mozilla/macgreek.ut")
graphdata.rhses["10081"] = graphdata.rhses["1281"] = parsers.read_mozilla_ut_file("Mozilla/macturki.ut")
graphdata.rhses["10029"] = graphdata.rhses["1282"] = parsers.read_mozilla_ut_file("Mozilla/macce.ut")
# 10007/1283 is the original MacCyrillic; current MacCyrillic is a Euro update of 10017.
# Mappings to U+00A4 changed to U+20AC across the board, so number the current one 10017, and use
#   a version with that change but not the others for 10007/1283.
graphdata.rhses["10017"] = parsers.read_single_byte("WHATWG/index-x-mac-cyrillic.txt")
maccy = list(graphdata.rhses["10017"])
maccy[0x22] = (0x00A2,)
maccy[0x36] = (0x2202,)
graphdata.rhses["10007"] = graphdata.rhses["1283"] = tuple(maccy)
graphdata.rhses["10082"] = graphdata.rhses["1284"] = parsers.read_mozilla_ut_file("Mozilla/maccroat.ut")
graphdata.rhses["10010"] = graphdata.rhses["1285"] = parsers.read_mozilla_ut_file("Mozilla/macro.ut")
graphdata.rhses["10079"] = graphdata.rhses["1286"] = parsers.read_mozilla_ut_file("Mozilla/macicela.ut")
#graphdata.rhses["10021"] = parsers.read_mozilla_ut_file("Mozilla/macthai.ut")
# The common C0 replacements are the device controls. Others seem to vary with version.
# Version attested in Chicago bitmaps from Mac OS 8.0. Note that the assignment of the escape
#   key symbol to the escape character will not be accessible in ecma35lib as it currently works.
graphdata.c0graphics["1275"] = graphdata.c0graphics["1280"] = graphdata.c0graphics["1281"] = \
graphdata.c0graphics["1282"] = graphdata.c0graphics["1283"] = graphdata.c0graphics["1284"] = \
graphdata.c0graphics["1285"] = graphdata.c0graphics["1286"] = \
  (None,      None,      (0x2B72,), (0x2B70,), (0x2324,), (0x21E7,), (0x2303,), (0x2325,),
   None,      None,      (0x2326,), (0x2B90,), (0x2B91,), None,      None,      None,
   (0x2B6D,), (0x2318,), (0x2713,), (0x2666,), (0xF8FF,), None,      None,      (0x232B,),
   (0x2B6A,), (0x2B6B,), (0x2B6C,), (0x238B,), (0x2327,),) + ((None,) * 4)
# Version attested in Chicago.ttf (not ChicagoFLF.ttf). Though U+2398 is an approximate mapping.
graphdata.c0graphics["10000"] = graphdata.c0graphics["10004"] = graphdata.c0graphics["10005"] = \
graphdata.c0graphics["10006"] = graphdata.c0graphics["10081"] = graphdata.c0graphics["10029"] = \
graphdata.c0graphics["10017"] = graphdata.c0graphics["10007"] = graphdata.c0graphics["10082"] = \
graphdata.c0graphics["10010"] = graphdata.c0graphics["10079"] = \
  (None,             (0x2325,), (0x2303,), (0x2324,), (0x21E7,), (0x21EA,), (0x238B,), (0x2423,),
   (0x232B,),        None,      (0x2B72,), (0x2B92,), (0x2398,), None,      (0x2B90,), (0x237D,),
   (0xF8FF, 0xF87A), (0x2318,), (0x2713,), (0x2666,), (0xF8FF,), (0x2326,), (0x2B70,), (0x2B91,),
   (0x2B93,)) + ((None,) * 8)

# KOI-8 encodings
graphdata.rhses["878"] = graphdata.rhses["20866"] = parsers.read_single_byte("WHATWG/index-koi8-r.txt")
# Note: 21866 is used for both KOI8-U and KOI8-RU.
graphdata.rhses["1168"] = graphdata.rhses["21866"] = parsers.read_single_byte("WHATWG/index-koi8-u.txt")





