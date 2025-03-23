#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019–2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# 7-bit APL
graphdata.gsets["ir068"] = (94, 1, parsers.read_single_byte("UTC/APL-ISO-IR-68.TXT", typ="GL94", filter_to_single=True))
graphdata.chcpdocs['371'] = 'ecma-35'
graphdata.defgsets['371'] = ('ir068', 'nil', 'nil', 'nil')

# I.S. 434 Latin/Ogham RHS
# Registered as a 96-set for some reason but doesn't actually allocate the corners.
graphdata.gsets["ir208"] = (96, 1, 
             ((None,) * 64) + tuple((i,) for i in range(0x1680, 0x169D)) + (None, None, None))
graphdata.gsets["ir208/94"] = (94, 1, graphdata.gsets["ir208"][2][1:-1])

# ISO-10585:1996 Armenian
# Not assigned an escape, but given the number here (possibly provisionally, but any new escape or
#   IR number being assigned in the future seems unlikely since ISO-IR is basically legacy now):
#   https://www.evertype.com/standards/iso10646/pdf/iso-10585.pdf
graphdata.gsets["ir221"] = (94, 1, (
               (0x0531,), (0x0532,), (0x0533,), (0x0534,), (0x0535,), (0x0536,), (0x0537,),
    (0x0538,), (0x0539,), (0x053A,), (0x053B,), (0x053C,), (0x053D,), (0x053E,), (0x053F,),
    (0x0540,), (0x0541,), (0x0542,), (0x0543,), (0x0544,), (0x0545,), (0x0546,), (0x0547,),
    (0x0548,), (0x0549,), (0x054A,), (0x054B,), (0x054C,), (0x054D,), (0x054E,), (0x054F,),
    (0x0550,), (0x0551,), (0x0552,), (0x0553,), (0x0554,), (0x0555,), (0x0556,), None,     
    (0x055D,), (0x055A,), (0x058A,), None,      (0x0589,), (0x002C,), (0x055E,), (0x055F,),
    None,      (0x0561,), (0x0562,), (0x0563,), (0x0564,), (0x0565,), (0x0566,), (0x0567,),
    (0x0568,), (0x0569,), (0x056A,), (0x056B,), (0x056C,), (0x056D,), (0x056E,), (0x056F,),
    (0x0570,), (0x0571,), (0x0572,), (0x0573,), (0x0574,), (0x0575,), (0x0576,), (0x0577,),
    (0x0578,), (0x0579,), (0x057A,), (0x057B,), (0x057C,), (0x057D,), (0x057E,), (0x057F,),
    (0x0580,), (0x0581,), (0x0582,), (0x0583,), (0x0584,), (0x0585,), (0x0586,), None,     
    (0x2015,), (0x2010,), (0x0022,), None,      (0x0387,), (0x055B,), (0x055C,),
))

# Armenian Standard AST 34.002 ("ArmSCII"); FreeDOS code page 65506
graphdata.gsets["armscii"] = (94, 1, ((1421,), (1415,), (1417,), (41,), (40,), (187,), (171,), (8212,), (8228,), (1373,), (44,), (173,), (1418,), (8230,), (1372,), (1371,), (1374,), (1329,), (1377,), (1330,), (1378,), (1331,), (1379,), (1332,), (1380,), (1333,), (1381,), (1334,), (1382,), (1335,), (1383,), (1336,), (1384,), (1337,), (1385,), (1338,), (1386,), (1339,), (1387,), (1340,), (1388,), (1341,), (1389,), (1342,), (1390,), (1343,), (1391,), (1344,), (1392,), (1345,), (1393,), (1346,), (1394,), (1347,), (1395,), (1348,), (1396,), (1349,), (1397,), (1350,), (1398,), (1351,), (1399,), (1352,), (1400,), (1353,), (1401,), (1354,), (1402,), (1355,), (1403,), (1356,), (1404,), (1357,), (1405,), (1358,), (1406,), (1359,), (1407,), (1360,), (1408,), (1361,), (1409,), (1362,), (1410,), (1363,), (1411,), (1364,), (1412,), (1365,), (1413,), (1366,), (1414,), (1370,)))

graphdata.chcpdocs['65506'] = 'ecma-35'
graphdata.defgsets['65506'] = ('ir006', 'armscii', 'nil', 'nil')

# OEM code page for Armenian; FreeDOS code page 899 (but unrelated to IBM code page 899)
graphdata.rhses["?899"] = parsers.read_single_byte("Other/DOS00899.ucm")
graphdata.defgsets["?899"] = ("alt646/freedos-armenian", "pclinedrawing", "nil", "nil")

