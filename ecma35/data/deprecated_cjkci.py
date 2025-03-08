#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2023, 2024, 2025.

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
    #
    # CNS 11643 references not moved yet but proposed to be:
    #   https://www.unicode.org/irg/docs/n2519-TSourceIssues.pdf#page=35
    #   https://www.unicode.org/L2/L2025/25009-cjk-unihan-wg-utc182.pdf#page=5
    #   https://www.unicode.org/irg/docs/n2778-Disunify.pdf
    0x2F81D: 0x20674,
    0x2F82C: 0x20984,
    0x2F82D: 0x2D161,
    0x2F85B: 0x21533,
    0x2F85D: 0x21587,
    0x2F860: 0x216A7,
    0x2F89C: 0x22505,
    0x2F905: 0x23D40,
    0x2F90E: 0x23F1C,
    0x2F91C: 0x242B3,
    0x2F927: 0x2AEC5,
    0x2F92B: 0x248FD,
    #0x2F935: 0x24C36, # disunified in other direction to U+24C53, thus redundant but valid
    0x2F943: 0x2511A,
    0x2F94B: 0x25271,
    0x2F953: 0x25632, # lacks acknowledgement in code chart cross-references
    0x2F96E: 0x31E7C, # lacks acknowledgement in code chart cross-references
    0x2F97E: 0x2659D,
    0x2F9A4: 0x26D06,
    0x2F9B6: 0x27205,
    0x2F9CB: 0x4695,
    0x2F9D6: 0x25AD4,
    #
    # U+2F980 is another candidate for future disunification and deprecation
    #   (located at U+2B73E in the alpha-stage code chart for Unicode 17.0):
    #     https://www.unicode.org/irg/docs/n2771-Disunify.pdf
    #     https://www.unicode.org/irg/docs/n2702-Recommendations.pdf#page=4
    #     https://www.unicode.org/irg/docs/n2704-MiscEditorialReport.pdf#page=2
    0x2F980: 0x2B73E,
    #
    # Note that U+FA99, U+FAB0 and U+FAD1 are candidates for future disunification and deprecation
    #   when the CJK-K block gets added in however many years' time, although this is disputed and
    #   may well not happen (U+FAD1 in particular seems not to be planned):
    #     https://www.unicode.org/irg/docs/n2510-Disunify3.pdf
    #     https://www.unicode.org/L2/L2021/21178-jiang-two-characters.pdf
    #     https://www.unicode.org/irg/docs/n2785-KPSourceFeedback.pdf
    #     https://hc.jsecs.org/irg/ws2024/app/?find=UTC-00777
    #     https://hc.jsecs.org/irg/ws2024/app/?find=UTC-03249
    # U+FACB and U+2F9FF have also been proposed for future disunification and deprecation (while
    #   U+2F9FE would remain valid):
    #     https://www.unicode.org/irg/docs/n2786-Disunify.pdf
}

def remove_deprecated_cjkci(pointer, ucs):
    if len(ucs) == 1 and ucs[0] in deprecated_compatibility_ideographs:
        return (deprecated_compatibility_ideographs[ucs[0]],)
    return ucs


