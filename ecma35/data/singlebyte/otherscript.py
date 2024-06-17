#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020, 2022, 2024.

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
graphdata.rhses["897"] = ((None,) * 33) + _the_mother + ((None,) * 32)
graphdata.defgsets["897"] = ("ir014", "ir013", "nil", "nil")
# IBM's 4992 (or unrestricted 896)
graphdata.gsets["ir013/ibm"] = (94, 1, _the_mother + (
                (0xA2,), (0xA3,), (0xAC,), (0x5C,), (0x7E,), (0x203E,), (0xA6,)) + ((None,) * 24))
# 1-byte MacJapanese
graphdata.gsets["ir013/mac"] = (94, 1, _the_mother + (
                (0x5C,), (0xA0,), (0xA9,), (0x2122,), (0x2026,), 
                (0xFC,), (0xF880,), (0xF881,), (0x20A9,), (0x2013,), (0xFF3F,)) + ((None,) * 20))
# For Windows code pages
graphdata.gsets["ir013/win"] = (94, 1, _the_mother + (
                (0x20AC,),) + tuple((i,) for i in range(0xF8F0, 0xF8F9)) + ((None,) * 21))
graphdata.gsetflags["ir013/win"] |= {"GBK:NO_EURO"}
graphdata.gsets["ir013/euro"] = graphdata.gsets["ir013/win"]

# ARIB STD-B24 Volume 1, single-byte Hiragana
graphdata.gsets["aribkana/hiragana"] = (94, 1, tuple((i,) if i else None for i in
            tuple(range(0x3041, 0x3094)) +
            (None, None, None, 0x309D, 0x309E, 0x30FC, 0x3002, 0x300C, 0x300D, 0x3001, 0x30FB)))

# ARIB STD-B24 Volume 1, single-byte non-JISX0201 Katakana
graphdata.gsets["aribkana/katakana"] = (94, 1, tuple((i,) if i else None for i in
            tuple(range(0x30A1, 0x30F7)) +
            (0x30FD, 0x30FE, 0x30FC, 0x3002, 0x300C, 0x300D, 0x3001, 0x30FB)))

# Non-Cyrillic INIS RHS. Greek support is insubstantial enough that it probably doesn't belong
#   in greek.py.
graphdata.gsets["ir050"] = (94, 1, (
               None,      None,      None,      None,      None,      None,      None, 
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None, 
    None,      None,      (0x03B1,), (0x03B2,), (0x03B3,), (0x03C3,), (0x039E,), None, 
    None,      None,      None,      None,      None,      None,      None,      None, 
    None,      None,      None,      None,      None,      None,      None,      None, 
    None,      None,      None,      None,      None,      None,      None,      None, 
    None,      None,      None,      None,      None,      None,      (0x2192,), (0x222B,), 
    (0x2070,), (0xB9,),   (0xB2,),   (0xB3,),   (0x2074,), (0x2075,), (0x2076,), (0x2077,), 
    (0x2078,), (0x2079,), (0x207A,), (0x207B,), (0x221A,), (0x0394,), (0x039B,), (0x03A9,), 
    (0x2080,), (0x2081,), (0x2082,), (0x2083,), (0x2084,), (0x2085,), (0x2086,), (0x2087,), 
    (0x2088,), (0x2089,), (0x03A3,), (0x03BC,), (0x03BD,), (0x03C9,), (0x03C0,)
))

# 7-bit APL
graphdata.gsets["ir068"] = (94, 1, parsers.read_single_byte("UTC/APL-ISO-IR-68.TXT", typ="GL94", filter_to_single=True))

# JIS X 9010 code for OCR-B font characters absent from JIS-Roman, basically a very small subset of
#   ISO-8859-1's RHS where the backslash is substituted for the yen sign (compare the derivation of
#   DRV from DIN 66003 and ISO-8859-1).
graphdata.gsets["ir093"] = (94, 1, (None, None, (0xA3,), (0xA4,), (0x5C,), None, (0xA7,)) + (None,) * 87)
graphdata.gsets["ir093/ext"] = (94, 1, tuple((i,) if i != 0xA5 else (0x5C,) for i in range(0xA1, 0xFF)))

