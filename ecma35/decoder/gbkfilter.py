#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Very incomplete filter for GBK.

from ecma35.data.multibyte import guobiao

gbkdocs = ("DOCS", False, (0x32,))

def decode_gbk(stream, state):
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
                state.cur_gsets = ["ir006", "ir058", "nil", "nil"]
            else:
                yield token
        elif state.docsmode == "gbk" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                yield ("C0", token[1], "CL")
            elif gbk_lead is None: # i.e. the current one is a lead (or single) byte
                if token[1] < 0x80:
                    yield ("GL", token[1] - 0x20)
                elif token[1] == 0x80:
                    yield ("G2", 0x40) # TODO review what to actually do here
                elif token[1] == 0xFF:
                    yield ("G2", 0x41) # TODO review what to actually do here
                else:
                    gbk_lead = token
            elif (0xA1 <= token[1] <= 0xFE) and (0xA1 <= gbk_lead[1] <= 0xFE):
                # Ordinary EUC code: treat normally.
                yield ("GR", gbk_lead[1] - 0xA0)
                yield ("GR", token[1] - 0xA0)
                gbk_lead = None
            elif (0x81 <= gbk_lead[1] <= 0xA0) and (
                          (0x40 <= token[1] <= 0x7E) or (0x80 <= token[1] <= 0xFE)):
                row_number = gbk_lead[1] - 0x81
                index = (row_number * 190) + (token[1] - 0x40)
                if token[1] > 0x7F:
                    index -= 1
                yield ("UCS", guobiao.non_euccn_uro101[index], "GBK", "GBK/3")
                gbk_lead = None
            elif (0xAA <= gbk_lead[1] <= 0xFE) and (
                          (0x40 <= token[1] <= 0x7E) or (0x80 <= token[1] <= 0xA0)):
                row_number = gbk_lead[1] - 0xAA
                index = (0x20 * 190) + (row_number * 96) + (token[1] - 0x40)
                if token[1] > 0x7F:
                    index -= 1
                #
                if index < len(guobiao.non_euccn_uro101):
                    yield ("UCS", guobiao.non_euccn_uro101[index], "GBK", "GBK/4")
                    gbk_lead = None
                else:
                    # TODO: the non-URO part of GBK/4
                    yield ("ERROR", "NOT_IMPLEMENTED", gbk_lead[1], token[1])
                    gbk_lead = None
            elif (0xA1 <= gbk_lead[1] <= 0xA9) and (
                          (0x40 <= token[1] <= 0x7E) or (0x80 <= token[1] <= 0xA0)):
                # TODO: the GBK/5 level and associated private use region
                yield ("ERROR", "NOT_IMPLEMENTED", gbk_lead[1], token[1])
                gbk_lead = None
            else:
                yield ("ERROR", "UHCTRUNCATE", gbk_lead[1])
                gbk_lead = None
                reconsume = token # Note: token being reconsumed is a non-letter single byte code.
        else:
            yield token
        #
    #
#








