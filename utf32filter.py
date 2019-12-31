#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

utf32docs = (("DOCS", True, (0x41,)),
             ("DOCS", True, (0x44,)),
             ("DOCS", True, (0x46,)))

def decode_utf32(stream, state):
    bomap = {"<": "le", ">": "be"}
    for token in stream:
        if (token[0] == "DOCS"):
            if token in utf32docs:
                yield ("RDOCS", "UTF-32", token[1], token[2])
                state.bytewidth = 4
                state.endian = state.default_endian
                firstchar = True
                state.docsmode = "utf-32"
            else:
                yield token
        elif state.docsmode == "utf-32":
            if token[0] != "WORD":
                # ESC passing through
                yield token
                continue
            subtype = "UCS-4"
            if (0xD800 <= token[1] < 0xE000) and state.pedantic_surrogates:
                yield ("ERROR", "UTF32SURROGATE", token[1])
                subtype = "WTF-32"
            #
            if token[1] > 0x10FFFF:
                yield ("ERROR", "UTF32BEYOND", token[1])
            elif token[1] == 0xFFFE and (
                    (firstchar and state.regard_bom) or (state.regard_bom > 1)):
                state.endian = {">": "<", "<": ">"}[state.endian]
                yield ("BOM", state.endian)
            elif token[1] == 0xFEFF and firstchar and state.regard_bom:
                yield ("BOM", state.endian) # Confirms the assumed byte order.
            else:
                bo = bomap[state.endian]
                yield ("UCS", token[1], "UTF-32", subtype + bo)
            firstchar = False
        else: # i.e. isn't a DOCS, nor a UTF-32 part of the stream
            yield token
        #
    #
#








