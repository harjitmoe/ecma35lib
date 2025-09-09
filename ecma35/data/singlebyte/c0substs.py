#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2024, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# The IBM PC (IBM 5150) OEM character set C0 control code replacement graphical characters.
# Note: this gets used as the default.
graphdata.c0graphics["437"] = (
  None,      (0x263A,), (0x263B,), (0x2665,), (0x2666,), (0x2663,), (0x2660,), (0x2022,),
  (0x25D8,), (0x25CB,), (0x25D9,), (0x2642,), (0x2640,), (0x266A,), (0x266B,), (0x263C,),
  (0x25BA,), (0x25C4,), (0x2195,), (0x203C,), (0x00B6,), (0x00A7,), (0x25AC,), (0x21A8,),
  (0x2191,), (0x2193,), (0x2192,), (0x2190,), (0x221F,), (0x2194,), (0x25B2,), (0x25BC,),
    (0x2302,))

# Slightly modified OEM C0 graphics set rendering 0x7F (ASCII DEL) as a shaded block rather than as
#   a "house", as in IBM's Hewlett-Packard-compatibility code pages
graphdata.c0graphics["1051"] = graphdata.c0graphics["1052"] = graphdata.c0graphics['1053'] = \
graphdata.c0graphics["1054"] = graphdata.c0graphics["1055"] = graphdata.c0graphics["1056"] = \
graphdata.c0graphics["1057"] = graphdata.c0graphics["1058"] = \
    graphdata.c0graphics["437"][:-1] + (0x2592,)

# A different C0 graphics set used in East Asian IBM code pages (i.e. IBM 5550 instead of IBM 5150)
graphdata.c0graphics['891'] = graphdata.c0graphics['897'] = graphdata.c0graphics['903'] = \
graphdata.c0graphics['904'] = graphdata.c0graphics['911'] = graphdata.c0graphics['1040'] = \
graphdata.c0graphics['1041'] = graphdata.c0graphics['1042'] = graphdata.c0graphics['1043'] = \
graphdata.c0graphics['1086'] = graphdata.c0graphics['1115'] = (
  None,      (0x2554,), (0x2557,), (0x255A,), (0x255D,), (0x2551,), (0x2550,), (0xFFEC,),
  (0x25D8,), (0xFFEE,), (0x25D9,), (0x303F,), (0x2588,), (0x2592,), (0xFFED,), (0x263C,),
  (0x256C,), (0x2584,), (0x2195,), (0x203C,), (0x2593,), (0x2569,), (0x2566,), (0x2563,),
  None,      (0x2560,), (0x2591,), (0x21B5,), (0xFFEA,), (0xFFE8,), (0xFFEB,), (0xFFE9,),
    (0x2302,))

# Somewhat of a hybrid of the two above, used in Korean IBM code pages
graphdata.c0graphics['1088'] = graphdata.c0graphics['1126'] = (
  None,      (0x250C,), (0x2510,), (0x2514,), (0x2518,), (0x2502,), (0x2500,), (0x2022,),
  (0x25D8,), (0x25CB,), (0x25D9,), (0x2642,), (0x2640,), (0x266A,), (0x266B,), (0x263C,),
  (0x253C,), (0x25C4,), (0x2195,), (0x203C,), (0x00B6,), (0x2534,), (0x252C,), (0x2524,),
  (0x2191,), (0x251C,), (0x2192,), (0x2190,), (0x221F,), (0x2194,), (0x25B2,), (0x25BC,),
    (0x2302,))

# Modified OEM set of C0 graphics containing double-lined box drawing characters; used in some
#   Arabic-language code pages where there was otherwise only space for single-lined box drawing
graphdata.c0graphics["165"] = graphdata.c0graphics["864"] = graphdata.c0graphics["17248"] = \
graphdata.c0graphics["50016"] = (
  None,      (0x263A,), (0x266A,), (0x266B,), (0x263C,), (0x2550,), (0x2551,), (0x256C,),
  (0x2563,), (0x2566,), (0x2560,), (0x2569,), (0x2557,), (0x2554,), (0x255A,), (0x255D,),
  (0x25BA,), (0x25C4,), (0x2195,), (0x203C,), (0x00B6,), (0x00A7,), (0x25AC,), (0x21A8,),
  (0x2191,), (0x2193,), (0x2192,), (0x2190,), (0x221F,), (0x2194,), (0x25B2,), (0x25BC,),
    (0x2302,))

