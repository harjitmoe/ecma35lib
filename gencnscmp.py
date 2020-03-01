#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import traditional
from ecma35.data import graphdata
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

def dump_plane(outfile, number, setnames, plarray):
    zplarray = tuple(zip(*plarray))
    print("<!DOCTYPE html><title>CNS 11643 plane {}</title>".format(number), file=outfile)
    print("""<style>
        table, th, tr, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        table {
            margin-left: auto;
            margin-right: auto;
            background: white;
            color: black;
        }
        th, td {
            max-width: 10rem;
            min-width: 7rem;
        }
        .codepoint {
            font-family: monospace;
            font-size: 0.7rem;
        }
        .codepicture {
            font-family: Noto Serif CJK TC, Source Han Serif TC, Noto Sans CJK TC, Source Han Sans TC, TW-Sung-Ext-B, TW-Kai-Ext-B, BabelStone Han, serif;
            font-size: 1.5rem;
        }
        .codepicture::after {
            /* Ensure more-or-less even vertical position of codepoint */
            content: "\u3000";
            font-family: Noto Serif CJK TC, Source Han Serif TC, Noto Sans CJK TC, Source Han Sans TC, TW-Sung-Ext-B, TW-Kai-Ext-B, BabelStone Han, serif;
            font-size: 1.5rem;
        }
        .pua {
            color: dimgray;
        }
        .spua {
            /* TW-Sung-Plus and TW-Kai-Plus are the Gov-TW-supplied SPUA fonts for CNS */
            font-family: TW-Sung-Plus, TW-Kai-Plus;
            font-size: 1.5rem;
        }
        .vertical {
            -webkit-writing-mode: tb-rl;
            -ms-writing-mode: tb-rl;
            writing-mode: tb-rl;
            writing-mode: vertical-rl;
            display: inline-block;
            width: 1em;
        }
        .undefined {
            background: #999;
        }
        .collision {
            background: #f99;
        }
    </style>""", file=outfile)
    print("<table>", file=outfile)
    for row in range(1, 95):
        print("<thead><tr><th>Codepoint</th>", file=outfile)
        for i in setnames:
            print("<th>", i, "<br>", file=outfile)
            if (i == "UTC CNS") and (number == 3):
                print('Plane "14"', file=outfile)
            elif (i == "ICU CNS 1992") and (number == 15):
                print('Plane "9"', file=outfile)
            elif "Big5" in i:
                print("Level {}".format(number) if number <= 2 else "(beyond)", file=outfile)
            else:
                print("Plane {}".format(number), file=outfile)
        print("</tr></thead>", file=outfile)
        for cell in range(1, 95):
            st = zplarray[((row - 1) * 94) + (cell - 1)]
            if len(set(i for i in st if i is not None)) > 1:
                print("<tr class=collision>", file=outfile)
            else:
                print("<tr>", file=outfile)
            if number == 1:
                euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
            else:
                euc = "8e{:02x}{:02x}{:02x}".format(0xA0 + number, 0xA0 + row, 0xA0 + cell)
            print("<th class=codepoint>{:02d}-{:02d}-{:02d}<br>(EUC {})".format(
                    number, row, cell, euc), file=outfile)
            if (number, row, cell) in inverse:
                print("<br>(Big5 {:04x})".format(inverse[number, row, cell]), file=outfile)
            print("</th>", file=outfile)
            for i in st:
                if i is not None:
                    if i[0] >= 0xF0000:
                        print("<td><span class='codepicture spua' lang=zh-TW>", file=outfile)
                        strep = "".join(chr(j) for j in i)
                    elif 0xE000 <= i[0] < 0xF900:
                        print("<td><span class='codepicture pua' lang=zh-TW>", file=outfile)
                        # Object Replacement Character (FFFD is already used by BIG5.TXT)
                        strep = "\uFFFC"
                    else:
                        print("<td><span class=codepicture lang=zh-TW>", file=outfile)
                        strep = "".join(chr(j) for j in i)
                    #
                    if i[-1] == 0xF87C: # Apple encoding hint for bold form
                        print("<b>", file=outfile)
                        print(strep.rstrip("\uF87C"), file=outfile)
                        print("</b>", file=outfile)
                    elif i[-1] == 0xF87E: # Apple encoding hint for vertical presentation form
                        print("<span class=vertical>", file=outfile)
                        print(strep.rstrip("\uF87E"), file=outfile)
                        print("</span>", file=outfile)
                    else:
                        # Horizontal presentation form, alternative form.
                        # Neither of which we can really do anything with here.
                        print(strep.rstrip("\uF87D\uF87F"), file=outfile)
                    print("</span>", file=outfile)
                    print("<br><span class=codepoint>", file=outfile)
                    print("U+" + "+".join("{:04X}".format(j) for j in i), file=outfile)
                    if len(i) == 1:
                        # BASIC MULTILINGUAL PLANE
                        if 0xE000 <= i[0] < 0xF900:
                            print("(PUA)", file=outfile) # Private-Use Area (of the BMP)
                        elif 0x4E00 <= i[0] < 0x9FA6:
                            print("(URO)", file=outfile) # Unified Repertoire and Ordering
                        elif 0x9FA6 <= i[0] < 0xA000:
                            print("(URO+)", file=outfile) # URO additions
                        elif 0x3400 <= i[0] < 0x4DC0:
                            print("(CJKA)", file=outfile) # CJK Unified Ideographs Extension A
                        elif 0xF900 <= i[0] < 0xFB00:
                            if i[0] in (0xFA0E, 0xFA0F, 0xFA11, 0xFA13, 0xFA14, 0xFA1F,
                                        0xFA21, 0xFA23, 0xFA24, 0xFA27, 0xFA28, 0xFA29):
                                # "Dirty Dozen" of not-actually-Compatibility kanji
                                print("(DD)", file=outfile)
                            else:
                                print("(CI)", file=outfile) # Compatibility Ideographs
                        elif i[0] in (0xFFFC, 0xFFFD):
                            print("(REPL)", file=outfile) # Replacement character (in BIG5.TXT)
                        elif i[0] < 0x10000:
                            print("(BMP)", file=outfile) # elsewhere on Basic Multilingual Plane
                        # SUPPLEMENTARY MULTILINGUAL PLANE
                        elif 0x10000 <= i[0] < 0x20000:
                            print("(SMP)", file=outfile) # Supplementary Multilingual Plane
                        # SUPPLEMENTARY IDEOGRAPHIC PLANE
                        elif 0x20000 <= i[0] < 0x2A6E0:
                            print("(CJKB)", file=outfile) # CJK Unified Ideographs Extension B
                        elif 0x2A700 <= i[0] < 0x2B740:
                            print("(CJKC)", file=outfile) # CJK Unified Ideographs Extension C
                        elif 0x2B740 <= i[0] < 0x2B820:
                            print("(CJKD)", file=outfile) # CJK Unified Ideographs Extension D
                        elif 0x2B820 <= i[0] < 0x2CEB0:
                            print("(CJKE)", file=outfile) # CJK Unified Ideographs Extension E
                        elif 0x2CEB0 <= i[0] < 0x2EBF0:
                            print("(CJKF)", file=outfile) # CJK Unified Ideographs Extension F
                        elif 0x2F800 <= i[0] < 0x2FA20:
                            print("(CIS)", file=outfile) # Compatibility Ideographs Supplement
                        elif 0x20000 <= i[0] < 0x30000:
                            print("(SIP)", file=outfile) # elsewhere on SIP (future-proofing)
                        # TERTIARY IDEOGRAPHIC PLANE
                        elif 0x30000 <= i[0] < 0x40000:
                            print("(TIP)", file=outfile) # Tertiary Ideographic Plane
                        # SUPPLEMENTARY SPECIAL-PURPOSE PLANE
                        elif 0xE0000 <= i[0] < 0xF0000:
                            print("(SSP)", file=outfile) # Supplementary Special-purpose Plane
                        # SUPPLEMENTARY PRIVATE USE AREA
                        elif 0xF0000 <= i[0] < 0x100000:
                            print("(SPUA)", file=outfile) # Supplementary Private-Use Area A
                        elif i[0] >= 0x100000:
                            print("(SPUB)", file=outfile) # Supplementary Private-Use Area B
                    print("</span></td>", file=outfile)
                else:
                    print("<td class=undefined></td>", file=outfile)
            print("</tr>", file=outfile)
    print("</table>", file=outfile)

f = open("cnsplane1.html", "w")
dump_plane(f, *plane1)
f.close()
f = open("cnsplane2.html", "w")
dump_plane(f, *plane2)
f.close()
f = open("cnsplane3.html", "w")
dump_plane(f, *plane3)
f.close()
f = open("cnsplane4.html", "w")
dump_plane(f, *plane4)
f.close()
f = open("cnsplane5.html", "w")
dump_plane(f, *plane5)
f.close()
f = open("cnsplane6.html", "w")
dump_plane(f, *plane6)
f.close()
f = open("cnsplane7.html", "w")
dump_plane(f, *plane7)
f.close()
f = open("cnsplaneF.html", "w")
dump_plane(f, *planeF)
f.close()





