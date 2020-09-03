#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd

from ecma35.data import graphdata, variationhints
from ecma35.data.singlebyte import sbmapparsers as parsers

# ELOT 927, also DEC Greek (7-bit)
graphdata.gsets["ir088"] = (94, 1, tuple((i,) for i in range(0x21, 0x41)) + 
                                   tuple((i,) for i in range(0x0391, 0x039A)) + (None,) + 
                                   tuple((i,) for i in range(0x039A, 0x03A2)) + 
                                   tuple((i,) for i in range(0x03A3, 0x03A7)) + (None,) + 
                                   tuple((i,) for i in range(0x03A7, 0x03AA)) + 
                                   tuple((i,) for i in range(0x5B, 0x61)) + 
                                   tuple((i,) for i in range(0x03B1, 0x03BA)) + (None,) + 
                                   tuple((i,) for i in range(0x03BA, 0x03C2)) + 
                                   tuple((i,) for i in range(0x03C3, 0x03C7)) + ((0x03C2,),) + 
                                   tuple((i,) for i in range(0x03C7, 0x03CA)) + 
                                   tuple((i,) for i in range(0x7B, 0x7F)))

# ELOT-928 ECMA-118 ISO-8859-7:1987 Latin/Greek RHS
graphdata.gsets["ir126"] = (96, 1, (
         (0x00A0,), (0x2018,), (0x2019,), (0x00A3,), None,      None,      (0x00A6,), (0x00A7,), 
         (0x00A8,), (0x00A9,), None,      (0x00AB,), (0x00AC,), (0x00AD,), None,      (0x2015,), 
         (0x00B0,), (0x00B1,), (0x00B2,), (0x00B3,), (0x0384,), (0x0385,), (0x0386,), (0x00B7,), 
         (0x0388,), (0x0389,), (0x038A,), (0x00BB,), (0x038C,), (0x00BD,), (0x038E,), (0x038F,), 
         (0x0390,), (0x0391,), (0x0392,), (0x0393,), (0x0394,), (0x0395,), (0x0396,), (0x0397,), 
         (0x0398,), (0x0399,), (0x039A,), (0x039B,), (0x039C,), (0x039D,), (0x039E,), (0x039F,), 
         (0x03A0,), (0x03A1,), None,      (0x03A3,), (0x03A4,), (0x03A5,), (0x03A6,), (0x03A7,), 
         (0x03A8,), (0x03A9,), (0x03AA,), (0x03AB,), (0x03AC,), (0x03AD,), (0x03AE,), (0x03AF,), 
         (0x03B0,), (0x03B1,), (0x03B2,), (0x03B3,), (0x03B4,), (0x03B5,), (0x03B6,), (0x03B7,), 
         (0x03B8,), (0x03B9,), (0x03BA,), (0x03BB,), (0x03BC,), (0x03BD,), (0x03BE,), (0x03BF,), 
         (0x03C0,), (0x03C1,), (0x03C2,), (0x03C3,), (0x03C4,), (0x03C5,), (0x03C6,), (0x03C7,), 
         (0x03C8,), (0x03C9,), (0x03CA,), (0x03CB,), (0x03CC,), (0x03CD,), (0x03CE,), None))

# IEC-P27-1 supplementary technical set
graphdata.gsets["ir143"] = (96, 1, (
        (0x02C7,), (0x2261,), (0x2227,), (0x2228,), (0x2229,), (0x222A,), (0x2282,), (0x2283,), 
        (0x21D0,), (0x21D2,), (0x2234,), (0x2235,), (0x2208,), (0x220B,), (0x2286,), (0x2287,), 
        (0x222B,), (0x222E,), (0x221E,), (0x2207,), (0x2202,), (0x223C,), (0x2248,), (0x2243,), 
        (0x2245,), (0x2264,), (0x2260,), (0x2265,), (0x2194,), (0x00AC,), (0x2200,), (0x2203,), 
        (0x2135,), (0x25A1,), (0x2225,), (0x0393,), (0x0394,), (0x22A5,), (0x2220,), (0x221F,), 
        (0x0398,), (0x27E8,), (0x27E9,), (0x039B,), (0x2032,), (0x2033,), (0x039E,), (0x2213,), 
        (0x03A0,), (0x00B2,), (0x03A3,), (0x00D7,), (0x00B3,), (0x03A5,), (0x03A6,), (0x00B7,), 
        (0x03A8,), (0x03A9,), (0x2205,), (0x21C0,), (0x221A,), (0x0192,), (0x221D,), (0x00B1,), 
        (0x00B0,), (0x03B1,), (0x03B2,), (0x03B3,), (0x03B4,), (0x03B5,), (0x03B6,), (0x03B7,), 
        (0x03B8,), (0x03B9,), (0x03BA,), (0x03BB,), (0x03BC,), (0x03BD,), (0x03BE,), (0x2030,), 
        (0x03C0,), (0x03C1,), (0x03C3,), (0x00F7,), (0x03C4,), (0x03C5,), (0x03C6,), (0x03C7,), 
        (0x03C8,), (0x03C9,), (0x2020,), (0x2190,), (0x2191,), (0x2192,), (0x2193,), (0x203E,)))

