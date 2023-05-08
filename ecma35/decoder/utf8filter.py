#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def decode_utf8(stream, state):
    utf8_brot = []
    utf8_seeking = 0
    reconsume = None
    firstchar = True
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if token[0] in ("DOCS", "RDOCS"):
            if utf8_brot:
                yield ("ERROR", "UTF8TRUNC", tuple(utf8_brot))
                del utf8_brot[:]
            if token[0] == "RDOCS" and token[1] == "utf-8":
                firstchar = True
                state.bytewidth = 1
                state.docsmode = "utf-8"
            yield token
        elif state.docsmode == "utf-8":
            if not utf8_brot:
                if token[0] != "WORD":
                    # ESC passing through
                    yield token
                    continue
                # Lead byte
                if token[1] < 0x80:
                    yield ("UCS", token[1], "UTF-8", "ASCII") # 1-byte code
                    firstchar = False
                elif (token[1] & 0b11000000) == 0x80:
                    # i.e. is a continuation byte
                    yield ("ERROR", "UTF8ISOLATE", (token[1],))
                    firstchar = False
                else:
                    for bc in range(8):
                        if not token[1] & (0x80 >> bc):
                            break
                    assert bc > 1
                    utf8_seeking = bc
                    utf8_brot.append(token[1])
            else:
                # Continuation byte
                if (token[0] != "WORD") or (token[1] < 0x80) or ((token[1] & 0b11000000) != 0x80):
                    # i.e. isn't a continuation byte
                    yield ("ERROR", "UTF8TRUNCATE", tuple(utf8_brot))
                    del utf8_brot[:]
                    reconsume = token
                    firstchar = False
                    continue
                else:
                    utf8_brot.append(token[1])
                    assert len(utf8_brot) <= utf8_seeking
                    if len(utf8_brot) == utf8_seeking:
                        save_brot = tuple(utf8_brot) # Converting to tuple, of course, copies it.
                        ucs = utf8_brot.pop(0) & ((0x80 >> utf8_seeking) - 1)
                        while utf8_brot:
                            ucs <<= 6
                            ucs |= utf8_brot.pop(0) & 0b00111111
                        #
                        subtype = "UTF-8"
                        overlong = (ucs < 0x80)
                        overlong = overlong or ((ucs < 0x800) and (utf8_seeking > 2))
                        overlong = overlong or ((ucs < 0x10000) and (utf8_seeking > 3))
                        if overlong:
                            firstchar = False
                            if (utf8_seeking == 2) and (ucs == 0):
                                # Two-byte U+0000 is sometimes deliberately used as an escaped NUL
                                # in a null-terminated UTF-8 string.
                                yield ("ERROR", "UTF8OVERLONGNULL", save_brot)
                                subtype = "UTF-8-OVERLONG-NULL"
                            else:
                                yield ("ERROR", "UTF8OVERLONG", save_brot)
                                subtype = "UTF-8-OVERLONG"
                        if ucs == 0xFEFF and firstchar:
                            yield ("BOM", None)
                        elif 0xD800 <= ucs < 0xE000:
                            # Pass surrogate halves through to the UTF-16 filter for handling.
                            # The UTF-16 filter must be used after the UTF-8 one.
                            yield ("CESU", ucs, "8")
                        elif ucs > 0x10FFFF:
                            yield ("ERROR", "UTF8BEYOND", ucs)
                        else:
                            yield ("UCS", ucs, "UTF-8", subtype)
                        firstchar = False
                        # utf8_brot is now empty, and utf8_seeking will be set by next lead byte
                    #
                #
            #
        else: # i.e. isn't a DOCS, nor a UTF-8 part of the stream
            yield token
        #
    #
#








