#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020, 2022, 2024.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# SNIMA (Morocco) CODAR-U 7-bit Arabic
graphdata.gsets["ir059"] = (94, 1, (
               (0x21,),   (0x22,),   (0x23,),   (0xA4,),   (0x25,),   (0x26,),   (0x27,),
    (0x28,),   (0x29,),   (0x2A,),   (0x2B,),   (0x060C,), (0x2D,),   (0x2E,),   (0x2F,),
    (0x30,),   (0x31,),   (0x32,),   (0x33,),   (0x34,),   (0x35,),   (0x36,),   (0x37,),
    (0x38,),   (0x39,),   (0x3A,),   (0x061B,), (0x3C,),   (0x3D,),   (0x3E,),   (0x061F,),
    (0x40,),          (0xFE7D, 0x064E), (0xFE7C, 0x064E), (0xFE7D, 0x064F),
    (0xFE7C, 0x064F), (0xFE77, 0x0651), (0xFE76, 0x0651), (0xFE77,),
    (0xFE76,), (0xFE70,), (0xFE79,), (0xFE78,), (0xFE72,), (0xFE7B,), (0xFE7A,), (0xFE74,),
    (0xFE7F,), (0xFE7E,), (0xFE7D,), (0xFE7C,), (0x0623,), (0x0622,), (0x0624,), (0xFE8A,),
    (0x0626,), (0x0625,), (0xFEF2,), (0x067E,), (0x06A4,), (0x06AF,), (0x0621,), (0x0627,),
    (0x0628,), (0x062A,), (0x0629,), (0x062B,), (0x062C,), (0x062D,), (0x062E,), (0x062F,),
    (0x0630,), (0x0631,), (0x0632,), (0x0633,), (0x0634,), (0x0635,), (0x0636,), (0x0637,),
    (0x0638,), (0x0639,), (0x063A,), (0x0641,), (0x0642,), (0x0643,), (0x0644,), (0x0645,),
    (0x0646,), (0x0647,), (0x0648,), (0x064A,), (0x7C,),   (0x0649,), (0xAC,),
))

# ASMO-449 ISO-9036 7-bit Arabic. TODO: does this use diacritic re-ordering? MARC 21 does, but
#   8-bit derivatives of the ASMO-449 layout do not (neither MacArabic nor ASMO-708).
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

# MARC 21 "Basic Arabic", basically a modified IR-089 although it uses a private-use escape (it
#   uses `ESC ( 3` in MARC-8). Note that MARC-8 explicitly uses prefix diacritics, and explicitly 
#   requires them to be re-ordered when transcoded to/from Unicode.
graphdata.gsets["ir089/marc"] = (94, 1, tuple((i,) if i else None for i in (
                     0x0021, 0x0022, 0x0023, 0x0024, 0x066A, 0x0026, 0x0027, 
             0x0028, 0x0029, 0x066D, 0x002B, 0x060C, 0x002D, 0x002E, 0x002F, 
             0x0660, 0x0661, 0x0662, 0x0663, 0x0664, 0x0665, 0x0666, 0x0667, 
             0x0668, 0x0669, 0x003A, 0x061B, 0x003C, 0x003D, 0x003E, 0x061F, 
             None,   0x0621, 0x0622, 0x0623, 0x0624, 0x0625, 0x0626, 0x0627, 
             0x0628, 0x0629, 0x062A, 0x062B, 0x062C, 0x062D, 0x062E, 0x062F, 
             0x0630, 0x0631, 0x0632, 0x0633, 0x0634, 0x0635, 0x0636, 0x0637, 
             0x0638, 0x0639, 0x063A, 0x005B, None,   0x005D, None,   None, 
             0x0640, 0x0641, 0x0642, 0x0643, 0x0644, 0x0645, 0x0646, 0x0647, 
             0x0648, 0x0649, 0x064A, -0x064B, -0x064C, -0x064D, -0x064E, -0x064F, 
             -0x0650, -0x0651, -0x0652, 0x0671, 0x0670, None,   None,   None, 
             0x066C, 0x201D, 0x201C, None,   None,   None,   None)))

