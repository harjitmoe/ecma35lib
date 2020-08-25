#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# TIS-620 (with NBSP) ISO-8859-11 Latin/Thai RHS
graphdata.gsets["ir166"] = (96, 1, (
             0x00A0, 0x0E01, 0x0E02, 0x0E03, 0x0E04, 0x0E05, 0x0E06, 0x0E07, 
             0x0E08, 0x0E09, 0x0E0A, 0x0E0B, 0x0E0C, 0x0E0D, 0x0E0E, 0x0E0F, 
             0x0E10, 0x0E11, 0x0E12, 0x0E13, 0x0E14, 0x0E15, 0x0E16, 0x0E17, 
             0x0E18, 0x0E19, 0x0E1A, 0x0E1B, 0x0E1C, 0x0E1D, 0x0E1E, 0x0E1F, 
             0x0E20, 0x0E21, 0x0E22, 0x0E23, 0x0E24, 0x0E25, 0x0E26, 0x0E27, 
             0x0E28, 0x0E29, 0x0E2A, 0x0E2B, 0x0E2C, 0x0E2D, 0x0E2E, 0x0E2F, 
             0x0E30, 0x0E31, 0x0E32, 0x0E33, 0x0E34, 0x0E35, 0x0E36, 0x0E37, 
             0x0E38, 0x0E39, 0x0E3A, None,   None,   None,   None,   0x0E3F, 
             0x0E40, 0x0E41, 0x0E42, 0x0E43, 0x0E44, 0x0E45, 0x0E46, 0x0E47, 
             0x0E48, 0x0E49, 0x0E4A, 0x0E4B, 0x0E4C, 0x0E4D, 0x0E4E, 0x0E4F, 
             0x0E50, 0x0E51, 0x0E52, 0x0E53, 0x0E54, 0x0E55, 0x0E56, 0x0E57, 
             0x0E58, 0x0E59, 0x0E5A, 0x0E5B, None,   None,   None,   None,))

# Code pages 874 (TIS-620 exts)
# Per alias comments in ICU's convrtrs.txt, IBM's 874 is identical to IBM's 9066.
# Microsoft's 874, on the other hand, matches the layout of IBM's 1162.
graphdata.rhses["1162"] = parsers.read_single_byte("WHATWG/index-windows-874.txt")
graphdata.rhses["9066"] = parsers.read_single_byte("ICU/ibm-874_P100-1995.ucm")
# The two only collide at 0xA0, which IBM uses for an alternate U+0E48 and which Microsoft
#   uses for an NBSP. Favour the more-deployed Microsoft / ISO-8859-11 NBSP for "874".
graphdata.rhses["874"] = tuple(a or b for a, b in zip(graphdata.rhses["1162"],
                                                      graphdata.rhses["9066"]))
graphdata.defgsets["874"] = graphdata.defgsets["1162"] = ("ir006", "ir166", "nil", "nil")

# Macintosh code page (doesn't have a Mozilla file)
#graphdata.rhses["10021"] = parsers.read_mozilla_ut_file("Mozilla/macthai.ut")



