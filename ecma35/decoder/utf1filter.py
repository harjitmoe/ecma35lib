#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# As defined to this day in ISO-IR-178

utf1docs = ("DOCS", False, (0x42,))

# ISO-IR-178's "U" function used in the *decoder* for UTF-1.
#  Basically: the GL range (narrowly defined) is mapped to the first 94 values, GR to the next 96.
#  The CL, SP, DEL and CR ranges are mapped to the remaining values, solely to make it a reversible
#   transformation (they're not actually used).
#  The "T" function used by the *encoder* for UTF-1 is the reverse of this transform.
def _decode_continuation_byte(z):
    if z <= 0x20:
        return z + 0xBE
    elif z <= 0x7E:
        return z - 0x21
    elif z <= 0x9F:
        return z + 0x60
    else:
        return z - 0x42

def decode_utf1(stream, state):
    utf1_brot = []
    utf1_seeking = 0
    reconsume = None
    firstchar = True
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if (token[0] == "DOCS"):
            if utf1_brot:
                yield ("ERROR", "UTF1TRUNC", tuple(utf1_brot))
                del utf1_brot[:]
            if token == utf1docs:
                yield ("RDOCS", "UTF-1", token[1], token[2])
                firstchar = True
                state.bytewidth = 1
                state.docsmode = "utf-1"
            else:
                yield token
        elif state.docsmode == "utf-1":
            if not utf1_brot:
                if token[0] != "WORD":
                    # ESC passing through
                    yield token
                    continue
                # Lead byte
                if token[1] < 0xA0:
                    yield ("UCS", token[1], "UTF-1", "DIRECT") # 1-byte code
                    firstchar = False
                else:
                    if token[1] < 0xF6:
                        utf1_seeking = 2
                    elif token[1] < 0xFC:
                        utf1_seeking = 3
                    else:
                        utf1_seeking = 5
                    utf1_brot.append(token[1])
            else:
                # Continuation byte
                if (token[0] != "WORD") or (token[1] < 0x21) or (0x7F <= token[1] <= 0x9F):
                    # i.e. isn't a continuation byte
                    yield ("ERROR", "UTF1TRUNCATE", tuple(utf1_brot))
                    del utf1_brot[:]
                    reconsume = token
                    firstchar = False
                    continue
                else:
                    utf1_brot.append(token[1])
                    assert len(utf1_brot) <= utf1_seeking
                    if len(utf1_brot) == utf1_seeking:
                        if utf1_brot[0] == 0xA0:
                            assert utf1_seeking == 2
                            ucs = utf1_brot[1]
                        elif utf1_seeking == 2:
                            ucs = 0x100
                            ucs += (utf1_brot[0] - 0xA1) * 0xBE
                            ucs += _decode_continuation_byte(utf1_brot[1])
                        elif utf1_seeking == 3:
                            ucs = 0x4016
                            # ISO-IR-178 lists 0xBE2 here, but it appears to be a typo for 0xBE**2
                            ucs += (utf1_brot[0] - 0xF6) * (0xBE**2)
                            ucs += _decode_continuation_byte(utf1_brot[1]) * 0xBE
                            ucs += _decode_continuation_byte(utf1_brot[2])
                        else:
                            assert utf1_seeking == 5
                            ucs = 0x38E2E
                            ucs += (utf1_brot[0] - 0xFC) * (0xBE**4)
                            ucs += _decode_continuation_byte(utf1_brot[1]) * (0xBE**3)
                            ucs += _decode_continuation_byte(utf1_brot[2]) * (0xBE**2)
                            ucs += _decode_continuation_byte(utf1_brot[3]) * 0xBE
                            ucs += _decode_continuation_byte(utf1_brot[4])
                        #
                        subtype = "UTF-1"
                        if ucs == 0xFEFF and firstchar:
                            yield ("BOM", None)
                        elif 0xD800 <= ucs < 0xE000:
                            # Pass surrogate halves through to the UTF-16 filter for handling.
                            # The UTF-16 filter must be used after the UTF-1 one.
                            yield ("CESU", ucs, "1")
                        elif ucs > 0x10FFFF:
                            yield ("ERROR", "UTF1BEYOND", ucs)
                        else:
                            yield ("UCS", ucs, "UTF-1", subtype)
                        firstchar = False
                        del utf1_brot[:]
                        #  is now empty, and utf1_seeking will be set by next lead byte
                    #
                #
            #
        else: # i.e. isn't a DOCS, nor a UTF-8 part of the stream
            yield token
        #
    #
#








