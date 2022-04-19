#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# TODO: ir059 (CODAR-U Arabic)

# ASMO-449 7-bit Arabic
graphdata.gsets["ir089"] = (94, 1, tuple((i,) if i else None for i in (
                     0x21,   0x22,   0x23,   0x00A4, 0x25,   0x26,   0x27, 
             0x0029, 0x0028, 0x2A,   0x2B,   0x060C, 0x2D,   0x2E,   0x2F, 
             0x30,   0x31,   0x32,   0x33,   0x34,   0x35,   0x36,   0x37, 
             0x38,   0x39,   0x3A,   0x061B, 0x003E, 0x3D,   0x003C, 0x061F, 
             0x40,   0x0621, 0x0622, 0x0623, 0x0624, 0x0625, 0x0626, 0x0627, 
             0x0628, 0x0629, 0x062A, 0x062B, 0x062C, 0x062D, 0x062E, 0x062F, 
             0x0630, 0x0631, 0x0632, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 
             0x0638, 0x0639, 0x063A, 0x005D, 0x5C,   0x005B, 0x5E,   0x5F, 
             0x0640, 0x0641, 0x0642, 0x0643, 0x0644, 0x0645, 0x0646, 0x0647, 
             0x0648, 0x0649, 0x064A, 0x064B, 0x064C, 0x064D, 0x064E, 0x064F, 
             0x0650, 0x0651, 0x0652, None,   None,   None,   None,   None, 
             None,   None,   None,   0x007D, 0x7C,   0x007B, 0x203E)))

# ASMO-708 ECMA-114 ISO-8859-6 Latin/Arabic RHS
graphdata.gsets["ir127"] = (96, 1, tuple((i,) if i else None for i in (
             0x00A0, None,   None,   None,   0x00A4, None,   None,   None, 
             None,   None,   None,   None,   0x060C, 0x00AD, None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   0x061B, None,   None,   None,   0x061F, 
             None,   0x0621, 0x0622, 0x0623, 0x0624, 0x0625, 0x0626, 0x0627, 
             0x0628, 0x0629, 0x062A, 0x062B, 0x062C, 0x062D, 0x062E, 0x062F, 
             0x0630, 0x0631, 0x0632, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 
             0x0638, 0x0639, 0x063A, None,   None,   None,   None,   None, 
             0x0640, 0x0641, 0x0642, 0x0643, 0x0644, 0x0645, 0x0646, 0x0647, 
             0x0648, 0x0649, 0x064A, 0x064B, 0x064C, 0x064D, 0x064E, 0x064F, 
             0x0650, 0x0651, 0x0652, None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None)))

# ECMA-121:1987 ISO-8859-8:1988 Latin/Hebrew RHS
graphdata.gsets["ir138"] = (96, 1, tuple((i,) if i else None for i in (
             0x00A0, None,   0x00A2, 0x00A3, 0x00A4, 0x00A5, 0x00A6, 0x00A7, 
             0x00A8, 0x00A9, 0x00D7, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x00AF, 
             0x00B0, 0x00B1, 0x00B2, 0x00B3, 0x00B4, 0x00B5, 0x00B6, 0x00B7, 
             0x00B8, 0x00B9, 0x00F7, 0x00BB, 0x00BC, 0x00BD, 0x00BE, None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   0x2017, 
             0x05D0, 0x05D1, 0x05D2, 0x05D3, 0x05D4, 0x05D5, 0x05D6, 0x05D7, 
             0x05D8, 0x05D9, 0x05DA, 0x05DB, 0x05DC, 0x05DD, 0x05DE, 0x05DF, 
             0x05E0, 0x05E1, 0x05E2, 0x05E3, 0x05E4, 0x05E5, 0x05E6, 0x05E7, 
             0x05E8, 0x05E9, 0x05EA, None,   None,   None,   None,   None)))

# CCITT Hebrew (pretty much ISO-8859-8 RHS but letters only)
# Registered as a 96-set for some reason but doesn't actually allocate the corners.
graphdata.gsets["ir164"] = (96, 1, tuple((i,) if i else None for i in (
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             0x05D0, 0x05D1, 0x05D2, 0x05D3, 0x05D4, 0x05D5, 0x05D6, 0x05D7, 
             0x05D8, 0x05D9, 0x05DA, 0x05DB, 0x05DC, 0x05DD, 0x05DE, 0x05DF, 
             0x05E0, 0x05E1, 0x05E2, 0x05E3, 0x05E4, 0x05E5, 0x05E6, 0x05E7, 
             0x05E8, 0x05E9, 0x05EA, None,   None,   None,   None,   None)))