# Modified OEM set of C0 graphics containing single-lined box drawing characters, used in some
#   Arabic-language code pages where there was otherwise no space for any box drawing characters
graphdata.c0graphics['1127'] = (
  None,      (0x263A,), (0x2500,), (0x2502,), (0x253C,), (0x2524,), (0x252C,), (0x2022,),
  (0x25D8,), (0x25CB,), (0x25D9,), (0x2642,), (0x2640,), (0x266A,), (0x266B,), (0x263C,),
  (0x25BA,), (0x25C4,), (0x251C,), (0x2534,), (0x00B6,), (0x00A7,), (0x2510,), (0x250C,),
  (0x2191,), (0x2193,), (0x2192,), (0x2190,), (0x2514,), (0x2518,), (0x25B2,), (0x25BC,),
    (0x2302,))

# 0xabad1dea's C0 graphics for Windows-1252 on the Famicom
# See: https://github.com/0xabad1dea/0xabad1dea.github.com/blob/master/img/nes-ansi.png
graphdata.c0graphics["1252"] = graphdata.c0graphics["101252"] = (
  None,      (0x1F7E5,), (0x1F7E9,), (0x2588,), (0x1CD2A,), (0x1FB97,), (0x2592,), (0x2661,),
  (0x2662,), (0x2667,),  (0x2664,),  (0x263A,), (0x2639,),  (0x1D15E,), (0x266B,), (0x266A,),
  (0x2640,), (0x2642,),  (0x23FB,),  (0x24B6,), (0x24B7,),  (0x2191,),  (0x2193,), (0x2190,),
  (0x2192,), (0x254B,),  (0x2503,),  (0x2501,), (0x2595,),  (0x2594,),  (0x2581,), (0x258F,),
    (0x2302,))

# Optical Character Recognition deletion marks
graphdata.c0graphics['877'] = (
  None,      None, None, None, None, None, None, None,
  None,      None, None, None, None, None, None, None,
  None,      None, None, None, None, None, None, None,
  (0x2E3B,), None, None, None, None, None, None, None,
    (0x2588,))

# IBM's extension of Windows-1252 with additional diacritical marks in the C0 area
graphdata.c0graphics['1004'] = (
  None,      None, None,      None,      (0x00AF,), (0x02D8,), (0x02D9,), None,
  (0x02DA,), None, (0x02DD,), (0x02DB,), (0x02C7,), None,      None,      None,
  None,      None, None,      None,      None,      None,      None,      None,
  None,      None, None,      None,      None,      None,      None,      None,
    None)

# IBM's modification of OEM-850 with additional professional-typesetting characters in the C0 area
graphdata.c0graphics["1108"] = (
  None,      (0x263A,), (0xFB00,), (0xFB01,), (0xFB02,), (0xFB03,), (0xFB04,), (0x2022,),
  (0x2013,), (0x25CB,), (0x2020,), (0x2021,), (0x2122,), (0x2014,), (0x2018,), (0x2019,),
  (0x25BA,), (0x25C4,), (0x215B,), (0x215C,), (0x215D,), (0x2070,), (0x2074,), (0x2075,),
  (0x2191,), (0x2193,), (0x2192,), (0x2190,), (0x2076,), (0x2077,), (0x2078,), (0x2079,),
    (0x2302,))

# "User-defined" (i.e. Private Use Area) C0 replacements
graphdata.c0graphics["42"] = graphdata.c0graphics["?42"] = (
  (0xF000,), (0xF001,), (0xF002,), (0xF003,), (0xF004,), (0xF005,), (0xF006,), (0xF007,),
  (0xF008,), (0xF009,), (0xF00A,), (0xF00B,), (0xF00C,), (0xF00D,), (0xF00E,), (0xF00F,),
  (0xF010,), (0xF011,), (0xF012,), (0xF013,), (0xF014,), (0xF015,), (0xF016,), (0xF017,),
  (0xF018,), (0xF019,), (0xF01A,), (0xF01B,), (0xF01C,), (0xF01D,), (0xF01E,), (0xF01F,),
    (0xF07F,))

