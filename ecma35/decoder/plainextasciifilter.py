#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Filter for "plain extended ASCII", i.e. a single-byte 8-bit encoding which encodes the C0 
# controls normally, but doesn't have a CR area. C1 controls might still be used (c.f. CSI 
# in ANSI.SYS) but they must be represented by escape sequences, like in a seven-bit code.
# Basically amounts to a 7-bit ECMA-35 code version plus 128 extra graphical codes, and not 
# an actual 8-bit ECMA-35 version.
# Also supports a "Print All Characters" mode, i.e. with C0 area graphics. It makes an exception
# for 0x1B, though, to try and keep it possible to go back (thus keeping it With Standard Return).

import sys
from ecma35.data import graphdata

def decode_plainextascii(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    for token in stream:
        if (token[0] == "RDOCS"):
            if token[1] == "plainextascii":
                state.bytewidth = 1
                state.docsmode = "plainextascii"
                state.cur_c0 = "ir001"
                state.cur_c1 = "RFC1345"
                state.glset = 0
                state.grset = 1
                state.cur_rhs = "437"
                state.cur_gsets = list(graphdata.defgsets[state.cur_rhs])
                state.is_96 = [graphdata.gsets[i][0] > 94 for i in state.cur_gsets]
                state.c0_graphics_mode = 3
            yield token
        elif state.docsmode == "plainextascii" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if token[1] < 0x20 or token[1] == 0x7F:
                assert state.c0_graphics_mode in (1, 2, 3, 5, 4), state.c0_graphics_mode
                if (state.c0_graphics_mode in (1, 2, 3)) or token[1] == 0x1B or (
                        state.c0_graphics_mode == 5 and token[1] in (7, 8, 9, 0xA, 0xD)):
                    # BEL, BS, HT, LF and CR don't print as graphic in Windows terminal mode.
                    # The rest do.
                    # They do have their own graphics though, used for Print All Characters.
                    # The 0x1B exception to Print All Characters arguably shouldn't be here, but
                    # since there's no out-of-band way of controlling the IO, not making this an
                    # exception would make the switch permanent. Although permanent switches can
                    # be a thing (as with DOCS / B), they're not really how this implementation
                    # is designed to work as a general rule.
                    # Also, not having that exception would make this filter without standard
                    # return, when the vast majority of usage cases are very much with it.
                    # So far as I can tell, using 0x1B as ESC does not damage TCVN-1/VSCII-1, nor
                    # VPS, nor VISCII. Damage to OEM is relatively minor, and 0x1B being read as
                    # ESC (vide ANSI.SYS) is probably expected anyway. So, it's fine.
                    if token[1] == 0x7F:
                        yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                    else:
                        yield ("C0", token[1], "CL")
                else:
                    c0replset = state.cur_rhs
                    if c0replset not in graphdata.c0graphics:
                        c0replset = "437"
                    c0repl = graphdata.c0graphics[c0replset][
                             token[1] if token[1] != 0x7F else 0x20]
                    if c0repl is not None:
                        yield ("CHAR", c0repl, c0replset, (token[1],), "C0REPL", "C0REPL")
                    else:
                        if token[1] == 0x7F:
                            yield ("CTRL", "DEL", "ECMA-35", 95, "GL", workingsets[state.glset])
                        else:
                            yield ("C0", token[1], "CL")
            elif token[1] < 0x80:
                if (not state.is_96[state.glset]) and (token[1] == 0x20):
                    yield ("CTRL", "SP", "ECMA-35", 0, "GL", workingsets[state.glset])
                else:
                    yield (workingsets[state.glset], token[1] - 0x20, "GL")
            elif state.c0_graphics_mode in (1, 2) and 0x80 <= token[1] < 0xA0:
                yield ("C1", token[1] - 0x80, "CR")
            else: # i.e. it is on the right-hand side
                index = token[1] - 0x80
                if state.cur_rhs not in graphdata.rhses:
                    yield ("CHAR?", state.cur_rhs, (index,), "RHS", "RHS")
                    continue
                ucs = graphdata.rhses[state.cur_rhs][index]
                if ucs is None:
                    yield ("ERROR", "UNDEFGRAPH", state.cur_rhs, (index,), -1, "RHS")
                elif isinstance(ucs, tuple):
                    for iucs in ucs:
                        yield ("CHAR", iucs, state.cur_rhs, (index,), "RHS", "RHS")
                else:
                    yield ("CHAR", ucs, state.cur_rhs, (index,), "RHS", "RHS")
        elif state.docsmode == "plainextascii" and token[0] == "CHCP":
            codepage = token[1]
            state.cur_rhs = codepage
            state.cur_gsets = list(graphdata.defgsets[state.cur_rhs
                                                      if state.cur_rhs in graphdata.defgsets
                                                      else "437"])
            state.is_96 = [graphdata.gsets[i][0] > 94 for i in state.cur_gsets]
            yield token
        elif state.docsmode == "plainextascii" and token[0] == "CSISEQ" and token[1] == "DECSDPT":
            # Select Digital Printed Data Type, also part of DEC's IBM ProPrinter emulation (i.e.
            #   for making print-to-terminal work the same as print-to-printer).
            # https://vt100.net/docs/vt510-rm/DECSDPT.html
            # Note: IBM documents "ESC X'7E08'", i.e. `ESC ~ BS`, as Print All Characters; this
            #   is not conformant with ECMA-35's use of ESC, unlike the DEC sequence:
            # https://web.archive.org/web/20160317081202/http://www-01.ibm.com/software/globalization/cp/cp01042.html
            # Note 2: having consulted PN6328945 (the original 1985 IBM ProPrinter manual), the
            #   relevant ProPrinter modes are:
            # - ESC 6: Select "Character Set 2" (i.e. the full code-page 437 minus C0 graphics)
            # - ESC 7: Select "Character Set 1" (i.e. code-page 437 without C0 *or* C1 area graphics)
            # - ESC \ (n) (n): Enable Print All Characters mode for the next (uInt16LE parameter)
            #     characters. Interestingly, it seems only to yet have supported a subset of the
            #     code-page 437 C0 graphics (and no DEL graphic).
            # - ESC ^: Same as ESC \ SOH NUL (i.e. Print All Characters as a single-shift).
            # From this, I can deduce the intended meanings of DEC's parameters as perhaps:
            # - `CSI ) p` or `CSI 0 ) p`: default as per ECMA-48 (i.e. same as `CSI 1 ) p`).
            # - `CSI 1 ) p`: "Print National Only" (i.e. 0x20–7E?)
            # - `CSI 2 ) p`: "Print National and Line Drawing" (i.e. 0x20–7E,A0–FF?)
            # - `CSI 3 ) p`: "Print Multinational" (i.e. 0x20–7E,80–FF?)
            # - `CSI 4 ) p`: "Print All Characters" (i.e. 0x00–FF?)
            # This does not quite match what we previously did, which was:
            # - `CSI 1 ) p`: 0x20–7E,80–FF
            # - `CSI 2 ) p`: 0x01–06,0B–0C,0E–1A,1C–FF
            # - `CSI 4 ) p`: 0x01–1A,1C–FF
            if token[2] == (0x31,): # Print GL region (currently also prints GR region)
                state.c0_graphics_mode = 1
                yield ("C0GRAPH", 1)
            elif token[2] == (0x32,): # Print GL and GR regions
                state.c0_graphics_mode = 2
                yield ("C0GRAPH", 2)
            elif token[2] == (0x33,): # Print GL, C1 and GR regions
                state.c0_graphics_mode = 3
                yield ("C0GRAPH", 3)
            elif token[2] == (0x35,): # Print it like a classic Windows Console (besides ESC)
                state.c0_graphics_mode = 5
                yield ("C0GRAPH", 5)
            elif token[2] == (0x34,): # Print C0, GL, C1 and GR regions (except ESC)
                state.c0_graphics_mode = 4
                yield ("C0GRAPH", 4)
            elif (not token[2]) or (token[2] == (0x30,)): # Use default behaviour
                state.c0_graphics_mode = 3
                yield ("C0GRAPH", 3)
            else:
                yield ("ERROR", "UNKNOWNC0GRAPHMODE", token)
        else:
            yield token
        #
    #
#








