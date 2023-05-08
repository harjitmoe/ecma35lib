#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def decode_ecma35docs(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    for token in stream:
        if (token[0] == "RDOCS"):
            if token[1] == "ecma-35":
                state.bytewidth = 1
                state.docsmode = "ecma-35"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir100", "nil", "nil"]
                state.is_96 = [0, 0, 1, 1]
            yield token
        elif state.docsmode == "ecma-35" and token[0] == "WORD":
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
            elif token[1] < 0xA0:
                yield ("C1", token[1] - 0x80, "CR")
            else:
                yield (workingsets[state.grset], token[1] - 0xA0, "GR")
        elif state.docsmode == "ecma-35" and token[0] == "CHCP":
            codepage = token[1]
            state.cur_gsets = list(graphdata.defgsets[codepage])
            state.is_96 = [graphdata.gsets[i][0] > 94 for i in state.cur_gsets]
            yield token
        else:
            yield token
        #
    #
#








