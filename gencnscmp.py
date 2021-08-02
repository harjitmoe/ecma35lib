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

print("Getting EACC coverage")
eacc_data = tuple(graphdata.gsets["eacc"][2])
eacc_rev = {}
for n, i in enumerate(eacc_data):
    if i and (i not in eacc_rev) and (n >= (96 * 99)) and (n < (95 * 96 * 96)):
        eacc_rev[i] = n
koha_data = tuple(graphdata.gsets["cccii-koha"][2])
for n, i in enumerate(koha_data):
    if i and (i not in eacc_rev) and (n >= (96 * 99)) and (n < (95 * 96 * 96)):
        eacc_rev[i] = n
cccii_data = tuple(graphdata.gsets["cccii"][2])
for n, i in enumerate(cccii_data):
    if i and (i not in eacc_rev) and (n >= (96 * 99)) and (n < (95 * 96 * 96)):
        eacc_rev[i] = n

inverse = dict(zip(traditional.big5_to_cns2.values(), traditional.big5_to_cns2.keys()))

# Swap these over so (a) the Gov.TW mapping's way around for the left and right arrows and (b) the
#   ordering of Big5 non-kanji codepoints compared to the ordering of CNS non-kanji codepoints both
#   look less weirdly non-sequitur. I want the output to be as elucidating as possible.
inverse[(1, 2, 55)] = 0xA1F6
inverse[(1, 2, 56)] = 0xA1F7
def swap_arrows(t):
    return t[:148] + (t[149], t[148]) + t[150:]

print("Loading 1")
plane1 = (1, ("UTC Big5", "UTC CNS", "MS Big5", "Mac Big5", "IBM Big5", "Web Big5", "Yasuoka CNS",
              "ICU '92CNS", "ICU EUC'14", "GOV-TW CNS", "Output"), [
          swap_arrows(traditional.read_big5_planes("UTC/BIG5.TXT", big5_to_cns_g2=traditional.big5_to_cns2, plane=1)),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("UTC/CNS11643.TXT"), 
                "CNS11643.TXT", 
                plane=1),
          swap_arrows(graphdata.gsets["ir171-ms"][2]),
          swap_arrows(graphdata.gsets["ir171-mac"][2]),
          swap_arrows(graphdata.gsets["ir171-ibm950"][2]),
          swap_arrows(graphdata.gsets["ir171-web"][2]),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("Other/Uni2CNS"), 
                "Uni2CNS", 
                plane=1),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=1),
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=1),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=1),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=1),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=1)
          )),
          graphdata.gsets["ir171"][2],
])

print("Loading 2")
plane2 = (2, ("UTC CNS", "Big5", "Yasuoka CNS", "ICU 1992 CNS", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          traditional.read_big5_planes("UTC/BIG5.TXT", big5_to_cns_g2=traditional.big5_to_cns2, plane=2),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("UTC/CNS11643.TXT"), 
                "CNS11643.TXT", 
                plane=2),
          graphdata.gsets["ir172-big5"][2],
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("Other/Uni2CNS"), 
                "Uni2CNS", 
                plane=2),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=2),
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=2),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=2),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=2),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=2)
          )),
          graphdata.gsets["ir172"][2],
])

print("Loading 3")
plane3 = (3, ("UTC CNS", "Yasuoka CNS", "ICU 1992 CNS",
              "ICU EUC 2014", "GOV-TW CNS", "Output", "Output Alt"), [
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("UTC/CNS11643.TXT"), 
                "CNS11643.TXT", 
                plane=14), # yes, really.
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("Other/Uni2CNS"), 
                "Uni2CNS", 
                plane=3),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=3),
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=3),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=3),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=3),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=3)
          )),
          graphdata.gsets["ir183-full"][2],
          graphdata.gsets["ir183-1988plus"][2],
])

print("Loading 4")
plane4 = (4, ("Yasuoka CNS", "ICU 1992 CNS", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("Other/Uni2CNS"), 
                "Uni2CNS", 
                plane=4),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=4),
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=4),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=4),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=4),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=4)
          )),
          graphdata.gsets["ir184"][2],
])

print("Loading 5")
plane5 = (5, ("Yasuoka CNS", "ICU 1992 CNS", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("Other/Uni2CNS"), 
                "Uni2CNS", 
                plane=5),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=5),
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=5),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=5),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=5),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=5)
          )),
          graphdata.gsets["ir185"][2],
])

