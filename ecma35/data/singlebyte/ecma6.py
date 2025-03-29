#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020, 2022, 2023, 2024, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

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
    "ir002/tilde": ([None, 0xA4, None, None, None, None, None, None, 
                                 None, None, None, None, None], {}),
    # BS 4730 (United Kingdom)
    "ir004": ([0xA3, None, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir004/dec": ([0xA3, None, None, None, None, None, None, None, 
                               None, None, None, None, None], {}),
    # ISO-646:1967 "sterling" variant for fixed-width old-pence data
    # Violation of ECMA-6:1991: 0x3A is not :.
    # Violation of ECMA-6:1991: 0x3B is not ;.
    "ir004/sterling": ([0xA3, None, None, None, None, None, None, None, 
                                    None, None, None, None, 0x203E], {0x3A: 0x2491, 0x3B: 0x2492}),
    # US-ASCII / New IRV, ISO/IEC 10367 G0 set
    "ir006": ([None, None, None, None, None, None, None, None, 
                           None, None, None, None, None], {}),
    # ASCII-1963
    # Violation of ECMA-6:1991: 0x5F is not _.
    # Violation of ECMA-6:1991: lowercase letters omitted.
    "ir006/1963": ([None, None, None, None, None, None, 0x2191, 0x2190, 
                                -1,   -1,   -1,   -1,   -1],
                   dict((i, -1) for i in range(0x61, 0x7B))),
    # ASCII-1967 with broken vertical bar, also basis of DP94-range subset of EBCDIC code pages 256
    #   and 500.
    "ir006/brvbar": ([None, None, None, None, None, None, None, None, 
                                  None, None, 0xA6, None, None], {}),
    # CNS 5205 and also apparently the Dutch (non-DEC) set; IBM's 1019.
    "ir006/overline": ([None, None, None, None, None, None, None, None, 
                                    None, None, None, None, 0x203E], {}),
    # Projection from DP94-range subset of EBCDIC code page 1278. Normally this case would be
    #   discarded since it's a CCSID 8448 superset, i.e. the vbar is only replaced because the
    #   ASCII vbar is included in its code page 500 location—however, the florin sign location
    #   projects to the same location as in code page 1102, i.e. DEC Dutch.
    "ir006/florin": ([None, None, None, None, None,   None, None, None, 
                                  None, None, 0x0192, None, None], {}),
    # ASCII-1967, PL/I variant.
    # Violation of ECMA-6:1991: 0x21 is not !.
    "ir006/pli": ([None, None, None, None, None, None, 0xAC, None, 
                               None, None, 0xA6, None, None], {0x21: 0x7C}),
    # ASCII-1967, PL/I variant, subset without lowercase letters
    #   (projection from EBCDIC code page 2097).
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: lowercase letters omitted.
    "ir006/pli/unicameral": ([None, None, None, None, None, None, 0xAC, None, 
                                          -1,   -1,   -1,   -1,   -1], dict([
        (0x21, 0x7C),
        *[(i, -1) for i in range(0x61, 0x7B)]])),
    # Left-hand side of IBM code page 877 for the OCR-B optical character recognition font
    # Violation of ECMA-6:1991: 0x5F is not (strictly) _.
    "ir006/ocr-b": ([None, None, None, None, None,   None, 0x2303, 0x02CD,
                                 None, None, 0xFFE8, None, None], {}),
    # Left-hand side of IBM HP-compatibility code page 1053
    "ir006/ibm-hp-diacritics": ([None, None, None,   None, None, None, 0x02C6, None,
                                             0x02CB, None, None, None, 0x02DC], {}),
    # Left-hand side of IBM HP-compatibility code page 1057
    "ir006/ibm-hp-alternatives": ([None, None, None,   None, None,   None, 0x02C6, None,
                                               0x02CB, None, 0xFFE8, None, 0x02DC], {}),
    # Left-hand side of IBM HP-compatibility code page 1058
    "ir006/ibm-hp-ascii-tilde": ([None, None, None,   None, None,   None, 0x02C6, None,
                                              0x02CB, None, 0xFFE8, None, None], {}),
    # ASCII-1967, curly quotation marks variant.
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    "ir006/smartquotes": ([None, None, None,   None, None, None, None, None, 
                                       0x2018, None, None, None, None], {0x27: 0x2019}),
    # NATS-SEFI (Swedish and Finnish Journalism)
    "ir008-1": ([None, None, 0x3000, 0xC4, 0xD6, 0xC5, 0x25A0, None, 
                             0x2007, 0xE4, 0xF6, 0xE5, 0x2013], {}),
    # DEC NRCS for Finland (apparently used in response to ir008-1 escape)
    "ir008-1/dec": ([None, None, None, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                                 0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # NATS-DANO (Danish and Norwegian Journalism)
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "ir009-1": ([0xBB, None, 0x3000, 0xC6, 0xD8, 0xC5, 0x25A0, None, 
                             0x2007, 0xE6, 0xF8, 0xE5, 0x2013], {0x22: 0xAB}),
    # DEC NRCS for Denmark and Norway
    "ir009-1/dec": ([None, None, 0xC4, 0xC6, 0xD8, 0xC5, 0xDC, None, 
                                 0xE4, 0xE6, 0xF8, 0xE5, 0xFC], {}),
    # SEN 85 02 00 ax B (Swedish and Finnish)
    "ir010": ([None, 0xA4, None, 0xC4, 0xD6, 0xC5, None, None, 
                           None, 0xE4, 0xF6, 0xE5, 0x203E], {}),
    # Projection from DP94-range subset of EBCDIC code page 19
    "ir010/ibm": ([0xA3, None, 0xA7, 0xC4, 0xD6, 0xC5, None, None, 
                               None, 0xE4, 0xF6, 0xE5, 0xB4], {}),
    # SEN 85 02 00 ax C (Swedish names), ETS for Sweden and Finland
    "ir011": ([None, 0xA4, 0xC9, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                           0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # DEC NRCS for Sweden
    "ir011/dec": ([None, None, 0xC9, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                               0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # JIS C 6220 / JIS X 0201 Roman set (JIS-Roman)
    "ir014": ([None, None, None, None, 0xA5, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir014/tilde": ([None, None, None, None, 0xA5, None, None, None, 
                                 None, None, None, None, None], {}),
    # KS X 1003 / G0 set of non-ASCII EUC-KR (KS-Roman, KSC-Roman)
    "alt646/ksroman": ([None, None, None, None, 0x20A9, None, None, None, 
                                    None, None, None, None, 0x203E], {}),
    "alt646/ksroman/tilde": ([None, None, None, None, 0x20A9, None, None, None, 
                                          None, None, None, None, None], {}),
    # Olivetti Italian
    "ir015": ([0xA3, None, 0xA7, 0xB0, 0xE7, 0xE9, None, None, 
                           0xF9, 0xE0, 0xF2, 0xE8, 0xEC], {}),
    # Roman G0 set of ETS 300 706 for Italy
    # Violation of ECMA-6:1991: 0x5F is not _.
    "ir015/ets": ([0xA3, None, 0xE9, 0xB0, 0xE7, 0x2192, 0x2191, 0x2317, 
                               0xF9, 0xE0, 0xF2, 0xE8,   0xEC], {}),
    # Projection from DP94-range subset of EBCDIC code page 389 (=ir015 but with ¬ not ^)
    "ir015/notsign": ([0xA3, None, 0xA7, 0xB0, 0xE7, 0xE9, 0xAC, None, 
                                   0xF9, 0xE0, 0xF2, 0xE8, 0xEC], {}),
    # Projection from DP94-range subset of EBCDIC code page 2060
    # Violation of ECMA-6:1991: 0x21 is not !.
    "ir015/ibmdcf": ([None, None, None, 0xB0, None, 0xE9, 0xAC, None, 
                                  0xF9, 0xE0, 0xF2, 0xE8, 0xEC], {0x21: 0x7C}),
    # Olivetti Portuguese
    "ir016": ([None, None, 0xA7, 0xC3, 0xC7, 0xD5, None, None, 
                           None, 0xE3, 0xE7, 0xF5, 0xB0], {}),
    # Olivetti Spanish
    "ir017": ([0xA3, None, 0xA7, 0xA1, 0xD1, 0xBF, None, None, 
                           None, 0xB0, 0xF1, 0xE7, None], {}),
    # DIN 66 003 (German; also same in DEC and ETS)
    "ir021": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, None, None, 
                           None, 0xE4, 0xF6, 0xFC, 0xDF], {}),
    # DIN 66003 variant projected from EBCDIC code page 8 (as opposed to EBCDIC code page 273, whose
    #   DP94 set (CCSID 4369) corresponds directly to the DIN 66003 map above)
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    "ir021/acute": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, None, None, 
                                 None, 0xE4, 0xF6, 0xFC, 0xDF], {0x27: 0xB4}),
    # Projection from DP94-range subset of EBCDIC code page 382
    "ir021/ibm38xx": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, 0xAC, None, 
                                   -1,   0xE4, 0xF6, 0xFC, 0xDF], {}),
    # Projection from DP94-range subset of EBCDIC code page 7
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "ir021/ibm-wp": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, 0xB4, None,
                                  None, 0xE4, 0xF6, 0xFC, 0xDF], {0x3C: 0xB2, 0x3E: 0xB3}),
    # NF Z 62-010:1973 (old or DEC version French)
    "ir025": ([0xA3, None, 0xE0, 0xB0, 0xE7, 0xA7, None, None, 
                           None, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # Projection from DP94 set of EBCDIC code page 274 (CCSID 4370)
    "ir025/ibmbelgian": ([None, None, 0xE0, None, 0xE7, None, None, None, 
                                      None, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # Projection from DP94-range subset of EBCDIC code page 9
    "ir025/ibmbelgianwp": ([None, None, 0xE0, 0xB0, 0xE7, 0xA7, None, None, 
                                        0xA3, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # Projection from DP94-range subset of EBCDIC code page 383
    "ir025/ibmbelgian38xx": ([None, None, 0xE0, None, 0xE7, None, 0xAC, None, 
                                          -1,   0xE9, 0xF9, 0xE8, -1], {}),
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
    # Projection from DP94-range subset of EBCDIC code page 20
    "ir060/ibm": ([0xA3, None, 0xB4, 0xC6, 0xD8, 0xC5, None, None, 
                               None, 0xE6, 0xF8, 0xE5, 0xA8], {}),
    # Danish version, adding u-umlaut; IBM's 1017
    "ir060/dk": ([None, 0xA4, None, 0xC6, 0xD8, 0xC5, 0xDC, None,
                              None, 0xE6, 0xF8, 0xE5, 0xFC], {}),
    # DEC alternative NRCS for Denmark and Norway
    "ir060/dec": ([None, None, None, 0xC6, 0xD8, 0xC5, None, None, 
                               None, 0xE6, 0xF8, 0xE5, None], {}),
    # NS 4551 version 2 (Norwegian)
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "ir061": ([0xA7, None, None, 0xC6, 0xD8, 0xC5, None, None, 
                           None, 0xE6, 0xF8, 0xE5, 0x7C], {}),
    # NF Z 62-010:1982 (new version French)
    "ir069": ([0xA3, None, 0xE0, 0xB0, 0xE7, 0xA7, None, None, 
                           0xB5, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # Projection from DP94-range subset of EBCDIC code page 421 (ir069 with µ/£ swap, à→á, ù→ú)
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "ir069/ibmmaghreb": ([0xB5, None, 0xE1, 0xB0, 0xE7, 0xA7, None, None, 
                                      0xA3, 0xE9, 0xFA, 0xE8, 0xA8], {}),
    # Projection from DP94-range subset of EBCDIC code page 388
    "ir069/ibm38xx": ([0xA3, None, 0xE0, 0xB0, 0xE7, 0xA7, 0xAC, None, 
                                   -1,   0xE9, 0xF9, 0xE8, -1], {}),
    # Projection from DP94-range subset of EBCDIC code page 2059
    "ir069/ibmdcf": ([None, None, 0xE0, 0xB0, 0xE7, 0xA7, 0xAC, None, 
                                  -1,   0xE9, 0xF9, 0xE8, -1], {}),
    # IBM Portuguese
    "ir084": ([None, None, 0xB4, 0xC3, 0xC7, 0xD5, None, None, 
                           None, 0xE3, 0xE7, 0xF5, None], {}),
    "ir084/dec": ([None, None, None, 0xC3, 0xC7, 0xD5, None, None, 
                               None, 0xE3, 0xE7, 0xF5, None], {}),
    # IBM Spanish
    "ir085": ([None, None, 0xB7, 0xA1, 0xD1, 0xC7, 0xBF, None, 
                           None, 0xB4, 0xF1, 0xE7, 0xA8], {}),
    # MSZ 7795/3 (Hungarian)
    "ir086": ([None, 0xA4, 0xC1, 0xC9, 0xD6, 0xDC, None, None, 
                           0xE1, 0xE9, 0xF6, 0xFC, 0x2DD], {}),
    # JIS X 9010 set for OCR-A font
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x28 is not (.
    # Violation of ECMA-6:1991: 0x29 is not ).
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    # Violation of ECMA-6:1991: lowercase letters omitted.
    "ir091": ([0xA3, None, -1, -1, 0xA5, 0x2442, -1, -1, 
                           -1, -1, None, -1, -1], dict([
        *{
            0x21: -1,
            0x28: 0x007B,
            0x29: 0x007D,
            0x3C: 0x2440,
            0x3E: 0x2441,
        }.items(),
        *[(i, -1) for i in range(0x61, 0x7B)]])),
    # JIS X 9010 primary set for OCR-B font
    "ir092": ([None, None, None, None, 0xA5, None, None, None, 
                           -1, None, None, None, -1], {}),
    # JIS X 9010 Roman set for JIS X 9008 font
    # Violation of ECMA-6:1991: lowercase letters omitted.
    "ir094": ([None, None, None, None, 0xA5, None, None, None, 
                           -1, -1, None, -1, -1], dict((i, -1) for i in range(0x61, 0x7B))),
    # LHS of IBM code page 4993
    # Violation of ECMA-6:1991: lowercase letters omitted.
    "ir094/ibm": ([None, None, None, -1, 0xA5, -1, -1, None, 
                               -1,   -1, None, -1, 0x203E],
                  dict((i, -1) for i in range(0x61, 0x7B))),
    # T.61 subset of IRV as in the IR-102 chart
    "ir102": ([None, 0xA4, None, None, -1, None, -1, None, 
                           -1, -1, None, -1, -1], {}),
    # T.61 subset of IRV by strict definition without the two alternative-choice characters
    "ir102/strict": ([-1, -1, None, None, -1, None, -1, None, 
                              -1, -1, None, -1, -1], {}),
    # IBM's reduced invariant set for ASN.1 (IBM code page 61710)
    # Violation of ECMA-6:1991: 0x21 is omitted.
    # Violation of ECMA-6:1991: 0x22 is omitted.
    # Violation of ECMA-6:1991: 0x25 is omitted.
    # Violation of ECMA-6:1991: 0x26 is omitted.
    # Violation of ECMA-6:1991: 0x2A is omitted.
    # Violation of ECMA-6:1991: 0x3B is omitted.
    # Violation of ECMA-6:1991: 0x3C is omitted.
    # Violation of ECMA-6:1991: 0x3E is omitted.
    # Violation of ECMA-6:1991: 0x5F is omitted.
    "ir102/ibm": ([-1, -1, -1, -1, -1, -1, -1, -1, 
                            -1, -1, -1, -1, -1],
                  {0x21: -1, 0x22: -1, 0x25: -1, 0x26: -1, 0x2A: -1, 0x3B: -1, 0x3C: -1, 0x3E: -1}),
    # Canadian Standard CSA Z243.4:1985 7-bit set main version (Canadian French)
    "ir121": ([None, None, 0xE0, 0xE2, 0xE7, 0xEA, 0xEE, None, 
                           0xF4, 0xE9, 0xF9, 0xE8, 0xFB], {}),
    # Canadian Standard CSA Z243.4:1985 7-bit set alternative version (Canadian French)
    "ir122": ([None, None, 0xE0, 0xE2, 0xE7, 0xEA, 0xC9, None, 
                           0xF4, 0xE9, 0xF9, 0xE8, 0xFB], {}),
    # JUS I.B1.002 (CROSCII / Croatian / YUSCII for Gajica)
    "ir141": ([None, None, 0x17D, 0x160, 0x110, 0x106, 0x10C, None, 
                           0x17E, 0x161, 0x111, 0x107, 0x10D], {}),
    # NC 99-10:81 (Cuban Spanish)
    "ir151": ([None, 0xA4, None, 0xA1, 0xD1, None, 0xBF, None, 
                           None, 0xB4, 0xF1, 0x5B, 0xA8], {}),
    # Invariant subset of ECMA-6
    "ir170": ([-1, -1, -1, -1, -1, -1, -1, None, 
                       -1, -1, -1, -1, -1], {}),
    # Invariant subset of DEC NRCS
    # Violation of ECMA-6:1991: 0x5F is omitted.
    "ir170/dec": ([-1, None, -1, -1, -1, -1, -1, -1, 
                             -1, -1, -1, -1, -1], {}),
    # Invariant subset of Roman G0 set of ETS 300 706
    # Violation of ECMA-6:1991: 0x5F is omitted.
    "ir170/ets": ([-1, -1, -1, -1, -1, -1, -1, -1, 
                           -1, -1, -1, -1, -1], {}),
    # IBM's version of the invariant set (IBM code page 61700)
    # Violation of ECMA-6:1991: 0x21 is omitted.
    "ir170/ibm": ([-1, -1, -1, -1, -1, -1, -1, None, 
                           -1, -1, -1, -1, -1], {0x21: -1}),
    # I.S. 433 (Irish Gaelic)
    "ir207": ([0xA3, None, 0xD3, 0xC9, 0xCD, 0xDA, 0xC1, None, 
                           0xF3, 0xE9, 0xED, 0xFA, 0xE1], {}),
    ##
    # DEC NRCS for Switzerland; IBM's 1021
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/decswiss": ([0xF9, None, 0xE0, 0xE9, 0xE7, 0xEA, 0xEE, 0xE8, 
                                     0xF4, 0xE4, 0xF6, 0xFC, 0xFB], {}),
    # DEC NRCS for the Netherlands; IBM's 1102
    "alt646/decdutch": ([0xA3, None, 0xBE, 0x133, 0xBD, 0x7C, None, None, 
                                     None, 0xA8, 0x192, 0xBC, 0xB4], {}),
    # Icelandic versions; see https://timarit.is/page/2356282#page/n3/mode/2up
    "alt646/icelandic": ([0xA3, None, 0xD0, 0xDE, 0xB4,  0xC6, 0xD6, None, 
                                      0xF0, 0xFE, 0x2CA, 0xE6, 0xF6], {}),
    "alt646/icelandic/alt": ([None, 0xA4, 0xD0, 0xDE, 0xB4,  0xC6, 0xD6, None, 
                                          0xF0, 0xFE, 0x2CA, 0xE6, 0xF6], {}),
    # Projection from DP94 set of EBCDIC code page 871 for Icelandic
    "alt646/icelandic/ibm": ([None, None, 0xD0, 0xDE, 0xB4, 0xC6, 0xD6, None, 
                                          0xF0, 0xFE, 0xA6, 0xE6, 0xF6], {}),
    # PN⁠-⁠T⁠-⁠42109-02-ZU0 for Polish
    "alt646/polish": ([None, 0xA4, 0x119, 0x17A, 0x141, 0x144, 0x15B, None, 
                                   0x105, 0xF3,  0x142, 0x17C, 0x107], {}),
    # PN⁠-⁠T⁠-⁠42109-02-ZU0 variant with Polish Złoty sign
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/polish/zloty": ([None, (0x7A, 0x200D, 0x142), 
                            0x119, 0x17A, 0x141, 0x144, 0x15B, None, 
                            0x105, 0xF3,  0x142, 0x17C, 0x107], {}),
    # PN⁠-⁠T⁠-⁠42109-03-ZU2 for Polish (supplementary set)
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x26 is not &.
    # Violation of ECMA-6:1991: 0x27 is not '.
    # Violation of ECMA-6:1991: 0x2A is not *.
    # Violation of ECMA-6:1991: 0x3B is not ;.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/polish/complete-uppercase": ([0x118, 0x106, 0x119, 0x17A, 0x141, 0x144, 0x15B, None, 
                                                        0x105, 0xF3,  0x142, 0x17C, 0x107],
                                         {0x26: 0x17B, 0x27: 0xD3,  0x2A: 0x179,
                                          0x3B: 0x104, 0x3C: 0x143, 0x3E: 0x15A}),
    # PN⁠-⁠T⁠-⁠42109-02-ZU0 variant projected from DP94-range subset of EBCDIC code page 252 for Polish
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    "alt646/polish/ibm": ([None, 0xA4, 0x119, 0x17A, 0x141, 0x144, 0x15B, None, 
                                       0x105, 0xF3,  0x142, 0x17C, 0x107], {0x27: 0xB4}),
    # PN⁠-⁠I-⁠10050 for Polish with Euro sign
    "alt646/newpolish": ([None, None, None,   0x104, 0x118, 0x141, 0x17B, None, 
                                      0x20AC, 0x105, 0x119, 0x142, 0x17C], {}),
    # ICT 1900 character set, standardised in Poland as PN⁠-⁠T⁠-⁠42109-02-ZU1
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/ict1900": ([None, 0xA3, None, None, 0x24, None, 0x2191, 0x2190, 
                                    0x5F, -1,   -1,   -1,   -1], {}),
    # Maltese version (Star Micronics code page 3041)
    "alt646/maltese": ([None, None, None,  0x121, 0x17C, 0x127, None, None, 
                                    0x10B, 0x120, 0x17B, 0x126, 0x10A], {}),
    ##
    # Roman G0 set of ETS 300 706 for French
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsfrench": ([0xE9, 0xEF, 0xE0, 0xEB, 0xEA, 0xF9, 0xEE, 0x2317, 
                                      0xE8, 0xE2, 0xF4, 0xFB, 0xE7], {}),
    # Roman G0 set of ETS 300 706 for Spain and Portugal
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsiberian": ([0xE7, None, 0xA1, 0xE1, 0xE9, 0xED, 0xF3, 
                                 0xFA, 0xBF, 0xFC, 0xF1, 0xE8, 0xE0], {}),
    # Roman G0 set of ETS 300 706 for Estonia
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsestonian": ([None, 0xF5, 0x160, 0xC4, 0xD6, 0x17D, 0xDC, 
                                  0xD5, 0x161, 0xE4, 0xF6, 0x17E, 0xFC], {}),
    # Roman G0 set of ETS 300 706 for Lithuania and Latvia
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsbaltic": ([None, None, 0x160, 0x117, 0x119, 0x17D, 0x10D, 0x16B, 
                                      0x161, 0x105, 0x173, 0x17E, 0x12F], {}),
    # Roman G0 set of ETS 300 706 for West South Slavic languages
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤ (except in the alternate version).
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsgajica": ([None, 0xCB, 0x10C, 0x106, 0x17D, 0x110, 0x160,
                                0xEB, 0x10D, 0x107, 0x17E, 0x111, 0x161], {}),
    "alt646/etsgajica/dollar": ([None, None, 0x10C, 0x106, 0x17D, 0x110, 0x160,
                                       0xEB, 0x10D, 0x107, 0x17E, 0x111, 0x161], {}),
    # Roman G0 set of ETS 300 706 for Czech and Slovak
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤ (except in the alternate version).
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsczechoslovak": ([None, 0x16F, 0x10D, 0x165, 0x17E, 0xFD, 0xED,
                                      0x159, 0xE9,  0xE1,  0x11B, 0xFA, 0x161], {}),
    # Roman G0 set of ETS 300 706 for Polish
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etspolish": ([None, 0x144, 0x105, (0x7A, 0x200D, 0x142), 
                                              0x15A, 0x141, 0x107, 0xF3, 
                                0x119, 0x17C, 0x15B, 0x142, 0x17A], {}),
    # Roman G0 set of ETS 300 706 for Romanian
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsromanian": ([None, 0xA4, 0x21A, 0xC2, 0x218, 0x102, 0xCE, 0x131, 
                                        0x21B, 0xE2, 0x219, 0x103, 0xEE], {}),
    # Roman G0 set of ETS 300 706 for Turkish
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "alt646/etsturkish": ([(0x54, 0x200D, 0x4C), 
                          0x11F, 0x130, 0x15E, 0xD6, 0xC7, 0xDC,
                          0x11E, 0x131, 0x15F, 0xF6, 0xE7, 0xFC], {}),
    # DEC 7-bit Turkish, related to but not identical to the ETS set.
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x26 is not &.
    "alt646/decturkish": ([None, None, 
                          0x130, 0x15E, 0xD6, 0xC7, 0xDC, None,
                          0x11E, 0x15F, 0xF6, 0xE7, 0xFC], {0x21: 0x131, 0x26: 0x11F}),
    ##
    # Projection from DP94-range subset of EBCDIC code page 24
    "alt646/ibmbritish": ([0xA3, None, None, None, 0xBD, None, 0xB5, None,
                                       0xB1, 0xB2, 0x23, 0xB3, 0xB0], {}),
    # Projection from DP94 set of EBCDIC code page 275
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmbrazil": ([0xD5, 0xC7, 0xC3, 0xC9, None, 0x24, None, None,
                                      0xE3, 0xF5, 0xE7, 0xE9, None], {}),
    # Projection from DP94 set of EBCDIC code page 384
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmbrazil/38xx": ([0xD5, 0xC7, 0xC3, 0xC9, None, 0x24, 0xAC, None,
                                           0xE3, 0xF5, 0xE7, 0xE9, -1], {}),
    # Projection from DP94 set of EBCDIC code page 260 or 276
    "alt646/ibmquebec": ([None, None, None, 0xE0, 0xB8, 0xB4, None, None,
                                      None, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # Projection from DP94-range subset of EBCDIC code page 11
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmquebec/wp": ([None, None, None, 0xA2, 0xB8, 0xB4, None, None,
                                         None, 0xE9, 0xB0, 0xB3, 0xA8],
                            {0x22: 0xB2, 0x3C: 0xAB, 0x3E: 0xBB}),
    # Projection from DP94 set of EBCDIC code page 277
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmdanish": ([0xC6, 0xC5, 0xD8, 0x23, None, 0xA4, None, None,
                                      None, 0xE6, 0xF8, 0xE5, 0xFC], {}),
    # Projection from DP94 set of EBCDIC code page 1142
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmdanish/euro": ([0xC6, 0xC5, 0xD8, 0x23, None, 0x20AC, None, None,
                                           None, 0xE6, 0xF8, 0xE5,   0xFC], {}),
    # Projection from DP94 set of EBCDIC code page 278
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmswedish": ([0xC4, 0xC5, 0xD6, 0xA7, 0xC9, 0xA4, None, None,
                                       0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # Projection from DP94 set of EBCDIC code page 1143
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmswedish/euro": ([0xC4, 0xC5, 0xD6, 0xA7, 0xC9, 0x20AC, None, None,
                                            0xE9, 0xE4, 0xF6, 0xE5,   0xFC], {}),
    # Projection from DP94 set of EBCDIC code page 282
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "alt646/ibmportugal": ([0xC3, None, 0xD5, None, 0xC7, None, None, None,
                                        None, 0xE3, 0xF5, 0xB4, 0xE7], {}),
    # Projection from DP94 set of EBCDIC code page 322, 905, 1026, 1155 or 1175
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmturkish": ([0xD6, 0x0130, 0x015E, 0xC7, 0xFC,   0x011E, None, None,
                                         0x0131, 0xE7, 0x015F, 0x011F, 0xF6], {0x22: 0xDC}),
    # Projection from DP94-range subset of EBCDIC code page 361
    "alt646/ibm38xx": ([None, None, None, None, None, None, 0xAC, None,
                                    -1,   None, None, None, -1], {}),
    # Projection from DP94-range subset of EBCDIC code page 423
    "alt646/ibmusedwithgreek": ([0xA3, None, 0xA7, None, 0xB0, None, None, None,
                                             None, 0xB8, None, 0xB4, 0xA8], {}),
    # Projection from DP94-range subset of EBCDIC code page 4519
    "alt646/ibmusedwithgreek/small": ([0xA3, None, 0xA7, None, 0xB0, None, None, None,
                                                   None, 0xB8, -1,   0xB4, 0xA8], {}),
    # Projection from DP94-range subset of EBCDIC code page 410
    "alt646/ibmusedwithcyrillic": ([None, None, None, None, None, None, None, None,
                                                0xA7, 0xA4, None, 0xB2, 0xB3], {}),
    # Projection from DP94-range subset of EBCDIC code page 4976
    "alt646/ibmusedwithcyrillic/small": ([None, None, None, None, None, None, 0x2303, None,
                                                      -1,   -1,   None, -1,   -1], {}),
    # Projection from DP94-range subset of EBCDIC code page 2056
    "alt646/ibmdcfbelgium": ([None, None, None,   None, None, None, None, None,
                                          0x25A0, None, 0xA6, None, 0x2070], {}),
    #
    # Projection from DP94-range subset of EBCDIC code page 1303
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmbarcode": ([None, None, None, -1,   None, 0x21, -1, None, 
                                       None, None, -1,   None, None], {0x21: 0x2503}),
    # Projection from DP94-range subset of EBCDIC code page 1002
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmdcf": ([None, None, None, 0xA2, None, 0x21, 0xAC, None, 
                                   -1,   -1,   -1,   -1,   -1], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 1068
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmdcf/braces": ([None, None, None, 0xA2, None, 0x21, 0xAC, None, 
                                          -1,   None, -1,   None, -1], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 1003
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmdcf/degreesign": ([None, None, None, 0xA2, None, 0x21, 0xAC, None, 
                                              -1,   -1,   -1,   -1,   0xB0], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 39
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmisrael": ([None, 0xA3, None, 0x24, 0xBD, 0x21, 0xB5, None, 
                                      0xB1, 0xB2, 0x5D, 0xB3, 0xB0], {0x21: 0x5B}),
    # Projection from DP94-range subset of EBCDIC code page 298
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmjapan": ([None, None, None, 0xA2, 0xA5, 0x21, 0xAC, None, 
                                     None, None, 0xA6, None, None], {0x21: 0x7C}),
    # IBM code page 9089
    "alt646/ibmjapan/tiny": ([None, None, None, -1,   -1,   -1,   -1, None, 
                                          None, None, None, None, -1], {}),
    # Projection from DP94-range subset of EBCDIC code page 1027
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmjapan/noyen": ([None, None, None, 0xA2, None, 0x21, 0xAC, None, 
                                           None, None, -1,   None, None], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 281
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmjapan/swapyen": ([None, 0xA5, None, 0xA3, 0x24, 0x21, 0xAC, None, 
                                             None, None, 0xA6, None, 0x203E], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 833
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmkorea": ([None, None, None, 0xA2, 0x20A9, 0x21, 0xAC, None, 
                                     None, None, 0xA6,   None, None], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 9025
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmkorea/small": ([None, None, None, -1,   0x20A9, 0x21, -1, None, 
                                           None, None, -1,     None, None], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 2105
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmlcs": ([None, None, None, 0xA2, -1, 0x21, 0xAC, None, 
                                   -1,   -1,   -1, -1,   0xB0], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 6201
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmlcs/big": ([None, None, None, 0xA2, None, 0x21, 0xAC, None, 
                                       -1,   -1,   0xA6, -1,   0xB0], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 284
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "alt646/ibmspanish": ([0xD1, None, None, None, None, None, 0xAC, None, 
                                       None, None, 0xF1, None, 0xA8], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 392
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "alt646/ibmspanish/38xx": ([0xD1, None, None, None, None, None, 0xAC, None, 
                                      -1,   None, 0xF1, None, -1], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 283
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmspanish/peseta": ([0xD1, 0x20A7, None, None, None, None, 0xAC, None, 
                                                None, None, 0xF1, None, 0xA8], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 285
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmuk": ([None, 0xA3, None, 0x24, None, 0x21, 0xAC, None, 
                                  None, None, 0xA6, None, 0x203E], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 40
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not <.
    "alt646/ibmuk/wp": ([-1, 0xA3, None, 0x24, 0xBD, 0x21, -1, None,
                                   -1,   -1,   0xBE, -1,   -1],
                        {0x21: 0xBC, 0x3C: -1, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 2116
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmuk/dcf": ([None, 0xA3, None, 0x24, None, 0x21, 0xAC, None, 
                                      -1,   -1,   -1,   -1,   -1], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 37
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmusa": ([None, None, None, 0xA2, None, 0x21, 0xAC, None, 
                                   None, None, 0xA6, None, None], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 24613
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmusa/asciinohatsqb": ([None, None, None, -1,   None, 0x21, -1, None, 
                                                 None, None, -1,   None, None], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 5413
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmusa/asciinosqb": ([None, None, None, -1,   None, 0x21, None, None, 
                                              None, None, -1,   None, None], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 1047
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmusa/hat": ([None, None, None, 0xA2, None, 0x21, None, None, 
                                       None, None, 0xA6, None, None], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 32805
    # Violation of ECMA-6:1991: 0x21 is not !.
    "alt646/ibmusa/tiny": ([None, None, None, -1,   -1, 0x21, -1, None, 
                                        None, None, -1, None, -1], {0x21: 0x7C}),
    # Projection from DP94-range subset of EBCDIC code page 9028
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibmschsmall": ([None, -1, None, -1,   0x24, 0x21, -1, None, 
                                      None, None, -1,   None, -1], {0x21: 0x7C}),
    # Left-hand side of IBM code page 1008
    # Violation of ECMA-6:1991: 0x25 is not (strictly) %.
    # Violation of ECMA-6:1991: 0x2A is not (strictly) *.
    "alt646/ibmarabic": ([None, None, None, None, None, None, None, None, 
                                      None, None, None, None, None],
                         {0x25: 0x066A, 0x2A: 0x066D}),
    # Left-hand side of IBM code page 13152
    # Violation of ECMA-6:1991: 0x25 is not (strictly) %.
    # Violation of ECMA-6:1991: 0x2A is not (strictly) *.
    "alt646/ibmarabic/tiny": ([None, None, None, -1, -1,   -1, -1, None, 
                                           -1,   -1, None, -1, -1],
                              {0x25: 0x066A, 0x2A: 0x066D}),
    # Left-hand side of IBM code page 906
    "alt646/ibm-minus3": ([None, None, None, None, None, None, -1, None,
                                       -1,   None, None, None, -1], {}),
    # Left-hand side of IBM code page 4947
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "alt646/ibm-minus6": ([-1, None, -1,   None, -1,   None, None, None,
                                     None, -1,   None, -1,   -1], {}),
    # Left-hand side of IBM code page 8629
    "alt646/ibm-minus7": ([None, None, -1,   -1,   -1, -1, None, None,
                                       None, -1, None, -1, -1], {}),
    # Left-hand side of IBM code page 16821
    "alt646/ibm-minus8": ([None, None, None, -1, -1, -1, None, None,
                                             -1,   -1, -1, -1, -1], {}),
    # Left-hand side of IBM code page 12725; DP94-range subset of IBM code pages 12544 and 12788
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "alt646/ibm-minus10": ([-1, None, -1, -1, -1, -1, None, None,
                                      -1, -1, -1, -1, -1], {}),
    # Left-hand side of IBM code page 1044
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    # Violation of ECMA-6:1991: 0x3F is not ?.
    # Violation of ECMA-6:1991: 0x5F is not _.
    # Violation of ECMA-6:1991: lowercase letters omitted.
    "alt646/ibm-minus41": ([-1, None, -1, -1, None, -1, -1, -1,
                                      -1, -1, -1,   -1, -1], dict([
        *{0x21: -1, 0x3C: -1, 0x3E: -1, 0x3F: -1}.items(),
        *[(i, -1) for i in range(0x61, 0x7B)]])),
    # Galaksija encoding for Gajica
    # Violation of ECMA-6:1991: 0x27 is not '.
    # Violation of ECMA-6:1991: lowercase letters omitted.
    "alt646/galaksija": ([None, None, 0x2962, 0x010C, 0x0106, 0x017D, 0x0160, None,
                                      -1, -1, -1, -1, -1], dict([
        *{0x27: 0x1F896}.items(),
        *[(i, -1) for i in range(0x61, 0x7B)]])),
    # Galaksija encoding for Gajica, extended with lowercase forms
    # Violation of ECMA-6:1991: 0x27 is not '.
    "alt646/galaksija/extended": ([None, None, 0x2962, 0x010C, 0x0106, 0x017D, 0x0160, None,
                                               None,   0x010D, 0x0107, 0x017E, 0x0161],
                                  {0x27: 0x1F896}),
    # HP 7-bit "Gothic Legal" (with e.g. trademark / section signs) encoding; IBM code page 1052.
    # Violation of ECMA-6:1991: 0x22 is not (strictly) ".
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/hplegal": ([None, None, None, None, 0xAE, None,   0xA9, None,
                                    0xB0, 0xA7, 0xB6, 0x2020, 0x2122],
                       {0x22: 0x2033, 0x27: 0x2032, 0x3C: 0x2017, 0x3E: 0xA2}),
    # Left-hand site of FreeDOS code page 60258
    # Violation of ECMA-6:1991: 0x49 is not (strictly) I.
    "alt646/freedos-turkic": ([None, None, None, None, None, None, None, None,
                                           None, None, None, None, None], {0x49: 0x0130}),
    # Left-hand site of FreeDOS code page 899
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    "alt646/freedos-armenian": ([None, None, None,   None, None, None, None, None,
                                             0x055D, None, None, None, 0x055C], {0x27: 0x055B}),
    # Projection from DP94-range subset of EBCDIC code page 1
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-usa-wp": ([None, None, None, None, 0xBC, None, 0xA2, None,
                                       0xB1, 0xB2, 0xBD, 0xB3, 0xB0],
                          {0x3C: 0xA7, 0x3E: 0xB6}),
    # Projection from DP94-range subset of EBCDIC code page 5
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-usa-wp/small": ([None, None, None, -1, 0xBC, -1, 0xA2, None,
                                             0xB1, -1, 0xBD, -1, -1],
                                {0x21: -1, 0x3C: -1, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 2
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-usa-alternative": ([None, None, None, None, -1,   None, 0xA2, None,
                                                -1,   -1,   0xAE, -1,   0xB0],
                                   {0x21: -1, 0x3C: -1, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 3
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-usa-accounting/a": ([None, None, None, -1, 0xBC,   -1, 0xA2, None,
                                                 -1,   -1, 0x2017, -1, -1],
                                    {0x21: 0xA3, 0x3C: -1, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 4
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-usa-accounting/b": ([None, None, None, 0xA3, -1,     -1, 0xA2, None,
                                                 -1,   -1,   0x2017, -1, -1],
                                    {0x3C: -1, 0x3E: -1}),
    # Hybrid of the two above
    "alt646/ibm-usa-accounting": ([None, None, None, 0xA3, 0xBC,   -1,   0xA2, None,
                                               None, None, 0x2017, None, None], {}),
    # Projection from DP94-range subset of EBCDIC code page 6
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-latin-america-wp": ([None, None, 0xBF, None, 0xD1, None, 0xA8, None,
                                                 0xB4, 0xA3, 0xF1, 0xA1, 0xB0],
                                    {0x3C: 0xBD, 0x3E: 0xBC}),
    # Projection from DP94-range subset of EBCDIC code page 10
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-canada-english-wp": ([None, None, None, None, 0xBC, None, 0xA2, None,
                                                  0xB1, 0xB2, 0xBD, 0xB3, 0xB0],
                                     {0x3C: 0xA3, 0x3E: 0xB6}),
    # Projection from DP94-range subset of EBCDIC code page 13
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmdutch": ([0xA3, None, 0x192, 0xA7, 0xBC, 0xB4, None, None,
                                     None,  0xB2, 0xBD, 0xB3, 0xA8],
                            {0x3C: 0xB1, 0x3E: 0xB0}),
    # Projection from DP94-range subset of EBCDIC code page 14
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-spain-wp": ([0x20A7, None, 0xBF, 0xE7, 0xD1, 0xB4, None, None,
                                           None, 0xBD, 0xF1, 0xA1, 0xA8],
                            {0x3C: 0xBA, 0x3E: 0xAA}),
    # Projection from DP94-range subset of EBCDIC code page 15
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x3B is not ;.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-swiss-french-wp": ([-1, None, 0xE7, 0xE0, 0xE9, 0xE8, None, None,
                                              0xF9, -1,   -1,   -1,   0xA8],
                                   {0x21: -1, 0x3B: -1, 0x3C: 0xBD, 0x3E: 0xBC}),
    # Projection from DP94-range subset of EBCDIC code page 16
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-switzerland-wp": ([0xA3, None, 0xE7, 0xE0, 0xE9, 0xE8, None, None,
                                               None, 0xE4, 0xF6, 0xFC, 0xA8],
                                  {0x21: 0xB4, 0x3C: 0xA7, 0x3E: 0xB0}),
    # Projection from DP94-range subset of EBCDIC code page 17
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x3B is not ;.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-swiss-german-wp": ([-1, None, 0xE7, -1,   0xE9, -1,   None, None,
                                              None, 0xE4, 0xF6, 0xFC, -1],
                                   {0x21: -1, 0x3B: -1, 0x3C: 0xA7, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 18
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x2A is not *.
    # Violation of ECMA-6:1991: 0x3B is not ;.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-sweden-finland-wp": ([0xA3, -1, 0xA7, 0xC4, 0xD6, 0xC5, -1, None,
                                                None, 0xE4, 0xF6, 0xE5, 0xB4],
                                     {0x21: -1, 0x2A: 0xFC, 0x3B: -1, 0x3C: -1, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 21
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-brazil-wp": ([0xA3, None, 0xAA, 0xA7, 0xC7, 0x7C, None, None,
                                          None, 0xBA, 0xE7, 0xB4, None],
                             {0x3C: 0xB2, 0x3E: 0xB3}),
    # Projection from DP94-range subset of EBCDIC code page 22
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-portugal-wp": ([0xA3, None, 0xAA, 0xA7, 0xC7, 0x7C, None, None,
                                            None, 0xBA, 0xE7, 0xB4, None],
                               {0x3C: 0x131, 0x3E: 0xA8}),
    # Projection from DP94-range subset of EBCDIC code page 23
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-uk-wp": ([0xA3, None, None, 0xBC, 0xBD, 0xBE, -1, None,
                                      -1,   -1,   -1,   -1,   -1],
                         {0x3C: -1, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 25
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-japan-wp/small": ([None, None, None, 0xA3, 0xA5, 0xB0, -1, None,
                                               -1,   -1,   -1,   -1,   -1],
                                  {0x21: 0xB1, 0x3C: -1, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 26
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-japan-wp": ([None, None, None, 0xA3, 0xA5, 0xB0, None, None,
                                         None, 0xA8, 0xB4, 0xA8, None],
                            {0x3C: 0xDF, 0x3E: 0xE7}),
    # Projection from DP94-range subset of EBCDIC code page 27
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-greece-wp": ([0xA3, None, None, 0xB0, 0xA2, 0xB8, None, None,
                                          None, 0xA8, 0xB4, 0xA8, None],
                             {0x3C: 0xBD, 0x3E: 0xBC}),
    # Projection from DP94-range subset of EBCDIC code page 29
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-iceland-wp": ([0xA3, None, 0xD0, 0xC6, 0xD6, 0xC5, 0xB0, None,
                                           0xF0, 0xE6, 0xF6, 0xE5, 0xA8],
                              {0x27: 0xB4, 0x3C: 0xDE, 0x3E: 0xFE}),
    # Projection from DP94-range subset of EBCDIC code page 30
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x26 is not &.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibm-turkish-wp": ([0x5E, 0x131, 0xE9, 0xC7, 0xD6, 0xDC, 0x11E, None,
                                            None, 0xE7, 0xF6, 0xFC, 0x11F],
                              {0x26: 0x130, 0x3C: 0x15F, 0x3E: 0x15E}),
    # Projection from DP94-range subset of EBCDIC code page 31
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmafrikaans": ([0xA3, None, None, 0xF7, 0xB4,  0x2113, None, None,
                                         None, 0xB2, 0x149, 0xB3,   0xA8],
                            {0x3C: 0xB0, 0x3E: 0xBD}),
    # Projection from DP94-range subset of EBCDIC code page 32
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x26 is not &.
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    # Violation of ECMA-6:1991: 0x2A is not *.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    # Violation of ECMA-6:1991: 0x25, 0x28, 0x29, 0x3B and 0x3D are omitted.
    "alt646/ibmczech/small": ([0x159, 0x161, 0x17E, -1,   0xED,  0x11B, 0x2C7, None,
                                             0xB4,  0xFD, 0x10D, 0xE1,  0xA8],
                              {0x25: -1, 0x26: 0xFA, 0x27: 0x60, 0x28: -1, 0x29: -1, 0x2A: 0x16F,
                               0x3B: -1, 0x3C: 0xE9, 0x3D: -1, 0x3E: 0xA7}),
    # Projection from DP94-range subset of EBCDIC code page 33
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x26 is not &.
    # Violation of ECMA-6:1991: 0x2A is not *.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmczech": ([0x159, 0x161, 0x17E, 0x2DA, 0xED,  0x11B, 0x2C7, None,
                                       0xB4,  0xFD,  0x10D, 0xE1,  0xA8],
                        {0x26: 0xFA, 0x2A: 0x16F, 0x3C: 0xE9, 0x3E: 0xA7}),
    # Projection from DP94-range subset of EBCDIC code page 34
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x26 is not &.
    # Violation of ECMA-6:1991: 0x27 is not '.
    # Violation of ECMA-6:1991: 0x2A is not *.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmslovak": ([0x13E, 0x161, 0x17E, 0x2DA, 0xED,  0x165, 0x2C7, None,
                                        0xB4,  0xFD,  0x10D, 0xE1,  0xE4],
                         {0x26: 0xFA, 0x27: 0x148, 0x2A: 0xF4, 0x3C: 0xE9, 0x3E: 0xA7}),
    # Projection from DP94-range subset of EBCDIC code page 35
    # Violation of ECMA-6:1991: 0x26 is not &.
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    # Violation of ECMA-6:1991: 0x2A is not *.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmromanian/small": ([0xA3, None, -1,   -1,    -1,   -1,   None, None,
                                              None, 0x103, 0xEE, 0xE2, 0xA8],
                                 {0x26: -1, 0x27: 0xB4, 0x2A: 0x163, 0x3C: 0x15F, 0x3E: -1}),
    # Projection from DP94-range subset of EBCDIC code page 36
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    # Violation of ECMA-6:1991: 0x2A is not *.
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmromanian": ([0xA3, None, 0x162, 0x102, 0xCE, 0xC2, 0xB8, None,
                                        None,  0x103, 0xEE, 0xE2, 0xA8],
                           {0x27: 0xB4, 0x2A: 0x163, 0x3C: 0x15F, 0x3E: 0x15E}),
    # Projection from DP94-range subset of EBCDIC code page 251
    # Violation of ECMA-6:1991: 0x3C is not <.
    # Violation of ECMA-6:1991: 0x3E is not >.
    "alt646/ibmhongkong": ([None, None, None, None, 0xBC, None, 0xA3, None,
                                        0xB1, 0xB2, 0xBD, 0xB3, 0xB0],
                           {0x3C: 0xA7, 0x3E: 0xB6}),
    # Projection from DP94-range subset of EBCDIC code page 286
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibm-3270-german": ([0xC4, 0xDC, 0xD6, 0xF6, -1,   0xFC, 0xAC, None,
                                            -1,   -1,   0xDF, -1,   -1],
                               {0x21: 0x7C, 0x22: 0xE4}),
    # Projection from DP94-range subset of EBCDIC code page 287
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibm-3270-denmark-norway": ([0xC6, 0xC5, 0xD8, 0xF8, -1,   0xE5, 0xAC, None,
                                                    -1,   -1,   0xA6, -1,   -1],
                                       {0x21: 0x7C, 0x22: 0xE6}),
    # Projection from DP94-range subset of EBCDIC code page 288
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibm-3270-sweden-finland": ([0xC4, 0xC5, 0xD6, 0xF6, -1,   0xE5, 0xAC, None,
                                                    -1,   -1,   0xA6, -1,   -1],
                                       {0x21: 0x7C, 0x22: 0xE4}),
    # Projection from DP94-range subset of EBCDIC code page 289
    # Violation of ECMA-6:1991: 0x21 is not !.
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/ibm-3270-spanish": ([0xD1, 0x20A7, None, 0xA2, -1,   0x21, 0xAC, None,
                                               -1,   -1,   0xA6, -1,   -1],
                                {0x21: 0x7C, 0x22: 0xF1}),
}

