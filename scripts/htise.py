#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2022.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, itertools
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data import graphdata

main_plane = graphdata.gsets["ir149/mac"][2]
side_plane = graphdata.gsets["mac-elex-extras"][2]

firsts = set(itertools.chain((i[0] for i in main_plane if i and len(i) == 1), (i[0] for i in side_plane if i and len(i) == 1)))

firsts |= set(range(128))

for i in itertools.chain(main_plane, side_plane):
    if not i:
        continue
    if i[0] not in firsts and not (0xF860 <= i[0] <= 0xF86F):
        print("".join(chr(j) for j in i), "+".join(f"{j:04X}" for j in i))

