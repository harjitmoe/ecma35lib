#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Note: since gsets specifies length as second member, no more need for "94n" distinct from "94".
# Necessary since a set could have a length of, say, 3 (take the EUC-TW (DRCS-ish) G2 set).
# Also, the individual characters may be:
#  - None, meaning reserved space.
#  - An integer, giving an equivalent UCS codepoint.
#  - A tuple of:
#     - Positive integers, giving an equivalent UCS codepoint sequence.
#     - The number -1 and one or more positive integers, giving one or more combining diacritics
#       to be combined with the next (not previous) spacing character (e.g. those from ANSEL or
#       from T.51), and would thus need to be moved after it in a Unicode representation.
# Beside None, these are put in CHAR tokens verbatim and may be processed by downstream filters.
gsets = {"nil": (94, 1, (None,)*94),
         "Unknown": (94, 1, (None,)*94)}

# Note: has to be imported after gsets is defined
import multibyte, singlebyte.ecma6, singlebyte.ecma43, singlebyte.ebcdic

g94bytes = {tuple(b"@"): "ir002",
            tuple(b"A"): "ir004",
            tuple(b"B"): "ir006",
            tuple(b"C"): "ir008-1",
            tuple(b"D"): "ir008-2",
            tuple(b"E"): "ir009-1",
            tuple(b"F"): "ir009-2",
            tuple(b"G"): "ir010",
            tuple(b"H"): "ir011",
            tuple(b"I"): "ir013",
            tuple(b"J"): "ir014",
            tuple(b"K"): "ir021",
            tuple(b"L"): "ir016",
            tuple(b"M"): "ir039",
            tuple(b"N"): "ir037",
            tuple(b"O"): "ir038",
            tuple(b"P"): "ir053",
            tuple(b"Q"): "ir054",
            tuple(b"R"): "ir025",
            tuple(b"S"): "ir055",
            tuple(b"T"): "ir057",
            tuple(b"U"): "ir027",
            tuple(b"V"): "ir047",
            tuple(b"W"): "ir049",
            tuple(b"X"): "ir031",
            tuple(b"Y"): "ir015",
            tuple(b"Z"): "ir017",
            tuple(b"["): "ir018",
            tuple(b"\\"): "ir019",
            tuple(b"]"): "ir050",
            tuple(b"^"): "ir051",
            tuple(b"_"): "ir059",
            tuple(b"`"): "ir060",
            tuple(b"a"): "ir061",
            tuple(b"b"): "ir070",
            tuple(b"c"): "ir071",
            tuple(b"d"): "ir173", # or pre-IRR ir072
            tuple(b"e"): "ir068",
            tuple(b"f"): "ir069",
            tuple(b"g"): "ir084",
            tuple(b"h"): "ir085",
            tuple(b"i"): "ir086",
            tuple(b"j"): "ir088",
            tuple(b"k"): "ir089",
            tuple(b"l"): "ir090",
            tuple(b"m"): "ir091",
            tuple(b"n"): "ir092",
            tuple(b"o"): "ir093",
            tuple(b"p"): "ir094",
            tuple(b"q"): "ir095",
            tuple(b"r"): "ir096",
            tuple(b"s"): "ir098",
            tuple(b"t"): "ir099",
            tuple(b"u"): "ir102",
            tuple(b"v"): "ir103",
            tuple(b"w"): "ir121",
            tuple(b"x"): "ir122",
            tuple(b"y"): "ir137",
            tuple(b"z"): "ir141",
            tuple(b"{"): "ir146",
            tuple(b"|"): "ir128",
            tuple(b"}"): "ir147",
            tuple(b"!@"): "ir150",
            tuple(b"!A"): "ir151",
            tuple(b"!B"): "ir170",
            tuple(b"!C"): "ir207",
            tuple(b"!D"): "ir230",
            tuple(b"!E"): "ir231",
            tuple(b"!F"): "ir232",
            tuple(b"~"): "nil"}

g96bytes = {tuple(b"@"): "ir111",
            tuple(b"A"): "ir100",
            tuple(b"B"): "ir101",
            tuple(b"C"): "ir109",
            tuple(b"D"): "ir110",
            tuple(b"E"): "ir123",
            tuple(b"F"): "ir126",
            tuple(b"G"): "ir127",
            tuple(b"H"): "ir138",
            tuple(b"I"): "ir139",
            tuple(b"J"): "ir142",
            tuple(b"K"): "ir143",
            tuple(b"L"): "ir144",
            tuple(b"M"): "ir148",
            tuple(b"N"): "ir152",
            tuple(b"O"): "ir153",
            tuple(b"P"): "ir154",
            tuple(b"Q"): "ir155",
            tuple(b"R"): "ir156",
            tuple(b"S"): "ir164",
            tuple(b"T"): "ir166",
            tuple(b"U"): "ir167",
            tuple(b"V"): "ir157",
            tuple(b"W"): "ir158",
            tuple(b"Y"): "ir179",
            tuple(b"Z"): "ir180",
            tuple(b"["): "ir181",
            tuple(b"\\"): "ir182",
            tuple(b"]"): "ir197",
            tuple(b"^"): "ir198",
            tuple(b"_"): "ir199",
            tuple(b"`"): "ir200",
            tuple(b"a"): "ir201",
            tuple(b"b"): "ir203",
            tuple(b"c"): "ir204",
            tuple(b"d"): "ir205",
            tuple(b"e"): "ir206",
            tuple(b"f"): "ir226",
            tuple(b"g"): "ir208",
            tuple(b"h"): "ir209",
            tuple(b"i"): "ir227",
            tuple(b"j"): "ir234",
            tuple(b"~"): "nil"}

g94nbytes = {tuple(b"@"): "ir042",
             tuple(b"A"): "ir058",
             tuple(b"B"): "ir168", # Or older pre-IRR "ir087"
             tuple(b"C"): "ir149",
             tuple(b"D"): "ir159",
             tuple(b"E"): "ir165",
             tuple(b"F"): "ir169",
             tuple(b"G"): "ir171",
             tuple(b"H"): "ir172",
             tuple(b"I"): "ir183",
             tuple(b"J"): "ir184",
             tuple(b"K"): "ir185",
             tuple(b"L"): "ir186",
             tuple(b"M"): "ir187",
             tuple(b"N"): "ir202",
             tuple(b"O"): "ir228",
             tuple(b"P"): "ir229",
             tuple(b"Q"): "ir233",
             tuple(b"~"): "nil"}

g96nbytes = {tuple(b"~"): "nil"}

sumps = {"94": g94bytes, "96": g96bytes, "94n": g94nbytes, "96n": g96nbytes}







 

