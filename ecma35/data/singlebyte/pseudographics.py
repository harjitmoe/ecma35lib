#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019–2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# Scope of this file is sets whose primary purpose is the provision of pseudographic characters, to
#   the extent that they are difficult to classify as otherwise providing script support.

# DEC Special Graphics ("DECGraphics")
graphdata.gsets["decgraphics"] = (94, 1, tuple((i,) if i else None for i in (
                    0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 
            0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x002D, 0x002E, 0x002F, 
            0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, 
            0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F, 
            0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 
            0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F, 
            0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, 
            0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x00A0, 
            0x25C6, 0x2592, 0x2409, 0x240C, 0x240D, 0x240A, 0x00B0, 0x00B1, 
            0x2424, 0x240B, 0x2518, 0x2510, 0x250C, 0x2514, 0x253C, 0x23BA, 
            0x23BB, 0x2500, 0x23BC, 0x23BD, 0x251C, 0x2524, 0x2534, 0x252C, 
            0x2502, 0x2264, 0x2265, 0x03C0, 0x2260, 0x00A3, 0x2219)))
graphdata.chcpdocs['1090'] = 'ecma-35'
graphdata.defgsets['1090'] = ('decgraphics', 'nil', 'nil', 'nil')

# Modified DEC Special Graphics
# As seen in e.g.: https://commons.wikimedia.org/wiki/File:Shift_In_and_Shift_out_on_Linux.png
graphdata.gsets["decgraphics/modified"] = (94, 1, tuple((i,) if i else None for i in (
                    0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 
            0x0028, 0x0029, 0x002A, 0x2192, 0x2190, 0x2191, 0x2193, 0x002F, 
            0x2588, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, 
            0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F, 
            0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 
            0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F, 
            0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, 
            0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x00A0, 
            0x0060, 0x2592, 0x0062, 0x0063, 0x0064, 0x0065, 0x00B0, 0x00B1, 
            0x2591, 0x0069, 0x2518, 0x2510, 0x250C, 0x2514, 0x253C, 0x006F, 
            0x0070, 0x2500, 0x0072, 0x0073, 0x251C, 0x2524, 0x2534, 0x252C, 
            0x2502, 0x2264, 0x2265, 0x03C0, 0x2260, 0x00A3, 0x2219)))

# Compromise between the above two
graphdata.gsets["decgraphics/composite"] = (94, 1, tuple((i,) if i else None for i in (
                    0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 
            0x0028, 0x0029, 0x002A, 0x2192, 0x2190, 0x2191, 0x2193, 0x002F, 
            0x2588, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, 
            0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F, 
            0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 
            0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F, 
            0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, 
            0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x00A0, 
            0x25C6, 0x2592, 0x2409, 0x240C, 0x240D, 0x240A, 0x00B0, 0x00B1, 
            0x2591, 0x240B, 0x2518, 0x2510, 0x250C, 0x2514, 0x253C, 0x23BA, 
            0x23BB, 0x2500, 0x23BC, 0x23BD, 0x251C, 0x2524, 0x2534, 0x252C, 
            0x2502, 0x2264, 0x2265, 0x03C0, 0x2260, 0x00A3, 0x2219)))

# DEC Special Graphics for VT52 as opposed to VT100
graphdata.gsets["decgraphicsold"] = (94, 1,
            tuple((i,) if i else None for i in range(0x21, 0x5E)) +
            ((0x2007,), (0x00A0,), None, (0x2588,),
             (0x215F,), (0x00B3, 0x2044), (0x2075, 0x2044), (0x2077, 0x2044),
             (0x00B0,), (0x00B1,), (0x2192,), (0x2026,), (0x00F7,), (0x2193,),
             (0x2594,), (0x1FB76,), (0x1FB77,), (0x1FB78,),
             (0x1FB79,), (0x1FB7A,), (0x1FB7B,), (0x2581,),
             (0x2080,), (0x2081,), (0x2082,), (0x2083,), (0x2084,),
             (0x2085,), (0x2086,), (0x2087,), (0x2088,), (0x2089,),
             (0x00B6,)))

