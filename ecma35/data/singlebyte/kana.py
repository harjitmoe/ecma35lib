#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019–2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers


# Hankaku Katakana
# Windows mappings:
#       0x80   0xA0   0xFD   0xFE   0xFF
# SJIS U+0080 U+F8F0 U+F8F1 U+F8F2 U+F8F3
# GBK  U+20AC (lead) (lead) (lead) U+F8F5 (U+20AC = €)
# UHC  U+0080 (lead) (lead) (lead) U+F8F7
# Big5 U+0080 (lead) (lead) (lead) U+F8F8
#
# Apple usage (editorial errors in comment blurb 2(second a) of CHINSIMP.TXT notwithstanding):
#       0x80   0x81   0x82   0x83   0x84   0xA0   0xFD   0xFE   0xFF
# SJIS   \    (lead) (lead) (lead) (lead)  NBSP    ©      ™      …
# Big5   \     HMC    WMC   (none) (none)  NBSP    ©      ™      …
# GB     ü     HMC    WMC   (none) (none)  NBSP    ©      ™      …   
# Elex  NBSP   Won   NDASH    ©     FW _  (none) (lead) (lead)   …    
#
# Note that HangulTalk's use of 0x80 and 0x84 is not documented by Lunde. 
#
# IBM usage:
#       0x80   0x81   0x82   0x83   0x84   0xA0   0xFD   0xFE   0xFF
# SJIS   ¢    (lead) (lead) (lead) (lead)   £      ¬      \      ~
# KSC    ¢      ¬      \     Ovln    ¦    (lead) (lead) (lead) (none)
# 
# Projected EUC mappings (SJIS from IBM's 1041 to 4992, rest extrapolated):
#          0x80   0x81   0x82   0x83   0x84   0xA0   0xFD   0xFE   0xFF
# SJIS    0x8EE0 (lead) (lead) (lead) (lead) 0x8EE1 0x8EE2 0x8EE3 0x8EE4
# MacBig5 0x8EE0 0x8EE6 0x8EE7 (none) (none) 0x8EE1 0x8EE2 0x8EE3 0x8EE4
# MacGB   0x8EE5 0x8EE6 0x8EE7 (none) (none) 0x8EE1 0x8EE2 0x8EE3 0x8EE4
# GBK     0x8EE0 (lead) (lead) (lead) (lead) (lead) (lead) (lead) 0x8EE6
# UHC     0x8EE0 (lead) (lead) (lead) (lead) (lead) (lead) (lead) 0x8EE8
# Big5    0x8EE0 (lead) (lead) (lead) (lead) (lead) (lead) (lead) 0x8EE9
# IBMKSC  0x8EE0 0x8EE2 0x8EE3 0x8EE5 0x8EE6 (lead) (lead) (lead) 0x8EE9
# Elex    0x8EE1 0x8EE8 0x8EE9 0x8EE2 0x8EEA 0x8EEB (lead) (lead) 0x8EE4
#
# Therefore:
# EUC  0x8EE0 0x8EE1 0x8EE2 0x8EE3 0x8EE4 0x8EE5 0x8EE6 0x8EE7 0x8EE8 0x8EE9 0x8EEA
# MS   0x80/€ U+F8F0 U+F8F1 U+F8F2 U+F8F3 U+F8F4 U+F8F5 U+F8F6 U+F8F7 U+F8F8 (none)
# Mac    \     NBSP    ©      ™      …      ü     HMC    WMC    Won   NDASH   FW _ 
# IBM    ¢      £      ¬      \      ~     Ovln    ¦    (none) (none) (none) (none)
#
# Sadly, since I'm already using EUC-TW's unused G3 set for the corporate regions,
# I can't use this mechanism for Big5, at least for the time being.

# JIS C 6220 / JIS X 0201 Katakana set
_the_mother = tuple((i,) for i in range(0xFF61, 0xFFA0))
graphdata.gsets["ir013"] = (94, 1, _the_mother + ((None,) * 31))
graphdata.chcpdocs['896'] = 'ecma-35'
graphdata.defgsets['896'] = ('ir013', 'nil', 'nil', 'nil')
graphdata.chcpdocs['1139'] = 'ecma-35'
graphdata.defgsets['1139'] = ('ir014', 'ir013', 'nil', 'nil')
graphdata.rhses["897"] = ((None,) * 33) + _the_mother + ((None,) * 32)
graphdata.defgsets["897"] = ("ir014", "ir013", "nil", "nil")
graphdata.chcpdocs['1086'] = 'ecma-35'
graphdata.defgsets['1086'] = ('ir014', 'ir013', 'nil', 'nil')
graphdata.chcpdocs['4993'] = 'ecma-35'
graphdata.defgsets['4993'] = ('ir094/ibm', 'ir013', 'nil', 'nil')
graphdata.chcpdocs['13185'] = 'ecma-35'
graphdata.defgsets['13185'] = ('ir014', 'ir013', 'nil', 'nil')
graphdata.chcpdocs['62337'] = 'ecma-35'
graphdata.defgsets['62337'] = ('ir014', 'ir013', 'nil', 'nil')
# IBM's 4992 (or unrestricted 896), plus further additions as explained above
graphdata.gsets["ir013/ibm"] = (94, 1, _the_mother + (
                (0xA2,), (0xA3,), (0xAC,), (0x5C,), (0x7E,), (0x203E,), (0xA6,)) + ((None,) * 24))
