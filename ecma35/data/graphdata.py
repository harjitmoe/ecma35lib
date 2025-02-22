#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2021/2023/2024/2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, urllib.parse, json, collections, shutil

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
        path = os.path.join(cachedirectory, urllib.parse.quote(label, "") + ".json")
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
#  - A tuple of integers, giving an equivalent UCS codepoint sequence.
# Negative integers may also be used, denoting a combining character which requires translocation
#   to after the next base character.
class GrumblingDict(dict):
    def __init__(self, name, initial = None):
        super().__init__(initial or {})
        self._name = name
    def __setitem__(self, key, value):
        if key in self:
            print(f"{key!r} already in dictionary {self._name!r}", file=sys.stderr)
        super().__setitem__(key, value)
gsets = GrumblingDict("gsets", {"nil": (94, 1, (None,)*94), "Unknown": (94, 1, (None,)*94)})
gsetflags = collections.defaultdict(set)

c0graphics = GrumblingDict("c0graphics")
rhses = GrumblingDict("rhses")
defgsets = GrumblingDict("defgsets")
chcpdocs = GrumblingDict("chcpdocs")
ebcdicdbcs = GrumblingDict("ebcdicdocs")

# Note: has to be imported after gsets &co are defined
from ecma35.data.multibyte import korea, japan, guobiao, traditional, tcvn
from ecma35.data.singlebyte import ecma6, extlatin, c0substs, dingbats, quoocs_ngwx, ccitt, cyrillic, semitic, greek, indic, otherscript, splitebcdic, pseudographics, kana, fragment, userdefined

for _i in rhses:
    chcpdocs.setdefault(_i, "plainextascii")

chcpdocs["1200"] = chcpdocs["1201"] = "utf-16be"
chcpdocs["1202"] = chcpdocs["1203"] = "utf-16le"
chcpdocs["1204"] = chcpdocs["1205"] = "utf-16"
chcpdocs["1208"] = chcpdocs["1209"] = "utf-8"
chcpdocs["1210"] = chcpdocs["1211"] = "utf-ebcdic"
chcpdocs["1212"] = chcpdocs["1213"] = "scsu"
chcpdocs["1232"] = chcpdocs["1233"] = "utf-32be"
chcpdocs["1234"] = chcpdocs["1235"] = "utf-32le"
chcpdocs["1236"] = chcpdocs["1237"] = "utf-32"
chcpdocs["1392"] = chcpdocs["5488"] = "gbk"

