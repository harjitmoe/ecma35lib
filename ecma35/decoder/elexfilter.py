#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2023/2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# DOCS filter for HangulTalk, aka MacKorean, aka MacOS-KH, aka x-mac-korean.
# Developed by Elex Computer (il'lek'seu) and easily the most annoying of
#   all four MacOS encodings to document, both in terms of colliding with 
#   UHC but with irreconcileable structures so there's no elegant way of 
#   even charting the collisions, and in terms of including a tonne of 
#   stylised arrows, enclosed forms and miscellaneous geometric dingbats 
#   without Unicode mappings (some of the arrows have mappings 
#   post-Unicode-7.0 due to the Wingdings 3 repertoire, but the mapping 
#   file has not been updated on this front). Apple's use of 
#   Private Use Area "encoding hints" as variation selectors really 
#   becomes very prominent here, but even then some end up mapped straight 
#   to PUA as base characters.

from ecma35.data import graphdata
from ecma35.data.multibyte import korea

def decode_elex(stream, state):
    workingsets = graphdata.workingsets
    elex_lead = None
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if (token[0] == "RDOCS"):
            if token[1] == "elex":
                state.bytewidth = 1
                state.docsmode = "elex"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir149/mac", "ir013/mac", "mac-elex-extras"]
                state.is_96 = [0, 0, 0, 0]
                state.cur_gsets.extend(graphdata.initial_gsets[len(state.cur_gsets):])
                state.is_96.extend(graphdata.initial_gsets[len(state.is_96):])
            yield token
        elif state.docsmode == "elex" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                if elex_lead is not None:
                    yield ("ERROR", "ELEXTRUNCATE", elex_lead[1])
                    elex_lead = None
                yield ("C0", token[1], "CL")
            # 0x80 thru 0x84 (per Apple) or 0x81 thru 0x83 (per Lunde) are used for graphics
            # Additionally, the C1 range is used as trail bytes.
            elif (0x85 <= token[1] < 0xA0) and (elex_lead is None):
                yield ("C1", token[1] - 0x80, "CR")
            elif elex_lead is None: # i.e. the current one is a lead (or single) byte
                if token[1] < 0x80:
                    if (not state.is_96[state.glset]) and (token[1] == 0x20):
                        yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                    elif (not state.is_96[state.glset]) and (token[1] == 0x7F):
                        yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                    else:
                        yield (workingsets[state.glset], token[1] - 0x20, "GL")
                elif token[1] == 0x80:
                    yield ("G2", 0x41, "ELEX1BYTE")
                elif token[1] == 0x81:
                    yield ("G2", 0x48, "ELEX1BYTE")
                elif token[1] == 0x82:
                    yield ("G2", 0x49, "ELEX1BYTE")
                elif token[1] == 0x83:
                    yield ("G2", 0x42, "ELEX1BYTE")
                elif token[1] == 0x84:
                    yield ("G2", 0x4A, "ELEX1BYTE")
                elif token[1] == 0xA0:
                    yield ("G2", 0x4B, "ELEX1BYTE")
                elif token[1] == 0xFF:
                    yield ("G2", 0x44, "ELEX1BYTE")
                else:
                    elex_lead = token
            elif 0xA1 <= token[1] <= 0xFE:
                # Ordinary EUC code: treat normally.
                yield (workingsets[state.grset], elex_lead[1] - 0xA0, "GR")
                yield (workingsets[state.grset], token[1] - 0xA0, "GR")
                elex_lead = None
            elif (0x41 <= token[1] <= 0x7D) or (0x81 <= token[1] <= 0xA0) or (token[1] == 0xFF):
                row_number = elex_lead[1] - 0xA0
                if token[1] == 0xFF:
                    cell_number = 94
                elif token[1] > 0x7D:
                    cell_number = (token[1] - 0x40) - 3
                else:
                    cell_number = token[1] - 0x40
                yield ("G3", row_number, "ELEXEXTRAS")
                yield ("G3", cell_number, "ELEXEXTRAS")
                elex_lead = None
            else:
                yield ("ERROR", "ELEXTRUNCATE", elex_lead[1])
                elex_lead = None
                reconsume = token # Note: token being reconsumed is a non-letter single byte code.
        else:
            yield token
        #
    #
#








