#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2022/2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, shutil
from ecma35.data import graphdata, variationhints
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


full2005dict = {(0xE78D,): (0xFE10,), (0xE78E,): (0xFE12,), (0xE78F,): (0xFE11,), 
                (0xE790,): (0xFE13,), (0xE791,): (0xFE14,), (0xE792,): (0xFE15,), 
                (0xE793,): (0xFE16,), (0xE794,): (0xFE17,), (0xE795,): (0xFE18,), 
                (0xE796,): (0xFE19,), (0xE816,): (0x20087,), (0xE817,): (0x20089,), 
                (0xE818,): (0x200CC,), (0xE81E,): (0x9FB4,), (0xE826,): (0x9FB5,), 
                (0xE82B,): (0x9FB6,), (0xE82C,): (0x9FB7,), (0xE831,): (0x215D7,), 
                (0xE832,): (0x9FB8,), (0xE83B,): (0x2298F,), (0xE843,): (0x9FB9,), 
                (0xE854,): (0x9FBA,), (0xE855,): (0x241FE,), (0xE864,): (0x9FBB,)}
def gb2005tofullmap(pointer, ucs):
    return full2005dict.get(ucs, ucs)
def gb2005to2000map(pointer, ucs):
    if ucs == (0x1E3F,):
        return (0xE7C7,)
    return ucs
def gbutcto1986map(pointer, ucs):
    # GB 2312 subset of GB 6345.1.
    # Contra Lunde, GB 6345.1 changes 03-71 from looped to open (not vice versa).
    if ucs == (0xFF47,):
        return (0x0261,)
    return ucs
def gbutcto1980map(pointer, ucs):
    # Original GB 2312. 
    if ucs == (0x953A,):
        return (0x937E,)
    return ucs

# GB/T 2312 (EUC-CN RHS); note that the 2000 and 2005 "editions" refer to GB 18030 edition subsets.
graphdata.gsets["ir058"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("UTC/GB2312.TXT"),
        "GB2312.TXT",
        mapper = gbutcto1980map))
graphdata.gsets["ir058/utc"] = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("UTC/GB2312.TXT"),
        "GB2312.TXT"))
graphdata.gsets["ir058/1986"] = gb2312_1986 = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("UTC/GB2312.TXT"),
        "GB2312.TXT",
        mapper = gbutcto1986map))
graphdata.gsets["ir058/ms"] = (94, 2,
    parsers.decode_main_plane_euc(
        parsers.parse_file_format("ICU/windows-936-2000.ucm"),
        "windows-936-2000.ucm",
        gbklike = True))
graphdata.gsets["ir058/ibm"] = (94, 2,
    parsers.decode_main_plane_euc(
        parsers.parse_file_format("ICU/ibm-1383_P110-1999.ucm"),
        "ibm-1383_P110-1999.ucm"))
graphdata.gsets["ir058/2000"] = (94, 2, 
    parsers.decode_main_plane_whatwg(
        parsers.parse_file_format("WHATWG/index-gb18030.txt"),
        "index-gb18030.txt",
        gbklike = True,
        mapper = gb2005to2000map))
graphdata.gsets["ir058/2005"] = (94, 2, 
    parsers.decode_main_plane_whatwg(
        parsers.parse_file_format("WHATWG/index-gb18030.txt"),
        "index-gb18030.txt",
        gbklike = True))
graphdata.gsetflags["ir058/2005"] |= {"GBK:ALT_4BYTE_CODES"}
# ir058-full differs from ir058-2005 in (a) ACTUALLY USING the Vertical Forms block that was added
#   for the precise purpose of GB18030 compatibility, and (b) not setting the GBK:ALT_4BYTE_CODES
#   flag, so the original codepoint-order four-byte codes are used (i.e. there are two m-acutes).
#   Since there are necessarily unencoded PUA codes and four-byte codes duplicating two-byte codes
#   anyway. And since the whole point of "-full" is to use the non-PUA codepoints where applicable.
graphdata.gsets["ir058/full"] = gb2312_full = (94, 2,
    parsers.decode_main_plane_whatwg(
        parsers.parse_file_format("WHATWG/index-gb18030.txt"),
        "index-gb18030.txt",
        gbklike = True,
        mapper = gb2005tofullmap))

# ITU's extension of ir058, i.e. with 6763 GB 2312 chars, 705 GB 8565.2 chars and 139 others.
# Basically sticks a load of stuff (both hankaku and zenkaku) in what GBK would consider the
#   PUA 1 and PUA 2.
# Actually includes the extended Pinyin letters from GB 6345.1-1986, which would later be
#   incorporated into GB 18030 (including the infamous m-acute). However, iso-ir-165.ucm doesn't 
#   have the benefit of all the GB 18030-2005 mappings, omitting any mapping for the n-grave, which
#   was added in Unicode 3.0.
_ir165_raw = parsers.decode_main_plane_gl(
    parsers.parse_file_format("ICU/iso-ir-165.ucm"),
    "iso-ir-165.ucm")
