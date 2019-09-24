#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

utf32docs = (("DOCS", True, (0x41,)),
             ("DOCS", True, (0x44,)),
             ("DOCS", True, (0x46,)))

def utf32filter(stream):
    is_utf32 = False
    for token in stream:
        if (token[0] == "DOCS"):
            is_utf32 = (token in utf32docs)
            yield token
        elif is_utf32:
            if token[0] != "WORD":
                yield token # Escape code passing through
            elif token[1] > 0x10FFFF:
                yield ("ERROR", "UTF32BEYOND", ucs)
            else:
                yield ("UCS", token[1])
        else: # i.e. isn't a DOCS, nor a UTF-32 part of the stream
            yield token
        #
    #
#