# JIS X 9010 code for JIS X 9008 font characters absent from JIS X 0201 (i.e. the backslash only),
#   a single-character subset of IR-093.
# Awkwardly, the sole character here is probably U+244A's character source, despite being evidently
#   intended to be U+005C (if one reads the reg's rubric).
graphdata.gsets["ir095"] = (94, 1, (None, None, None, None, (0x5C,), None, None) + (None,) * 87)
graphdata.gsets["ir095/double"] = (94, 1, (None, None, None, None, (0x244A,), None, None) + (None,) * 87)

# JIS X 9010 Kana set for JIS X 9008 font (which supports large katakana only)
graphdata.gsets["ir096"] = (94, 1, (None,) + _the_mother[1:3] + (None, None) + _the_mother[5:6] + (None,)*9 + _the_mother[15:] + (None,)*31)

# ISO 2033 / JIS X 9010 code for E-13B font (machine-readable lines on cheques)
graphdata.gsets["ir098"] = (94, 1, (
               None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,  
    (0x0030,), (0x0031,), (0x0032,), (0x0033,), (0x0034,), (0x0035,), (0x0036,), (0x0037,), 
    (0x0038,), (0x0039,), (0x2446,), (0x2447,), (0x2448,), (0x2449,), None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,  
    None,      None,      None,      None,      None,      None,      None,      None, 
    None,      None,      None,      None,      None,      None,      None,      None,  
    None,      None,      None,      None,      None,      None,      None,      None, 
    None,      None,      None,      None,      None,      None,      None,      None,  
    None,      None,      None,      None,      None,      None,      None,      None,  
    None,      None,      None,      None,      None,      None,      None,      None,  
    None,      None,      None,      None,      None,      None,      None,
))

# ISO-10367's box drawing set
graphdata.gsets["ir155"] = (96, 1, (
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    (0x2503,), (0x2501,), (0x250F,), (0x2513,), (0x2517,), (0x251B,), (0x2523,), (0x252B,), 
    (0x2533,), (0x253B,), (0x254B,), (0x2580,), (0x2584,), (0x2588,), (0x25AA,), None,      
    (0x2502,), (0x2500,), (0x250C,), (0x2510,), (0x2514,), (0x2518,), (0x251C,), (0x2524,), 
    (0x252C,), (0x2534,), (0x253C,), (0x2591,), (0x2592,), (0x2593,), None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,      
    None,      None,      None,      None,      None,      None,      None,      None,
))

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

# MARC 21's MARC-8 subscript numbers set
graphdata.gsets["marc-subscript"] = (94, 1, tuple((i,) if i else None for i in (
                     None, None, None, None, None, None, None,
             0x208D, 0x208E, None, 0x208A, None, 0x208B, None, None,
             0x2080, 0x2081, 0x2082, 0x2083, 0x2084, 0x2085, 0x2086, 0x2087,
             0x2088, 0x2089, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None)))

# MARC 21's MARC-8 superscript numbers set
graphdata.gsets["marc-superscript"] = (94, 1, tuple((i,) if i else None for i in (
                     None, None, None, None, None, None, None,
             0x207D, 0x207E, None, 0x207A, None, 0x207B, None, None,
             0x2070, 0x00B9, 0x00B2, 0x00B3, 0x2074, 0x2075, 0x2076, 0x2077,
             0x2078, 0x2079, None, None, None, None, None, None, 
             None, None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None, None, 
             None, None, None, None, None, None, None)))

# DEC Special Graphics ("DECGraphics")
graphdata.gsets["decgraphics"] = (94, 1, tuple((i,) if i else None for i in (
                    0x0021, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 
            0x0028, 0x0029, 0x002A, 0x002B, 0x002C, 0x002D, 0x002E, 0x002F, 
            0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, 
            0x0038, 0x0039, 0x003A, 0x003B, 0x003C, 0x003D, 0x003E, 0x003F, 
            0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 
            0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004D, 0x004E, 0x004F, 
            0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, 
            0x0058, 0x0059, 0x005A, 0x005B, 0x005C, 0x005D, 0x005E, 0x00A0, 
            0x25C6, 0x2592, 0x2409, 0x240C, 0x240D, 0x240A, 0x00B0, 0x00B1, 
            0x2424, 0x240B, 0x2518, 0x2510, 0x250C, 0x2514, 0x253C, 0x23BA, 
            0x23BB, 0x2500, 0x23BC, 0x23BD, 0x251C, 0x2524, 0x2534, 0x252C, 
            0x2502, 0x2264, 0x2265, 0x03C0, 0x2260, 0x00A3, 0x2219)))