g94bytes = {tuple(b"@"): ("ir002", # Preferred version
                          ("ir002/tilde",), # Private versions
                          ("ir002",)), # Original followed by any registered revisions, each of which must be superset of the previous
            tuple(b"A"): ("ir004", ("ir004/dec",), ("ir004",)),
            tuple(b"B"): ("ir006",
                          ("ir006/overline", "ir006/brvbar", "ir006/pli", "ir006/florin",
                           "ir006/smartquotes", "ir006/ocr-a", "ir006/ibm-hp-alternatives",
                           "ir006/ibm-hp-diacritics", "ir006/ibm-hp-ascii-tilde"),
                          ("ir006",)),
            tuple(b"C"): ("ir008-1", ("ir008-1/dec",), ("ir008-1",)),
            tuple(b"D"): "ir008-2",
            tuple(b"E"): ("ir009-1", ("ir009-1/dec",), ("ir009-1",)),
            tuple(b"F"): "ir009-2",
            tuple(b"G"): ("ir010", ("ir010/ibm",), ("ir010",)),
            # Note: some pre-standardised variants of ISO-2022-JP / JIS_Encoding, as well as OKI
            #   dot-matrix / line printers, interpret "H" in a nonstandard way
            #   (as "ir013" or "ir006").
            tuple(b"H"): ("ir011", ("ir011/dec",), ("ir011",)),
            tuple(b"I"): ("ir013", ("ir013/ibm", "ir013/mac", "ir013/win", "ir013/euro",
                                    "ir013/ibm/strict", "ir013/ibm/alternate", "ir013/ibm/sjis"),
                                   ("ir013",)),
            tuple(b"J"): ("ir014", ("ir014/tilde",), ("ir014",)),
            tuple(b"K"): ("ir021", ("ir021/acute", "ir021/ibm38xx"), ("ir021",)),
            tuple(b"L"): "ir016",
            tuple(b"M"): "ir039",
            tuple(b"N"): "ir037",
            tuple(b"O"): ("ir038/ext", ("ir038/ext",), ("ir038",)),
            tuple(b"P"): ("ir053/ext", ("ir053/ext",), ("ir053",)),
            tuple(b"Q"): "ir054", # Note: VTx/XTerm/compatibles interpret this as ir121, bizarrely.
            tuple(b"R"): ("ir025", ("ir025/ibmbelgian", "ir025/ibmbelgianwp", "ir025/ibmbelgian38xx"), ("ir025",)),
            tuple(b"S"): "ir055",
            tuple(b"T"): "ir057",
            tuple(b"U"): "ir027",
            tuple(b"V"): "ir047",
            tuple(b"W"): "ir049",
            tuple(b"X"): "ir031",
            tuple(b"Y"): ("ir015", ("ir015/ets", "ir015/notsign", "ir015/ibmdcf"), ("ir015",)),
            tuple(b"Z"): "ir017",
            tuple(b"["): "ir018",
            tuple(b"\\"): "ir019",
            tuple(b"]"): "ir050",
            tuple(b"^"): ("ir051", ("ir051/dec",), ("ir051",)),
            tuple(b"_"): "ir059",
            tuple(b"`"): ("ir060", ("ir060/dec", "ir060/dk", "ir060/ibm"), ("ir060",)),
            tuple(b"a"): "ir061",
            tuple(b"b"): "ir070",
            tuple(b"c"): "ir071",
            tuple(b"d"): ("ir173", # Preferred version
                          (), # Private versions
                          ("ir072", "ir173")), # Original followed by any registered revisions, each of which must be superset of the previous
            tuple(b"e"): "ir068",
            tuple(b"f"): ("ir069", ("ir069/ibmmaghreb", "ir069/ibm38xx", "ir069/ibmdcf"), ("ir069",)),
            tuple(b"g"): ("ir084", ("ir084/dec",), ("ir084",)),
            tuple(b"h"): "ir085",
            tuple(b"i"): "ir086",
            tuple(b"j"): "ir088",
            tuple(b"k"): ("ir089", ("ir089/marc",), ("ir089",)),
            tuple(b"l"): ("ir090/ets",
                          ("ir090/ets", "ir090/ets-alpha"),
                          ("ir090",)),
            tuple(b"m"): "ir091",
            tuple(b"n"): "ir092",
            tuple(b"o"): ("ir093/ext", ("ir093/ext",), ("ir093",)),
            tuple(b"p"): ("ir094", ("ir094/ibm",), ("ir094",)),
            tuple(b"q"): ("ir095", ("ir095/double",), ("ir095",)),
            tuple(b"r"): "ir096",
            tuple(b"s"): ("ir098/extended", ("ir098/extended",), ("ir098",)),
            tuple(b"t"): "ir099",
            tuple(b"u"): ("ir102", ("ir102/ibm", "ir102/strict"), ("ir102",)),
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
            tuple(b"!B"): ("ir170", ("ir170/dec", "ir170/ets", "ir170/ibm"), ("ir170",)),
            tuple(b"!C"): "ir207",
            tuple(b"!D"): "ir230",
            tuple(b"!E"): ("ir231/full", ("ir231/marc", "ir231/full"), ("ir231",)),
            tuple(b"!F"): "ir232",
            #
            # "0":
            #     VTx/XTerm/compatible: "decgraphics"
            #     ARIB: fixed-width "aribkana/hiragana"
            # "1":
            #     VTx/MSTerm: "ir006"
            #     ARIB: fixed-width "aribkana/katakana"
            # "2":
            #     VTx/MSTerm: "decgraphics"
            #     MARC: "marc-he"
            #     ARIB: "ir071"
            # "3":
            #     MARC: "ir089/marc"
            #     ARIB and ITU-T.101-B: "ir137"
            # "4":
            #     VTx/XTerm/compatible: "alt646/decdutch"
            #     MARC: "ir224/marc"
            #     ARIB: "aribmosaic-c"
            # "5":
            #     VTx/XTerm/compatible: "ir008-1/dec"
            #     ARIB: nonspacing "Mosaic D" pseudographics
            # "6":
            #     VTx/XTerm/compatible: "ir009-1/dec"
            #     ARIB: proportional-width "ir014"
            # "7":
            #     VTx/XTerm/compatible: "ir011/dec"
            #     ARIB: proportional-width "aribkana/hiragana"
            #
            tuple(b"8"): "aribkana/katakana", # Thus ARIB STD B24 Volume 1
            tuple(b"9"): "ir121", # Thus VTx and compatibles
            tuple(b":"): "user-defined/94",
            tuple(b";"): "alt646/freedos-armenian",
            #tuple(b"<"): preferred supplementary set (set via DECAUPSS; default Latin-1 or DEC MCS)
            tuple(b"="): "alt646/decswiss", # Thus VTx and compatibles
            tuple(b">"): "dectechnical", # Thus VTx and compatibles
            tuple(b"?"): "aribkana/hiragana",
            tuple(b"!0"): "alt646/freedos-turkic",
            tuple(b"!1"): "ibmsymbol",
            tuple(b"!2"): ("alt646/ibm-minus10",
                           ("alt646/ibm-minus3", "alt646/ibm-minus41", "alt646/ibm-minus6",
                            "alt646/ibm-minus7", "alt646/ibm-minus8"),
                           ("alt646/ibm-minus10",)),
            tuple(b"!3"): "ir213",
            tuple(b"!4"): "ir217",
            tuple(b"!5"): "ir218",
            tuple(b"!6"): "ir223",
            tuple(b"!7"): "ibmhebrew7",
            tuple(b"!8"): "digits-only",
            tuple(b"!9"): "ibm-e13b",
            tuple(b"!:"): "ir219",
            tuple(b"!;"): "ir220",
            tuple(b"!<"): "webdings_g0",
            tuple(b"!="): "wingdings1_g0",
            tuple(b"!>"): "wingdings2_g0",
            tuple(b"!?"): "wingdings3_g0",
            tuple(b"\"0"): "iscii/devanagari",
            tuple(b"\"1"): "nbytehangul",
            tuple(b"\"2"): "alt646/hplegal",
            tuple(b"\"3"): "pclinedrawing",
            tuple(b"\"4"): "ir138/dec", # Thus VTx and compatibles
            tuple(b"\"5"): "hplinedrawing",
            tuple(b"\"6"): "hproman",
            tuple(b"\"7"): "ibm-troff",
            tuple(b"\"8"): "stop-symbol",
            tuple(b"\"9"): "adobe-standard",
            tuple(b"\":"): ("alt646/ibmarabic", ("alt646/ibmarabic/tiny",), ("alt646/ibmarabic",)),
            tuple(b"\";"): ("ir166/1986", (), ("ir166/minimal", "ir166/1986")),
            tuple(b"\"<"): "aribmosaic-c",
            tuple(b"\"="): ("alt646/galaksija/extended",
                            (),
                            ("alt646/galaksija", "alt646/galaksija/extended")),
            tuple(b"\">"): "decgreek7", # Thus VTx and compatibles
            tuple(b"\"?"): "decgreek8", # Thus VTx and compatibles
            tuple(b"#0"): ("alt646/ksroman", ("alt646/ksroman/tilde",), ("alt646/ksroman",)),
            tuple(b"#1"): "alt646/etsfrench",
            tuple(b"#2"): "alt646/etsiberian",
            tuple(b"#3"): "alt646/etsestonian",
            tuple(b"#4"): "alt646/etsbaltic",
            tuple(b"#5"): ("alt646/etsgajica", ("alt646/etsgajica/dollar",), ("alt646/etsgajica",)),
            tuple(b"#6"): "alt646/etsczechoslovak",
            tuple(b"#7"): "alt646/etspolish",
            tuple(b"#8"): "alt646/etsromanian",
            tuple(b"#9"): "alt646/etsturkish",
            tuple(b"#:"): "sbank2gpageE",
            tuple(b"#;"): "sbank2gpageF",
            tuple(b"#<"): "sbank2gpageG",
            tuple(b"#="): "sbank2gpageO",
            tuple(b"#>"): "sbank2gpageP",
            tuple(b"#?"): "sbank2gpageQ",
            tuple(b"$0"): "decgraphicsold",
            tuple(b"$1"): "alt646/decswiss", # Note: DEC itself uses b"="
            tuple(b"$2"): "alt646/decdutch", # Note: DEC itself uses b"4"
            tuple(b"$3"): "marlett",
            tuple(b"$4"): "zdings_g0",
            tuple(b"$5"): "zdings_g1",
            tuple(b"$6"): "symbolgl",
            tuple(b"$7"): "symbolgr",
            tuple(b"$8"): "alt646/maltese",
            tuple(b"$9"): ("alt646/icelandic", ("alt646/icelandic/ibm",), ("alt646/icelandic",)),
            tuple(b"$:"): ("alt646/polish/full", 
                           ("alt646/polish/ibm", "alt646/polish/full"), 
                           ("alt646/polish",)),
            tuple(b"$;"): ("ir224", ("ir224/marc",), ("ir224",)), # Note: MARC itself uses b"4"
            tuple(b"$<"): "ir222",
            tuple(b"$="): "ir221",
            tuple(b"$>"): "marc-he", # Note: MARC itself uses b"2"
            tuple(b"$?"): "armscii",
            tuple(b"%0"): "decturkish8", # Thus VTx and compatible
            tuple(b"%1"): "marc-superscript",
            tuple(b"%2"): "alt646/decturkish", # Thus VTx and compatibles
            # %3 collides with VTx "SCS NRCS" (so far as I know, nobody knows what this means)
            tuple(b"%4"): "alt646/ibmquebec",
            tuple(b"%5"): "decmultinational", # Thus VTx and compatibles
            tuple(b"%6"): "ir084/dec", # Thus VTx and compatibles
            tuple(b"%7"): "alt646/ibmportugal",
            tuple(b"%8"): "alt646/ibmturkish",
            tuple(b"%9"): "alt646/ibm38xx",
            tuple(b"%:"): ("alt646/ibmusedwithgreek", 
                           (), 
                           ("alt646/ibmusedwithgreek/small", "alt646/ibmusedwithgreek")),
            tuple(b"%;"): ("alt646/ibmusedwithcyrillic",
                           ("alt646/ibmusedwithcyrillic/small",),
                           ("alt646/ibmusedwithcyrillic",)),
            tuple(b"%<"): "alt646/ibmdcfbelgium",
            tuple(b"%="): "hebrew7", # Thus VTx and compatibles
            tuple(b"%>"): ("alt646/ibmdcf", ("alt646/ibmdcf/braces", "alt646/ibmdcf/degreesign"), ("alt646/ibmdcf",)),
            tuple(b"%?"): "alt646/ibmisrael",
            tuple(b"&0"): ("alt646/ibmjapan", ("alt646/ibmjapan/noyen", "alt646/ibmjapan/swapyen", "alt646/ibmjapan/tiny"), ("alt646/ibmjapan",)),
            tuple(b"&1"): ("alt646/ibmkorea", ("alt646/ibmkorea/small",), ("alt646/ibmkorea",)),
            tuple(b"&2"): ("alt646/ibmlcs/big", ("alt646/ibmlcs/big",), ("alt646/ibmlcs",)),
            tuple(b"&3"): "alt646/ibmschsmall",
            tuple(b"&4"): "ir051/dec", # Thus VTx and compatibles
            tuple(b"&5"): "shortkoi", # Thus VTx and compatibles
            tuple(b"&6"): ("alt646/ibmspanish", ("alt646/ibmspanish/38xx", "alt646/ibmspanish/peseta"), ("alt646/ibmspanish",)),
            tuple(b"&7"): ("alt646/ibmuk", ("alt646/ibmuk/dcf",), ("alt646/ibmuk",)),
            tuple(b"&8"): ("alt646/ibmusa", ("alt646/ibmusa/asciinohatsqb", "alt646/ibmusa/asciinosqb", "alt646/ibmusa/hat", "alt646/ibmusa/tiny"), ("alt646/ibmusa",)),
            tuple(b"&9"): "marc-subscript",
            tuple(b"&:"): "alt646/ibmbritish",
            tuple(b"&;"): ("alt646/ibmbrazil", ("alt646/ibmbrazil/38xx",), ("alt646/ibmbrazil",)),
            tuple(b"&<"): ("alt646/ibmdanish/euro", ("alt646/ibmdanish/euro",), ("alt646/ibmdanish",)),
            tuple(b"&="): ("alt646/ibmswedish/euro", 
                           ("alt646/ibmswedish/euro",), 
                           ("alt646/ibmswedish",)),
            tuple(b"&>"): "alt646/ibmbarcode",
            tuple(b"&?"): ("decgraphics/composite", 
                           ("decgraphics/modified", "decgraphics/composite"), 
                           ("decgraphics",)),
            tuple(b"'0"): "ibmextras/zh-hant",
            tuple(b"'1"): "enyay",
            tuple(b"~"): "nil"}

