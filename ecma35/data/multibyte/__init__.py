#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from ecma35.data import graphdata
_dir = os.path.dirname(os.path.abspath(__file__))

_temp = []
def _read(fil, whatwgjis=False):
    for _i in open(os.path.join(_dir, fil), "r"):
        if _i.strip() and (_i[0] != "#"):
            byts, ucs = _i.split("\t", 2)[:2]
            #
            if byts[:2] == "0x":
                ku = int(byts[2:4], 16) - 0x20
                ten = int(byts[4:6], 16) - 0x20
            elif whatwgjis:
                pointer = int(byts.strip(), 10)
                ku = (pointer // 94) + 1
                ten = (pointer % 94) + 1
                if ku > 94:
                    continue
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

def _read_jistrailer(fil):
    for _i in open(os.path.join(_dir, fil), "r"):
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

# JIS C 6226:1978 / JIS X 0208:1978
graphdata.gsets["ir042"] = jisx0208_gzdm4_at = (94, 2, _read("x208_1978.txt"))
# GB 2312 (EUC-CN RHS)
graphdata.gsets["ir058"] = gb2312 = (94, 2, _read("index-gb18030.txt"))
# JIS C 6226:1983 / JIS X 0208:1983
graphdata.gsets["ir087"] = jisx0208_gzdm4_b = (94, 2, _read("x208_1983.txt"))
# KS C 5601 / KS X 1001 EUC-KR Wansung RHS
graphdata.gsets["ir149"] = wansung = (94, 2, _read("index-euc-kr.txt"))
# JIS X 0212:1990 (i.e. the 1990 supplementary plane)
graphdata.gsets["ir159"] = jisx0212 = (94, 2, _read("index-jis0212.txt", whatwgjis=True))
# JIS X 0208:1990 or 1997
graphdata.gsets["ir168"] = jisx0208_irr_at_gzdm4_b = (94, 2, _read("x208_1990.txt"))
# JIS X 0208, Microsoft and WHATWG version, as specified for use in HTML5
graphdata.gsets["ir168web"] = jisx0208_html5 = (94, 2, _read("index-jis0208.txt", whatwgjis=True))
graphdata.gsets["ibmsjisext"] = sjis_html5_g3 = (94, 2, _read_jistrailer("index-jis0208.txt"))