# MARC 21 "Basic Hebrew"
graphdata.gsets["marc-he"] = (94, 1, tuple((i,) if i else None for i in (
                     0x0021, 0x05F4, 0x0023, 0x0024, 0x0025, 0x0026, 0x05F3,
             0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x05BE, 0x002E, 0x002F,
             0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037,
             0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F,
             -0x05B7, -0x05B8, -0x05B6, -0x05B5, -0x05B4, -0x05B9, -0x05BB, -0x05B0,
             -0x05B2, -0x05B3, -0x05B1, -0x05BC, -0x05BF, -0x05C1, -0xFB1E, None,
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   0x005B, None,   0x005D, None,   None, 
             0x05D0, 0x05D1, 0x05D2, 0x05D3, 0x05D4, 0x05D5, 0x05D6, 0x05D7, 
             0x05D8, 0x05D9, 0x05DA, 0x05DB, 0x05DC, 0x05DD, 0x05DE, 0x05DF, 
             0x05E0, 0x05E1, 0x05E2, 0x05E3, 0x05E4, 0x05E5, 0x05E6, 0x05E7, 
             0x05E8, 0x05E9, 0x05EA, 0x05F0, 0x05F1, 0x05F2, None)))

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
graphdata.chcpdocs['1089'] = 'ecma-35'
graphdata.defgsets['1089'] = ('alt646/ibmarabic', 'ir127', 'nil', 'nil')

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
graphdata.chcpdocs['916'] = 'ecma-35'
graphdata.defgsets['916'] = ('ir006', 'ir138', 'nil', 'nil')

# DEC 8-bit Hebrew
graphdata.gsets["ir138/dec"] = (94, 1, tuple((i,) if i else None for i in (
                     0x00A1, 0x00A2, 0x00A3, None,   0x00A5, None,   0x00A7, 
             0x00A4, 0x00A9, 0x00AA, 0x00AB, None,   None,   None,   None, 
             0x00B0, 0x00B1, 0x00B2, 0x00B3, None,   0x00B5, 0x00B6, 0x00B7, 
             None,   0x00B9, 0x00BA, 0x00BB, 0x00BC, 0x00BD, None,   0x00BF, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             None,   None,   None,   None,   None,   None,   None,   None, 
             0x05D0, 0x05D1, 0x05D2, 0x05D3, 0x05D4, 0x05D5, 0x05D6, 0x05D7, 
             0x05D8, 0x05D9, 0x05DA, 0x05DB, 0x05DC, 0x05DD, 0x05DE, 0x05DF, 
             0x05E0, 0x05E1, 0x05E2, 0x05E3, 0x05E4, 0x05E5, 0x05E6, 0x05E7, 
             0x05E8, 0x05E9, 0x05EA, None,   None,   None,   None)))

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
graphdata.chcpdocs['5012'] = 'ecma-35'
graphdata.defgsets['5012'] = ('ir006', 'ir198', 'nil', 'nil')

