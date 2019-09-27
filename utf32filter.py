#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

utf32docs = (("DOCS", True, (0x41,)),
             ("DOCS", True, (0x44,)),
             ("DOCS", True, (0x46,)))

def decode_utf32(stream):
    is_utf32 = False
    bo = "?"
    for token in stream:
        if (token[0] == "DOCS"):
            is_utf32 = (token in utf32docs)
            if is_utf32:
                yield ("RDOCS", "UTF-32", token[1], token[2])
                bo = "?"
            else:
                yield token
        elif is_utf32:
            if token[0] == "DEFBO":
                bo = {"<": "le", ">": "be"}[token[1]]
            elif token[0] == "BOM":
                bo = {"<": "le", ">": "be"}[token[1]]
                yield token
            elif token[0] != "WORD":
                yield token # Escape code passing through
            elif token[1] > 0x10FFFF:
                yield ("ERROR", "UTF32BEYOND", ucs)
            else:
                yield ("UCS", token[1], "UTF-32", "UCS-4" + bo)
        else: # i.e. isn't a DOCS, nor a UTF-32 part of the stream
            yield token
        #
    #
#








