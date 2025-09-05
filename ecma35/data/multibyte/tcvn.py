#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, shutil
from ecma35.data import graphdata, variationhints
from ecma35.data.multibyte import mbmapparsers as parsers

tcvn5773 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/ChuwxNoom/TCVN5773.txt"),
    "TCVN5773.txt",
    skip_invalid_kuten=False)

graphdata.gsets["tcvn5773"] = (94, 2, tcvn5773)

tcvn6056 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/ChuwxNoom/TCVN6056.txt"),
    "TCVN6056.txt",
    skip_invalid_kuten=False)

graphdata.gsets["tcvn6056"] = (94, 2, tcvn6056)

pseudo_tcvn6056 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/ChuwxNoom/V1_OLD.txt"),
    "V1_OLD.txt",
    skip_invalid_kuten=False)

graphdata.gsets["pseudo-tcvn6056"] = (94, 2, pseudo_tcvn6056)

vhn01 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/ChuwxNoom/VHN01.txt"),
    "VHN01.txt",
    skip_invalid_kuten=False)

graphdata.gsets["vhn01-row-minus-19"] = (94, 2, vhn01[94*19:94*113])

graphdata.gsets["tcvn5773/extended"] = (94, 2, parsers.fuse([
    tcvn5773, tcvn6056, vhn01[:94*94],
], "TCVN5773_TCVN6056.json"))

_vhn01_in_style_of_sjis = {parsers._sjis_xkt_to_mkt((n // 94) + 1, (n % 94) + 1): i for n, i in enumerate(vhn01)}
vhn01_in_style_of_sjis_plane_2 = tuple(_vhn01_in_style_of_sjis.get((2, (n // 94) + 1, (n % 94) + 1), None) for n in range(94*94))

vhn02 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/ChuwxNoom/VHN02.txt"),
    "VHN02.txt",
    skip_invalid_kuten=False)

graphdata.gsets["vhn02"] = (94, 2, vhn02)

vhn03 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/ChuwxNoom/VHN03.txt"),
    "VHN03.txt",
    skip_invalid_kuten=False)

graphdata.gsets["vhn03"] = (94, 2, vhn03)

graphdata.gsets["vhn02/extended"] = (94, 2, parsers.fuse([
    vhn01_in_style_of_sjis_plane_2, vhn02, vhn03,
], "VHN02_extended.json"))

