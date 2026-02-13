#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021, 2022, 2023, 2024, 2025, 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import korea, cellemojidata
from ecma35.data import graphdata, showgraph
import json

# №0: GB-2312: Coding of Chinese Ideogram Set for Information Interchange, Basic Set
# №1: GB-12345: Code of Chinese Ideogram Set for Information Interchange, Supplementary Set
# №2: GB-7589: Code of Chinese Ideograms Set for Information Interchange, the 2nd Supplementary Set
# №3: GB-13131: Code of Chinese Ideogram Set for Information Interchange, the 3rd Supplementary Set
# №4: GB-7590: Code of Chinese Ideogram Set for Information Interchange, the 4th Supplementary Set
# №5: GB-13132: Code of Chinese Ideogram Set for Information Interchange, the 5th Supplementary Set
# There appears to be no №6 (unless GB-12052 is it?)
# №7: GB-16500: Code of Chinese Ideograms Set for Information Interchange, the 7th Supplementary Set 
# Unihan uses "G7" for a different source which isn't a CCS, and calls GB-16500 GE, but its title indicates it is in fact №7
# №8: SJ-11239: Chinese Ideograms Coded Character Set for Information Interchange, the 8th Supplementary Set 
# GB-8565.2: Information Processing - Coded Character Sets for Text Communication - Part 2: Graphic Characters (Unihan calls it G8; it is an expansion of GB-2312 though, not a plane in its own right.)
# GB-12052: Korean Coded Character Set for Information Interchange (Unihan's GK)
# GB-15564: Code of Chinese ideogram set for teletext broadcasting--HongKong subset

# ITU T.101-C is 1994 (2nd ed; 1st ed didn't include this one afaict); IR-165 reg is 1992.
MACSET = "Apple"
plane0 = (0, ("GB 2312<br>1980", "GB 2312<br>UTC", "GB 6345.1<br>1986", "GB 8565.2<br>1988", "ITU T.101-C<br>IR-165", "\"GB 8565.2\"<br>Old Unihan", "GB 12052<br>1989", "GB 12345<br>1990", "GB 12345<br>UTC", "IBM-1382", MACSET, "Windows", "GB 18030<br>2000", "GB 18030<br>2005", "GB 18030<br>2022", "GB 18030<br>Full"), [
          graphdata.gsets["ir058"][2],
          graphdata.gsets["ir058/utc"][2],
          graphdata.gsets["gb6345"][2],
          graphdata.gsets["gb8565"][2],
          graphdata.gsets["ir165"][2],
          graphdata.gsets["gb8565-oldwrongunihan"][2],
          graphdata.gsets["gb12052"][2][:94*15] + ((None,) * (94*78)),
          graphdata.gsets["ir058/hant-strict"][2][:94*15] + ((None,) * (94*78)),
          graphdata.gsets["ir058/hant-utc"][2][:94*15] + ((None,) * (94*78)),
          graphdata.gsets["ir058/ibm"][2],
          graphdata.gsets["ir058/mac"][2],
          graphdata.gsets["ir058/ms"][2],
          graphdata.gsets["ir058/2000"][2],
          graphdata.gsets["ir058/2005"][2],
          graphdata.gsets["ir058/2022"][2],
          graphdata.gsets["ir058/full"][2],
])
plane1 = (1, ("GB 12345<br>1990", "GB 12345<br>UTC", "GB 12345<br>Unihan Ext"), [
          graphdata.gsets["ir058/hant-strict"][2],
          graphdata.gsets["ir058/hant-utc"][2],
          graphdata.gsets["ir058/hant-full"][2],
])
plane2 = (2, ("GB 7589<br>like GB3 draft", "GB 7589<br>1987"), [
          graphdata.gsets["gb7589/gb13131-draft-homologue"][2],
          graphdata.gsets["gb7589"][2],
])
plane3 = (3, ("GB 13131<br>IRGN2376", "GB 13131<br>like GB 7589"), [
          graphdata.gsets["gb13131/draft"][2],
          graphdata.gsets["gb13131"][2],
])
plane4 = (4, ("GB 7590<br>like GB5 draft", "GB 7590<br>1987"), [
          graphdata.gsets["gb7590/gb13132-draft-homologue"][2],
          graphdata.gsets["gb7590"][2],
])
plane5 = (5, ("GB 13132<br>IRGN2376", "GB 13132<br>like GB 7590"), [
          graphdata.gsets["gb13132/draft"][2],
          graphdata.gsets["gb13132"][2],
])
plane7 = (7, ("Unihan G7<br>pre-IRGN2808", "Unihan G7<br>IRGN2808", "GB16500"), [
          graphdata.gsets["the-old-other-gb7"][2],
          graphdata.gsets["the-new-other-gb7"][2],
          graphdata.gsets["gb16500"][2],
])
plane8 = (8, ("Subset", "PUA<br>BabelStone"), [
          graphdata.gsets["sj11239"][2],
          graphdata.gsets["sj11239/babelstonehan"][2],
])
KPLANE = 9
planeK = (KPLANE, ("GB12052",), [
          graphdata.gsets["gb12052"][2],
])

