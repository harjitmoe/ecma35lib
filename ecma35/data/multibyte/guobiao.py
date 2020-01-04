#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from ecma35.data import graphdata
from ecma35.data.multibyte import parsers

# Layout of GBK (per GB 18030:2005):
#   GB2312-inherited main EUC plane: [A1-FE][A1-FE], charted between:
#     DBCS 1: [A1-A9][A1-FE] (GB2312 non-hanzi)
#     DBCS PUA 1: [AA-AF][A1-FE] (U+E000 thru U+E233)
#     DBCS 2: [B0-F7][A1-FE] (GB2312 hanzi)
#     DBCS PUA 2: [F8-FE][A1-FE] (U+E234 thru U+E4C5)
#   Lowered lead byte:
#     DBCS 3: [81-A0][40-7E,80-FE] (non-GB2312 hanzi)
#   Lowered trail byte:
#     DBCS PUA 3: [A1-A7][40-7E,80-A0] (U+E4C6 thru U+E765) [A3A0 → IDSP in WHATWG]
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
# 0xFD9B (U+9FA5, i.e. the last one in the "URO proper" from Unicode 1.0.1 and 2.0,
# as opposed to URO additions) as the last one following this pattern. The remaining
# row-and-a-bit is used for non-URO non-GB2312 kanji which are allocated two-byte
# codes, and are somewhat chaotic, with a mixture of mappings to PUA, CJKA, CJKCI.

_temp = []
def read_gbkexceptions(fil):
    # Read GBK/5 and the non-URO part of GBK/4 to an array. Since this part of the
    # mapping cannot be generated automatically from the GB 2312 mapping.
    for _i in open(os.path.join(parsers.directory, fil), "r"):
        if (not _i.strip()) or _i[0] == "#":
            continue
        byts, ucs = _i.split("\t", 2)[:2]
        extpointer = int(byts.strip(), 10)
        pseudoku = (extpointer // 190)
        pseudoten = (extpointer % 190)
        if (pseudoku not in (0x27, 0x28, 0x7C, 0x7D)) or (pseudoten > 95):
            continue
        if (pseudoku == 0x7C) and (pseudoten <= 90):
            continue # Still in the URO part.
        assert ucs[:2] == "0x"
        _temp.append(int(ucs[2:], 16))
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    return r

# GB 2312 (EUC-CN RHS)
graphdata.gsets["ir058"] = gb2312 = (94, 2, parsers.read_main_plane("index-gb18030.txt"))
# Since graphdata.gsets isn't merely a dict, the above line also set graphdata.codepoint_coverages

# Amounting to the entirety of GBK/3 and most of GBK/4, minus the non-URO end part.
non_euccn_uro101 = [i for i in range(0x4E00, 0x9FA6) 
                      if i not in graphdata.codepoint_coverages["ir058"]]

gbk_exceptions = read_gbkexceptions("index-gb18030.txt")
gbk_exceptions_coverage = set(gbk_exceptions)




