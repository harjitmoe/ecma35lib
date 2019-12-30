#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import controldata

def decode_esc_sequences(stream, state):
    active = []
    idbytes = []
    parbytes = []
    inesc = False
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if not inesc:
            if (token[0] == "CTRL") and (token[1] in ("ESC",)):
                active.append(token)
                inesc = True
            else:
                yield token # Pass everything else through
        else:
            if token[0] == "UCS" and 0x20 <= token[1] < 0x7F:
                # If we're in a Unicode format
                code = token[1]
            elif token[0] == "CODEWORD" and 0x20 <= token[2] < 0x7F:
                # If we're in an unknown DOCS with standard return
                code = token[2]
            elif token[0] == "GL":
                # If we're in ECMA-35
                code = token[1] + 0x20
            else:
                yield ("ERROR", "TRUNCESC", tuple(active), token)
                del active[:]
                del idbytes[:]
                del parbytes[:]
                inesc = False
                reconsume = token
                continue
            active.append(token)
            if code < 0x30:
                idbytes.append(code)
                continue
            ret = ("ESC", idbytes[0] if idbytes else None, tuple(idbytes[1:]), code)
            if ret[1] == b"%"[0]:
                if ret[2] and (ret[2][0] == b"/"[0]):
                    ret2 = ("DOCS", True, ret[2][1:] + (ret[3],))
                else:
                    ret2 = ("DOCS", False, ret[2] + (ret[3],))
                # Deal with byte-width changes, mode changes and raw mode instigation.
                if not ret2[1]:
                    # UTF-8 (DOCS G), UTF-1 (DOCS B), ECMA-35 (DOCS @), or otherwise bytewise with 
                    # standard return.
                    state.hasesc = True # Only referenced if there is no filter for this DOCS.
                else:
                    # Something else to be dealt with by its own filter, or treated as raw.
                    state.hasesc = False # Only referenced if there is no filter for this DOCS.
                state.bytewidth = 1 # May be subsequently overridden by the specific filter.
                state.feedback.append(ret2)
            elif (not ret[1]) and (not ret[2]) and (0x40 <= ret[3] < 0x60):
                # C1 control characters in 7-bit escape form.
                state.feedback.append(("C1", ret[3] - 0x40, "ESC"))
            else:
                state.feedback.append(ret)
            inesc = False
            del active[:]
            del idbytes[:]
            del parbytes[:]








                