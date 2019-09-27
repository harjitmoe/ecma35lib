#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

def simple_print(stream):
    for token in stream:
        if token[0] == "CHAR" and token[1]:
            print(end = chr(token[1]))
        elif token[0] in ("RAWBYTE",):
            print(end = "[{:02X}]".format(token[1]))
        elif token[0] == "CTRL" and token[1] == "LF":
            print()
        elif token[0] == "CTRL" and token[1] == "SP":
            print(end = " ")
        elif token[0] == "CTRL" and token[1] in ("SI", "SO", "LS0", "LS1", "LS2", "LS3",
                                                 "LS1R", "LS2R", "LS3R"):
            pass
        elif token[0] in ("DESIG", "RDESIG", "BOM", "DOCS", "RDOCS", "SINGLEOVER"):
            pass
        elif token[0] == "ERROR":
            print(end = "\uFFFD")
        else:
            print(end = "\uFFFC")
        yield token
    print()
    print()
