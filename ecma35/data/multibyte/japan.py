#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2022/2023/2024/2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, shutil
from ecma35.data import graphdata, variationhints
from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import cellemojidata
from ecma35.data.names import namedata

# Use of Zenkaku vs. Hankaku codepoints differs between the x0213.org mappings for EUC vs. SJIS.
# If we don't know what SBCS it's being used with, best to just use Zenkaku consistently…
def _flatten(u):
    if u == "\uffe3":
        # U+203E is usually considered the normal equivalent, at least in CJK contexts, although
        # the formal name seems to suggest U+00AF (informal annotations identify U+203E as
        # another). In either case, the NFKC is actually U+0020+0304, which isn't suitable here.
        return "\u203e"
    decomp = namedata.compat_decomp.get(u, (None, u))
    if decomp[0] == "wide":
        return decomp[1]
    return u
_to_zenkaku = dict([
    (ord(_flatten(chr(i))), i)
    for i in range(0xFF00, 0xFFF0) 
    if i not in (0xFFE0, 0xFFE1, 0xFFE2) # Not affected by which out of EUC and SJIS is used.
])
def map_to_zenkaku(pointer, ucs):
    if len(ucs) == 1 and ucs[0] in _to_zenkaku:
        return (_to_zenkaku[ucs[0]],)
    return ucs

to_1978_1990pivot = {
    '―': '—',
    #
    '∈': None, '∋': None, '⊆': None, '⊇': None, '⊂': None, '⊃': None, '∪': None, '∩': None, 
    '∧': None, '∨': None, '¬': None, '⇒': None, '⇔': None, '∀': None, '∃': None, '∠': None, 
    '⊥': None, '⌒': None, '∂': None, '∇': None, '≡': None, '≒': None, '≪': None, '≫': None, 
    '√': None, '∽': None, '∝': None, '∵': None, '∫': None, '∬': None, 'Å': None, '‰': None, 
    '♯': None, '♭': None, '♪': None, '†': None, '‡': None, '¶': None, '◯': None, 
    #
    '─': None, '│': None, '┌': None, '┐': None, '┘': None, '└': None, '├': None, '┬': None, 
    '┤': None, '┴': None, '┼': None, '━': None, '┃': None, '┏': None, '┓': None, '┛': None, 
    '┗': None, '┣': None, '┳': None, '┫': None, '┻': None, '╋': None, '┠': None, '┯': None, 
    '┨': None, '┷': None, '┿': None, '┝': None, '┰': None, '┥': None, '┸': None, '╂': None, 
    #
    '唖': '啞', '鯵': '鰺', '焔': '焰', '鴬': '鶯', '鴎': '鷗', '蛎': '蠣', '撹': '攪', '竃': '竈', 
    '噛': '嚙', '潅': '灌', '諌': '諫', '侠': '俠', '尭': '堯', '躯': '軀', '繋': '繫', '頚': '頸', 
    '鹸': '鹼', '砿': '礦', '麹': '麴', '屡': '屢', '蕊': '蘂', '繍': '繡', '蒋': '蔣', '醤': '醬', 
    '靭': '靱', '賎': '賤', '掻': '搔', '痩': '瘦', '掴': '摑', '壷': '壺', '填': '塡', '顛': '顚', 
    '砺': '礪', '梼': '檮', '涛': '濤', '祷': '禱', '涜': '瀆', '迩': '邇', '嚢': '囊', '蝿': '蠅', 
    '溌': '潑', '醗': '醱', '桧': '檜', '頬': '頰', '槙': '槇', '侭': '儘', '麺': '麵', '薮': '藪', 
    '遥': '遙', '莱': '萊', '篭': '籠', '蝋': '蠟', '儘': '侭', '壺': '壷', '攪': '撹', '攅': '攢', 
    '檜': '桧', '檮': '梼', '濤': '涛', '灌': '潅', '瑶': '瑤', '礦': '砿', '礪': '砺', '竈': '竃', 
    '籠': '篭', '蘂': '蕊', '藪': '薮', '蠣': '蛎', '蠅': '蝿', '諫': '諌', '賤': '賎', '邇': '迩', 
    '靱': '靭', '頸': '頚', '鰺': '鯵', '鶯': '鴬', 
    #
    '堯': None, '槇': None, '遙': None, '瑤': None, '凜': None, '熙': None, 
}
to_1978 = to_1978_1990pivot.copy()
to_1978.update({
    '澗': '㵎',
    '昂': '昻',
    '柵': '栅',
    '蝉': '蟬',
    '騨': '驒',
    '箪': '簞',
    '剥': '剝',
    '寃': '𡨚',
    '屏': '屛',
})
to_1983 = {'―': '—', '凜': None, '熙': None}
to_1990 = {'―': '—'}
to_2000_from_2004 = {(0xFF5F,): (0x2985,), (0xFF60,): (0x2986,)}

