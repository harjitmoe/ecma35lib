#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# Note: since gsets specifies length as second member, no more need for "94n" distinct from "94".
# Necessary since a set could have a length of, say, 3 (take the EUC-TW (DRCS-ish) G2 set).
gsets = {"006": (94, 1, tuple(range(0x21, 0x7F))),
         "100": (96, 1, tuple(range(0xA0, 0x100))),
         "nil": (94, 1, (None,)*94)}

g94bytes = {tuple(b"B"): "006",
            tuple(b"~"): "nil"}

g96bytes = {tuple(b"A"): "100",
            tuple(b"~"): "nil"}

g94nbytes = {tuple(b"~"): "nil"}

g96nbytes = {tuple(b"~"): "nil"}

sumps = {"94": g94bytes, "96": g96bytes, "94n": g94nbytes, "96n": g96nbytes}

def _tonumber(s):
    if (len(s) != 2) or (s[0] != "G") or (s[1] not in "0123"):
        return -1
    return ord(s[1]) - ord("0")

def decode_graphical_sets(stream, *, def_g0="006", def_g1="100", def_g2="nil", def_g3="nil"):
    curs = [(def_g0, gsets[def_g0]),
            (def_g1, gsets[def_g1]),
            (def_g2, gsets[def_g2]),
            (def_g3, gsets[def_g3])]
    pending = []
    pset = -1
    for token in stream:
        tno = _tonumber(token[0])
        if (tno >= 0) and (pset in (-1, tno)):
            if pset == -1:
                pset = tno
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
                    yield ("ERROR", "UNDEFGRAPH", tuple(pending), curs[tno][0], token)
                else:
                    yield ("CHAR", ucs, curs[tno][0], token)
                pset = -1
                del pending[:]
        elif pending:
            yield ("ERROR", "TRUNCMB", tuple(pending))
            del pending[:]
            pset = -1
        elif token[0] == "UCS":
            yield ("CHAR", token[1], "ucs", token)
        elif token[0] == "DESIG":
            sump = sumps[token[2]]
            try:
                curs[token[1]] = sump[token[3]], gsets[sump[token[3]]]
            except KeyError:
                yield ("ERROR", "UNSUPSET", token)
                curs[token[1]] = "nil", gsets["nil"]
        else:
            yield token














