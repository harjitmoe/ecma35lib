#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020, 2022, 2023, 2024.

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
    # US-ASCII / New IRV, ISO/IEC 10367 G0 set
    "ir006": ([None, None, None, None, None, None, None, None, 
                           None, None, None, None, None], {}),
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
    # Olivetti Portugese
    "ir016": ([None, None, 0xA7, 0xC3, 0xC7, 0xD5, None, None, 
                           None, 0xE3, 0xE7, 0xF5, 0xB0], {}),
    # Olivetti Spanish
    "ir017": ([0xA3, None, 0xA7, 0xA1, 0xD1, 0xBF, None, None, 
                           None, 0xB0, 0xF1, 0xE7, None], {}),
    # DIN 66 003 (German; also same in DEC and ETS)
    "ir021": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, None, None, 
                           None, 0xE4, 0xF6, 0xFC, 0xDF], {}),
    # DIN 66003 variant projected from EBCDIC code page 9 (as opposed to EBCDIC code page 273, whose
    #   DP94 set (CCSID 4369) corresponds directly to the DIN 66003 map above)
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    "ir021/acute": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, None, None, 
                           None, 0xE4, 0xF6, 0xFC, 0xDF], {0x27: 0xB4}),
    # Projection from DP94-range subset of EBCDIC code page 382
    "ir021/ibm38xx": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, 0xAC, None, 
                                   -1,   0xE4, 0xF6, 0xFC, 0xDF], {}),
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
    # IBM Portugese
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
    # T.61 subset of IRV
    "ir102": ([None, 0xA4, None, None, -1, None, -1, None, 
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
    # CSA Z243.4:1985 primary set main version (Canadian French)
    "ir121": ([None, None, 0xE0, 0xE2, 0xE7, 0xEA, 0xEE, None, 
                           0xF4, 0xE9, 0xF9, 0xE8, 0xFB], {}),
    # CSA Z243.4:1985 primary set alternative version (Canadian French)
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
    # Supposed Icelandic version (close to IBM one below)
    "alt646/icelandic": ([None, 0xA4, 0xD0, 0xDE, None, 0xC6, 0xD6, None, 
                                      0xF0, 0xFE, None, 0xE6, 0xF6], {}),
    # Projection from DP94 set of EBCDIC code page 871
    "alt646/icelandic/ibm": ([None, None, 0xD0, 0xDE, 0xB4, 0xC6, 0xD6, None, 
                                          0xF0, 0xFE, 0xA6, 0xE6, 0xF6], {}),
    # BN-74/3101-01 for Polish (not verified but close to IBM one below)
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "alt646/polish": ([None, (0x7A, 0x200D, 0x142), 
                            0x119, 0x17A, None, 0x144, 0x15B, None, 
                            0x105, 0xF3, 0x142, 0x17C, 0x107], {}),
    # BN-74/3101-01 variant projected from DP94-range subset of EBCDIC code page 252
    # Violation of ECMA-6:1991: 0x27 is not (strictly) '.
    "alt646/polish/ibm": ([None, 0xA4, 0x119, 0x17A, 0x141, 0x144, 0x15B, None, 
                                       0x105, 0xF3, 0x142, 0x17C, 0x107], {0x27: 0xB4}),
    # Compromise of the two above
    "alt646/polish/full": ([None, 0xA4, 0x119, 0x17A, 0x141, 0x144, 0x15B, None, 
                                        0x105, 0xF3, 0x142, 0x17C, 0x107], {}),
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
    # Galaksija encoding for Gajica, extended with lowercase forms
    # Violation of ECMA-6:1991: 0x27 is not '.
    "alt646/galaksija/extended": ([None, None, 0x2962, 0x010C, 0x0106, 0x017D, 0x0160, None,
                                               None,   0x010D, 0x0107, 0x017E, 0x0161],
                                  {0x27: 0x1F896}),
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



