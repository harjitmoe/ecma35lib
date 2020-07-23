#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Must be at the end of the chain. Yields points of deviance for a
# known test string.

from ecma35.data import controldata

def simple_comparator_maker(target_string):
    target = iter(target_string)
    def simple_comparator(stream, state):
        for token in stream:
            if token[0] == "CHAR" and token[1]:
                expected = next(target)
                if token[1] != ord(expected):
                    yield (expected, token)
                else:
                    yield (expected, "SUCCESS")
            elif token[0] == "COMPCHAR":
                for i in token[1]:
                    expected = next(target)
                    assert isinstance(i, int), i
                    if i != ord(expected):
                        yield (expected, token)
                    else:
                        yield (expected, "SUCCESS")
            elif token[0] in ("RAWBYTE",):
                yield (next(target), token)
            elif token[0] == "CTRL" and token[1] == "LF":
                expected = next(target)
                if expected != "\n":
                    yield (expected, token)
                else:
                    yield (expected, "SUCCESS")
            elif token[0] == "CTRL" and token[1] in controldata.rformats:
                expected = next(target)
                if expected != chr(controldata.rformats[token[1]]):
                    yield (expected, token)
                else:
                    yield (expected, "SUCCESS")
            elif token[0] == "CTRL":
                expected = next(target)
                if ord(expected) >= 0x20 and not (0x7F <= ord(expected) < 0xA0):
                    yield (expected, token)
                else:
                    yield (expected, "SUCCESS")
            elif token[0] in ("DESIG", "RDESIG", "BOM", "DOCS", "RDOCS", "SINGLEOVER", "SCSUSHIFT",
                              "SCSUDESIG", "C0GRAPH", "CHCP"):
                # In-band logging of code features used; does not correspond to anything in reference Unicode.
                pass
            elif token[0] == "ERROR":
                yield (next(target), token)
                return # Fatal: can't keep in sync, ERROR could correspond to zero or more reference codepoints.
            else:
                yield (next(target), token)
    return simple_comparator

