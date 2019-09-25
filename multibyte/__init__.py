#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import os
_dir = os.path.dirname(os.path.abspath(__file__))

_temp = []
def _read(fil):
    for _i in open(os.path.join(_dir, fil), "r"):
        if _i.strip() and (_i[0] != "#"):
            byts, ucs = _i.split("\t", 2)[:2]
            #
            if byts[:2] == "0x":
                ku = int(byts[2:4], 16) - 0x20
                ten = int(byts[4:6], 16) - 0x20
            else:
                extpointer = int(byts.strip(), 10)
                ku = (extpointer // 190) - 31
                ten = (extpointer % 190) - 95
                if not ((1 <= ku <= 94) and (1 <= ten <= 94)):
                    continue
            pointer = ((ku - 1) * 94) + (ten - 1)
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

jisx0208_gzdm4_at = (94, 2, _read("x208_1978.txt"))
jisx0208_gzdm4_b = (94, 2, _read("x208_1983.txt"))
jisx0208_irr_at_gzdm4_b = (94, 2, _read("x208_1990.txt"))
jisx0212 = (94, 2, _read("x212_1990.txt"))
gb2312 = (94, 2, _read("index-gb18030.txt"))
wansung = (94, 2, _read("index-euc-kr.txt"))





