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

inverse = dict(zip(traditional.big5_to_cns2.values(), traditional.big5_to_cns2.keys()))

# Swap these over so (a) the Gov.TW mapping's way around for the left and right arrows and (b) the
#   ordering of Big5 non-kanji codepoints compared to the ordering of CNS non-kanji codepoints both
#   look less weirdly non-sequitur. I want the output to be as elucidating as possible.
inverse[(1, 2, 55)] = 0xA1F6
inverse[(1, 2, 56)] = 0xA1F7
def swap_arrows(t):
    return t[:148] + (t[149], t[148]) + t[150:]

macbig5 = tuple(tuple(i) if i is not None else None for i in 
                json.load(open(os.path.join(parsers.directory, "Vendor/macBig5.json"), "r")))

plane1 = (1, ("UTC Big5", "UTC CNS", "MS Big5", "Mac Big5", "Yasuoka CNS",
              "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          swap_arrows(traditional.read_big5_planes("UTC/BIG5.TXT", plane=1)),
          parsers.read_main_plane("UTC/CNS11643.TXT", plane=1),
          swap_arrows(traditional.read_big5_planes("Vendor/CP950.TXT", plane=1)),
          swap_arrows(macbig5[:94*94]),
          parsers.read_main_plane("Other/Uni2CNS", plane=1),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=1),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=1),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=1),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=1),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=1)
          )),
          graphdata.gsets["ir171"][2],
])

plane2 = (2, ("UTC Big5", "UTC CNS", "MS Big5", "Mac Big5", "Yasuoka CNS",
              "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          traditional.read_big5_planes("UTC/BIG5.TXT", plane=2),
          parsers.read_main_plane("UTC/CNS11643.TXT", plane=2),
          traditional.read_big5_planes("Vendor/CP950.TXT", plane=2),
          macbig5[94*94:],
          parsers.read_main_plane("Other/Uni2CNS", plane=2),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=2),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=2),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=2),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=2),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=2)
          )),
          graphdata.gsets["ir172"][2],
])

plane3 = (3, ("UTC CNS", "Yasuoka CNS", "ICU CNS 1992",
              "ICU EUC 2014", "GOV-TW CNS", "Output", "Output Alt"), [
          parsers.read_main_plane("UTC/CNS11643.TXT", plane=14), # yes, really.
          parsers.read_main_plane("Other/Uni2CNS", plane=3),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=3),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=3),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=3),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=3),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=3)
          )),
          graphdata.gsets["ir183"][2],
          graphdata.gsets["ir183-1988plus"][2],
])

plane4 = (4, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=4),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=4),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=4),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=4),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=4),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=4)
          )),
          graphdata.gsets["ir184"][2],
])

plane5 = (5, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=5),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=5),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=5),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=5),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=5),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=5)
          )),
          graphdata.gsets["ir185"][2],
])

plane6 = (6, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=6),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=6),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=6),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=6),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=6),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=6)
          )),
          graphdata.gsets["ir186"][2],
])

plane7 = (7, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=7),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=7),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=7),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=7),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=7),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=7)
          )),
          graphdata.gsets["ir187"][2],
])

planeF = (15, ("ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=9), # yes, really.
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=15),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=15),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=15),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=15)
          )),
          graphdata.gsets["cns-eucg2"][2][94*94*14:94*94*15],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "CNS 11643 plane {:d}".format(number)
    else:
        if (mapname == "UTC CNS") and (number == 3):
            return '<br>Plane "14"'
        elif (mapname == "ICU CNS 1992") and (number == 15):
            return '<br>Plane "9"'
        elif "Big5" in mapname:
            return "<br>Level {}".format(number) if number <= 2 else "(beyond)"
        else:
            return "<br>Plane {}".format(number)

def kutenfunc(number, row, cell):
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    else:
        euc = "8e{:02x}{:02x}{:02x}".format(0xA0 + number, 0xA0 + row, 0xA0 + cell)
    big5 = ""
    if (number, row, cell) in inverse:
        big5 = "<br>(Big5 {:04x})".format(inverse[number, row, cell])
    return "{:02d}-{:02d}-{:02d}<br>(<abbr title='Extended Unix Code'>EUC</abbr> {}){}".format(
           number, row, cell, euc, big5)

for n, p in enumerate([plane1, plane2, plane3, plane4, plane5, plane6, plane7, planeF]):
    for q in range(1, 7):
        bnx = (1, 2, 3, 4, 5, 6, 7, 15)
        bn = bnx[n]
        f = open("cnsplane{:X}{}.html".format(bn, chr(0x60 + q)), "w")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "cnsplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "CNS 11643 plane {:d}, part {:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "cnsplane{:X}f.html".format(bnx[n - 1])
            lastname = "CNS 11643 plane {:d}, part 6".format(bnx[n - 1])
        if q < 6:
            nexturl = "cnsplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "CNS 11643 plane {:d}, part {:d}".format(bn, q + 1)
        elif bn < 15:
            nexturl = "cnsplane{:X}a.html".format(bnx[n + 1])
            nextname = "CNS 11643 plane {:d}, part 1".format(bnx[n + 1])
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-TW", part=q, css="/css/cns.css",
                             menuurl="/cns-conc.html", menuname="CNS 11643 and Big5 comparison tables",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname)
        f.close()








