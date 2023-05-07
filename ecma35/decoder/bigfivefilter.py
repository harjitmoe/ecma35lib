#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.multibyte import traditional

def decode_bigfive(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    big5_lead = None
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if (token[0] == "RDOCS"):
            if token[1] in ("bigfive", "bigfivenarrow"):
                state.bytewidth = 1
                state.docsmode = token[1]
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir171/ms", "cns-eucg2-ms", "hkscs"]
                state.is_96 = [0, 0, 0, 0]
            yield token
        elif state.docsmode in ("bigfive", "bigfivenarrow") and token[0] == "WORD":
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
                elif (token[1] in (0x80, 0xFF)) or ((state.docsmode == "bigfivenarrow") and
                                                  (token[1] in (0x81, 0x82, 0xA0, 0xFD, 0xFE))):
                    if graphdata.gsets[state.cur_gsets[3]][1] != 1:
                        yield ("ERROR", "BIG5UNUSEDBYTE")
                    elif token[1] == 0x80:
                        yield ("G3", 0x40, "BIG5ONEBYTE")
                    elif token[1] == 0xA0:
                        yield ("G3", 0x41, "BIG5MONEBYTE")
                    elif token[1] == 0xFD:
                        yield ("G3", 0x42, "BIG5MONEBYTE")
                    elif token[1] == 0xFE:
                        yield ("G3", 0x42, "BIG5MONEBYTE")
                    elif (token[1] == 0xFF) and (state.docsmode == "bigfivenarrow"):
                        yield ("G3", 0x44, "BIG5MONEBYTE")
                    elif token[1] == 0x81:
                        yield ("G3", 0x46, "BIG5MONEBYTE")
                    elif token[1] == 0x82:
                        yield ("G3", 0x47, "BIG5MONEBYTE")
                    else:
                        assert token[1] == 0xFF
                        yield ("G3", 0x49, "BIG5ONEBYTE")
                else:
                    big5_lead = token
            elif (0x40 <= token[1] <= 0xFE) and (token[1] != 0x7F):
                number = (big5_lead[1] << 8) | token[1]
                if "BIG5:IBMCOMPATKANJI" in graphdata.gsetflags[state.cur_gsets[2]]:
                    # Compatibility ideographs mapped to IBM's nonstandard plane 13
                    big5_to_cns2 = traditional.big5_to_cns2_ibmvar
                else:
                    big5_to_cns2 = traditional.big5_to_cns2
                #
                if (((number < 0xA140) or (0xC6A1 <= number < 0xC940) or (number >= 0xF9D6)) and
                        (graphdata.gsets[state.cur_gsets[3]][1] == 2)):
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
                elif number in traditional.big5_to_cns1:
                    for i in traditional.big5_to_cns1[number]:
                        yield ("G1", i, "Big5")
                        big5_lead = None
                elif number in big5_to_cns2:
                    for i in big5_to_cns2[number]:
                        yield ("G2", i, "Big5")
                        big5_lead = None
                else:
                    yield ("ERROR", "BIG5NOEUCMAPPING")
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








