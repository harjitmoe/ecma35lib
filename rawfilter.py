#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

rawdocs = ("DOCS", True, (0x42,))

def decode_raw(stream, state):
    is_raw = False
    for token in stream:
        if (token[0] == "DOCS"):
            is_raw = (token == rawdocs)
            if is_raw:
                yield ("RDOCS", "RAW", token[1], token[2])
            else:
                yield token
        elif is_raw:
            if token[0] == "ENDSTREAM":
                yield token
            else:
                assert token[0] == "BYTE" # Anything else shouldn't get here.
                yield ("RAWBYTE", token[1])
        else: # i.e. isn't a DOCS, nor a raw part of the stream
            yield token
        #
    #
#








