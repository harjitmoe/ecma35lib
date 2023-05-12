#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Note that this also handles surrogate pairs retrieved by DOCS filters upstream, either as an
# error case (UTF-8, UTF-1, UTF-32) or as a legitimate part of the respective encodings 
# (SCSU, LMBCS, UTF-7). Hence, it must be used after most UCS formats (except maybe GB18030).

def decode_utf16(stream, state):
    utf16_lead = None
    reconsume = None
    bomap = {"<": "le", ">": "be"}
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        docsmap = {"utf-16": state.default_endian, "utf-16le": "<", "utf-16be": ">"}
        if token[0] in ("DOCS", "RDOCS"):
            if utf16_lead:
                yield ("ERROR", "UTF16ISOLATE", utf16_lead)
                yield ("UCS", utf16_lead, "UTF-16", "WTF-16" + bo) # "Wobbly UTF-16"
                utf16_lead = None
            if token[0] == "RDOCS" and token[1] in docsmap:
                state.bytewidth = 2
                state.endian = docsmap[token[1]]
                firstchar = token[1] == "utf-16"
                state.docsmode = "utf-16"
            yield token
        elif (state.docsmode == "utf-16") or (token[0] in ("CESU", "PAIR")):
            if not utf16_lead:
                if token[0] not in ("WORD", "CESU", "PAIR"):
                    # ESC passing through
                    yield token
                    continue
                # Lead word
                if (token[1] < 0xD800) or (token[1] >= 0xDC00):
                    if 0xDC00 <= token[1] < 0xE000:
                        # isolated trailing surrogate
                        if token[0] == "CESU":
                            utf = token[2]
                            yield ("ERROR", "UTF" + utf + "SURROGATE", token[1])
                            yield ("UCS", token[1], "UTF-" + utf, "WTF-" + utf) # "Wobbly UTF"
                        elif token[0] == "PAIR":
                            yield ("ERROR", token[2] + "SURROGATE", token[1])
                            yield ("UCS", token[1], token[2], "WTF-" + token[3])
                        else:
                            yield ("ERROR", "UTF16ISOLATE", token[1])
                            yield ("UCS", token[1], "UTF-16", "WTF-16" + bo) # "Wobbly UTF-16"
                    elif token[1] == 0xFFFE and (
                            (firstchar and state.regard_bom) or (state.regard_bom > 1)):
                        state.endian = {">": "<", "<": ">"}[state.endian]
                        yield ("BOM", state.endian)
                    elif token[1] == 0xFEFF and firstchar and state.regard_bom:
                        yield ("BOM", state.endian) # Confirms the assumed byte order.
                    elif token[0] in ("CESU", "PAIR"):
                        raise AssertionError("non-surrogate passed through to UTF-16 filter")
                    else:
                        bo = bomap[state.endian]
                        yield ("UCS", token[1], "UTF-16", "UCS-2" + bo) # single BMP code
                    firstchar = False
                else:
                    utf16_lead = token
            else:
                # Trail word
                if ((token[0] not in ("WORD", "CESU", "PAIR")) or (token[1] < 0xDC00)
                                                               or (token[1] >= 0xE000)):
                    # i.e. isn't a continuation word
                    if utf16_lead[0] == "CESU":
                        utf = utf16_lead[2]
                        yield ("ERROR", "UTF" + utf + "SURROGATE", utf16_lead[1])
                        yield ("UCS", utf16_lead[1], "UTF-" + utf, "WTF-" + utf) # "Wobbly UTF"
                    elif utf16_lead[0] == "PAIR":
                        yield ("ERROR", fmat + "SURROGATE", utf16_lead[1])
                        yield ("UCS", utf16_lead[1], utf16_lead[2], "WTF-" + utf16_lead[3])
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
                        yield ("ERROR", "UTF" + token[2] + "CESU", ucs)
                        yield ("UCS", ucs, "UTF-" + token[2], "CESU-" + token[2])
                    elif token[0] == "PAIR":
                        # Main difference against CESU is that PAIR is for DOCS sets which are
                        # actually supposed to embed surrogate pairs. So, no ERROR here.
                        yield ("UCS", ucs, token[2], token[3])
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