g96bytes = {tuple(b"@"): "ir111",
            tuple(b"A"): "ir100",
            tuple(b"B"): ("ir101", ("ir101/overring",), ("ir101",)),
            tuple(b"C"): "ir109",
            tuple(b"D"): "ir110",
            tuple(b"E"): "ir123",
            tuple(b"F"): ("ir126/euro", ("ir126/euro",), ("ir126",)),
            tuple(b"G"): "ir127",
            tuple(b"H"): "ir138",
            tuple(b"I"): "ir139",
            tuple(b"J"): ("ir142+ir156", ("ir142+ir156",), ("ir142",)),
            tuple(b"K"): "ir143",
            tuple(b"L"): ("ir144", ("ir144/ukraine",), ("ir144",)),
            tuple(b"M"): "ir148",
            tuple(b"N"): "ir152",
            tuple(b"O"): "ir153",
            tuple(b"P"): "ir154",
            tuple(b"Q"): "ir155",
            tuple(b"R"): ("ir142+ir156", ("ir142+ir156",), ("ir156",)),
            tuple(b"S"): ("ir164", ("ir164/ibm",), ("ir164",)),
            tuple(b"T"): ("ir166", ("ir166/ibm", "ir166/ibm/euro"), ("ir166",)),
            tuple(b"U"): "ir167",
            tuple(b"V"): "ir157",
            # "W" exceptionally reserved for the ITU-T.101-B "Picture Description Instructions" set
            tuple(b"X"): "ir158",
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
            # "8": ITU-T.101-B "Display Control" set
            # "9": ITU-T.101-B "MVI" set (TODO what does "MVI" stand for?)
            tuple(b":"): ("user-defined/96", ("user-defined/96/web",), ("user-defined/96",)),
            tuple(b"!0"): "rfc1345-ir111", # Not even a private IRR: no practical compatibility.
            tuple(b"!1"): "t101c-mosaic1",
            tuple(b"!2"): "abicomp",
            tuple(b"!3"): ("ibmvietnamese/euro", ("ibmvietnamese/euro",), ("ibmvietnamese",)),
            tuple(b"!4"): "ibmlao",
            tuple(b"!5"): ("ibmestonian/euro", ("ibmestonian/euro",), ("ibmestonian",)),
            tuple(b"!6"): "lithuanian8",
            tuple(b"!7"): ("ibmarabic/euro", ("ibmarabic/euro",), ("ibmarabic",)),
            tuple(b"!8"): "ibmurdu",
            tuple(b"!9"): ("ibmaix-arabic/isoextended",
                           ("ibmaix-arabic/isoextended",),
                           ("ibmaix-arabic/base",)),
            tuple(b"!<"): ("ibmpc-arabic/base",
                           ("ibmpc-arabic/small", "ibmpc-arabic/tiny", "ibmpc-arabic/alternate", "ibmpc-arabic/alternate/small"),
                           ("ibmpc-arabic/base",)),
            tuple(b"\"1"): "nbytehangul/ext",
            tuple(b"\"?"): "decgreek8/nbsp",
            tuple(b"%0"): "decturkish8/nbsp",
            tuple(b"$7"): ("symbolgr/euro/numsp",
                           ("symbolgr/numsp",),
                           ("symbolgr/euro", "symbolgr/euro/numsp")),
            tuple(b"'0"): "ibmextras/zh-hans",
            tuple(b"~"): "nil"}

