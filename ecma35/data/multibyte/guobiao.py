#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from ecma35.data import graphdata
from ecma35.data.multibyte import parsers

# GB 2312 (EUC-CN RHS)
graphdata.gsets["ir058"] = gb2312 = (94, 2, parsers.read_main_plane("index-gb18030.txt"))





