#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Improves the aggregated versions of the EACC and CCCII mappings, by
case-by-case picking from the documented mappings to maximise the number 
of distinct Unicode characters represented between the twelve main CCCII 
layers for a given kanji's itaiji stack."""

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data import graphdata
from ecma35.data.maxmat import maximum_matching # Split off from this script to use elsewhere.
from ecma35.data.multibyte import traditional
from ecma35.data.names import namedata

sets = [((None,) * (96 * 112)) + graphdata.gsets["cccii-koha"][2][96*112:],
        ((None,) * (96 * 112)) + traditional.cccii_unihan[96*112:],
        ((None,) * (96 * 112)) + graphdata.gsets["eacc-pure"][2][96*112:],
        ((None,) * (96 * 112)) + graphdata.gsets["eacc-hongkong"][2][96*112:],
        ((None,) * (96 * 112)) + graphdata.gsets["~cccii"][2][96*112:],
        ((None,) * (96 * 112)) + graphdata.gsets["~eacc"][2][96*112:]]

out_set1 = list(graphdata.gsets["~cccii"][2][:96*96*73])
out_set2 = list(graphdata.gsets["~eacc"][2][:96*96*73])
out_set1[:96 * 112] = [None] * (96 * 112)
out_set2[:96 * 112] = [None] * (96 * 112)

for bplane in range(1, 7):
    print("Base plane", bplane)
    for row in range(0, 96):
        for cell in range(0, 96):
            layers = []
            # Track how many unique assigments both out_sets start with, so we don't change them
            #   from one setup to a no-better setup:
            initial_uniques1 = set()
            initial_uniques2 = set()
            for rlayer in range(12):
                plane = bplane + (rlayer * 6)
                pointer = (plane * 96 * 96) + (row * 96) + cell
                layers.append(set(i[pointer] for i in sets if pointer < len(i) and i[pointer]))
                if out_set1[pointer]:
                    initial_uniques1.update({out_set1[pointer]})
                if out_set2[pointer]:
                    initial_uniques2.update({out_set2[pointer]})
            alpha_to_possible = dict(enumerate(layers))
            assignments = maximum_matching(alpha_to_possible)
            for rlayer in assignments:
                plane = bplane + (rlayer * 6)
                pointer = (plane * 96 * 96) + (row * 96) + cell
                if len(assignments) > len(initial_uniques1):
                    out_set1[pointer] = assignments[rlayer]
                if len(assignments) > len(initial_uniques2):
                    out_set2[pointer] = assignments[rlayer]

for (fn, oset) in (("cccii-maxmat.txt", out_set1), ("eacc-maxmat.txt", out_set2)):
    f = open(fn, "w")
    for plane in range(0, 96):
        for row in range(0, 96):
            for cell in range(0, 96):
                pointer = (plane * 96 * 96) + (row * 96) + cell
                if (pointer < len(oset)) and oset[pointer]:
                    hexd = "0x{:02X}{:02X}{:02X}".format(plane + 0x20, row + 0x20, cell + 0x20)
                    ucs = "U+" + "+".join("{:04X}".format(i) for i in oset[pointer])
                    names = "# " + " + ".join(namedata.get_ucsname(chr(i), "(unnamed)") for i in oset[pointer])
                    print(hexd, ucs, names, sep="\t", file=f)
    f.close()

