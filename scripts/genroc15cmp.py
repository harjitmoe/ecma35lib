#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data import graphdata, showgraph

plane_1 = (1, ("HP-UX", "Microsoft", "Output"), [
    graphdata.gsets["tch-teletext-1/hp"][2],
    graphdata.gsets["tch-teletext-1/ms"][2],
    graphdata.gsets["tch-teletext-1"][2],
])

plane_2 = (2, ("HP-UX", "Microsoft", "Output"), [
    graphdata.gsets["tch-teletext-2/hp"][2],
    graphdata.gsets["tch-teletext-2/ms"][2],
    graphdata.gsets["tch-teletext-2"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return f"Traditional Chinese Teletext plane {number:d}"
    return f"<br/>Plane {number}"

def kutenfunc(number, row, cell):
    x = row + 0xA0
    y = cell + (0x20 if number > 1 else 0xA0)
    return f"<a href='#{number:d}.{row:d}.{cell:d}'>{number:02d}-{row:02d}-{cell:02d}</a><br/>0x{x:02X}{y:02X}"

blot = ""
if os.path.exists("__analyt__"):
    blot = open("__analyt__").read()

for p in [plane_1, plane_2]:
    for q in range(1, 7):
        bn = p[0]
        f = open(f"roc15plane{bn:X}{chr(0x60 + q)}.html", "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = f"roc15plane{bn:X}{chr(0x60 + q - 1)}.html"
            lastname = f"Traditional Chinese Teletext plane {bn:d}, part {q - 1:d}"
        elif bn > 1:
            lasturl = f"roc15plane{bn - 1:X}f.html"
            lastname = f"Traditional Chinese Teletext plane {bn - 1:d}, part 6"
        else:
            lasturl = None
            lastname = None
        if q < 6:
            nexturl = f"roc15plane{bn:X}{chr(0x60 + q + 1)}.html"
            nextname = f"Traditional Chinese Teletext plane {bn:d}, part {q+1:d}"
        elif bn < 2:
            nexturl = f"roc15plane{bn + 1:X}a.html"
            nextname = f"Traditional Chinese Teletext plane {bn + 1:d}, part 1"
        else:
            nexturl = None
            nextname = None
        showgraph.dump_plane(
            f, planefunc, kutenfunc, *p, lang="zh-TW", part=q, css="../css/codechart.css",
            lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
            selfhandledanchorlink=True, blot=blot, pua_collides=True, siglum="ROC15")
        f.close()



