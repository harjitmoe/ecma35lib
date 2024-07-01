#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2023.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Unicode compatibility ideograph codepoints (from both blocks) whose Unihan source mappings
#   have been replaced by self-references (i.e. they are no longer used for source-separation).
#   Usually, this is because they were found to represent misunifications, and the source standard
#   mapping has been moved to the correct disunified character (or a newer compatibility ideograph
#   which decomposes to the correct unified ideograph).
deprecated_compatibility_ideographs = {
    #0x2F949: 0x04039, # U+FAD4 disunified from U+4039 (to U+9FC3) makes U+2F949 redundant but valid
    #
    0x2F89F: 0x05FF9,
    0x0FAD4: 0x09FC3, # See above.
    #
    0x0F92C: 0x0FA2E,
    0x0F9B8: 0x0FA2F,
    #
    0x2F9B2: 0x270F0,
    0x2F83A: 0x2B738,
    0x2F8FD: 0x2DC09,
    0x2F8A4: 0x317AB,
    0x2F936: 0x31C2D,
    #
    # U+4DB7 was disunified from a unified ideograph (U+53FD) directly, with no CJKCI involved
    0x2F83B: 0x04DB8, # n.b. for some reason, HKSCS ref not moved yet
    0x2F878: 0x04DB9, # n.b. for some reason, HKSCS ref not moved yet
    0x2F8D6: 0x04DBA,
    0x2F8D7: 0x04DBB,
    #0x2F984: 0x0440B, # Disunified other way: U+4DBC takes the CNS 11643 char that had been U+440B
    0x2F8DA: 0x04DBD,
    0x2F8F0: 0x04DBE,
    0x2FA02: 0x04DBF,
    # Note that U+FA99, U+FAB0 and U+FAD1 are candidates for future disunification and deprecation
    #   when the CJK-K block gets added in however many years' time:
    # https://appsrv.cse.cuhk.edu.hk/~irg/irg/irg57/IRGN2510_Disunify-3-chars.pdf
}

def remove_deprecated_cjkci(pointer, ucs):
    if len(ucs) == 1 and ucs[0] in deprecated_compatibility_ideographs:
        return (deprecated_compatibility_ideographs[ucs[0]],)
    return ucs


