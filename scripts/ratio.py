#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2022.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, pprint
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.graphdata import gsets
maxes = []
for (setcode, (kind, bytecount, entries)) in gsets.items():
    for pointer, entry in enumerate(entries):
        assert kind==94 or kind==96
        if entry:
            if not hasattr(entry, "__iter__"):
                entry = [entry]
            utf8 = "".join(chr(abs(i)) for i in entry).encode("utf8")
            ratio = len(utf8) / bytecount
            if ratio > 6:
                maxes.append((ratio, setcode, kind, pointer, utf8.decode("utf8")))

maxes.sort()
pprint.pprint(maxes)