# ISO-8859-7:2003 Latin/Greek RHS
graphdata.gsets["ir227"] = (96, 1, (
         (0x00A0,), (0x2018,), (0x2019,), (0x00A3,), (0x20AC,), (0x20AF,), (0x00A6,), (0x00A7,), 
         (0x00A8,), (0x00A9,), (0x037A,), (0x00AB,), (0x00AC,), (0x00AD,), None,      (0x2015,), 
         (0x00B0,), (0x00B1,), (0x00B2,), (0x00B3,), (0x0384,), (0x0385,), (0x0386,), (0x00B7,), 
         (0x0388,), (0x0389,), (0x038A,), (0x00BB,), (0x038C,), (0x00BD,), (0x038E,), (0x038F,), 
         (0x0390,), (0x0391,), (0x0392,), (0x0393,), (0x0394,), (0x0395,), (0x0396,), (0x0397,), 
         (0x0398,), (0x0399,), (0x039A,), (0x039B,), (0x039C,), (0x039D,), (0x039E,), (0x039F,), 
         (0x03A0,), (0x03A1,), None,      (0x03A3,), (0x03A4,), (0x03A5,), (0x03A6,), (0x03A7,), 
         (0x03A8,), (0x03A9,), (0x03AA,), (0x03AB,), (0x03AC,), (0x03AD,), (0x03AE,), (0x03AF,), 
         (0x03B0,), (0x03B1,), (0x03B2,), (0x03B3,), (0x03B4,), (0x03B5,), (0x03B6,), (0x03B7,), 
         (0x03B8,), (0x03B9,), (0x03BA,), (0x03BB,), (0x03BC,), (0x03BD,), (0x03BE,), (0x03BF,), 
         (0x03C0,), (0x03C1,), (0x03C2,), (0x03C3,), (0x03C4,), (0x03C5,), (0x03C6,), (0x03C7,), 
         (0x03C8,), (0x03C9,), (0x03CA,), (0x03CB,), (0x03CC,), (0x03CD,), (0x03CE,), None))

# Windows code page
graphdata.rhses["1253"] = parsers.read_single_byte("WHATWG/index-windows-1253.txt")

# OEM code pages
graphdata.rhses["737"] = parsers.read_single_byte("ICU/ibm-737_P100-1997.ucm")
graphdata.rhses["869"] = parsers.read_single_byte("ICU/ibm-869_P100-1995.ucm")

# Macintosh code page
graphdata.rhses["10006"] = graphdata.rhses["1280"] = parsers.read_mozilla_ut_file("Mozilla/macgreek.ut")

# TODO: ir018/19, Greek Teletext, 
# ir181 (Technical), ir055, ir031, ir050 (INIS Greek non-homoglyphs)

# Symbol (ibm-1038)
graphdata.gsets["symbolgl"] = (94, 1, parsers.read_single_byte("UTC/symbol.txt", typ="GL94"))
# TODO: symbolgl-swapphi
graphdata.gsets["symbolgr"] = (94, 1, parsers.read_single_byte("UTC/symbol.txt", typ="GR94", mapper=variationhints.ahmap))
graphdata.gsets["symbolgr-euro"] = (96, 1, parsers.read_single_byte("UTC/symbol.txt", typ="GR96", mapper=variationhints.ahmap))
graphdata.gsets["symbolgr-numsp"] = (96, 1, ((0x2007,),) + graphdata.gsets["symbolgr"] + (None,))








