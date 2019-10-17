#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import controldata

def decode_control_strings(stream, state):
    active = []
    idbytes = []
    parbytes = []
    mode = "normal"
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if mode == "normal":
            if (token[0] == "CTRL") and (token[1] in ("DCS", "SOS", "OSC", "PM", "APC")):
                active.append(token)
                mode = "string"
            elif (token[0] == "CTRL") and (token[1] in ("CSI",)):
                active.append(token)
                mode = "csi"
            elif (token[0] == "CTRL") and (token[1] in ("CEX",)):
                active.append(token)
                mode = "cex"
            elif (token[0] == "CTRL") and (token[1] in ("ESC",)):
                active.append(token)
                mode = "esc"
            else:
                yield token # Pass everything else through
        elif mode == "esc":
            if token[0] == "ENDSTREAM":
                yield ("ERROR", "TRUNCESC", tuple(active), None)
                yield token
                return
            elif token[0] == "UCS" and 0x20 <= token[1] < 0x7F:
                code = token[1]
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
        elif mode == "string":
            if token[0] == "CTRL" and (token[1] == "ST" or
                    (token[1] == "BEL" and active[0][1] == "OSC" and state.osc_bel_term)):
                active.append(token)
                yield ("CTRLSTRING", active[0][1], tuple(active))
                del active[:]
                mode = "normal"
            elif token[0] == "ENDSTREAM":
                # String was never terminated.
                yield ("ERROR", "TRUNCSEQ", tuple(active))
                yield token
                return
            else:
                active.append(token)
        elif mode in ("csi", "csinoparam"):
            savetoken = token
            if token[0] == "UCS" and 0x20 <= token[1] < 0x7F:
                # Can use CSI in UTF-8.
                # Note the following transformation is only appropriate *because* we know that
                # we're in a CSI sequence, hence savetoken is used for reconsume.
                token = ("GL", token[1] - 0x20)
            # Not elif:
            bytevalue = token[1] + 0x20
            if token[0] == "GL" and (0x30 <= bytevalue < 0x40) and (mode != "csinoparam"):
                active.append(token)
                parbytes.append(bytevalue)
            elif token[0] == "GL" and (0x20 <= bytevalue < 0x30):
                active.append(token)
                idbytes.append(bytevalue)
                mode = "csinoparam"
            elif token[0] == "GL" and (bytevalue >= 0x40):
                active.append(token)
                idbytes.append(bytevalue)
                puscbytes = [] # Corporate (or private) use subcommand
                while parbytes and parbytes[0] in tuple(b"<=>?"):
                    puscbytes.append(parbytes.pop(0))
                # Note: puscbytes are appended, not prepended, to idbytes in controldata.
                # Some are mnemoniced separately, others should just get the puscbytes in
                # their parbytes and go to the same handler.
                if tuple(idbytes) + tuple(puscbytes) in controldata.csiseq:
                    yield ("CSISEQ", controldata.csiseq[tuple(idbytes) + tuple(puscbytes)], 
                                     tuple(parbytes), active[0][3])
                elif tuple(idbytes) in controldata.csiseq:
                    yield ("CSISEQ", controldata.csiseq[tuple(idbytes)], 
                                     tuple(puscbytes) + tuple(parbytes), active[0][3])
                else:
                    yield ("CTRLSTRING", active[0][1], tuple(active))
                del active[:]
                del idbytes[:]
                del parbytes[:]
                mode = "normal"
                continue
            else:
                yield ("ERROR", "TRUNCSEQ", tuple(active))
                del active[:]
                del idbytes[:]
                del parbytes[:]
                mode = "normal"
                reconsume = savetoken
                continue
        else:
            assert mode == "cex"
            savetoken = token
            if token[0] == "UCS" and 0x20 <= token[1] < 0x7F:
                # Treat the same as CSI (see above)
                token = ("GL", token[1] - 0x20)
            elif token[0] != "GL":
                yield ("ERROR", "TRUNCSEQ", tuple(active))
                del active[:]
                mode = "normal"
                reconsume = savetoken
                continue
            bytevalue = token[1] + 0x20
            if bytevalue in controldata.cexseq:
                yield ("CEXSEQ", controldata.cexseq[bytevalue], (), active[0][3])
                del active[:]
                mode = "normal"
            else:
                # Some take parameters (including CEX $ n, CEX 0 n1 n2 and 
                # CEX 2 a1 a2 d1 d2 d3 ... d72). Sadly, I've not been able to
                # find adequate documentation on the format or parsing of
                # those parameters.
                active.append(token)
                yield ("ERROR", "UNSUPCEX", tuple(active))
                del active[:]
                mode = "normal"
                reconsume = savetoken
                continue
            
            







                