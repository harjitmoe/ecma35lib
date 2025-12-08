#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019–2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

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

# Windows-1252 modification for Georgian, sometimes called the "GEORGIAN-ACADEMY" charset.
# The use of the code-page number 58596 for it is compatible with FreeDOS.
georgian_academy_charset = parsers.read_single_byte("Other/T1058596.ucm")
graphdata.gsets["georgian-academy/94"] = (94, 1, georgian_academy_charset[33:127])
graphdata.gsets["georgian-academy/96"] = (96, 1, georgian_academy_charset[32:])
graphdata.rhses["58596"] = georgian_academy_charset
graphdata.defgsets["58596"] = ("ir006", "georgian-academy/96", "nil", "nil")

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

# SPAchmim charset for Sahidic Coptic (modified Thesaurus Linguae Graecae)
graphdata.gsets["spachmim"] = (94, 1, (
               None,      (0x00A8,), None,      None,      None,      None,      None,
    None,      None,      None,      (0x00A8,), None,      (0x00AF,), None,      None,
    None,      (0x03E6,), (0x03ED,), (0x03E5,), (0x03E3,), (0x03EF,), (0x03E9,), (0x00A0,),
    (0x2CC9,), None,      None,      None,      None,      (0x03E7,), None,      (0x0323,),
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      (0x00AF,), None,      None,      (0x00AF,),
    (0x03EB,), (0x2C81,), (0x2C83,), (0x2C9D,), (0x2C87,), (0x2C89,), (0x2CAB,), (0x2C85,),
    (0x2C8F,), (0x2C93,), None,      (0x2C95,), (0x2C97,), (0x2C99,), (0x2C9B,), (0x2C9F,),
    (0x2CA1,), (0x2C91,), (0x2CA3,), (0x2CA5,), (0x2CA7,), (0x2CA9,), None,      (0x2CB1,),
    (0x2CAD,), (0x2CAF,), (0x2C8D,), None,      (0x2CEF,), None,      None))

# SPAchmim charset for Sahidic Coptic (modified Thesaurus Linguae Graecae) with extensions
#   adapted from the SPIonic Biblical Greek charset
graphdata.gsets["spachmim/ext"] = (94, 1, (
               None,      (0x00A8,), None,      None,      None,      None,      None,
    None,      None,      None,      (0x00A8,), None,      (0x00AF,), None,      None,
    None,      (0x03E6,), (0x03ED,), (0x03E5,), (0x03E3,), (0x03EF,), (0x03E9,), (0x00A0,),
    (0x2CC9,), None,      None,      None,      None,      (0x03E7,), None,      (0x0323,),
    (0x03EA,), (0x2C80,), (0x2C82,), (0x2C9C,), (0x2C86,), (0x2C88,), (0x2CAA,), (0x2C84,),
    (0x2C8E,), (0x2C92,), (0x03D8,), (0x2C94,), (0x2C96,), (0x2C98,), (0x2C9A,), (0x2C9E,),
    (0x2CA0,), (0x2C90,), (0x2CA2,), (0x2CA4,), (0x2CA6,), (0x2CA8,), (0x2C8A,), (0x2CB0,),
    (0x2CAC,), (0x2CAE,), (0x2C8C,), None,      (0x00AF,), None,      None,      (0x00AF,),
    (0x03EB,), (0x2C81,), (0x2C83,), (0x2C9D,), (0x2C87,), (0x2C89,), (0x2CAB,), (0x2C85,),
    (0x2C8F,), (0x2C93,), (0x03D9,), (0x2C95,), (0x2C97,), (0x2C99,), (0x2C9B,), (0x2C9F,),
    (0x2CA1,), (0x2C91,), (0x2CA3,), (0x2CA5,), (0x2CA7,), (0x2CA9,), (0x2C8B,), (0x2CB1,),
    (0x2CAD,), (0x2CAF,), (0x2C8D,), None,      (0x2CEF,), None,      None))

