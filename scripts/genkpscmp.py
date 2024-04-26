#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import korea, cellemojidata
from ecma35.data import graphdata, showgraph
import json

plane1 = (1, ("1997 KPS", "2003 KPS", "2011 KPS", "Output"), [
          graphdata.gsets["ir202"][2],
          graphdata.gsets["ir202/2003"][2],
          graphdata.gsets["ir202/2011"][2],
          graphdata.gsets["ir202/full"][2],
])

def planefunc(number, mapname=None):
    assert number == 1
    if mapname is None:
        return "KPS 9566"
    else:
        return ""

def kutenfunc(number, row, cell):
    assert number == 1
    euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    fmteuc = "(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
    anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                 number, row, cell, number, row, cell)
    return "{}<br>{}".format(anchorlink, fmteuc)

cdispmap = {}
annots = {
    (1, 1, 32): "This is a vertical presentation form of a full stop, not a diacritic.",
    (1, 1, 35): "These are vertical punctuation marks, not diacritics.&ensp;The newer mappings "
                "take advantage of additional vertical forms added more recently from GB/T 12345 "
                "and, theoretically, GB 18030.",
    (1, 1, 36): "All deployed mappings use U+22EE (⋮); an argument for U+FE19 (︙) could also be "
                "made.&ensp;U+FE19 was added more recently from GB/T 12345 (and, theoretically, "
                "GB 18030); it differs in that U+FE19 NFKCs to U+2026 (…) and is always vertical, "
                "while U+22EE may rotate to remain perpendicular to the line in vertical display.",
    (1, 1, 37): "This is the vertical counterpart of 01-01-13, and corresponds to 0xEB60 "
                "(KanjiTalk 7 or PostScript) or 0x8660 (KanjiTalk 6) in MacJapanese, which gets "
                "mapped to U+301C+F87E by Apple (U+F87E is a PUA hint).&ensp;U+2E2F is a by-name "
                "mapping to a substantially different character (a spacing form of a Cyrillic "
                "diacritic).&ensp;Concavity is the same as U+2E2F in all KP family fonts (in both "
                "2005 and 2012 versions) but reversed in the 1997 code chart.",
    (1, 1, 62): "This appears to be an opening quote for vertical writing, and should be aligned "
                "to the right of the em square.&ensp;BabelStone Han does this.",
    (1, 1, 63): "This appears to be a closing quote for vertical writing, and should be aligned "
                "to the left of the em square in contrast to the right-aligned U+2018; KP fonts "
                "actually use the shape of U+2018, making the Unicode mapping a cludge.&ensp;"
                "BabelStone Han shows both right-aligned, however.",
    (1, 1, 64): "This appears to be an opening quote for vertical writing, and should be aligned "
                "to the right of the em square.&ensp;BabelStone Han does this.",
    (1, 1, 65): "This appears to be a closing quote for vertical writing, and should be aligned "
                "to the left of the em square in contrast to the right-aligned U+201C; KP fonts "
                "actually use the shape of U+201C, making the Unicode mapping a cludge.&ensp;"
                "BabelStone Han shows both right-aligned, however.",
    (1, 2, 81): "This corresponds graphically to 0xA79B in HangulTalk (MacKorean), which Apple "
                "maps as U+25B4+20E4, and semantically to U+26F0, but as a version with an outer "
                "border which is apparently a specific symbol used on DPRK signage.</p><p>Apple's "
                "mappings for HangulTalk include a large number of kludges, a few of which have "
                "since gained closer Unicode characters.&ensp;Nanum Gothic includes several "
                "HangulTalk glyphs which are inaccessible from Unicode.",
    (1, 2, 84): "Stripy upward triangles, for ascent (≡ stripes), slope on left (\\\\\\ "
                "stripes) and slope on right (/// stripes) respectively.",
    (1, 4, 80): "Emphasised forms of the names of North Korea's leaders.&ensp;Prior to Jong-un's "
                "ascent to the position, U+F120, U+F121 and U+F122 were used for ㍹, ㏞ and ㏟ "
                "respectively, though their then-newly added Unicode codepoints were favoured "
                "from 2003 onward.",
    (1, 7, 94): "Horizontal-barred presentation forms of the fractions (it is unlikely that they "
                "appear as such here).",
    (1, 8, 6): "Changed from Kelvin to Euro in 2003.&ensp;The 1997 code charts show a degree sign "
               "in the Kelvin symbol, as do the 2005 KP fonts (except for PusKul, which shows "
               "even the Kelvin codepoint as a Euro sign).&ensp;The Kelvin was re-instated at "
               "non-EUC code 0xE988 in 2011.",
    (1, 12, 2): "The hammer, sickle and brush of the Workers' Party of Korea, supposedly used as "
                "a map symbol.&ensp;Probably not rendered correctly here.",
    (1, 12, 27): "These two characters (⬀ , ⬁) used incorrectly swapped mappings in the 2003 "
                 "edition (and were thus reversed in fonts targetting it, e.g. the 2005 KP "
                 "fonts), but this was corrected in the UTC mappings and the 2011 mappings.",
    (1, 12, 51): "2011 KPS assigns U+261E (☞) the non-EUC code 0xE04D.&ensp;This character, "
                 "by contast, is backhand, i.e. U+1F449 (👉).&ensp;Resorting to changing this "
                 "one to PUA U+F13B might suggest poor astral character support.",
    (1, 12, 53): "Northwest-pointing scissors.",
    (1, 14, 94): "The 2003 edition adds U+00FF (ÿ) as non-EUC code 0xAEFF immediately following.",
    (1, 69, 9): "U+67FF is a persimmon, while the rather less common U+676E refers to "
                "wood shavings.&ensp;Since the characters are in phonetic order by North "
                "Korean collation, it is apparent that the former is intended.&ensp;See "
                "<a href='https://www.unicode.org/L2/L2021/21059-irgn2479-mapping.pdf'>"
                "UTC L2/21-059 (IRG N2479)</a>."
}

blot = ""
if os.path.exists("__analyt__"):
    blot = open("__analyt__").read()

for n, p in enumerate([plane1]):
    for q in range(1, 7):
        bn = n + 1
        f = open("kpsplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "kpsplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "KPS 9566, part {1:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "kpsplane{:X}f.html".format(bn - 1)
            lastname = "KPS 9566, part 6".format(bn - 1)
        if q < 6:
            nexturl = "kpsplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "KPS 9566, part {1:d}".format(bn, q + 1)
        elif bn < 1:
            nexturl = "kpsplane{:X}a.html".format(bn + 1)
            nextname = "KPS 9566, part 1".format(bn + 1)
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KP", part=q, css="../css/codechart.css",
                             menuurl="/kps-conc.html", menuname="KPS character set variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True, blot=blot,
                             pua_collides=True)
        f.close()








