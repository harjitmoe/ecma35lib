#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# DOCS filter for GBK, also generating GBHALFCODE tokens for GB18030.

from ecma35.data.multibyte import guobiao

gbkdocs = ("DOCS", False, (0x32,))

def decode_gbk(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    gbk_lead = None
    reconsume = None
    while 1:
        token = (next(stream) if reconsume is None else reconsume)
        reconsume = None
        if (token[0] == "DOCS"):
            if token == gbkdocs:
                yield ("RDOCS", "GBK", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "gbk"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir058-2005", "ir013euro", "nil"]
                state.is_96 = [0, 0, 0, 0]
            else:
                yield token
        elif state.docsmode == "gbk" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                yield ("C0", token[1], "CL")
            elif gbk_lead is None: # i.e. the current one is a lead (or single) byte
                if token[1] < 0x80:
                    if (not state.is_96[state.glset]) and (token[1] == 0x20):
                        yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                    elif (not state.is_96[state.glset]) and (token[1] == 0x7F):
                        yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                    else:
                        yield (workingsets[state.glset], token[1] - 0x20, "GL")
                elif token[1] == 0x80:
                    if state.cur_gsets[2] == "ir013win":
                        yield ("C1", 0x00, "GBK1BYTE")
                    else:
                        yield ("G2", 0x40, "GBK1BYTE")
                elif token[1] == 0xFF:
                    yield ("G2", 0x46, "GBK1BYTE")
                else:
                    gbk_lead = token
            elif (0xA1 <= token[1] <= 0xFE) and (0xA1 <= gbk_lead[1] <= 0xFE):
                # Ordinary EUC code ("Level 1" / "Level 2"): treat normally.
                yield (workingsets[state.grset], gbk_lead[1] - 0xA0, "GR")
                yield (workingsets[state.grset], token[1] - 0xA0, "GR")
                gbk_lead = None
            elif (0x81 <= gbk_lead[1] <= 0xA0) and (
                          (0x40 <= token[1] <= 0x7E) or (0x80 <= token[1] <= 0xFE)):
                # "Level 3"
                row_number = gbk_lead[1] - 0x81
                index = (row_number * 190) + (token[1] - 0x40)
                if token[1] > 0x7F:
                    index -= 1
                yield ("UCS", guobiao.non_euccn_uro101[index], "GBK", "GBK/3")
                gbk_lead = None
            elif (0xAA <= gbk_lead[1] <= 0xFE) and (
                          (0x40 <= token[1] <= 0x7E) or (0x80 <= token[1] <= 0xA0)):
                # "Level 4"
                row_number = gbk_lead[1] - 0xAA
                index = (0x20 * 190) + (row_number * 96) + (token[1] - 0x40)
                if token[1] > 0x7F:
                    index -= 1
                #
                if index < len(guobiao.non_euccn_uro101):
                    yield ("UCS", guobiao.non_euccn_uro101[index], "GBK", "GBK/4")
                    gbk_lead = None
                else:
                    exception_index = 192 + index - len(guobiao.non_euccn_uro101)
                    if state.cur_gsets[1] != "ir058-full":
                        yield ("UCS", guobiao.gbk_exceptions[exception_index], "GBK", "GBK/4+")
                    else:
                        yield ("UCS", guobiao.gbk_exceptions_full[exception_index], "GBK", "GBK/4+")
                    gbk_lead = None
            elif (0xA1 <= gbk_lead[1] <= 0xA9) and (
                          (0x40 <= token[1] <= 0x7E) or (0x80 <= token[1] <= 0xA0)):
                # "Level 5"
                row_number = gbk_lead[1] - 0xA1
                extra_index = (row_number * 96) + (token[1] - 0x40)
                if token[1] > 0x7F:
                    extra_index -= 1
                #
                if extra_index < (96 * 7):
                    if (extra_index == (0xE5E5 - 0xE4C6)) and (
                            state.cur_gsets[1] in ("ir058-web", "ir058-full")):
                        yield ("UCS", 0x3000, "GBK", "GBK/UDC3")
                    else:
                        yield ("UCS", 0xE4C6 + extra_index, "GBK", "GBK/UDC3")
                else:
                    exception_index = extra_index - (96 * 7)
                    assert exception_index < 192
                    yield ("UCS", guobiao.gbk_exceptions[exception_index], "GBK", "GBK/5")
                gbk_lead = None
            elif (0x81 <= gbk_lead[1] <= 0xFE) and (0x30 <= token[1] <= 0x39):
                # GB18030 half-code
                pointer = ((gbk_lead[1] - 0x81) * 10) + (token[1] - 0x30)
                yield ("GBHALFCODE", pointer)
                gbk_lead = None
            else:
                yield ("ERROR", "GBKTRUNCATE", gbk_lead[1])
                gbk_lead = None
                reconsume = token # Note: token being reconsumed is a non-letter single byte code.
        else:
            yield token
        #
    #
#








