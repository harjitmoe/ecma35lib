#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2022, 2024, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# Scope of this file is the ITU-T.61-based supplements and their further supplements, i.e. the
#   closely interrelated ITU T.51, ITU T.61, ITU T.101, DIN 31624, ISO 5426, ISO 6937, ETS 300 706,
#   excluding those in the scope of ecma6.py, greek.py, cyrillic.py, semitic.py, pseudographics.py

# ITU T.51 RHS, ETS 300 706 version
_t51 =  [  (0x00A1,), (0x00A2,), (0x00A3,), (0x0024,), (0x00A5,), (0x0023,), (0x00A7,), 
(0x00A4,), (0x2018,), (0x201C,), (0x00AB,), (0x2190,), (0x2191,), (0x2192,), (0x2193,), 
(0x00B0,), (0x00B1,), (0x00B2,), (0x00B3,), (0x00D7,), (0x00B5,), (0x00B6,), (0x00B7,), 
(0x00F7,), (0x2019,), (0x201D,), (0x00BB,), (0x00BC,), (0x00BD,), (0x00BE,), (0x00BF,), 
(0x00A0,), (-0x300,), (-0x301,), (-0x302,), (-0x303,), (-0x304,), (-0x306,), (-0x307,), 
(-0x308,), (-0x323,), (-0x30A,), (-0x327,), (-0x332,), (-0x30B,), (-0x328,), (-0x30C,),
# 0x2015 per WG3 N 454: http://open-std.org/JTC1/sc2/wg3/docs/n454.pdf
(0x2015,), (0x00B9,), (0x00AE,), (0x00A9,), (0x2122,), (0x266A,), (0x20A0,), (0x2030,),
(0x03B1,), None,      None,      None,      (0x215B,), (0x215C,), (0x215D,), (0x215E,), 
(0x03A9,), (0x00C6,), (0x00D0,), (0x00AA,), (0x0126,), None,      (0x0132,), (0x013F,), 
(0x0141,), (0x00D8,), (0x0152,), (0x00BA,), (0x00DE,), (0x0166,), (0x014A,), (0x0149,), 
(0x0138,), (0x00E6,), (0x0111,), (0x00F0,), (0x0127,), (0x0131,), (0x0133,), (0x0140,), 
(0x0142,), (0x00F8,), (0x0153,), (0x00DF,), (0x00FE,), (0x0167,), (0x014B,)]
graphdata.gsets["ir090/ets-alpha"] = (94, 1, tuple(_t51))
# I'll be honest, the ETS glyph for so-called U+03B1 in the Latin G2 set does not match
#   the U+03B1 in the Greek G0 set, so I'm VERY skeptical about whether ETS really treats
#   them as the same character when their charts font clearly doesn't.
# U+221D seems like a more appropriate mapping.
_t51[55] = (0x221D,)
graphdata.gsets["ir090/ets"] = (94, 1, tuple(_t51))

# ITU T.51 RHS, vanilla old version
_t51[31] = _t51[40] = _t51[53] = _t51[54] = _t51[55] = None
graphdata.gsets["ir090"] = (94, 1, tuple(_t51))

# ITU T.101-C (Videotex Data Syntax 2) G2 set
_ir70 = _t51[:]
_ir70[31] = (-0x0344,)
_ir70[40] = (-0x0308,)
graphdata.gsets["ir070"] = (94, 1, tuple(_ir70))

# ITU T.61 RHS
_t61 = _t51[:] # Make a copy
_t61[8] = _t61[9] = _t61[11] = _t61[12] = _t61[13] = _t61[14] = \
_t61[24] = _t61[25] = _t61[47] = _t61[48] = _t61[49] = _t61[50] = \
_t61[51] = _t61[52] = _t61[59] = _t61[60] = _t61[61] = _t61[62] = None
_t61[40] = (-0x0308,)
graphdata.gsets["ir103"] = (94, 1, tuple(_t61))
graphdata.chcpdocs['1036'] = 'ecma-35'
graphdata.defgsets['1036'] = ('ir102/strict', 'ir103', 'nil', 'nil')

