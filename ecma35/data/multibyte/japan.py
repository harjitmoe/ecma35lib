#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from ecma35.data import graphdata
from ecma35.data.multibyte import parsers

# JIS C 6226:1978 / JIS X 0208:1978
graphdata.gsets["ir042"] = jisx0208_gzdm4_at = (94, 2, parsers.read_main_plane("x208_1978.txt"))
# JIS C 6226:1983 / JIS X 0208:1983
graphdata.gsets["ir087"] = jisx0208_gzdm4_b = (94, 2, parsers.read_main_plane("x208_1983.txt"))
# JIS X 0212:1990 (i.e. the 1990 supplementary plane)
graphdata.gsets["ir159"] = jisx0212 = (94, 2, parsers.read_main_plane("index-jis0212.txt", whatwgjis=True))
# JIS X 0208:1990 or 1997
graphdata.gsets["ir168"] = jisx0208_irr_at_gzdm4_b = (94, 2, parsers.read_main_plane("x208_1990.txt"))
# JIS X 0208, Microsoft and WHATWG version, as specified for use in HTML5
graphdata.gsets["ir168web"] = jisx0208_html5 = (94, 2, parsers.read_main_plane("index-jis0208.txt", whatwgjis=True))
graphdata.gsets["ibmsjisext"] = sjis_html5_g3 = (94, 2, parsers.read_jis_trailer("index-jis0208.txt"))





