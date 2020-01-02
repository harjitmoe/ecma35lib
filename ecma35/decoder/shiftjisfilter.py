#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Note that this works by interpreting Shift_JIS codes as the correspending EUC-JP codes would
# have been interpreted; it is therefore possible to make full use of designation sequences to,
# for example, switch to a certain edition of JIS X 0208, or switch to JIS X 0213 (inc. plane 2).

# The 1B 25 40 sequence will indeed switch to ECMA-35, and cannot occur coincidentally since C0/CL
# bytes are not used as trail bytes, so it is in fact "with standard return".
shiftjisdocs = ("DOCS", False, (0x30,))

def decode_shiftjis(stream, state):
    sjis_lead = None
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if (token[0] == "DOCS"):
            if sjis_lead:
                yield ("ERROR", "SJISTRUNC", sjis_lead)
                sjis_lead = None
            if token == shiftjisdocs:
                yield ("RDOCS", "Shift_JIS", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "shift_jis"
                # Sensible-ish defaults (corresponding to Windows-31J, or WHATWG's Shift_JIS)
                state.cur_gsets = ["ir014", "ir168web", "ir013", "ibmsjisext"]
            else:
                yield token
        elif state.docsmode == "shift_jis" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if sjis_lead is None:
                if token[1] < 0x20:
                    yield ("C0", token[1], "SJISONEBYTE")
                elif token[1] < 0x80:
                    # Note: using "G0" rather than "GL" will break ESC entirely, since it relies
                    #       on raw GL (or UCS) opcodes going through (for obvious reasons).
                    yield ("GL", token[1] - 0x20)
                elif token[1] == 0x80:
                    # With reference to correspondances between IBM's 1041 and 4992 (full 896)
                    yield ("G2", 0x40, "SJISONEBYTE")
                elif token[1] < 0xA0:
                    # Lead bytes before the single-byte Katakana
                    sjis_lead = token
                elif token[1] == 0xA0:
                    # Also with reference to IBM 1041/4992.
                    yield ("G2", 0x41, "SJISONEBYTE")
                elif token[1] < 0xE0:
                    # Standard mapping of the JIS X 0201 Kana set to Shift_JIS.
                    yield ("G2", token[1] - 0xA0, "SJISONEBYTE")
                elif token[1] < 0xFD:
                    # Lead bytes after the single-byte Katakana, including those beyond JIS X 0208
                    sjis_lead = token
                else:
                    # Also with reference to IBM 1041/4992.
                    yield ("G2", token[1] - 0xFD + 0x42, "SJISONEBYTE")
            else:
                if token[1] < 0x40 or token[1] > 0xFC or token[1] == 0x7F:
                    yield ("ERROR", "SJISTRUNC", sjis_lead)
                    sjis_lead = None
                    reconsume = token
                    continue
                leadoffset = 0x81 if sjis_lead[1] < 0xA0 else 0xC1
                trailoffset = 0x40 if token[1] < 0x80 else 0x41
                pointer = ((sjis_lead[1] - leadoffset) * 94 * 2) + (token[1] - trailoffset)
                ku = (pointer // 94) + 1
                ten = (pointer % 94) + 1
                if ku <= 94:
                    # JIS X 0208 or JIS X 0213 plane 1 rows.
                    yield ("G1", ku, "SJIS")
                    yield ("G1", ten, "SJIS")
                elif ku <= 103:
                    # JIS X 0213 plane 2 Kanji rows interspersed amongst JIS X 0212 non-Kanji.
                    # Or it could be part of a purpose-designed SJIS trailer set which I've
                    # re-ordered homologously to JIS X 0213 plane 2 so that it can be put in G3.
                    # Shift_JISx0213's placement of row 8 between rows 1 and 3 means that the usual
                    # correspondence between odd/evenness of the ku and the range over which the
                    # ten can be considered to be encoded is preserved.
                    yield ("G3", (1, 8, 3, 4, 5, 12, 13, 14, 15)[ku - 95], "SJIS")
                    yield ("G3", ten, "SJIS")
                else:
                    # JIS X 0213 plane 2 Kanji rows following JIS X 0212 Kanji.
                    # Same as above applies regarding other possible sets.
                    yield ("G3", ku - 104 + 78, "SJIS")
                    yield ("G3", ten, "SJIS")
                sjis_lead = None
            #
        else:
            yield token
        #
    #
#








