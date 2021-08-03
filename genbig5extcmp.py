#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import traditional, cellemojidata
from ecma35.data import graphdata, showgraph
import json, os
import unicodedata as ucd

cdispmap = {}
annots = {}

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

plane1 = (1, ("UTC <br/>BIG5.TXT", "Microsoft <br/>MS-950", "Python <br/>\"MS-950\"", "IBM <br/>IBM-950", "CNS Big5 <br/>Big5-2003", "CNS Big5 <br/>Big5-E", "ETEN", "HKSCS <br/>GCCS", "HKSCS <br/>1999", "HKSCS <br/>2001", "HKSCS <br/>2004", "HKSCS <br/>WHATWG", "WHATWG <br/>Encoder", "ChinaSea <br/>At-On 2.41", "ChinaSea <br/>At-On 2.50", "Dynalab <br/>Ext. A", "Dynalab <br/>Ext. B", "Monotype <br/>Extensions"), [
          graphdata.gsets["utcbig5exts"][2],
          graphdata.gsets["ms950exts"][2],
          pseudomicrosoft,
          graphdata.gsets["ibmbig5exts"][2],
          graphdata.gsets["big5-2003-exts"][2],
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

def planefunc(number, mapname=None):
    if mapname is None:
        return "Big5 extension set"
    else:
        return ""

def kutenfunc(number, row, cell):
    lead = ((row + 1) // 2) + 0x80
    if lead >= 164:
        lead += 85
    elif lead >= 161:
        lead += 37
    if row % 2:
        trail = cell + 0x20
    else:
        trail = cell + 0xA0
    anchorlink = "<a href='#{:d}.{:d}.{:d}'>0x{:02X}{:02X}</a>".format(
                 number, row, cell, lead, trail)
    pseudokuten = "(Ψ-{:02d}-{:02d})".format(row, cell)
    return "{}<br>{}".format(anchorlink, pseudokuten)

for p in [plane1]:
    for q in range(1, 7):
        bn = p[0]
        f = open("b5xplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "b5xplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "Big5 extension set, part {1:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "b5xplane{:X}f.html".format(bn - 1)
            lastname = "Big5 extension set, part 6".format(bn - 1)
        else:
            lasturl = "cnsplane2f.html"
            lastname = "CNS 11643 plane 2, part 6"
        if q < 6:
            nexturl = "b5xplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "Big5 extension set, part {1:d}".format(bn, q + 1)
        elif bn < 1:
            nexturl = "b5xplane{:X}a.html".format(bn + 1)
            nextname = "Big5 extension set, part 1".format(bn + 1)
        else:
            nexturl = "cnsplane3a.html"
            nextname = "CNS 11643 plane 3, part 1"
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-HK", part=q, css="/css/codechart.css",
                             menuurl="/cns-conc.html", menuname="CNS 11643 and Big5 comparison tables",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             pua_collides=False, big5ext_mode=True, siglum="CNS")
        f.close()








