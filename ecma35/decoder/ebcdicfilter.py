#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Filter for EBCDIC. The ranges used by most non-256/500-based DP94 base sets are used as the GL
# area, mapped in accordance with code page 38 (like 500 ASCII subset, but the ASCII vbar is 0x6A).

# Key point is that the ranges of e.g. code page 38 or CCSID 8229 or most non-500-based DP94s should
#   map to GL as ISO 646 or pseudo ISO 646 sets. The remaining 96 graphical positions are mapped
#   per `dd`'s `ibm` conversion (which, when combined with the code page 38 mapping for ASCII, is
#   actually reversible, unlike with the CCSID 5143 mapping it actually uses for some reason), but
#   with the mappings for EBCDIC 0xE1 and EBCDIC 0xFF swapped in accordance with changes to the
#   mappings for EBCDIC control codes made in 1986 (U+009F maps to EO at 0xFF now, not NSP at 0xE1).
#   With the exception of the business with 0xE1, this is a simple sequential mapping of GR to the
#   non-DP94 ranges.
# Note also that EBCDIC encodings of the 65th control code other than 0xE1 and 0xFF exist: the XHCS
#   manual from Siemens/Fujitsu lists (non-IBM) EBCDIC code pages that freely assign 0xFF to normal
#   graphical chars without batting an eyelid, although they generally have at least one
#   unassignable position (usually but not always including 0x5F) elsewhere in the graphical region:
#     https://bs2manuals.ts.fujitsu.com/download/manual/3085.5
#   In these cases, U+009F does indeed map to 0x5F (not to 0xE1 or 0xFF):
#     https://www.iana.org/assignments/charset-reg/OSD-EBCDIC-DF04-1
# For this reason, the position of the 65th control code (U+009F) is made configurable below; the
#   mapping itself is in given in terms of 0xFF as a sensible default (applicable to post-1986 code
#   page 37, for example).
conv_map = [0, 1, 2, 3, 156, 9, 134, 127, 151, 141, 142, 11, 12, 13, 14, 15, 16, 17, 18, 19, 157, 133, 8, 135, 24, 25, 146, 143, 28, 29, 30, 31, 128, 129, 130, 131, 132, 10, 23, 27, 136, 137, 138, 139, 140, 5, 6, 7, 144, 145, 22, 147, 148, 149, 150, 4, 152, 153, 154, 155, 20, 21, 158, 26, 32, 160, 161, 162, 163, 164, 165, 166, 167, 168, 91, 46, 60, 40, 43, 33, 38, 169, 170, 171, 172, 173, 174, 175, 176, 177, 93, 36, 42, 41, 59, 94, 45, 47, 178, 179, 180, 181, 182, 183, 184, 185, 124, 44, 37, 95, 62, 63, 186, 187, 188, 189, 190, 191, 192, 193, 194, 96, 58, 35, 64, 39, 61, 34, 195, 97, 98, 99, 100, 101, 102, 103, 104, 105, 196, 197, 198, 199, 200, 201, 202, 106, 107, 108, 109, 110, 111, 112, 113, 114, 203, 204, 205, 206, 207, 208, 209, 126, 115, 116, 117, 118, 119, 120, 121, 122, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 123, 65, 66, 67, 68, 69, 70, 71, 72, 73, 232, 233, 234, 235, 236, 237, 125, 74, 75, 76, 77, 78, 79, 80, 81, 82, 238, 239, 240, 241, 242, 243, 92, 255, 83, 84, 85, 86, 87, 88, 89, 90, 244, 245, 246, 247, 248, 249, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 250, 251, 252, 253, 254, 159]

import sys
from ecma35.data import graphdata

ebcdicdocs = ("DOCS", True, (0x36,))