# ISO-11822:1996 (a supplement for use with ASMO-449 / ISO-9036)
# Not assigned an escape, but given the number here (possibly provisionally, but any new escape or
#   IR number being assigned in the future seems unlikely since ISO-IR is basically legacy now):
#   https://www.evertype.com/standards/iso10646/pdf/iso-11822.pdf
# Note: that linked document lists a mapping to U+06C9 ۉ despite the glyph shown being clearly a
#   U+06CB ۋ, not a ۉ. The Library of Congress (as part of MARC-8) maps it appropriately to U+06CB.
graphdata.gsets["ir224"] = (94, 1, (
               (0x06FD,), (0x0672,), (0x0673,), (0x0679,), (0x067A,), (0x067B,), (0x067C,),
    (0x067D,), (0x067E,), (0x067F,), (0x0680,), (0x0681,), (0x0682,), (0x0683,), (0x0684,),
    (0x0685,), (0x0686,), (0x06BF,), (0x0687,), (0x0688,), (0x0689,), (0x068A,), (0x068B,),
    (0x068C,), (0x068D,), (0x068E,), (0x068F,), (0x0690,), (0x0691,), (0x0692,), (0x0693,),
    (0x0694,), (0x0695,), (0x0696,), (0x0697,), (0x0698,), (0x0699,), (0x069A,), (0x069B,),
    (0x069C,), (0x06FA,), (0x069D,), (0x069E,), (0x06FB,), (0x069F,), (0x06A0,), (0x06FC,),
    (0x06A1,), (0x06A2,), (0x06A3,), (0x06A4,), (0x06A5,), (0x06A6,), (0x06A7,), (0x06A8,),
    (0x06A9,), (0x06AA,), (0x06AB,), (0x06AC,), (0x06AD,), (0x06AE,), (0x06AF,), (0x06B0,),
    (0x06B1,), (0x06B2,), (0x06B3,), (0x06B4,), (0x06B5,), (0x06B6,), (0x06B7,), (0x06B8,),
    (0x06BA,), (0x06BB,), (0x06BC,), (0x06BD,), (0x06B9,), (0x06BE,), (0x06C0,), (0x06C4,),
    (0x06C5,), (0x06C6,), (0x06CA,), (0x06CB,), (0x06CD,), (0x06CE,), (0x06D0,), (0x06D2,),
    (0x06D3,), None,      None,      None,      None,      (0x0306,), (0x030C,),
))

# MARC 21 "Extended Arabic" (i.e. ISO-11822:1996; uses private use `ESC ( 4` in MARC). Since I'm
#   (tentatively) not using diacritic re-ordering for ir089 and ir224 while MARC-8 *does*, I'm
#   including this as a separate variant even though I'm using effectively the same mapping.
graphdata.gsets["ir224/marc"] = (94, 1, tuple((i,) if i else None for i in (
                     0x06FD, 0x0672, 0x0673, 0x0679, 0x067A, 0x067B, 0x067C, 
             0x067D, 0x067E, 0x067F, 0x0680, 0x0681, 0x0682, 0x0683, 0x0684, 
             0x0685, 0x0686, 0x06BF, 0x0687, 0x0688, 0x0689, 0x068A, 0x068B, 
             0x068C, 0x068D, 0x068E, 0x068F, 0x0690, 0x0691, 0x0692, 0x0693, 
             0x0694, 0x0695, 0x0696, 0x0697, 0x0698, 0x0699, 0x069A, 0x069B, 
             0x069C, 0x06FA, 0x069D, 0x069E, 0x06FB, 0x069F, 0x06A0, 0x06FC, 
             0x06A1, 0x06A2, 0x06A3, 0x06A4, 0x06A5, 0x06A6, 0x06A7, 0x06A8, 
             0x06A9, 0x06AA, 0x06AB, 0x06AC, 0x06AD, 0x06AE, 0x06AF, 0x06B0, 
             0x06B1, 0x06B2, 0x06B3, 0x06B4, 0x06B5, 0x06B6, 0x06B7, 0x06B8, 
             0x06BA, 0x06BB, 0x06BC, 0x06BD, 0x06B9, 0x06BE, 0x06C0, 0x06C4, 
             0x06C5, 0x06C6, 0x06CA, 0x06CB, 0x06CD, 0x06CE, 0x06D0, 0x06D2, 
             0x06D3, None, None, None, None, -0x0306, -0x030C)))

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
             0x05E8, 0x05E9, 0x05EA, 0x202A, 0x202B, 0x200E, 0x200F, None)))

