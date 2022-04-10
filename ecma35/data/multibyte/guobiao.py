#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

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
def gb1986to1980map(pointer, ucs):
    # Reversing non-extensional changes made to GB 2312-1980 by GB 6345.1-1986 and also included
    # in GB 8565.2-1988 (which did not include the extensional changes, rather being an independent
    # but non-collisive extension). These corrigienda were incoporated into mappings such as
    # GB2312.TXT, and into GB 18030.
    if ucs == (0x953A,):
        return (0x937E,)
    if ucs == (0xFF47,):
        return (0x0261,)
    return ucs
def gb1986toregmap(pointer, ucs):
    # The registered ISO-IR chart apparently does it like this. Go figure. Although it does make
    # the ISO-IR chart for the ITU version swapping the lowercase Gs seem even weirder, considering
    # that the ISO-IR reg for GB 2312 displayed a closed one in the ISO-646 row to begin with…
    if ucs == (0x953A,):
        return (0x937E,)
    return ucs

# GB/T 2312 (EUC-CN RHS); note that the 2000 and 2005 "editions" refer to GB 18030 edition subsets.
graphdata.gsets["ir058-1980"] = gb2312_1980 = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("UTC/GB2312.TXT"),
        "GB2312.TXT",
        mapper = gb1986to1980map))
graphdata.gsets["ir058"] = gb2312_1980reg = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("UTC/GB2312.TXT"),
        "GB2312.TXT",
        mapper = gb1986toregmap))
graphdata.gsets["ir058-1986"] = gb2312_1986 = (94, 2,
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("UTC/GB2312.TXT"),
        "GB2312.TXT"))
graphdata.gsets["ir058-ms"] = gb2312_ms = (94, 2,
    parsers.decode_main_plane_euc(
        parsers.parse_file_format("ICU/windows-936-2000.ucm"),
        "windows-936-2000.ucm",
        gbklike = True))
graphdata.gsets["ir058-ibm"] = gb2312_ibm = (94, 2,
    parsers.decode_main_plane_euc(
        parsers.parse_file_format("ICU/ibm-1383_P110-1999.ucm"),
        "ibm-1383_P110-1999.ucm"))
graphdata.gsets["ir058-2000"] = gb2312_2000 = (94, 2, 
    parsers.decode_main_plane_whatwg(
        parsers.parse_file_format("WHATWG/index-gb18030.txt"),
        "index-gb18030.txt",
        gbklike = True,
        mapper = gb2005to2000map))
graphdata.gsets["ir058-2005"] = gb2312_2005 = (94, 2, 
    parsers.decode_main_plane_whatwg(
        parsers.parse_file_format("WHATWG/index-gb18030.txt"),
        "index-gb18030.txt",
        gbklike = True))