def map_to_2000(pointer, ucs):
    if ucs in to_2000_from_2004:
        return to_2000_from_2004[ucs]
    return map_to_zenkaku(pointer, ucs)

def utcto78jis(pointer, ucs):
    sucs = "".join(chr(i) for i in ucs)
    if sucs in to_1978_1990pivot:
        ret = to_1978_1990pivot[sucs]
        return tuple(ord(i) for i in ret) if ret else ret
    return ucs
def utcto78jisstricter(pointer, ucs):
    sucs = "".join(chr(i) for i in ucs)
    if sucs in to_1978:
        ret = to_1978[sucs]
        return tuple(ord(i) for i in ret) if ret else ret
    return ucs
def utcto83jis(pointer, ucs):
    sucs = "".join(chr(i) for i in ucs)
    if sucs in to_1983:
        ret = to_1983[sucs]
        return tuple(ord(i) for i in ret) if ret else ret
    return ucs
def utcto90jis(pointer, ucs):
    sucs = "".join(chr(i) for i in ucs)
    if sucs in to_1990:
        ret = to_1990[sucs]
        return tuple(ord(i) for i in ret) if ret else ret
    return ucs

# JIS C 6226:1978 / JIS X 0208:1978
graphdata.gsets["ir042/1990pivot"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/JIS0208.TXT"),
    "JIS0208.TXT",
    mapper = utcto78jis))
graphdata.gsets["ir042"] = jisx0208_1978_stricter = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/JIS0208.TXT"),
    "JIS0208.TXT",
    mapper = utcto78jisstricter))
graphdata.gsets["ir042/ibm"] = (94, 2, parsers.decode_main_plane_sjis(
    parsers.parse_file_format("ICU/ibm-942_P12A-1999.ucm"),
    "ibm-942_P12A-1999.ucm",
    plane = 1))
graphdata.gsets["ir042/nec"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/NEC-C-6226-visual3.txt"),
    "NEC-C-6226-visual3.txt"))
graphdata.gsets["ir042/adobe"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Adobe/AdobeJapan.txt", cidmap=("78", "UniJIS-UTF32")),
    "AdobeJapan.txt-78-UniJIS-UTF32"))
# JIS C 6226:1983 / JIS X 0208:1983
graphdata.gsets["ir087"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/JIS0208.TXT"),
    "JIS0208.TXT",
    mapper = utcto83jis))
graphdata.gsets["ir087/fujitsu"] = (94, 2, parsers.fuse([
    parsers.without_ideocompat(
        parsers.decode_main_plane_gl(
            parsers.parse_file_format("Adobe/AdobeJapan.txt", cidmap=("Add", "UniJIS-UTF32")),
            "AdobeJapan.txt-Add-UniJIS-UTF32"),
        "JIS-FujitsuCIDIdeoNorm.json",
    ),
    jisx0208_1978_stricter[2],
], "JIS-Fujitsu3.json"))

# JIS X 0212:1990 (i.e. the 1990 supplementary plane)
graphdata.gsets["ir159"] = jisx0212 = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("WHATWG/index-jis0212.txt"),
    "index-jis0212.txt"))
# JIS X 0212 with allocated but not published (per Lunde) va/vi/ve/vo codepoints. Note that these
# codepoints explicitly clash with (either plane of) JIS X 0213.
graphdata.gsets["ir159/va"] = (94, 2, parsers.fuse([
        ((None,) * 462) + tuple((_i,) for _i in range(0x30F7, 0x30FB)), 
        jisx0212[2]], "JISX0212-VaExt.json"))
