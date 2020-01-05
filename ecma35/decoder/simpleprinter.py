#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def simple_print(stream, state):
    for token in stream:
        if token[0] == "CHAR" and token[1]:
            if token[5][:3] == "WTF": # wobbly UTF, i.e. an isolated surrogate
                print(end = "\uFFFD")
            elif token[1] >= 0:
                print(end = chr(token[1]))
            else:
                raise ValueError("prefix diacritics unhandled")
        elif token[0] == "COMPCHAR":
            if token[1][0] >= 0:
                print(end = "".join(chr(i) for i in token[1]))
            else:
                raise ValueError("prefix diacritics unhandled")
        elif token[0] in ("RAWBYTE",):
            print(end = "[{:02X}]".format(token[1]))
        elif token[0] == "CTRL" and token[1] == "LF":
            print()
        elif token[0] == "CTRL" and token[1] == "SP":
            print(end = " ")
        elif token[0] == "CTRL" and token[1] in ("SI", "SO", "LS0", "LS1", "LS2", "LS3",
                                                 "LS1R", "LS2R", "LS3R"):
            pass
        elif token[0] in ("DESIG", "RDESIG", "BOM", "DOCS", "RDOCS", "SINGLEOVER", "SCSUSHIFT",
                          "SCSUDESIG", "C0GRAPH", "CHCP"):
            pass
        elif token[0] == "ERROR":
            print(end = "\uFFFD")
        else:
            print(end = "\uFFFC")
        yield token
    print()
    print()
