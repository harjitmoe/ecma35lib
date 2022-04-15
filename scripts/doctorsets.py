#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2022.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, pprint
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.graphdata import gsets, g94bytes, g96bytes, g94nbytes, g96nbytes
used = set()
for (idbytes, bit) in [*g94bytes.items(), *g96bytes.items(), *g94nbytes.items(), *g96nbytes.items()]:
    if isinstance(bit, tuple):
        preferred, private, formal = bit
        for i in [preferred, *private, *formal]:
            used.add(i)
    else:
        used.add(bit)

complaints = set()
for (setcode, (kind, bytecount, entries)) in gsets.items():
    assert kind==94 or kind==96
    if setcode not in used:
        complaints.add((setcode, "NotDesignable"))
    for pointer, entry in enumerate(entries):
        if not isinstance(entry, (tuple, type(None))):
            complaints.add((setcode, "NotNullOrTuple"))
        if entry:
            if not hasattr(entry, "__iter__"):
                entry = (entry,)
            if entry == (-1,):
                complaints.add((setcode, "ExpiredMinusOne"))
            elif None in entry:
                complaints.add((setcode, "NullInTuple"))
            elif any((abs(i) < 0x20 or 0x7F <= abs(i) < 0xA0) for i in entry):
                complaints.add((setcode, "MapToCcCharacter"))


pprint.pprint([*sorted(complaints)])

