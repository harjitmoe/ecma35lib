#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata

def decode_invocations(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    single_set = -1
    single_token = None
    single_need = 0
    single_area = None
    start_of_ge = False
    for token in stream:
        if start_of_ge:
            if token[0] in workingsets and token[2] in ("GL", "GR"):
                single_area = token[2]
                single_set = (2 if single_area == "GL" else 3)
                single_need = graphdata.gsets[state.cur_gsets[single_set]][1]
                if not single_need:
                    yield ("ERROR", "INDETERMSINGLE", token)
                    single_set = -1
            else:
                single_set = 2 # will get set to -1 in next part
            start_of_ge = False
            # (Fall through to next part.)
        #
        if single_set >= 0:
            expected = (single_area,) if single_area else ("GL", "GR")
            if token[0] in workingsets and token[2] in expected:
                if not single_area: # Don't inject in the middle of the code sequence.
                    # For announcement verification.
                    yield ("SINGLEOVER", token[2], single_token[1], single_token[2], single_token[3])
                    single_area = token[2]
                yield (workingsets[single_set], token[1], "SS" + token[2])
                single_need -= 1
                if not single_need:
                    single_set = -1
                continue
            else:
                yield ("ERROR", "SINGLETRUNCATE", single_token)
                single_set = -1
                # (Fall through to next part.)
            #
        # Keep the locking shift tokens in the stream for metadata, announcements, etc…
        # Since no GL or GR opcodes will remain, this won't break anything.
        # NOT elif (so byte after truncated single shift sequence isn't swallowed):
        if token[0] == "CTRL" and token[1] in ("SI", "LS0"):
            if state.docsmode == "ebcdic" and token[1] == "SI":
                state.in_ebcdic_dbcs_mode = False
            else:
                state.glset = 0
            yield token
        elif token[0] == "CTRL" and token[1] in ("SO", "LS1"):
            if state.docsmode == "ebcdic" and token[1] == "SO":
                state.in_ebcdic_dbcs_mode = True
            else:
                state.glset = 1
            yield token
        elif token[0] == "CTRL" and token[1] == "LS2":
            state.glset = 2
            yield token
        elif token[0] == "CTRL" and token[1] == "LS1R":
            state.grset = 1
            yield token
        elif token[0] == "CTRL" and token[1] == "LS2":
            state.glset = 2
            yield token
        elif token[0] == "CTRL" and token[1] == "LS2R":
            state.grset = 2
            yield token
        elif token[0] == "CTRL" and token[1] == "SS2":
            single_area = None
            single_set = 2
            single_token = token
            single_need = graphdata.gsets[state.cur_gsets[single_set]][1]
            if single_set in (state.glset, state.grset):
                yield ("ERROR", "REDUNDANTSINGLESHIFT", single_set)
            if not single_need:
                yield ("ERROR", "INDETERMSINGLE", token)
                single_set = -1
        elif token[0] == "CTRL" and token[1] == "LS3":
            state.glset = 3
            yield token
        elif token[0] == "CTRL" and token[1] == "LS3R":
            state.grset = 3
            yield token
        elif token[0] == "CTRL" and token[1] == "SS3":
            single_area = None
            single_set = 3
            single_token = token
            single_need = graphdata.gsets[state.cur_gsets[single_set]][1]
            if single_set in (state.glset, state.grset):
                yield ("ERROR", "REDUNDANTSINGLESHIFT", single_set)
            if not single_need:
                yield ("ERROR", "INDETERMSINGLE", token)
                single_set = -1
        elif token[0] == "CTRL" and token[1] == "GE":
            single_token = token
            start_of_ge = True
        elif token[0] == "DESIG":
            yield token
            state.is_96[token[1]] = (token[2] not in ("94", "94n"))
        elif token[0] == "UCS" and token[1] == 0x20:
            yield ("CTRL", "SP", "UCS", (token[1],), token[2], token[3])
        elif token[0] == "UCS" and token[1] == 0x7F:
            yield ("CTRL", "DEL", "UCS", (token[1],), token[2], token[3])
        else:
            yield token












