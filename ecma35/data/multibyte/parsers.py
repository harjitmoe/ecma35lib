#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, binascii

directory = os.path.dirname(os.path.abspath(__file__))
_temp = []

def read_main_plane(fil, *, whatwgjis=False, plane=None):
    for _i in open(os.path.join(directory, fil), "r"):
        if _i.strip() and (_i[0] != "#"):
            if _i[:2] == "0x":
                # Consortium-style format, over GL without transformation.
                byts, ucs = _i.split("\t", 2)[:2]
                men = 1
                ku = int(byts[2:4], 16) - 0x20
                ten = int(byts[4:6], 16) - 0x20
            elif _i[:2] == "<U":
                # ICU-style format, over GL without transformation
                ucs, byts, direction = _i.split(" ", 2)
                assert byts[:2] == "\\x"
                byts = [int(i, 10) for i in byts[2:].split("\\x")]
                if len(byts) == 3:
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
            assert ucs[:2] in ("0x", "U+")
            ucs = int(ucs[2:], 16)
            #
            assert len(_temp) <= pointer
            while len(_temp) < pointer:
                _temp.append(None)
            _temp.append(ucs)
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    return r

def read_jis_trailer(fil):
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
            ucs = int(ucs[2:], 16)
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