# SI-960 7-bit Hebrew
graphdata.gsets["hebrew7"] = (94, 1, ((0x21,), (0x22,), (0x23,), (0x24,), (0x25,), (0x26,), (0x27,), (0x28,), (0x29,), (0x2A,), (0x2B,), (0x2C,), (0x2D,), (0x2E,), (0x2F,), (0x30,), (0x31,), (0x32,), (0x33,), (0x34,), (0x35,), (0x36,), (0x37,), (0x38,), (0x39,), (0x3A,), (0x3B,), (0x3C,), (0x3D,), (0x3E,), (0x3F,), (0x40,), (0x41,), (0x42,), (0x43,), (0x44,), (0x45,), (0x46,), (0x47,), (0x48,), (0x49,), (0x4A,), (0x4B,), (0x4C,), (0x4D,), (0x4E,), (0x4F,), (0x50,), (0x51,), (0x52,), (0x53,), (0x54,), (0x55,), (0x56,), (0x57,), (0x58,), (0x59,), (0x5A,), (0x5B,), (0x5C,), (0x5D,), (0x5E,), (0x5F,), (0x05D0,), (0x05D1,), (0x05D2,), (0x05D3,), (0x05D4,), (0x05D5,), (0x05D6,), (0x05D7,), (0x05D8,), (0x05D9,), (0x05DA,), (0x05DB,), (0x05DC,), (0x05DD,), (0x05DE,), (0x05DF,), (0x05E0,), (0x05E1,), (0x05E2,), (0x05E3,), (0x05E4,), (0x05E5,), (0x05E6,), (0x05E7,), (0x05E8,), (0x05E9,), (0x05EA,), (0x7B,), (0x7C,), (0x7D,), (0x7E,)))

# Corresponding G0 set to EBCDIC code page 803
graphdata.gsets["ibmhebrew7"] = (94, 1, ((124,), (34,), (35,), (1500, 8205, 1524, 8205, 1497), (37,), (1488,), (39,), (40,), (41,), (42,), (43,), (44,), (45,), (46,), (47,), (48,), (49,), (50,), (51,), (52,), (53,), (54,), (55,), (56,), (57,), (58,), (59,), (60,), (61,), (62,), (63,), (64,), (65,), (66,), (67,), (68,), (69,), (70,), (71,), (72,), (73,), (74,), (75,), (76,), (77,), (78,), (79,), (80,), (81,), (82,), (83,), (84,), (85,), (86,), (87,), (88,), (89,), (90,), (36,), None, (33,), (172,), (95,), None, (1489,), (1490,), (1491,), (1492,), (1493,), (1494,), (1495,), (1496,), (1497,), (1498,), (1499,), (1500,), (1501,), (1502,), (1503,), (1504,), (1505,), (1506,), (1507,), (1508,), (1509,), (1510,), (1511,), (1512,), (1513,), (1514,), None, None, None, None))

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


graphdata.gsets["ibmurdu"] = (96, 1, ((160,), (1776,), (1777,), (1778,), (1779,), (1780,), (1781,), (1782,), (1783,), (1784,), (1785,), (1548,), (1563,), (173,), (1567,), (65153,), (65165,), (65166,), (1575,), (65167,), (65169,), (64342,), (64344,), (65171,), (65173,), (65175,), (64358,), (64360,), (65177,), (65179,), (65181,), (65183,), (64378,), (64380,), (65185,), (65187,), (65189,), (65191,), (65193,), (64392,), (65195,), (65197,), (64396,), (65199,), (64394,), (65201,), (65203,), (65205,), (65207,), (65209,), (65211,), (65213,), (65215,), (65219,), (65223,), (65225,), (65226,), (65227,), (65228,), (65229,), (65230,), (65231,), (65232,), (65233,), (65235,), (65237,), (65239,), (64398,), (65243,), (64402,), (64404,), (65245,), (65247,), (65248,), (65249,), (65251,), (64414,), (65253,), (65255,), (65157,), (65261,), (64422,), (64424,), (64425,), (64426,), (65152,), (65161,), (65162,), (65163,), (64508,), (64509,), (64510,), (64432,), (64430,), (65148,), (65149,)))
graphdata.chcpdocs['1006'] = 'ecma-35'
graphdata.defgsets['1006'] = ('alt646/ibmarabic', 'ibmurdu', 'nil', 'nil')

