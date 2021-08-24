#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import korea, cellemojidata
from ecma35.data import graphdata, showgraph
import json

plane1 = (1, ("Old UTC<br>Ported", "IBM", "Macintosh", "MS/New UTC<br>Unicode 2.0", "MS/HTML5<br>1998 Update", "2002 Update<br>MS-Style"), [
          graphdata.gsets["ir149-altutc"][2],
          graphdata.gsets["ir149-ibm"][2],
          graphdata.gsets["ir149-mac"][2],
          graphdata.gsets["ir149"][2],
          graphdata.gsets["ir149-1998"][2],
          graphdata.gsets["ir149-2002"][2],
])

plane2 = (2, ("KS X 1002<br>No symbols"), [
          graphdata.gsets["ksx1002"][2],
])

plane3 = (3, ("KS X 1027-1<br>Unihan"), [
          graphdata.gsets["ksx1027_1"][2],
])

plane4 = (4, ("KS X 1027-2<br>Unihan"), [
          graphdata.gsets["ksx1027_2"][2],
])

titles = [
    "KSC plane 1 (Wansung)",
    "KSC plane 2 (KS X 1002)",
    "KSC plane 3 (KS X 1027-1)",
    "KSC plane 4 (KS X 1027-2)"
]

def planefunc(number, mapname=None):
    if mapname is None:
        return titles[number - 1]
    return ""

def kutenfunc(number, row, cell):
    if cell >= 0:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                     number, row, cell, number, row, cell)
    else:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{}</a>".format(
                     number, row, -cell, number, row, 
                     "{:02d}+".format(-cell) if cell != -1 else "*")
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
        anchorlink += "<br>(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
    return anchorlink

cdispmap = {}
for n, i in enumerate(korea.rawmac):
    j = graphdata.gsets["ir149-mac"][2][n]
    if j != i:
        cdispmap[(n, j)] = i
for n, i in enumerate(korea.oldunicodeksc):
    j = graphdata.gsets["ir149-altutc"][2][n]
    if j != i:
        cdispmap[(plane1[1][0], n, j)] = i
annots = {
    (1, 1, 75): 'This KS C 6501 character is a "bad character mark", i.e. geta mark, although its '
                'rendition in the code chart is significantly less bold than fonts tend to show '
                'it, being closer to an elongated equals sign.&ensp;Compare the nominally bolder, '
                'but still nominally much less bold/tall than typical display, mark at Ψ-06-61.',
    (1, 1, 77): 'Compare these two with Ψ-06-28 and Ψ-06-29.',
}

for n, p in enumerate([plane1, plane2, plane3, plane4]):
    for q in range(1, 7):
        bn = n + 1
        f = open("kscplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        currentbit = titles[n]
        #
        if q > 1:
            lasturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = f"{currentbit}, part {q-1:d}"
        elif bn > 1:
            lasturl = "kscplane{:X}f.html".format(bn - 1)
            lastname = titles[n - 1] + ", part 6"
        #
        if q < 6:
            nexturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = f"{currentbit}, part {q+1:d}"
        elif bn < 4:
            nexturl = "kscplane{:X}a.html".format(bn + 1)
            nextname = titles[n + 1] + ", part 1"
        else:
            nexturl = "htxplane1a.html"
            nextname = "HangulTalk additional plane, part 1"
        #
        noallocatenotice = None
        planewarn = None
        if bn == 2:
            noallocatenotice = ("Established or deployed mappings do not exist for rows 1&ndash;15 "
                                "of KS X 1002, although they are not empty.&ensp;See also "
                                "<a href='https://twitter.com/ken_lunde/status/398651431072575488'>"
                                "this excerpt of row 12 and part of 11</a> and "
                                "<a href='https://charset.fandom.com/ko/wiki/KS_X_1002'>this "
                                "speculative table</a>.")
            planewarn = ("Rows 1&ndash;15 and 37&ndash;54 are not empty, although they are not "
                         "shown since established or deployed mappings do not exist.&ensp;See "
                         "also <a href='https://twitter.com/ken_lunde/status/398651431072575488'>"
                         "this excerpt of row 12 and part of 11</a> and "
                         "<a href='https://charset.fandom.com/ko/wiki/KS_X_1002'>this speculative "
                         "table</a>.")
        if bn == 4:
            planewarn = ("My sole source for the mapping of KS X 1027-2 is the Unihan database; "
                         "the frequent gaps are likely supposed to contain other hanja characters "
                         "which are either absent from Unicode, or where KS X 1027-2 is not "
                         "listed as their South Korean source mapping.")
        #
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KR", part=q, css="../css/codechart.css",
                             menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             noallocatenotice=noallocatenotice, planewarn=planewarn,
                             skiprows = range(37, 55) if bn == 2 else None, siglum="KSC")
        f.close()









