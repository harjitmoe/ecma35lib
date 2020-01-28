#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = [
    "codepoint_coverages", "gsets", "g94bytes", "g96bytes", "g94nbytes", "g96nbytes", "sumps",
    "rhses", "c0graphics"
]

# Although we could just use (x in gsets[foo][2]) to test whether a codepoint is covered by a
# given set, it is almost certainly faster to look it up in a set than having to sequentially 
# search a list every time, especially if we're doing it for a large number of codepoints 
# (e.g. the entire original URO in multibyte.guobiao).
codepoint_coverages = {}
class GSetCollection(dict):
    def __setitem__(self, label, data):
        super().__setitem__(label, data)
        codepoint_coverages[label] = my_coverage = set()
        kind, xbcs, codepoints = data
        for codeset in codepoints:
            if isinstance(codeset, tuple):
                if len(codeset) != 1:
                    continue
                codeset = codeset[0]
            if codeset is not None:
                my_coverage |= {codeset}

# Note: since gsets specifies length as second member, no more need for "94n" distinct from "94".
# Necessary since a set could have a length of, say, 3 (take the EUC-TW G2 set).
# Also, the individual characters may be:
#  - None, meaning reserved encoding space.
#  - An integer, giving an equivalent UCS codepoint.
#  - A tuple of:
#     - Positive integers, giving an equivalent UCS codepoint sequence.
#     - The number -1 and one or more positive integers, giving one or more combining diacritics
#       to be combined with the next (not previous) spacing character (e.g. those from ANSEL or
#       from T.51), and would thus need to be moved after it in a Unicode representation.
# The individual codepoints are put in individual CHAR tokens verbatim without re-ordering, and
# may be processed further by downstream filters.
gsets = GSetCollection({"nil": (94, 1, (None,)*94),
                        "Unknown": (94, 1, (None,)*94)})
# Presumably not getting codepoint_coverages for "nil" and "Unknown" doesn't really matter. 

c0graphics = {}
rhses = {}
defgsets = {}

# Note: has to be imported after gsets &co are defined
from ecma35.data.multibyte import korea, japan, guobiao, traditional
from ecma35.data.singlebyte import ecma6, ecma43, plainext

g94bytes = {tuple(b"@"): ("ir002", # Preferred version
                          ("ir002tilde",), # Private versions
                          ("ir002",)), # Original followed by any registered revisions
            tuple(b"A"): ("ir004", ("ir004dec",), ("ir004",)),
            tuple(b"B"): ("ir006", ("ir006overline",), ("ir006",)),
            tuple(b"C"): ("ir008-1", ("ir008-1dec",), ("ir008-1",)),
            tuple(b"D"): "ir008-2",
            tuple(b"E"): ("ir009-1", ("ir009-1dec",), ("ir009-1dec",)),
            tuple(b"F"): "ir009-2",
            tuple(b"G"): "ir010",
            tuple(b"H"): ("ir011", ("ir011dec",), ("ir011dec",)),
            tuple(b"I"): ("ir013", ("ir013ibm", "ir013apple", "ir013win", "ir013euro"),
                                   ("ir013",)),
            tuple(b"J"): ("ir014", ("ir014tilde",), ("ir014",)),
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
            tuple(b"Y"): ("ir015", ("ir015ets",), ("ir015",)),
            tuple(b"Z"): "ir017",
            tuple(b"["): "ir018",
            tuple(b"\\"): "ir019",
            tuple(b"]"): "ir050",
            tuple(b"^"): "ir051",
            tuple(b"_"): "ir059",
            tuple(b"`"): ("ir060", ("ic060dk", "ir060dec"), ("ir060",)),
            tuple(b"a"): "ir061",
            tuple(b"b"): "ir070",
            tuple(b"c"): "ir071",
            tuple(b"d"): ("ir173", # Preferred version
                          (), # Private versions
                          ("ir072", "ir173")), # Original followed by any registered revisions
            tuple(b"e"): "ir068",
            tuple(b"f"): "ir069",
            tuple(b"g"): ("ir084", ("ir084dec",), ("ir084",)),
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
            tuple(b"!B"): ("ir170", ("ir170dec", "ir170ets"), ("ir170",)),
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
             tuple(b"A"): ("ir058-2005", # Preferred version
                           # Private versions
                           ("ir058-hant", "ir058-2000", "ir058-2005", "ir058-web", "ir058-full"),
                           ("ir058-1980",)), # Original followed by any registered revisions
             tuple(b"B"): ("ir168web",
                           ("ir168web"),
                           ("ir087", "ir168")),
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
             # Traditional Chinese off doing its own thing, as you do... no standard escapes here.
             # Private designators, so not much point using private revision identifiers.
             tuple(b"!1"): "cns-eucg2",
             tuple(b"!2"): ("hkscs", (), ("ms950exts", "etenexts", "hkscs")),
             tuple(b"!3"): ("ms950utcexts", (), ("utcbig5exts", "ms950utcexts")),
             tuple(b"~"): "nil"}

