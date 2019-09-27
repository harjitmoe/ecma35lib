#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import graphdata

def _tonumber(s):
    if (len(s) != 2) or (s[0] != "G") or (s[1] not in "0123"):
        return -1
    return ord(s[1]) - ord("0")

def decode_graphical_sets(stream, *, def_g0="006", def_g1="100", def_g2="nil", def_g3="nil"):
    curs = [(def_g0, graphdata.gsets[def_g0]),
            (def_g1, graphdata.gsets[def_g1]),
            (def_g2, graphdata.gsets[def_g2]),
            (def_g3, graphdata.gsets[def_g3])]
    pending = []
    pset = -1
    invrange = None
    reconsume = None
    hwat = [None, None, None, None]
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        tno = _tonumber(token[0])
        if (tno >= 0) and (pset in (-1, tno)) and (invrange in (token[2], None)):
            if pset == -1:
                pset = tno
                invrange = token[2]
            # NOT else (falls through from first "then" clause)
            size = curs[tno][1][1]
            pending.append(token[1])
            assert len(pending) <= size
            if len(pending) == size:
                pointer = 0
                if curs[tno][1][0] == 94:
                    for byt in pending:
                        assert 1 <= byt <= 94
                        pointer *= 94
                        pointer += byt - 1
                else:
                    assert curs[tno][1][0] == 96
                    for byt in pending:
                        assert 0 <= byt <= 95
                        pointer *= 96
                        pointer += byt
                ucs = curs[tno][1][2][pointer]
                if ucs is None:
                    if curs[tno][0] != "Unknown":
                        yield ("ERROR", "UNDEFGRAPH", curs[tno][0], tuple(pending), pset, invrange)
                    else:
                        yield ("CHAR?", hwat[tno], tuple(pending), token[0], invrange)
                else:
                    yield ("CHAR", ucs, curs[tno][0], tuple(pending), token[0], invrange)
                pset = -1
                invrange = None
                del pending[:]
        elif pending:
            yield ("ERROR", "TRUNCMB", curs[tno][0], tuple(pending), pset, invrange)
            del pending[:]
            pset = -1
            invrange = None
            reconsume = token
        elif token[0] == "UCS":
            yield ("CHAR", token[1], "UCS", (token[1],), token[2], token[3])
        elif token[0] == "DESIG":
            sump = graphdata.sumps[token[2]]
            try:
                curs[token[1]] = sump[token[3]], graphdata.gsets[sump[token[3]]]
            except KeyError:
                yield token
                curs[token[1]] = "Unknown", graphdata.gsets["nil"]
                hwat[token[1]] = token[2], token[3]
            else:
                yield ("RDESIG", "G{}".format(token[1]), sump[token[3]],
                       token[2], token[3], token[4])
        else:
            yield token














