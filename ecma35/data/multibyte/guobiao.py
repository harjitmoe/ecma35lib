#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json
from ecma35.data import graphdata
from ecma35.data.multibyte import mbmapparsers as parsers

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

full2005dict = {0xE78D: 0xFE10, 0xE78E: 0xFE12, 0xE78F: 0xFE11, 0xE790: 0xFE13, 0xE791: 0xFE14, 0xE792: 0xFE15, 0xE793: 0xFE16, 0xE794: 0xFE17, 0xE795: 0xFE18, 0xE796: 0xFE19, 0xE816: 0x20087, 0xE817: 0x20089, 0xE818: 0x200CC, 0xE81E: 0x9FB4, 0xE826: 0x9FB5, 0xE82B: 0x9FB6, 0xE82C: 0x9FB7, 0xE831: 0x215D7, 0xE832: 0x9FB8, 0xE83B: 0x2298F, 0xE843: 0x9FB9, 0xE854: 0x9FBA, 0xE855: 0x241FE, 0xE864: 0x9FBB}
gb2005tofullmap = lambda pointer, ucs: (full2005dict.get(ucs[0], ucs[0]),) if not ucs[1:] else ucs
gb2005to2000map = lambda pointer, ucs: ucs if ucs != (0x1E3F,) else (0xE7C7,)

# GB/T 2312 (EUC-CN RHS); note that the 2000 and 2005 "editions" refer to GB 18030 edition subsets.
graphdata.gsets["ir058-1980"] = gb2312_1980 = (94, 2, # is this same as ibm-5478_P100-1995.ucm ?
                                parsers.read_main_plane("GB2312.TXT"))
graphdata.gsets["ir058-2000"] = gb2312_2000 = (94, 2, 
                                parsers.read_main_plane("index-gb18030.txt", mapper = gb2005to2000map))
graphdata.gsets["ir058-2005"] = gb2312_2005 = (94, 2, 
                                parsers.read_main_plane("index-gb18030.txt"))
graphdata.gsets["ir058-web"] = gb2312_2005 # Not different here, but treated differently by gbkfilter
graphdata.gsets["ir058-full"] = gb2312_full = (94, 2,
                                parsers.read_main_plane("index-gb18030.txt", mapper = gb2005tofullmap))
# Since graphdata.gsets isn't merely a dict, the above lines also set graphdata.codepoint_coverages

# ITU's extension of ir058-1980, i.e. with 6763 GB 2312 chars, 705 GB 8565.2 chars and 139 others.
# Basically sticks a load of stuff (both hankaku and zenkaku) in what GBK would consider the
# PUA 1 and PUA 2.
graphdata.gsets["ir165"] = gb2312_1980 = (94, 2, parsers.read_main_plane("iso-ir-165.ucm"))

# GB/T 12345 (Traditional Chinese in Mainland China, homologous to GB/T 2312 where possible)
# Unlike GB2312.TXT, redistribution of GB12345.TXT itself is apparently not permitted, although
#   using/incorporating the information is apparently fine.
graphdata.gsets["ir058-hant"] = gb12345 = (94, 2, tuple(tuple(i) if i is not None else None for
    i in json.load(open(os.path.join(parsers.directory, "GB_12345.json"), "r"))))

# Amounting to the entirety of GBK/3 and most of GBK/4, minus the non-URO end part.
# And, yes, it would indeed be more straightforward to just read the GBK mappings for
# this part from index-gb18030.txt, but I'm trying to make this source code educational on how the
# GBK and UHC pages are laid out.
non_euccn_uro101 = [i for i in range(0x4E00, 0x9FA6) 
                      if i not in graphdata.codepoint_coverages["ir058-2005"]]

# GBK/5, and the non-URO part of GBK/4.
gbk_exceptions = read_gbkexceptions("index-gb18030.txt")
gbk_exceptions_full = tuple(full2005dict.get(_i, _i) for _i in gbk_exceptions) # For use with ir058-full
gbk_exceptions_coverage = set(gbk_exceptions)
gbk_exceptions_full_coverage = set(gbk_exceptions_full)

# Amounting to the first section of four-byte codes in GB18030: the second section can be mapped
# directly, since no astral codepoint is in any part of the 2000 standard mappings for GBK (nor in
# the 2005 standard mappings, for that matter), even though they do appear there in _de facto_
# mappings which avoid mapping fully defined characters to PUA (see full2005dict above).
# This does have to be generated from the 2000 edition standard mappings for the two-byte codes
# (if the 2005 edition mappings are used, everything between U+1E3F and U+E7C7 finishes up off by 
# one); the re-mapping of index 7457(dec) to 0xE7C7 in the 2005 version is handled directly by 
# decoders.gbhalfcodes itself.
non_gbk_bmp = [i for i in range(0x0080, 0x10000)
           if ((i < 0x4E00 or i > 0x9FA5) and # i.e. not part of the original URO set
               (i < 0xE4C6 or i > 0xE765) and # i.e. not part of the GBK third PUA section
               (i < 0xD800 or i > 0xDFFF) and # i.e. not surrogate (don't count as codepoints)
               (i not in gbk_exceptions_coverage) and # i.e. not part of GBK/4 additions or GBK/5
               (i not in graphdata.codepoint_coverages[ # i.e. not in main plane of 2000 edition
                         "ir058-2000"]))]