titles = [
    "GB 2312",
    "GB 12345",
    "GB 7589",
    "GB 13131",
    "GB 7590",
    "GB 13132",
    "nul points",
    "GB 16500 + Table of Hanzi not in GB 2312",
    "SJ 11239",
    "GB 12052",
]

def planefunc(number, mapname=None):
    if mapname is None:
        return titles[number]
    return ""

def planefunc2(number, mapname=None):
    if mapname is None:
        return "General Purpose Han Characters for Modern Chinese" if number == 7 else "Guobiao 94×94 sets"
    return ""

def planefunc3(number, mapname=None):
    if mapname is None:
        if number == 7:
            return "GB 16500"
        return titles[number]
    return ""

def kutenfunc(number, row, cell):
    if cell >= 0:
        if number == KPLANE:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>K-{:02d}-{:02d}</a>".format(
                         KPLANE, row, cell, row, cell)
        elif number == 0 and row < 16:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}</a>".format(
                         number, row, cell, row, cell)
        else:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                         number, row, cell, number, row, cell)
    else:
        if number == KPLANE:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>K-{:02d}-{}</a>".format(
                         KPLANE, row, -cell, row, 
                         "{:02d}+".format(-cell) if cell != -1 else "*")
        else:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{}</a>".format(
                         number, row, -cell, number, row, 
                         "{:02d}+".format(-cell) if cell != -1 else "*")
    if number == 0:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
        anchorlink += "<br>(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
    return anchorlink

