#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, sys
from ecma35.data.names import namedata

# GCC invocation (per ECMA-48):
#   CSI SP _ or CSI 0 SP _: combine next two characters.
#   CSI 1 SP _: start of combining text.
#   CSI 2 SP _: end of combining text.
# This applies to combining in one space: it explicitly does not (per ECMA-43) overstamp anything.

__all__ = ("gcc_sequences", "gcc_tuples")

cachefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gcc_sequences.json")

if not os.path.exists(cachefile):
    gcc_sequences = {
        # "Pts" is specifically listed as a GCC example in Annex C of ECMA-43, so we should
        # include it. It doesn't have a standard decomposition, so including it manually.
        # Although rendering of U+20A7 is actually quite varied: it might show up as any symbol 
        # sometimes used for the Peseta (including a single-barred P), depending on font.
        "Pts": "₧",
        # The basmala is included as a single codepoint but, unlike the SAW, doesn't have a
        # decomposition. So, including it manually (at the same level of pointing as with the SAW).
        "بسم الله الرحمن الرحيم": "﷽",
        # MacJapanese mapping uses a character combination of ↓ and ↑ for ⇵ (added to UCS later??).
        # Other adjacently stacked vertical arrow pairs are included for purpose of completeness.
        "↓↑": "⇵", "↑↓": "⇅", "↑↑": "⇈", "↓↓": "⇊",
        "⭣⭡": "⮃", "⭡⭣": "⮁", "⭡⭡": "⮅", "⭣⭣": "⮇",
        "⇃↾": "⥯", "↿⇂": "⥮", "↿↾": "⥣", "⇃⇂": "⥥",
        # MacKorean's shadowed keycapped number 10
        "\uF864[10]": "\U0001F51F",
    }

    # Exclude most Arabic composites, since they're just sequences of letters, and often one sequence 
    #   of normalised letters maps onto multiple presentation forms depending on position, making
    #   unambiguous GCC sequences an issue.
    # Include the Arabic composites from the last line of Arabic Presentation Forms-A, since they do
    #   in fact correspond to the type of composition we're talking about here (U+FDFx).
    # Include the Roman pairs of letters, since they're only included in exceptional cases where two
    #   letters are collated and/or rendered as one (much less usual in Roman print than Arabic) and 
    #   can be given unambiguous GCC sequences.
    # Exclude the Thai/Lao "AM", since it's just a standalone vowel with a nasal point, and not
    #   actually a digraph. Include the Ho No and Ho Mo digraphs though.
    # Trivia: the Thai and Lao vowel points are the only Unicode combining marks which logically 
    #   associate with the following, not preceding, base character, due to visually being placed to 
    #   its left, an approach not taken for other Brahmi scripts. (This would presumably be why the 
    #   AM doesn't break apart on a mere NFD?)
    for i in (list(range(0x600)) + list(range(0x700, 0xE00)) + list(range(0xEDC, 0xFB4F)) + 
               list(range(0xFDF0, 0xFE00)) + list(range(0xFF00, 0x10FFFF))):
        i = chr(i)
        if i in namedata.canonical_decomp:
            continue
        k = namedata.compat_decomp.get(i, (None, i))[1]
        if (len(k) > len(i)) and (namedata.get_ucscategory(k[1])[0] != "M"):
            gcc_sequences[k] = i

    gcc_sequences["pH"] = gcc_sequences["PH"] # Well, they messed that decomposition up, didn't they.

    # Generally speaking, GCC sequences are expected to be of ISO 8859 characters where applicable.
    # Doesn't mean that their Unicode decompositions can't also be supported.
    # I don't think any uses multiple at the moment, but one loop each covers for that.
    for i in gcc_sequences.copy():
        if "\u2044" in i:
            gcc_sequences[i.replace("\u2044", "/")] = gcc_sequences[i]
    for i in gcc_sequences.copy():
        if "\u2215" in i:
            gcc_sequences[i.replace("\u2215", "/")] = gcc_sequences[i]
    for i in gcc_sequences.copy():
        if "\u02BC" in i:
            gcc_sequences[i.replace("\u02BC", "'")] = gcc_sequences[i]
    for i in gcc_sequences.copy():
        if "ℓ" in i:
            gcc_sequences[i.replace("ℓ", "l")] = gcc_sequences[i]

    # Micro-thing unit symbol blocks just as much sense in contexts with the ISO-8859-1 repertoire 
    # (including U+00B5) as in those with the ISO-8859-7 repertoire (including U+03BC). It's the 
    # U+03BC that's used in the decompositions, for reference.
    for i in gcc_sequences.copy():
        if "\u03BC" in i:
            gcc_sequences[i.replace("\u03BC", "\xB5")] = gcc_sequences[i]
    f = open(cachefile, "w")
    f.write(json.dumps(gcc_sequences))
    f.close()
else:
    f = open(cachefile, "r")
    gcc_sequences = json.load(f)
    f.close()

gcc_tuples = {}
for i, j in gcc_sequences.items():
    gcc_tuples[tuple(ord(k) for k in i)] = tuple(ord(k) for k in j)




