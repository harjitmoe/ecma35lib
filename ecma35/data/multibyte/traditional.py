#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from ecma35.data import graphdata
from ecma35.data.multibyte import parsers

# CNS 11643
graphdata.gsets["ir171"] = cns1 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=1))
graphdata.gsets["ir172"] = cns2 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=2))
# ISO-IR numbers jump by ten here (between the Big-5 and non-Big-5 planes).
graphdata.gsets["ir183"] = cns3 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=3))
graphdata.gsets["ir184"] = cns4 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=4))
graphdata.gsets["ir185"] = cns5 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=5))
graphdata.gsets["ir186"] = cns6 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=6))
graphdata.gsets["ir187"] = cns7 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=7))
# Plane 7 is the last one to be registered with ISO-IR. Plane 8 is unused.
graphdata.gsets["cns-9"] = cns9 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=9))
# The entirety does also exist as an unregistered 94^n set, used by EUC-TW:
graphdata.gsets["cns-eucg2"] = euctw_g2 = (94, 3, parsers.read_main_plane("cns-11643-1992.ucm"))





