#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from ecma35.data import graphdata

def decode_eight_ones_terminated(stream, state):
    for token in stream:
        if (token[0] == "RDOCS"):
            if token[1] == "eight-ones-terminated":
                state.bytewidth = 1
                state.docsmode = "eight-ones-terminated"
                state.cur_lhs = "437"
                state.cur_rhs = "437"
            yield token
        elif state.docsmode == "eight-ones-terminated" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] == 0x00:
                yield ("CTRL", "SP", state.cur_lhs, token[1], "LHS", state.cur_lhs)
            elif token[1] == 0xFF:
                yield ("CTRL", "CMD", state.cur_rhs, token[1], "RHS", state.cur_rhs)
            else:
                if token[1] < 0x80:
                    index = token[1]
                    setname = state.cur_lhs
                    sump = graphdata.lhses
                    region = "LHS"
                else:
                    index = token[1] - 0x80
                    setname = state.cur_rhs
                    sump = graphdata.rhses
                    region = "RHS"
                if setname not in sump:
                    yield ("CHAR?", setname, (index,), region, region)
                    continue
                ucs = sump[setname][index]
                if ucs is None:
                    yield ("ERROR", "UNDEFGRAPH", setname, (index,), -1, region)
                elif isinstance(ucs, tuple):
                    for iucs in ucs:
                        yield ("CHAR", iucs, setname, (index,), region, region)
                else:
                    yield ("CHAR", ucs, setname, (index,), region, region)
        elif state.docsmode == "eight-ones-terminated" and token[0] == "CHCP":
            codepage = token[1]
            state.cur_lhs = state.cur_rhs = codepage
            yield token
        else:
            yield token