for (name, (myvars, override)) in raw_variants.items():
    myset = list((i,) for i in range(0x21, 0x7F))
    for frm, to in list(zip(variants, myvars)) + list(override.items()):
        if to is not None:
            if to != -1:
                myset[frm - 0x21] = to if isinstance(to, tuple) else (to,)
            else:
                myset[frm - 0x21] = None
    graphdata.gsets[name] = (94, 1, tuple(myset))

graphdata.chcpdocs['367'] = graphdata.chcpdocs['895'] = graphdata.chcpdocs['1009'] = graphdata.chcpdocs['1010'] = graphdata.chcpdocs['1011'] = graphdata.chcpdocs['1012'] = graphdata.chcpdocs['1013'] = graphdata.chcpdocs['1014'] = graphdata.chcpdocs['1015'] = graphdata.chcpdocs['1016'] = graphdata.chcpdocs['1017'] = graphdata.chcpdocs['1018'] = graphdata.chcpdocs['1019'] = graphdata.chcpdocs['1020'] = graphdata.chcpdocs['1021'] = graphdata.chcpdocs['1023'] = graphdata.chcpdocs['1052'] = graphdata.chcpdocs['1054'] = graphdata.chcpdocs['1088'] = graphdata.chcpdocs['1101'] = graphdata.chcpdocs['1102'] = graphdata.chcpdocs['1103'] = graphdata.chcpdocs['1104'] = graphdata.chcpdocs['1105'] = graphdata.chcpdocs['1106'] = graphdata.chcpdocs['1107'] = graphdata.chcpdocs['1114'] = graphdata.chcpdocs['1126'] = graphdata.chcpdocs['5211'] = graphdata.chcpdocs['5222'] = graphdata.chcpdocs['9089'] = graphdata.chcpdocs['9444'] = graphdata.chcpdocs['61697'] = graphdata.chcpdocs['61698'] = graphdata.chcpdocs['61699'] = graphdata.chcpdocs['61700'] = graphdata.chcpdocs['61710'] = 'ecma-35'

