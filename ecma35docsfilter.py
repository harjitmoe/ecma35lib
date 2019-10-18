#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

ecma35docs = ("DOCS", False, (0x40,))

def decode_ecma35docs(stream, state):
    for token in stream:
        reconsume = None
        if (token[0] == "DOCS"):
            if token == ecma35docs:
                yield ("RDOCS", "ECMA-35", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "ecma-35"
            else:
                yield token
        elif state.docsmode == "ecma-35" and token[0] == "WORD":
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








