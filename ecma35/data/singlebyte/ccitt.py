#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# ITU T.51 RHS, ETS 300 706 version
_t51 =  [  (0x00A1,), (0x00A2,), (0x00A3,), (0x0024,), (0x00A5,), (0x0023,), (0x00A7,), 
(0x00A4,), (0x2018,), (0x201C,), (0x00AB,), (0x2190,), (0x2191,), (0x2192,), (0x2193,), 
(0x00B0,), (0x00B1,), (0x00B2,), (0x00B3,), (0x00D7,), (0x00B5,), (0x00B6,), (0x00B7,), 
(0x00F7,), (0x2019,), (0x201D,), (0x00BB,), (0x00BC,), (0x00BD,), (0x00BE,), (0x00BF,), 
(0x00A0,), (-0x300,), (-0x301,), (-0x302,), (-0x303,), (-0x304,), (-0x306,), (-0x307,), 
(-0x308,), (-0x323,), (-0x30A,), (-0x327,), (-0x332,), (-0x30B,), (-0x328,), (-0x30C,), 
(0x2500,), (0x00B9,), (0x00AE,), (0x00A9,), (0x2122,), (0x266A,), (0x20A0,), (0x2030,),
(0x03B1,), None,      None,      None,      (0x215B,), (0x215C,), (0x215D,), (0x215E,), 
(0x03A9,), (0x00C6,), (0x00D0,), (0x00AA,), (0x0126,), None,      (0x0132,), (0x013F,), 
(0x0141,), (0x00D8,), (0x0152,), (0x00BA,), (0x00DE,), (0x0166,), (0x014A,), (0x0149,), 
(0x0138,), (0x00E6,), (0x0111,), (0x00F0,), (0x0127,), (0x0131,), (0x0133,), (0x0140,), 
(0x0142,), (0x00F8,), (0x0153,), (0x00DF,), (0x00FE,), (0x0167,), (0x014B,)]
graphdata.gsets["ir090-ets-alpha"] = (94, 1, tuple(_t51))
# I'll be honest, the ETS glyph for so-called U+03B1 in the Latin G2 set does not match
#   the U+03B1 in the Greek G0 set, so I'm VERY skeptical about whether ETS really treats
#   them as the same character when their charts font clearly doesn't.
# U+221D seems like a more appropriate mapping.
_t51[55] = (0x221D,)
graphdata.gsets["ir090-ets"] = (94, 1, tuple(_t51))

# ITU T.51 RHS, vanilla old version
_t51[31] = _t51[40] = _t51[53] = _t51[54] = _t51[55] = None
graphdata.gsets["ir090"] = (94, 1, tuple(_t51))

# ITU T.101 Data Syntax 2 G2 set
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
graphdata.gsets["ir142-ir156"] = (96, 1, tuple(_t51))

# TODO: ir152 (T.51 minus Latin-1 thru Latin-9 repertoires, which exists for some reason)
# TODO: ir099, 
# TODO: ir071/173 (Mosaics)



