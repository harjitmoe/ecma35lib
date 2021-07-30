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

plane1 = (1, ("UTC<br>Ported old", "UTC<br>New files", "MS/HTML5", "Macintosh"), [
          graphdata.gsets["ir149-altutc"][2],
          graphdata.gsets["ir149"][2],
          graphdata.gsets["ir149-1998"][2],
          graphdata.gsets["ir149-mac"][2],
])

plane2 = (2, ("Apple<br>Unicode 3.2", "Apple<br>Unicode 4.0", "Updated", "Updated<br>Nishiki-teki"), [
          graphdata.gsets["mac-elex-extras-unicode3_2"][2],
          graphdata.gsets["mac-elex-extras-unicode4_0"][2],
          graphdata.gsets["mac-elex-extras"][2],
          graphdata.gsets["mac-elex-extras-nishiki-teki"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        if number == 1:
            return "Wansung code"
        elif number == 2:
            return "HangulTalk additional plane"
    else:
        return ""

def kutenfunc(number, row, cell):
    anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                 number, row, cell, number, row, cell)
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
        fmteuc = "(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
    elif cell < 0:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{}</a>".format(
                     number, row, -cell, number, row, 
                     "{:02d}+".format(-cell) if cell != -1 else "*")
        cellbyte = 0x40 - cell
        if cellbyte > 0x7D:
            cellbyte += 3
        euc = "{:02X}{:02X}".format(0xA0 + row, cellbyte)
        if cellbyte < 0x70:
            fmteuc = "<nobr>(Mac {}_)</nobr><br/>(EUC-ish ".format(euc[:-1])
        elif cellbyte == 0x70:
            fmteuc = "(Mac {}_, {}81-2)<br/>(EUC-ish ".format(euc[:-1], euc[:-2])
        else:
            fmteuc = "<nobr>(Mac {}+)</nobr><br/>(EUC-ish ".format(euc)
        fmteuc += "1B4F{:02X}{:X}_)".format(0xa0 + row, (0xA0 - cell) >> 4)
    else:
        cellbyte = 0x40 + cell
        if cellbyte > 0x7D:
            cellbyte += 3
        if cellbyte == 0xA1: # not elif
            cellbyte = 0xFF
        euc = "{:02X}{:02X}".format(0xA0 + row, cellbyte)
        fmteuc = "(MacKR {})".format(euc)
    return "{}<br>{}".format(anchorlink, fmteuc)

cdispmap = {}
for n, i in enumerate(korea.rawmac):
    j = graphdata.gsets["ir149-mac"][2][n]
    if j != i:
        cdispmap[(n, j)] = i
"""for n, i in enumerate(korea.rawelex):
    j = graphdata.gsets["mac-elex-extras-nishiki-teki"][2][n]
    if j != i:
        cdispmap[(n + (94 * 94), j)] = i"""
annots = {}

for n, p in enumerate([plane1, plane2]):
    for q in range(1, (7 if n != 1 else 2)):
        bn = n + 1
        f = open("kscplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "{}, part {:d}".format("Wansung code" if (bn == 1) else "HangulTalk additional plane", q - 1)
        elif bn > 1:
            lasturl = "kscplane{:X}f.html".format(bn - 1)
            lastname = "Wansung code, part 6"
        if q < (6 if bn != 2 else 1):
            nexturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "{}, part {:d}".format("Wansung code" if (bn == 1) else "HangulTalk additional plane", q + 1)
        elif bn < 2:
            nexturl = "kscplane{:X}a.html".format(bn + 1)
            nextname = "HangulTalk additional plane, part 1"
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KR", part=q, css="codechart.css",
                             menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             pua_collides=True, showbmppua=(bn == 2))
        f.close()









