#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, shutil
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
    for _i in open(os.path.join(parsers.directory, fil), "r", encoding="utf-8"):
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
def gb2005tofullmap(pointer, ucs):
    if not ucs[1:]:
        return (full2005dict.get(ucs[0], ucs[0]),)
    return ucs
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
                            parsers.read_main_plane("UTC/GB2312.TXT", mapper = gb1986to1980map))
graphdata.gsets["ir058"]      = gb2312_1980 = (94, 2,
                            parsers.read_main_plane("UTC/GB2312.TXT", mapper = gb1986toregmap))
graphdata.gsets["ir058-1986"] = gb2312_1980 = (94, 2, # is this same as ibm-5478_P100-1995.ucm ?
                            parsers.read_main_plane("UTC/GB2312.TXT"))
graphdata.gsets["ir058-2000"] = gb2312_2000 = (94, 2, 
            parsers.read_main_plane("WHATWG/index-gb18030.txt", euckrlike=True, mapper = gb2005to2000map))
graphdata.gsets["ir058-2005"] = gb2312_2005 = (94, 2, 
                            parsers.read_main_plane("WHATWG/index-gb18030.txt", euckrlike=True))
graphdata.gsetflags["ir058-2005"] |= {"GBK:ALT_4BYTE_CODES"}
graphdata.gsets["ir058-web"]  = gb2312_2005
graphdata.gsetflags["ir058-web"] |= {"GBK:UDC_E5E5_AS_SPACE"}
graphdata.gsetflags["ir058-web"] |= {"GBK:ALT_4BYTE_CODES"}
graphdata.gsets["ir058-full"] = gb2312_full = (94, 2,
            parsers.read_main_plane("WHATWG/index-gb18030.txt", euckrlike=True, mapper = gb2005tofullmap))
graphdata.gsetflags["ir058-full"] |= {"GBK:FULLEXCEPTIONS"}
graphdata.gsetflags["ir058-full"] |= {"GBK:UDC_E5E5_AS_SPACE"}

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
ir165 = list(parsers.read_main_plane("ICU/iso-ir-165.ucm"))
ir165[688] = (0x01F9,) # in IR-165 but not mapped in UCM; added in Unicode 3.0.
ir165[916] = ir165[258] + (0xF87F,)
for _i in range(658, 689): # Not 689/971 itself since that one gets equated to the ASCII characters.
    _j = _i + (3 * 94)
    ir165[_j] = ir165[_i] + (0xF87F,)
# The various pattern fill characters in the latter part of the Greek row are still unmapped,
#   but shouganai. (The range also corresponds to GB 18030 and Macintosh vertical forms, and 
#   appears to be original to ITU.)
graphdata.gsets["ir165"] = isoir165 = (94, 2, tuple(ir165))
# Include one which actually conforms to standards in which way around the lowercase Gs are too…
ir165_std = ir165[:]
ir165_std[258], ir165_std[689] = ir165_std[689], ir165_std[258]
ir165_std[916], ir165_std[971] = ir165_std[971], ir165_std[916]
graphdata.gsets["ir165std"] = isoir165 = (94, 2, tuple(ir165_std))

# GB/T 12345 (Traditional Chinese in Mainland China, homologous to GB/T 2312 where possible, with
#   the others being added as a couple of rows at the end)
# Unlike GB2312.TXT, redistribution of GB12345.TXT itself is apparently not permitted, although
#   using/incorporating the information is apparently fine.
graphdata.gsets["ir058-hant"] = gb12345 = (94, 2, tuple(tuple(i) if i is not None else None for
    i in json.load(open(os.path.join(parsers.directory, "UTC/GB_12345.json"), "r"))))

# Being as GB 7589, 13131, 7590, 13132 do not include non-Kanji, Unihan mappings theoretically can
#   describe their entire mappings… in reality, the GB 13131 mapping contains more or less the
#   entire set with only a few gaps, whereas the GB 13132 mapping is full of holes.
# kGB3 and kGB5 actually provide the same data as the G3 and G5 in kIRG_GSource (despite the later
#   citing 13131/13132 and the former citing 7589/7590), except for that kGB3 and kGB5 have many
#   more gaps (they seem to only cover the URO).
graphdata.gsets["gb13131"] = gb13131 = (94, 2, 
        parsers.read_unihan_source("UCD/Unihan_IRGSources.txt", "G", "G3"))
graphdata.gsets["gb13132"] = gb13132 = (94, 2, 
        parsers.read_unihan_source("UCD/Unihan_IRGSources.txt", "G", "G5"))

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
resolve = {(0x8b78,): (0x8bea,), (0x8b32,): (0x2c904,), (0x9c44,): (0x2b68b,), (0x9c68,): (0x9cbf,), (0x9766,): (0x4a44,), (0x7060,): (0x30710,), (0x9d82,): (0x2cdfc,)}
tradat = parsers.parse_variants("UCD/Unihan_Variants.txt")
graphdata.gsets["gb7589"] = gb7589 = (94, 2, tuple(resolve.get(i, (tradat.get(i, [[],[]])[1] + [i])[0]) for i in gb13131[2]))
graphdata.gsets["gb7590"] = gb7590 = (94, 2, tuple(resolve.get(i, (tradat.get(i, [[],[]])[1] + [i])[0]) for i in gb13132[2]))
# Some traditional forms remain, but I guess this is good enough. They would presumably be forms
#  where simplified counterparts do not exist in Unicode anyway.

# Apple's version. Note that it changes 0xFD and 0xFE to single-byte codes.
# Includes the vertical form encodings which would make it into GB 18030, plus a few more which
#   didn't. Not all exist as Unicode presentation forms.
# It also includes the GB 6345.1-1986 letters (seeming to have "ɒ" instead of "ɑ" is an editorial
#   error in CHINSIMP.TXT; the listed mapping (as opposed to name) is "ɑ").
if os.path.exists(os.path.join(parsers.directory, "Vendor/CHINSIMP.TXT")):
    macgbdata = parsers.read_main_plane("Vendor/CHINSIMP.TXT", euckrlike = 1, mapper = parsers.ahmap)
    try:
        if os.path.exists(os.path.join(parsers.directory, "Vendor/macGB2312.json")):
            os.unlink(os.path.join(parsers.directory, "Vendor/macGB2312.json"))
        shutil.copy(os.path.join(parsers.cachedirectory, "Vendor---CHINSIMP_mainplane_ahmap.json"),
                    os.path.join(parsers.directory, "Vendor/macGB2312.json"))
    except EnvironmentError:
        pass
else:
    macgbdata = tuple(tuple(i) if i is not None 
        else None for i in json.load(open(os.path.join(parsers.directory, "Vendor/macGB2312.json"), "r")))
graphdata.gsets["ir058-mac"] = gb2312_mac = (94, 2, macgbdata)

# Amounting to the entirety of GBK/3 and most of GBK/4, minus the non-URO end part.
# And, yes, it would indeed be more straightforward to just read the GBK mappings for
# this part from index-gb18030.txt, but I'm trying to make this source code educational on how the
# GBK and UHC pages are laid out.
non_euccn_uro101 = [i for i in range(0x4E00, 0x9FA6) 
                      if i not in graphdata.codepoint_coverages["ir058-2005"]]

# GBK/5, and the non-URO part of GBK/4.
gbk_exceptions = read_gbkexceptions("WHATWG/index-gb18030.txt")
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