# ARIB STD-B24 Volume 1 Mosaic Set A, ITU T.101-B (Videotex Data Syntax 1) Mosaic Set 2
_ir071 = ((0x1FB00,), (0x1FB01,), (0x1FB02,), (0x1FB03,), (0x1FB04,), (0x1FB05,), (0x1FB06,), (0x1FB07,), (0x1FB08,), (0x1FB09,), (0x1FB0A,), (0x1FB0B,), (0x1FB0C,), (0x1FB0D,), (0x1FB0E,), (0x1FB0F,), (0x1FB10,), (0x1FB11,), (0x1FB12,), (0x1FB13,), (0x258C,), (0x1FB14,), (0x1FB15,), (0x1FB16,), (0x1FB17,), (0x1FB18,), (0x1FB19,), (0x1FB1A,), (0x1FB1B,), (0x1FB1C,), (0x1FB1D,), (0x1FB3C,), (0x1FB3D,), (0x1FB3E,), (0x1FB3F,), (0x1FB40,), (0x25E3,), (0x1FB41,), (0x1FB42,), (0x1FB43,), (0x1FB44,), (0x1FB45,), (0x1FB46,), (0x1FB68,), (0x1FB69,), (0x1FB70,), (0x1FB95,), (0x1FB47,), (0x1FB48,), (0x1FB49,), (0x1FB4A,), (0x1FB4B,), (0x25E2,), (0x1FB4C,), (0x1FB4D,), (0x1FB4E,), (0x1FB4F,), (0x1FB50,), (0x1FB51,), (0x1FB6A,), (0x1FB6B,), (0x1FB75,), (0x2588,), (0x1FB1E,), (0x1FB1F,), (0x1FB20,), (0x1FB21,), (0x1FB22,), (0x1FB23,), (0x1FB24,), (0x1FB25,), (0x1FB26,), (0x1FB27,), (0x2590,), (0x1FB28,), (0x1FB29,), (0x1FB2A,), (0x1FB2B,), (0x1FB2C,), (0x1FB2D,), (0x1FB2E,), (0x1FB2F,), (0x1FB30,), (0x1FB31,), (0x1FB32,), (0x1FB33,), (0x1FB34,), (0x1FB35,), (0x1FB36,), (0x1FB37,), (0x1FB38,), (0x1FB39,), (0x1FB3A,), (0x1FB3B,))
graphdata.gsets["ir071"] = (94, 1, _ir071)

# ITU T.101-C (Videotex Data Syntax 2) Mosaic Set 1
graphdata.gsets["t101c-mosaic1"] = (96, 1, 
    ((0xA0,),) +
    _ir071[:31] +
    tuple((i,) for i in range(0x40, 0x5B)) +
    ((0x2190,), (0xBD,), (0x2192,), (0x2191,), (0x2317,)) +
    _ir071[-31:] +
    ((0x2588,),))