annots = {
    (0, 1, 0): "Rows 1 through 15 (\"part 1\") mostly correspond between Guobiao planes that populate them, and are deliberately left unpopulated by the others.&ensp;Hence they are charted together here.",
    (0, 1, 4): "U+30FB's name KATAKANA MIDDLE DOT and U+00B7's name MIDDLE DOT might have led implementers to map 01-04 to the latter instead in Chinese, rather than Japanese contexts.&ensp;Typographically, however, 01-04 would be rather closer to the Japanese interpunct than the Catalan interpunct.&ensp;Compare JIS 01-01-06.",
    (0, 1, 10): "Compare behaviour of JIS 01-01-29.",
    (0, 1, 11): "Compare, and in particular contrast, the behaviour of JIS 01-01-33.",
    (0, 1, 12): "Compare 01-46 and JIS 01-01-34.&ensp;UTC initially mapped this to U+2225 (duplicating 01-46), but corrected this in their GB 2312 (but not GB 12345) mapping in 1999.",
    (0, 1, 13): "Compare JIS 01-01-36.&ensp;Unlike the JIS character, Apple seem not to have altered this one from the initial mapping to U+22EF.",
    (0, 1, 46): "Compare 01-12, JIS 01-01-34, and JIS 01-02-52.",
    (0, 1, 71): "Compare 03-04.",
    (0, 2, 67): "Microsoft encodes the euro sign as a single byte code (0x80) instead.",
    (0, 3, 4): "Compare 01-71.",
    (0, 3, 13): "Compare both JIS 01-01-61 and JIS 01-02-17.",
    (0, 3, 71): "Compare 08-32.&ensp;Mapping to U+FF47 is usual regardless of reference glyph (except for the old ICU mapping for the IR-165 set), but this has been avoided here for the sake of illustration.&ensp;Lunde (2009) lists the change in GB 6345.1 as from open to looped (i.e. <em>away</em> from U+0261), but he appears to have gotten this backward (<a href='https://www.itscj-ipsj.jp/ir/058.pdf'>in GB 2312</a>, <a href='https://i.imgur.com/3L2CMyr.png'>in GB 6345.1</a>).",
    (0, 3, 94): "Compare JIS 01-01-17.",
    (0, 6, 56): "Some explanation is in order for the following characters.&ensp;The Unicode Vertical Forms block (containing the vertical forms from GB 18030) apparently postdates GB 18030, hence the Apple mappings using PUA hints and the GB18030 and Windows mappings to the Private Use Area.&ensp;This doesn't affect the vertical presentation forms with correspondances to Big5, which were already included in the CJK Compatibility Forms block.",
    (0, 6, 59): "ITU T.101-C instead includes pattern characters in the following range; they are largely unmappable.&ensp;<em>Extremely</em> approximate mappings that I essentially made up (although not without justifications) are used below so that the collision with the vertical forms is visible.",
    (0, 8, 32): "Compare 03-71.&ensp;Mapping to U+0261 is usual regardless of reference glyph (except for the old ICU mapping for the IR-165 set), but this has been avoided here for the sake of illustration.",
    (0, 90, 30): "This character is mapped to Unicode as U+4FB4 (侴; compare 04-17-31) in the ICU mapping data, although its reference glyph (which matches 02-18-93 in all charts although, confusingly, 03-18-93 is used as U+4FB4's Unihan source) does not entirely match U+4FB4's reference glyph (although it is a minor variant).&ensp; However, it <a href=\"https://hc.jsecs.org/irg/ws2024/app/?id=00266\">may be disunified as a CJK Extension K character in a future Unicode version</a>.&ensp; In any case, this is the unregistered BabelStone IVS U+4FB4+E0101.",
    (1, 93, 0): "The extension in this row had the purpose of adding the repertoire of rows 71 and 72 of GB 12052 (beginning K-71-89).&ensp; See my annotations to those rows for further details.",
    (2, 54, 0): "Properly, 02-54-53 is U+7001 (瀁) with its right-hand component simplified to 飬 (unregistered BabelStone IVS: U+7001+E0103), while U+3071D 𰜝 instead simplifies the right-hand component to 养.",
    (2, 18, 93): "Compare 04-17-31; see remarks at 00-90-30.",
    (4, 17, 0): "Compare 04-17-31 with 00-90-30 and 02-18-93.",
    (5, 37, 0): "Compare 05-37-52 with 07-56-19.",
    (7, 1, 0): "There are multiple constituent character sets shown here in plane 7:</p><ul><li>Selections from the \"General Purpose Han Characters for Modern Chinese\" (row 1), followed by 07-01-43 which <a href=\"https://www.unicode.org/irg/docs/n2788-GSourceIssues.pdf#page=4\">appears to be additional to that</a>.&ensp;This character set is first attested in <a href=\"https://web.archive.org/web/20150104034755/http://std.dkuug.dk/jtc1/sc2/wg2/docs/N0667.doc\">WG2 N667</a> from before the ISO 10646 / Unicode merger, and has been listed since the first version of the Unihan database mappings (<a href=\"https://www.unicode.org/Public/1.1-Update/CJKXREF.TXT\">CJKXREF</a>).&ensp;Having been included since Unicode 1.0.1, these characters are included in the Unicode URO.\n<li>Selections from the \"General List of Simplified Hanzi\" (row 2).&ensp;These were added in Unicode 3.0; hence, they are included in CJK Extension A; they were kept under the same \"G7\" source prefix, but a mention of \"General List of Simplified Hanzi\" was added to the documentation of that source prefix.\n<li>Row 3.&ensp;These were also added in Unicode 3.0 as part of CJK Extension A, and also given source references with the \"G7-\" prefix, but <a href=\"https://www.unicode.org/irg/docs/n2788-GSourceIssues.pdf#page=4\">appear not to have been sourced from either list</a>.\n<li>GB 16500, the \"Seventh Supplementary Set\" (rows 16 and up).&ensp;It was intended to <a href=\"https://www.unicode.org/L2/L2018/18263-telegraph-add.pdf\">include all of the characters in the Unicode 2.0 URO that did not have another Mainland China source reference</a>.&ensp;Despite its title, this part was not added to the Unihan \"G7-\" source when it was published.&ensp;Instead, it was added pursuant to <a href='https://web.archive.org/web/20241124092456/https://appsrv.cse.cuhk.edu.hk/~irg/irg/N376'>IRG N376</a> as a separate source, and given the \"GE-\" source prefix—the \"E\" appears to stand for \"extension\", in reference to <a href=\"https://www.unicode.org/L2/L2023/23089-irgn2609-extb-g-glyph-changes.pdf#page=5\">its status as a set of horizontal extensions</a> (i.e. additional reference glyphs for existing Unicode codepoints).\n<li>The complete sixth appendix (\"Data Statistics Table of Hanzi not included in GB 2312\") of the \"General Purpose Han Characters for Modern Chinese\", which was converted to a 94×94 set in <a href=\"https://www.unicode.org/irg/docs/n2808-GSourceChanges.pdf\">IRGN2808</a>.&ensp;Since this also uses rows 16 and up, it collides with GB 16500.</ul><p>",
    (7, 56, 0): "07-56-19 is not, strictly speaking, part of GB 16500, but a small extension to it; it was disunified from 05-37-52.&ensp;See <a href=\"https://www.unicode.org/irg/docs/n2297-GSourceChanges.pdf\">IRG N2297</a>.",
    (8, 16, 36): "U+2B92C 𫤬 is a pictographic variant of 溝 (\"ditch\") and should have straight vertical lines (while the horizontal lines may be straight or slanted), but its reference glyph was poorly designed, making it look more like U+5146 兆 (\"trillion\").&ensp;See <a href=\"https://www.unicode.org/L2/L2023/23244-irgn2616-glyph-corr.pdf\">IRG N2616 (UTC L2/23-244)</a>.&ensp;This is expected to be fixed in Unicode 16 (2024), per <a href=\"https://www.unicode.org/L2/L2023/23250-irgn2620-recs.pdf#page=3\">IRG recommendation IRG M61.07</a>.",
    (KPLANE, 72, 0): "This row is nominally equivalent to 01-93-07 through 01-93-94, since GB 12052 was not one of the sources submitted for inclusion in the original Unicode URO, so its hanja (from both this row and row 71) were submitted as part of an extended version of GB 12345 instead.</p><p>The handwritten glyphs in GB 12052 <a href=\"https://hc.jsecs.org/irg/ws2021/app/index.php?find=UTC-03193\">differ in a number of places</a> from the typeset glyphs in the extended version of GB 12345.&ensp; By far the most prominent of these is K-72-67, which the handwritten GB 12052 gives as an icheja of the immediately preceeding K-72-66 (U+7233 爳) with the bottom component written as 𰆊, while the GB 12345 extension instead gives it as U+5655 噕, whence the conventional Unicode mapping.",
}
cdispmap = {}
for n, i in enumerate(graphdata.gsets["ir058/macraw"][2]):
    j = graphdata.gsets["ir058/mac"][2][n]
    if i != j:
        cdispmap[(MACSET, n - (94 * 94), j)] = i # Dock by 94*94, negative since it's plane 0.