_ir165_add = [None] * (94 * 94)
_ir165_add[688] = (0x01F9,) # in IR-165 but not mapped in UCM; added in Unicode 3.0.
_ir165_add[916] = (0x0261, 0xF87F)
X = [0x0101, 0x00E1, 0x01CE, 0x00E0, 0x0113, 0x00E9, 0x011B, 
     0x00E8, 0x012B, 0x00ED, 0x01D0, 0x00EC, 0x014D, 0x00F3, 
     0x01D2, 0x00F2, 0x016B, 0x00FA, 0x01D4, 0x00F9, 0x01D6, 
     0x01D8, 0x01DA, 0x01DC, 0x00FC, 0x00EA, 0x0251, 0x1E3F, 
     0x0144, 0x0148, 0x01F9]
for _i in range(658, 689): # Not 689/971 itself since that one gets equated to the ASCII characters.
    _j = _i + (3 * 94)
    _ir165_add[_j] = (X[_i - 658], 0xF87F)
# The range also is used in GB/T 12345, GB 18030 and Macintosh for vertical forms, and the
#   use for fills appears to be original to ITU. Exact mappings don't exist, use approximate ones.
# Consulting both T.101-C and IR-165, since both are imperfect scans, and starting at 06-60:
#   six verticals (U+25A5 is five), 
#   eight verticals (red/gules hatch U+1F7E5), 
#   eight horizontals (blue/azure hatch U+1F7E6), 
#   six horizontals (U+25A4 is five), 
#   8x8 dots (U+1FB90 closest), 
#   6x6 orthogonal hash (verticals almost invisible in IR-165, visible in T.101-C) (U+25A6 is 5x5), 
#   8x8 orthogonal hash (verticals almost invisible in IR-165, visible in T.101-C) (black/sable hatch) (U+2593 closest), 
#   three verticals (U+1D36B), 
#   four verticals (U+1D36C), 
#   three horizontals (U+2630), 
#   four horizontals (U+1FB81), 
#   3x3 orthogonal hash (U+2A69), 
#   orthogonal hash with four verticals and three horizontals (U+1699 closest), 
#   6x6 dots (U+2592 closest), 
#   dots in 4 rows and 6 columns (U+2591 closest), 
#   repeated horizontal dashes in rows with staggered x-offsets (aqua hatch, DoCoMo variant U+1F301), 
#   jagged backslash diagonal (U+25A7 closest, proper hatch), 
#   fine backslash diagonal (green/vert hatch U+1F7E9, closer to U+1FB98 though), 
#   chequer (U+1FB95), 
#   bricks (Noto variant U+1F9F1), 
#   Electric album cover ripples (closest I can find is U+224B sadly), 
#   diamond tesselation (U+25A9 closest).
# 0xFE0E here is partly appropriate, partly kludges related to the CSS fontstacks I'm using.
patterns = (None,) * (5*94 + 59) + ((0x25A5,), (0x1F7E5, 0xFE0E), (0x1F7E6, 0xFE0E), (0x25A4,), (0x1FB90, 0xFE0E), (0x25A6,), (0x2593, 0xFE0E), (0x1D36B,), (0x1D36C,), (0x2630,), (0x1FB81,), (0x2A69,), (0x1699,), (0x2592, 0xFE0E), (0x2591, 0xFE0E), (0x1F301, 0xFE0E), (0x25A7,), (0x1FB98,), (0x1FB95,), (0x1F9F1, 0xFE0E), (0x224B,), (0x25A9,), )
ir165 = parsers.fuse([_ir165_add, _ir165_raw, patterns], "CCITT-Chinese-Full.json")
graphdata.gsets["ir165"] = isoir165 = (94, 2, ir165)
#
# More conventional mapping of the lowercase gs.
_ir165_swapg_add = _ir165_add[:]
_ir165_swapg_add[258], _ir165_swapg_add[689] = (0xFF47,), (0x0261,)
_ir165_swapg_add[916], _ir165_swapg_add[971] = (0x0067,), _ir165_swapg_add[916]
ir165_std = parsers.fuse([_ir165_swapg_add, _ir165_raw, patterns], "CCITT-Chinese-Full-Std.json")
graphdata.gsets["ir165/swapg"] = (94, 2, ir165_std)
#
# Further extended version of IR-165 with additional hanzi in the end of row 8, after the Zhuyin
#   (i.e. kuten 08-83 thru 08-94).
# This, along with the CCITT additions, were two extensions to GB 8565 which formerly left imprints
#   on the Unihan database: https://appsrv.cse.cuhk.edu.hk/~irg/irg/irg50/IRGN2276.pdf
# That this resulted in a duplicate encoding of U+9B25 (between GB 8565 and this unnamed extension)
#   apparently created confusion resulting in four characters (覀粦亅啰) being encoded off by one. The
#   "ir165ext" table probably shouldn't recreate that, since it's merely a combination of extensions,
#   but see "gb8565-oldwrongunihan" below.
ir165_engorged = parsers.fuse([
        ir165,
        (None,) * (7*94 + 82) + ((0x540B,), (0x544E,), (0x5521,), (0x6D6C,), (0x74E9,), (0x96BB,), (0x6E96,), (0x5338,), (0x590A,), (0x897E,), (0x9B25,), (0x9B31,)),
    ], "CCITT-Chinese-Extended.json")
