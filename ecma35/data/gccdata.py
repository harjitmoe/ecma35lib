#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd
import os, json

# GCC invocation (per ECMA-48):
#   CSI SP _ or CSI 0 SP _: combine next two characters.
#   CSI 1 SP _: start of combining text.
#   CSI 2 SP _: end of combining text.
# This applies to combining in one space: it explicitly does not (per ECMA-43) overstamp anything.

__all__ = ("gcc_sequences", "gcc_tuples")

cachefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gcc_sequences.json")

if not os.path.exists(cachefile):
    gcc_sequences = {
        # "Pts" is specifically listed as a GCC example in Annex C of ECMA-43.
        # It doesn't have a standard decomposition, so including it manually.
        # Although rendering of U+20A7 is actually quite varied: it might show up as any symbol 
        # sometimes used for the Peseta (including a single-barred P), depending on font.
        "Pts": "₧",
        # The basmala is included as a single codepoint but, unlike the SAW, doesn't have a
        # decomposition. So, including it manually (at the same level of pointing as with the SAW).
        "بسم الله الرحمن الرحيم": "﷽",
        # For now, the Reiwa might not be present in the unicodedata module, so make sure it's there.
        "令和": "㋿",
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
    for ii in (list(range(0x600)) + list(range(0x700, 0xE00)) + list(range(0xEDC, 0xFB4F)) + 
               list(range(0xFDF0, 0xFE00)) + list(range(0xFF00, 0x10FFFF))):
        i = ucd.normalize("NFD", chr(ii))[0]
        k = ucd.normalize("NFKC", ucd.normalize("NFKD", i))
        if (len(k) > len(i)) and (ucd.category(k[1])[0] != "M"):
            # Restore superscripting in the compatibility mappings which is included in the UCD data 
            # but which gets wiped out by the idempotent version (NFKD).
            if k[-1] == "2" and (ucd.category(k[0])[0] != "N"):
                k = k[:-1] + "²"
            elif k[-1] == "3" and (ucd.category(k[0])[0] != "N"):
                k = k[:-1] + "³"
            gcc_sequences[k] = i

    gcc_sequences["pH"] = gcc_sequences["PH"] # Well, they messed that decomposition up, didn't they.

    # The following both have the same NFKD (idempotent compatibility decomposition), so separate them.
    # Incidentally, they don't have the same compatibility decomposition mapping (just that ſ further
    # decomposes to s), but Python doesn't provide a convenient way to use those.
    (gcc_sequences["ſt"], gcc_sequences["st"]) = ("ﬅ", "ﬆ")

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



