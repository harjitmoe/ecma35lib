#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2024.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Vietnamese Roman (quo^'c ngu*~) encodings

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

graphdata.gsets["ibmvietnamese"] = (96, 1, ((160,), (161,), (162,), (163,), (164,), (165,), (166,), (167,), (339,), (169,), (170,), (171,), (172,), (173,), (174,), (175,), (176,), (177,), (178,), (179,), (376,), (181,), (182,), (183,), (338,), (185,), (186,), (187,), (188,), (189,), (190,), (191,), (192,), (193,), (194,), (258,), (196,), (197,), (198,), (199,), (200,), (201,), (202,), (203,), (768,), (205,), (206,), (207,), (272,), (209,), (777,), (211,), (212,), (416,), (214,), (215,), (216,), (217,), (218,), (219,), (220,), (431,), (771,), (223,), (224,), (225,), (226,), (259,), (228,), (229,), (230,), (231,), (232,), (233,), (234,), (235,), (769,), (237,), (238,), (239,), (273,), (241,), (803,), (243,), (244,), (417,), (246,), (247,), (248,), (249,), (250,), (251,), (252,), (432,), (8363,), (255,)))

graphdata.gsets["ibmvietnamese/euro"] = (96, 1, ((160,), (161,), (162,), (163,), (8364,), (165,), (166,), (167,), (339,), (169,), (170,), (171,), (172,), (173,), (174,), (175,), (176,), (177,), (178,), (179,), (376,), (181,), (182,), (183,), (338,), (185,), (186,), (187,), (188,), (189,), (190,), (191,), (192,), (193,), (194,), (258,), (196,), (197,), (198,), (199,), (200,), (201,), (202,), (203,), (768,), (205,), (206,), (207,), (272,), (209,), (777,), (211,), (212,), (416,), (214,), (215,), (216,), (217,), (218,), (219,), (220,), (431,), (771,), (223,), (224,), (225,), (226,), (259,), (228,), (229,), (230,), (231,), (232,), (233,), (234,), (235,), (769,), (237,), (238,), (239,), (273,), (241,), (803,), (243,), (244,), (417,), (246,), (247,), (248,), (249,), (250,), (251,), (252,), (432,), (8363,), (255,)))

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

# TODO: VNI, VNI-Mac, VNI-DOS


