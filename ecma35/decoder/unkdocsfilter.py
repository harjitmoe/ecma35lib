#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def decode_remaining_docs(stream, state):
    lingering = None
    for token in stream:
        if (token[0] == "DOCS"):
            lingering = (token[1], token[2])
            state.docsmode = "Unknown"
            state.unk_hasesc = (not token[1])
            state.bytewidth = 1
            yield token
        elif (token[0] == "RDOCS"):
            lingering = None
            yield token
        elif token[0] == "ENDSTREAM":
            yield token
        elif lingering:
            if token[0] == "WORD":
                if state.unk_hasesc and (token[1] == 0x1B):
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








