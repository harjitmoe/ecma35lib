#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data import graphdata

sets_s = ("ir058", "gb7589", "gb7590")
sets_t = ("ir058/hant-strict", "gb13131", "gb13132")

seen_s = {}
for set_s in sets_s:
    for n, i in enumerate(graphdata.gsets[set_s][2]):
        if not i:
            continue
        k = (n // 94) + 1
        t = (n % 94) + 1
        b = f"0x{k+0x20:02X}{t+0x20:02X}"
        if i in seen_s:
            print(set_s, k, t, b, "=", *seen_s[i])
        else:
            seen_s[i] = (set_s, k, t, b)

seen_t = {}
for set_t in sets_t:
    for n, i in enumerate(graphdata.gsets[set_t][2]):
        if not i:
            continue
        k = (n // 94) + 1
        t = (n % 94) + 1
        b = f"0x{k+0x20:02X}{t+0x20:02X}"
        if i in seen_t:
            print(set_t, k, t, b, "=", *seen_t[i])
        else:
            seen_t[i] = (set_t, k, t, b)


