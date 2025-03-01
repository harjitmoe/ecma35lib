#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import controldata
from ecma35.decoder.graphsets import proc_irrset

def decode_control_sets(stream, state):
    for token in stream:
        if token[0] == "UCS" and token[1] < 0x20:
            token = ("C0", token[1], token[3])
        elif token[0] == "UCS" and 0x80 <= token[1] < 0xA0:
            token = ("C1", token[1] - 0x80, token[3])
        # Not elif:
        if token[0] == "CDESIG":
            if token[1] == "C0":
                try:
                    mycset = controldata.c0bytes[token[2]]
                except KeyError:
                    yield token
                    state.cur_c0 = "Unknown"
                    state.hwotc0 = token[2]
                else:
                    mycseti = proc_irrset(mycset, token[3])
                    if mycseti is not None:
                        state.cur_c0 = mycseti
                    else:
                        yield ("ERROR", "UNRECIRR", mycset, token[3])
                        state.cur_c0 = mycset[0] if isinstance(mycset, tuple) else mycset
                    yield ("RDESIG", "C0", controldata.c0bytes[token[2]], "C0", token[2], False, token[3])
            else:
                assert token[1] == "C1"
                try:
                    mycset = controldata.c1bytes[token[2]]
                except KeyError:
                    yield token
                    state.cur_c1 = "Unknown"
                    state.hwotc1 = token[2]
                else:
                    mycseti = proc_irrset(mycset, token[3])
                    if mycseti is not None:
                        state.cur_c1 = mycseti
                    else:
                        yield ("ERROR", "UNRECIRR", mycset, token[3])
                        state.cur_c1 = mycset[0] if isinstance(mycset, tuple) else mycset
                    yield ("RDESIG", "C1", controldata.c1bytes[token[2]], "C1", token[2], False, token[3])
        elif token[0] == "C0":
            ctr = controldata.c0sets[state.cur_c0][token[1]]
            if ctr is None:
                if state.cur_c0 == "Unknown":
                    yield ("CTRL?", state.hwotc0, token[1], "C0", token[2])
                else:
                    yield ("ERROR", "UNDEFC0", token[1], state.cur_c0)
            else:
                yield ("CTRL", ctr, state.cur_c0, token[1], "C0", token[2])
        # NOTE: assumes C1 escapes will be recognised as such by decode_esc_sequences, and sent
        # back through as "C1" tokens via state.feedback.
        elif token[0] == "C1":
            ctr = controldata.c1sets[state.cur_c1][token[1]]
            if ctr is None:
                if state.cur_c1 == "Unknown":
                    yield ("CTRL?", state.hwotc1, token[1], "C1", token[2])
                else:
                    yield ("ERROR", "UNDEFC1", token[1], state.cur_c1)
            else:
                yield ("CTRL", ctr, state.cur_c1, token[1], "C1", token[2])
        else:
            yield token














