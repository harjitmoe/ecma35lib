#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2023 (with some earlier material partly derived from other parts of ecma35lib).

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Note this is the UTF-EBCDIC byte map, which is different from the one used in ebcdicfilter
conv_map = [0, 1, 2, 3, 156, 9, 134, 127, 151, 141, 142, 11, 12, 13, 14, 15, 16, 17, 18, 19, 157, 133, 8, 135, 24, 25, 146, 143, 28, 29, 30, 31, 128, 129, 130, 131, 132, 10, 23, 27, 136, 137, 138, 139, 140, 5, 6, 7, 144, 145, 22, 147, 148, 149, 150, 4, 152, 153, 154, 155, 20, 21, 158, 26, 32, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 46, 60, 40, 43, 124, 38, 170, 171, 172, 173, 174, 175, 176, 177, 178, 33, 36, 42, 41, 59, 94, 45, 47, 179, 180, 181, 182, 183, 184, 185, 186, 187, 44, 37, 95, 62, 63, 188, 189, 190, 191, 192, 193, 194, 195, 196, 96, 58, 35, 64, 39, 61, 34, 197, 97, 98, 99, 100, 101, 102, 103, 104, 105, 198, 199, 200, 201, 202, 203, 204, 106, 107, 108, 109, 110, 111, 112, 113, 114, 205, 206, 207, 208, 209, 210, 211, 126, 115, 116, 117, 118, 119, 120, 121, 122, 212, 213, 214, 91, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 93, 230, 231, 123, 65, 66, 67, 68, 69, 70, 71, 72, 73, 232, 233, 234, 235, 236, 237, 125, 74, 75, 76, 77, 78, 79, 80, 81, 82, 238, 239, 240, 241, 242, 243, 92, 244, 83, 84, 85, 86, 87, 88, 89, 90, 245, 246, 247, 248, 249, 250, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 251, 252, 253, 254, 255, 159]

import sys
from ecma35.data import graphdata

def decode_utfebcdic(stream, state):
    utfebcdic_brot = []
    utfebcdic_seeking = 0
    reconsume = None
    firstchar = True
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if token[0] in ("DOCS", "RDOCS"):
            if utfebcdic_brot:
                yield ("ERROR", "UTFEBCDICTRUNC", tuple(utfebcdic_brot))
                del utfebcdic_brot[:]
            if token[0] == "RDOCS" and token[1] == "utf-ebcdic":
                firstchar = True
                state.bytewidth = 1
                state.docsmode = "utf-ebcdic"
            yield token
        elif state.docsmode == "utf-ebcdic":
            if not utfebcdic_brot:
                if token[0] != "WORD":
                    # ESC passing through
                    yield token
                    continue
                i8byte = conv_map[token[1]]
                # Lead byte
                if i8byte < 0xA0:
                    yield ("UCS", i8byte, "UTF-EBCDIC", "ASCII") # 1-byte code
                    firstchar = False
                elif (i8byte & 0b11100000) == 0xA0:
                    # i.e. is a continuation byte
                    yield ("ERROR", "UTFEBCDICISOLATE", (token[1],))
                    firstchar = False
                else:
                    for bc in range(8):
                        if not i8byte & (0x80 >> bc):
                            break
                    assert bc > 1
                    utfebcdic_seeking = bc
                    utfebcdic_brot.append(token[1])
            else:
                i8byte = conv_map[token[1]] if token[0] == "WORD" else None
                # Continuation byte
                if (token[0] != "WORD") or (i8byte < 0xA0) or ((i8byte & 0b11100000) != 0xA0):
                    # i.e. isn't a continuation byte
                    yield ("ERROR", "UTFEBCDICTRUNCATE", tuple(utfebcdic_brot))
                    del utfebcdic_brot[:]
                    reconsume = token
                    firstchar = False
                    continue
                else:
                    utfebcdic_brot.append(token[1])
                    assert len(utfebcdic_brot) <= utfebcdic_seeking
                    if len(utfebcdic_brot) == utfebcdic_seeking:
                        save_brot = tuple(utfebcdic_brot) # Converting to tuple, of course, copies it.
                        ucs = conv_map[utfebcdic_brot.pop(0)] & ((0x80 >> utfebcdic_seeking) - 1)
                        while utfebcdic_brot:
                            ucs <<= 5
                            ucs |= conv_map[utfebcdic_brot.pop(0)] & 0b00011111
                        #
                        subtype = "UTF-EBCDIC"
                        overlong = (ucs < 0xA0)
                        overlong = overlong or ((ucs < 0x400) and (utfebcdic_seeking > 2))
                        overlong = overlong or ((ucs < 0x4000) and (utfebcdic_seeking > 3))
                        overlong = overlong or ((ucs < 0x40000) and (utfebcdic_seeking > 4))
                        if overlong:
                            firstchar = False
                            if (utfebcdic_seeking == 2) and (ucs == 0):
                                yield ("ERROR", "UTFEBCDICOVERLONGNULL", save_brot)
                                subtype = "UTF-EBCDIC-OVERLONG-NULL"
                            else:
                                yield ("ERROR", "UTFEBCDICOVERLONG", save_brot)
                                subtype = "UTF-EBCDIC-OVERLONG"
                        if ucs == 0xFEFF and firstchar:
                            yield ("BOM", None)
                        elif 0xD800 <= ucs < 0xE000:
                            # Pass surrogate halves through to the UTF-16 filter for handling.
                            # The UTF-16 filter must be used after the UTF-EBCDIC one.
                            yield ("CESU", ucs, "8")
                        elif ucs > 0x10FFFF:
                            yield ("ERROR", "UTFEBCDICBEYOND", ucs)
                        else:
                            yield ("UCS", ucs, "UTF-EBCDIC", subtype)
                        firstchar = False
                        # utfebcdic_brot is now empty, and utfebcdic_seeking will be set by next lead byte
                    #
                #
            #
        else: # i.e. isn't a DOCS, nor a UTF-EBCDIC part of the stream
            yield token
        #
    #
#