# ITU T.101-C (Videotex Data Syntax 2) Mosaic Set 3
_ir173 = [(0x2528,), (0x2512,), (0x2511,), (0x251A,), (0x2519,), (0x2520,), (0x2538,), (0x2530,), (0x2516,), (0x2515,), (0x250D,), (0x250E,), (0x2542,), (0x25A6,), (0x258C,), (0x2503,), (0x2501,), (0x250F,), (0x2513,), (0x2517,), (0x251B,), (0x2523,), (0x252B,), (0x2533,), (0x253B,), (0x254B,), (0x2580,), (0x2584,), (0x2588,), (0x25AA,), (0x2590,), (0x2537,), (0x252F,), (0x251D,), (0x2525,), (0x1FBA4,), (0x1FBA5,), (0x1FBA6,), (0x1FBA7,), (0x1FBA0,), (0x1FBA1,), (0x1FBA2,), (0x1FBA3,), (0x253F,), (0x2022,), (0x25CF,), (0x25CB,), (0x2502,), (0x2500,), (0x250C,), (0x2510,), (0x2514,), (0x2518,), (0x251C,), (0x2524,), (0x252C,), (0x2534,), (0x253C,), (0x2192,), (0x2190,), (0x2191,), (0x2193,), (0x2591,), (0x1FB52,), (0x1FB53,), (0x1FB54,), (0x1FB55,), (0x1FB56,), (0x25E5,), (0x1FB57,), (0x1FB58,), (0x1FB59,), (0x1FB5A,), (0x1FB5B,), (0x1FB5C,), (0x1FB6C,), (0x1FB6D,), (0x2592,), (0x2593,), (0x1FB5D,), (0x1FB5E,), (0x1FB5F,), (0x1FB60,), (0x1FB61,), (0x25E4,), (0x1FB62,), (0x1FB63,), (0x1FB64,), (0x1FB65,), (0x1FB66,), (0x1FB67,), (0x1FB6E,), (0x1FB6F,), (0x25A6, 0xF87F)]
graphdata.gsets["ir173"] = (94, 1, tuple(_ir173))
_ir072 = _ir173[:]
_ir072[:31] = (None,) * 31
_ir072[62] = _ir072[77] = _ir072[78] = _ir072[93] = None
graphdata.gsets["ir072"] = (94, 1, tuple(_ir072))

# ARIB STD-B24 Volume 1 Mosaic Set B, ITU T.101-B (Videotex Data Syntax 1) Mosaic Set 1
graphdata.gsets["ir137"] = (94, 1, ((0x2596,), (0x25AA,), (0x1CE47,), (0x259F,), (0x259C, 0xF87F), (0x1FB63, 0xF87F), (0x25B6,), (0x1CC86, 0xF87F), (0x1F837,), (0x25C0, 0xF87A), (0x1F835, 0xF87A), (0x1FB9B,), (0x1FBE3,), (0x1FBEB,), (0x25D7, 0xF87A), 
(0x2584,), (0x2597,), (0x25AC,), (0x1CE50,), (0x2599,), (0x259B, 0xF87F), (0x1FB58, 0xF87F), (0x25C0,), (0x1CC87, 0xF87F), (0x1F835,), (0x25B6, 0xF87A), (0x1F837, 0xF87A), (0x1FB9A,), (0x1FBE1,), (0x1FBE9,), (0x25D6, 0xF87A),
None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (0x1FB52,), (0x1FB53,), (0x1FB54,), (0x1FB55,), (0x1FB56,), (0x25E5,), (0x1FB57,), (0x1FB58,), (0x1FB59,), (0x1FB5A,), (0x1FB5B,), (0x1FB5C,), (0x1FB6C,), (0x1FB6D,), None, None, (0x1FB5D,), (0x1FB5E,), (0x1FB5F,), (0x1FB60,), (0x1FB61,), (0x25E4,), (0x1FB62,), (0x1FB63,), (0x1FB64,), (0x1FB65,), (0x1FB66,), (0x1FB67,), (0x1FB6E,), (0x1FB6F,), None))

# ISO-10367's box drawing set
graphdata.gsets["ir155"] = (96, 1, (
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    (0x2503,), (0x2501,), (0x250F,), (0x2513,), (0x2517,), (0x251B,), (0x2523,), (0x252B,), 
    (0x2533,), (0x253B,), (0x254B,), (0x2580,), (0x2584,), (0x2588,), (0x25AA,), None,      
    (0x2502,), (0x2500,), (0x250C,), (0x2510,), (0x2514,), (0x2518,), (0x251C,), (0x2524,), 
    (0x252C,), (0x2534,), (0x253C,), (0x2591,), (0x2592,), (0x2593,), None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,
))
graphdata.gsets["ir155/94"] = (94, 1, graphdata.gsets["ir155"][2][1:-1])

