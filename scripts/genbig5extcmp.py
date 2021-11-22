#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import traditional, cellemojidata
from ecma35.data import graphdata, showgraph
import json
import unicodedata as ucd

cdispmap = {}
annots = {
 (2, 61, 33): "In IBM's private use area fallback scheme (code pages 1445 and 1449, 1449 in this case) which is being used here, U+F83F through U+F842 are basically duplicates of U+FE33 ︳, U+2574 ╴, U+FE34 ︴ and U+FE4F ﹏ respectively.&ensp;These also appear in IBM CSIC, at 13-04-25 through 13-04-28.&ensp;Compare 01-01-26 through 01-01-29.",
}

def _foo(label, inpt):
    for n, (mebbepua, mebbenot) in enumerate(zip(inpt, graphdata.gsets["hkscs"][2])):
        if mebbepua and mebbenot and (mebbepua != mebbenot) and ucd.category(chr(mebbepua[0])) == "Co":
            cdispmap[(label, n, mebbenot)] = mebbepua
            yield mebbenot
        else:
            yield mebbepua

pseudomicrosoft = tuple(i if i and ucd.category(chr(i[0])) != "Co" else None
                        for i in graphdata.gsets["ms950utcexts"][2])

_blendy = graphdata.gsets["etenextsplus"][2]
lastcode = (0x2550, 0x255E, 0x2561, 0x256A, 0x5341, 0x5345)
deja = set()
def _bar():
    for i in _blendy:
        if not i or i in deja or (len(i) == 1 and i[0] in graphdata.codepoint_coverages["cns-eucg2-ms"] and i[0] not in lastcode):
            yield None
        else:
            deja.update({i})
            yield i
blendy = tuple(_bar())

plane1 = (1, ("UTC <br/>BIG5.TXT", "Microsoft <br/>MS-950", "Python <br/>\"MS-950\"", "IBM <br/>IBM-950", "CNS Big5 <br/>Big5-2003", "CNS Big5 <br/>Big5-Plus", "CNS Big5 <br/>Big5-E", "ETEN", "HKSCS <br/>GCCS", "HKSCS <br/>1999", "HKSCS <br/>2001", "HKSCS <br/>2004", "HKSCS <br/>WHATWG", "WHATWG <br/>Encoder", "ChinaSea <br/>At-On 2.41", "ChinaSea <br/>At-On 2.50", "Dynalab <br/>Ext. A", "Dynalab <br/>Ext. B", "Monotype <br/>Extensions"), [
          graphdata.gsets["utcbig5exts"][2],
          graphdata.gsets["ms950exts"][2],
          pseudomicrosoft,
          graphdata.gsets["ibmbig5exts"][2],
          graphdata.gsets["big5-2003-exts"][2],
          graphdata.gsets["big5-plus-exts1"][2],
          graphdata.gsets["big5e-exts"][2],
          tuple(_foo("ETEN", graphdata.gsets["etenexts"][2])),
          graphdata.gsets["gccs"][2],
          tuple(_foo("HKSCS <br/>1999", graphdata.gsets["hkscs1999"][2])),
          tuple(_foo("HKSCS <br/>2001", graphdata.gsets["hkscs2001"][2])),
          graphdata.gsets["hkscs2004"][2],
          graphdata.gsets["hkscs"][2],
          blendy,
          graphdata.gsets["aton-exts"][2],
          graphdata.gsets["aton-exts2"][2],
          traditional.dynalab_a,
          traditional.dynalab_b,
          graphdata.gsets["monotypeexts"][2],
])

plane2 = (2, ("IBM <br/>IBM-950", "CNS Big5 <br/>Big5-Plus"), [
          graphdata.gsets["ibmbig5exts2"][2],
          graphdata.gsets["big5-plus-exts2"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "Big5 extension set number {0:d}".format(number)
    else:
        return ""

def kutenfunc(number, row, cell):
    if number == 1:
        lead = ((row + 1) // 2) + 0x80
        if lead >= 164:
            lead += 85
        elif lead >= 161:
            lead += 37
        if row % 2:
            trail = abs(cell) + 0x20
        else:
            trail = abs(cell) + 0xA0
    elif number == 2:
        lead = ((row - 1) * 2) + 0x81
        if abs(cell) >= 47:
            lead += 1
        trail = 0x80 + ((abs(cell) - 1) % 47)
    else:
        raise ValueError("plane not 1 or 2")
    if cell >= 0:
        pseudokuten = "({}-{:02d}-{:02d})".format("¿ΨΩ"[number], row, cell)
        big5code = "0x{:02X}{:02X}".format(lead, trail)
    else:
        pseudokuten = "({}-{:02d}-{})".format("¿ΨΩ"[number], row,
            "{:02d}+".format(-cell) if cell != -1 else "*")
        if abs(cell) >= 47:
            big5code = "0x{:02X}{:X}_".format(lead, trail >> 4)
        elif abs(cell) > 1:
            big5code = "0x{:02X}{:02X}+".format(lead, trail)
        else:
            big5code = "0x{:02X}{:02X}+".format(lead, trail - 1)
    if number == 2 and ((abs(cell) - 1) % 47) >= 33:
        return "<a href='#{:d}.{:d}.{:d}'>{}</a>".format(
                     number, row, cell, pseudokuten)
    else:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}</a>".format(
                     number, row, cell, big5code)
        return "{}<br>{}".format(anchorlink, pseudokuten)

for p in [plane1, plane2]:
    for q in range(1, 7):
        bn = p[0]
        f = open("b5xplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "b5xplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "Big5 extension set number {0:d}, part {1:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "b5xplane{:X}f.html".format(bn - 1)
            lastname = "Big5 extension set number {0:d}, part 6".format(bn - 1)
        else:
            lasturl = "cnsplane2f.html"
            lastname = "CNS 11643 plane 2, part 6"
        if q < 6:
            nexturl = "b5xplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "Big5 extension set number {0:d}, part {1:d}".format(bn, q + 1)
        elif bn < 2:
            nexturl = "b5xplane{:X}a.html".format(bn + 1)
            nextname = "Big5 extension set number {0:d}, part 1".format(bn + 1)
        else:
            nexturl = "cnsplane3a.html"
            nextname = "CNS 11643 plane 3, part 1"
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-HK", part=q, css="../css/codechart.css",
                             menuurl="/cns-conc.html", menuname="CNS 11643 and Big5 comparison tables",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             pua_collides=False, big5ext_mode=(bn == 1), siglum="CNS")
        f.close()








