#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# DOCS filter for Unified Hangul Code (what WHATWG calls EUC-KR).

from ecma35.data.multibyte import korea

uhcdocs = ("DOCS", False, (0x31,))

def decode_uhc(stream, state):
    uhc_lead = None
    reconsume = None
    while 1:
        token = (next(stream) if reconsume is None else reconsume)
        reconsume = None
        if (token[0] == "DOCS"):
            if token == uhcdocs:
                yield ("RDOCS", "UHC", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "uhc"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir149", "nil", "nil"]
            else:
                yield token
        elif state.docsmode == "uhc" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                yield ("C0", token[1], "CL")
            elif uhc_lead is None: # i.e. the current one is a lead (or single) byte
                if token[1] < 0x80:
                    yield ("GL", token[1] - 0x20)
                elif token[1] == 0x80:
                    yield ("G2", 0x40) # TODO review what to actually do here
                elif token[1] == 0xFF:
                    yield ("G2", 0x41) # TODO review what to actually do here
                else:
                    uhc_lead = token
            elif (0xA1 <= token[1] <= 0xFE) and (0xA1 <= uhc_lead[1] <= 0xFE):
                # Ordinary EUC code: treat normally.
                yield ("GR", uhc_lead[1] - 0xA0)
                yield ("GR", token[1] - 0xA0)
                uhc_lead = None
            elif (0x41 <= token[1] <= 0x5A) or (0x61 <= token[1] <= 0x7A) or (
                  0x81 <= token[1] <= 0xFE):
                row_number = uhc_lead[1] - 0x81
                prev_rows_next_to_wansung = (uhc_lead[1] - 0xA1) if uhc_lead[1] >= 0xA1 else 0
                index = (row_number * 178) - (prev_rows_next_to_wansung * 94)
                if token[1] <= 0x5A:
                    index += (token[1] - 0x41)
                elif token[1] <= 0x7A:
                    index += 26 + (token[1] - 0x61)
                else:
                    index += 52 + (token[1] - 0x81)
                if index < len(korea.non_wangsung_johab):
                    yield ("CHAR", korea.non_wangsung_johab[index], 
                           "UHCext", (index,), "UHC", "UHCext")
                    uhc_lead = None
                else:
                    # Following the UHC structure but beyond the region used.
                    # TODO is this the appropriate response?
                    yield ("ERROR", "UHCTRUNCATE", uhc_lead[1])
                    uhc_lead = None
                    reconsume = token
            else:
                yield ("ERROR", "UHCTRUNCATE", uhc_lead[1])
                uhc_lead = None
                reconsume = token # Note: token being reconsumed is a non-letter single byte code.
        else:
            yield token
        #
    #
#








