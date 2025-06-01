#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata

def decode_invocations(stream, state):
    workingsets = graphdata.workingsets
    single_set = -1
    single_token = None
    single_need = 0
    single_area = None
    start_of_ge = False
    locking_shift_introducer_seen = False
    single_shift_codes = (None, "SS1", "SS2", "SS3", "SS4", "SS5", "SS6", "SS7", "SS8", "SS9", "SS10", "SS11", "SS12", "SS13", "SS14", "SS15")
    locking_shift_codes_left = ("LS0", "LS1", "LS2", "LS3", "LS4", "LS5", "LS6", "LS7", "LS8", "LS9", "LS10", "LS11", "LS12", "LS13", "LS14", "LS15")
    locking_shift_codes_right = (None, "LS1R", "LS2R", "LS3R", "LS4R", "LS5R", "LS6R", "LS7R", "LS8R", "LS9R", "LS10R", "LS11R", "LS12R", "LS13R", "LS14R", "LS15R")
    for token in stream:
        if locking_shift_introducer_seen:
            if token[0] not in workingsets:
                yield ("ERROR", "TRUNCATEDLOCKINGSHIFTINTRODUCER")
            elif token[1] <= 0xF and token[1] != 0xD and token[2] == "GR":
                # https://stratadoc.stratus.com/vos/19.3.1/r194-02/appbr194-02h.html
                token = ("CTRL", "LS" + {0: "1", 0xE: "2", 0xF: "3"}.get(token[1], f"{(token[1] + 3):d}") + "R", "LSI", (token[1],), "LSI", "LSI")
            elif 1 <= token[1] <= 0xF and token[1] != 0xD and token[2] == "GL":
                token = ("CTRL", "LS" + {0xE: "2", 0xF: "3"}.get(token[1], f"{(token[1] + 3):d}"), "LSI", (token[1],), "LSI", "LSI")
            locking_shift_introducer_seen = False
        #
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
        if token[0] == "CTRL" and token[1] == "LSI":
            locking_shift_introducer_seen = True
        elif token[0] == "CTRL" and token[1] == "SI":
            if state.docsmode == "ebcdic":
                state.in_ebcdic_dbcs_mode = False
            else:
                state.glset = 0
            yield token
        elif token[0] == "CTRL" and token[1] == "SO":
            if state.docsmode == "ebcdic":
                state.in_ebcdic_dbcs_mode = True
            else:
                state.glset = 1
            yield token
        elif token[0] == "CTRL" and token[1] is not None and token[1] in locking_shift_codes_left:
            state.glset = locking_shift_codes_left.index(token[1])
            yield token
        elif token[0] == "CTRL" and token[1] is not None and token[1] in locking_shift_codes_right:
            state.grset = locking_shift_codes_right.index(token[1])
            yield token
        elif token[0] == "CTRL" and token[1] is not None and token[1] in single_shift_codes:
            single_area = None
            single_set = single_shift_codes.index(token[1])
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












