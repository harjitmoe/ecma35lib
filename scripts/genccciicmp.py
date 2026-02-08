#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021, 2023, 2025, 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import traditional
from ecma35.data import graphdata, showgraph
import json

print("Getting CNS coverage")
cns_data = tuple(graphdata.gsets["cns-eucg2"][2])
cns_data_ms = tuple(graphdata.gsets["cns-eucg2/ms"][2])
cns_data_old = tuple(graphdata.gsets["cns-eucg2/icu/old"][2])
cns_data_icu2014 = tuple(graphdata.gsets["cns-eucg2/icu/2014/full"][2])
cns_data_ibm = tuple(graphdata.gsets["cns-eucg2/ibm/full"][2])
cns_rev = {}
for n, (i, j) in enumerate(zip(cns_data, cns_data_ms)):
    if i and (i == j):
        cns_rev.setdefault(i, n)
for n, (i, j) in enumerate(zip(cns_data, cns_data_old)):
    if i and (i == j):
        cns_rev.setdefault(i, n)
for n, (i, j, k) in enumerate(zip(cns_data, cns_data_icu2014, cns_data_ibm)):
    if i and (i == j) and (i != k):
        cns_rev.setdefault(i, n)
for n, i in enumerate(cns_data):
    if i:
        cns_rev.setdefault(i, n)

