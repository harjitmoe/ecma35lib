#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import controldata

def decode_control_strings_st(stream, *, accept_bel_as_st=True):
    active = []
    mode = "normal"
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if mode == "normal":
            if (token[0] == "CTRL") and (token[1] in ("DCS", "SOS", "OSC", "PM", "APC")):
                active.append(token)
                mode = "string"
            elif (token[0] == "CTRL") and (token[1] in ("CSI", "CEX")):
                raise ValueError("run decode_control_strings_csi before "+
                                 "decode_invocations and decode_control_strings_st")
            else:
                yield token # Pass everything else through
        elif mode == "string":
            # FIXME: Running this at such a late stage is an awful kludge, since the actual string
            # itself (apart from SOS) is supposed to be of CL bytes and format effectors.
            # However, in practice, you can set window titles in UTF-8 mode as follows:
            #   OSC 0 ; 庭 に は 二 羽 鶏 が い る 。 ST
            # Thus, this is possibly the correct approach? I'm not sure how it ought to be 
            # processed when (say) JIS X 0208 is over CL.
            if token[0] == "CHAR":
                active.append(token)
                continue
            elif token[0] == "CTRL":
                if token[1] in controldata.format_effectors:
                    active.append(token)
                    continue
                elif token[1] == "ST":
                    active.append(token)
                    yield ("CTRLSTRING", active[0][1], tuple(active))
                    del active[:]
                    mode = "normal"
                    continue
                elif token[1] == "BEL" and accept_bel_as_st: # TODO for all or just OSC?
                    active.append(token)
                    yield ("CTRLSTRING", active[0][1], tuple(active))
                    del active[:]
                    mode = "normal"
                    continue
                # Otherwise fall through
            # Not elif (this is fall-through from several cases):
            if active[0][1] == "SOS":
                # All characters permitted, only terminates at ST (TODO does it at BEL?)
                active.append(token)
            else:
                yield ("ERROR", "TRUNCSEQ", tuple(active))
                del active[:]
                mode = "normal"
                reconsume = token
                continue

def decode_control_strings_csi(stream):
    active = []
    idbytes = []
    parbytes = []
    mode = "normal"
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if mode == "normal":
            if (token[0] == "CTRL") and (token[1] in ("CSI",)):
                active.append(token)
                mode = "csi"
            elif (token[0] == "CTRL") and (token[1] in ("CEX",)):
                active.append(token)
                mode = "cex"
            else:
                yield token # Pass everything else through
        elif mode in ("csi", "csinoparam"):
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
                if tuple(idbytes) in controldata.csiseq:
                    yield ("CSISEQ", controldata.csiseq[tuple(idbytes)], tuple(parbytes), active[0][3])
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
                reconsume = token
                continue
        else:
            raise NotImplementedError
            
            







                