# ITU T.51 RHS, new version (with additions to fully support the Latin-1/7 repertoire)
_t51.insert(0, (0xA0,))
_t51.append((0xAD,))
_t51[54] = ((0xAC,))
_t51[55] = ((0xA6,))
# 142 includes the dollar but not the universal currency, 156 includes the universal currency
#   but not the dollar, and neither includes the hash. All are included in T.51 itself, but
#   the dollar and hash are deprecated in favour of the ASCII characters except for
#   existing services.
_t51_142 = _t51[:]
_t51_142[6] = _t51_142[8] = None
_t51_156 = _t51[:]
_t51_156[4] = _t51_156[6] = None
graphdata.gsets["ir142"] = (96, 1, tuple(_t51_142))
graphdata.gsets["ir156"] = (96, 1, tuple(_t51_156))
graphdata.gsets["ir142+ir156"] = (96, 1, tuple(_t51))

# ISO 5426-1, bibliographic extended Latin, related to T.51 but moves a few diacritics, has much more diacritics, fewer base letters, different non-letters
_bibliot51 = _t51[1:-1]
_bibliot51[1] = (0x201E,)
_bibliot51[5] = (0x2020,)
_bibliot51[7] = (0x2032,)
_bibliot51[11] = (0x266D,)
_bibliot51[12] = (0x00A9,)
_bibliot51[13] = (0x2117,)
_bibliot51[14] = (0x00AE,)
_bibliot51[15] = (0x02BF,)
_bibliot51[16] = (0x02BE,)
_bibliot51[17] = (0x201A,)
_bibliot51[21] = (0x2021,)
_bibliot51[23] = (0x2033,)
_bibliot51[27] = (0x266F,)
_bibliot51[28] = (0x02B9,)
_bibliot51[29] = (0x02BA,)
_bibliot51[31] = (-0x0309,)
_bibliot51[40] = _t61[40]
_bibliot51[42] = (-0x0315,)
_bibliot51[43] = (-0x0312,)
_bibliot51[45] = (-0x031B,)
_bibliot51[47] = (-0x0327,)
_bibliot51[48] = (-0x031C,)
_bibliot51[49] = (-0x0326,)
_bibliot51[50] = (-0x0328,)
_bibliot51[51] = (-0x0325,)
_bibliot51[52] = (-0x032E,)
_bibliot51[53] = (-0x0323,)
_bibliot51[54] = (-0x0324,)
_bibliot51[55] = (-0x0332,)
_bibliot51[56] = (-0x0333,)
_bibliot51[57] = (-0x0329,)
_bibliot51[58] = (-0x032D,)
_bibliot51[60] = (-0xFE20,)
_bibliot51[61] = (-0xFE21,)
_bibliot51[62] = (-0xFE23,)
_megabibliot51 = _bibliot51[:]
_bibliot51[18] = _bibliot51[19] = _bibliot51[20] = _bibliot51[59] = _bibliot51[63] = _bibliot51[66] = _bibliot51[67] = _bibliot51[68] = _bibliot51[70] = _bibliot51[74] = _bibliot51[76] = _bibliot51[77] = _bibliot51[78] = _bibliot51[79] = _bibliot51[83] = _bibliot51[86] = _bibliot51[92] = _bibliot51[93] = None
graphdata.gsets["ir053"] = (94, 1, tuple(_bibliot51))
graphdata.gsets["ir053/ext"] = (94, 1, tuple(_megabibliot51))

# DIN 31624, related to ISO 5426-1 but avoids duplicating DIN 66003, lacks some chars that ISO 5426-1 has (adds?) including base letters, and includes ASCII chars that DIN 66003 lacks and an extra base letter.
_germanyt51 = _bibliot51[:]
_germanyt51[3] = (0x00A4,)
_germanyt51[4] = (0x2030,)
_germanyt51[6] = (0x0040,)
_germanyt51[7] = (0x00B0,)
_germanyt51[8] = (0x005B,)
_germanyt51[9] = (0x007B,)
_germanyt51[19] = (0x005C,)
_germanyt51[20] = (0x007C,)
_germanyt51[23] = (0x2192,)
_germanyt51[24] = (0x005D,)
_germanyt51[25] = (0x007D,)
_germanyt51[40] = (-0x0336,)
_germanyt51[90] = (0x01A6,)
_germanyt51[69] = _germanyt51[85] = None
graphdata.gsets["ir038"] = (94, 1, tuple(_germanyt51))
graphdata.gsets["ir038/ext"] = (94, 1, tuple(map(lambda a, b: a or b, _germanyt51, _megabibliot51)))