graphdata.gsets["ibmarabic"] = (96, 1, ((160,), (1548,), (162,), (1563,), (1567,), (65148,), (166,), (65149,), (1600,), (65139,), (65152,), (65153,), (172,), (173,), (65154,), (65155,), (1632,), (1633,), (1634,), (1635,), (1636,), (1637,), (1638,), (1639,), (1640,), (1641,), (65156,), (65157,), (65163,), (65165,), (65166,), (65167,), (65169,), (65171,), (65173,), (65175,), (65177,), (65179,), (65181,), (65183,), (65185,), (65187,), (65189,), (65191,), (65193,), (65195,), (65197,), (65199,), (1587,), (65203,), (1588,), (65207,), (1589,), (65211,), (1590,), (215,), (65215,), (65219,), (65223,), (65225,), (65226,), (65227,), (65228,), (65229,), (65230,), (65231,), (65232,), (65233,), (65235,), (65237,), (65239,), (65241,), (65243,), (65245,), (65269,), (65270,), (65271,), (65272,), (65275,), (65276,), (65247,), (65249,), (65251,), (65253,), (65255,), (65257,), (65259,), (247,), (65260,), (65261,), (65263,), (65264,), (65265,), (65266,), (65267,), None))
graphdata.chcpdocs['1008'] = 'ecma-35'
graphdata.defgsets['1008'] = ('alt646/ibmarabic', 'ibmarabic', 'nil', 'nil')

graphdata.gsets["ibmaix-arabic/isoextended"] = (96, 1, ((160,), (1570,), (1571,), (1573,), (164,), (65163,), (1575,), (65169,), (65175,), (65179,), (65183,), (65187,), (1548,), (173,), (65191,), (65203,), (1632,), (1633,), (1634,), (1635,), (1636,), (1637,), (1638,), (1639,), (1640,), (1641,), (65207,), (1563,), (65211,), (65215,), (65226,), (1567,), (65227,), (65152,), (65154,), (65156,), (65157,), (65160,), (1574,), (65166,), (65167,), (65171,), (65173,), (65177,), (65181,), (65185,), (65189,), (65193,), (65195,), (65197,), (65199,), (65201,), (65205,), (65209,), (65213,), (65219,), (65223,), (65225,), (65229,), (65228,), (65230,), (65231,), (65232,), (65235,), (1600,), (65233,), (65237,), (65241,), (65245,), (65249,), (65253,), (65257,), (65261,), (65264,), (1610,), (65136,), (65138,), (65140,), (65142,), (65144,), (65146,), (65148,), (65150,), (65239,), (65243,), (65247,), (65251,), (65255,), (65259,), (65267,), (65143,), (65145,), (65147,), (65149,), (65151,), None))
graphdata.chcpdocs['1029'] = 'ecma-35'
graphdata.defgsets['1029'] = ('alt646/ibmarabic', 'ibmaix-arabic/isoextended', 'nil', 'nil')

graphdata.gsets["ibmarabic/euro"] = (96, 1, ((160,), (1548,), (162,), (1563,), (1567,), (65148,), (166,), (65149,), (1600,), (65139,), (65152,), (65153,), (172,), (173,), (65154,), (65155,), (1632,), (1633,), (1634,), (1635,), (1636,), (1637,), (1638,), (1639,), (1640,), (1641,), (65156,), (65157,), (65163,), (65165,), (65166,), (65167,), (65169,), (65171,), (65173,), (65175,), (65177,), (65179,), (65181,), (65183,), (65185,), (65187,), (65189,), (65191,), (65193,), (65195,), (65197,), (65199,), (1587,), (65203,), (1588,), (65207,), (1589,), (65211,), (1590,), (215,), (65215,), (65219,), (65223,), (65225,), (65226,), (65227,), (65228,), (65229,), (65230,), (65231,), (65232,), (65233,), (65235,), (65237,), (65239,), (65241,), (65243,), (65245,), (65269,), (65270,), (65271,), (65272,), (65275,), (65276,), (65247,), (65249,), (65251,), (65253,), (65255,), (65257,), (65259,), (247,), (65260,), (65261,), (65263,), (65264,), (65265,), (65266,), (65267,), (8364,)))
graphdata.chcpdocs['5104'] = 'ecma-35'
graphdata.defgsets['5104'] = ('alt646/ibmarabic', 'ibmarabic/euro', 'nil', 'nil')