graphdata.gsets["ir159/ibm"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/ibm-954_P101-2007.ucm"),
    "ibm-954_P101-2007.ucm",
    eucjp = 1,
    plane = 2))
graphdata.gsets["ir159/icueuc"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/euc-jp-2007.ucm"),
    "euc-jp-2007.ucm",
    eucjp = 1,
    plane = 2))
def irgn2722proposal(pointer, ucs):
    # https://www.unicode.org/irg/docs/n2722-JSourceIssues.pdf
    if pointer == 4661 and ucs == (0x7BF9,):
        return (0x25CBB,)
    return ucs
graphdata.gsets["ir159/irgn2722"] = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("WHATWG/index-jis0212.txt"),
    "index-jis0212.txt",
    mapper = irgn2722proposal))

# JIS X 0208:1990 or 1997
graphdata.gsets["ir168"] = jisx0208_1990 = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/JIS0208.TXT"),
    "JIS0208.TXT",
    mapper = utcto90jis))
graphdata.gsets["ir168/utc"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/JIS0208.TXT"),
    "JIS0208.TXT"))
graphdata.gsets["ir168/ibm"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/ibm-954_P101-2007.ucm"),
    "ibm-954_P101-2007.ucm",
    eucjp = 1,
    plane = 1))
#graphdata.gsets["ir168/icueuc"] = (94, 2, # Same as web, basically
#        parsers.read_main_plane("ICU/euc-jp-2007.ucm", eucjp=1, plane=1))
# JIS X 0208, Microsoft and WHATWG version, as specified for use in HTML5
graphdata.gsets["ir168/web"] = jisx0208_html5 = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("WHATWG/index-jis0208.txt"),
    "index-jis0208.txt",
    plane = 1))

# Apple's three versions (KanjiTalk 7, PostScript, KanjiTalk 6)
kanjitalk7data = parsers.read_untracked(
    "Mac/macJIS.json",
    "Mac/JAPANESE.TXT",
    parsers.decode_main_plane_sjis,
    parsers.parse_file_format("Mac/JAPANESE.TXT"),
    "JAPANESE.TXT",
    mapper = variationhints.ahmap)
rawmac = parsers.read_untracked(
    "Mac/macJIS-raw.json",
    "Mac/JAPANESE.TXT",
    parsers.decode_main_plane_sjis,
    parsers.parse_file_format("Mac/JAPANESE.TXT"),
    "JAPANESE.TXT-noahmap")
graphdata.gsets["ir168/mac"] = jisx0208_applekt7 = (94, 2, kanjitalk7data)
graphdata.gsets["ir168/mac-raw"] = (94, 2, rawmac)
graphdata.gsets["ir168/macps"] = jisx0208_appleps = (94, 2, parsers.decode_main_plane_sjis(
    parsers.parse_file_format("Custom/JAPAN_PS.TXT"),
    "JAPAN_PS.TXT",
    plane = 1,
    mapper = variationhints.ahmap))
graphdata.gsets["ir168/macps-raw"] = (94, 2, parsers.decode_main_plane_sjis(
    parsers.parse_file_format("Custom/JAPAN_PS.TXT"),
    "JAPAN_PS.TXT-noahmap",
    plane = 1))
_kt6fn = os.path.join(parsers.cachedirectory, "Mac-KanjiTalk6.json")
if not os.path.exists(_kt6fn):
    kanjitalk6 = (jisx0208_applekt7[2][:8 * 94] + ((None,) * 188) + # Normal non-Kanji rows
                  jisx0208_applekt7[2][84 * 94 : 86 * 94] +         # Vertical forms
                  jisx0208_appleps[2][12 * 94 : 13 * 94] +          # NEC Row Thirteen
                  jisx0208_applekt7[2][87 * 94 : 89 * 94] +         # Vertical forms
                  jisx0208_applekt7[2][15 * 94 : 84 * 94] + ((None,) * 940))
    f = open(_kt6fn, "w")
    f.write(json.dumps(kanjitalk6))
    f.close()
else:
    kanjitalk6 = parsers.LazyJSON(os.path.basename(_kt6fn))
