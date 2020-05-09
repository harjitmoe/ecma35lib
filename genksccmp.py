#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import japan, cellemojidata
from ecma35.data import graphdata, showgraph
import json, os

plane1 = (1, ("UTC<br>Ported old", "UTC<br>New files", "MS/HTML5", "Macintosh"), [
          graphdata.gsets["ir149-altutc"][2],
          graphdata.gsets["ir149"][2],
          graphdata.gsets["ir149-1998"][2],
          graphdata.gsets["ir149-mac"][2],
])

def planefunc(number, mapname=None):
    assert number == 1
    if mapname is None:
        return "Wansung code"
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
annots = {}

for n, p in enumerate([plane1]):
    for q in range(1, 7):
        bn = n + 1
        f = open("kscplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "Wansung code, part {1:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "kscplane{:X}f.html".format(bn - 1)
            lastname = "Wansung code, part 6".format(bn - 1)
        if q < 6:
            nexturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "Wansung code, part {1:d}".format(bn, q + 1)
        elif bn < 2:
            nexturl = "kscplane{:X}a.html".format(bn + 1)
            nextname = "Wansung code, part 1".format(bn + 1)
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KR", part=q, css="http://harjit.moe/css/jis.css",
                             menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True)
        f.close()








