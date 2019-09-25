#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import os
_dir = os.path.dirname(os.path.abspath(__file__))

_temp = []
def _read(fil):
    for _i in open(os.path.join(_dir, fil), "r"):
        if _i.strip():
            byts, ucs = _i.split("\t", 2)[:2]
            ku = int(byts[2:4], 16) - 0x20
            ten = int(byts[4:6], 16) - 0x20
            ucs = int(ucs[2:], 16)
            pointer = ((ku - 1) * 94) + (ten - 1)
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