g96nbytes = {tuple(b"~"): "nil"}

sumps = {"94": g94bytes, "96": g96bytes, "94n": g94nbytes, "96n": g96nbytes}

def show(name, *, plane=None):
    import unicodedata as ucd
    if isinstance(name, tuple):
        x = name
    elif name in rhses:
        if name in c0graphics:
            c0list = c0graphics[name]
        else:
            c0list = c0graphics["437"]
        assert len(c0list) == 33
        if name in defcsets:
            g0set = defcsets[name][0]
        else:
            g0set = "ir006"
        if gsets[g0set][0] == 94:
            x = (256, 1, c0list[:-1] + (0x20,) + gsets[g0set][2] + 
                         c0list[-1:] + rhses[name])
        else:
            assert gsets[g0set][0] == 96
            x = (256, 1, c0list[:-1] + gsets[g0set][2] + rhses[name])
    elif name in gsets:
        x = gsets[name]
    else:
        raise ValueError("unknown set: {!r}".format(name))
    #
    if x[1] == 1:
        sz = 0
        hs = 16
        ofs = 2 if x[0] <= 96 else (8 if x[0] <= 128 else 0)
        series = ((0x20,) if x[0] < 96 else ()) + x[2]
    elif x[1] == 2:
        sz = x[0]
        hs = sz // 2
        ofs = (8 - (hs % 8)) % 8
        series = x[2]
    elif x[1] == 3:
        if plane is None:
            raise ValueError("must specify a single plane to display a multi-plane set")
        elif (plane < 1) and (x[0] <= 94):
            raise ValueError("plane number for a 94^n-set must be at least 1")
        elif plane < 0:
            raise ValueError("plane number for a 96^n-set must be at least 0")
        sz = x[0]
        hs = sz // 2
        ofs = (8 - (hs % 8)) % 8
        series = x[2][(sz * sz) * ((plane - 1) if x[0] <= 94 else plane):][:(sz * sz)]
    else:
        raise ValueError("unsupported set byte length size")
    for (n, i) in enumerate(series):
        if not (n % hs):
            print()
            if sz:
                if not ((n // hs) % 2):
                    print(end = "{:2d}: ".format((n // sz) + ofs))
                else:
                    print(end = " " * 4)
            else:
                print(end = "{:2d}: ".format((n // hs) + ofs))
        #
        if i is None:
            curchar = "\uFFFD"
            zenkaku = False
        elif isinstance(i, tuple) and (len(i) == 1) and (
                (ucd.category(chr(i[0])) == "Co") or (0x80 <= i[0] <= 0x9F)):
            curchar = "\uFFFC"
            zenkaku = False
        elif isinstance(i, tuple):
            curchar = "".join(chr(j) for j in i)
            zenkaku = (ucd.east_asian_width(chr(i[0])) in ("W", "F"))
        elif (ucd.category(chr(i)) == "Co") or (0x80 <= i <= 0x9F):
            curchar = "\uFFFC"
            zenkaku = False
        else:
            curchar = chr(i)
            zenkaku = (ucd.east_asian_width(chr(i)) in ("W", "F"))
        print(curchar, end = " " if not zenkaku else "")
    for i in range((hs - (n % hs) - 1) % hs):
        print(end = "\uFFFD ")
    print()





 

