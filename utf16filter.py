#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

utf16docs = (("DOCS", True, (0x40,)),
             ("DOCS", True, (0x43,)),
             ("DOCS", True, (0x45,)),
             ("DOCS", True, (0x4A,)),
             ("DOCS", True, (0x4B,)),
             ("DOCS", True, (0x4C,)))

def decode_utf16(stream, state):
    utf16_lead = None
    reconsume = None
    bomap = {"<": "le", ">": "be"}
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if (token[0] == "DOCS"):
            if utf16_lead:
                yield ("ERROR", "UTF16ISOLATE", utf16_lead)
                yield ("UCS", utf16_lead, "UTF-16", "WTF-16" + bo) # "Wobbly UTF-16"
                utf16_lead = None
            if token in utf16docs:
                yield ("RDOCS", "UTF-16", token[1], token[2])
                state.bytewidth = 2
                state.endian = state.default_endian
                firstchar = True
                state.docsmode = "utf-16"
            else:
                yield token
        elif (state.docsmode == "utf-16") or (token[0] == "CESU"):
            if not utf16_lead:
                if token[0] not in ("WORD", "CESU"):
                    # ESC passing through
                    yield token
                    continue
                # Lead word
                if (token[1] < 0xD800) or (token[1] >= 0xDC00):
                    if 0xDC00 <= token[1] < 0xE000:
                        # isolated trailing surrogate
                        if token[0] == "CESU":
                            utf = utf16_lead[2][-1] # "1" or "8"
                            yield ("ERROR", "UTF" + utf + "SURROGATE", token[1])
                            yield ("UCS", token[1], "UTF-" + utf, "WTF-" + utf) # "Wobbly UTF"
                        else:
                            yield ("ERROR", "UTF16ISOLATE", token[1])
                            yield ("UCS", token[1], "UTF-16", "WTF-16" + bo) # "Wobbly UTF-16"
                    elif token[1] == 0xFFFE and (
                            (firstchar and state.regard_bom) or (state.regard_bom > 1)):
                        state.endian = {">": "<", "<": ">"}[state.endian]
                        yield ("BOM", state.endian)
                    elif token[1] == 0xFEFF and firstchar and state.regard_bom:
                        yield ("BOM", state.endian) # Confirms the assumed byte order.
                    elif token[0] == "CESU":
                        raise AssertionError("non-surrogate UTF-8 passed through to UTF-16 filter")
                    else:
                        bo = bomap[state.endian]
                        yield ("UCS", token[1], "UTF-16", "UCS-2" + bo) # single BMP code
                    firstchar = False
                else:
                    utf16_lead = token
            else:
                # Trail word
                if ((token[0] not in ("WORD", "CESU")) or (token[1] < 0xDC00)
                                                       or (token[1] >= 0xE000)):
                    # i.e. isn't a continuation word
                    if utf16_lead[0] == "CESU":
                        utf = utf16_lead[2][-1] # "1" or "8"
                        yield ("ERROR", "UTF" + utf + "SURROGATE", utf16_lead[1])
                        yield ("UCS", utf16_lead[1], "UTF-" + utf, "WTF-" + utf) # "Wobbly UTF"
                    else:
                        bo = bomap[state.endian]
                        yield ("ERROR", "UTF16ISOLATE", utf16_lead[1])
                        yield ("UCS", utf16_lead[1], "UTF-16", "WTF-16" + bo) # "Wobbly UTF-16"
                    firstchar = False
                    utf16_lead = None
                    reconsume = token
                else:
                    ucs = (((utf16_lead[1] & 1023) << 10) | (token[1] & 1023)) + 0x10000
                    if token[0] == "CESU":
                        utf = utf16_lead[2][-1] # "1" or "8"
                        yield ("ERROR", "UTF" + utf + "CESU", ucs)
                        yield ("UCS", ucs, "UTF-" + utf, token[2])
                    else:
                        bo = bomap[state.endian]
                        yield ("UCS", ucs, "UTF-16", "UTF-16" + bo) # validly coded surrogate pair
                    firstchar = False
                    utf16_lead = None
                #
            #
        else: # i.e. isn't a DOCS, nor a UTF-16 part of the stream
            yield token
        #
    #
#