graphdata.gsets["ir168/mackt6"] = (94, 2, kanjitalk6)

# Emoji
_windows_noNECSel = parsers.fuse([
    ((None,) * 7996) + (((-1,),) * 840),
    jisx0208_html5[2]], "WinJIS_noNECSel.json")
_windows_noNECSel_au = parsers.fuse([
    ((None,) * 7996) + (((-1,),) * 840),
    parsers.decode_main_plane_sjis(
        parsers.parse_file_format("ICU/kddi-sjis.ucm"),
        "kddi-sjis.ucm",
        plane = 1)
], "WinJIS_noNECSel_au.json")
arib_extonly = parsers.decode_main_plane_sjis(
    parsers.parse_file_format("Custom/pict_arib.txt"),
    "pict_arib.txt")
graphdata.gsets["ir168/arib"] = (94, 2, parsers.fuse([
        arib_extonly,
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-17.txt", "kIRG_JSource", "JARIB"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-16.txt", "kIRG_JSource", "JARIB"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-15-1.txt", "kIRG_JSource", "JARIB"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-15.txt", "kIRG_JSource", "JARIB"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-14.txt", "kIRG_JSource", "JARIB"),
        parsers.read_unihan_planes("UCD/Unihan_IRGSources-13.txt", "kIRG_JSource", "JARIB"),
        parsers.decode_main_plane_gl(
            parsers.parse_file_format("Custom/kanji_arib.txt"),
            "kanji_arib.txt"),
        jisx0208_1990[2],
    ], "JISX0208--ARIB.json"))
graphdata.gsets["ir168/docomo"] = (94, 2, 
        parsers.fuse([cellemojidata.outmap["docomo"][:94*94], _windows_noNECSel],
                     "Emoji--DoCoMo-4.json"))
graphdata.gsets["ir168/kddipict"] = (94, 2, 
        parsers.fuse([cellemojidata.outmap["kddi"][:94*94],
                      _windows_noNECSel_au],
                     "Emoji--KDDI-5-pictzodiac.json"))
graphdata.gsets["ir168/kddisym"] = (94, 2, 
        parsers.fuse([cellemojidata.outmap["kddi_symboliczodiac"][:94*94],
                      _windows_noNECSel_au],
                     "Emoji--KDDI-5-symzodiac.json"))
graphdata.gsets["ir168/sbank"] = (94, 2, 
        parsers.fuse([cellemojidata.outmap["softbank"][:94*94], _windows_noNECSel],
                     "Emoji--Softbank-4.json"))
graphdata.gsets["sjisext/ibm"] = sjis_html5_g3 = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("WHATWG/index-jis0208.txt"),
    "index-jis0208.txt",
    plane = 2))
graphdata.gsets["sjisext/ibm/old"] = (94, 2, parsers.decode_main_plane_sjis(
    parsers.parse_file_format("ICU/ibm-942_P12A-1999.ucm"),
    "ibm-942_P12A-1999.ucm",
    plane = 2))
