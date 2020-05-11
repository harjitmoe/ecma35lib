#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata

# DEC doesn't vary 0x24. ECMA-6:1991 does not vary 0x5F, and puts strict restrictions on permitted
# glyphs for 0x23 (# or £) and 0x24 ($ or ¤), which is deviated from by the Mainland Chinese
# version. ETS 300 706 liberally varies all three.
variants = [0x23, 0x24, 0x40, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x7B, 0x7C, 0x7D, 0x7E]

# Only specifying the changed points. None for unchanged. -1 for unused.
# Dict is for changes to characters invariant even in ETS 300 706 Roman G0.
# What WHATWG would call "willful violations" wrt ECMA-6:1991 are acknowledged where applicable.
raw_variants = {
    # Old IRV
    # Worth pointing out from the get-go that I'm mapping the ISO 646 overline to U+203E (per CJK
    # convention) rather than U+00AF (per convention in more ISO 8859 influenced areas).
    "ir002": ([None, 0xA4, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir002tilde": ([None, 0xA4, None, None, None, None, None, None, 
                                None, None, None, None, None], {}),
    # BS 4730 (United Kingdom)
    "ir004": ([0xA3, None, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir004dec": ([0xA3, None, None, None, None, None, None, None, 
                              None, None, None, None, None], {}),
    # US-ASCII / New IRV, ISO/IEC 10367 G0 set
    "ir006": ([None, None, None, None, None, None, None, None, 
                           None, None, None, None, None], {}),
    # CNS 5205 and also apparently the Dutch (non-DEC) set; IBM's 1019.
    "ir006overline": ([None, None, None, None, None, None, None, None, 
                                   None, None, None, None, 0x203E], {}),
    # NATS-SEFI (Swedish and Finnish Journalism)
    "ir008-1": ([None, None, 0x3000, 0xC4, 0xD6, 0xC5, 0x25A0, None, 
                             0x2007, 0xE4, 0xF6, 0xE5, 0x2013], {}),
    # DEC NRCS for Finland (apparently used in response to ir008-1 escape)
    "ir008-1dec": ([None, 0xA4, None, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                                0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # NATS-DANO (Danish and Norwegian Journalism)
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "ir009-1": ([0xBB, None, 0x3000, 0xC6, 0xD8, 0xC5, 0x25A0, None, 
                             0x2007, 0xE6, 0xF8, 0xE5, 0x2013], {0x22: 0xAB}),
    # DEC NRCS for Denmark and Norway
    "ir009-1dec": ([None, None, 0xC4, 0xC6, 0xD8, 0xC5, 0xDC, None, 
                                0xE4, 0xE6, 0xF8, 0xE5, 0xFC], {}),
    # SEN 85 02 00 ax B (Swedish and Finnish)
    "ir010": ([None, None, 0xC9, 0xC4, 0xD6, 0xC5, None, None, 
                           None, 0xE4, 0xF6, 0xE5, 0x203E], {}),
    # SEN 85 02 00 ax C (Swedish names), ETS for Sweden and Finland
    "ir011": ([None, 0xA4, None, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                           0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # DEC NRCS for Sweden
    "ir011dec": ([None, None, None, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                              0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # JIS C 6220 / JIS X 0201 Roman set (JIS-Roman)
    "ir014": ([None, None, None, None, 0xA5, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir014tilde": ([None, None, None, None, 0xA5, None, None, None, 
                                None, None, None, None, None], {}),
    # KS X 1003 / G0 set of non-ASCII EUC-KR (KS-Roman, KSC-Roman)
    "ksroman": ([None, None, None, None, 0x20A9, None, None, None, 
                             None, None, None, None, 0x203E], {}),
    "ksromantilde": ([None, None, None, None, 0x20A9, None, None, None, 
                                  None, None, None, None, None], {}),
    # Olivetti Italian
    "ir015": ([0xA3, None, 0xA7, 0xB0, 0xE7, 0xE9, None, None, 
                           0xF9, 0xE0, 0xF2, 0xE8, 0xEC], {}),
    # Roman G0 set of ETS 300 706 for Italy
    # Violation of ECMA-6:1991: 0x5F is not _.
    "ir015ets": ([0xA3, None, 0xE9, 0xB0, 0xE7, 0x2192, 0x2191, 0x2317, 
                              0xF9, 0xE0, 0xF2, 0xE8,   0xEC], {}),
    # Olivetti Portugese
    "ir016": ([None, None, 0xA7, 0xC3, 0xC7, 0xD5, None, None, 
                           None, 0xE3, 0xE7, 0xF5, 0xB0], {}),
    # Olivetti Spanish
    "ir017": ([0xA3, None, 0xA7, 0xA1, 0xD1, 0xBF, None, None, 
                           None, 0xB0, 0xF1, 0xE7, None], {}),
    # DIN 66 003 (German; also same in DEC and ETS)
    "ir021": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, None, None, 
                           None, 0xE4, 0xF6, 0xFC, 0xDF], {}),
    # NF Z 62-010:1973 (old or DEC version French)
    "ir025": ([0xA3, None, 0xE0, 0xB0, 0xE7, 0xA7, None, None, 
                           None, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # Honeywell-Bull's "mixed" Latin-Greek
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x3A is not :.
    # Violation of ECMA-6:1991: 0x3F is not ?.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "ir027": ([0x393, 0xA4, 0x394, 0x3A9, 0x398, 0x3A6, 0x39B, 0x3A3, 
                            None, None, None, None, 0x203E], {
              0x21: 0x39E, 0x3A: 0x3A8, 0x3F: 0x3A0}),
    # BS_Viewdata (Roman G0 set of ETS 300 706 for United Kingdom)
    # Violation of ECMA-6:1991: 0x5F is not _.
    "ir047": ([0xA3, None, None, 0x2190, 0xBD, 0x2192, 0x2191, 0x2317, 
                           0x2015, 0xBC, 0x2016, 0xBE, 0xF7], {}),
    # INIS subset of ASCII
    # Violation of ECMA-6:1991: 0x21, 0x22, 0x26, 0x3F and 0x5F are omitted.
    # Violation of ECMA-6:1991: 0x23 is omitted, not # or £.
    "ir049": ([-1, None, -1, None, -1, None, -1, -1, 
                         -1, -1, None, -1, -1], {
              0x21: -1, 0x22: -1, 0x26: -1, 0x3F: -1}),
    # GB 1988 (Mainland China)
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "ir057": ([None, 0xA5, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    # NS 4551 version 1 (Norwegian)
    "ir060": ([None, None, None, 0xC6, 0xD8, 0xC5, None, None, 
                           None, 0xE6, 0xF8, 0xE5, 0x203E], {}),
    # Danish version, adding u-umlaut; IBM's 1017
    "ir060dk": ([None, 0xA4, None, 0xC6, 0xD8, 0xC5, 0xDC, None,
                             None, 0xE6, 0xF8, 0xE5, 0xFC], {}),
    # DEC alternative NRCS for Denmark and Norway
    "ir060dec": ([None, None, None, 0xC6, 0xD8, 0xC5, None, None, 
                              None, 0xE6, 0xF8, 0xE5, None], {}),
    # NS 4551 version 2 (Norwegian)
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "ir061": ([0xA7, None, None, 0xC6, 0xD8, 0xC5, None, None, 
                           None, 0xE6, 0xF8, 0xE5, 0x7C], {}),
    # NF Z 62-010:1982 (new version French)
    "ir069": ([0xA3, None, 0xE0, 0xB0, 0xE7, 0xA7, None, None, 
                           0xB5, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # IBM Portugese
    "ir084": ([None, None, 0xB4, 0xC3, 0xC7, 0xD5, None, None, 
                           None, 0xE3, 0xE7, 0xF5, None], {}),
    "ir084dec": ([None, None, None, 0xC3, 0xC7, 0xD5, None, None, 
                              None, 0xE3, 0xE7, 0xF5, None], {}),
    # IBM Spanish
    "ir085": ([None, None, 0xB7, 0xA1, 0xD1, 0xC7, 0xBF, None, 
                           None, 0xB4, 0xF1, 0xE7, 0xA8], {}),
    # MSZ 7795/3 (Hungarian)
    "ir086": ([None, 0xA4, 0xC1, 0xC9, 0xD6, 0xDC, None, None, 
                           0xE1, 0xE9, 0xF6, 0xFC, 0x2DD], {}),
    # JIS C 6220 / JIS X 0201 Roman set, OCR subset
    "ir092": ([None, None, None, None, 0xA5, None, None, None, 
                           -1, None, None, None, -1], {}),
    # T.61 subset of IRV
    "ir102": ([None, 0xA4, None, None, -1, None, -1, None, 
                           -1, -1, None, -1, -1], {}),
    # CSA Z243.4:1985 main version (Canadian French)
    "ir121": ([None, None, 0xE0, 0xE2, 0xE7, 0xEA, 0xEE, None, 
                           0xF4, 0xE9, 0xF9, 0xE8, 0xFB], {}),
    # CSA Z243.4:1985 alternative version (Canadian French)
    "ir121": ([None, None, 0xE0, 0xE2, 0xE7, 0xEA, 0xC9, None, 
                           0xF4, 0xE9, 0xF9, 0xE8, 0xFB], {}),
    # JUS I.B1.002 (CROSCII / Croatian / YUSCII for Gajica)
    "ir141": ([None, None, 0x17D, 0x160, 0x110, 0x106, 0x10C, None, 
                           0x17E, 0x161, 0x111, 0x107, 0x10D], {}),
    # NC 99-10:81 (Cuban Spanish)
    "ir151": ([None, 0xA4, None, 0xA1, 0xD1, None, 0xBF, None, 
                           None, 0xB4, 0xF1, 0x5B, 0xA8], {}),
    # Invariant subset of ECMA-6
    "ir170": ([-1, -1, -1, -1, -1, -1, -1, 0x5F, 
                       -1, -1, -1, -1, -1], {}),
    # Invariant subset of DEC NRCS
    # Violation of ECMA-6:1991: 0x5F is omitted.
    "ir170dec": ([-1, None, -1, -1, -1, -1, -1, -1, 
                            -1, -1, -1, -1, -1], {}),
    # Invariant subset of Roman G0 set of ETS 300 706
    # Violation of ECMA-6:1991: 0x5F is omitted.
    "ir170ets": ([-1, -1, -1, -1, -1, -1, -1, -1, 
                          -1, -1, -1, -1, -1], {}),
    # I.S. 433 (Irish Gaelic)
    "ir207": ([0xA3, None, 0xD3, 0xC9, 0xCD, 0xDA, 0xC1, None, 
                           0xF3, 0xE9, 0xED, 0xFA, 0xE1], {}),
    ##
    # DEC NRCS for Switzerland; IBM's 1021
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "decswiss": ([0xF9, None, 0xE0, 0xE9, 0xE7, 0xEA, 0xEE, 0xE8, 
                              0xF4, 0xE4, 0xF6, 0xFC, 0xFB], {}),
    # DEC NRCS for the Netherlands; IBM's 1102
    "decdutch": ([0xA3, None, 0xBE, 0x133, 0xBD, 0x7C, None, None, 
                              None, 0xA8, 0x192, 0xBC, 0xB4], {}),
    # Supposed Icelandic version (cannot verify)
    "icelandic": ([None, None, 0xD0, 0xDE, None, 0xC6, 0xD6, None, 
                               0xF0, 0xFE, None, 0xE6, 0xF6], {}),
    # Supposedly matches BN-74/3101-01 for Polish (cannot verify)
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "polish": ([None, (0x7A, 0x200D, 0x142), 
                            0x119, 0x17A, None, 0x144, 0x15B, None, 
                            0x105, 0xF3, 0x142, 0x17C, 0x107], {}),
    # Supposed Maltese version (cannot verify)
    "maltese": ([None, None, None,  0x121, 0x17C, 0x127, None, None, 
                             0x10B, 0x120, 0x17B, 0x126, 0x10A], {}),
    ##
    # Roman G0 set of ETS 300 706 for French
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsfrench": ([0xE9, 0xEF, 0xE0, 0xEB, 0xEA, 0xF9, 0xEE, 0x2317, 
                               0xE8, 0xE2, 0xF4, 0xFB, 0xE7], {}),
    # Roman G0 set of ETS 300 706 for Spain and Portugal
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsiberian": ([0xE7, None, 0xA1, 0xE1, 0xE9, 0xED, 0xF3, 
                          0xFA, 0xBF, 0xFC, 0xF1, 0xE8, 0xE0], {}),
    # Roman G0 set of ETS 300 706 for Estonia
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsestonian": ([None, 0xF5, 0x160, 0xC4, 0xD6, 0x17D, 0xDC, 
                           0xD5, 0x161, 0xE4, 0xF6, 0x17E, 0xFC], {}),
    # Roman G0 set of ETS 300 706 for Lithuania and Latvia
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsbaltic": ([None, None, 0x160, 0x117, 0x119, 0x17D, 0x10D, 0x16B, 
                               0x161, 0x105, 0x173, 0x17E, 0x12F], {}),
    # Roman G0 set of ETS 300 706 for West South Slavic languages
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤ (except in the alternate version).
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsgajica": ([None, 0xCB, 0x10C, 0x106, 0x17D, 0x110, 0x160,
                         0xEB, 0x10D, 0x107, 0x17E, 0x111, 0x161], {}),
    "etsgajicadollar": ([None, None, 0x10C, 0x106, 0x17D, 0x110, 0x160,
                               0xEB, 0x10D, 0x107, 0x17E, 0x111, 0x161], {}),
    # Roman G0 set of ETS 300 706 for Czech and Slovak
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤ (except in the alternate version).
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsczechoslovak": ([None, 0x16F, 0x10D, 0x165, 0x17E, 0xFD, 0xED,
                               0x159, 0xE9,  0xE1,  0x11B, 0xFA, 0x161], {}),
    # Roman G0 set of ETS 300 706 for Polish
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etspolish": ([None, 0x144, 0x105, (0x7A, 0x200D, 0x142), 
                                              0x15A, 0x141, 0x107, 0xF3, 
                                0x119, 0x17C, 0x15B, 0x142, 0x17A], {}),
    # Roman G0 set of ETS 300 706 for Romanian
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsromanian": ([None, 0xA4, 0x21A, 0xC2, 0x218, 0x102, 0xCE, 0x131, 
                                 0x21B, 0xE2, 0x219, 0x103, 0xEE], {}),
    # Roman G0 set of ETS 300 706 for Turkish
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsturkish": ([(0x54, 0x200D, 0x4C), 
                          0x11F, 0x130, 0x15E, 0xD6, 0xC7, 0xDC,
                          0x11E, 0x131, 0x15F, 0xF6, 0xE7, 0xFC], {}),
}

for (name, (myvars, override)) in raw_variants.items():
    myset = list(range(0x21, 0x7F))
    for frm, to in list(zip(variants, myvars)) + list(override.items()):
        if to is not None:
            if to != -1:
                myset[frm - 0x21] = to
            else:
                myset[frm - 0x21] = None
    graphdata.gsets[name] = (94, 1, tuple(myset))

# Assorted supplements

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