# ISO-10586:1996 Georgian
# Not assigned an escape, but given the number here (possibly provisionally, but any new escape or
#   IR number being assigned in the future seems unlikely since ISO-IR is basically legacy now):
#   https://www.evertype.com/standards/iso10646/pdf/iso-10586.pdf
graphdata.gsets["ir222"] = (94, 1, (
               None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      (0x0589,), (0x0387,), (0x10FB,),
    (0x10D0,), (0x10D1,), (0x10D2,), (0x10D3,), (0x10D4,), (0x10D5,), (0x10D6,), (0x10F1,),
    (0x10D7,), (0x10D8,), (0x10D9,), (0x10DA,), (0x10DB,), (0x10DC,), (0x10F2,), (0x10DD,),
    (0x10DE,), (0x10DF,), (0x10E0,), (0x10E1,), (0x10E2,), (0x10E3,), (0x10F3,), (0x10E4,),
    (0x10E5,), (0x10E6,), (0x10E7,), (0x10E8,), (0x10E9,), (0x10EA,), (0x10EB,), (0x10EC,),
    (0x10ED,), (0x10EE,), (0x10F4,), (0x10EF,), (0x10F0,), (0x10F5,), (0x10F6,), None,      
    None,      None,      None,      None,      None,      None,      None,
))

# Windows-1252 modification for Georgian
graphdata.rhses["58596"] = parsers.read_single_byte("Other/T1058596.ucm")

# OEM code page for unicameral Georgian
graphdata.rhses["59829"] = parsers.read_single_byte("Other/T1059829.ucm")

# OEM code page for bicameral Georgian
graphdata.rhses["60853"] = parsers.read_single_byte("Other/T1060853.ucm")

# KS C 5601's alternative "N-byte Hangul Code" (IBM code page 891)
graphdata.gsets["nbytehangul"] = (94, 1, (
               None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    (0xFFA0,), (0xFFA1,), (0xFFA2,), (0xFFA3,), (0xFFA4,), (0xFFA5,), (0xFFA6,), (0xFFA7,),
    (0xFFA8,), (0xFFA9,), (0xFFAA,), (0xFFAB,), (0xFFAC,), (0xFFAD,), (0xFFAE,), (0xFFAF,),
    (0xFFB0,), (0xFFB1,), (0xFFB2,), (0xFFB3,), (0xFFB4,), (0xFFB5,), (0xFFB6,), (0xFFB7,),
    (0xFFB8,), (0xFFB9,), (0xFFBA,), (0xFFBB,), (0xFFBC,), (0xFFBD,), (0xFFBE,), None,
    None,      None,      (0xFFC2,), (0xFFC3,), (0xFFC4,), (0xFFC5,), (0xFFC6,), (0xFFC7,),
    None,      None,      (0xFFCA,), (0xFFCB,), (0xFFCC,), (0xFFCD,), (0xFFCE,), (0xFFCF,),
    None,      None,      (0xFFD2,), (0xFFD3,), (0xFFD4,), (0xFFD5,), (0xFFD6,), (0xFFD7,),
    None,      None,      (0xFFDA,), (0xFFDB,), (0xFFDC,), None,      None))
graphdata.rhses["25467"] = ((None,) * 33) + graphdata.gsets["nbytehangul"][2] + (None,)
graphdata.chcpdocs["891"] = "ecma-35"
graphdata.defgsets["891"] = graphdata.defgsets["25467"] = ("alt646/ksroman", "nbytehangul", "nil", "nil")

graphdata.gsets["nbytehangul/ext"] = (96, 1, (
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    (0xFFA0,), (0xFFA1,), (0xFFA2,), (0xFFA3,), (0xFFA4,), (0xFFA5,), (0xFFA6,), (0xFFA7,),
    (0xFFA8,), (0xFFA9,), (0xFFAA,), (0xFFAB,), (0xFFAC,), (0xFFAD,), (0xFFAE,), (0xFFAF,),
    (0xFFB0,), (0xFFB1,), (0xFFB2,), (0xFFB3,), (0xFFB4,), (0xFFB5,), (0xFFB6,), (0xFFB7,),
    (0xFFB8,), (0xFFB9,), (0xFFBA,), (0xFFBB,), (0xFFBC,), (0xFFBD,), (0xFFBE,), (0x00A6,),
    None,      None,      (0xFFC2,), (0xFFC3,), (0xFFC4,), (0xFFC5,), (0xFFC6,), (0xFFC7,),
    None,      None,      (0xFFCA,), (0xFFCB,), (0xFFCC,), (0xFFCD,), (0xFFCE,), (0xFFCF,),
    None,      None,      (0xFFD2,), (0xFFD3,), (0xFFD4,), (0xFFD5,), (0xFFD6,), (0xFFD7,),
    None,      None,      (0xFFDA,), (0xFFDB,), (0xFFDC,), (0x00AC,), (0x005C,), (0x007E,)))
