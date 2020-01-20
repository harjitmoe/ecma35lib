#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import traditional

bigfivedocs = ("DOCS", False, (0x34,))

def decode_bigfive(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    big5_lead = None
    reconsume = None
    while 1:
        token = (next(stream) if reconsume is None else reconsume)
        reconsume = None
        if (token[0] == "DOCS"):
            if token == bigfivedocs:
                yield ("RDOCS", "BIGFIVE", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "bigfive"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir171", "cns-eucg2", "hkscs"]
                state.is_96 = [0, 0, 0, 0]
            else:
                yield token
        elif state.docsmode == "bigfive" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                yield ("C0", token[1], "CL")
            elif big5_lead is None: # i.e. the current one is a lead (or single) byte
                if token[1] < 0x80:
                    if (not state.is_96[state.glset]) and (token[1] == 0x20):
                        yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                    elif (not state.is_96[state.glset]) and (token[1] == 0x7F):
                        yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                    else:
                        yield (workingsets[state.glset], token[1] - 0x20, "GL")
                elif token[1] == 0x80:
                    yield ("ERROR", "BIG5UNUSEDBYTE")
                elif token[1] == 0xFF:
                    yield ("ERROR", "BIG5UNUSEDBYTE")
                else:
                    big5_lead = token
            elif (0x40 <= token[1] <= 0xFE) and (token[1] != 0x7F):
                number = (big5_lead[1] << 8) | token[1]
                if number in traditional.big5_to_cns1:
                    for i in traditional.big5_to_cns1[number]:
                        yield ("G1", i, "Big5")
                        big5_lead = None
                elif number in traditional.big5_to_cns2:
                    for i in traditional.big5_to_cns2[number]:
                        yield ("G2", i, "Big5")
                        big5_lead = None
                elif (number < 0xA140) or (0xC6A1 <= number < 0xC940) or (number >= 0xF9D6):
                    extku = big5_lead[1] - 0x81 + 1
                    extten = (token[1] - 0x40) + 1 if token[1] < 0x7F else (token[1] - 0xA1 + 63) + 1
                    if number < 0xA140:
                        pass
                    elif number < 0xC940:
                        extku -= 37
                    else:
                        extku -= 85
                    #
                    if extten <= 63:
                        ku = (extku * 2) - 1
                        ten = (extten - 63) + 94
                    else:
                        ku = extku * 2
                        ten = extten - 63
                    yield ("G3", ku, "Big5")
                    yield ("G3", ten, "Big5")
                    big5_lead = None
            else:
                yield ("ERROR", "BIG5TRUNCATE", big5_lead[1])
                big5_lead = None
                reconsume = token
                continue
        else:
            yield token
        #
    #
#