graphdata.gsets["ir165/ext"] = (94, 2, ir165_engorged)
#
# For GB 6345: knock out 06-60 thru 06-81, rows 12 thru 15, 90 thru 94.
graphdata.gsets["gb6345"] = (94, 2, parsers.fuse([
        (None,) * (5*94 + 59) + ((-1,),) * (22),
        (None,) * (11*94) + ((-1,),) * (4*94),
        (None,) * (89*94) + ((-1,),) * (5*94),
        ir165,
    ], "GB6345.json"))
#
# For GB 8565: knock out 06-60 thru 06-81, 08-27 thru 08-32, rows 10 thru 12, 13-51 thru 13-94, and 15-94.
graphdata.gsets["gb8565"] = (94, 2, parsers.fuse([
        (None,) * (5*94 + 59) + ((-1,),) * (22),
        (None,) * (7*94 + 26) + ((-1,),) * 6,
        (None,) * (9*94) + ((-1,),) * (3*94),
        (None,) * (12*94 + 50) + ((-1,),) * 44,
        (None,) * (14*94 + 93) + ((-1,),),
        ir165,
    ], "GB8565.json"))
#
# Reconstruction of the pre-IRGN2276 pseudo-G8 source, complete with erroneous mappings for 覀粦亅啰.
#   See comments above.
graphdata.gsets["gb8565-oldwrongunihan"] = (94, 2, parsers.fuse([
        (None,) * (5*94 + 59) + ((-1,),) * (22),
        (None,) * (7*94 + 26) + ((-1,),) * 6,
        (None,) * (9*94) + ((-1,),) * (2*94),
        (None,) * (14*94 + 88) + ir165_engorged[14*94 + 89:14*94 + 93] + ((-1,), (-1,)),
        ir165_engorged,
    ], "GB8565-OldWrongUnihan.json"))

# Apple's version. Note that it changes 0xFD and 0xFE to single-byte codes.
# Includes the vertical form encodings from GB/T 12345 which would make it into GB 18030, but
#   also without the benefit of the Vertical Forms block; unlike GB 18030, hint sequences are used
#   rather than PUA assignments (and yes, that row maps both unassigned and some assigned to PUA).
# It also includes the GB 6345.1-1986 letters (seeming to have "ɒ" instead of "ɑ" is an editorial
#   error in CHINSIMP.TXT; the listed mapping (as opposed to name) is "ɑ").
macrawgbdata = parsers.read_untracked(
    "Mac/macGB2312.json",
    "Mac/CHINSIMP.TXT",
    parsers.decode_main_plane_euc,
    parsers.parse_file_format("Mac/CHINSIMP.TXT"),
    "Mac/CHINSIMP.TXT-raw",
    gbklike = True)
macgbdata = parsers.read_untracked(
    "Mac/macGB2312.json",
    "Mac/CHINSIMP.TXT",
    parsers.decode_main_plane_euc,
    parsers.parse_file_format("Mac/CHINSIMP.TXT"),
    "Mac/CHINSIMP.TXT",
    gbklike = True,
    mapper = variationhints.ahmap)
graphdata.gsets["ir058/macraw"] = (94, 2, macrawgbdata)
graphdata.gsets["ir058/macsemiraw"] = (94, 2, macgbdata)
graphdata.gsets["ir058/mac"] = gb2312_macfull = (94, 2, parsers.fuse([
    (None,) * 526 + gb2312_full[2][526:555],
    macgbdata], "Mac---CHINSIMP_mainplane_ahmap_fullverts.json"))

