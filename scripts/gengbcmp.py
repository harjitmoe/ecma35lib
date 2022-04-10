#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021, 2022.

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
# There appears to be no №6
# №7: GB-16500: Code of Chinese Ideograms Set for Information Interchange, the 7th Supplementary Set 
# Unihan uses "G7" for a different source which isn't a CCS, and calls GB-16500 GE, but its title indicates it is in fact №7
# GB-8565.2: Information Processing - Coded Character Sets for Text Communication - Part 2: Graphic Characters (Unihan calls it G8; it is an expansion of GB-2312 though, not a plane in its own right.)
# GB-12052: Korean Coded Character Set for Information Interchange (Unihan's GK)

MACSET = "Apple"
plane0 = (0, ("GB 2312<br>1980", "Registration<br>IR-058", "UTC", "IBM-1382", "GB12345", MACSET, "Windows", "GB18030<br>2000", "GB18030<br>2005", "GB18030<br>Full", "CCITT<br>Specified", "CCITT<br>Base Stds", "GB12052"), [
          graphdata.gsets["ir058-1980"][2],
          graphdata.gsets["ir058"][2],
          graphdata.gsets["ir058-1986"][2],
          graphdata.gsets["ir058-ibm"][2],
          graphdata.gsets["ir058-hant"][2][:94*15] + ((None,) * (94*78)),
          graphdata.gsets["ir058-mac"][2],
          graphdata.gsets["ir058-ms"][2],
          graphdata.gsets["ir058-2000"][2],
          graphdata.gsets["ir058-2005"][2],
          graphdata.gsets["ir058-full"][2],
          graphdata.gsets["ir165"][2],
          graphdata.gsets["ir165std"][2],
          graphdata.gsets["gb12052"][2][:94*15] + ((None,) * (94*78)),
])
plane1 = (1, ("GB12345",), [
          graphdata.gsets["ir058-hant"][2],
])
plane2 = (2, ("GB7589",), [
          graphdata.gsets["gb7589"][2],
])
plane3 = (3, ("GB13131",), [
          graphdata.gsets["gb13131"][2],
])
plane4 = (4, ("GB7590",), [
          graphdata.gsets["gb7590"][2],
])
plane5 = (5, ("GB13132",), [
          graphdata.gsets["gb13132"][2],
])
plane7 = (7, ("GB16500",), [
          graphdata.gsets["gb16500"][2],
])
KPLANE = 8
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
    "GB 16500",
    "GB 12052",
]

def planefunc(number, mapname=None):
    if mapname is None:
        return titles[number]
    return ""

def planefunc2(number, mapname=None):
    if mapname is None:
        return "Guobiao 94×94 sets"
    return ""

def kutenfunc(number, row, cell):
    if cell >= 0:
        if number == KPLANE:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>K-{:02d}-{:02d}</a>".format(
                         number, row, cell, row, cell)
        elif number == 0 and row < 16:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}</a>".format(
                         number, row, cell, row, cell)
        else:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                         number, row, cell, number, row, cell)
    else:
        if number == KPLANE:
            anchorlink = "<a href='#{:d}.{:d}.{:d}'>K-{:02d}-{}</a>".format(
                         number, row, -cell, row, 
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
    (0, 1, 12): "Compare 01-46 and JIS 01-01-34.",
    (0, 1, 13): "Compare JIS 01-01-36.&ensp;Unlike the JIS character, Apple seem not to have altered this one from the initial mapping to U+22EF.",
    (0, 1, 46): "Compare 01-12, JIS 01-01-34, and JIS 01-02-52.",
    (0, 1, 71): "Compare 03-04.",
    (0, 2, 67): "Microsoft encodes the euro sign as a single byte code (0x80) instead.",
    (0, 3, 4): "Compare 01-71.",
    (0, 3, 13): "Compare both JIS 01-01-61 and JIS 01-02-17.",
    (0, 3, 71): "Compare 08-32.",
    (0, 3, 94): "Compare JIS 01-01-17.",
    (0, 6, 56): "Some explanation is in order for the following characters.&ensp;The Unicode Vertical Forms block (containing the vertical forms from GB 18030) apparently postdates GB 18030, hence the Apple mappings using PUA hints and the GB18030 and Windows mappings to the Private Use Area.&ensp;This doesn't affect the vertical presentation forms with correspondances to Big5, which were already included in the CJK Compatibility Forms block.",
    (0, 8, 32): "Compare 03-71.",
}
cdispmap = {}
for n, i in enumerate(graphdata.gsets["ir058-macraw"][2]):
    j = graphdata.gsets["ir058-mac"][2][n]
    if i != j:
        cdispmap[(MACSET, n, j)] = i

fnbn = lambda bn: "{:X}".format(bn) if bn != KPLANE else "K"

for n, p in enumerate([plane0, plane1, plane2, plane3, plane4, plane5, plane7, planeK]):
    for q in range(1, 7) if p[0] == 0 else range(2, 7):
        bn = p[0]
        f = open("gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        currentbit = titles[bn]
        #
        if q > 2:
            lasturl = "gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q - 1))
            lastname = f"{currentbit}, part {q-1:d}"
        elif q == 2 and bn == 0:
            lasturl = "gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q - 1))
            lastname = f"{planefunc2(0)}, part {q-1:d}"
        elif bn > 0:
            lastbn = bn - 1 if bn != 7 else 5
            lasturl = "gbplane{}f.html".format(fnbn(lastbn))
            lastname = titles[lastbn] + ", part 6"
        #
        if q < 6:
            nexturl = "gbplane{}{}.html".format(fnbn(bn), chr(0x60 + q + 1))
            nextname = f"{currentbit}, part {q+1:d}"
        elif bn < 8:
            nextbn = bn + 1 if bn != 5 else 7
            nexturl = "gbplane{}b.html".format(fnbn(nextbn))
            nextname = titles[nextbn] + ", part 2"
        #
        planewarn = None
        if bn in (4, 5):
            planewarn = "The copious gaps shown in this plane are probably not actually empty, but rather a result of lack of mapping information (although this probably makes them <i>de facto</i> empty)."
        #
        showgraph.dump_plane(f, planefunc if bn > 0 or q > 1 else planefunc2,
                             kutenfunc, *p, lang="zh-CN" if bn != KPLANE else "ko-CN",
                             part=q, css="../css/codechart.css",
                             menuurl="/gb-conc.html", menuname="Guobiao code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             planewarn=planewarn, siglum="GB")
        f.close()









