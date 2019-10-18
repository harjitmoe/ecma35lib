#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

def decode_remaining_docs(stream, state):
    lingering = None
    for token in stream:
        if (token[0] == "DOCS"):
            lingering = (token[1], token[2])
            yield token
        elif (token[0] == "RDOCS"):
            lingering = None
            yield token
        elif token[0] == "ENDSTREAM":
            yield token
        elif lingering:
            if token[0] == "WORD":
                if state.hasesc and (token[1] == 0x1B):
                    # We need to recognise standard return if we're in a DOCS with standard return.
                    yield ("C0", token[1], "CL")
                else:
                    yield ("CODEWORD", lingering, token[1])
            else:
                yield token
        else:
            yield token
        #
    #
#