fnbn = lambda bn: "{:X}".format(bn) if bn != KPLANE else "K"

blot = ""
if os.path.exists("__analyt__"):
    blot = open("__analyt__").read()

for n, p in enumerate([plane0, plane1, plane2, plane3, plane4, plane5, plane7, plane8, planeK]):
    for q in range(1, 7) if p[0] in (0, 7) else range(2, 7):
        bn = p[0]
        f = open("gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        currentbit = titles[bn]
        #
        if q > 2:
            lasturl = "gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q - 1))
            lastname = f"{currentbit}, part {q-1:d}"
        elif q == 2 and bn in (0, 7):
            lasturl = "gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q - 1))
            lastname = f"{planefunc2(bn)}, part {q-1:d}"
        elif bn > 0:
            lastbn = bn - 1 if bn != 7 else 5
            lasturl = "gbplane{}f.html".format(fnbn(lastbn))
            lastname = titles[lastbn] + ", part 6"
        #
        if q < 6:
            nexturl = "gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q + 1))
            nextname = f"{currentbit}, part {q+1:d}"
        elif bn < KPLANE and bn != 5:
            nextbn = bn + 1
            nexturl = "gbplane{}b.html".format(fnbn(nextbn))
            nextname = titles[nextbn] + ", part 2"
        elif bn == 5:
            nexturl = "gbplane{}a.html".format(fnbn(7))
            nextname = planefunc2(7) + ", part 1"
        #
        planewarn = None
        if bn == 8:
            planewarn = "Not all of this plane exists in Unicode.&ensp;This plane is visualised mainly from BabelStone's <a href=\"https://babelstone.co.uk/CJK/SJT-IDS.TXT\">SJT-IDS.TXT</a>."
        #
        showbmppuas = None if bn != 8 else (False, True)
        showgraph.dump_plane(f, planefunc if 1 < q <= 3 else (planefunc2 if q == 1 else planefunc3),
                             kutenfunc, *p, lang="zh-CN" if bn != KPLANE else "ko-CN",
                             part=q, css="../css/codechart.css",
                             menuurl="/gb-conc.html", menuname="Guobiao code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             planewarn=planewarn, siglum="GB", showbmppuas=showbmppuas, blot=blot,
                             pua_collides=(bn == 8))
        f.close()









