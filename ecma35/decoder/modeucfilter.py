#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2025 (with some earlier material partly derived from other parts of ecma35lib).

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata

def decode_modeuc(stream, state):
    workingsets = graphdata.workingsets
    possible_lead_token = None
    for token in stream:
        if possible_lead_token:
            assert possible_lead_token[0] == "WORD", possible_lead_token
            invoking_singlebyte_set = (possible_lead_token[1] == 0x80)
            if state.docsmode == "modified-euc" and token[0] == "WORD":
                if 0x20 <= token[1] <= 0x7F and bool(invoking_singlebyte_set) == bool(graphdata.gsets[state.cur_gsets[5]][1] == 1):
                    if possible_lead_token[1] != 0x80:
                        yield ("G4", possible_lead_token[1] - 0xA0, "GRGL")
                    yield ("G4", token[1] - 0x20, "GRGL")
                    possible_lead_token = None
                    continue
                elif 0xA0 <= token[1] <= 0xFF and bool(invoking_singlebyte_set) == bool(graphdata.gsets[state.cur_gsets[state.grset]][1] == 1):
                    if possible_lead_token[1] != 0x80:
                        yield (workingsets[state.grset], possible_lead_token[1] - 0xA0, "GR")
                    yield (workingsets[state.grset], token[1] - 0xA0, "GR")
                    possible_lead_token = None
                    continue
            #
            if possible_lead_token[1] == 0x80: # NOT elif (fall through from above)
                yield ("C1", 0, "CR")
            elif 0xA0 <= possible_lead_token[1] <= 0xFF:
                yield (workingsets[state.grset], possible_lead_token[1] - 0xA0, "GR")
            else:
                raise AssertionError(possible_lead_token)
            possible_lead_token = None
        #
        if (token[0] == "RDOCS"): # not elif (fall through from above)
            if token[1] == "modified-euc":
                state.bytewidth = 1
                state.docsmode = "modified-euc"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir168/web", "ir013", "ir159", "user-defined/6204"]
                state.is_96 = [0, 0, 0, 0, 0]
                state.cur_gsets.extend(graphdata.initial_gsets[len(state.cur_gsets):])
                state.is_96.extend(graphdata.initial_gsets[len(state.is_96):])
            yield token
        elif state.docsmode == "modified-euc" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                yield ("C0", token[1], "CL")
            elif token[1] < 0x80:
                if (not state.is_96[state.glset]) and (token[1] == 0x20):
                    yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                elif (not state.is_96[state.glset]) and (token[1] == 0x7F):
                    yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                else:
                    yield (workingsets[state.glset], token[1] - 0x20, "GL")
            elif token[1] == 0x80 and (1 in (graphdata.gsets[state.cur_gsets[state.grset]][1],
                                             graphdata.gsets[state.cur_gsets[4]][1])):
                possible_lead_token = token
                continue
            elif token[1] < 0xA0:
                yield ("C1", token[1] - 0x80, "CR")
            elif 2 in (graphdata.gsets[state.cur_gsets[state.grset]][1],
                       graphdata.gsets[state.cur_gsets[4]][1]):
                possible_lead_token = token
                continue
            else:
                yield (workingsets[state.grset], token[1] - 0xA0, "GR")
        elif state.docsmode == "modified-euc" and token[0] == "CHCP":
            codepage = token[1]
            state.cur_gsets = list(graphdata.defgsets[codepage])
            state.is_96 = [graphdata.gsets[i][0] > 94 for i in state.cur_gsets]
            state.cur_gsets.extend(graphdata.initial_gsets[len(state.cur_gsets):])
            state.is_96.extend(graphdata.initial_gsets[len(state.is_96):])
            yield token
        else:
            yield token
        #
    #
#








