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
# Dict is for changes to normally invariant characters.
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
    # BS_Viewdata (Roman G0 set of ETS 300 706 for United Kingdom)
    # Violation of ECMA-6:1991: 0x5F is not _.
    "ir047": ([0xA3, None, None, 0x2190, 0xBD, 0x2192, 0x2191, 0x2317, 
                           0x2015, 0xBC, 0x2016, 0xBE, 0xF7], {}),
    # INIS subset of ASCII
    # Violation of ECMA-6:1991: 0x21, 0x22, 0x26, 0x3F and 0x5F are omitted.
    # Violation of ECMA-6:1991: 0x23 is omitted, not # or £.
    "ir049": ([-1, None, -1, None, -1, None, -1, None, 
                         -1, -1, None, -1, -1], {0x21: -1, 0x22: -1, 0x26: -1, 0x3F: -1, 0x5F: -1}),
    # Mainland Chinese GB 1988
    # Violation of ECMA-6:1991: 0x24 is not $ or ¤.
    "ir057": ([None, 0xA5, None, None, None, None, None, None, 
                           None, None, None, None, 0x203E], {}),
    # JIS C 6220 / JIS X 0201 Roman set, OCR subset
    "ir092": ([None, None, None, None, 0xA5, None, None, None, 
                           -1, None, None, None, -1], {}),
    # T.61 subset of IRV
    "ir102": ([None, 0xA4, None, None, -1, None, -1, None, 
                           -1, -1, None, -1, -1], {}),
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






