#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019–2026.

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

# A hiragana/katakana encoding sometimes used on GBA consoles
graphdata.lhses["993300"] = (
    None,      (0x3042,), (0x3044,), (0x3046,), (0x3048,), (0x304A,), (0x304B,), (0x304D,),
    (0x304F,), (0x3051,), (0x3053,), (0x3055,), (0x3057,), (0x3059,), (0x305B,), (0x305D,),
    (0x305F,), (0x3061,), (0x3064,), (0x3066,), (0x3068,), (0x306A,), (0x306B,), (0x306C,),
    (0x306D,), (0x306E,), (0x306F,), (0x3072,), (0x3075,), (0x3078,), (0x307B,), (0x307E,),
    (0x307F,), (0x3080,), (0x3081,), (0x3082,), (0x3084,), (0x3086,), (0x3088,), (0x3089,),
    (0x308A,), (0x308B,), (0x308C,), (0x308D,), (0x308F,), (0x3092,), (0x3093,), (0x3041,),
    (0x3043,), (0x3045,), (0x3047,), (0x3049,), (0x3083,), (0x3085,), (0x3087,), (0x304C,),
    (0x304E,), (0x3050,), (0x3052,), (0x3054,), (0x3056,), (0x3058,), (0x305A,), (0x305C,),
    (0x305E,), (0x3060,), (0x3062,), (0x3065,), (0x3067,), (0x3069,), (0x3070,), (0x3073,),
    (0x3076,), (0x3079,), (0x307C,), (0x3071,), (0x3074,), (0x3077,), (0x307A,), (0x307D,),
    (0x3063,), (0x30A2,), (0x30A4,), (0x30A6,), (0x30A8,), (0x30AA,), (0x30AB,), (0x30AD,),
    (0x30AF,), (0x30B1,), (0x30B3,), (0x30B5,), (0x30B7,), (0x30B9,), (0x30BB,), (0x30BD,),
    (0x30BF,), (0x30C1,), (0x30C4,), (0x30C6,), (0x30C8,), (0x30CA,), (0x30CB,), (0x30CC,),
    (0x30CD,), (0x30CE,), (0x30CF,), (0x30D2,), (0x30D5,), (0x30D8,), (0x30DB,), (0x30DE,),
    (0x30DF,), (0x30E0,), (0x30E1,), (0x30E2,), (0x30E4,), (0x30E6,), (0x30E8,), (0x30E9,),
    (0x30EA,), (0x30EB,), (0x30EC,), (0x30ED,), (0x30EF,), (0x30F2,), (0x30F3,), (0x30A1,))
graphdata.rhses["993300"] = (
    (0x30A3,), (0x30A5,), (0x30A7,), (0x30A9,), (0x30E3,), (0x30E5,), (0x30E7,), (0x30AC,),
    (0x30AE,), (0x30B0,), (0x30B2,), (0x30B4,), (0x30B6,), (0x30B8,), (0x30BA,), (0x30BC,),
    (0x30BE,), (0x30C0,), (0x30C2,), (0x30C5,), (0x30C7,), (0x30C9,), (0x30D0,), (0x30D3,),
    (0x30D6,), (0x30D9,), (0x30DC,), (0x30D1,), (0x30D4,), (0x30D7,), (0x30DA,), (0x30DD,),
    (0x30C3,), (0x0030,), (0x0031,), (0x0032,), (0x0033,), (0x0034,), (0x0035,), (0x0036,),
    (0x0037,), (0x0038,), (0x0039,), (0x0021,), (0x003F,), (0x3002,), (0x002D,), (0x30FB,),
    (0x2026,), (0x300E,), (0x300F,), (0x300C,), (0x300D,), (0x2642,), (0x2640,), (0x5186,),
    (0x002E,), (0x00D7,), (0x002F,), (0x0041,), (0x0042,), (0x0043,), (0x0044,), (0x0045,),
    (0x0046,), (0x0047,), (0x0048,), (0x0049,), (0x004A,), (0x004B,), (0x004C,), (0x004D,),
    (0x004E,), (0x004F,), (0x0050,), (0x0051,), (0x0052,), (0x0053,), (0x0054,), (0x0055,),
    (0x0056,), (0x0057,), (0x0058,), (0x0059,), (0x005A,), (0x0061,), (0x0062,), (0x0063,),
    (0x0064,), (0x0065,), (0x0066,), (0x0067,), (0x0068,), (0x0069,), (0x006A,), (0x006B,),
    (0x006C,), (0x006D,), (0x006E,), (0x006F,), (0x0070,), (0x0071,), (0x0072,), (0x0073,),
    (0x0074,), (0x0075,), (0x0076,), (0x0077,), (0x0078,), (0x0079,), (0x007A,), (0x25BA,),
    (0x003A,), (0x00C4,), (0x00D6,), (0x00DC,), (0x00E4,), (0x00F6,), (0x00FC,), None,
    None,      None,      None,      None,      None,      None,      None,      None)
graphdata.chcpdocs["993300"] = "eight-ones-terminated"
graphdata.defgsets["993300"] = ("nil", "nil", "nil", "nil")

