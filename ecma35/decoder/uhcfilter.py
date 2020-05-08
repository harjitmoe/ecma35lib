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
    workingsets = ("G0", "G1", "G2", "G3")
    uhc_lead = None
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
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
                state.cur_gsets = ["ir006", "ir149", "ir013win", "2011kpsextras"]
                state.is_96 = [0, 0, 0, 0]
            else:
                yield token
        elif state.docsmode == "uhc" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                yield ("C0", token[1], "CL")
            elif uhc_lead is None: # i.e. the current one is a lead (or single) byte
                if token[1] < 0x80:
                    if (not state.is_96[state.glset]) and (token[1] == 0x20):
                        yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                    elif (not state.is_96[state.glset]) and (token[1] == 0x7F):
                        yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                    else:
                        yield (workingsets[state.glset], token[1] - 0x20, "GL")
                elif token[1] == 0x80:
                    if state.cur_gsets[2] == "ir013win":
                        yield ("C1", 0x00, "UHC1BYTE")
                    else:
                        yield ("G2", 0x40, "UHC1BYTE")
                elif token[1] == 0xFF:
                    yield ("G2", 0x48, "UHC1BYTE")
                else:
                    uhc_lead = token
            elif (0xA1 <= uhc_lead[1] <= 0xFE) and (0xA1 <= token[1] <= 0xFE):
                # Ordinary EUC code: treat normally.
                yield (workingsets[state.grset], uhc_lead[1] - 0xA0, "GR")
                yield (workingsets[state.grset], token[1] - 0xA0, "GR")
                uhc_lead = None
            elif (0x41 <= token[1] <= 0x5A) or (0x61 <= token[1] <= 0x7A) or (
                  0x81 <= token[1] <= 0xFE):
                row_number = uhc_lead[1] - 0x81
                prev_rows_next_to_wansung = (uhc_lead[1] - 0xA1) if uhc_lead[1] >= 0xA1 else 0
                index = ref_index = (row_number * 178) - (prev_rows_next_to_wansung * 94)
                if token[1] <= 0x5A:
                    index += (token[1] - 0x41)
                elif token[1] <= 0x7A:
                    index += 26 + (token[1] - 0x61)
                else:
                    index += 52 + (token[1] - 0x81)
                if (state.cur_gsets[1] in ("ir149", "ir149-mac")) and (
                      index < len(korea.non_wangsung_johab)):
                    yield ("CHAR", korea.non_wangsung_johab[index], 
                           "ExtWansung", (0, index), "UHC", "UHCext")
                    uhc_lead = None
                elif (state.cur_gsets[1] in ("ir202", "ir202-2003", "ir202-2011", "ir202-full")) and (
                      index < len(korea.non_kps9566_johab)):
                    yield ("CHAR", korea.non_kps9566_johab[index], 
                           "ExtKPS9566", (0, index), "UHC", "UHCext")
                    uhc_lead = None
                elif uhc_lead[1] >= 0xC8:
                    yield ("G3", uhc_lead[1] + 1 - 0xC8, "UHCBEYONDEXT")
                    yield ("G3", index + 1 - ref_index, "UHCBEYONDEXT")
                    uhc_lead = None
                else:
                    # Following the UHC structure but beyond the region used.
                    # TODO is this the appropriate response?
                    yield ("ERROR", "UHCTRUNCATE", uhc_lead[1])
                    uhc_lead = None
                    reconsume = token
            elif (uhc_lead[1] == 0xAE) and (token[1] == 0xFF) and (state.cur_gsets[1] in ("ir202-2003", "ir202-full")):
                # Encoding of ÿ.
                yield ("CHAR", 0xFF, "ExtKPS9566", (14, 95), "UHC", "UHCext")
                uhc_lead = None
            else:
                yield ("ERROR", "UHCTRUNCATE", uhc_lead[1])
                uhc_lead = None
                reconsume = token # Note: token being reconsumed is a non-letter single byte code.
        else:
            yield token
        #
    #
#