# Alternative representations of two characters in the DOS code page for IBM Symbols Set 7
graphdata.c0graphics["899"] = graphdata.c0graphics["1092"] = (
  None, None, None, None, None, None,      None, None,
  None, None, None, None, None, None,      None, None,
  None, None, None, None, None, (0x2085,), None, None,
  None, None, None, None, None, None,      None, None,
    (0x0020,))

# LaTeX C0 graphics
graphdata.c0graphics["996710"] = graphdata.c0graphics["996740"] = graphdata.c0graphics["996219"] = \
graphdata.c0graphics["996742"] = graphdata.c0graphics["996812"] = graphdata.c0graphics["996819"] = \
graphdata.c0graphics["996824"] = ( # "OT1" and charsets supplementing it
  (0x0393,), (0x0394,), (0x0398,), (0x039B,), (0x039E,), (0x03A0,), (0x03A3,), (0x03D2,),
  (0x03A6,), (0x03A8,), (0x03A9,), (0xFB00,), (0xFB01,), (0xFB02,), (0xFB03,), (0xFB04,),
  (0x0131,), (0x0237,), (0x0060,), (0x00B4,), (0x02C7,), (0x02D8,), (0x00AF,), (0x02DA,),
  (0x00B8,), (0x00DF,), (0x00E6,), (0x0153,), (0x00F8,), (0x00C6,), (0x0152,), (0x00D8,),
    (0x00A8,))
graphdata.c0graphics["996320"] = ( # "X2"
  (0x02CB,), (0x00B4,), (0x02C6,),        (0x02DC,), (0x00A8,), (0x02DD,), (0x02DA,), (0x02C7,),
  (0x02D8,), (0x00AF,), (0x02D9,),        (0x00B8,), (0x02DB,), (0x04C0,), (0x2329,), (0x232A,),
  (0x201C,), (0x201D,), (0x2007, 0x0311), (0x02F5,), (0x02D8,), (0x2013,), (0x2014,), (0x200B,),
  (0xFF61,), (0x02CE,), (0x02CF,), (0x2007, 0x0335), (0xA7D8,), (0xA7D9,), (0x0528,), (0x0529,),
    (0x00AD,))
graphdata.c0graphics["996741"] = ( # "OT4" variant
  (0x03B1,), (0x2206,),            (0x03B2,), (0x03B4,), (0x03C0,), (0x03A0,), (0x03A3,), (0x00B5,),
  (0x2026,), (0x66, 0x200D, 0x6B), (0x2126,), (0xFB00,), (0xFB01,), (0xFB02,), (0xFB03,), (0xFB04,),
  (0x0131,), (0x0237,),            (0x0060,), (0x00B4,), (0x02C7,), (0x02D8,), (0x00AF,), (0x02DA,),
  (0x00B8,), (0x00DF,),            (0x00E6,), (0x0153,), (0x00F8,), (0x00C6,), (0x0152,), (0x00D8,),
    (0x00A8,))
graphdata.c0graphics["101257"] = graphdata.c0graphics["996110"] = graphdata.c0graphics["996111"] = \
graphdata.c0graphics["996112"] = ( # "T1" (Cork) and others using the same C0 replacements
  (0x02CB,), (0x00B4,), (0x02C6,), (0x02DC,), (0x00A8,), (0x02DD,), (0x02DA,), (0x02C7,),
  (0x02D8,), (0x00AF,), (0x02D9,), (0x00B8,), (0x02DB,), (0x201A,), (0x2039,), (0x203A,),
  (0x201C,), (0x201D,), (0x201E,), (0x00AB,), (0x00BB,), (0x2013,), (0x2014,), (0x200B,),
  (0xFF61,), (0x0131,), (0x0237,), (0xFB00,), (0xFB01,), (0xFB02,), (0xFB03,), (0xFB04,),
    (0x00AD,))
