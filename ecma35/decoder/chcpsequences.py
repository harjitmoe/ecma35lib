#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from ecma35.data import graphdata

def decode_chcp(stream, state):
    for token in stream:
        if token[0] == "CSISEQ" and token[1] == "DECSPPCS":
            # DEC Select [IBM] ProPrinter Character Set, i.e. CSI sequence for basically chcp.
            codepage = bytes(token[2]).decode("ascii")
            if codepage not in graphdata.chcpdocs:
                yield ("ERROR", "UNRECCHCP", token)
                continue
            elif graphdata.chcpdocs[codepage] != state.docsmode:
                yield ("RDOCS", graphdata.chcpdocs[codepage], None, None)
            yield ("CHCP", codepage)
        else:
            yield token

