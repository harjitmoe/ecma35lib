#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import traditional
from ecma35.data import graphdata, showgraph
import json, os

lavail = []
print("Scanning layer availability")
for pointer in range(96*96*7): # Remember plane 0 exists in the array and is completely empty
    avail = set()
    lavail.append(avail)
    for layer in range(1, 13):
        if graphdata.gsets["eacc"][2][pointer + (96*96*6*(layer - 1))]:
            avail.update({layer})

planes = []
for number in range(1, 73):
    print("Loading {:d}".format(number))
    planes.append((number, ("Koha Taiwan", "Unihan DB", "Lib. of Cong.", "HKIUG", 
                            "CCCII Out", "EACC Out"), [
              graphdata.gsets["cccii-koha"][2][96*96*number:96*96*(number + 1)],
              traditional.cccii_unihan[96*96*number:96*96*(number + 1)],
              graphdata.gsets["eacc-pure"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["eacc-hongkong"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["eacc"][2][96*96*number:96*96*(number + 1)],
    ]))
print("Loading 73")
planes.append((73, ("Koha Taiwan", "Unihan DB", "Lib. of Cong.", "HKIUG", "1990 JIS<br>Plane 1", 
                    "CCCII Out", "EACC Out"), [
          graphdata.gsets["cccii-koha"][2][96*96*73:96*96*74],
          traditional.cccii_unihan[96*96*73:96*96*74],
          graphdata.gsets["eacc-pure"][2][96*96*73:96*96*74],
          graphdata.gsets["eacc-hongkong"][2][96*96*73:96*96*74],
          parsers.to_96(graphdata.gsets["ir168"][2]),
          graphdata.gsets["cccii"][2][96*96*73:96*96*74],
          graphdata.gsets["eacc"][2][96*96*73:96*96*74],
]))
for number in range(74, 96):
    print("Loading {:d}".format(number))
    planes.append((number, ("Koha Taiwan", "Unihan DB", "Lib. of Cong.", "HKIUG", 
                            "CCCII Out", "EACC Out"), [
              graphdata.gsets["cccii-koha"][2][96*96*number:96*96*(number + 1)],
              traditional.cccii_unihan[96*96*number:96*96*(number + 1)],
              graphdata.gsets["eacc-pure"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["eacc-hongkong"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["eacc"][2][96*96*number:96*96*(number + 1)],
    ]))

def planefunc(number, mapname=None):
    if mapname is None:
        return "CCCII plane {:d}".format(number)
    else:
        return "<br>Plane {}".format(number) if "<br>" not in mapname else ""

def kutenfunc(number, row, cell):
    anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                 number, row, cell, number, row, cell)
    hex7 = "<br>0x{:02X}{:02X}{:02X}".format(0x20 + number, 0x20 + row, 0x20 + cell)
    phase = ""
    templ = "<br>←<a href='ccciiplane{:02d}{}.html#{:d}.{:d}.{:d}'>L1</a>"
    templ2 = "<a href='ccciiplane{:02d}{}.html#{:d}.{:d}.{:d}'>L{:d}</a>"
    if (number < 73) and (((number % 6) != 1) or (row >= 16)):
        layer = ((number - 1) // 6) + 1
        number_in_layer = ((number - 1) % 6) + 1
        target_part = chr(0x61 + (row // 16))
        #
        pointer = (number_in_layer * 96 * 96) + (row * 96) + cell
        layers = sorted(list(lavail[pointer]))
        if 1 in layers:
            layers.remove(1)
        if layer > 1:
            if layer in layers:
                phase = templ.format(number_in_layer, target_part, number_in_layer, row, cell)
        elif layers:
            phase = "<br>→"
            phase += "･".join([templ2.format(number_in_layer + ((i - 1) * 6), target_part, 
                                 number_in_layer + ((i - 1) * 6), row, cell, i)
                               for i in layers])
        # Otherwise add nothing.
    return "{}{}{}".format(anchorlink, hex7, phase)

annots = {}

print("Writing HTML")
for n, p in enumerate(planes):
    for q in range(1, 7):
        bnx = tuple(range(1, 96))
        bn = bnx[n]
        f = open("ccciiplane{:02d}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "ccciiplane{:02d}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "CCCII plane {:d}, part {:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "ccciiplane{:02d}f.html".format(bnx[n - 1])
            lastname = "CCCII plane {:d}, part 6".format(bnx[n - 1])
        if q < 6:
            nexturl = "ccciiplane{:02d}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "CCCII plane {:d}, part {:d}".format(bn, q + 1)
        elif bn < 95:
            nexturl = "ccciiplane{:02d}a.html".format(bnx[n + 1])
            nextname = "CCCII plane {:d}, part 1".format(bnx[n + 1])
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-TW", part=q, css="/css/cns.css",
                             menuurl="/eacc-conc.html", menuname="CCCII and EACC comparison tables",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, selfhandledanchorlink=True, is_96=True)
        f.close()

f = open("eacc-conc.txt", "w")
for base_plane in range(1, 7):
    planes = list(range(base_plane, 73, 6))
    fplanes = "/".join("{:d}".format(i) for i in planes)
    print("* Plane {}".format(fplanes), file=f)
    for part in range(6):
        print(end="  * Rows {:d}–{:d}: ".format(16 * part, 16 * (part + 1)), file=f)
        partletter = chr(0x61 + part)
        print(*["[plane {:d}](/eacctables/ccciiplane{:02d}{}.html )".format(i, i, partletter) 
              for i in planes], sep=", ", file=f)
for plane in range(73, 96):
    print("* Plane {:d}".format(plane), file=f)
    for part in range(6):
        partletter = chr(0x61 + part)
        print("  * [Plane {:d}, rows {:d}–{:d}](/eacctables/ccciiplane{:02d}{}.html )".format(
              plane, 16 * part, 16 * (part + 1), plane, partletter), file=f) 
f.close()







