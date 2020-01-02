#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from ecma35.data import graphdata
from ecma35.data.multibyte import parsers

# KS C 5601 / KS X 1001 EUC-KR Wansung RHS
graphdata.gsets["ir149"] = wansung = (94, 2, parsers.read_main_plane("index-euc-kr.txt"))