print("Loading 6")
plane6 = (6, ("Yasuoka CNS", "ICU 1992 CNS", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("Other/Uni2CNS"), 
                "Uni2CNS", 
                plane=6),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=6),
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=6),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=6),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=6),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=6)
          )),
          graphdata.gsets["ir186"][2],
])

print("Loading 7")
plane7 = (7, ("Yasuoka CNS", "ICU 1992 CNS", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("Other/Uni2CNS"), 
                "Uni2CNS", 
                plane=7),
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=7),
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=7),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=7),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=7),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=7)
          )),
          graphdata.gsets["ir187"][2],
])

print("Loading 8")
plane8 = (8, ("GOV-TW CNS",), [
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=8),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=8),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=8)
          )),
])

print("Loading 9")
plane9 = (9, ("GOV-TW CNS",), [
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=9),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=9),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=9)
          )),
])

print("Loading 10")
planeA = (10, ("GOV-TW CNS",), [
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=10),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=10),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=10)
          )),
])

print("Loading 11")
planeB = (11, ("GOV-TW CNS",), [
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=11),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=11),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=11)
          )),
])

print("Loading 12")
planeC = (12, ("ICU EUC 2014", "GOV-TW CNS",), [
          graphdata.gsets["cns-eucg2-ibm"][2][94*94*11:94*94*12],
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=12),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=12),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=12)
          )),
])

print("Loading 13")
planeD = (13, ("ICU EUC 2014", "GOV-TW CNS",), [
          graphdata.gsets["cns-eucg2-ibm"][2][94*94*12:94*94*13],
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=13),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=13),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=13)
          )),
])

print("Loading 14")
planeE = (14, ("GOV-TW CNS",), [
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=14),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=14),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=14)
          )),
])

print("Loading 15")
planeF = (15, ("ICU 1992 CNS", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.decode_main_plane_gl(
                parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
                "cns-11643-1992.ucm", 
                plane=9), # yes, really.
          parsers.decode_main_plane_euc(
                parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
                "euc-tw-2014.ucm", 
                plane=15),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
                    "CNS2UNICODE_Unicode BMP.txt", 
                    plane=15),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
                    "CNS2UNICODE_Unicode 2.txt", 
                    plane=15),
              parsers.decode_main_plane_gl(
                    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
                    "CNS2UNICODE_Unicode 15.txt", 
                    plane=15)
          )),
          graphdata.gsets["cns-eucg2"][2][94*94*14:94*94*15],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "CNS 11643 plane {:d}".format(number)
    else:
        if (mapname == "UTC CNS") and (number == 3):
            return '<br>Plane "14"'
        elif (mapname == "ICU 1992 CNS") and (number == 15):
            return '<br>Plane "9"'
        elif "Big5" in mapname:
            return "<br>Level {}".format(number) if number <= 2 else "(beyond)"
        else:
            return "<br>Plane {}".format(number)

def jlfunc(number, row, cell):
    linknumber = (number * 0x10000) + ((0x20 + row) * 0x100) + (0x20 + cell)
    return "https://www.cns11643.gov.tw/wordView.jsp?ID={:d}".format(linknumber)

def kutenfunc(number, row, cell):
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    elif cell < 0:
        euc = "8e{:02x}{:x}_".format(0xa0 + row, (0xA0 - cell) >> 4)
    else:
        euc = "8e{:02x}{:02x}{:02x}".format(0xA0 + number, 0xA0 + row, 0xA0 + cell)
    big5 = ""
    if (number, row, cell) in inverse:
        big5 = "<br>(Big5 {:04x})".format(inverse[number, row, cell])
    plane_hex = "{:d}-{:02X}{:02X}".format(number, 0x20 + row, 0x20 + cell)
    wordview = jlfunc(number, row, cell)
    if cell >= 0:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                     number, row, cell, number, row, cell)
        linkhtml = "(CNS <a href='{}'>{}</a>)".format(wordview, plane_hex)
    else:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{}</a>".format(
                     number, row, -cell, number, row, 
                     "{:02d}+".format(-cell) if cell != -1 else "*")
        plane_hex = "{:d}-{:02X}{:02X}".format(number, 0x20 + row, 0x20 - cell)
        linkhtml = "(CNS {}_)".format(plane_hex[:-1])
    fmteuc = "(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
    return "{}<br>{}<br>{}{}".format(
           anchorlink, linkhtml, fmteuc, big5)