# ANSI X3.110:1983, CSA T500:1983, ITU T.101-D, FIPS PUB 121, NAPLPS, Videotex Data Syntax 3.
#   IR-099 is identical to IR-128; IR-128 is preferred.
_t51videotex3 = _t51[1:-1]
_t51videotex3[31] = (-0x20D1,)
_t51videotex3[40] = (-0x0338,)
_t51videotex3[53] = (0x2500,)
_t51videotex3[54] = (0x2502,)
_t51videotex3[55] = (0x2571,)
_t51videotex3[56] = (0x2572,)
_t51videotex3[57] = (0x25E2,)
_t51videotex3[58] = (0x25E3,)
_t51videotex3[68] = (0x253C,)
graphdata.gsets["ir099"] = graphdata.gsets["ir128"] = (94, 1, tuple(_t51videotex3))

# The "Adobe Standard" or "PostScript Standard" encoding, yet another encoding related to T.61.
graphdata.gsets["adobe-standard"] = (94, 1, ((161,), (162,), (163,), (8260,), (165,), (402,), (167,), (164,), (39,), (8220,), (171,), (8249,), (8250,), (64257,), (64258,), None, (8211,), (8224,), (8225,), (183,), None, (182,), (8226,), (8218,), (8222,), (8221,), (187,), (8230,), (8240,), None, (191,), None, (96,), (180,), (710,), (732,), (175,), (728,), (729,), (168,), None, (730,), (184,), None, (733,), (731,), (711,), (8212,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (198,), None, (170,), None, None, None, None, (321,), (216,), (338,), (186,), None, None, None, None, None, (230,), None, None, None, (305,), None, None, (322,), (248,), (339,), (223,), None, None, None))
graphdata.chcpdocs['1276'] = 'ecma-35'
graphdata.defgsets['1276'] = ('ir006/smartquotes', 'adobe-standard', 'nil', 'nil')

#######################################################
# FURTHER SUPPLEMENTS TO ITU-T.61-DERIVED SUPPLEMENTS #
#######################################################

# CENELEC supplement for characters listed in Annex A of T.51 but not in *any* of ISO-8859-1 thru 9.
#   Contrast IR-154.
_ir152 = [(i if n in (10, 12, 13, 14, 15, 26, 52, 53, 60, 61, 62, 63, 64, 70, 71, 74, 79, 86, 87, 90) else None) for n, i in enumerate(_t51)]
_ir152[76] = (0x0174,)
_ir152[77] = (0x0176,)
_ir152[78] = (0x0178,)
_ir152[92] = (0x0175,)
_ir152[93] = (0x0177,)
graphdata.gsets["ir152"] = (96, 1, tuple(_ir152))

# ISO 5426-2, supplement to ISO 5426-1 containing mainly mediæval scribal notation
graphdata.gsets["ir213"] = (94, 1, ((0x2215,), (0x273D,), (0x00B6,), (0x261E,), (0x204C,), (0x2619,), (0x2202,), None, (0x204A,), (0x1D97,), (0xA75D,), (0x2E39,), (0xA76F,), (0xA76D,), (0xA770,), None, (0x02B9,), (0x203B,), (0x204B,), (0x2720,), (0x204D,), (0x2767,), (0x213A,), None, (0x204A, 0x0334,), (0xA794,), (0x2183,), (0xA76B,), (0x1613,), (0xA75B,), None, (0x0313,), (0x1DE3,), (0x1DF1,), (0x1AB0,), (0x1DC8,), (0x0363,), (0x0364,), (0x030A,), (0x1DE6,), (0x0334,), (0x0335,), (0x0338,), (0x0337,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (0x01B7,), (0x01E4,), (0x0126,), (0x004B, 0x0315,), (0x014A,), (0xA752,), (0xA754,), (0xA750,), (0xA756,), (0x01A6,), (0x0166,), (0x01F7,), (0x021C,), (0xA759,), (0x017F,), None, (0x0292,), (0x01E5,), (0x0127,), (0x0138,), (0x014B,), (0xA753,), (0xA755,), (0xA751,), (0xA757,), (0x0280,), (0x0167,), (0x01BF,), (0x021D,), (0x0071, 0x200D, 0xA76B,), (0x017F, 0x200D, 0x0A6D)))



