#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Implements the Maximum Matching Algorithm (as on the A-level syllabus)."""

# Split off from what is now maximise_cccii.py

import collections

def _improve_matching(alpha, alpha_to_possible, assignments, rassignments, betas_considered=()):
    pairs = []
    betas = alpha_to_possible[alpha]
    for beta in betas:
        if (alpha in assignments) and (beta == assignments[alpha]):
            continue
        elif beta not in rassignments:
            pairs.append((alpha, beta))
            return pairs
        elif beta not in betas_considered: # avoid infinite recursion back and forth between two alphas
            nextalpha = rassignments[beta]
            result = _improve_matching(nextalpha, alpha_to_possible, assignments, rassignments,
                                       betas_considered + (beta,))
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