whatwgsjispuaonly = []
for u, i in enumerate(range(0xE000, 0xE758)):
    # Yes, the WHATWG does this, albeit only in the SJIS codec, and then only in the decoder.
    a, b = (u // 188), (u % 188)
    a += 0xF0
    b += 0x40
    if b >= 0x7F:
        b += 1
    men, ku, ten = parsers._parse_sjis(bytes([a, b]))
    pointer = ((ku - 1) * 94) + (ten - 1)
    if len(whatwgsjispuaonly) > pointer:
        assert whatwgsjispuaonly[pointer] is None
        whatwgsjispuaonly[pointer] = (i,)
    else:
        if len(whatwgsjispuaonly) < pointer:
            whatwgsjispuaonly.extend([None] * (pointer - len(whatwgsjispuaonly)))
        whatwgsjispuaonly.append((i,))
graphdata.gsets["sjisext/ibm/pua"] = (94, 2, 
        parsers.fuse([whatwgsjispuaonly, sjis_html5_g3[2]], "ibmextwithpua.json"))
graphdata.gsets["sjisext/docomo"] = (94, 2, cellemojidata.outmap["docomo"][94*94:])
graphdata.gsets["sjisext/kddi/sym"] = (94, 2, cellemojidata.outmap["kddi_symboliczodiac"][94*94:])
graphdata.gsets["sjisext/kddi/pict"] = (94, 2, cellemojidata.outmap["kddi"][94*94:])
graphdata.gsets["sjisext/sbank"] = (94, 2, cellemojidata.outmap["softbank"][94*94:])
graphdata.gsets["sbank2gpageG"] = (94, 1, tuple(cellemojidata.softbank_pages[0]))
graphdata.gsets["sbank2gpageE"] = (94, 1, tuple(cellemojidata.softbank_pages[1]))
graphdata.gsets["sbank2gpageF"] = (94, 1, tuple(cellemojidata.softbank_pages[2]))
graphdata.gsets["sbank2gpageO"] = (94, 1, tuple(cellemojidata.softbank_pages[3]))
graphdata.gsets["sbank2gpageP"] = (94, 1, tuple(cellemojidata.softbank_pages[4]))
graphdata.gsets["sbank2gpageQ"] = (94, 1, tuple(cellemojidata.softbank_pages[5]))

# JIS X 2013:2000 and :2004
# Note: Python's *jisx0213 (i.e. JIS X 0213:2000) codecs map 02-93-27 to U+9B1D, rather than U+9B1C
#   as done by its *jis-2004 codecs and also by the Project X0213 mappings.
# Since only plane 1 got a new ISO 2022 registration in 2004, one would expect plane 2 to stay the
#   same. Moreover, the glyph in the ISO-IR-229 registration itself (despite being barely legible) 
#   is clearly already U+9B1C, not U+9B1D.
graphdata.gsets["ir233"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("Other/euc-jis-2004-std.txt"),
    "euc-jis-2004-std.txt",
    eucjp = True,
    plane = 1,
    mapper = map_to_zenkaku))
graphdata.gsets["ir228"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("Other/euc-jis-2004-std.txt", skipstring = "[2004]"),
    "euc-jis-2004-std.txt",
    eucjp = True,
    plane = 1,
    mapper = map_to_2000))
graphdata.gsets["ir229"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("Other/euc-jis-2004-std.txt"),
    "euc-jis-2004-std.txt",
    eucjp = True,
    plane = 2,
    mapper = map_to_zenkaku))

# The Open Group Japan's (OSF Japan's) definitions of EUC-JP
osfeuc_0208j = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-0208.txt"), 
    "eucJP-0208.txt", 
    eucjp = True, 
    plane = 1)
osfeuc_0208a = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-0208A.txt"), 
    "eucJP-0208A.txt", 
    eucjp = True, 
    plane = 1)
osfeuc_0208m = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-0208M.txt"), 
    "eucJP-0208M.txt", 
    eucjp = True, 
    plane = 1)
osfeuc_nec = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-13th.txt"), 
    "eucJP-13th.txt", 
    eucjp = True, 
    plane = 1)
osfeuc_0212j = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-0212.txt"), 
    "eucJP-0212.txt", 
    eucjp = True, 
    plane = 2)
osfeuc_0212a = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-0212A.txt"), 
    "eucJP-0212A.txt", 
    eucjp = True, 
    plane = 2)
osfeuc_0212m = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-0212M.txt"), 
    "eucJP-0212M.txt", 
    eucjp = True, 
    plane = 2)
# Oddly different and even mutually collisive with the IBM JIS X 0212 extensions (per ICU).
# Repertoire matches the IBM JIS X 0212 extensions though.
osfeuc_ibm = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-ibmext.txt"), 
    "eucJP-ibmext.txt", 
    eucjp = True, 
    plane = 2)
osfeuc_puaone = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-udc.txt"), 
    "eucJP-udc.txt", 
    eucjp = True, 
    plane = 1)
osfeuc_puatwo = parsers.decode_main_plane_euc(
    parsers.parse_file_format("OSF/eucJP-udc.txt"), 
    "eucJP-udc.txt", 
    eucjp = True, 
    plane = 2)
#
graphdata.gsets["ir168/osf"]  = (94, 2, parsers.fuse([
    osfeuc_0208j, osfeuc_nec, osfeuc_puaone], "OSF--eucJP-0208j-complete.json"))