graphdata.defgsets['895'] = ('ir014', 'nil', 'nil', 'nil')
graphdata.defgsets['1009'] = ('ir002/tilde', 'nil', 'nil', 'nil')
graphdata.defgsets['1010'] = ('ir069', 'nil', 'nil', 'nil')
graphdata.defgsets['1011'] = ('ir021', 'nil', 'nil', 'nil')
graphdata.defgsets['1012'] = ('ir015', 'nil', 'nil', 'nil')
graphdata.defgsets['1013'] = ('ir004', 'nil', 'nil', 'nil')
graphdata.defgsets['1014'] = ('ir085', 'nil', 'nil', 'nil')
graphdata.defgsets['1015'] = ('ir084', 'nil', 'nil', 'nil')
graphdata.defgsets['1016'] = ('ir060', 'nil', 'nil', 'nil')
graphdata.defgsets['1017'] = ('ir060/dk', 'nil', 'nil', 'nil')
graphdata.defgsets['1018'] = ('ir010', 'nil', 'nil', 'nil')
graphdata.defgsets['1019'] = ('ir006/overline', 'nil', 'nil', 'nil')
graphdata.defgsets['1020'] = ('ir121', 'nil', 'nil', 'nil')
graphdata.defgsets['1021'] = ('alt646/decswiss', 'nil', 'nil', 'nil')
graphdata.defgsets['1023'] = ('ir017', 'nil', 'nil', 'nil')
graphdata.defgsets['1052'] = ('alt646/hplegal', 'nil', 'nil', 'nil')
graphdata.defgsets['1088'] = graphdata.defgsets['1126'] = graphdata.defgsets['5222'] = ('alt646/ksroman/tilde', 'nil', 'nil', 'nil')