graphdata.rhses["1040"] = graphdata.rhses["29712"] = ((0x00A2,),) + ((None,) * 31) + graphdata.gsets["nbytehangul/ext"][2]
graphdata.defgsets["1040"] = graphdata.defgsets["29712"] = ("alt646/ksroman", "nbytehangul/ext", "nil", "nil")

# ISO 6826-A (mathematical symbols)
graphdata.gsets["ir217"] = (94, 1, ((0x0338,), (0x20D2,), (0x20D3,), (0x0335,), (0x20D8,), (0x20DA,), (0x20D9,), (0x20D4,), (0x0307,), (0x0308,), (0x20D6,), (0x0302,), (0x030C,), (0x20D7,), (0x20D5,), (0x00D7,), (0x00B1,), (0x223C,), (0x2248,), (0x2261,), (0x2264,), (0x2276,), (0x2272,), (0x226A,), (0x2225,), (0x221F,), (0x2206,), (0x00B0,), (0x27E8,), (0x27E6,), (0x2211,), (0x00F7,), (0x2213,), (0x2243,), (0x2245,), (0x224F,), (0x2265,), (0x2277,), (0x2273,), (0x226B,), (0x22A5,), (0x2220,), (0x2207,), (0x2030,), (0x27E9,), (0x27E7,), (0x220F,), (0x002B,), (0x2282,), (0x2286,), (0x2208,), (0x222A,), (0x2200,), (0x2201,), (0x2191,), (0x2190,), (0x21B6,), (0x2194,), (0x21C6,), (0x21A6,), (0x21D1,), (0x21D0,), (0x221E,), (0x2212,), (0x2283,), (0x2287,), (0x220B,), (0x2229,), (0x2203,), (0x2205,), (0x2193,), (0x2192,), (0x21B7,), (0x2195,), (0x21C4,), (0x21C5,), (0x21D3,), (0x21D2,), (0x221A,), (0x2032,), (0x2033,), (0x2034,), (0x2228,), (0x2227,), (0x00AC,), (0x210E,), (0x22A2,), (0x222B,), (0x222C,), (0x222D,), (0x2202,), (0x210F,), (0x2135,), (0x2218,)))

# ISO 6826-B (mathematical symbols)
graphdata.gsets["ir218"] = (94, 1, ((0x2295,), (0x2296,), (0x2297,), (0x2299,), (0x2234,), (0x2235,), (0x228F,), (0x2290,), (0x22B7,), (0x22B6,), (0x22B9,), (0x2214,), (0x223E,), (0x223B,), (0x22B0,), (0x2260,), (0x2253,), (0x27EC,), (0x230A,), (0x22EE,), (0x2308,), (0x2291,), (0x2294,), (0x22B2,), (0x227F,), (0x227A,), (0x227C,), (0x2238,), (0x2258,), (0x25C3,), (0x25B5,), (0x2243,), (0x2237,), (0x27ED,), (0x230B,), (0x224E,), (0x2309,), (0x2292,), (0x2293,), (0x22B4,), (0x227E,), (0x227B,), (0x227D,), (0x2250,), (0x225A,), (0x25B9,), (0x25BF,), (0x2016,), (0x2215,), (0x22A4,), (0x22C1,), (0x22C3,), (0x2E26,), (0x220A,), (0x2196,), (0x2199,), (0x21BE,), (0x219B,), (0x21AA,), (0x25CB,), (0x25A1,), (0x25AD,), (0x25CA,), (0x2223,), (0x29F5,), (0x2216,), (0x22C0,), (0x22C2,), (0x2E27,), (0x220D,), (0x2197,), (0x2198,), (0x21DD,), (0x21A0,), (0x21A9,), (0x25CF,), (0x25A0,), (0x25B1,), (0x2222,), (0x2252,), (0x223A,), (0x221D,), (0x2307,), (0x22A8,), (0x22A6,), (0x2226,), (0x2224,), (0x219A,), (0x21DC,), (0x21D4,), (0x21D5,), (0x2129,), (0x2118,), (0x211E,)))

# DOS code page for IBM Symbols Set 7 (mostly mathematical symbols)
graphdata.rhses["899"] = parsers.read_single_byte("Other/T1000899.ucm")
graphdata.defgsets["899"] = ("ibmsymbol", "pclinedrawing", "nil", "nil")
graphdata.rhses["1092"] = parsers.read_single_byte("Other/T1001092.ucm")
graphdata.defgsets["1092"] = ("ibmsymbol", "pclinedrawing", "nil", "nil")