graphdata.gsets["ibmaix-arabic/base"] = (96, 1, ((160,), None, None, None, (164,), None, None, None, None, None, None, None, (1548,), (173,), None, None, None, None, None, None, None, None, None, None, None, None, None, (1563,), None, None, None, (1567,), None, (1569,), (1570,), (1571,), (1572,), (1573,), (65161,), (1575,), (1576,), (1577,), (1578,), (1579,), (1580,), (1581,), (1582,), (1583,), (1584,), (1585,), (1586,), (1587,), (1588,), (1589,), (1590,), (1591,), (1592,), (1593,), (1594,), None, None, None, None, None, (1600,), (1601,), (1602,), (1603,), (1604,), (1605,), (1606,), (1607,), (1608,), (1609,), (1610,), (1611,), (1612,), (1613,), (1614,), (1615,), (1616,), (1617,), (1618,), None, None, None, None, None, None, None, None, None, None, None, None, None))
graphdata.chcpdocs['5142'] = 'ecma-35'
graphdata.defgsets['5142'] = ('alt646/ibmarabic', 'ibmaix-arabic/base', 'nil', 'nil')

graphdata.gsets["ibmpc-arabic/small"] = (96, 1, ((160,), (173,), None, (163,), (164,), None, None, None, None, None, None, None, (1548,), None, None, None, (1632,), (1633,), (1634,), (1635,), (1636,), (1637,), (1638,), (1639,), (1640,), (1641,), None, (1563,), None, None, None, (1567,), (162,), (1569,), (1570,), (1571,), (1572,), None, (1574,), (1575,), (1576,), (1577,), (1578,), (1579,), (1580,), (1581,), (1582,), (1583,), (1584,), (1585,), (1586,), (1587,), (1588,), (1589,), (1590,), (1591,), (1592,), (1593,), (1594,), (166,), (172,), (247,), (215,), None, (1600,), (1601,), (1602,), (1603,), (1604,), (1605,), (1606,), (1607,), (1608,), (1609,), (1610,), None, None, None, None, None, None, (1617,), None, None, None, None, None, None, None, None, None, None, None, None, None, None))
graphdata.chcpdocs['9056'] = 'ecma-35'
graphdata.defgsets['9056'] = ('alt646/ibmarabic', 'ibmpc-arabic/small', 'nil', 'nil')

graphdata.gsets["ibmpc-arabic/tiny"] = (96, 1, ((160,), (173,), None, None, None, None, None, None, None, (1576,), (1578,), (1579,), (1548,), (1580,), (1581,), (1582,), None, None, None, None, None, None, None, None, None, None, (1601,), (1563,), (1587,), (1588,), (1589,), (1567,), (162,), (1569,), (1570,), (1571,), (1572,), None, (1574,), (1575,), None, (1577,), None, None, None, None, None, (1583,), (1584,), (1585,), (1586,), None, None, None, None, (1591,), (1592,), None, None, (166,), (172,), (247,), (215,), (1593,), (1600,), None, None, None, None, None, None, None, (1608,), (1609,), None, (1590,), None, None, (1594,), (1605,), None, (1617,), (1606,), (1607,), None, None, None, None, (1602,), None, None, (1604,), (1603,), (1610,), None, None))
graphdata.chcpdocs['13152'] = 'ecma-35'
graphdata.defgsets['13152'] = ('alt646/ibmarabic/tiny', 'ibmpc-arabic/tiny', 'nil', 'nil')

graphdata.gsets["ibmpc-arabic/base"] = (96, 1, tuple(i or j for i, j in zip(graphdata.gsets["ibmpc-arabic/small"][2], graphdata.gsets["ibmpc-arabic/tiny"][2])))


