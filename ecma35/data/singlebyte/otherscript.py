#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# I.S. 434 Latin/Ogham RHS
# Registered as a 96-set for some reason but doesn't actually allocate the corners.
graphdata.gsets["ir208"] = (96, 1, 
             ((None,) * 64) + tuple(range(0x1680, 0x169D)) + (None, None, None))

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
graphdata.gsets["ir013"] = (94, 1, tuple(range(0xFF61, 0xFFA0)) + ((None,) * 31))
graphdata.rhses["897"] = ((None,) * 33) + tuple(range(0xFF61, 0xFFA0)) + ((None,) * 32)
graphdata.defgsets["897"] = ("ir014", "ir013", "nil", "nil")
# IBM's 4992 (or unrestricted 896)
graphdata.gsets["ir013ibm"] = (94, 1, tuple(range(0xFF61, 0xFFA0)) + (
                0xA2, 0xA3, 0xAC, 0x5C, 0x7E, 0x203E, 0xA6) + ((None,) * 24))
# 1-byte MacJapanese
graphdata.gsets["ir013mac"] = (94, 1, tuple(range(0xFF61, 0xFFA0)) + (
                0x5C, 0xA0, 0xA9, 0x2122, 0x2026, 
                0xFC, 0xF880, 0xF881, 0x20A9, 0x2013, 0xFF3F) + ((None,) * 21))
# For Windows code pages
graphdata.gsets["ir013win"] = (94, 1, tuple(range(0xFF61, 0xFFA0)) + (
                0x20AC,) + tuple(range(0xF8F0, 0xF8F9)) + ((None,) * 21))
graphdata.gsetflags["ir013win"] |= {"GBK:NO_EURO"}
graphdata.gsets["ir013euro"] = graphdata.gsets["ir013win"]

# TODO: ir155 (ISO 10367 box drawing set), ir068 (APL)