graphdata.gsets["ir168/osfa"] = (94, 2, parsers.fuse([
    osfeuc_0208a, osfeuc_nec, osfeuc_puaone], "OSF--eucJP-0208a-complete.json"))
graphdata.gsets["ir168/osfm"] = (94, 2, parsers.fuse([
    osfeuc_0208m, osfeuc_nec, osfeuc_puaone], "OSF--eucJP-0208m-complete.json"))
graphdata.gsets["ir159/osf"]  = (94, 2, parsers.fuse([
    osfeuc_0212j, osfeuc_ibm, osfeuc_puatwo], "OSF--eucJP-0212j-complete.json"))
graphdata.gsets["ir159/osfa"] = (94, 2, parsers.fuse([
    osfeuc_0212a, osfeuc_ibm, osfeuc_puatwo], "OSF--eucJP-0212a-complete.json"))
graphdata.gsets["ir159/osfm"] = (94, 2, parsers.fuse([
    osfeuc_0212m, osfeuc_ibm, osfeuc_puatwo], "OSF--eucJP-0212m-complete.json"))

graphdata.gsets["japan-plane-3"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/jasource.txt"),
    "jasource.txt"))

graphdata.gsets["japan-plane-4"] = (94, 2, parsers.decode_main_plane_gl(parsers.parse_file_format("Other/plane_IB.txt"), "plane_IB.txt"))
graphdata.gsets["japan-plane-5"] = (94, 2, parsers.decode_main_plane_gl(parsers.parse_file_format("Other/plane_FT.txt"), "plane_FT.txt"))
graphdata.gsets["japan-plane-6"] = (94, 2, parsers.decode_main_plane_gl(parsers.parse_file_format("Other/plane_HG.txt"), "plane_HG.txt"))

graphdata.chcpdocs["20932"] = "modified-euc"
graphdata.defgsets["20932"] = ("ir006", "ir168/web", "nil", "nil", "ir159")

graphdata.gsets["ibmjapan/1992"] = (190, 2, parsers.decode_main_plane_dbebcdic(parsers.parse_file_format("ICU/ibm-930_P120-1999.ucm"), "ibm-930_P120-1999.ucm"))
graphdata.ebcdicdbcs["300"] = graphdata.ebcdicdbcs["930"] = graphdata.ebcdicdbcs["931"] = graphdata.ebcdicdbcs["939"] = graphdata.ebcdicdbcs["9122"] = "ibmjapan/1992"
graphdata.chcpdocs["300"] = graphdata.chcpdocs["930"] = graphdata.chcpdocs["931"] = graphdata.chcpdocs["939"] = graphdata.chcpdocs["9122"] = "ebcdic"
graphdata.defgsets["930"] = ("gl290", "gr290", "gl310", "gr310")
graphdata.defgsets["931"] = ("alt646/ibmusa", "nil", "gl310", "gr310")
graphdata.defgsets["939"] = ("alt646/ibmjapan/noyen", "gr1027", "gl310", "gr310")
graphdata.defgsets["9122"] = ("gl887", "gr4386", "gl310", "gr310")

graphdata.gsets["ibmjapan/2002"] = (190, 2, parsers.decode_main_plane_dbebcdic(parsers.parse_file_format("ICU/ibm-16684_P110-2003.ucm"), "ibm-16684_P110-2003.ucm"))
graphdata.ebcdicdbcs["1390"] = graphdata.ebcdicdbcs["1399"] = graphdata.ebcdicdbcs["9582"] = graphdata.ebcdicdbcs["9591"] = graphdata.ebcdicdbcs["16684"] = graphdata.ebcdicdbcs["24876"] = "ibmjapan/2002"
graphdata.chcpdocs["1390"] = graphdata.chcpdocs["1399"] = graphdata.chcpdocs["9582"] = graphdata.chcpdocs["9591"] = graphdata.chcpdocs["16684"] = graphdata.chcpdocs["24876"] = "ebcdic"
graphdata.defgsets["1390"] = graphdata.defgsets["9582"] = ("gl290", "gr8482", "gl310", "gr310")
graphdata.defgsets["1399"] = graphdata.defgsets["9591"] = ("alt646/ibmjapan/noyen", "gr5123", "gl310", "gr310")


