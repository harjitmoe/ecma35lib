#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import controldata

def decode_esc_sequences(stream, state):
    active = []
    idbytes = []
    parbytes = []
    mode = "normal"
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if mode == "normal":
            if (token[0] == "CTRL") and (token[1] in ("ESC",)):
                active.append(token)
                mode = "esc"
            else:
                yield token # Pass everything else through
        else:
            assert mode == "esc"
            if token[0] == "ENDSTREAM":
                yield ("ERROR", "TRUNCESC", tuple(active), None)
                yield token
                return
            elif token[0] == "UCS" and 0x20 <= token[1] < 0x7F:
                code = token[1]
            elif token[0] == "CODEWORD" and 0x20 <= token[2] < 0x7F:
                # CODEWORD may reach here if were in an unknown DOCS with standard return.
                code = token[2]
            elif token[0] == "GL":
                code = token[1] + 0x20
            else:
                yield ("ERROR", "TRUNCESC", tuple(active), token)
                del active[:]
                del idbytes[:]
                del parbytes[:]
                mode = "normal"
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
                if (not ret2[1]) and (ret2[2] == (b"@"[0],)):
                    # Standard return to ECMA-35 (DOCS @)
                    state.mode, state.bytewidth, state.firstchar = "normal", 1, True
                    state.feedback.append(ret2)
                elif not ret2[1]:
                    # UTF-8 (DOCS G), UTF-1 (DOCS B), or otherwise bytewise with standard return.
                    state.mode, state.bytewidth, state.firstchar = "wsr", 1, True
                    state.feedback.append(ret2)
                elif (not ret[2][1:]) and (ret[3] in tuple(b"GHI")):
                    # UTF-8 (DOCS / I preferred, others deprecated)
                    # Afaict, ISO 10646 doesn't actually distinguish DOCS / I from DOCS G.
                    state.mode, state.bytewidth, state.firstchar = "wsr", 1, True
                    state.feedback.append(ret2)
                elif (not ret[2][1:]) and (ret[3] in tuple(b"@CEJKL")):
                    # UTF-16 (DOCS / L preferred, others deprecated)
                    # Not a WSR sequence due to different word size, but WSR once we know the size.
                    state.mode, state.bytewidth, state.firstchar = "wsr", 2, True
                    state.feedback.append(ret2)
                elif (not ret[2][1:]) and (ret[3] in tuple(b"ADF")):
                    # UTF-32 (DOCS / F preferred, others deprecated)
                    # Not a WSR sequence due to different word size, but WSR once we know the size.
                    state.mode, state.bytewidth, state.firstchar = "wsr", 4, True
                    state.feedback.append(ret2)
                else:
                    # Either raw pass-through (DOCS / B), or as-good-as so far as we can know.
                    state.mode, state.bytewidth, state.firstchar = "raw", 1, True
                    state.feedback.append(ret2)
            elif (not ret[1]) and (not ret[2]) and (0x40 <= ret[3] < 0x60):
                # C1 control characters in 7-bit escape form.
                state.firstchar = False
                state.feedback.append(("C1", ret[3] - 0x40, "ESC"))
            else:
                state.firstchar = False
                state.feedback.append(ret)
            mode = "normal"
            del active[:]
            del idbytes[:]
            del parbytes[:]








                