graphdata.c0graphics["60643"] = graphdata.c0graphics["996121"] = graphdata.c0graphics["996122"] = \
graphdata.c0graphics["996123"] = ( # "T2" (FreeDOS code page 60643 is LaTeX "T2A")
  (0x02CB,), (0x00B4,), (0x02C6,),        (0x02DC,), (0x00A8,), (0x02DD,), (0x02DA,), (0x02C7,),
  (0x02D8,), (0x00AF,), (0x02D9,),        (0x00B8,), (0x02DB,), (0x04C0,), (0x2329,), (0x232A,),
  (0x201C,), (0x201D,), (0x2007, 0x0311), (0x02F5,), (0x02D8,), (0x2013,), (0x2014,), (0x200B,),
  (0xFF61,), (0x0131,), (0x0237,),        (0xFB00,), (0xFB01,), (0xFB02,), (0xFB03,), (0xFB04,),
    (0x00AD,))
graphdata.c0graphics["996150"] = ( # "T5"
  (0x02CB,), (0x00B4,), (0x02C6,), (0x02DC,), (0x00A8,), (0x2007, 0x0323), (0x02DA,), (0x02C7,),
  (0x02D8,), (0x00AF,), (0x02D9,), (0x00B8,), (0x2007, 0x0309), (0x201A,), (0x2039,), (0x203A,),
  (0x201C,), (0x201D,), (0x201E,), (0x00AB,), (0x00BB,),        (0x2013,), (0x2014,), (0x200B,),
  (0xFF61,), (0x0131,), (0x1EF6,), (0x1EF7,), (0x1EF4,),        (0x1EF5,), (0x0110,), (0x0111,),
    (0x00AD,))
graphdata.c0graphics["996210"] = ( # "TS1"
  (0x0060,), (0x00B4,), (0x02C6,), (0x02DC,), (0x00A8,), (0x02DD,), (0x02DA,), (0x02C7,),
  (0x02D8,), (0x00AF,), (0x02D9,), (0x00B8,), (0x02DB,), (0x02CC,), None,      None,
  None,      None,      (0x201E,), None,      None,      (0x2015,), (0x2014,), None,
  (0x2190,), (0x2192,), (0x2007, 0x0311), (0x2322,), (0x2007, 0x0311), (0x2007, 0x0311), None, None,
    (0x30A0,))
graphdata.c0graphics["300819"] = (
  (0x005E,), (0x007E,), (0x0160,), (0x017D,), (0x0161,), (0x017E,), (0x0178,), (0x2122,),
  (0x0027,), (0x20AC,), None,      None,      None,      None,      None,      None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
    (0x2302,))
graphdata.c0graphics["201252"] = ( # "LY1"
  None,      (0x20AC,), None,      None,      (0x2044,), (0x02D9,), (0x02DD,), (0x02DB,),
  (0xFB02,), None,      (0x200B,), (0xFB00,), (0xFB01,), None,      (0xFB03,), (0xFB04,),
  (0x0131,), (0x0237,), (0x0060,), (0x00B4,), (0x02C7,), (0x02D8,), (0x00AF,), (0x02DA,),
  (0x00B8,), (0x00DF,), (0x00E6,), (0x0153,), (0x00F8,), (0x00C6,), (0x0152,), (0x00D8,),
    (0x00A8,))
graphdata.c0graphics["301252"] = ( # "TeX Base1"
  None,      (0x02D9,), (0xFB01,), (0xFB02,), (0x2044,), (0x02DD,), (0x0141,), (0x0142,),
  (0x02DB,), (0x02DA,), None,      (0x02D8,), (0x2212,), None,      (0x017D,), (0x017E,),
  (0x02C7,), (0x0131,), (0x0237,), (0xFB00,), (0xFB03,), (0xFB04,), (0x2260,), (0x221E,),
  (0x2264,), (0x2265,), (0x2202,), (0x2211,), (0x220F,), (0x03C0,), (0x0060,), (0x0027,),
    (0x2302,))
graphdata.c0graphics["101276"] = (
  (0x017D,), (0x017E,), (0x0237,), (0xFB00,), (0xFB03,), (0xFB04,), (0x2122,), (0x0178,),
  (0x0160,), (0x0161,), (0x00A6,), (0x00A9,), (0x00AC,), (0x00AE,), (0x00B0,), (0x00B1,),
  (0x00B2,), (0x00B3,), (0x00B5,), (0x00B9,), (0x00BC,), (0x00BD,), (0x00BE,), None,
  None,      None,      None,      None,      None,      None,      None,      None,
    (0x00C0,))