manies = []
lavail = []
print("Scanning layer availability")
for pointer in range(96*96*7): # Remember plane 0 exists in the array and is completely empty
    avail = set()
    lavail.append(avail)
    for layer in range(1, 13):
        if graphdata.gsets["cccii/eacc"][2][pointer + (96*96*6*(layer - 1))]:
            avail.update({layer})
    if len(avail) >= 5:
        manies.append(((pointer // 96) // 96, (pointer // 96) % 96, 
                                pointer % 96, len(avail)))
print(manies)

planes = []
are_96 = []
bnx = []
for number in range(1, 73):
    if set(graphdata.gsets["cccii/eacc"][2][96*96*number:96*96*(number + 1)]) == {None}:
        continue
    print("Loading {:d}".format(number))
    planes.append((number, ("Koha Taiwan", "Unihan DB", "Lib. of Cong.", "HKIUG", 
                            "CCCII Out", "EACC Out"), [
              graphdata.gsets["cccii/koha"][2][96*96*number:96*96*(number + 1)],
              traditional.cccii_unihan[96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii/eacc/loc"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii/eacc/hk"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii/eacc"][2][96*96*number:96*96*(number + 1)],
    ]))
    bnx.append(number)
    is_96 = False
    if parsers.to_96(parsers.to_94(planes[-1][2][-1])) != planes[-1][2][-1]:
        is_96 = True
    are_96.append(is_96)
    if not is_96:
        for n, i in enumerate(planes[-1][2]):
            planes[-1][2][n] = parsers.to_94(i)
print("Loading 73")
planes.append((73, ("Koha Taiwan", "Unihan DB", "Lib. of Cong.", "HKIUG", "1990 JIS<br>Plane 1", 
                    "CCCII Out", "EACC Out"), [
          parsers.to_94(graphdata.gsets["cccii/koha"][2][96*96*73:96*96*74]),
          parsers.to_94(traditional.cccii_unihan[96*96*73:96*96*74]),
          parsers.to_94(graphdata.gsets["cccii/eacc/loc"][2][96*96*73:96*96*74]),
          parsers.to_94(graphdata.gsets["cccii/eacc/hk"][2][96*96*73:96*96*74]),
          graphdata.gsets["ir168"][2],
          parsers.to_94(graphdata.gsets["cccii"][2][96*96*73:96*96*74]),
          parsers.to_94(graphdata.gsets["cccii/eacc"][2][96*96*73:96*96*74]),
]))
bnx.append(73)
are_96.append(False)
for number in range(74, 95):
    if set(graphdata.gsets["cccii/eacc"][2][96*96*number:96*96*(number + 1)]) == {None}:
        continue
    print("Loading {:d}".format(number))
    planes.append((number, ("Koha Taiwan", "Unihan DB", "Lib. of Cong.", "HKIUG", 
                            "CCCII Out", "EACC Out"), [
              graphdata.gsets["cccii/koha"][2][96*96*number:96*96*(number + 1)],
              traditional.cccii_unihan[96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii/eacc/loc"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii/eacc/hk"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii"][2][96*96*number:96*96*(number + 1)],
              graphdata.gsets["cccii/eacc"][2][96*96*number:96*96*(number + 1)],
    ]))
    bnx.append(number)
    is_96 = False
    if parsers.to_96(parsers.to_94(planes[-1][2][-1])) != planes[-1][2][-1]:
        is_96 = True
    are_96.append(is_96)
    if not is_96:
        for n, i in enumerate(planes[-1][2]):
            planes[-1][2][n] = parsers.to_94(i)

def planefunc(number, mapname=None):
    if mapname is None:
        return "CCCII plane {:d}".format(number)
    else:
        return "<br>Plane {}".format(number) if "<br>" not in mapname else ""

def kutenfunc(number, row, cell):
    if (cell not in (0, 95)) and (row not in (0, 95)):
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                     number, row, cell, number, row, cell)
        hex7 = "<br>0x{:02X}{:02X}{:02X}".format(0x20 + number, 0x20 + row, 0x20 + cell)
    else:
        # Don't give a kuten for parts outside the 94^n subset
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>0x{:02X}{:02X}{:02X}</a>".format(
                     number, row, cell, 0x20 + number, 0x20 + row, 0x20 + cell)
        hex7 = ""
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

def unicodefunc(cdisplayi, outfile, i=None, jlfunc=None, number=None, row=None, cell=None):
    # Adds CSIC cross references.
    print("<br><span class=codepoint>", file=outfile)
    assert not isinstance(cdisplayi, list)
    print("U+" + "<wbr>+".join(showgraph._codepfmt(j, len(cdisplayi))
                           for j in cdisplayi), file=outfile)
    if len(cdisplayi) == 1:
        showgraph._classify(cdisplayi, outfile)
    assert i in (cdisplayi, None)
    target = None
    if cdisplayi in cns_rev:
        target = cns_rev[cdisplayi]
    elif cdisplayi + (0xF87F,) in cns_rev:
        target = cns_rev[cdisplayi + (0xF87F,)]
    #
    if target:
        plane = (target // (94 * 94)) + 1
        row = ((target // 94) % 94) + 1
        cell = (target % 94) + 1
        cns_scalar = "{:d}-{:02X}{:02X}".format(plane, row+0x20, cell+0x20)
        part = chr(0x61 + (row // 16))
        target = "../cnstables/cnsplane{:X}{}.html#{:d}.{:d}.{:d}".format(
                 plane, part, plane, row, cell)
        print("<br><a href='{}'>CSIC {}</a>".format(target, cns_scalar), file=outfile)
    print(end="</span>", file=outfile)

annots = {
    (1, 11, 48): "Mapping the escudo sign to U+1F4B2 is an absolute kludge, purely to prevent it "
                 "from duplicating the dollar sign mapping.",
    (1, 11, 60): "Apparently, this is a scribal abbreviation of the word \"per\", at least per "
                 "its name in Unicode—although it is substantially the same symbol as the \"Old "
                 "English Libra\" sign encoded at PUA F52D in Aletheia and PUA F5F0 in "
                 "Nishiki-teki.",
    (79, 46, 49): "Considering which initial-consonant group this syllable cluster is in the "
                  "codepoint range for, U+BF01 is likely to be a typo for U+B701.",
    (79, 54, 87): "Glyphs are similar but they are completely different syllables; if considering "
                  "that U+C655 is in all three of KS X 1001, KPS 9566 and GB/T 12052, while "
                  "U+C78F isn't (it's in KS X 1002), U+C655 seems somewhat more likely to be the "
                  "intended syllable.</p><p>Like, 79-48-75, 79-54-87 seems to have been appended "
                  "to its initial-consonant group (hence, neither follows the usual ordering "
                  "within the initial-consonant group, and both are followed by only one "
                  "unallocated position before the next initial-consonant group instead of two), "
                  "so the fact that U+C78F follows the usual codepoint ordering is less relevant "
                  "here.",
    (79, 60, 49): "Both U+D494 and U+D4CC are in all three of KS X 1001, KPS 9566 and GB/T 12052, "
                  "so it's not clear which is intended here.",
}

blot = ""
if os.path.exists("__analyt__"):
    blot = open("__analyt__").read()

print("Writing HTML")
for n, (p, is_96) in enumerate(zip(planes, are_96)):
    for q in range(1, 7):
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
        elif bn < 92:
            nexturl = "ccciiplane{:02d}a.html".format(bnx[n + 1])
            nextname = "CCCII plane {:d}, part 1".format(bnx[n + 1])
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-TW", part=q, css="../css/codechart.css",
                             menuurl="/eacc-conc.html", menuname="CCCII and EACC comparison tables",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, selfhandledanchorlink=True, is_96=is_96, blot=blot,
                             unicodefunc=unicodefunc, always_multicolumn=True)
        f.close()








