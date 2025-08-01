#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2023, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import controldata, graphdata

def decode_csi_sequences(stream, state):
    workingsets = graphdata.workingsets
    active = []
    idbytes = []
    parbytes = []
    mode = "normal"
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if mode == "normal":
            if (token[0] == "CTRL") and (token[1] in ("CSI",)):
                active.append(token)
                mode = "csi"
            elif (token[0] == "CTRL") and (token[1] in ("CEX",)):
                active.append(token)
                mode = "cex"
            # Both the IBM and Fujitsu-Siemens mappings for EBCDIC controls to the C1 area (we're
            #   using the IBM one) map CSI onto Customer Use 3 (CU3). We want to have easy access
            #   to CSI inside the EBCDIC DOCS either way.
            elif (token[0] == "CTRL") and (token[1] in ("CU3",)) and state.docsmode in ("ebcdic", "utf-ebcdic"):
                active.append(token)
                mode = "csi"
            else:
                yield token # Pass everything else through
        elif mode in ("csi", "csinoparam"):
            savetoken = token
            if token[0] == "UCS" and 0x20 <= token[1] < 0x7F:
                # Can use CSI in UTF-8.
                # Note the following transformation is only appropriate *because* we know that
                # we're in a CSI sequence, hence savetoken is used for reconsume.
                token = ("G0", token[1] - 0x20, "GL")
            if token == ("CTRL", "SP", "ECMA-35", 0, "GL", "G0"):
                # Space is exceptionally not treated the same as DEL here.
                token = ("G0", 0, "GL")
            # Not elif:
            bytevalue = token[1] + 0x20 if isinstance(token[1], int) else None
            if token[0] in workingsets and token[2] == "GL" and (0x30 <= bytevalue < 0x40) and (mode != "csinoparam"):
                active.append(token)
                parbytes.append(bytevalue)
            elif token[0] in workingsets and token[2] == "GL" and (0x20 <= bytevalue < 0x30):
                active.append(token)
                idbytes.append(bytevalue)
                mode = "csinoparam"
            elif token[0] in workingsets and token[2] == "GL" and (bytevalue >= 0x40):
                active.append(token)
                idbytes.append(bytevalue)
                puscbytes = [] # Corporate (or private) use subcommand
                while parbytes and parbytes[0] in tuple(b"<=>?"):
                    puscbytes.append(parbytes.pop(0))
                # Note: puscbytes are appended, not prepended, to idbytes in controldata.
                # Some are mnemoniced separately, others should just get the puscbytes in
                # their parbytes and go to the same handler.
                # Need to feedback since some CSI sequences control some designations
                # (notably in the plainextascii DOCS).
                if tuple(idbytes) + tuple(puscbytes) in controldata.csiseq:
                    state.feedback.append(("CSISEQ", controldata.csiseq[tuple(idbytes) + 
                                     tuple(puscbytes)], tuple(parbytes), tuple(active)))
                elif tuple(idbytes) in controldata.csiseq:
                    state.feedback.append(("CSISEQ", controldata.csiseq[tuple(idbytes)], 
                                     tuple(puscbytes) + tuple(parbytes), tuple(active)))
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
                token = ("G0", token[1] - 0x20, "GL")
            elif token[0] not in workingsets or token[2] != "GL":
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
            
            







                