# Extended version of ASMO-708/ISO-8859-6 to also support French and German, RHS
graphdata.gsets["ir167"] = (96, 1, (
    (0xA0,),   None,      None,      None,      (0xA4,),   None,      None,      None, 
    (0xC8,),   (0xC9,),   (0xCA,),   (0xCB,),   (0x060C,), (0xAD,),   (0xCE,),   (0xCF,), 
    (0xC0,),   (0xC2,),   (0xE2,),   (0xC4,),   (0xDF,),   (0xE4,),   (0xC7,),   (0xE7,), 
    (0xE8,),   (0xE9,),   (0xEA,),   (0x061B,), (0xEB,),   (0xEE,),   (0xEF,),   (0x061F,), 
    (0xE0,),   (0x0621,), (0x0622,), (0x0623,), (0x0624,), (0x0625,), (0x0626,), (0x0627,), 
    (0x0628,), (0x0629,), (0x062A,), (0x062B,), (0x062C,), (0x062D,), (0x062E,), (0x062F,), 
    (0x0630,), (0x0631,), (0x0632,), (0x0633,), (0x0634,), (0x0635,), (0x0636,), (0x0637,), 
    (0x0638,), (0x0639,), (0x063A,), (0xD4,),   (0xD6,),   (0xDA,),   (0xDB,),   (0xDC,), 
    (0x0640,), (0x0641,), (0x0642,), (0x0643,), (0x0644,), (0x0645,), (0x0646,), (0x0647,), 
    (0x0648,), (0x0649,), (0x064A,), (0x064B,), (0x064C,), (0x064D,), (0x064E,), (0x064F,), 
    (0x0650,), (0x0651,), (0x0652,), None,      None,      None,      None,      None, 
    None,      None,      None,      (0xF4,),   (0xF6,),   (0xFA,),   (0xFB,),   (0xFC,),
))

# ECMA-121:2000 ISO-8859-8:1999 Latin/Hebrew RHS
graphdata.gsets["ir198"] = (96, 1, tuple((i,) if i else None for i in (
             0x00A0, None,   0x00A2, 0x00A3, 0x00A4, 0x00A5, 0x00A6, 0x00A7, 
             0x00A8, 0x00A9, 0x00D7, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x00AF, 
             0x00B0, 0x00B1, 0x00B2, 0x00B3, 0x00B4, 0x00B5, 0x00B6, 0x00B7, 
             0x00B8, 0x00B9, 0x00F7, 0x00BB, 0x00BC, 0x00BD, 0x00BE, None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   0x2017, 
             0x05D0, 0x05D1, 0x05D2, 0x05D3, 0x05D4, 0x05D5, 0x05D6, 0x05D7, 
             0x05D8, 0x05D9, 0x05DA, 0x05DB, 0x05DC, 0x05DD, 0x05DE, 0x05DF, 
             0x05E0, 0x05E1, 0x05E2, 0x05E3, 0x05E4, 0x05E5, 0x05E6, 0x05E7, 
             0x05E8, 0x05E9, 0x05EA, None,   None,   0x200E, 0x200F, None)))

# SI-1311:2002 Latin/Hebrew RHS
graphdata.gsets["ir234"] = (96, 1, tuple((i,) if i else None for i in (
             0x00A0, None,   0x00A2, 0x00A3, 0x00A4, 0x00A5, 0x00A6, 0x00A7, 
             0x00A8, 0x00A9, 0x00D7, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x00AF, 
             0x00B0, 0x00B1, 0x00B2, 0x00B3, 0x00B4, 0x00B5, 0x00B6, 0x00B7, 
             0x00B8, 0x00B9, 0x00F7, 0x00BB, 0x00BC, 0x00BD, 0x00BE, None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   0x20AC, 0x20AA, 0x202D, 0x202E, 0x202C, None,   0x2017, 
             0x05D0, 0x05D1, 0x05D2, 0x05D3, 0x05D4, 0x05D5, 0x05D6, 0x05D7, 
             0x05D8, 0x05D9, 0x05DA, 0x05DB, 0x05DC, 0x05DD, 0x05DE, 0x05DF, 
             0x05E0, 0x05E1, 0x05E2, 0x05E3, 0x05E4, 0x05E5, 0x05E6, 0x05E7, 
             0x05E8, 0x05E9, 0x05EA, None,   None,   0x200E, 0x200F, None)))

# Windows code pages
graphdata.rhses["1255"] = parsers.read_single_byte("WHATWG/index-windows-1255.txt") # Hebrew
graphdata.rhses["1256"] = parsers.read_single_byte("WHATWG/index-windows-1256.txt") # Arabic

# OEM code pages
graphdata.rhses["720"] = parsers.read_single_byte("ICU/ibm-720_P100-1997.ucm") # Arabic
graphdata.rhses["862"] = parsers.read_single_byte("ICU/ibm-862_P100-1995.ucm") # Hebrew
graphdata.rhses["864"] = parsers.read_single_byte("ICU/ibm-864_X110-1999.ucm") # Arabic

# Macintosh code pages (both seem to have only Microsoft IDs?)
graphdata.rhses["10004"] = parsers.read_mozilla_ut_file("Mozilla/macarabic.ut")
graphdata.rhses["10005"] = parsers.read_mozilla_ut_file("Mozilla/machebrew.ut")