def decode_ebcdic(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    dbcs_lead = None
    seeking_65th_control_code = None
    for token in stream:
        if dbcs_lead and (token[0] != "WORD" or state.docsmode != "ebcdic"):
            yield ("ERROR", "DBEBCDICTRUNCATE", dbcs_lead)
            dbcs_lead = None
            # Fall through.
        #
        if seeking_65th_control_code:
            if state.docsmode == "ebcdic" and token[0] == "WORD":
                if token[1] <= 0x40:
                    yield ("ERROR", "SEEK65THNOTVALID", (seeking_65th_control_code, token))
                    seeking_65th_control_code = None
                    # Fall through
                else:
                    yield ("SET65THCONTROL", token[1])
                    state.ebcdic_65th_control_code = token[1]
                    seeking_65th_control_code = None
                    continue
            else:
                yield ("ERROR", "SEEK65THTRUNCATE", seeking_65th_control_code)
                seeking_65th_control_code = None
                # Fall through.
        #
        if (token[0] == "DOCS"):
            if token == ebcdicdocs:
                yield ("RDOCS", "ebcdic", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "ebcdic"
                state.cur_c0 = "ir001"
                state.cur_c1 = "c1ebcdic"
                state.glset = 0
                state.grset = 1
                state.cur_rhs = "37"
                state.cur_gsets = list(graphdata.defgsets[state.cur_rhs])
                state.is_96 = [graphdata.gsets[i][0] > 94 for i in state.cur_gsets]
                state.c0_graphics_mode = 1
                state.in_ebcdic_dbcs_mode = False # Gets set by special-casing in invocations module
                state.ebcdic_dbcs = "nil"
                state.ebcdic_65th_control_code = 0xFF
            else:
                yield token
        elif state.docsmode == "ebcdic" and token == ("ESC", None, (), 0x30):
            # Private use sequence, make use of it for setting the 65th control code position
            seeking_65th_control_code = token
        elif state.docsmode == "ebcdic" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] == 0xFF:
                conv_byte = conv_map[state.ebcdic_65th_control_code]
            elif token[1] == state.ebcdic_65th_control_code:
                conv_byte = conv_map[0xFF]
            else:
                conv_byte = conv_map[token[1]]
            if conv_byte < 0x20 or 0x7F <= conv_byte < 0xA0:
                assert state.c0_graphics_mode in (1, 2, 4), state.c0_graphics_mode
                if (state.c0_graphics_mode == 1) or token[1] == 0x1B or (
                        state.c0_graphics_mode == 2 and token[1] in (7, 8, 9, 0xA, 0xD, 0x85)):
                    if conv_byte == 0x7F:
                        yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                    elif conv_byte >= 0x80:
                        yield ("C1", conv_byte - 0x80, "CR")
                    else:
                        yield ("C0", conv_byte, "CL")
                elif conv_byte >= 0x80:
                    c1replset = state.cur_rhs
                    if c1replset not in graphdata.rhses:
                        yield ("CHAR?", c1replset, (conv_byte - 0x80,), "RHS", "RHS")
                        continue
                    c1repl = graphdata.rhses[c1replset][conv_byte - 0x80]
                    if c1repl is not None:
                        yield ("CHAR", c1repl, c1replset, (conv_byte,), "RHS", "RHS")
                    else:
                        yield ("C1", conv_byte - 0x80, "CL")
                else:
                    c0replset = state.cur_rhs
                    if c0replset not in graphdata.c0graphics:
                        c0replset = "437"
                    c0repl = graphdata.c0graphics[c0replset][
                             conv_byte if conv_byte != 0x7F else 0x20]
                    if c0repl is not None:
                        yield ("CHAR", c0repl, c0replset, (conv_byte,), "C0REPL", "C0REPL")
                    else:
                        if token[1] == 0x7F:
                            yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                        else:
                            yield ("C0", conv_byte, "CL")
            elif state.in_ebcdic_dbcs_mode:
                if not dbcs_lead:
                    dbcs_lead = token
                elif dbcs_lead[1] == 0x40:
                    if token[1] == 0x40:
                        yield ("CHAR", 0x3000, "EBCDIC", (0x40, 0x40), "DBEBCDIC", "DBEBCDIC")
                        dbcs_lead = None
                    else:
                        yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                        dbcs_lead = token
                else:
                    pointer = ((dbcs_lead[1] - 0x41) * 190) + (token[1] - 0x41)
                    array = graphdata.gsets[state.ebcdic_dbcs][2]
                    ucs = array[pointer] if pointer < len(array) else None
                    codebytes = (dbcs_lead[1], token[1])
                    if ucs is None:
                        yield ("ERROR", "UNDEFGRAPH", state.ebcdic_dbcs, codebytes, "DB", "DB")
                    elif isinstance(ucs, tuple):
                        for iucs in ucs:
                            yield ("CHAR", iucs, state.ebcdic_dbcs, codebytes, "DB", "DB")
                    else:
                        yield ("CHAR", ucs, state.ebcdic_dbcs, codebytes, "DB", "DB")
                    dbcs_lead = None
            elif conv_byte < 0x80:
                if (not state.is_96[state.glset]) and (conv_byte == 0x20):
                    yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                else:
                    yield (workingsets[state.glset], conv_byte - 0x20, "GL")
            else:
                yield (workingsets[state.grset], conv_byte - 0xA0, "GR")
        elif state.docsmode == "ebcdic" and token[0] == "CSISEQ" and token[1] == "DECSPPCS":
            # DEC Select [IBM] ProPrinter Character Set, i.e. CSI sequence for basically chcp.
            codepage = bytes(token[2]).decode("ascii")
            state.cur_rhs = codepage
            state.cur_gsets = list(graphdata.defgsets[state.cur_rhs
                                                      if state.cur_rhs in graphdata.defgsets
                                                      else "437"])
            state.is_96 = [graphdata.gsets[i][0] > 94 for i in state.cur_gsets]
            yield ("CHCP", codepage)
        elif state.docsmode == "ebcdic" and token[0] == "CSISEQ" and token[1] == "DECSDPT":
            # Select Digital Printed Data Type, also part of DEC's IBM ProPrinter emulation.
            if token[2] == (0x34,): # 4: Print All Characters
                state.c0_graphics_mode = 4
                yield ("C0GRAPH", 4)
            elif token[2] == (0x32,): # 2: National and Line Drawing
                state.c0_graphics_mode = 2
                yield ("C0GRAPH", 2)
            else: # Default behaviour
                state.c0_graphics_mode = 1
                yield ("C0GRAPH", 1)
        else:
            yield token
        #
    #
#








