#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata

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
        # The cur_gsets state prop might not yet be defined if e.g. DOCS % @ hasn't happened yet.
        tgset = state.cur_gsets[tno] if hasattr(state, "cur_gsets") else "Unknown"
        if (tno >= 0) and (pset in (-1, tno)) and (invrange in (token[2], None)) and (
                    graphdata.gsets[tgset][0] == 96 or 1 <= token[1] <= 94):
            if pset == -1:
                pset = tno
                invrange = token[2]
            # NOT else (falls through from first "then" clause)
            size = graphdata.gsets[tgset][1]
            pending.append(token[1])
            assert len(pending) <= size
            if len(pending) == size:
                pointer = 0
                if graphdata.gsets[tgset][0] == 94:
                    for byt in pending:
                        assert 1 <= byt <= 94
                        pointer *= 94
                        pointer += byt - 1
                else:
                    assert graphdata.gsets[tgset][0] == 96
                    for byt in pending:
                        assert 0 <= byt <= 95
                        pointer *= 96
                        pointer += byt
                array = graphdata.gsets[tgset][2]
                ucs = array[pointer] if pointer < len(array) else None
                if ucs is None:
                    if tgset != "Unknown":
                        yield ("ERROR", "UNDEFGRAPH", tgset, tuple(pending), pset, invrange)
                    else:
                        yield ("CHAR?", state.ghwots[tno], tuple(pending), token[0], invrange)
                elif isinstance(ucs, tuple):
                    for iucs in ucs:
                        yield ("CHAR", iucs, tgset, tuple(pending), token[0], invrange)
                else:
                    yield ("CHAR", ucs, tgset, tuple(pending), token[0], invrange)
                pset = -1
                invrange = None
                del pending[:]
        elif pending:
            yield ("ERROR", "TRUNCMB", tgset, tuple(pending), pset, invrange)
            del pending[:]
            pset = -1
            invrange = None
            reconsume = token
        elif (tno >= 0) and (graphdata.gsets[tgset][0] == 94) and token[1] in (0, 95):
            # Should only get here if using 0xA0 or 0xFF when a 94 or 94^n set is in GR.
            assert token[2] in ("GR", "SSGR")
            yield ("ERROR", "OUTSIDE94", token[0], token[1], token[2], tgset)
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














