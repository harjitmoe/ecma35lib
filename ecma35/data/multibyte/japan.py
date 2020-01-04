#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import unicodedata as ucd
from ecma35.data import graphdata
from ecma35.data.multibyte import parsers

_temp = []
def read_jis_trailer(fil, *, mapper=parsers.identitymap):
    # Read the post-94^n part from the end of the extended JIS X 0208 index from WHATWG and map it
    # onto a G3 set by JIS X 0213 rules.
    # Only used here, so not much point putting this in multibyte.parsers…
    for _i in open(os.path.join(parsers.directory, fil), "r"):
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

# Use of Zenkaku vs. Hankaku codepoints differs between the x0213.org mappings for EUC vs. SJIS.
# If we don't know what SBCS it's being used with, best to just use Zenkaku consistently…
def _flatten(u):
    if u == "\uffe3":
        # U+203E is usually considered the normal equivalent, at least in CJK contexts, although
        # the formal name seems to suggest U+00AF (informal annotations identify U+203E as
        # another). In either case, the NFKC is actually U+0020+0304, which isn't suitable here.
        return "\u203e"
    return ucd.normalize("NFKC", u)
_to_zenkaku = dict([
    (ord(_flatten(chr(i))), i)
    for i in range(0xFF00, 0xFFF0) 
    if ucd.east_asian_width(chr(i)) == "F"
])
def map_to_zenkaku(pointer, ucs):
    if len(ucs) == 1 and ucs[0] in _to_zenkaku:
        return (_to_zenkaku[ucs[0]],)
    return ucs

# JIS C 6226:1978 / JIS X 0208:1978
graphdata.gsets["ir042"] = jisx0208_gzdm4_at = (94, 2, parsers.read_main_plane("x208_1978.txt"))
# JIS C 6226:1983 / JIS X 0208:1983
graphdata.gsets["ir087"] = jisx0208_gzdm4_b = (94, 2, parsers.read_main_plane("x208_1983.txt"))
# JIS X 0212:1990 (i.e. the 1990 supplementary plane)
graphdata.gsets["ir159"] = jisx0212 = (94, 2, parsers.read_main_plane("index-jis0212.txt", whatwgjis=True))
# JIS X 0208:1990 or 1997
graphdata.gsets["ir168"] = jisx0208_irr_at_gzdm4_b = (94, 2, parsers.read_main_plane("x208_1990.txt"))
# JIS X 0208, Microsoft and WHATWG version, as specified for use in HTML5
graphdata.gsets["ir168web"] = jisx0208_html5 = (94, 2, parsers.read_main_plane("index-jis0208.txt", whatwgjis=True))
graphdata.gsets["ibmsjisext"] = sjis_html5_g3 = (94, 2, read_jis_trailer("index-jis0208.txt"))
# JIS X 2013:2004
graphdata.gsets["ir233"] = jisx0213_plane1 = (94, 2,
        parsers.read_main_plane("euc-jis-2004-std.txt", eucjp = True, plane = 1, mapper = map_to_zenkaku))
graphdata.gsets["ir228"] = jisx0213_plane1 # 2000 edition with different escape, treat same for now
graphdata.gsets["ir229"] = jisx0213_plane2 = (94, 2, # Code unchanged from original edition.
        parsers.read_main_plane("euc-jis-2004-std.txt", eucjp = True, plane = 2, mapper = map_to_zenkaku))