graphdata.defgsets['1101'] = ('ir004/dec', 'nil', 'nil', 'nil')
graphdata.defgsets['1102'] = ('alt646/decdutch', 'nil', 'nil', 'nil')
graphdata.defgsets['1103'] = ('ir008-1/dec', 'nil', 'nil', 'nil')
graphdata.defgsets['1104'] = ('ir025', 'nil', 'nil', 'nil')
graphdata.defgsets['1105'] = ('ir009-1/dec', 'nil', 'nil', 'nil')
graphdata.defgsets['1106'] = ('ir011/dec', 'nil', 'nil', 'nil')
graphdata.defgsets['1107'] = ('ir060/dec', 'nil', 'nil', 'nil')
graphdata.defgsets['9089'] = ('alt646/ibmjapan/tiny', 'nil', 'nil', 'nil')

graphdata.defgsets['367'] = graphdata.defgsets['1054'] = graphdata.defgsets['1114'] = graphdata.defgsets['5211'] = graphdata.defgsets['9444'] = ('ir006', 'nil', 'nil', 'nil')
graphdata.defgsets["61697"] = graphdata.defgsets["61698"] = graphdata.defgsets["61699"] = graphdata.defgsets["61700"] = ("ir170/ibm", "nil", "nil", "nil")
graphdata.defgsets['61710'] = ('ir102/ibm', 'nil', 'nil', 'nil')

