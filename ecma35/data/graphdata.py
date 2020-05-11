#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd
import os, urllib.parse, json, collections, shutil

__all__ = [
    "codepoint_coverages", "gsets", "g94bytes", "g96bytes", "g94nbytes", "g96nbytes", "sumps",
    "rhses", "c0graphics", "gsetflags"
]

# Although we could just use (x in gsets[foo][2]) to test whether a codepoint is covered by a
# given set, it is almost certainly faster to look it up in a set than having to sequentially 
# search a list every time, especially if we're doing it for a large number of codepoints 
# (e.g. the entire original URO in multibyte.guobiao).
cachedirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "covcache")
if (os.environ.get("ECMA35LIBDECACHE", "") == "1") and os.path.exists(cachedirectory):
    shutil.rmtree(cachedirectory)
    os.makedirs(cachedirectory)
class CoveragesOnDemand(dict):
    def __getitem__(self, label):
        if super().__contains__(label):
            return super().__getitem__(label)
        path = os.path.join(cachedirectory, urllib.parse.quote(label) + ".json")
        if not os.path.exists(path):
            my_coverage = set()
            kind, xbcs, codepoints = gsets[label]
            for codeset in codepoints:
                if isinstance(codeset, tuple):
                    if len(codeset) != 1:
                        continue
                    codeset = codeset[0]
                if isinstance(codeset, (list, tuple)): # i.e. STILL tuple (was double wrapped)
                    raise ValueError(codepoints)
                if codeset is not None:
                    my_coverage |= {codeset}
            f = open(path, "w")
            f.write(json.dumps(tuple(my_coverage)))
            f.close()
        else:
            f = open(path, "r")
            my_coverage = set(json.load(f))
            f.close()
        self[label] = my_coverage
        return my_coverage
codepoint_coverages = CoveragesOnDemand()

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
gsets = {"nil": (94, 1, (None,)*94), "Unknown": (94, 1, (None,)*94)}
gsetflags = collections.defaultdict(set)

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
            tuple(b"E"): ("ir009-1", ("ir009-1dec",), ("ir009-1",)),
            tuple(b"F"): "ir009-2",
            tuple(b"G"): "ir010",
            tuple(b"H"): ("ir011", ("ir011dec",), ("ir011",)),
            tuple(b"I"): ("ir013", ("ir013ibm", "ir013mac", "ir013win", "ir013euro"),
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
            tuple(b"`"): ("ir060", ("ir060dec", "ir060dk"), ("ir060",)),
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
            # Other ETS sets
            tuple(b"#1"): "etsfrench",
            tuple(b"#2"): "etsiberian",
            tuple(b"#3"): "etsestonian",
            tuple(b"#4"): "etsbaltic",
            tuple(b"#5"): ("etsgajica", ("etsgajicadollar",), ("etsgajica",)),
            tuple(b"#6"): "etsczechoslovak",
            tuple(b"#7"): "etspolish",
            tuple(b"#8"): "etsromanian",
            tuple(b"#9"): "etsturkish",
            # Other NRCS sets
            tuple(b"$1"): "decswiss", # Note: DEC itself uses b"4" (collides with ARIB Mosaic C)
            tuple(b"$2"): "decdutch", # Note: DEC itself uses b"="
            # Others
            tuple(b"#0"): ("ksroman", ("ksromantilde",), ("ksroman",)),
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
            tuple(b"!0"): "ir111rfc1345", # Not even a private IRR: no practical compatibility.
            tuple(b"~"): "nil"}

g94nbytes = {tuple(b"@"): ("ir042nec", ("ir042ibm", "ir042nec"), ("ir042",)),
             tuple(b"A"): ("ir058-2005", # Preferred version
                           # Private versions
                           ("ir058-hant", "ir058-2000", "ir058-2005", None, "ir058-full",
                            "ir058-mac", "ir058-1980", "ir058-1986"),
                           ("ir058",)), # Original followed by any registered revisions
             tuple(b"B"): ("ir168web",
                           ("ir168web", "ir168mac", "ir168macps", "ir168mackt6", "ir168utc",
                            "ir168osf", "ir168osfa", "ir168osfm", "ir168ibm",
                            "ir168docomo", "ir168kddisym", "ir168sbank", "ir168kddipict"),
                           ("ir087", "ir168")),
             tuple(b"C"): ("ir149-2002", ("ir149-altutc", "ir149-1998", "ir149-2002", "ir149-mac"), ("ir149",)),
             tuple(b"D"): ("ir159",
                           ("ir159va", "ir159osf", "ir159osfa", "ir159osfm", "ir159ibm"),
                           ("ir159",)),
             tuple(b"E"): ("ir165", ("ir165std",), ("ir165",)),
             tuple(b"F"): "ir169",
             tuple(b"G"): ("ir171",
                           ("ir171", "ir171-ms", "ir171-utc", "ir171-utcbig5", "ir171-mac", "ir171-govtw", "ir171-ibm"),
                           ("ir171",)),
             tuple(b"H"): ("ir172",
                           ("ir172", "ir172-ms", "ir172-utc", "ir172-utcbig5", "ir172-mac"),
                           ("ir172",)),
             tuple(b"I"): ("ir183-full",
                           ("ir183-1988", "ir183-1988plus", "ir183", "ir183-full"),
                           ("ir183-1992",)),
             tuple(b"J"): "ir184",
             tuple(b"K"): "ir185",
             tuple(b"L"): "ir186",
             tuple(b"M"): "ir187",
             tuple(b"N"): ("ir202-full", ("ir202-2003", "ir202-2011", "ir202-full"), ("ir202",)),
             tuple(b"O"): "ir228",
             tuple(b"P"): "ir229",
             tuple(b"Q"): "ir233",
             # Traditional Chinese off doing its own thing, as you do... no standard escapes here.
             tuple(b"!1"): ("cns-eucg2", ("cns-eucg2-ibm", "cns-eucg2-ms", "cns-eucg2-mac"), ("cns-eucg2",)),
             tuple(b"!2"): ("hkscs", (), ("ms950exts", "etenexts", "hkscs")),
             tuple(b"!3"): ("ms950utcexts", (), ("utcbig5exts", "ms950utcexts")),
             # Shift_JIS extensions for IBM/Windows/HTML5 and for cellular emoji
             tuple(b"!4"): ("ibmsjisextpua", (), ("ibmsjisext", "ibmsjisext")),
             tuple(b"!5"): "docomosjisext",
             tuple(b"!6"): ("kddipictsjisext", ("kddisymsjisext",), ("kddipictsjisext",)),
             tuple(b"!7"): "sbanksjisext",
             # GB 7589/13131 and GB 7590/13132. Insofar as I can support them.
             tuple(b"!8"): ("gb13131", ("gb7589",), ("gb13131",)),
             tuple(b"!9"): ("gb13132", ("gb7590",), ("gb13132",)),
             tuple(b"!:"): ("mac-elex-extras", ("mac-elex-extras",), ("mac-elex-extras-unicode3_2",)),
             tuple(b"!;"): "2011kpsextras",
             tuple(b"~"): "nil"}

g96nbytes = {tuple(b"!0"):("gbk-nonuro-extras", ("gbk-nonuro-extras-web", "gbk-nonuro-extras-full"), ("gbk-nonuro-extras",)),
             tuple(b"~"): "nil"}

sumps = {"94": g94bytes, "96": g96bytes, "94n": g94nbytes, "96n": g96nbytes}





