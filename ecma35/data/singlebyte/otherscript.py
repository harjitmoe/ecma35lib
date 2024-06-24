#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019–2024.

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

