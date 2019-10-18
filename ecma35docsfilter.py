#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

ecma35docs = (("DOCS", False, (0x40,)),)

def decode_ecma35docs(stream, state):
    is_ecma35 = True
    for token in stream:
        reconsume = None
        if (token[0] == "DOCS"):
            is_ecma35 = (token in ecma35docs)
            if is_ecma35:
                yield ("RDOCS", "ECMA-35", token[1], token[2])
                state.bytewidth = 1
            else:
                yield token
        elif is_ecma35 and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                yield ("C0", token[1], "CL")
            elif token[1] < 0x80:
                yield ("GL", token[1] - 0x20)
            elif token[1] < 0xA0:
                yield ("C1", token[1] - 0x80, "CR")
            else:
                yield ("GR", token[1] - 0xA0)
        else:
            yield token
        #
    #
#








