#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2022.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.gccdata import bs_handle

def proc_bs_sequences(stream, state):
    mode = "normal"
    reconsume = None
    stack = []
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if token[0] in ("CHAR", "COMPCHAR") and not (len(stack) % 2):
            stack.append(token)
        elif token[:2] == ("CTRL", "BS") and len(stack) % 2:
            stack.append(token)
        elif stack:
            if len(stack) <= 2 or any(i[0] == "CHAR" and i[1] < 0 for i in stack) or any(
                    i[0] == "COMPCHAR" and
                    any(j < 0 for j in i[1])
                    for i in stack):
                yield from stack
            else:
                charses = tuple(chr(i[1]) if i[0] == "CHAR" else "".join(map(chr, i[1]))
                                for i in stack if i[0] != "CTRL")
                output = bs_handle(charses)
                yield ("COMPCHAR", tuple(map(ord, output)), tuple(stack))
            stack.clear()
            reconsume = token
        else:
            yield token



