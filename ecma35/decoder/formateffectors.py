#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/. 

from ecma35.data import controldata

def format_effectors(stream, state):
    # Format effectors hold an interesting status. Standing between
    #   a true control code (due to changing renderer behaviour without
    #   displaying) and a graphical character (due to counting as part
    #   of the content, and affecting only the renderer), they can
    #   appear in both graphical sets (such as UCS) and control sets.
    # For example, BPH appears in a control code set (ECMA-48), while
    #   ZWSP appears in a graphical character set (UCS), despite doing
    #   essentially the same thing, give or take.  The same applieth to
    #   their antonyms (NBH and WJ), to DINOSC versus ISO 8859's SHY,
    #   and so forth.
    # Moreover, MARC-8 makes two of its C1 codes explicitly map to
    #   UCS's ZWJ and ZWNJ when transcoded to Unicode.
    # Accordingly, format effectors which appear as CHAR tags should
    #   be converted to CTRL tags.
    for token in stream:
        if token[0] == "CHAR" and token[1] in controldata.formats:
            yield ("CTRL", controldata.formats[token[1]], token[2], token[3], token[4], token[5])
        else:
            yield token