# GB/T 12345 (Traditional Chinese in Mainland China, homologous to GB/T 2312 where possible, with
#   the others being added as a couple of rows at the end)
# Unlike GB2312.TXT, redistribution of GB12345.TXT itself is apparently not permitted, although
#   using/incorporating the information is apparently fine.
gbtrad = parsers.read_untracked(
        "UTC/GB_12345.json",
        "UTC/GB12345.TXT",
        parsers.decode_main_plane_euc,
        parsers.parse_file_format("UTC/GB12345.TXT"),
        "UTC/GB12345.TXT",
        gbklike = True)
graphdata.gsets["ir058/hant-utc"] = gb12345_utc = (94, 2, gbtrad + (None,) * (94*94 - len(gbtrad)))
graphdata.gsets["ir058/hant"] = gb12345 = (94, 2, parsers.fuse([
        # U+2225 is already used elsewhere; UTC corrected GB2312 in 1999 but didn't change GB12345.
        (None,) * 11 + ((0x2016,),),
        gb12345_utc[2], 
        (None,) * 526 + gb2312_full[2][526:555],
        (None,) * 684 + gb2312_full[2][684:690],
    ], "GB12345.json"))
graphdata.gsets["ir058/hant-full"] = gb12345_full = (94, 2, parsers.fuse([
        gb12345[2],
        parsers.read_unihan_planes("UCD/Unihan_OtherMappings-15.txt", "kPseudoGB1", kutenform=True),
    ], "GB12345full.json"))
#
# Certain characters are still simplified in GB 12345 proper, but were replaced with traditional
#   characters in the version of GB 12345 supplied to the UTC. Source: Lunde 2009, p.102.
gb1_strict_chars = tuple(((i - 1) * 94) + (j - 1) for i, j in (
    (21, 94),
    (27, 27),
    (27, 29),
    (27, 30),
    (27, 32),
    (27, 33),
    (29, 90),
    (30, 18),
    (30, 27),
    (38, 60),
    (38, 90),
    (39, 17),
    (53, 85),
    (53, 86),
    (53, 88),
    (53, 89),
    (56, 89),
    (58, 77),
    (59, 28),
    (65, 31),
    (74, 15),
    (83, 61),
))
graphdata.gsets["ir058/hant-strict"] = gb12345_strict = (94, 2, parsers.fuse([
        [i if n in gb1_strict_chars else None for n, i in enumerate(gb2312_full[2])],
        gb12345[2],
    ], "GB12345strict.json"))

# GB/T 12052 (Korean in Mainland China). The non-Hangul non-kanji rows are basically
#   the same as GB2312, but there is a second dollar sign instead of a yuan sign.
graphdata.gsets["gb12052"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("Other/gb12052-uni.txt", gb12052 = True),
    "gb12052-uni.txt"))
#
# Being as GB 7589, 13131, 7590, 13132、16500 do not include non-Kanji, Unihan mappings theoretically
#   can describe their entire mappings… in reality, the GB 13131 and 16500 mappings contain almost
#   everything with only a few gaps (listed below), whereas the GB 13132 mapping is full of holes.
# kGB3 and kGB5 actually provide the same data as the G3 and G5 in kIRG_GSource (despite the later
#   citing 13131/13132 and the former citing 7589/7590), except for that kGB3 and kGB5 have many
#   more gaps (they seem to only cover the URO).
#
# A few of the Unihan mappings for GB 13131 and 13132 are off by one:
#   https://appsrv.cse.cuhk.edu.hk/~irg/irg/irg50/IRGN2302EddieLi.pdf
#   Unihan's 03-16-65 thru 03-16-82 should be 03-16-66 thru 03-16-83
#     The 03-16-65 position should be ⿰亻兮 or some traditional variant of it (U+202F9 𠋹 ???).
#     Unihan's 03-16-83 shouldn't be present.
#   Unihan's 05-67-11 thru 05-67-24 should be 05-67-12 thru 05-67-25
#   Unihan's 05-74-05 thru 05-74-15 should be 05-74-04 thru 05-74-14
#
# Handful of GB 7589 / 13131 not mapped to Unicode in kIRG_GSource:
#     U+72AE at 19-57 (traditional / simplified)
#     U+5829 at 20-53 (traditional; simplified not in Unicode)
#     U+22341 at 21-05 (traditional / simplified)
#     U+7D94 at 21-25 (traditional / simplified)
#     U+5570/U+56C9 at 22-51 (simplified: U+5570; traditional: U+56C9)
#     U+625C at 41-53 (traditional / simplified)
#     U+781E at 55-58 (traditional / simplified)
#     U+77AD at 58-43 (traditional; traditional even in GB 7589 since simplified converges to 了)
#     U+79C4 at 59-51 (traditional / simplified)
#     U+8226 at 69-53 (traditional / simplified)
#     U+84C3 at 73-83 (traditional / simplified)
graphdata.gsets["gb13131-unihan"] = (94, 2, parsers.fuse([
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-15.txt", "kIRG_GSource", "G3"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-14.txt", "kIRG_GSource", "G3"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-13.txt", "kIRG_GSource", "G3"),
        (None,) * ((94 * 18) + 56) + ((0x72AE,),),
        (None,) * ((94 * 19) + 52) + ((0x5829,),),
        (None,) * ((94 * 20) + 4) + ((0x22341,),),
        (None,) * ((94 * 20) + 24) + ((0x7D94,),),
        (None,) * ((94 * 21) + 50) + ((0x56C9,),),
        (None,) * ((94 * 40) + 52) + ((0x625C,),),
        (None,) * ((94 * 54) + 57) + ((0x781E,),),
        (None,) * ((94 * 57) + 42) + ((0x77AD,),),
        (None,) * ((94 * 58) + 50) + ((0x79C4,),),
        (None,) * ((94 * 68) + 52) + ((0x8226,),),
        (None,) * ((94 * 72) + 82) + ((0x84C3,),),
    ], "GB13131-Unihan.json"))