graphdata.gsetflags["ir058-2005"] |= {"GBK:ALT_4BYTE_CODES"}
# ir058-full differs from ir058-2005 in (a) ACTUALLY USING the Vertical Forms block that was added
#   for the precise purpose of GB18030 compatibility, and (b) not setting the GBK:ALT_4BYTE_CODES
#   flag, so the original codepoint-order four-byte codes are used (i.e. there are two m-acutes).
#   Since there are necessarily unencoded PUA codes and four-byte codes duplicating two-byte codes
#   anyway. And since the whole point of "-full" is to use the non-PUA codepoints where applicable.
graphdata.gsets["ir058-full"] = gb2312_full = (94, 2,
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
# Also, the closed-tail and open-tail "g" glyphs are inverted in the ISO-IR-165 registration with
#   respect to (say) GB 18030 or Macintosh Simplified Chinese, and this is reflected in the UCM  
#   file from ICU, with their mappings also being the other way around. This is apparently related 
#   to the plain "g" being defined as open-tailed in GB 2312-1980, and altered to closed-tailed in 
#   GB 6345.1-1986 (which added the separate code for the open-tailed one), with GB 8565.2-1988 
#   also including this change (see Lunde). The question remains, of course, of whether the ITU
#   version swapped them to restore the 1980 layout, or just double-applied the swap (that the
#   ISO-IR-58 registration actually shows a closed-tail version for the plain "g" anyway — despite
#   not changing 鍾 to 锺, per the other corrigiendum made by GB 6345.1 to an existing GB 2312
#   character — might suggest the latter, if it had any impact). Interestingly, Lunde doesn't seem
#   to mention this discrepency, rather listing it as incorporating all modifications and additions
#   in both GB 6345.1 and GB 8565.2… but keeping ICU mappings, in all respects besides adding the
#   missing ones where possible, seems sensible.
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
# The various pattern fill characters in the latter part of the Greek row are still unmapped,
#   but shouganai. (The range also is used in GB/T 12345, GB 18030 and Macintosh for vertical
#   forms, and the use for fills appears to be original to ITU.)
ir165 = parsers.fuse([_ir165_add, _ir165_raw], "CCITT-Chinese-Full.json")
graphdata.gsets["ir165"] = isoir165 = (94, 2, ir165)
# Include one which actually conforms to standards in which way around the lowercase Gs are too…
_ir165_std_add = _ir165_add[:]
_ir165_std_add[258], _ir165_std_add[689] = (0xFF47,), (0x0261,)
_ir165_std_add[916], _ir165_std_add[971] = (0x0067,), _ir165_std_add[916]
ir165_std = parsers.fuse([_ir165_std_add, _ir165_raw], "CCITT-Chinese-Full-Std.json")
graphdata.gsets["ir165std"] = isoir165 = (94, 2, ir165_std)

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
graphdata.gsets["ir058-macraw"] = (94, 2, macrawgbdata)
graphdata.gsets["ir058-macsemiraw"] = (94, 2, macgbdata)
graphdata.gsets["ir058-mac"] = gb2312_macfull = (94, 2, parsers.fuse([
    (None,) * 526 + gb2312_full[2][526:555],
    macgbdata], "Mac---CHINSIMP_mainplane_ahmap_fullverts.json"))

# GB/T 12345 (Traditional Chinese in Mainland China, homologous to GB/T 2312 where possible, with
#   the others being added as a couple of rows at the end)
# Unlike GB2312.TXT, redistribution of GB12345.TXT itself is apparently not permitted, although
#   using/incorporating the information is apparently fine.
graphdata.gsets["ir058-hant"] = gb12345 = (94, 2, parsers.fuse([parsers.read_untracked(
        "UTC/GB_12345.json",
        "UTC/GB12345.TXT",
        parsers.decode_main_plane_euc,
        parsers.parse_file_format("UTC/GB12345.TXT"),
        "UTC/GB12345.TXT",
        gbklike = True), 
    (None,) * 526 + gb2312_full[2][526:555],
    (None,) * 684 + gb2312_full[2][684:690]], "GB12345.json"))

# GB/T 12052 (Korean in Mainland China). The non-Hangul non-kanji rows are basically
#   the same as GB2312, but there is a second dollar sign instead of a yuan sign.
graphdata.gsets["gb12052"] = gb12052 = (94, 2, parsers.decode_main_plane_euc(
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
# Handful of GB 7589 / 13131 not mapped to Unicode in Unihan:
#     U+72AE at 19-57 (traditional / simplified)
#     U+5829 at 20-53 (traditional; simplified not in Unicode)
#     U+22341 at 21-05 (traditional / simplified)
#     U+7D94 at 21-25 (traditional / simplified)
#     U+5570/U+56C9 at 22-51 (simplified: U+5570; traditional: U+56C9)
#     U+625C at 41-53 (traditional / simplified)
#     U+781E at 55-58 (traditional / simplified)
#     ??? at 58-43
#     U+79C4 at 59-51 (traditional / simplified)
#     U+8226 at 69-53 (traditional / simplified)
#     U+84C3 at 73-83 (traditional / simplified)
graphdata.gsets["gb13131"] = gb13131 = (94, 2, parsers.fuse([
        parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_GSource", "G3"),
        (None,) * ((94 * 18) + 56) + ((0x72AE,),),
        (None,) * ((94 * 19) + 52) + ((0x5829,),),
        (None,) * ((94 * 20) + 4) + ((0x22341,),),
        (None,) * ((94 * 20) + 24) + ((0x7D94,),),
        (None,) * ((94 * 21) + 50) + ((0x56C9,),),
        (None,) * ((94 * 40) + 52) + ((0x625C,),),
        (None,) * ((94 * 54) + 57) + ((0x781E,),),
        (None,) * ((94 * 58) + 50) + ((0x79C4,),),
        (None,) * ((94 * 68) + 52) + ((0x8226,),),
        (None,) * ((94 * 72) + 82) + ((0x84C3,),),
    ], "GB13131.json"))
graphdata.gsets["gb13132"] = gb13132 = (94, 2, 
        parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_GSource", "G5"))
#
# Small handful of GB16500 not mapped to Unicode in Unihan:
#     U+6FF9 at 32-29
#     U+809E at 40-50
#     U+891D at 44-23
graphdata.gsets["gb16500"] = gb16500 = (94, 2, parsers.fuse([
        parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_GSource", "GE"),
        (None,) * ((94 * 31) + 28) + ((0x6FF9,),),
        (None,) * ((94 * 39) + 49) + ((0x809E,),),
        (None,) * ((94 * 43) + 22) + ((0x891D,),),
    ], "GB16500.json"))

# GB 7589 and GB 7590 are just the simplified versions, right?
# (Contrary to docs, kGB3 and kGB5 seem to be a subset of the G3 and G5 in kIRG_GSource, i.e. they
#  are the traditional GB 13131/13132 forms. Notably, GB 13131/13132 appear never published.)
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
_gb7589fn = os.path.join(parsers.cachedirectory, "GB7589.json")
_gb7590fn = os.path.join(parsers.cachedirectory, "GB7590.json")
if (not os.path.exists(_gb7589fn)) or (not os.path.exists(_gb7590fn)):
    _gb7589 = tuple(resolve.get(i, (tradat.get(i, [[],[]])[1] + [i])[0]) for i in gb13131[2])
    _gb7590 = tuple(resolve.get(i, (tradat.get(i, [[],[]])[1] + [i])[0]) for i in gb13132[2])
    f = open(_gb7589fn, "w")
    f.write(json.dumps(_gb7589))
    f.close()
    f = open(_gb7590fn, "w")
    f.write(json.dumps(_gb7590))
    f.close()
else:
    _gb7589 = parsers.LazyJSON(os.path.basename(_gb7589fn))
    _gb7590 = parsers.LazyJSON(os.path.basename(_gb7590fn))
graphdata.gsets["gb7589"] = gb7589 = (94, 2, _gb7589)
graphdata.gsets["gb7590"] = gb7590 = (94, 2, _gb7590)
# Some traditional forms remain, but I guess this is good enough. They would presumably be forms
#  where simplified counterparts do not exist in Unicode anyway.

# Amounting to the entirety of GBK/3 and most of GBK/4, minus the non-URO end part.
# And, yes, it would indeed be more straightforward to just read the GBK mappings for
# this part from index-gb18030.txt, but I'm trying to make this source code educational on how the
# GBK and UHC pages are laid out.
non_euccn_uro101 = [i for i in range(0x4E00, 0x9FA6) 
                      if i not in graphdata.codepoint_coverages["ir058-2005"]]

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
               (i not in graphdata.codepoint_coverages["ir058-2000"]))]




