#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019–2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

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
graphdata.gsets["ir098/extended"] = (94, 1, (None, None, None, (9287,), None, None, None, None, None, (9286,), None, None, (9289,), None, (9288,), (48,), (49,), (50,), (51,), (52,), (53,), (54,), (55,), (56,), (57,), (9286,), (9287,), (9288,), (9289,), None, None, None, (9286,), (9287,), (9288,), (9289,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (8203,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))

graphdata.gsets["ibm-e13b"] = (94, 1, (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (9287,), None, None, None, None, None, (9286,), None, None, None, None, None, (9288,), None, None, None, None, None, (9289,), None, None, None))

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

# IBM code page 1034 "Printer Application - Shipping Label, Set #2", containing only what IBM calls
#   the "Vital Safety Parts (VSP) Symbol" and which is better recognised as a symbol for "halt"
#   on buttons or the old-style (pre-octagon) "type B2b" stop sign.
graphdata.gsets["stop-symbol"] = (94, 1, (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (9098,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
graphdata.chcpdocs['1034'] = 'ecma-35'
graphdata.defgsets['1034'] = ('stop-symbol', 'nil', 'nil', 'nil')

graphdata.gsets["digits-only"] = (94, 1, (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (48,), (49,), (50,), (51,), (52,), (53,), (54,), (55,), (56,), (57,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))

graphdata.gsets["ibmextras/zh-hans"] = (96, 1, (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (0x00AC,), (0x005C,), (0x007E,)))
graphdata.rhses["1042"] = graphdata.rhses["29714"] = ((0x00A3,),) + ((None,) * 31) + graphdata.gsets["ibmextras/zh-hans"][2]
graphdata.defgsets["1042"] = graphdata.defgsets["29714"] = ("ir014", "ibmextras/zh-hans", "nil", "nil")

graphdata.gsets["ibmextras/zh-hant"] = (94, 1, (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (0x00AC,), (0x00A6,)))
graphdata.rhses["1043"] = graphdata.rhses["29715"] = ((0x00A2,),) + ((None,) * 31) + graphdata.gsets["ibmextras/zh-hant"][2]
graphdata.defgsets["1043"] = graphdata.defgsets["29715"] = ("ir006", "ibmextras/zh-hant", "nil", "nil")

graphdata.gsets["enyay"] = (94, 1, (None, None, None, (0x00F1,), (0x00D1,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
graphdata.rhses["20917"] = graphdata.rhses["49589"] = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (0x00A3,), None, None, None, None) + graphdata.gsets["enyay"][2]
graphdata.defgsets["20917"] = graphdata.defgsets["49589"] = ("ir006", "enyay", "nil", "nil")

graphdata.rhses["1115"] = ((0x00A3,), (0x00AC,), (0x00A5,), (0x203E,), (0x00A6,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)

graphdata.gsets["square-brackets"] = (94, 1, (
               None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, (0x5B,), None,
         None, None, None, None, (0x5D,), None, None, None,
         None, None, None, None, None, None, None))

graphdata.gsets["squared-and-cubed"] = (94, 1, (
               None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, (0xB3,), None,
         None, None, None, None, (0xB2,), None, None, None,
         None, None, None, None, None, None, None))

graphdata.gsets["half-and-trema"] = (94, 1, (
               None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, (0xA8,), None,
         None, None, None, None, (0xBD,), None, None, None,
         None, None, None, None, None, None, None))

# Technical symbols from the IBM 5080 or IBM 6090 graphics system.
# Projected supplementary portion of EBCDIC code pages 881, 882, 883, 884 and 1037, superset of
#   that of EBCDIC code pages 885 and 886, subset of that of EBCDIC code page 887.
graphdata.gsets["ibm5080-technical"] = (94, 1, (
               None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None,
         None, None, None, (8452,), None, None, None, (176,),
         (177,), None, (9012,), (8615,), None, (8960,), None, (8804,),
         (8805,), (8486,), None, None, (9013,), (181,), (8901,)))

# LaTeX Text Symbols ("TS1")
_ts1_gl = (   None,       None,       None,       (0x0024,),  None,       None,       (0x02C8,),
  None,       None,       (0x2217,),  None,       (0x002C,),  (0x2E40,),  (0x002E,),  (0x2044,),
  (0x1D7CE,), (0x1D7CF,), (0x1D7D0,), (0x1D7D1,), (0x1D7D2,), (0x1D7D3,), (0x1D7D4,), (0x1D7D5,),
  (0x1D7D6,), (0x1D7D7,), None,       None,       (0x27E8,),  (0x2212,),  (0x27E9,),  None,
  None,       None,       None,       None,       None,       None,       None,       None,
  None,       None,       None,       None,       None,       (0x2127,),  None,       (0x25EF,),
  None,       None,       None,       None,       None,       None,       None,       (0x2126,),
  None,       None,       None,       (0x27E6,),  None,       (0x27E7,),  (0x2191,),  (0x2193,),
  (0x2035,),  None,       (0x22C6,),  (0x26AE,),  (0x271D,),  None,       None,       None,
  None,       None,       None,       None,       (0x2E19,),  (0x26AD,),  (0x266A,),  None,
  None,       None,       None,       (0x017F,),  None,       None,       None,       None,
  None,       None,       None,       None,       None,       None,       (0x223C,))
graphdata.gsets["tex-symbols-gl/94"] = (94, 1, _ts1_gl)
graphdata.gsets["tex-symbols-gl/96"] = (96, 1, ((0x2422,), *_ts1_gl, (0x30A0,)))
graphdata.rhses["996210"] = (
    (0x02D8,), (0x02C7,), (0x2033,),        (0x2036,), (0x2020,), (0x2021,), (0x2016,), (0x2030,),
    (0x2022,), (0x2103,), (0x0053, 0x20E6), (0x023C,), (0x0192,), (0x20A1,), (0x20A9,), (0x20A6,),
    (0x20B2,), (0x20BD,), (0x20A4,),        (0x211E,), (0x203D,), (0x2E18,), (0x20AB,), (0x2122,),
    (0x2031,), (0x2761,), (0x0E3F,),        (0x2116,), (0x2052,), (0x212E,), (0x25E6,), (0x2120,),
    (0x2045,), (0x2046,), (0x00A2,),        (0x00A3,), (0x00A4,), (0x00A5,), (0x00A6,), (0x00A7,),
    (0x00A8,), (0x00A9,), (0x00AA,),       (0x1F12F,), (0x00AC,), (0x2117,), (0x00AE,), (0x203E,),
    (0x00B0,), (0x00B1,), (0x00B2,),        (0x00B3,), (0x2032,), (0x00B5,), (0x00B6,), (0x00B7,),
    (0x203B,), (0x00B9,), (0x00BA,),        (0x221A,), (0x00BC,), (0x00BD,), (0x00BE,), (0x20AC,),
    None, None, None, None, None, None, None,      None,
    None, None, None, None, None, None, None,      None,
    None, None, None, None, None, None, (0x00D7,), None,
    None, None, None, None, None, None, None,      None,
    None, None, None, None, None, None, None,      None,
    None, None, None, None, None, None, None,      None,
    None, None, None, None, None, None, (0x00F7,), None,
    None, None, None, None, None, None, None,      None)
graphdata.defgsets["996210"] = ("tex-symbols-gl/94", "nil", "nil", "nil")

# SPCaesarea charset for notational symbols for New Testament textual apparatus
graphdata.gsets["spcaesarea"] = (94, 1, (
                None,      None,      (0x2E00,), (0x2E06,), None,       None,      None,
    (0x27E6,),  (0x27E7,), (0x203B,), None,      None,      None,       (0x2E14,), (0x2E13,),
    None,       None,      None,      None,      None,      None,       None,      None,
    None,       None,      None,      None,      None,      None,       None,      None,
    (0x2022,),  None,      None,      None,      None,      None,       None,      None,
    None,       None,      None,      None,      None,      (0x1D510,), None,      None,
    (0x1D513,), None,      None,      None,      None,      None,       None,      None,
    None,       None,      None,      (0x005B,), (0x2E0C,), (0x005D,),  None,      None,
    None,       None,      None,      None,      None,      None,       None,      None,
    None,       None,      None,      None,      None,      None,       None,      (0x00B0,),
    None,       None,      None,      None,      (0x2020,), None,       None,      None,
    None,       None,      None,      (0x2E21,), (0x2E0B,), (0x2E20,),  None))

# Bookshelf Symbol 3 charset for astrological symbols and musical accidentals
graphdata.gsets["bookshelf-3"] = (94, 1, (
               None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      (0x260C,), (0x260D,), (0x263C,), (0x263F,), (0x2640,), (0x2641,), (0x2642,),
    (0x2643,), (0x266D,), (0x266E,), (0x261E,), (0x2648,), (0x2649,), (0x264A,), (0x264B,),
    (0x264C,), (0x264D,), (0x260A,), (0x260B,), (0x266F,), (0x2610,), (0x2644,), (0x26E2,),
    (0x2646,), (0x264E,), (0x264F,), (0x2650,), (0x2653,), (0x211E,), (0x2647,), (0x263D,),
    (0x263E,), (0x2651,), (0x2652,), None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None,      None,
    None,      None,      None,      None,      None,      None,      None))

# Hershey "markers" font's codepage for bullet-points for lists
graphdata.gsets["hershey-list-markers"] = (94, 1, (
               None,      None,             None,      None,      None,      None,      None,
    None,      None,      None,             None,      None,      None,      None,      None,
    None,      None,      None,             None,      None,      None,      None,      None,
    None,      None,      None,             None,      None,      None,      None,      None,
    None,      (0x25E6,), (0x25FD, 0xFE0E), (0x25B5,), (0x25CA,), (0x2606,), (0x2719,), (0x1F7A3,),
    (0x2715,), (0x2217,), (0x2022,), (0x25FE, 0xFE0E), (0x2BC5,), (0x2BC7,), (0x2BC6,), (0x2BC8,),
    (0x26DB,), None,      None,             None,      None,      None,      None,      None,
    None,      None,      None,             None,      None,      None,      None,      None,
    None,      (0x25E6,), (0x25FD, 0xFE0E), (0x25B5,), (0x25CA,), (0x2606,), (0x2719,), (0x1F7A3,),
    (0x2715,), (0x2217,), (0x2022,), (0x25FE, 0xFE0E), (0x2BC5,), (0x2BC7,), (0x2BC6,), (0x2BC8,),
    (0x26DB,), None,      None,             None,      None,      None,      None,      None,
    None,      None,      None,             None,      None,      None,      None))