_pseudogb3 = graphdata.gsets["gb13131-unihan"][2]
graphdata.gsets["gb13131"] = (94, 2, (
    *_pseudogb3[:1474],
    (0xFFFD,),
    *_pseudogb3[1474:1492],
    *_pseudogb3[1493:]))
graphdata.gsets["gb13132-unihan"] = (94, 2, parsers.fuse([
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-15.txt", "kIRG_GSource", "G5"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-14.txt", "kIRG_GSource", "G5"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-13.txt", "kIRG_GSource", "G5"),
        parsers.read_unihan_planes("UCD/Unihan_OtherMappings-15.txt", "kGB5", kutenform=True),
        parsers.read_unihan_planes("UCD/Unihan_OtherMappings-14.txt", "kGB5", kutenform=True),
        parsers.read_unihan_planes("UCD/Unihan_OtherMappings-13.txt", "kGB5", kutenform=True),
    ], "GB13132-Unihan.json"))
_pseudogb5 = graphdata.gsets["gb13132-unihan"][2]
graphdata.gsets["gb13132"] = (94, 2, (
    *_pseudogb5[:6214],
    None,
    *_pseudogb5[6214:6228],
    *_pseudogb5[6229:6865],
    *_pseudogb5[6866:6877],
    None,
    *_pseudogb5[6877:]))
#
# Small handful of GB16500 not in kIRG_GSource in Unihan 13.0 (Unihan 14.0 unmaps a few more):
#     U+6FF9 at 32-29
#     U+809E at 40-50
#     U+891D at 44-23
graphdata.gsets["gb16500"] = (94, 2, parsers.fuse([
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-15.txt", "kIRG_GSource", "GE"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-14.txt", "kIRG_GSource", "GE"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-13.txt", "kIRG_GSource", "GE"),
        (None,) * ((94 * 31) + 28) + ((0x6FF9,),),
        (None,) * ((94 * 39) + 49) + ((0x809E,),),
        (None,) * ((94 * 43) + 22) + ((0x891D,),),
    ], "GB16500.json"))

# This is an interesting one. Known as G7 or GB7 in Unihan, it is not the Seventh Supplementary Set
#   (which would be GB 16500, Unihan's GE). It seems to have been one of the original source
#   standards from the very beginning: WG2N667 lists nine Chinese sources to be consolidated, being
#   GBs 2312, 12545, 7589, 13131 (not yet so called), 7590, 13132 (likewise) and 8565, "A few
#   additional Han characters (< 100) for Modern Chinese" (presumably this one, since there's only
#   42 or 43 in the first row, which is the only URO-mapped row with the rest being CJKA-mapped,
#   and less than 200 in total) and CNS 11643. It is therefore a supplement to be used alongside
#   GBs 2312, 7589 and 7590 for modern Chinese. Its characters are Simplified in all three rows.
# It has likewise been in the Unihan data since its very first manifestation (CJKXREF), which calls
#   it "General Purpose Han Characters for Modern Chinese", and first assigns it the number 7;
#   GB 16500 is not amongst its sources, and was added later pursuant to IRGN376. Current Unihan
#   calls the Unihan GB7 "General Purpose Hanzi List for Modern Chinese Language, and General List
#   of Simplified Hanzi" ("General List of Simplified Hanzi" may be the CJKA-mapped portion in
#   rows 2 and 3).
# Given this information, I suspect this CCS is entirely fictitious, since it would clearly predate
#   the ability to submit NCSes to the IRG, and it doesn't seem to follow the usual structure of
#   either mostly following GB2312 where applicable in the first 15 rows or leaving them empty
#   (though this, plus its small size, means it doesn't actually *collide* with GB 16500 either).
graphdata.gsets["the-other-gb7"] = (94, 2, parsers.fuse([
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-15.txt", "kIRG_GSource", "G7"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-14.txt", "kIRG_GSource", "G7"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-13.txt", "kIRG_GSource", "G7"),
        parsers.read_unihan_planes("UCD/Unihan_OtherMappings-15.txt", "kGB7", kutenform=True),
        parsers.read_unihan_planes("UCD/Unihan_OtherMappings-14.txt", "kGB7", kutenform=True),
        parsers.read_unihan_planes("UCD/Unihan_OtherMappings-13.txt", "kGB7", kutenform=True),
    ], "the-other-GB7.json"))

