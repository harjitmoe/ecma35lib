#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import japan
from ecma35.data import graphdata
import json, os

plane1 = (1, ("1978", "1983", "1990", "HTML5", "Mac KT7", "Mac PS", "2004"), [
          graphdata.gsets["ir042"][2],
          graphdata.gsets["ir087"][2],
          graphdata.gsets["ir168"][2],
          graphdata.gsets["ir168web"][2],
          graphdata.gsets["ir168mac"][2],
          graphdata.gsets["ir168macps"][2],
          graphdata.gsets["ir233"][2],
])

plane2 = (2, ("1990", "1990+", "HTML5", "2004"), [
          graphdata.gsets["ir159"][2],
          graphdata.gsets["ir159va"][2],
          #graphdata.gsets["ibmsjisext"][2],
          graphdata.gsets["ir229"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "JIS plane {:d}".format(number)
    else:
        return "Plane {}".format(number)

def kutenfunc(number, row, cell):
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    else:
        assert number == 2
        euc = "8f{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    sjis = "" # TODO
    return "{:02d}-{:02d}-{:02d}<br>(<abbr title='Extended Unix Code'>EUC</abbr> {}){}".format(
           number, row, cell, euc, sjis)

for n, p in enumerate([plane1, plane2]):
    for q in range(1, 7):
        bn = (1, 2, 3, 4, 5, 6, 7, 15)[n]
        f = open("jisplane{:X}{}.html".format(bn, chr(0x60 + q)), "w")
        graphdata.dump_plane(f, planefunc, kutenfunc, "cns.css", "/jis-conc.html", *p, part=q)
        f.close()