# ARIB STD-B24 Volume 1 Mosaic Set C
graphdata.gsets["aribmosaic-c"] = (94, 1,
    tuple((i,) for i in range(0x1CE51, 0x1CE70)) +
    (None,) * 31 +
    ((0x1CE8F,),) +
    tuple((i,) for i in range(0x1CE70, 0x1CE8F)))

# TODO: ARIB STD-B24 Volume 1 Mosaic set D

# IBM code page 1109 "DITROFF Specials Compatibility", consisting mainly of pieces of tall bracket
graphdata.gsets["ibm-troff"] = (94, 1, ((9615,), (9146,), (9149,), (9148,), (9121,), (9123,), (9124,), (9126,), (9127,), (9128,), (9129,), (9131,), (9132,), (9133,), (9130,), (9633,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
graphdata.chcpdocs['1109'] = 'ecma-35'
graphdata.defgsets['1109'] = ('ibm-troff', 'nil', 'nil', 'nil')

# HP 2640 series terminal Line Drawing set; IBM code page 1056
graphdata.gsets["hplinedrawing"] = (94, 1, ((9504,), (9512,), (9519,), (9527,), (9567,), (9570,), (9572,), (9575,), (9553,), (9538,), (9535,), (9472,), (118295,), (9474,), (9532,), (9547,), (9507,), (9515,), (9523,), (9531,), (9500,), (9508,), (9516,), (9524,), (9552,), (9475,), (9473,), (9579,), (118294,), (9578,), (117826,), (9566,), (9495,), (9545,), (9608,), (9612,), (9615,), (9492,), (9496,), (118287,), (118292,), (118288,), (118289,), (118290,), (9543,), (9544,), (118293,), (118297,), (9487,), (9484,), (9499,), (9488,), (118291,), (9546,), (9491,), (9632,), (118296,), (9604,), (9569,), (9548,), (9576,), (118286,), (9573,), (9566,), (9495,), (9545,), (9608,), (9612,), (9615,), (9492,), (9496,), (118287,), (118292,), (118288,), (118289,), (118290,), (9543,), (9544,), (118293,), (118297,), (9487,), (9484,), (9499,), (9488,), (118291,), (9546,), (9491,), (9632,), (118296,), (9604,), (9569,), (9548,), (9576,), (118286,)))
graphdata.chcpdocs['1056'] = 'ecma-35'
graphdata.defgsets['1056'] = ('hplinedrawing', 'nil', 'nil', 'nil')

# Line Drawing subset from RHS of code page 437; IBM's code page 1055
graphdata.gsets["pclinedrawing"] = (94, 1, (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (9617,), (9618,), (9619,), (9474,), (9508,), (9569,), (9570,), (9558,), (9557,), (9571,), (9553,), (9559,), (9565,), (9564,), (9563,), (9488,), (9492,), (9524,), (9516,), (9500,), (9472,), (9532,), (9566,), (9567,), (9562,), (9556,), (9577,), (9574,), (9568,), (9552,), (9580,), (9575,), (9576,), (9572,), (9573,), (9561,), (9560,), (9554,), (9555,), (9579,), (9578,), (9496,), (9484,), (9608,), (9604,), (9612,), (9616,), (9600,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (8729,), (183,), None, None, None, (9632,)))
graphdata.chcpdocs['1055'] = 'ecma-35'
graphdata.defgsets['1055'] = ('pclinedrawing', 'nil', 'nil', 'nil')

# Line Drawing LCS (library character set) of the IBM 3800 laser printer
graphdata.gsets["ibm3800-linedrawing"] = (94, 1, (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (8282,), (9523,), (9531,), (9507,), (9515,), (9547,), (9473,), (9475,), (9550,), (9551,), None, None, None, None, None, None, None, (9484,), (9488,), (9496,), (9492,), (9516,), (9524,), (9500,), (9508,), (9532,), (9472,), (9474,), (9485,), (9489,), (9497,), (9493,), (9516, 63612), (9524, 63612), (9500, 63612), (9508, 63612), (9532, 63612), (9472, 63612), (65512, 63612), (9487,), (9491,), (9499,), (9495,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))

