#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def decode_utf32(stream, state):
    bomap = {"<": "le", ">": "be"}
    for token in stream:
        docsmap = {"utf-32": state.default_endian, "utf-32le": "<", "utf-32be": ">"}
        if (token[0] == "RDOCS"):
            if token[1] in docsmap:
                state.bytewidth = 4
                state.endian = docsmap[token[1]]
                firstchar = token[1] == "utf-32"
                state.docsmode = "utf-32"
            yield token
        elif state.docsmode == "utf-32":
            if token[0] != "WORD":
                # ESC passing through
                yield token
                continue
            if (0xD800 <= token[1] < 0xE000) and state.pedantic_surrogates:
                yield ("CESU", token[1], "32" + bo)
            elif token[1] > 0x10FFFF:
                yield ("ERROR", "UTF32BEYOND", token[1])
            elif token[1] == 0xFFFE and (
                    (firstchar and state.regard_bom) or (state.regard_bom > 1)):
                state.endian = {">": "<", "<": ">"}[state.endian]
                yield ("BOM", state.endian)
            elif token[1] == 0xFEFF and firstchar and state.regard_bom:
                yield ("BOM", state.endian) # Confirms the assumed byte order.
            else:
                bo = bomap[state.endian]
                yield ("UCS", token[1], "UTF-32", "UCS-4" + bo)
            firstchar = False
        else: # i.e. isn't a DOCS, nor a UTF-32 part of the stream
            yield token
        #
    #
#








