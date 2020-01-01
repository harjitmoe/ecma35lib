#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import graphdata

def _tonumber(s):
    if (len(s) != 2) or (s[0] != "G") or (s[1] not in "0123"):
        return -1
    return ord(s[1]) - ord("0")

def decode_graphical_sets(stream, state):
    pending = []
    pset = -1
    invrange = None
    reconsume = None
    state.ghwots = [None, None, None, None]
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        tno = _tonumber(token[0])
        if (tno >= 0) and (pset in (-1, tno)) and (invrange in (token[2], None)):
            if pset == -1:
                pset = tno
                invrange = token[2]
            # NOT else (falls through from first "then" clause)
            size = graphdata.gsets[state.cur_gsets[tno]][1]
            pending.append(token[1])
            assert len(pending) <= size
            if len(pending) == size:
                pointer = 0
                if graphdata.gsets[state.cur_gsets[tno]][0] == 94:
                    for byt in pending:
                        assert 1 <= byt <= 94
                        pointer *= 94
                        pointer += byt - 1
                else:
                    assert graphdata.gsets[state.cur_gsets[tno]][0] == 96
                    for byt in pending:
                        assert 0 <= byt <= 95
                        pointer *= 96
                        pointer += byt
                ucs = graphdata.gsets[state.cur_gsets[tno]][2][pointer]
                if ucs is None:
                    if state.cur_gsets[tno] != "Unknown":
                        yield ("ERROR", "UNDEFGRAPH", state.cur_gsets[tno],
                               tuple(pending), pset, invrange)
                    else:
                        yield ("CHAR?", state.ghwots[tno], tuple(pending), token[0], invrange)
                elif isinstance(ucs, tuple):
                    for iucs in ucs:
                        yield ("CHAR", iucs, state.cur_gsets[tno], tuple(pending), 
                               token[0], invrange)
                else:
                    yield ("CHAR", ucs, state.cur_gsets[tno], tuple(pending), token[0], invrange)
                pset = -1
                invrange = None
                del pending[:]
        elif pending:
            yield ("ERROR", "TRUNCMB", state.cur_gsets[tno], tuple(pending), pset, invrange)
            del pending[:]
            pset = -1
            invrange = None
            reconsume = token
        elif token[0] == "UCS":
            yield ("CHAR", token[1], "UCS", (token[1],), token[2], token[3])
        elif token[0] == "DESIG":
            sump = graphdata.sumps[token[2]]
            try:
                state.cur_gsets[token[1]] = sump[token[3]]
            except KeyError:
                yield token
                state.cur_gsets[token[1]] = "Unknown"
                state.ghwots[token[1]] = token[2], token[3]
            else:
                yield ("RDESIG", "G{}".format(token[1]), sump[token[3]],
                       token[2], token[3], token[4])
        else:
            yield token














