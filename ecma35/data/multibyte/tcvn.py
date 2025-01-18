#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, shutil
from ecma35.data import graphdata, variationhints
from ecma35.data.multibyte import mbmapparsers as parsers

graphdata.gsets["tcvn5773"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/ChuwxNoom/TCVN5773.txt"),
        "TCVN5773.txt",
        skip_invalid_kuten=False))

graphdata.gsets["tcvn6056"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/ChuwxNoom/TCVN6056.txt"),
        "TCVN6056.txt",
        skip_invalid_kuten=False))

graphdata.gsets["pseudo-tcvn6056"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/ChuwxNoom/V1_OLD.txt"),
        "V1_OLD.txt",
        skip_invalid_kuten=False))

graphdata.gsets["vhn01-row-minus-19"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/ChuwxNoom/VHN01.txt"),
        "VHN01.txt",
        skip_invalid_kuten=False)[94*19:94*113])

graphdata.gsets["vhn02"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/ChuwxNoom/VHN02.txt"),
        "VHN02.txt",
        skip_invalid_kuten=False))

graphdata.gsets["vhn03"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/ChuwxNoom/VHN03.txt"),
        "VHN03.txt",
        skip_invalid_kuten=False))

