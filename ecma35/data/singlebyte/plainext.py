#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

graphdata.c0graphics["437"] = (None, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022, 0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C, 0x25BA, 0x25C4, 0x2195, 0x203C, 0xB6, 0xA7, 0x25AC, 0x21A8, 0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC, 0x2302)
graphdata.c0graphics["904"] = (None, 0x2554, 0x2557, 0x255A, 0x255D, 0x2551, 0x2550, 0xFFEC, None, 0xFFEE, None, 0x303F, None, None, 0xFFED, 0x263C, 0x256C, None, 0x2195, None, 0x2593, 0x2569, 0x2566, 0x2563, None, 0x2560, 0x2591, 0x21B5, 0xFFEA, 0xFFE8, 0xFFEB, 0xFFE9, None)

# Windows-125x pages
graphdata.rhses["1250"] = parsers.read_single_byte("index-windows-1250.txt")
graphdata.rhses["1251"] = parsers.read_single_byte("index-windows-1251.txt")
graphdata.rhses["1252"] = parsers.read_single_byte("index-windows-1252.txt") # ISO-8859-1 ext.
graphdata.rhses["1253"] = parsers.read_single_byte("index-windows-1253.txt")
graphdata.rhses["1254"] = parsers.read_single_byte("index-windows-1254.txt") # ISO-8859-9 ext.
graphdata.rhses["1255"] = parsers.read_single_byte("index-windows-1255.txt")
graphdata.rhses["1256"] = parsers.read_single_byte("index-windows-1256.txt")
graphdata.rhses["1257"] = parsers.read_single_byte("index-windows-1257.txt")
graphdata.rhses["1258"] = parsers.read_single_byte("index-windows-1258.txt")

# OEM pages
graphdata.rhses["437"] = parsers.read_single_byte("ibm-437_P100-1995.ucm")
graphdata.rhses["720"] = parsers.read_single_byte("ibm-720_P100-1997.ucm")
graphdata.rhses["737"] = parsers.read_single_byte("ibm-737_P100-1997.ucm")
graphdata.rhses["775"] = parsers.read_single_byte("ibm-775_P100-1996.ucm")
graphdata.rhses["850"] = parsers.read_single_byte("ibm-850_P100-1995.ucm")
graphdata.rhses["852"] = parsers.read_single_byte("ibm-852_P100-1995.ucm")
graphdata.rhses["855"] = parsers.read_single_byte("ibm-855_P100-1995.ucm")
graphdata.rhses["857"] = parsers.read_single_byte("ibm-857_P100-1995.ucm")
graphdata.rhses["858"] = parsers.read_single_byte("ibm-858_P100-1997.ucm")
graphdata.rhses["860"] = parsers.read_single_byte("ibm-860_P100-1995.ucm")
graphdata.rhses["861"] = parsers.read_single_byte("ibm-861_P100-1995.ucm")
graphdata.rhses["862"] = parsers.read_single_byte("ibm-862_P100-1995.ucm")
graphdata.rhses["863"] = parsers.read_single_byte("ibm-863_P100-1995.ucm")
graphdata.rhses["864"] = parsers.read_single_byte("ibm-864_X110-1999.ucm")
graphdata.rhses["865"] = parsers.read_single_byte("ibm-865_P100-1995.ucm")
graphdata.rhses["866"] = parsers.read_single_byte("index-ibm866.txt")
graphdata.rhses["869"] = parsers.read_single_byte("ibm-869_P100-1995.ucm")
graphdata.rhses["904"] = (None,) * 128

# Code pages 874 (ISO-8859-11 exts)
# Per alias comments in ICU's convrtrs.txt, IBM's 874 is identical to IBM's 9066.
# Microsoft's 874, on the other hand, matches the layout of IBM's 1162.
graphdata.rhses["1162"] = parsers.read_single_byte("index-windows-874.txt")
graphdata.rhses["9066"] = parsers.read_single_byte("ibm-874_P100-1995.ucm")
# Since the two extensions collide in neither repertoire nor allocations, use both for "874":
graphdata.rhses["874"] = tuple(a or b for a, b in zip(graphdata.rhses["1162"],
                                                      graphdata.rhses["9066"]))

# Macintosh pages
graphdata.rhses["10000"] = parsers.read_single_byte("index-macintosh.txt")
# 10007 is the original MacCyrillic; current MacCyrillic is a Euro update of 10017.
graphdata.rhses["10017"] = parsers.read_single_byte("index-x-mac-cyrillic.txt")

# KOI-8 encodings
graphdata.rhses["878"] = graphdata.rhses["20866"] = parsers.read_single_byte("index-koi8-r.txt")
# Note: 21866 is used for both KOI8-U and KOI8-RU.
graphdata.rhses["1168"] = graphdata.rhses["21866"] = parsers.read_single_byte("index-koi8-u.txt")





