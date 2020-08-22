#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Vietnamese Roman encodings (Quo^'c ngu*~), besides Windows-1258 which is in plainext.py

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# VPS
graphdata.rhses["997000"] = parsers.read_mozilla_ut_file("Mozilla/vps.ut")
graphdata.c0graphics["997000"] = parsers.read_mozilla_ut_file("Mozilla/vps.ut", typ="CL33")

# TCVN (TCVN 5712, VSCII; not VISCII)
graphdata.rhses["997001"] = parsers.read_mozilla_ut_file("Mozilla/tcvn5712.ut")
graphdata.c0graphics["997001"] = parsers.read_mozilla_ut_file("Mozilla/tcvn5712.ut", typ="CL33")
graphdata.gsets["ir180"] = (96, 1, parsers.read_mozilla_ut_file("Mozilla/tcvn5712.ut", typ="GR96"))
graphdata.defgsets["997001"] = ("ir014", "ir180", "nil", "nil")

# VISCII (not VSCII)
graphdata.rhses["997002"] = parsers.read_mozilla_ut_file("Mozilla/viscii.ut")
graphdata.c0graphics["997002"] = parsers.read_mozilla_ut_file("Mozilla/viscii.ut", typ="CL33")

# TODO: VNI, VNI-Mac, VNI-DOS


