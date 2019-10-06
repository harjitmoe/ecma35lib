#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import graphdata

# ISO/IEC 10367 G0 set (i.e. same as ECMA-6:US, current ECMA-6:IRV, US-ASCII)
graphdata.gsets["ir006"] = (94, 1, tuple(range(0x21, 0x7F)))

# DEC doesn't vary 0x24. ECMA-6:1991 does not vary 0x5F, and puts strict restrictions on permitted
# glyphs for 0x23 (# or £) and 0x24 ($ or ¤), which is deviated from by the Mainland Chinese
# version. ETS 300 706 liberally varies all three.
variants = [0x23, 0x24, 0x40, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x7B, 0x7C, 0x7D, 0x7E]

# Only specifying the changed points. None for unchanged. -1 for unused.
# Dict is for changes to characters invariant even in ETS 300 706 Roman G0.
# Violations of ECMA-6:1991 are acknowledged where applicable.
raw_variants = {
    # Old IRV
    "ir002": ([None, 0xA4, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir002tilde": ([None, 0xA4, None, None, None, None, None, None, 
                                None, None, None, None, None], {}),
    # BS 4730 (United Kingdom)
    "ir004": ([0xA3, None, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir004dec": ([0xA3, None, None, None, None, None, None, None, 
                              None, None, None, None, None], {}),
    # US-ASCII / New IRV
    "ir006": ([None, None, None, None, None, None, None, None, 
                           None, None, None, None, None], {}),
    # NATS-SEFI (Swedish and Finnish Journalism)
    "ir008-1": ([None, None, 0x3000, 0xC4, 0xD6, 0xC5, 0x25A0, None, 
                             0x2007, 0xE4, 0xF6, 0xE5, 0x2013], {}),
    # NATS-DANO (Danish and Norwegian Journalism)
    # Violation of ECMA-6:1991: 0x22 is not ".
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    "ir009-1": ([0xBB, None, 0x3000, 0xC6, 0xD8, 0xC5, 0x25A0, None, 
                             0x2007, 0xE6, 0xF8, 0xE5, 0x2013], {0x22: 0xBA}),
    # SEN 85 02 00 ax B (Swedish and Finnish)
    "ir010": ([None, None, 0xC9, 0xC4, 0xD6, 0xC5, None, None, 
                           None, 0xE4, 0xF6, 0xE5, 0x203E], {}),
    # DEC NRCS for Finland (somewhere between ir010 and ir011)
    "ir010dec": ([None, 0xA4, 0xC9, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                              None, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # SEN 85 02 00 ax C (Swedish names), ETS for Sweden and Finland
    "ir011": ([None, 0xA4, None, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                           0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # DEC NRCS for Sweden (almost the same as ir011)
    "ir011dec": ([None, None, None, 0xC4, 0xD6, 0xC5, 0xDC, None, 
                              0xE9, 0xE4, 0xF6, 0xE5, 0xFC], {}),
    # Roman G0 set of ETS 300 706 for Estonia
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etseesti": ([None, 0xF5, 0x160, 0xC4, 0xD6, 0x17D, 0xDC, 0xD5, 
                              0x161, 0xE4, 0xF6, 0x17E, 0xFC], {}),
    # Roman G0 set of ETS 300 706 for Lithuania and Latvia
    "etsebaltic": ([None, None, 0x160, 0x117, 0x119, 0x17D, 0x10D, 0x16B, 
                                0x161, 0x105, 0x173, 0x17E, 0x12F], {}),
    # JIS C 6220 / JIS X 0201 Roman set
    "ir014": ([None, None, None, None, 0xA5, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    "ir014tilde": ([None, None, None, None, 0xA5, None, None, None, 
                                None, None, None, None, None], {}),
    # KS X 1003 / G0 set of non-ASCII EUC-KR
    "ksroman": ([None, None, None, None, 0x20A9, None, None, None, 
                             None, None, None, None, 0x203E], {}),
    "ksromantilde": ([None, None, None, None, 0x20A9, None, None, None, 
                                  None, None, None, None, None], {}),
    # DIN 66 003 (German; also same in DEC and ETS)
    "ir021": ([None, None, 0xA7, 0xC4, 0xD6, 0xDC, None, None, 
                           None, 0xE4, 0xF6, 0xFC, 0xDF], {}),
    # NF Z 62-010:1973 (old or DEC version French)
    "ir025": ([0xA3, None, 0xE0, 0xB0, 0xE7, 0xA7, None, None, 
                           None, 0xE9, 0xF9, 0xE8, 0xA8], {}),
    # BS_Viewdata (Roman G0 set of ETS 300 706 for United Kingdom)
    # Violation of ECMA-6:1991: 0x5F is not _.
    "ir047": ([0xA3, None, None, 0x2190, 0xBD, 0x2192, 0x2191, 0x2317, 
                           0x2015, 0xBC, 0x2016, 0xBE, 0xF7], {}),
    # Roman G0 set of ETS 300 706 for France
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "etsfrench": ([0xE9, 0xEF, 0xE0, 0xEB, 0xEA, 0xF9, 0xEE, 0x2317, 
                               0xE8, 0xE2, 0xF4, 0xFB, 0xE7], {}),
    # INIS subset of ASCII
    # Violation of ECMA-6:1991: 0x21, 0x22, 0x26, 0x3F and 0x5F are omitted.
    # Violation of ECMA-6:1991: 0x23 is omitted, not # or £.
    "ir049": ([-1, None, -1, None, -1, None, -1, None, 
                         -1, -1, None, -1, -1], {
              0x21: -1, 0x22: -1, 0x26: -1, 0x3F: -1, 0x5F: -1}),
    # Mainland Chinese GB 1988
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "ir057": ([None, 0xA5, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    # NF Z 62-010:1982 (new version French)
    "ir069": ([0xA3, None, 0xE0, 0xB0, 0xE7, 0xA7, None, None, 
                           0xB5, 0xE9, 0xF9, 0xE8, 0xA8], {}),
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
    # DEC NRCS for Switzerland
    # Violation of ECMA-6:1991: 0x23 is not # or £.
    # Violation of ECMA-6:1991: 0x5F is not _.
    "decswiss": ([0xF9, None, 0xE0, 0xE9, 0xE7, 0xEA, 0xEE, 0xE8, 
                              0xF4, 0xE4, 0xF6, 0xFC, 0xFB], {}),
    # Invariant subset of ECMA-6
    "ir170": ([-1, -1, -1, -1, -1, -1, -1, -1, 
                       -1, -1, -1, -1, -1], {}),
    # Invariant subset of DEC NRCS
    # Violation of ECMA-6:1991: 0x5F is omitted.
    "ir170dec": ([-1, None, -1, -1, -1, -1, -1, -1, 
                            -1, -1, -1, -1, -1], {0x5F: -1}),
    # Invariant subset of Roman G0 set of ETS 300 706
    # Violation of ECMA-6:1991: 0x5F is omitted.
    "ir170ets": ([-1, -1, -1, -1, -1, -1, -1, -1, 
                          -1, -1, -1, -1, -1], {0x5F: -1}),
    # I.S. 433 (Irish Gaelic)
    "ir207": ([0xA3, None, 0xD3, 0xC9, 0xCD, 0xDA, 0xC1, None, 
                           0xF3, 0xE9, 0xED, 0xFA, 0xE1], {}),
}

for (name, (myvars, override)) in raw_variants.items():
    myset = list(range(0x21, 0x7F))
    for frm, to in list(zip(variants, myvars)) + list(override.items()):
        if to is not None:
            if to > 0:
                myset[frm - 0x21] = to
            else:
                myset[frm - 0x21] = None
    graphdata.gsets[name] = (94, 1, tuple(myset))






