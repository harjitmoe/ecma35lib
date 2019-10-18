#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

utf32docs = (("DOCS", True, (0x41,)),
             ("DOCS", True, (0x44,)),
             ("DOCS", True, (0x46,)))

def decode_utf32(stream, state):
    is_utf32 = False
    bomap = {"<": "le", ">": "be"}
    for token in stream:
        if (token[0] == "DOCS"):
            is_utf32 = (token in utf32docs)
            if is_utf32:
                yield ("RDOCS", "UTF-32", token[1], token[2])
                state.hasesc = 0x1B
                state.bytewidth = 4
                state.endian = state.default_endian
                firstchar = True
            else:
                yield token
        elif is_utf32:
            if token[0] != "WORD":
                yield token # Escape code passing through
            elif (0xD800 <= token[1] < 0xE000) and state.pedantic_surrogates:
                yield ("ERROR", "UTF32SURROGATE", token[1])
            elif token[1] > 0x10FFFF:
                yield ("ERROR", "UTF32BEYOND", token[1])
            elif token[1] == 0xFFFE and (
                    (firstchar and state.regard_bom) or (state.regard_bom > 1)):
                state.endian = {">": "<", "<": ">"}[state.endian]
                yield ("BOM", state.endian)
            elif token[1] == 0xFEFF and firstchar and state.regard_bom:
                yield ("BOM", state.endian) # Confirms the assumed byte order.
            else:
                if token[1] == 0xFFFE:
                    print(token, firstchar, state.regard_bom)
                    raise AssertionError
                bo = bomap[state.endian]
                yield ("UCS", token[1], "UTF-32", "UCS-4" + bo)
            firstchar = False
        else: # i.e. isn't a DOCS, nor a UTF-32 part of the stream
            yield token
        #
    #
#








