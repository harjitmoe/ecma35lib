#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# DOCS filter for HangulTalk.

from ecma35.data.multibyte import korea

elexdocs = ("DOCS", False, (0x36,))

def decode_elex(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    elex_lead = None
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if (token[0] == "DOCS"):
            if token == elexdocs:
                yield ("RDOCS", "ELEX", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "elex"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "ir149", "ir013win", "mac-elex-extras"]
                state.is_96 = [0, 0, 0, 0]
            else:
                yield token
        elif state.docsmode == "elex" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20:
                if elex_lead is not None:
                    yield ("ERROR", "ELEXTRUNCATE", elex_lead[1])
                    elex_lead = None
                yield ("C0", token[1], "CL")
            elif 0x80 <= token[1] < 0xA0:
                if elex_lead is not None:
                    yield ("ERROR", "ELEXTRUNCATE", elex_lead[1])
                    elex_lead = None
                yield ("C1", token[1] - 0x80, "CR")
            elif elex_lead is None: # i.e. the current one is a lead (or single) byte
                if token[1] < 0x80:
                    if (not state.is_96[state.glset]) and (token[1] == 0x20):
                        yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                    elif (not state.is_96[state.glset]) and (token[1] == 0x7F):
                        yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                    else:
                        yield (workingsets[state.glset], token[1] - 0x20, "GL")
                elif token[1] == 0xA0: # TODO fix this
                    yield ("G2", 0x40, "ELEX1BYTE")
                elif token[1] == 0xFF:
                    yield ("G2", 0x48, "ELEX1BYTE")
                else:
                    elex_lead = token
            elif 0xA1 <= token[1] <= 0xFE:
                # Ordinary EUC code: treat normally.
                yield (workingsets[state.grset], elex_lead[1] - 0xA0, "GR")
                yield (workingsets[state.grset], token[1] - 0xA0, "GR")
                elex_lead = None
            elif (0x41 <= token[1] <= 0x7D) or (0x81 <= token[1] <= 0xA0):
                row_number = elex_lead[1] - 0xA0
                cell_number = token[1] - 0x40
                if token[1] > 0x7D:
                    cell_number -= 3
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