graphdata.gsets["gb16500-ext"] = (94, 2, parsers.fuse([
        graphdata.gsets["gb16500"][2],
        graphdata.gsets["the-other-gb7"][2],
    ], "GB16500-with-the-other-GB7.json"))

babelstone_update_map = parsers.read_babelstone_update_file("BabelStone/PUA_1_357_MAPPINGS.TXT")

def babelstone_update_map2(pointer, ucs):
    if stducs := {
            # Not sure why this one hasn't been moved out
            (0xF188,): (0x2EBF0,),
            #
            # Traditional forms etc noted in https://babelstone.co.uk/Fonts/PUA.html
            (0xE1BB,): (0x66AA, 0xF87F),
            (0xE1D0,): (0x983C, 0xF87F),
            (0xE1E1,): (0x24130, 0xF87F),
            (0xE1E4,): (0x2A0E1, 0xF87F),
            (0xE237,): (0x2123B, 0xF87F),
            (0xE238,): (0x22126, 0xF87F),
            (0xE239,): (0x2258D, 0xF87F),
            (0xE23A,): (0x3E93, 0xF87F),
            (0xE23B,): (0x28CCD, 0xF87F),
            (0xE23C,): (0x9587, 0xF87F),
            (0xE23D,): (0x95B3, 0xF87F),
            (0xE23E,): (0x95D8, 0xF87F),
            (0xE23F,): (0x2BCD2, 0xF87F),
            (0xE240,): (0x2B605, 0xF87F),
            (0xE241,): (0x2E73F, 0xF87F),
            (0xE242,): (0x2E75A, 0xF87F),
            (0xE243,): (0x28369, 0xF87F),
            (0xE244,): (0x2839D, 0xF87F),
            (0xE245,): (0x658D, 0xF87F),
            (0xE246,): (0x2445F, 0xF87F),
            (0xE248,): (0x2E056, 0xF87F),
            (0xE249,): (0x2E059, 0xF87F),
            (0xE24A,): (0x21FA9, 0xF87F),
            (0xE24B,): (0x289BC, 0xF87F),
            (0xE24C,): (0x289E7, 0xF87F),
            (0xE24D,): (0x4171, 0xF87F),
            (0xE24E,): (0x7A72, 0xF87F),
            (0xE24F,): (0x4CC6, 0xF87F),
            (0xE250,): (0x4CE9, 0xF87F),
            (0xE251,): (0x2A134, 0xF87F),
            (0xE252,): (0x259E1, 0xF87F),
            (0xE253,): (0x27793, 0xF87F),
            (0xE254,): (0x2A027, 0xF87F),
            (0xE255,): (0x2C83B, 0xF87F),
            (0xE256,): (0x27523, 0xF87F),
            (0xE260,): (0x8AE9, 0xF87F),
            (0xE2A7,): (0x2BBAE, 0xF87F),
            (0xE2A8,): (0x2A927, 0xF87F),
            (0xE2B6,): (0x2139E, 0xF87F),
            (0xE2C7,): (0x2A90E, 0xF87F),
            (0xE2CE,): (0x2BB96, 0xF87F),
            (0xE2D8,): (0x2141B, 0xF87F),
            (0xE2D9,): (0x302B7, 0xF87F),
            (0xE2E1,): (0x58B3, 0xF87F),
            (0xE2F4,): (0x583D, 0xF87F),
            (0xE2FB,): (0x214C7, 0xF87F),
            (0xE301,): (0x214D2, 0xF87F),
            (0xE325,): (0x58A4, 0xF87F),
            (0xE392,): (0x2A00B, 0xF87F),
            (0xE39B,): (0x2B48C, 0xF87F),
            (0xE4A8,): (0x214EB, 0xF87F),
            (0xE4B7,): (0x2C775, 0xF87F),
            (0xE4B9,): (0x8632, 0xF87F),
            (0xE4D1,): (0x30FDF, 0xF87F),
            (0xE4D4,): (0x23DE3, 0xF87F),
            (0xE4DB,): (0x299B5, 0xF87F),
            (0xE4DE,): (0x470C, 0xF87F),
            (0xE4E4,): (0x236E0, 0xF87F),
            (0xE4E5,): (0x2364B, 0xF87F),
            (0xE4E9,): (0x23869, 0xF87F),
            (0xE4EA,): (0x6ACA, 0xF87F),
            (0xE4EF,): (0x22D33, 0xF87F),
            (0xE4F6,): (0x2AD82, 0xF87F),
            (0xE509,): (0x2524A, 0xF87F),
            (0xE511,): (0x26253, 0xF87F),
            (0xE512,): (0x9DF9, 0xF87F),
            (0xE513,): (0x2A0D1, 0xF87F),
            (0xE516,): (0x2CC43, 0xF87F),
            (0xE520,): (0x2A04C, 0xF87F),
            (0xE522,): (0x8E5F, 0xF87F),
            (0xE525,): (0x4C8E, 0xF87F),
            (0xE527,): (0x29F2F, 0xF87F),
            (0xE64B,): (0x214B5, 0xF87F),
            (0xE737,): (0x28D9B, 0xF87F),
            (0xE7F1,): (0x4B7E, 0xF87F),
            (0xEA2F,): (0x4C76, 0xF87F),
            (0xEB6D,): (0x2570B, 0xF87F),
            (0xF187,): (0x23B1B, 0xF87F),
            (0xF1CF,): (0x21804, 0xF87F),
            (0xF200,): (0x254DD, 0xF87F),
            (0xF39E,): (0x29DE8, 0xF87F),
            (0xF39F,): (0x9BCF, 0xF87F),
            (0xF3A0,): (0x9BD3, 0xF87F),
            (0xF3A1,): (0x29E3E, 0xF87F),
            (0xF3A2,): (0x29E1E, 0xF87F),
            (0xF3A3,): (0x29E34, 0xF87F),
            (0xF3A4,): (0x29E97, 0xF87F),
            (0xF3A5,): (0x2B66E, 0xF87F),
            (0xF3A6,): (0x29EF8, 0xF87F),
            (0xF3CC,): (0x22B72, 0xF87F),
            (0xF3D0,): (0x650A, 0xF87F),
            (0xF3D3,): (0x22CF6, 0xF87F),
            }.get(ucs, None):
        return stducs
    return babelstone_update_map(pointer, ucs)