# "Bee" charset for the Deseret Alphabet.
graphdata.gsets["bee"] = (94, 1, (
                (0x0021,),  (0x0022,),  (0x10406,), (0x1042B,), (0x10403,), (0x10408,), (0x0027,),
    (0x0028,),  (0x0029,),  (0x10409,), (0x1040B,), (0x002C,),  (0x10432,), (0x002E,),  (0x10431,),
    (0x0030,),  (0x0031,),  (0x0032,),  (0x0033,),  (0x0034,),  (0x0035,),  (0x0036,),  (0x0037,),
    (0x0038,),  (0x0039,),  (0x1041B,), (0x10443,), (0x1044D,), (0x10433,), (0x10425,), (0x003F,),
    (0x1042E,), (0x10402,), (0x10412,), (0x10415,), (0x10414,), (0x10401,), (0x10419,), (0x10418,),
    (0x10410,), (0x10400,), (0x10416,), (0x10417,), (0x10422,), (0x10423,), (0x10424,), (0x10404,),
    (0x10411,), (0x1041F,), (0x10421,), (0x1041D,), (0x10413,), (0x10405,), (0x1041A,), (0x1040E,),
    (0x10420,), (0x1040F,), (0x1041E,), (0x10434,), (0x10444,), (0x10435,), (0x10430,), (0x1040A,),
    (0x1042F,), (0x1042A,), (0x1043A,), (0x1043D,), (0x1043C,), (0x10429,), (0x10441,), (0x10440,),
    (0x10438,), (0x10428,), (0x1043E,), (0x1043F,), (0x1044A,), (0x1044B,), (0x1044C,), (0x1042C,),
    (0x10439,), (0x10447,), (0x10449,), (0x10445,), (0x1043B,), (0x1042D,), (0x10442,), (0x10436,),
    (0x10448,), (0x10437,), (0x10446,), (0x1040C,), (0x1041C,), (0x1040D,), (0x10407,)))

# LaTeX "desalph" charset for the Deseret Alphabet.
graphdata.rhses["999904"] = (
    (0x10400,), (0x10401,), (0x10402,), (0x10403,), (0x10404,), (0x10405,), (0x10406,), (0x10407,),
    (0x10408,), (0x10409,), (0x1040A,), (0x1040B,), (0x1040C,), (0x1040D,), (0x1040E,), (0x1040F,),
    (0x10410,), (0x10411,), (0x10412,), (0x10413,), (0x10414,), (0x10415,), (0x10416,), (0x10417,),
    (0x10418,), (0x10419,), (0x1041A,), (0x1041B,), (0x1041C,), (0x1041D,), (0x1041E,), (0x1041F,),
    None,       None,       (0x10420,), None,       None,       None,       None,       (0x10421,),
    None,       None,       None,       (0x10422,), (0x10423,), None,       (0x10424,), (0x10425,),
    (0x10426,), (0x10427,), None,       None,       (0x10428,), None,       (0x10429,), (0x1042A,),
    (0x1042B,), (0x1042C,), (0x1042D,), (0x1042E,), (0x1042F,), (0x10430,), (0x10431,), (0x10432,),
    (0x10433,), (0x10434,), None,       None,       None,       None,       None,       None,
    None,       None,       None,       (0x10435,), (0x10436,), (0x10437,), (0x10438,), (0x10439,),
    None,       None,       None,       None,       None,       None,       None,       None,
    (0x1043A,), (0x1043B,), None,       None,       None,       None,       (0x1043C,), (0x1043D,),
    None,       None,       None,       None,       None,       (0x1043E,), (0x1043F,), (0x10440,),
    (0x10441,), (0x10442,), (0x10443,), (0x10444,), (0x10445,), (0x10446,), (0x10447,), (0x10448,),
    None,       (0x10449,), (0x1044A,), (0x1044B,), (0x1044C,), (0x1044D,), (0x1044E,), (0x1044F,),
    None,       None,       None,       None,       None,       None,       None,       None)
graphdata.defgsets["999904"] = ("alt646/knuth", "nil", "nil", "nil")

