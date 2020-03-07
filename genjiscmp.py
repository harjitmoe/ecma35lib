#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import japan
from ecma35.data import graphdata, showgraph
import json, os

def to_sjis(men, ku, ten):
    if men == 2:
        if ku < 16:
            order = (1, 8, 3, 4, 5, 12, 13, 14, 15)
            if ku not in order:
                return ""
            ku = order.index(ku) + 95
        elif ku >= 78:
            ku = (ku - 78) + 104
        else:
            return ""
    sward = (ku - 1) >> 1
    spos = (((ku - 1) & 0x1) * 94) + ten - 1
    lead = sward + 0x81
    if lead >= 0xA0:
        lead += 0x40
    trail = spos + 0x40
    if trail >= 0x7F:
        trail += 1
    if men == 2:
        return "<br>{:02d}-{:02d}<br>(<abbr title='Shift JIS'>SJIS</abbr> {:02x}{:02x})".format(
                ku, ten, lead, trail)
    else:
        return "<br>(<abbr title='Shift JIS'>SJIS</abbr> {:02x}{:02x})".format(lead, trail)

plane1 = (1, ("1978 JIS",   "NEC 78JIS", "1983 JIS", "1990 JIS", "UTC JIS", 
              "MS / HTML5", "Mac KT6",   "Mac KT7",  "Mac PS",
              "OSF JIS<br>Plane 1", "OSF JIS<br>Plane 1A", "OSF JIS<br>Plane 1M",
              "IBM 78JIS", "IBM 90JIS",
              "ARIB<br>JIS", "DoCoMo<br>JIS", "KDDI<br>JIS", "SoftBank<br>JIS",
              "2000 JIS",  "2004 JIS"), [
          graphdata.gsets["ir042"][2],
          graphdata.gsets["ir042nec"][2],
          graphdata.gsets["ir087"][2],
          graphdata.gsets["ir168"][2],
          graphdata.gsets["ir168utc"][2],
          graphdata.gsets["ir168web"][2],
          graphdata.gsets["ir168mackt6"][2],
          graphdata.gsets["ir168mac"][2],
          graphdata.gsets["ir168macps"][2],
          graphdata.gsets["ir168osf"][2],
          graphdata.gsets["ir168osfa"][2],
          graphdata.gsets["ir168osfm"][2],
          graphdata.gsets["ir042ibm"][2],
          graphdata.gsets["ir168ibm"][2],
          graphdata.gsets["ir168arib"][2],
          graphdata.gsets["ir168docomo"][2],
          graphdata.gsets["ir168kddi"][2],
          graphdata.gsets["ir168sbank"][2],
          graphdata.gsets["ir228"][2],
          graphdata.gsets["ir233"][2],
])

plane2 = (2, ("1990 JIS", "1990 JIS Ext", "MS / HTML5<br>SJIS Ext",
              "OSF JIS<br>Plane 1", "OSF JIS<br>Plane 1A", "OSF JIS<br>Plane 1M",
              "IBM 90JIS", "DoCoMo<br>SJIS Ext", "KDDI<br>SJIS Ext", "SoftBank<br>SJIS Ext",
              "2000/04 JIS"), [
          graphdata.gsets["ir159"][2],
          graphdata.gsets["ir159va"][2],
          graphdata.gsets["ibmsjisext"][2],
          graphdata.gsets["ir159osf"][2],
          graphdata.gsets["ir159osfa"][2],
          graphdata.gsets["ir159osfm"][2],
          graphdata.gsets["ir159ibm"][2],
          graphdata.gsets["docomosjisext"][2],
          graphdata.gsets["kddisjisext"][2],
          graphdata.gsets["sbanksjisext"][2],
          graphdata.gsets["ir229"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "JIS plane {:d}".format(number)
    elif mapname in ("1978 JIS", "1983 JIS", "Mac KT6", "Mac KT7", "Mac PS", "IBM 78JIS"):
        return ""
    elif "<br>" in mapname:
        return ""
    else:
        return "<br>Plane {}".format(number)

def kutenfunc(number, row, cell):
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    else:
        assert number == 2
        euc = "8f{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    sjis = "" # TODO
    return "{:02d}-{:02d}-{:02d}<br>(<abbr title='Extended Unix Code'>EUC</abbr> {}){}".format(
           number, row, cell, euc, sjis) + to_sjis(number, row, cell)

for n, p in enumerate([plane1, plane2]):
    for q in range(1, 7):
        bn = (1, 2, 3, 4, 5, 6, 7, 15)[n]
        f = open("jisplane{:X}{}.html".format(bn, chr(0x60 + q)), "w")
        showgraph.dump_plane(f, planefunc, kutenfunc, "/css/jis.css", "/jis-conc.html",
                             *p, lang="ja", part=q)
        f.close()