graphdata.gsets["sj11239/babelstonehan"] = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_sjt11239_mapping_file("BabelStone/SJT-IDS.TXT"),
    "SJT-IDS.TXT",
    mapper=babelstone_update_map))

graphdata.gsets["sj11239"] = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_sjt11239_mapping_file("BabelStone/SJT-IDS.TXT",
        include_variation_selectors=False,
        include_uncertain_mappings=True,
        fallback_nothing_selector=(lambda ucs: babelstone_update_map2(None, ucs) == ucs),
        fallback_preferencer=(lambda ucs: babelstone_update_map2(None, ucs) == ucs)),
    "SJT-IDS-supported.TXT",
    mapper=babelstone_update_map2))

# GB 7589 and GB 7590 are just the simplified versions, right?
# (Contrary to docs, kGB3 and kGB5 seem to be less complete mappings to the same G3 and G5
#  in kIRG_GSource, i.e. they are the traditional GB 13131/13132 forms.
#  Notably, GB 13131/13132 appear never published.)
# Cases of multiple Simplified mappings though:
#     GB 13131:
#   0x8b78 譸 → 0x8bea 诪,  0x2c8aa 𬢪 (0x2c8aa is a hybrid; favour BMP over SIP)
#   0x8b32 謲 → 0x2c8b3 𬢳, 0x2c904 𬤄 (0x2c8b3 is a hybrid)
#   0x9c44 鱄 → 0x2b68b 𫚋, 0x31210 𱈐 (0x31210 is a hybrid; favour SIP over TIP)
#   0x9c68 鱨 → 0x9cbf 鲿,  0x31218 𱈘 (0x31218 is a hybrid; favour BMP over TIP)
#   0x9766 靦 → 0x4a44 䩄,  0x817c 腼  (no idea; 腼 is in GB 2312 though, so 䩄 must be GB 7589)
#     GB 13132:
#   0x7060 灠 → 0x6f24 漤,  0x30710 𰜐 (漤 is more common in both and in GB 2312; 𰜐 is simplified 灠)
#   0x9d82 鶂 → 0x2cdfc 𬷼, 0x31288 𱊈 (trad 鷁, simp 鹢 is today more common; favour SIP over TIP)
resolve = {(0x8b78,): (0x8bea,), (0x8b32,): (0x2c904,), (0x9c44,): (0x2b68b,), 
           (0x9c68,): (0x9cbf,), (0x9766,): (0x4a44,), (0x7060,): (0x30710,), 
           (0x9d82,): (0x2cdfc,)}
