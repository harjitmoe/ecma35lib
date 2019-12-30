#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Completely private (hence in col 3); should come up with some way to config this.
shiftjisdocs = ("DOCS", False, (0x30,))

def decode_shiftjis(stream, state):
    sjis_lead = None
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if (token[0] == "DOCS"):
            if sjis_lead:
                yield ("ERROR", "SJISTRUNC", sjis_lead)
                sjis_lead = None
            if token == shiftjisdocs:
                yield ("RDOCS", "Shift_JIS", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "shift_jis"
                # Sensible-ish defaults (entirety of ir159 is inaccessible)
                state.cur_gsets = ["ir014", "ir168web", "ir013", "nil"]
            else:
                yield token
        elif state.docsmode == "shift_jis" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if sjis_lead is None:
                if token[1] < 0x20:
                    yield ("C0", token[1], "CL")
                elif token[1] < 0x80:
                    yield ("GL", token[1] - 0x20)
                elif token[1] == 0x80:
                    yield ("G2", 0x40, "SJISONEBYTE")
                elif token[1] < 0xA0:
                    sjis_lead = token
                elif token[1] == 0xA0:
                    yield ("G2", 0x41, "SJIS")
                elif token[1] < 0xE0:
                    yield ("G2", token[1] - 0xA0, "SJISONEBYTE")
                elif token[1] < 0xFD:
                    sjis_lead = token
                else:
                    yield ("G2", token[1] - 0xFD + 0x42, "SJISONEBYTE")
            else:
                if token[1] < 0x40 or token[1] > 0xFC or token[1] == 0x7F:
                    yield ("ERROR", "SJISTRUNC", sjis_lead)
                    sjis_lead = None
                    reconsume = token
                    continue
                leadoffset = 0x81 if sjis_lead[1] < 0xA0 else 0xC1
                trailoffset = 0x40 if token[1] < 0x80 else 0x41
                pointer = ((sjis_lead[1] - leadoffset) * 94 * 2) + (token[1] - trailoffset)
                ku = (pointer // 94) + 1
                ten = (pointer % 94) + 1
                if ku <= 94:
                    yield ("G1", ku, "SJIS")
                    yield ("G1", ten, "SJIS")
                elif ku <= 103:
                    yield ("G3", (1, 8, 3, 4, 5, 12, 13, 14, 15)[ku - 94], "SJIS")
                    yield ("G3", ten, "SJIS")
                else:
                    yield ("G3", ku - 104 + 78, "SJIS")
                    yield ("G3", ten, "SJIS")
                sjis_lead = None
            #
        else:
            yield token
        #
    #
#








