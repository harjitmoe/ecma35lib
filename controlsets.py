#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import controldata

def decode_control_sets(stream, *, def_c0="001", def_c1="RFC1345"):
    cur_c0 = def_c0, controldata.c0sets[def_c0]
    cur_c1 = def_c1, controldata.c1sets[def_c1]
    hwotc0 = hwotc1 = None
    for token in stream:
        if token[0] == "UCS" and token[1] < 0x20:
            token = ("C0", token[1], token[3])
        elif token[0] == "UCS" and 0x80 <= token[1] < 0xA0:
            token = ("C1", token[1] - 0x80, token[3])
        # Not elif:
        if token[0] == "CDESIG":
            if token[1] == "C0":
                try:
                    cur_c0 = controldata.c0bytes[token[2]]
                    cur_c0 = cur_c0, controldata.c0sets[cur_c0]
                except KeyError:
                    yield token
                    cur_c0 = "Unknown", controldata.c0sets["nil"]
                    hwotc0 = token[2]
                else:
                    yield ("RDESIG", "C0", controldata.c0bytes[token[2]], "C0", token[2], False)
            else:
                assert token[1] == "C1"
                try:
                    cur_c1 = controldata.c1bytes[token[2]]
                    cur_c1 = cur_c1, controldata.c1sets[cur_c1]
                except KeyError:
                    yield token
                    cur_c1 = "Unknown", controldata.c1sets["nil"]
                    hwotc1 = token[2]
                else:
                    yield ("RDESIG", "C1", controldata.c1bytes[token[2]], "C1", token[2], False)
        elif token[0] == "C0":
            ctr = cur_c0[1][token[1]]
            if ctr is None:
                if cur_c0 == "Unknown":
                    yield ("CTRL?", hwotc0, token[1], "C0", token[2])
                else:
                    yield ("ERROR", "UNDEFC0", token[1], cur_c0[0])
            else:
                yield ("CTRL", ctr, cur_c1[0], token[1], "C0", token[2])
        # NOTE: assumes C1 control escape sequences already recognised as such by tokenfeed.
        elif token[0] == "C1":
            ctr = cur_c1[1][token[1]]
            if ctr is None:
                if cur_c1 == "Unknown":
                    yield ("CTRL?", hwotc1, token[1], "C1", token[2])
                else:
                    yield ("ERROR", "UNDEFC1", token[1], cur_c1[0])
            else:
                yield ("CTRL", ctr, cur_c1[0], token[1], "C1", token[2])
        else:
            yield token














