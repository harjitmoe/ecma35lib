#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, shutil
import unicodedata as ucd
from ecma35.data import graphdata
from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import cellemojidata

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
       and i not in (0xFFE0, 0xFFE1, 0xFFE2) # Not affected by which out of EUC and SJIS is used.
])
def map_to_zenkaku(pointer, ucs):
    if len(ucs) == 1 and ucs[0] in _to_zenkaku:
        return (_to_zenkaku[ucs[0]],)
    return ucs

to_1978 = {
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
to_1983 = {'―': '—', '凜': None, '熙': None}
to_1990 = {'―': '—'}
to_2000_from_2004 = {(0xFF5F,): (0x2985,), (0xFF60,): (0x2986,)}

def map_to_2000(pointer, ucs):
    if ucs in to_2000_from_2004:
        return to_2000_from_2004[ucs]
    return map_to_zenkaku(pointer, ucs)

def utcto78jis(pointer, ucs):
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
graphdata.gsets["ir042"] = jisx0208_1978 = (94, 2, 
        parsers.read_main_plane("UTC/JIS0208.TXT", mapper = utcto78jis))
graphdata.gsets["ir042ibm"] = jisx0208_ibm78 = (94, 2,
        parsers.read_main_plane("ICU/ibm-942_P12A-1999.ucm", sjis=True))
graphdata.gsets["ir042nec"] = jisx0208_nec = (94, 2,
        parsers.read_main_plane("Custom/NEC-C-6226-visual.txt"))
# JIS C 6226:1983 / JIS X 0208:1983
graphdata.gsets["ir087"] = jisx0208_1983 = (94, 2, 
        parsers.read_main_plane("UTC/JIS0208.TXT", mapper = utcto83jis))

# JIS X 0212:1990 (i.e. the 1990 supplementary plane)
graphdata.gsets["ir159"] = jisx0212 = (94, 2,
        parsers.read_main_plane("WHATWG/index-jis0212.txt"))
# JIS X 0212 with allocated but not published (per Lunde) va/vi/ve/vo codepoints. Note that these
# codepoints explicitly clash with (either plane of) JIS X 0213.
graphdata.gsets["ir159va"] = jisx0212_extva = (94, 2,
        jisx0212[2][:462] + tuple((_i,) for _i in range(0x30F7, 0x30FB)) + jisx0212[2][466:])
graphdata.gsets["ir159ibm"] = jisx0212ibm = (94, 2,
        parsers.read_main_plane("ICU/ibm-954_P101-2007.ucm", eucjp=1, plane=2))

# JIS X 0208:1990 or 1997
graphdata.gsets["ir168"] = jisx0208_1990 = (94, 2, 
        parsers.read_main_plane("UTC/JIS0208.TXT", mapper = utcto90jis))
graphdata.gsets["ir168utc"] = jisx0208_utc = (94, 2, parsers.read_main_plane("UTC/JIS0208.TXT"))
graphdata.gsets["ir168ibm"] = jisx0208_ibm90 = (94, 2,
        parsers.read_main_plane("ICU/ibm-954_P101-2007.ucm", eucjp=1, plane=1))
# JIS X 0208, Microsoft and WHATWG version, as specified for use in HTML5
graphdata.gsets["ir168web"] = jisx0208_html5 = (94, 2,
        parsers.read_main_plane("WHATWG/index-jis0208.txt"))

# Apple's three versions (KanjiTalk 7, PostScript, KanjiTalk 6)
if os.path.exists(os.path.join(parsers.directory, "Vendor/JAPANESE.TXT")):
    kanjitalk7data = parsers.read_main_plane("Vendor/JAPANESE.TXT", sjis=1, mapper = parsers.ahmap)
    try:
        if os.path.exists(os.path.join(parsers.directory, "Vendor/macJIS.json")):
            os.unlink(os.path.join(parsers.directory, "Vendor/macJIS.json"))
        shutil.copy(os.path.join(parsers.cachedirectory, "Vendor---JAPANESE_mainplane_ahmap.json"),
                    os.path.join(parsers.directory, "Vendor/macJIS.json"))
    except EnvironmentError:
        pass
else:
    kanjitalk7data = tuple(parsers.ahmap(0, tuple(i)) if i is not None 
        else None for i in json.load(open(os.path.join(parsers.directory, "Vendor/macJIS.json"), "r")))
graphdata.gsets["ir168mac"] = jisx0208_applekt7 = (94, 2, kanjitalk7data)
graphdata.gsets["ir168macps"] = jisx0208_appleps = (94, 2,
        parsers.read_main_plane("Custom/JAPAN_PS.TXT", sjis=1, plane=1, mapper = parsers.ahmap))
kanjitalk6 = (jisx0208_applekt7[2][:8 * 94] + ((None,) * 188) + # Normal non-Kanji rows
              jisx0208_applekt7[2][84 * 94 : 86 * 94] +         # Vertical forms
              jisx0208_appleps[2][12 * 94 : 13 * 94] +          # NEC Row Thirteen
              jisx0208_applekt7[2][87 * 94 : 89 * 94] +         # Vertical forms
              jisx0208_applekt7[2][15 * 94 : 84 * 94] + ((None,) * 940))
graphdata.gsets["ir168mackt6"] = jisx0208_applekt6 = (94, 2, kanjitalk6)

# Emoji
graphdata.gsets["ir168arib"] = jisx0208_arib = (94, 2, 
        parsers.fuse([parsers.read_main_plane("Custom/pict_arib.txt", sjis=1), jisx0208_1990[2]],
                     "Emoji--ARIB.json"))
graphdata.gsets["ir168docomo"] = jisx0208_arib = (94, 2, 
        parsers.fuse([cellemojidata.outmap["docomo"][:94*94], jisx0208_html5[2][:-840]],
                     "Emoji--DoCoMo-4.json"))
graphdata.gsets["ir168kddipict"] = jisx0208_arib = (94, 2, 
        parsers.fuse([cellemojidata.outmap["kddi"][:94*94],
                      parsers.read_main_plane("ICU/kddi-sjis.ucm", sjis=1, plane=1)[:-840]],
                     "Emoji--KDDI-5-pictzodiac.json"))
graphdata.gsets["ir168kddisym"] = jisx0208_arib = (94, 2, 
        parsers.fuse([cellemojidata.outmap["kddi_symboliczodiac"][:94*94],
                      parsers.read_main_plane("ICU/kddi-sjis.ucm", sjis=1, plane=1)[:-840]],
                     "Emoji--KDDI-5-symzodiac.json"))
graphdata.gsets["ir168sbank"] = jisx0208_arib = (94, 2, 
        parsers.fuse([cellemojidata.outmap["softbank"][:94*94], jisx0208_html5[2][:-840]],
                     "Emoji--Softbank-4.json"))
graphdata.gsets["ibmsjisext"] = sjis_html5_g3 = (94, 2, 
        parsers.read_main_plane("WHATWG/index-jis0208.txt", sjis=1, plane=2))
whatwgsjispuaonly = []
for u, i in enumerate(range(0xE000, 0xE758)):
    # Yes, the WHATWG does this, albeit only in the SJIS codec, and then only in the decoder.
    a, b = (u // 188), (u % 188)
    a += 0xF0
    b += 0x40
    if b >= 0x7F:
        b += 1
    men, ku, ten = parsers._grok_sjis(bytes([a, b]))
    pointer = ((ku - 1) * 94) + (ten - 1)
    if len(whatwgsjispuaonly) > pointer:
        assert whatwgsjispuaonly[pointer] is None
        whatwgsjispuaonly[pointer] = (i,)
    else:
        if len(whatwgsjispuaonly) < pointer:
            whatwgsjispuaonly.extend([None] * (pointer - len(whatwgsjispuaonly)))
        whatwgsjispuaonly.append((i,))
graphdata.gsets["ibmsjisextpua"] = sjis_html5_g3_pua = (94, 2, 
        parsers.fuse([whatwgsjispuaonly, sjis_html5_g3[2]], "ibmextwithpua.json"))
graphdata.gsets["docomosjisext"] = docomo_g3 = (94, 2, cellemojidata.outmap["docomo"][94*94:])
graphdata.gsets["kddisymsjisext"] = docomo_g3 = (94, 2, cellemojidata.outmap["kddi_symboliczodiac"][94*94:])
graphdata.gsets["kddipictsjisext"] = docomo_g3 = (94, 2, cellemojidata.outmap["kddi"][94*94:])
graphdata.gsets["sbanksjisext"] = sbank_g3 = (94, 2, cellemojidata.outmap["softbank"][94*94:])
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
graphdata.gsets["ir233"] = jisx0213_plane1 = (94, 2,
        parsers.read_main_plane("Other/euc-jis-2004-std.txt", eucjp = True, plane = 1,
            mapper = map_to_zenkaku))
graphdata.gsets["ir228"] = jisx0213_oldplane1 = (94, 2,
        parsers.read_main_plane("Other/euc-jis-2004-std.txt", eucjp = True, plane = 1,
            skipstring = "[2004]", mapper = map_to_2000))
graphdata.gsets["ir229"] = jisx0213_plane2 = (94, 2, # Code unchanged from original edition.
        parsers.read_main_plane("Other/euc-jis-2004-std.txt", eucjp = True, plane = 2,
            mapper = map_to_zenkaku))

# The Open Group Japan's (OSF Japan's) definitions of EUC-JP
osfeuc_0208j = parsers.read_main_plane("OSF/eucJP-0208.txt", eucjp = True, plane = 1)
osfeuc_0208a = parsers.read_main_plane("OSF/eucJP-0208A.txt", eucjp = True, plane = 1)
osfeuc_0208m = parsers.read_main_plane("OSF/eucJP-0208M.txt", eucjp = True, plane = 1)
osfeuc_nec = parsers.read_main_plane("OSF/eucJP-13th.txt", eucjp = True, plane = 1)
osfeuc_0212j = parsers.read_main_plane("OSF/eucJP-0212.txt", eucjp = True, plane = 2)
osfeuc_0212a = parsers.read_main_plane("OSF/eucJP-0212A.txt", eucjp = True, plane = 2)
osfeuc_0212m = parsers.read_main_plane("OSF/eucJP-0212M.txt", eucjp = True, plane = 2)
# Oddly different and even mutually collisive with the IBM JIS X 0212 extensions (per ICU).
# Repertoire matches the IBM JIS X 0212 extensions though.
osfeuc_ibm = parsers.read_main_plane("OSF/eucJP-ibmext.txt", eucjp = True, plane = 2)
osfeuc_puaone = parsers.read_main_plane("OSF/eucJP-udc.txt", eucjp = True, plane = 1)
osfeuc_puatwo = parsers.read_main_plane("OSF/eucJP-udc.txt", eucjp = True, plane = 2)
#
graphdata.gsets["ir168osf"]  = osf_0208_j = (94, 2, parsers.fuse([
    osfeuc_0208j, osfeuc_nec, osfeuc_puaone], "OSF--eucJP-0208j-complete.json"))
graphdata.gsets["ir168osfa"] = osf_0208_a = (94, 2, parsers.fuse([
    osfeuc_0208a, osfeuc_nec, osfeuc_puaone], "OSF--eucJP-0208a-complete.json"))
graphdata.gsets["ir168osfm"] = osf_0208_m = (94, 2, parsers.fuse([
    osfeuc_0208m, osfeuc_nec, osfeuc_puaone], "OSF--eucJP-0208m-complete.json"))
graphdata.gsets["ir159osf"]  = osf_0212_j = (94, 2, parsers.fuse([
    osfeuc_0212j, osfeuc_ibm, osfeuc_puatwo], "OSF--eucJP-0212j-complete.json"))
graphdata.gsets["ir159osfa"] = osf_0212_a = (94, 2, parsers.fuse([
    osfeuc_0212a, osfeuc_ibm, osfeuc_puatwo], "OSF--eucJP-0212a-complete.json"))
graphdata.gsets["ir159osfm"] = osf_0212_m = (94, 2, parsers.fuse([
    osfeuc_0212m, osfeuc_ibm, osfeuc_puatwo], "OSF--eucJP-0212m-complete.json"))