# IBM's 4992 (or unrestricted 896) only
graphdata.gsets["ir013/ibm/strict"] = (94, 1, _the_mother + (
                (0xA2,), (0xA3,), (0xAC,), (0x5C,), (0x7E,)) + ((None,) * 26))
graphdata.chcpdocs['4992'] = 'ecma-35'
graphdata.defgsets['4992'] = ('ir013/ibm/strict', 'nil', 'nil', 'nil')
# RHS of IBM's code page 911
graphdata.gsets["ir013/ibm/alternate"] = (94, 1, _the_mother + (
                None, (0xA3,), (0xA2,), (0xAC,)) + ((None,) * 27))
graphdata.chcpdocs['911'] = 'ecma-35'
graphdata.defgsets['911'] = ('ir014', 'ir013/ibm/alternate', 'nil', 'nil')
# 1-byte MacJapanese
graphdata.gsets["ir013/mac"] = (94, 1, _the_mother + (
                (0x5C,), (0xA0,), (0xA9,), (0x2122,), (0x2026,), 
                (0xFC,), (0xF880,), (0xF881,), (0x20A9,), (0x2013,), (0xFF3F,)) + ((None,) * 20))
# For Windows code pages
graphdata.gsets["ir013/win"] = (94, 1, _the_mother + (
                (0x20AC,),) + tuple((i,) for i in range(0xF8F0, 0xF8F9)) + ((None,) * 21))
graphdata.gsetflags["ir013/win"] |= {"GBK:NO_EURO"}
graphdata.gsets["ir013/euro"] = graphdata.gsets["ir013/win"]

# Hiragana homologue to JIS C 6220 / JIS X 0201 (dubbed simply "Hiragana" by Adobe-Japan1)
graphdata.gsets["ir013/hiragana"] = _hiragana = (94, 1, (
             (0xFF61,), (0xFF62,), (0xFF63,), (0xFF64,), (0xFF65,), (0x3092,), (0x3041,),
  (0x3043,), (0x3045,), (0x3047,), (0x3049,), (0x3083,), (0x3085,), (0x3087,), (0x3063,),
  (0xFF70,), (0x3042,), (0x3044,), (0x3046,), (0x3048,), (0x304A,), (0x304B,), (0x304D,),
  (0x304F,), (0x3051,), (0x3053,), (0x3055,), (0x3057,), (0x3059,), (0x305B,), (0x305D,),
  (0x305F,), (0x3061,), (0x3064,), (0x3066,), (0x3068,), (0x306A,), (0x306B,), (0x306C,),
  (0x306D,), (0x306E,), (0x306F,), (0x3072,), (0x3075,), (0x3078,), (0x307B,), (0x307E,),
  (0x307F,), (0x3080,), (0x3081,), (0x3082,), (0x3084,), (0x3086,), (0x3088,), (0x3089,),
  (0x308A,), (0x308B,), (0x308C,), (0x308D,), (0x308F,), (0x3093,), (0xFF9E,), (0xFF9F,),
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None))
graphdata.chcpdocs["994001"] = "ecma-35"
graphdata.defgsets["994001"] = ("ir014", "ir013/hiragana", "nil", "nil")

graphdata.chcpdocs["994002"] = "ecma-35"
graphdata.defgsets["994002"] = ("ir014", "ir013", "nil", "nil")

# The charset dubbed "Hankaku" by Adobe-Japan1: an extension of 8-bit JIS X 0201 adding Hiragana
_hiragana_table = parsers.derive_supplementary_cid_mapping(
    "../../multibyte/mbmaps/Adobe/AdobeJapan.txt",
    "Hiragana", _hiragana[2], "GL94")
graphdata.rhses["994003"] = parsers.read_single_byte(
    "../../multibyte/mbmaps/Adobe/AdobeJapan.txt",
    typ = "plainext",
    cidmap = ("Hankaku", "UniJIS-UTF32"),
    cidmap_extra = _hiragana_table)

# ARIB STD-B24 Volume 1, single-byte Hiragana
graphdata.gsets["aribkana/hiragana"] = (94, 1, tuple((i,) if i else None for i in
            tuple(range(0x3041, 0x3094)) +
            (None, None, None, 0x309D, 0x309E, 0x30FC, 0x3002, 0x300C, 0x300D, 0x3001, 0x30FB)))

# ARIB STD-B24 Volume 1, single-byte non-JISX0201 Katakana
graphdata.gsets["aribkana/katakana"] = (94, 1, tuple((i,) if i else None for i in
            tuple(range(0x30A1, 0x30F7)) +
            (0x30FD, 0x30FE, 0x30FC, 0x3002, 0x300C, 0x300D, 0x3001, 0x30FB)))

# JIS X 9010 Kana set for JIS X 9008 font (which supports large katakana only)
graphdata.gsets["ir096"] = (94, 1, (None,) + _the_mother[1:3] + (None, None) + _the_mother[5:6] + (None,)*9 + _the_mother[15:] + (None,)*31)

graphdata.gsets["ir013/ibm/sjis"] = (94, 1, _the_mother + (None,) * 29 + ((0x00AC,), (0x005C,)))
graphdata.defgsets["1041"] = graphdata.defgsets["5137"] = graphdata.defgsets["29713"] = graphdata.defgsets["54289"] = ("ir014", "ir013/ibm/sjis", "nil", "nil")
graphdata.rhses["1041"] = graphdata.rhses["5137"] = graphdata.rhses["29713"] = graphdata.rhses["54289"] = ((0x00A2,),) + ((None,) * 31) + ((0x00A3,),) + graphdata.gsets["ir013/ibm/sjis"][2] + ((0x007E,),)

