#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/. 

# Handles prefixed diacritics, à la T.51 (and friends), ANSEL etc.

def handle_prefix_diacritics(stream, state):
    tseq = []
    cseq = []
    bank = []
    for token in stream:
        if token[0] == "CHAR" and token[1] < 0:
            tseq.append(token)
            cseq.insert(0, -token[1])
        elif tseq:
            if token[0] == "ENDSTREAM":
                yield from iter(tseq)
                yield from iter(bank)
                yield token
                return
            elif token[0] != "CHAR":
                bank.append(token)
            else:
                tseq.append(token)
                cseq.insert(0, token[1])
                yield ("COMPCHAR", tuple(cseq), tuple(tseq))
                yield from iter(bank)
                del tseq[:] ; del cseq[:] ; del bank[:]
        else:
            yield token

