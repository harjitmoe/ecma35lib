#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import korea, cellemojidata
from ecma35.data import graphdata, showgraph
import json, os

plane1 = (1, ("Old UTC<br>Ported", "IBM", "Macintosh", "MS/New UTC<br>Unicode 2.0", "MS/HTML5<br>1998 Edition", "2002 Edition"), [
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

plane5 = (5, ("Apple<br>Unicode 3.2", "Apple<br>Unicode 4.0", "Updated", "Updated<br>Nishiki-teki PUA"), [
          graphdata.gsets["mac-elex-extras-unicode3_2"][2],
          graphdata.gsets["mac-elex-extras-unicode4_0"][2],
          graphdata.gsets["mac-elex-extras"][2],
          graphdata.gsets["mac-elex-extras-nishiki-teki"][2],
])

titles = [
    "KSC plane 1 (Wansung)",
    "KSC plane 2 (KS X 1002)",
    "KSC plane 3 (KS X 1027-1)",
    "KSC plane 4 (KS X 1027-2)",
    "HangulTalk additional plane",
]

def planefunc(number, mapname=None):
    if mapname is None:
        return titles[number - 1]
    else:
        return ""

def kutenfunc(number, row, cell):
    if cell >= 0:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}-{:02d}-{:02d}</a>".format(
                     number, row, cell, f"{number:02d}" if number != 5 else "Ψ", row, cell)
    else:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}-{:02d}-{}</a>".format(
                     number, row, -cell, f"{number:02d}" if number != 5 else "Ψ", row, 
                     "{:02d}+".format(-cell) if cell != -1 else "*")
    #
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
        fmteuc = "<br>(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
    elif number < 5:
        fmteuc = ""
    elif cell < 0:
        cellbyte = 0x40 - cell
        if cellbyte > 0x7D:
            cellbyte += 3
        euc = "{:02X}{:02X}".format(0xA0 + row, cellbyte)
        if cellbyte < 0x70:
            fmteuc = "<br><nobr>(Mac {}_)</nobr><br/>(EUC-ish ".format(euc[:-1])
        elif cellbyte == 0x70:
            fmteuc = "<br>(Mac {}_, {}81-2)<br/>(EUC-ish ".format(euc[:-1], euc[:-2])
        else:
            fmteuc = "<br><nobr>(Mac {}+)</nobr><br/>(EUC-ish ".format(euc)
        fmteuc += "1B4F{:02X}{:X}_)".format(0xa0 + row, (0xA0 - cell) >> 4)
    else:
        cellbyte = 0x40 + cell
        if cellbyte > 0x7D:
            cellbyte += 3
        if cellbyte == 0xA1: # not elif
            cellbyte = 0xFF
        euc = "{:02X}{:02X}".format(0xA0 + row, cellbyte)
        fmteuc = "<br>(MacKR {})".format(euc)
    return "{}{}".format(anchorlink, fmteuc)

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
    (5, 7, 63): 'Compare Ψ-11-04.',
    (5, 11, 4): 'Compare Ψ-07-63.',
    (5, 8, 73): 'Most fonts show U+2939\'s head pointing SW rather than the south intended here.&ensp;'
                '<a href="https://www.fileformat.info/info/unicode/char/2939/fontsupport.htm">'
                'PragmataPro</a> is apparently one exception.',
    (5, 8, 81): 'This is a cross barby, which has meanings as diverse as a "move window" cursor, '
                'or Nazism and white supremacy, amongst other uses.',
}

for n, p in enumerate([plane1, plane2, plane3, plane4, plane5]):
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
        elif bn < 5:
            nexturl = "kscplane{:X}a.html".format(bn + 1)
            nextname = titles[n + 1] + ", part 1"
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
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KR", part=q, css="codechart.css",
                             menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             pua_collides=True, showbmppuas=None if (bn != 5) else (0, 0, 0, 1),
                             noallocatenotice=noallocatenotice, planewarn=planewarn,
                             skiprows = range(37, 55) if bn == 2 else None, siglum="KSC")
        f.close()









