#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def decode_raw(stream, state):
    for token in stream:
        if (token[0] == "RDOCS"):
            if token[1] == "raw":
                state.bytewidth = 1
                state.docsmode = "raw"
            yield token
        elif state.docsmode == "raw":
            if token[0] == "ENDSTREAM":
                yield token
            else:
                assert (token[0] == "WORD") and (0 <= token[1] < 256), token
                yield ("RAWBYTE", token[1])
        else: # i.e. isn't a DOCS, nor a raw part of the stream
            yield token
        #
    #
#








