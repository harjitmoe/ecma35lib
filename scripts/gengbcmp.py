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

plane1 = (1, ("GB 2312<br>1980", "Registration<br>IR-058", "UTC", "Apple", "GB18030<br>2000", "GB18030<br>2005", "GB18030<br>Full", "CCITT<br>Specified", "CCITT<br>Base Stds"), [
          graphdata.gsets["ir058-1980"][2],
          graphdata.gsets["ir058"][2],
          graphdata.gsets["ir058-1986"][2],
          graphdata.gsets["ir058-mac"][2],
          graphdata.gsets["ir058-2000"][2],
          graphdata.gsets["ir058-2005"][2],
          graphdata.gsets["ir058-full"][2],
          graphdata.gsets["ir165"][2],
          graphdata.gsets["ir165std"][2],
])

titles = [
    "GB 2312",
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

annots = {}
cdispmap = {}

for n, p in enumerate([plane1]):
    for q in range(1, 7):
        bn = n + 1
        f = open("gbplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        currentbit = titles[n]
        #
        if q > 1:
            lasturl = "gbplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = f"{currentbit}, part {q-1:d}"
        elif bn > 1:
            lasturl = "gbplane{:X}f.html".format(bn - 1)
            lastname = titles[n - 1] + ", part 6"
        #
        if q < 6:
            nexturl = "gbplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = f"{currentbit}, part {q+1:d}"
        elif bn < 1:
            nexturl = "gbplane{:X}a.html".format(bn + 1)
            nextname = titles[n + 1] + ", part 1"
        #
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-CN", part=q, css="../css/codechart.css",
                             menuurl="/gb-conc.html", menuname="Guobiao code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             siglum="GB")
        f.close()









