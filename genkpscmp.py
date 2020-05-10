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

plane1 = (1, ("1997 KPS", "2003 KPS", "2011 KPS"), [
          graphdata.gsets["ir202"][2],
          graphdata.gsets["ir202-2003"][2],
          graphdata.gsets["ir202-2011"][2],
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
annots = {}

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
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KP", part=q, css="/css/kps.css",
                             menuurl="/kps-conc.html", menuname="KPS character set variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True)
        f.close()