tradat = parsers.parse_variants("UCD/Unihan_Variants.txt")
_gb7589fn = os.path.join(parsers.cachedirectory, "GB7589-Actual.json")
_gb7590fn = os.path.join(parsers.cachedirectory, "GB7590-Actual.json")
_pseudogb7589fn = os.path.join(parsers.cachedirectory, "GB7589-Unihan.json")
_pseudogb7590fn = os.path.join(parsers.cachedirectory, "GB7590-Unihan.json")
def blonkit(i):
    ret = resolve.get(i, (tradat.get(i, [[],[]])[1] + [i])[0])
    if ret in gb2312_1986[2]:
        return i
    return ret
if (not os.path.exists(_gb7589fn)) or (not os.path.exists(_gb7590fn)) or (not os.path.exists(_pseudogb7589fn)) or (not os.path.exists(_pseudogb7590fn)):
    _gb7589 = tuple(blonkit(i) for i in graphdata.gsets["gb13131"][2])
    _gb7590 = tuple(blonkit(i) for i in graphdata.gsets["gb13132"][2])
    _pseudogb7589 = tuple(blonkit(i) for i in graphdata.gsets["gb13131-unihan"][2])
    _pseudogb7590 = tuple(blonkit(i) for i in graphdata.gsets["gb13132-unihan"][2])
    f = open(_gb7589fn, "w")
    f.write(json.dumps(_gb7589))
    f.close()
    f = open(_gb7590fn, "w")
    f.write(json.dumps(_gb7590))
    f.close()
    f = open(_pseudogb7589fn, "w")
    f.write(json.dumps(_pseudogb7589))
    f.close()
    f = open(_pseudogb7590fn, "w")
    f.write(json.dumps(_pseudogb7590))
    f.close()
else:
    _gb7589 = parsers.LazyJSON(os.path.basename(_gb7589fn))
    _gb7590 = parsers.LazyJSON(os.path.basename(_gb7590fn))
    _pseudogb7589 = parsers.LazyJSON(os.path.basename(_pseudogb7589fn))
    _pseudogb7590 = parsers.LazyJSON(os.path.basename(_pseudogb7590fn))
graphdata.gsets["gb7589"] = gb7589 = (94, 2, _gb7589)
graphdata.gsets["gb7590"] = gb7590 = (94, 2, _gb7590)
graphdata.gsets["gb7589-unihan"] = gb7589 = (94, 2, _pseudogb7589)
graphdata.gsets["gb7590-unihan"] = gb7590 = (94, 2, _pseudogb7590)
# Some traditional forms remain, but I guess this is good enough. They would presumably be forms
#  where simplified counterparts do not exist in Unicode anyway.

# Amounting to the entirety of GBK/3 and most of GBK/4, minus the non-URO end part.
# And, yes, it would indeed be more straightforward to just read the GBK mappings for
# this part from index-gb18030.txt, but I'm trying to make this source code educational on how the
# GBK and UHC pages are laid out.
non_euccn_uro101 = [i for i in range(0x4E00, 0x9FA6) 
                      if i not in graphdata.codepoint_coverages["ir058/2005"]]

# GBK/5, and the non-URO part of GBK/4.
_gbk_exceptions_web = parsers.decode_gbk_non_uro_extras(
    parsers.parse_file_format("WHATWG/index-gb18030.txt"),
    "index-gb18030.txt")
_gbk_exceptions_full = tuple(full2005dict.get(_i, _i) for _i in _gbk_exceptions_web)
_gbk_exceptions = tuple({(0x3000,): (0xE5E5,)}.get(_i, _i) for _i in _gbk_exceptions_web)
graphdata.gsets["gbk-nonuro-extras"] = (96, 2, _gbk_exceptions)
graphdata.gsets["gbk-nonuro-extras-web"] = (96, 2, _gbk_exceptions_web)
graphdata.gsets["gbk-nonuro-extras-full"] = (96, 2, _gbk_exceptions_full)

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
               (i < 0xD800 or i > 0xDFFF) and # i.e. not surrogate (don't count as codepoints)
               (i not in graphdata.codepoint_coverages["gbk-nonuro-extras"]) and
               (i not in graphdata.codepoint_coverages["ir058/2000"]))]




