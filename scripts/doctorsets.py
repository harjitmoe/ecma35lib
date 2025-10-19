#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2022, 2024, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, pprint, re
import unicodedata as ucd
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.graphdata import gsets, g94bytes, g96bytes, g94nbytes, g96nbytes, defgsets, gsetflags, ebcdicdbcs, rhses
used = set()
complaints = set()
nominal_kind = {}
for (kind, (idbytes, bit)) in [
        *[("94", i) for i in g94bytes.items()],
        *[("96", i) for i in g96bytes.items()],
        *[("94n", i) for i in g94nbytes.items()],
        *[("96n", i) for i in g96nbytes.items()]]:
    if isinstance(bit, tuple):
        preferred, private, formal = bit
        expected_size = expected_width = None
        for i in [preferred, *private, *formal]:
            used.add(i)
            if nominal_kind.setdefault(i, kind) != kind and i != "nil":
                complaints.add((i, "ReferencedWithConflictingKinds", nominal_kind[i], kind))
            if i in gsets:
                size, width = gsets[i][:2]
                if len(kind) == 2 and width != 1 and size != int(kind, 10):
                    complaints.add((i, "ReferencedWithWrongKind", nominal_kind[i], size, width))
                if expected_size is None:
                    expected_size, expected_width = size, width
                elif (expected_size, expected_width) != (size, width):
                    complaints.add((i, "MultipleKinds", expected_size, expected_width, size, width))
    else:
        used.add(bit)
        if nominal_kind.setdefault(bit, kind) != kind and bit != "nil":
            complaints.add((bit, "ReferencedWithConflictingKinds", nominal_kind[bit], kind))
defgsetscountsasused = re.compile(r"^g[lr]\d+(?:/\w+)?\Z")
for sets in defgsets.values():
    for i in sets:
        if defgsetscountsasused.match(i):
            used.add(i)
for i in ebcdicdbcs.values():
    used.add(i)
used.remove(None)
for i in used:
    assert isinstance(i, str), i
    if i not in gsets:
        complaints.add((i, "DoesNotExist"))
    else:
        if i[0] == "~":
            complaints.add((i, "TildeDesignatable"))
        #
        if i in nominal_kind:
            if gsets[i][0] == 94 and gsets[i][1] == 1 and nominal_kind[i] != "94":
                complaints.add((i, "ReferencedWithWrongKind", nominal_kind[i], "ShouldBe", "94"))
            elif gsets[i][0] == 96 and gsets[i][1] == 1 and nominal_kind[i] != "96":
                complaints.add((i, "ReferencedWithWrongKind", nominal_kind[i], "ShouldBe", "96"))
            elif gsets[i][0] == 94 and gsets[i][1] > 1 and nominal_kind[i] != "94n":
                complaints.add((i, "ReferencedWithWrongKind", nominal_kind[i], "ShouldBe", "94n"))
            elif gsets[i][0] == 96 and gsets[i][1] > 1 and nominal_kind[i] != "96n":
                complaints.add((i, "ReferencedWithWrongKind", nominal_kind[i], "ShouldBe", "96n"))

for i in gsetflags:
    if i not in gsets:
        complaints.add((i, "OrphanFlag"))

checksums = {}
for (setcode, (kind, bytecount, entries)) in sorted(gsets.items()):
    running_hash = 0
    for n, entry in enumerate(entries):
        if entry:
            if not hasattr(entry, "__iter__"):
                entry = (entry,)
            element = sum(i or 0 for i in entry)
            running_hash += (element * n)
            running_hash %= 0x40000000
    if running_hash in checksums:
        edoctes = checksums[running_hash]
        if gsets[setcode] == gsets[edoctes] and gsetflags[setcode] == gsetflags[edoctes]:
            complaints.add((setcode, "Duplicates", checksums[running_hash]))
    else:
        checksums[running_hash] = setcode

for setcode, entries in sorted(rhses.items()):
    running_hash = 0
    for n, entry in enumerate(entries):
        if entry:
            if not hasattr(entry, "__iter__"):
                entry = (entry,)
            element = sum(i or 0 for i in entry)
            running_hash += (element * n)
            running_hash %= 0x40000000
    if running_hash in checksums:
        edoctes = checksums[running_hash]
        if edoctes in rhses and rhses[setcode] == rhses[edoctes]:
            complaints.add((setcode, "Duplicates", checksums[running_hash]))
    else:
        checksums[running_hash] = setcode

for (setcode, (kind, bytecount, entries)) in gsets.items():
    assert kind==94 or kind==96 or kind==190
    if setcode not in used and setcode[0] != "~":
        complaints.add((setcode, "NotDesignatable"))
    if len(entries) < (kind ** bytecount):
        if bytecount < 3:
            complaints.add((setcode, "ShortArray"))
        elif len(entries) % (kind * kind):
            complaints.add((setcode, "LastPlaneShort"))
    if len(entries) > (kind ** bytecount):
        complaints.add((setcode, "OverlongArray"))
    for pointer, entry in enumerate(entries):
        if not isinstance(entry, (tuple, type(None))):
            complaints.add((setcode, "NotNullOrTuple"))
        if entry is not None:
            if not hasattr(entry, "__iter__"):
                entry = (entry,)
            if len(entry) == 0:
                complaints.add((setcode, "EmptyMappingTarget"))
            elif entry == (-1,):
                complaints.add((setcode, "ExposedMinusOne"))
            else:
                if None in entry:
                    complaints.add((setcode, "NullInTuple"))
                if any((abs(i) < 0x20 or 0x7F <= abs(i) < 0xA0) for i in entry):
                    complaints.add((setcode, "MapToCcCharacter"))
                if len(entry) > 1 and all(i >= 0 for i in entry):
                    string = "".join(chr(i) for i in entry)
                    if string != ucd.normalize("NFC", string):
                        complaints.add((setcode, "NotNormalised", entry))


pprint.pprint([*sorted(complaints)])

print("Forcing all gsets to test whether any lazy code is broken")
for i in gsets.values():
    tuple(i[2])


