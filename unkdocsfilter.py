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
            if token[0] == "BYTE":
                # A single byte in an encoding of unknown code width
                yield ("CODEBYTE", lingering, token[1])
            elif token[0] == "WORD":
                # A single one-byte word in an encoding with a known code width of one byte
                yield ("CODEWORD", lingering, token[1])
            else:
                yield token
        else:
            yield token
        #
    #
#








