#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2024, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Vietnamese Roman (quo^'c ngu*~) encodings

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

graphdata.gsets["ibmvietnamese"] = (96, 1, ((160,), (161,), (162,), (163,), (164,), (165,), (166,), (167,), (339,), (169,), (170,), (171,), (172,), (173,), (174,), (175,), (176,), (177,), (178,), (179,), (376,), (181,), (182,), (183,), (338,), (185,), (186,), (187,), (188,), (189,), (190,), (191,), (192,), (193,), (194,), (258,), (196,), (197,), (198,), (199,), (200,), (201,), (202,), (203,), (768,), (205,), (206,), (207,), (272,), (209,), (777,), (211,), (212,), (416,), (214,), (215,), (216,), (217,), (218,), (219,), (220,), (431,), (771,), (223,), (224,), (225,), (226,), (259,), (228,), (229,), (230,), (231,), (232,), (233,), (234,), (235,), (769,), (237,), (238,), (239,), (273,), (241,), (803,), (243,), (244,), (417,), (246,), (247,), (248,), (249,), (250,), (251,), (252,), (432,), (8363,), (255,)))
graphdata.chcpdocs['1129'] = 'ecma-35'
graphdata.defgsets['1129'] = ('ir006', 'ibmvietnamese', 'nil', 'nil')

graphdata.gsets["ibmvietnamese/euro"] = (96, 1, ((160,), (161,), (162,), (163,), (8364,), (165,), (166,), (167,), (339,), (169,), (170,), (171,), (172,), (173,), (174,), (175,), (176,), (177,), (178,), (179,), (376,), (181,), (182,), (183,), (338,), (185,), (186,), (187,), (188,), (189,), (190,), (191,), (192,), (193,), (194,), (258,), (196,), (197,), (198,), (199,), (200,), (201,), (202,), (203,), (768,), (205,), (206,), (207,), (272,), (209,), (777,), (211,), (212,), (416,), (214,), (215,), (216,), (217,), (218,), (219,), (220,), (431,), (771,), (223,), (224,), (225,), (226,), (259,), (228,), (229,), (230,), (231,), (232,), (233,), (234,), (235,), (769,), (237,), (238,), (239,), (273,), (241,), (803,), (243,), (244,), (417,), (246,), (247,), (248,), (249,), (250,), (251,), (252,), (432,), (8363,), (255,)))
graphdata.chcpdocs['1163'] = 'ecma-35'
graphdata.defgsets['1163'] = ('ir006', 'ibmvietnamese/euro', 'nil', 'nil')

# Windows-1258
graphdata.rhses["1258"] = parsers.read_single_byte("WHATWG/index-windows-1258.txt")
graphdata.defgsets["1258"] = ("ir006", "ibmvietnamese/euro", "nil", "nil")

# VPS
graphdata.rhses["997000"] = parsers.read_mozilla_ut_file("Mozilla/vps.ut")
graphdata.c0graphics["997000"] = parsers.read_mozilla_ut_file("Mozilla/vps.ut", typ="CL33")

# TCVN (TCVN 5712, VSCII; not VISCII)
graphdata.rhses["997001"] = parsers.read_mozilla_ut_file("Mozilla/tcvn5712.ut")
graphdata.c0graphics["997001"] = parsers.read_mozilla_ut_file("Mozilla/tcvn5712.ut", typ="CL33")
graphdata.gsets["ir180"] = (96, 1, parsers.read_mozilla_ut_file("Mozilla/tcvn5712.ut", typ="GR96"))
graphdata.defgsets["997001"] = ("ir006", "ir180", "nil", "nil")

# VISCII (not VSCII)
graphdata.rhses["997002"] = parsers.read_mozilla_ut_file("Mozilla/viscii.ut")
graphdata.c0graphics["997002"] = parsers.read_mozilla_ut_file("Mozilla/viscii.ut", typ="CL33")

# LaTeX "T5" encoding
graphdata.rhses["996150"] = (
  (0x00C0,), (0x00C1,), (0x00C3,), (0x1EA2,), (0x1EA0,), (0x00C2,), (0x1EA6,), (0x1EA4,),
  (0x1EAA,), (0x1EA8,), (0x1EAC,), (0x0102,), (0x1EB0,), (0x1EAE,), (0x1EB4,), (0x1EB2,),
  (0x1EB6,), (0x00C8,), (0x00C9,), (0x1EBC,), (0x1EBA,), (0x1EB8,), (0x00CA,), (0x1EC0,),
  (0x1EBE,), (0x1EC4,), (0x1EC2,), (0x1EC6,), (0x00CC,), (0x00CD,), (0x0128,), (0x1EC8,),
  (0x00E0,), (0x00E1,), (0x00E3,), (0x1EA3,), (0x1EA1,), (0x00E2,), (0x1EA7,), (0x1EA5,),
  (0x1EAB,), (0x1EA9,), (0x1EAD,), (0x0103,), (0x1EB1,), (0x1EAF,), (0x1EB5,), (0x1EB3,),
  (0x1EB7,), (0x00E8,), (0x00E9,), (0x1EBD,), (0x1EBB,), (0x1EB9,), (0x00EA,), (0x1EC1,),
  (0x1EBF,), (0x1EC5,), (0x1EC3,), (0x1EC7,), (0x00EC,), (0x00ED,), (0x0129,), (0x1EC9,),
  (0x1ECA,), (0x00D2,), (0x00D3,), (0x00D5,), (0x1ECE,), (0x1ECC,), (0x00D4,), (0x1ED2,),
  (0x1ED0,), (0x1ED6,), (0x1ED4,), (0x1ED8,), (0x01A0,), (0x1EDC,), (0x1EDA,), (0x1EE0,),
  (0x1EDE,), (0x1EE2,), (0x00D9,), (0x00DA,), (0x0168,), (0x1EE6,), (0x1EE4,), (0x01AF,),
  (0x1EEA,), (0x1EE8,), (0x1EEE,), (0x1EEC,), (0x1EF0,), (0x1EF2,), (0x00DD,), (0x1EF8,),
  (0x1ECB,), (0x00F2,), (0x00F3,), (0x00F5,), (0x1ECF,), (0x1ECD,), (0x00F4,), (0x1ED3,),
  (0x1ED1,), (0x1ED7,), (0x1ED5,), (0x1ED9,), (0x01A1,), (0x1EDD,), (0x1EDB,), (0x1EE1,),
  (0x1EDF,), (0x1EE3,), (0x00F9,), (0x00FA,), (0x0169,), (0x1EE7,), (0x1EE5,), (0x01B0,),
  (0x1EEB,), (0x1EE9,), (0x1EEF,), (0x1EED,), (0x1EF1,), (0x1EF3,), (0x00FD,), (0x1EF9,))
graphdata.defgsets["996150"] = ("ir006/smartquotes", "nil", "nil", "nil")

# TODO: VNI, VNI-Mac, VNI-DOS


