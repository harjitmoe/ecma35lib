#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, binascii

directory = os.path.dirname(os.path.abspath(__file__))
_temp = []
_identitymap = lambda pointer, ucs: ucs

def read_main_plane(fil, *, whatwgjis=False, eucjp=False, plane=None, mapper=_identitymap):
    for _i in open(os.path.join(directory, fil), "r"):
        if not _i.strip():
            continue
        elif _i[0] == "#":
            continue # is a comment.
        elif _i[0] == "<" and _i[:2] != "<U":
            continue # is ICU metadata or state machine config which isn't relevant to us.
        elif _i.strip() in ("CHARMAP", "END CHARMAP"):
            continue # ICU delimitors we don't care about.
        elif _i[:2] == "0x":
            # Consortium-style format, over GL (or GR with eucjp=1) without transformation.
            byts, ucs = _i.split("\t", 2)[:2]
            if not eucjp:
                men = 1
                ku = int(byts[2:4], 16) - 0x20
                ten = int(byts[4:6], 16) - 0x20
            else:
                men = 1
                if byts[2].upper() in "01234567": # ASCII
                    continue
                elif byts[2:4].upper() == "8E": # Half-width Katakana (via SS2)
                    continue
                elif byts[2:4].upper() == "8F":
                    if len(byts) == 4: # i.e. SS3 itself rather than an SS3 sequence
                        continue
                    byts = byts[2:]
                    men = 2
                elif byts[2].upper() in ("8", "9"): # Remaining CR C1 controls
                    continue
                elif not ucs.strip(): # i.e. code not used
                    continue
                ku = int(byts[2:4], 16) - 0xA0
                ten = int(byts[4:6], 16) - 0xA0
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
        elif _i[:2] == "<U":
            # ICU-style format, over GL without transformation
            ucs, byts, direction = _i.split(" ", 2)
            assert byts[:2] == "\\x"
            byts = [int(i, 16) for i in byts[2:].split("\\x")]
            if direction.strip() == "|1":
                # i.e. best-fit mapped by the encoder only
                # Whereas, |3 means it's used only be the decoder (usually because duplicate)
                continue
            if len(byts) == 3:
                if 0x80 < byts[0] < 0xA0: # cns-11643-1992.ucm does this for some reason.
                    men = byts[0] - 0x80
                else:
                    men = byts[0] - 0x20
                ku = byts[1] - 0x20
                ten = byts[2] - 0x20
            else:
                assert len(byts) == 2 # Otherwise why is it in the multibyte folder?
                men = 1
                ku = byts[0] - 0x20
                ten = byts[1] - 0x20
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
        elif whatwgjis:
            # Format of the WHATWG-supplied indices for Windows-31J and JIS X 0212.
            # Needs an argument since we can't otherwise tell it from the next one.
            byts, ucs = _i.split("\t", 2)[:2]
            pointer = int(byts.strip(), 10)
            men = 1
            ku = (pointer // 94) + 1
            ten = (pointer % 94) + 1
            if ku > 94:
                continue
        else:
            # Format of the WHATWG-supplied indices for UHC and GBK.
            byts, ucs = _i.split("\t", 2)[:2]
            extpointer = int(byts.strip(), 10)
            men = 1
            ku = (extpointer // 190) - 31
            ten = (extpointer % 190) - 95
            if not ((1 <= ku <= 94) and (1 <= ten <= 94)):
                continue
        pointer = ((men - 1) * 94 * 94) + ((ku - 1) * 94) + (ten - 1)
        #
        assert ucs[:2] in ("0x", "U+", "<U"), ucs
        ucs = mapper(pointer, tuple(int(j, 16) for j in ucs[2:].rstrip(">").split("+")))
        #
        if len(_temp) > pointer:
            assert _temp[pointer] is None
            _temp[pointer] = ucs
        else:
            while len(_temp) < pointer:
                _temp.append(None)
            _temp.append(ucs)
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    return r

def read_jis_trailer(fil, *, mapper=_identitymap):
    for _i in open(os.path.join(directory, fil), "r"):
        if _i.strip() and (_i[0] != "#"):
            byts, ucs = _i.split("\t", 2)[:2]
            #
            pointer = int(byts.strip(), 10)
            ku = (pointer // 94) + 1
            ten = (pointer % 94) + 1
            if ku <= 94:
                continue
            elif ku <= 103:
                g3ku = (1, 8, 3, 4, 5, 12, 13, 14, 15)[ku - 95]
            else:
                g3ku = ku + 78 - 104
            g3pointer = ((g3ku - 1) * 94) + (ten - 1)
            #
            assert ucs[:2] in ("0x", "U+")
            ucs = mapper(g3pointer, int(ucs[2:], 16))
            #
            if len(_temp) > g3pointer:
                assert _temp[g3pointer] is None
                _temp[g3pointer] = ucs
            else:
                while len(_temp) < g3pointer:
                    _temp.append(None)
                _temp.append(ucs)
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    return r

# Layout of GBK (per GB 18030:2005):
#   GB2312-inherited main EUC plane: [A1-FE][A1-FE], charted between:
#     DBCS 1: [A1-A9][A1-FE] (GB2312 non-hanzi)
#     DBCS PUA 1: [AA-AF][A1-FE] (U+E11A thru U+E233)
#     DBCS 2: [B0-F7][A1-FE] (GB2312 hanzi)
#     DBCS PUA 2: [F8-FE][A1-FE] (U+E234 thru U+E4C5)
#   Lowered lead byte:
#     DBCS 3: [81-A0][40-7E,80-FE] (non-GB2312 hanzi)
#   Lowered trail byte:
#     DBCS PUA 3: [A1-A7][40-7E,80-A0] (U+E4C6 thru U+E765)
#     DBCS 5: [A8-A9][40-7E,80-A0] (non-GB2312 non-hanzi)
#     DBCS 4: [AA-FE][40-7E,80-A0] (non-GB2312 hanzi)
#
# SBCS ([00-80,FF]) is GB/T 11383 without shift codes in theory, although it's
# ASCII with a Euro sign at 0x80 in practice. Notably, the Yen sign U+00A5 is
# encoded at 0x81308436, so this is literally just GB 18030 displaying U+0024 as 
# a Yuan sign, not a difference in mapping. Why you make this so confusing?
#
# From a cursory skim, DBCS 3 seems to be walking through the URO and picking only
# the hanzi not included in DBCS 2, abruptly finishing when it runs out of space.
# DBCS 4 picks up immediately from where DBCS 3 left off, and continues this until
# 0xFD9B (U+9FA5, i.e. the last character in the "URO proper" from Unicode 1.0.1,
# as opposed to URO additions) as the last one following this pattern. The remaining
# row-and-a-bit is somewhat chaotic, with a mixture of mappings to PUA, CJKA, CJKCI.