def unicodefunc(cdisplayi, outfile, i=None, jlfunc=None, number=None, row=None, cell=None):
    # Adds EACC cross references.
    print("<br><span class=codepoint>", file=outfile)
    assert not isinstance(cdisplayi, list)
    print("U+" + "<wbr>+".join(showgraph._codepfmt(j, len(cdisplayi))
                           for j in cdisplayi), file=outfile)
    if len(cdisplayi) == 1:
        showgraph._classify(cdisplayi, outfile)
    assert i in (cdisplayi, None)
    target = None
    if cdisplayi in eacc_rev:
        target = eacc_rev[cdisplayi]
    elif cdisplayi + (0xF87F,) in eacc_rev:
        target = eacc_rev[cdisplayi + (0xF87F,)]
    #
    if target:
        plane = (target // (96 * 96))
        row = ((target // 96) % 96)
        cell = (target % 96)
        cccii_scalar = "{:d}-{:02X}{:02X}".format(plane, row+0x20, cell+0x20)
        part = chr(0x61 + (row // 16))
        target = "../eacctables/ccciiplane{:02d}{}.html#{:d}.{:d}.{:d}".format(
                 plane, part, plane, row, cell)
        print("<br><a href='{}'>EACC {}</a>".format(target, cccii_scalar), file=outfile)
    print(end="</span>", file=outfile)

annots = {
 (1, 1, 0): 'All of plane 1 has two possible EUC codes, a four-byte code prefixed with 0x8EA1 '
            'and a two-byte code without that prefix.&ensp;The ICU mapping for EUC-TW-2014 treats '
            'the four-byte plane 1 codes as unassigned, while the GOV-TW CNS 11643 Word View '
            '(linked from the left column) lists only the four-byte codes.&ensp;It is the '
            'two-byte codes that are listed in this chart.',
 (1, 1, 29): 'All four of these are underscores (horizontal versus vertical, straight versus '
             'squiggly.\u2002For some reason, older CNS charts such as ISO-IR-171 showed them '
             'aligned to the top and right of the box (possibly with the intention to use them for '
             'underlining the previous line?), as opposed to to the bottom and left as in Big5, '
             'current CNS charts, and typical rendering.\u2002This seems to have influenced UTC and '
             'Yasuoka to consider most of them unmapped, except for Yasuoka mapping the horizontal '
             'squiggly one to U+FE4B (which consequently means leaving 01-02-11 unmapped).\u2002The '
             'non-EUC ICU mapping references Yasuoka and follows suit.</p><p>Note that the "normal" '
             'underscore gets mapped to either 01-02-05 or 01-02-06.\u2002Microsoft\' mapping of '
             'the horizontal, straight one here to U+2574 seems to be an arbitrary selection of a '
             'similar character not already used, and current GOV-TW mappings simply follow '
             'the Windows convention here, although CNS charts still display it as an '
             'underscore.\u2002Apple uses a PUA variation hint for a duplicate or alternate form.',
 (1, 2, 6): 'Mapping of bold versus light overscore and underscore is sometimes difficult.\u2002'
            'The UTC Big5 mapping simply maps the bold ones to the replacement character, under '
            'the belief that no acceptable Unicode mapping exists.\u2002Apple uses a PUA variation '
            'hint for a bold form.\u2002Yasuoka (and non-EUC ICU referencing Yasuoka) regards the '
            'bolder of the two underscores as the "normal" underscore, and doesn\'t map the '
            'others.\u2002Microsoft maps the bolder underscore to U+02CD, which appears to be an '
            'arbitrary selection of a similar character not otherwise mapped to (compare '
            '01-01-27 for Microsoft\'s other by-elimination underscore mapping).\u2002Current '
            'GOV-TW mappings appear to follow the Windows convention here (for want of a better '
            'option?).',
 (1, 2, 11): 'Compare 01-01-29.\u2002This one may have fewer, larger peaks compared to that one.',
 (1, 2, 12): 'Big5 and CNS consider this character slightly bolder than the previous one, whereas '
             'Unicode considers it doubled for some reason.\u2002Apple\'s mapping instead uses '
             'an appended PUA variation hint for a bold form.',
 (1, 2, 36): 'Various mappings of various legacy CJK sets map this character to either U+223C '
             '(tilde operator), U+301C (wave dash), or U+FF5E (fullwidth tilde).\u2002Of these: '
             'U+301C was allocated specifically for the character as it appears in JIS (at '
             'JIS 01-01-33), but was displayed in the Unicode charts with curvature inverted '
             'relative to the JIS charts for a considerable time (and is still displayed as '
             'such by some older fonts such as MS PMincho); U+223C is primarily intended as a '
             "mathematical operator (perhaps justifiable in this specific case, since it's in "
             "the middle of several mathematical operaters), and usually shorter; U+FF5E is just "
             'the fullwidth version of the ASCII character and might therefore be rendered '
             'as either a tilde dash or a spacing tilde accent, of any glyph width, within a '
             'roughly 1em advance—although a wave dash is the most common by far.',
 (1, 2, 51): 'U+2641 is the astrological symbol for the earth, and is usually rendered as a globus '
             'cruciger (upside-down Venus); if the version with cross inside the circle is '
             'desired specifically, U+1F728 (🜨, verdigris) is probably more semantically relevant '
             'than U+2295 (⨁, a mathematical symbol), although the latter is often '
             'substituted.\u2002For mathematical use, U+2295 would of course be preferred.',
 (1, 2, 52): 'U+2609 is the astrological symbol for the sun, and U+2299 is a mathematical symbol. '
             'Besides that, they are visually much the same symbol.',
 (1, 2, 56): "Although which way around the arrows are in Big5 is not particularly controversial, "
             "their order within CNS 11643 seems to have changed to match Big5 relatively "
             "recently.\u2002Indeed, current data (as of March 2020) from the National Development "
             "Council in Taiwan (also the source for the GOV-TW column) map 01-02-55 and 01-02-56 "
             "to Big5 A1F6 and A1F7 respectively (see "
             "<a href='https://www.cns11643.gov.tw/wordView.jsp?ID=74327'>here</a> and "
             "<a href='https://www.cns11643.gov.tw/wordView.jsp?ID=74328'>here</a>), "
             "in contrast to older sources such as RFC 1922 "
             "(which ecma35lib uses as its primary concordance of Big5 to CNS), which go out of "
             "their way to interrupt their neat range mappings to swap them.\u2002Both the code "
             "chart registered as ISO-IR-171, and all older CNS mappings, show these arrows in the "
             "opposite order to Big5.\u2002I've deliberately deviated from the RFC 1922 "
             "correspondance for this chart only (not the ecma35lib internals) here since that way "
             "seems to make this chart more self-explanatory.",
 (1, 2, 61): 'For JIS sets, U+2225 is used by Microsoft-influenced mappings where U+2016 is used '
             'by others. This pattern does not seem to hold up for variation in CNS / Big5 '
             'mappings, besides that Microsoft are indeed using U+2225. Graphically, the '
             'difference is that U+2016 is necessarily two straight vertical lines, whereas U+2225 '
             'is sometimes shown vertical and sometimes shown slanted.',
 (1, 3, 3): 'The preceding sequence of nine Chinese characters were created as unit symbols; '
             'Big5 and CNS include them in their unit symbols section, not their Chinese character '
             'section.',
 (1, 4, 32): 'The Suzhou numerals for ten, twenty and thirty were originally unified with the '
             'sinograms of the same glyph and meaning.\u2002This made the ten and thirty here '
             'duplicates before they were disunified in Unicode 3.0.\u2002The UTC Big5 mapping '
             'just maps them to the replacement character, suggesting a suitable mapping not to '
             'exist.\u2002Apple uses a private-use transcoding hint to allow round-tripping.\u2002'
             'Those mappings map the twenty to its URO codepoint, since its other CNS encoding '
             '(03-01-24) was outside of Big5.',
 (1, 5, 77): "The UTC mappings' rubrics also list U+2003 as an alternative here, since some "
             "existing implementations rendered an empty space here.\u2002This is attributed to "
             "the absence of a marker being standard zhuyin for the tone in question.",
 (1, 6, 10): "The older ICU mapping file counts Yasuoka amongst its attributed sources, so this "
             "seems to be an error on Yasuoka's part.\u2002Indeed, ISO-IR-171 includes the circled "
             "numbers 1 through 10 here, like the other mappings.",
 (1, 6, 94): "CNS uses a slightly modified classical radical system, in which ⼡ is not included, "
             "and its characters are listed under ⼢ instead (see 01-07-34 below).\u2002This is "
             "presumably an extension to allow all of Unicode's classical radicals to be encoded.",
 (1, 7, 0): "Regarding the next two-and-a-bit rows: mappings too old to have made use of Unicode's "
            "classical radical codepoints either miss these out altogether (they're outside Big5, "
            "so arguably expendable), or many-to-one map them to their ordinary Chinese character "
            "codepoints from the URO.\u2002The URO mappings for the small number of them which "
            "are only included in this section (i.e. not in the regular Chinese character part "
            "of CNS 11643) seem to have been kept in more recent mappings though.",
 (1, 11, 45): "The CNS encoding for kana is outside of Big5; confusingly, there are actually two "
              "overlapping and incompatible / collisive ways of representing kana in Big5 "
              "(BIG5.TXT versus ETEN).\u2002For interoperability's sake, don't encode kana in Big5 "
              "if you can possibly help it.</p><p>On a more positive note, the CNS kana encoding "
              "remembers the vowel extender (<em>cough</em> GB 2312 <em>cough</em>).",
 (1, 21, 0): "Series of private use (i.e. not standard Unicode) mappings for various positional "
             "forms of various strokes, characters and components in brush script.\u2002This being "
             "additional to the strokes section, the radicals section, and the Chinese character "
             "section, which sections it frequently duplicates (besides being in brush-script "
             "even in mincho/songti style fonts for some reason).\u2002I do not know what they "
             "are intended to be used for.",
 (1, 34, 35): "The Euro sign and circle were added to CNS 11643 in 2007, although Microsoft had "
              "added the Euro sign to Big5 in the corresponding location earlier.",
 (1, 34, 52): "Using private use assignments for grapheme clusters which have standard Unicode "
              "representations just (presumably) because they don't have single codepoints… why?",
 (1, 86, 33): "These two differ in the form of the snout radical used, and are otherwise variants "
              "of the same character.&ensp;Notably, the mappings directly related to CNS 11643 "
              "as opposed to just Big5 use U+5F5E.&ensp;Although Windows-950 uses U+5F5D, IBM-1373 " 
              "(otherwise identical to Windows-950 as far as the CNS-mapped part of Big5 is "
              "concerned, hence it is not shown here) actually follows IBM-950 instead in this "
              "specific location in mapping it to U+5F5E.",
 (2, 23, 79): "I'm following RFC 1922 mappings between CNS and Big5 here, even though the gov-tw "
              "mappings seem to differ.&ensp;Not sure if these two are consistently supposed "
              "to look different in all styles (their TW Kai reference glyphs seem to be the same, "
              "although the TW Sung ones differ).&ensp;Compare 02-30-67.",
 (2, 30, 67): "I'm following RFC 1922 mappings between CNS and Big5 here, even though the gov-tw "
              "mappings seem to differ.&ensp;Not sure if these two are consistently supposed "
              "to look different in all styles (their TW Kai reference glyphs seem to be the same, "
              "although the TW Sung ones differ).&ensp;Compare 02-23-79.",
 (3, 1, 24): "Compare 01-04-31.",
 (3, 66, 38): "Between 1992 and 2007, this was the last <i>de jure</i> codepoint on this "
              "plane.\u200203-66-39 through 03-68-21 were removed and distributed amongst plane 4 "
              "in 1992 (at the same time this plane was moved from an extension in plane 14 to a "
              "standard inclusion in plane 3).\u200203-68-40 onward were included as fictitious "
              "extensions in the version of CNS submitted for incorporating into the original URO, "
              "and only standardised beyond the <i>de facto</i> level in 2007.",
 (3, 68, 63): 'Compare 04-03-65.',
 (3, 68, 77): 'Compare 04-08-93.',
 (3, 69, 26): "The <a href='https://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=6BF6'>"
              "Unihan database</a> (i.e. the up-to-date UCS source) regards this as U+6BF6, while "
              "the <a href='https://www.cns11643.gov.tw/wordView.jsp?ID=222522'>CNS 11643 Word "
              "View</a> (i.e. the up-to-date CNS / GovTW source) regards this one as U+6BF5.&ensp;They "
              "seem to be variants of the same character, but 毵 is more common.&ensp;In "
              "whatever case, compare 15-28-28 (always mapped to U+6BF5 毵), 15-28-30 (always "
              "U+6BF6 毶, although absent in non-GovTW mappings) and 02-49-32 (毿, the version "
              "present in Big5, due to being the favoured version in zh-Hant).",
 (3, 69, 34): 'Compare 04-24-60.',
 (3, 69, 44): 'Compare 04-10-78.',
 (3, 69, 59): 'Compare 04-36-56.',
 (3, 70, 17): 'Compare 04-07-74.',
 (3, 70, 80): 'Compare 04-16-34.',
 (3, 70, 87): 'Compare 04-67-25.',
 (4, 2, 59): "Compare 04-06-05",
 (4, 3, 65): 'Compare 03-68-63.',
 (4, 6, 5): "Compare 04-02-59",
 (4, 7, 74): 'Compare 03-70-17.',
 (4, 8, 7): "Compare 15-08-82",
 (4, 8, 93): 'Compare 03-68-77.',
 (4, 10, 78): 'Compare 03-69-44.',
 (4, 16, 34): 'Compare 03-70-80.',
 (4, 24, 60): 'Compare 03-69-34.',
 (4, 36, 56): 'Compare 03-69-59.',
 (4, 51, 28): "Compare 15-49-93",
 (4, 67, 25): 'Compare 03-70-87.',
 (4, 72, 47): "Compare 05-79-52",
 (5, 79, 52): "Compare 04-72-47",
 (6, 1, 3): "U+3405 㐅 is the number five (also 𠄡, but much more commonly 五 or 伍, hence 㐅 is in the CJKA block).&ensp;U+4E44 乄, on the other hand, is a duplicate encoding in the URO (JIS X 0212's fault) of 〆 (U+3006 IDEOGRAPHIC CLOSING MARK), which is a Japanese abbreviation for words pronounced しめ (shi\u202Fme).&ensp;Both the current and 1992 CNS glyphs are very clearly 㐅, as in, the middle of 𠄡.</p><p>Yasuoka's mapping was published in March 1998, however, and hence predates the CJKA block (the 1992 in ICU's 1992 CNS mapping, unlike the 2014 in its EUC 2014 mapping, references the standard year, not the mapping timestamp, hence it is a shade newer than Yasuoka's, which it cites).",
 (15, 8, 82): "Compare 04-08-07",
 (15, 16, 80): "U+3DB7 and U+2420E (CJKB) are "
               "<a href='https://unicode.org/wg2/docs/n2644.pdf'>known exact duplicates</a>.",
 (15, 28, 28): "See comments at 03-69-26.",
 (15, 28, 30): "See comments at 03-69-26.",
 (15, 49, 93): "Compare 04-51-28",
 (15, 67, 66): "Compare 15-67-74",
 (15, 67, 74): "Compare 15-67-66",
}

blot = ""
if os.path.exists("__analyt__"):
    blot = open("__analyt__").read()

print("Writing HTML")
for n, p in enumerate([plane1, plane2, plane3, plane4, plane5, plane6, plane7, plane8, plane9, planeA, planeB, planeC, planeD, planeE, planeF]):
    for q in range(1, 7):
        bnx = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        bn = bnx[n]
        f = open("cnsplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "cnsplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "CNS 11643 plane {:d}, part {:d}".format(bn, q - 1)
        elif bn == 3:
            lasturl = "b5xplane1f.html"
            lastname = "Big5 extension set, part 6"
        elif bn > 1:
            lasturl = "cnsplane{:X}f.html".format(bnx[n - 1])
            lastname = "CNS 11643 plane {:d}, part 6".format(bnx[n - 1])
        if q < 6:
            nexturl = "cnsplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "CNS 11643 plane {:d}, part {:d}".format(bn, q + 1)
        elif bn == 2:
            nexturl = "b5xplane1a.html"
            nextname = "Big5 extension set, part 1"
        elif bn < 15:
            nexturl = "cnsplane{:X}a.html".format(bnx[n + 1])
            nextname = "CNS 11643 plane {:d}, part 1".format(bnx[n + 1])
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-TW", part=q, css="/css/codechart.css",
                             menuurl="/cns-conc.html", menuname="CNS 11643 and Big5 comparison tables",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, selfhandledanchorlink=True, jlfunc=jlfunc, blot=blot,
                             unicodefunc=unicodefunc, siglum="CNS")
        f.close()