graphdata.c0graphics["201276"] = (
  (0x0104,), (0x0118,), (0x012E,), (0x0136,), (0x013B,), (0x013D,), (0x0145,), (0x0156,),
  (0x0218,), (0x015E,), (0x021A,), (0x0172,), None,      None,      None,      None,
  (0x0105,), (0x0119,), (0x012F,), (0x0137,), (0x013C,), (0x013E,), (0x0146,), (0x0157,),
  (0x0219,), (0x015F,), (0x021B,), (0x0173,), None,      None,      None,      None,
    (0x00AD,))
graphdata.c0graphics["999901"] = ( # LaTeX "Storm" charset
  (0x2212,), (0x00B9,), (0x00B2,), (0x00B3,), (0x2264,),  (0x2260,), (0x2265,), (0x00B1,),
  (0x00BC,), (0x00BD,), (0x00BE,), (0x2044,), (0x00B0,),  (0x00A6,), None,      None,
  (0x2211,), (0x2126,), (0x03C0,), (0x00B5,), (0x2206,),  None,      None,      None,
  (0x00AC,), (0x221E,), (0x221A,), None,      (0x1F34E,), (0x00AA,), (0x00BA,), None,
    (0x00B7,))
graphdata.c0graphics["999902"] = ( # LaTeX "dvips" charset
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, (0x0027,), (0x00A1,), (0x00BF,),
  (0x0131,), (0x0237,), (0x0060,), (0x00B4,), (0x02C7,), (0x02D8,), (0x00AF,), (0x02DA,),
  (0x00B8,), (0x00DF,), (0x00E6,), (0x0153,), (0x00F8,), (0x00C6,), (0x0152,), (0x00D8,),
    (0x00A8,))
graphdata.c0graphics["999903"] = ( # LaTeX "LGR" (full Greek with diacritics) charset
  (0x2013,), (0x2007, 0x032F), (0x10144,), (0x10145,), (0x10146,), (0x10147,), (0x03DB,), (0x0377,),
  (0x03B9,), (0x1FBC,),        (0x1FCC,),  (0x1FFC,),  (0x0391,),  (0x03AB,),  (0x03B1,), (0x03CB,),
  (0x02CF,), (0x02CE,),     (0x03DF,), (0x03D9,), (0x2007, 0x032E), (0x03D8,), (0x03DA,), (0x03E0,),
  (0x20AC,), (0x2030,),        (0x0259,),  (0x03E1,),  (0x2018,),  (0x2019,),  (0x02D8,), (0x00AF,),
    (0x2014,))

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
graphdata.c0graphics["1285"] = graphdata.c0graphics["1286"] = (
  None,      None,      (0x2B72,), (0x2B70,), (0x2324,), (0x21E7,), (0x2303,), (0x2325,),
  None,      (0x2423,), (0x2326,), (0x2B90,), (0x2B91,), None,      None,      (0x1F589,),
  (0x2B6D,), (0x2318,), (0x2713,), (0x25C6,), (0xF8FF,), None,      None,      (0x232B,),
  (0x2B6A,), (0x2B6B,), (0x2B6C,), (0x238B,), (0x2327,), None,      None,      None,
    None)
# Version attested in Chicago.ttf (not ChicagoFLF.ttf). Though U+2398 is an approximate mapping.
graphdata.c0graphics["10000"] = graphdata.c0graphics["10004"] = graphdata.c0graphics["10005"] = \
graphdata.c0graphics["10006"] = graphdata.c0graphics["10081"] = graphdata.c0graphics["10029"] = \
graphdata.c0graphics["10017"] = graphdata.c0graphics["10007"] = graphdata.c0graphics["10082"] = \
graphdata.c0graphics["10010"] = graphdata.c0graphics["10079"] = graphdata.c0graphics["10021"] = (
  None,             (0x2325,), (0x2303,), (0x2324,), (0x21E7,), (0x21EA,), (0x238B,), (0x2423,),
  (0x232B,),        None,      (0x2B72,), (0x2B92,), (0x2398,), None,      (0x2B90,), (0x237D,),
  (0xF8FF, 0xF87A), (0x2318,), (0x2713,), (0x2666,), (0xF8FF,), (0x2326,), (0x2B70,), (0x2B91,),
  (0x2B93,),        None,      None,      None,      None,      None,      None,      None,
    None)