g94nbytes = {tuple(b"@"): ("ir042/nec", ("ir042/ibm", "ir042/nec", "ir042/1990pivot", "ir042/adobe"), ("ir042",)),
             tuple(b"A"): ("ir058/2022", # Preferred version
                           # Private versions
                           ("ir058/hant", "ir058/2000", "ir058/2005", "ir058/2022", "ir058/full",
                            "ir058/mac", "ir058/utc", "ir058/1986", "ir058/hant-strict",
                            "ir058/hant-utc", "ir058/ibm", "ir058/macraw", "ir058/macsemiraw",
                            "ir058/ms", "ir058/hant-full"),
                           ("ir058",)), # Original followed by any registered revisions
             tuple(b"B"): ("ir168/web",
                           ("ir168/web", "ir168/mac", "ir168/macps", "ir168/mackt6", "ir168/utc",
                            "ir168/osf", "ir168/osfa", "ir168/osfm", "ir168/ibm",
                            "ir168/docomo", "ir168/kddisym", "ir168/sbank", "ir168/kddipict",
                            "ir087/fujitsu", "ir168/arib", "ir168/mac-raw", "ir168/macps-raw"),
                           ("ir087", "ir168")),
             tuple(b"C"): ("ir149/unihan", ("ir149/altutc", "ir149/1998", "ir149/2002", "ir149/mac", "ir149/ibm", "ir149/mac-unicode2_1", "ir149/mac-unicode3_2", "ir149/unihan", "ir149/irgn2298feedback"), ("ir149",)),
             tuple(b"D"): ("ir159",
                           ("ir159/va", "ir159/osf", "ir159/osfa", "ir159/osfm", "ir159/ibm", "ir159/icueuc", "ir159/irgn2722"),
                           ("ir159",)),
             tuple(b"E"): ("ir165", ("ir165/swapg", "ir165/ext", "gb6345", "gb8565", "gb8565-oldwrongunihan", "gb15564"), ("ir165",)), # n.b. KS X 1002 seems to unilaterally usurp this one?
             tuple(b"F"): "ir169",
             tuple(b"G"): ("ir171/full",
                           ("ir171/full", "ir171/ms", "ir171/utc", "ir171/utcbig5", "ir171/mac", "ir171/govtw", "ir171/ibm", "ir171/ibm950", "ir171/ibm1373", "ir171/web", "ir171/1984moz", "ir171/icu", "ir171/icu-2014", "ir171/yasuoka", "ir171/hkscs2016"),
                           ("ir171",)),
             tuple(b"H"): ("ir172",
                           (None, "ir172/big5", None, None, None, "ir172/unihan", "ir172/hkscs2016"),
                           ("ir172",)),
             tuple(b"I"): ("ir183/full",
                           ("ir183/1988", "ir183/1988plus", "ir183/govtw", "ir183/full", "ir183/utc", "ir183/icu", "ir183/icu-2014", "ir183/yasuoka", "ir183/unihan"),
                           ("ir183",)),
             tuple(b"J"): ("ir184", ("ir184/govtw", "ir184/icu", "ir184/icu-2014", "ir184/yasuoka", "ir184/unihan"), ("ir184",)),
             tuple(b"K"): ("ir185", ("ir185/govtw", "ir185/icu", "ir185/icu-2014", "ir185/yasuoka", "ir185/unihan"), ("ir185",)),
             tuple(b"L"): ("ir186", ("ir186/govtw", "ir186/icu", "ir186/icu-2014", "ir186/yasuoka", "ir186/unihan"), ("ir186",)),
             tuple(b"M"): ("ir187", ("ir187/govtw", "ir187/icu", "ir187/icu-2014", "ir187/yasuoka", "ir187/unihan"), ("ir187",)),
             tuple(b"N"): ("ir202/full", ("ir202/2003", "ir202/2011", "ir202/full"), ("ir202",)),
             tuple(b"O"): "ir228",
             tuple(b"P"): "ir229",
             tuple(b"Q"): "ir233",
             tuple(b":"): "user-defined/6204",
             tuple(b"!0"): "gb12052",
             # Traditional Chinese off doing its own thing, as you do... no standard escapes here.
             tuple(b"!1"): ("cns-eucg2", ("cns-eucg2-icu-2014-full", "cns-eucg2-ms", "cns-eucg2-mac", "cns-eucg2-govtw", "cns-eucg2-icu-old", "cns-eucg2-ibm-full", "cns-eucg2-yasuoka", "cns-eucg2-icu-2014-noplane1", "cns-eucg2-ibm-noplane1", "cns-eucg2-unihan", "cns-eucg2-lax-matching"), ("cns-eucg2",)),
             tuple(b"!2"): ("hkscs-updated", ("ibmbig5exts", "etenextsplus"), ("ms950exts", "big5-2003-exts", "etenexts", "gccs", "hkscs1999", "hkscs2001", "hkscs2004", "hkscs", "hkscs-updated",)),
             tuple(b"!3"): ("ms950utcexts", (), ("utcbig5exts", "ms950utcexts")),
             # Shift_JIS extensions for IBM/Windows/HTML5 and for cellular emoji
             tuple(b"!4"): ("ibmsjisextpua", ("ibmsjisextold",), ("ibmsjisext", "ibmsjisextpua")),
             tuple(b"!5"): "docomosjisext",
             tuple(b"!6"): ("kddipictsjisext", ("kddisymsjisext",), ("kddipictsjisext",)),
             tuple(b"!7"): "sbanksjisext",
             # GB 7589/13131 and GB 7590/13132. Insofar as I can support them.
             tuple(b"!8"): ("gb13131", ("gb7589/gb13131-homologue", "gb13131", "gb7589", "gb13131/gb7589-homologue"), ("gb13131",)),
             tuple(b"!9"): ("gb13132", ("gb7590/gb13132-homologue", "gb13132", "gb7590", "gb13132/gb7590-homologue"), ("gb13132",)),
             tuple(b"!:"): ("mac-elex-extras", 
                            ("mac-elex-extras", "mac-elex-extras-unicode4_0", "mac-elex-extras-unicode2_1", "mac-elex-extras-adobe", "mac-elex-extras-nishiki-teki"),
                            ("mac-elex-extras-unicode3_2",)),
             tuple(b"!;"): "2011kpsextras",
             tuple(b"!<"): ("big5e-exts", (), ("big5e-exts",)),
             tuple(b"!="): "ksx1002",
             tuple(b"!>"): "ksx1027_1",
             tuple(b"!?"): "ksx1027_2",
             tuple(b"\"0"): ("aton-exts", ("aton-exts2", "chinasea-exts-core", "chinasea-exts-gothic"), ("aton-exts",)),
             tuple(b"\"1"): ("oldibmkorea", ("oldibmkorea-withcorppua",), ("oldibmkorea-excavated", "oldibmkorea")),
             tuple(b"\"2"): ("gb16500/ext", ("the-other-gb7", "gb16500"), ("gb16500/strict", "gb16500/ext")),
             tuple(b"\"3"): ("dynalabexts", (), ("dynalabexts",)),
             tuple(b"\"4"): ("monotypeexts", (), ("monotypeexts",)),
             tuple(b"\"5"): ("big5-plus-exts1", (), ("big5-plus-exts1",)),
             tuple(b"\"6"): ("big5-plus-exts2", (), ("big5-plus-exts2",)),
             tuple(b"\"7"): ("ibmbig5exts2", (), ("ibmbig5exts2",)),
             tuple(b"\"8"): ("sj11239", ("sj11239/babelstonehan",), ("sj11239",)),
             tuple(b"\"9"): ("japan-plane-3", (), ("japan-plane-3",)),
             tuple(b"\":"): ("tcvn5773", (), ("tcvn5773",)),
             tuple(b"\";"): ("tcvn6056", (), ("tcvn6056",)),
             tuple(b"\"<"): ("vhn01-row-minus-19", (), ("vhn01-row-minus-19",)),
             tuple(b"\"="): ("vhn02", (), ("vhn02",)),
             tuple(b"\">"): ("vhn03", (), ("vhn03",)),
             tuple(b"\"?"): ("ibm-euctw-extension-plane", (), ("ibm-euctw-extension-plane",)),
             tuple(b"#0"): ("csic8", ("csic8/govtw",), ("csic8",)),
             tuple(b"#1"): ("csic9", ("csic9/govtw",), ("csic9",)),
             tuple(b"#2"): ("csic10", (), ("csic10",)),
             tuple(b"#3"): ("csic11", ("csic11/govtw",), ("csic11",)),
             tuple(b"#4"): ("csic12", ("csic12/govtw",), ("csic12",)),
             tuple(b"#5"): ("csic13-2007", ("csic13-2007/govtw",), ("csic13-2007",)),
             tuple(b"#6"): ("csic14-2007", ("csic14-2007/govtw",), ("csic14-2007",)),
             tuple(b"#7"): ("csic15", ("csic15/govtw", "csic15/icu", "csic15/icu-2014", None, "csic15/unihan"), ("csic15",)),
             tuple(b"#9"): ("csic17", (), ("csic17",)),
             tuple(b"#;"): ("csic19", (), ("csic19",)),
             tuple(b"%0"): ("unihan-singapore-characters", (), ("unihan-singapore-characters",)),
             tuple(b"%1"): ("pseudo-tcvn6056", (), ("pseudo-tcvn6056",)),
             tuple(b"~"): "nil"}

g96nbytes = {tuple(b"!0"):("gbk-nonuro-extras-2022", ("gbk-nonuro-extras-web", "gbk-nonuro-extras-full", "gbk-nonuro-extras-2022"), ("gbk-nonuro-extras",)),
             tuple(b"!1"): ("cccii", ("cccii-koha", "eacc-hongkong", "cccii", "eacc",), ("eacc-pure",)),
             tuple(b"~"): "nil"}

sumps = {"94": g94bytes, "96": g96bytes, "94n": g94nbytes, "96n": g96nbytes}





