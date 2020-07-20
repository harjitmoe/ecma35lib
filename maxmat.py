#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Implements the Maximum Matching Algorithm (as on the A-level syllabus)
to improve the aggregated versions of the EACC and CCCII mappings, by
case-by-case picking from the documented mappings to maximise the number 
of distinct Unicode characters represented between the twelve main CCCII 
layers for a given kanji's itaiji stack."""

from ecma35.data import graphdata
from ecma35.data.multibyte import traditional
import collections
import unicodedata as ucd

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

def _improve_matching(alpha, alpha_to_possible, assignments, rassignments):
    pairs = []
    betas = alpha_to_possible[alpha]
    for beta in betas:
        if (alpha in assignments) and (beta == assignments[alpha]):
            continue
        elif beta not in rassignments:
            pairs.append((alpha, beta))
            return pairs
        else:
            nextalpha = rassignments[beta]
            result = _improve_matching(nextalpha, alpha_to_possible, assignments, rassignments)
            if result:
                pairs.append((alpha, beta))
                pairs.extend(result)
                return pairs
    return None

def maximum_matching(alpha_to_possible):
    #
    # First get the trivial matching:
    popularities = collections.defaultdict(int)
    for alpha in alpha_to_possible:
        for beta in set(alpha_to_possible[alpha]):
            popularities[beta] += 1
    ascending = sorted(list(popularities.keys()), key=popularities.__getitem__)
    assignments = {}
    rassignments = {}
    for beta in ascending:
        for alpha, betas in alpha_to_possible.items():
            if (beta in betas) and (alpha not in assignments):
                assignments[alpha] = beta
                rassignments[beta] = alpha
                break # Break the inner of the two for loops
    #
    # Now try to find alternating paths to improve it:
    while len(assignments) < len(ascending):
        for alpha, betas in alpha_to_possible.items():
            if (not betas) or (alpha in assignments):
                continue
            result = _improve_matching(alpha, alpha_to_possible, assignments, rassignments)
            if result:
                for alpha, beta in result:
                    if alpha in assignments:
                        del rassignments[assignments[alpha]]
                    #
                    if beta in rassignments:
                        del assignments[rassignments[beta]]
                    #
                    assignments[alpha] = beta
                    rassignments[beta] = alpha
                break
        else: # for...else, i.e. for loop finished without encountering break
            break # i.e. it is maximal, even if not total, since we cannot improve it.
    return assignments

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
                    names = "# " + " + ".join(ucd.name(chr(i), "(unnamed)") for i in oset[pointer])
                    print(hexd, ucs, names, sep="\t", file=f)
    f.close()

