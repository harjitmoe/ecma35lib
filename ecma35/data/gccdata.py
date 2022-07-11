#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2022.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, sys, binascii
from ecma35.data.names import namedata

# GCC invocation (per ECMA-48):
#   CSI SP _ or CSI 0 SP _: combine next two characters.
#   CSI 1 SP _: start of combining text.
#   CSI 2 SP _: end of combining text.
# This applies to combining in one space: it explicitly does not (per ECMA-43) overstamp anything.

__all__ = ("gcc_sequences", "gcc_tuples", "bs_handle")

cachefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gcc_sequences.json")
bscachefile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bs_sequences.json")
confusablesfn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "names", "namemaps", "UCD", "confusables.txt")

conformation_sets = {frozenset(i) for i in (
    # Generally speaking, GCC sequences are expected to be of ISO 8859 characters where applicable.
    # Doesn't mean that their Unicode decompositions can't also be supported.
    {"\u2044", "/", "\u2215", "/"}, {"\u02BC", "'"}, {"ℓ", "l"},
    #
    # Variation in Unicode mappings for APL characters
    {"⎕", "▯", "□"}, {"⋄", "◊"}, {"∣", "|", "│"},
    {"∩", "⋂"}, {"∪", "⋃"}, {"∼", "~"},
    {"∧", "⋀"}, {"∨", "⋁"}, {"!", "ǃ"},
    {"\\", "\u2216"}, {"⋆", "*"}, {"-", "−"},
    {"⍺", "α"}, {"∊", "ε", "∈"}, {"⍳", "ι"}, {"⍴", "ρ"}, {"⍵", "ω"},
    {":", "∶"},
    #
    # Misc
    {"⊲", "◅"}, {"⊳", "▻"}, {"∘", "◦"}, {"¯", "‾"}, {"∙", "⋅", "·", "･", "・"}, {"∫", "ʃ"},
    {"‖", "∥"}, # Some CJK sets distinguish (making ∥ like ⫽), others unify so mappings differ
    {"∇", "🜄"},
)}

if not os.path.exists(cachefile) or not os.path.exists(bscachefile):
    uts39data = {}
    with open(confusablesfn, "r", encoding="utf-8-sig") as f:
        for line in f:
            if (not line.strip()) or line[0] == "#":
                continue
            frm, to, detail = tuple(i.strip() for i in line.split(";", 2))
            ma, human, via = tuple(i.strip() for i in detail.split("#"))
            frombit = "".join(chr(int(i, 16)) for i in frm.split())
            if via:
                assert via[0] == "→"
                tobit = via[1:].split("→", 1)[0].replace("\u200E", "")
            else:
                tobit = "".join(chr(int(i, 16)) for i in to.split())
            if 0xFB4F < ord(frombit[0]) < 0xFDF0:
                continue
            elif 0xFEF0 <= ord(frombit[0]) <= 0xFEFF:
                continue
            elif tobit == "\u0d28\u0d41":
                continue
            elif len(frombit) == 1 and len(tobit) > 1:
                be_overridden_list = ("ꓺ", "⳹", "ꜻ", "Ꜻ", "Ƃ", "ꮜ", "Ɏ", "Ᏺ", "ǳ", "ѳ", "Ɵ", "ꚙ", "Ꚙ", "ѣ", r"ݲ", r"Ӊ", "ӊ")
                if frombit in be_overridden_list:
                    continue
                elif (tobit not in uts39data) or (uts39data[tobit] in be_overridden_list):
                    uts39data[tobit] = frombit
                else:
                    print(tobit, ascii(tobit), uts39data[tobit], ascii(uts39data[tobit]), frombit, ascii(frombit))

if not os.path.exists(cachefile):
    gcc_sequences = {
        # "Pts" is specifically listed as a GCC example in Annex C of ECMA-43, so we should
        # include it. It doesn't have a standard decomposition, so including it manually.
        # Although rendering of U+20A7 is actually quite varied: it might show up as any symbol 
        # sometimes used for the Peseta (including a single-barred P), depending on font.
        "Pts": "₧",
        # The basmala is included as a single codepoint but, unlike the SAW, doesn't have a
        # decomposition. So, including it manually (at the same level of pointing as with the SAW).
        r"بسم الله الرحمن الرحيم": r"﷽",
        # MacJapanese mapping uses a character combination of ↓ and ↑ for ⇵ (added to UCS later??).
        # Other adjacently stacked vertical arrow pairs are included for purpose of completeness.
        '↓↑': '⇵', '↑↓': '⇅', '↑↑': '⇈', '↓↓': '⇊', '⭣⭡': '⮃', '⭡⭣': '⮁', '⭡⭡': '⮅', '⭣⭣': '⮇',
        # MacKorean's shadowed keycapped number 10
        "\uF864[10]": "\U0001F51F",
        # Mathematical symbols that have no Unicode decompositions (unlike e.g. ⩴, ⩵, ⩶) and no
        #   UTS39-gleaned compositions either
        '||': '‖', '|||': '⦀', '::': '∷', '-:': '∹', ':=': '≔', '=:': '≕', ':-:': '∺', '|⊢': '⊩',
        '||⊢': '⊪', '⊣|': '⫣', '∙∙∙': '⋯', '∩∩': '⩋', '∪∪': '⩊', '⊣⊢': '⟛', '⫤⊨': '⟚',
        '++': '⧺', '+++': '⧻',
        # Alchemical symbols without decompositions or UTS39-gleaned compositions
        'SSS': '🝜', '🜄F': '🜅', '🜄R': '🜆'
    }
    for i in uts39data:
        if i not in gcc_sequences and namedata.get_ucscategory(i[-1]) != "Mn":
            gcc_sequences[i] = uts39data[i]
    from_1F18B = ["IC", "PA", "SA", "AB", "WC", "DJ",
                  "CL", "COOL", "FREE", "ID", "NEW", "NG", "OK", "SOS", "UP!", "VS", "3D", 
                  "2ndScr", "2K", "4K", "8K", "5.1", "7.1", "22.2", "60P", "120P", "d", 
                  "HC", "HDR", "Hi-Res", "Lossless", "SHV", "UHD", "VOD"]
    for n, i in enumerate(from_1F18B):
        if len(i) > 1:
            gcc_sequences[i] = chr(0x1F18B + n)

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

    for cset in conformation_sets:
        for i in tuple(gcc_sequences.keys()):
            for c1 in cset:
                for c2 in cset - {c1}:
                    if c1 in i:
                        gcc_sequences.setdefault(i.replace(c1, c2), gcc_sequences[i])

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

_rbs_maps = {
     '̀': ('`', 'ˋ'),
     '́': ("'", '´', 'ˊ', '\u0384', '\u1ffd'),
     '̂': ('^', 'ˆ'),
     '̃': ('~', '˜', '῀'),
     '̴': ('~', '∼', '⁓', '～', '〜'),
     '̄': ('¯', '‾'),
     '̆': ('˘',),
     '̇': ('˙',),
     '̈': ('"', '¨'),
     '̈́': ('\u0385', '\u1fee'),
     '̊': ('°', '˚', '*'),
     '⃰': ("*",),
     '̋': ('˝',),
     '̌': ('ˇ',),
     '̓': ('᾽', '᾿'),
     '̣': ('.',),
     '̦': (',',),
     '̧': (',', '¸'),
     '̨': (',', '˛'),
     '̡': (',', ),
     '̱': ('_', 'ˍ'),
     '̵': ('-',),
     '̸': ('/',),
     '⃥': ('\\',),
     '⃦': ('‖', '∥'),
     '⃒': ("|",),
     '⃙': ("⥁",),
     '⃚': ("⥀ ",),
     '⃝': ("○", "◯"),
     '⃘': ("∘", "◦"),
     '⃞': ("□", "⎕"),
     '⃟': ("◇",),
     '⃠': ("🛇", "🚫"),
     '⃢': ("🖵",),
     '⃤': ("△",),
     '⃧': ("⌉", "⌝", "˺"),
     '⃫': ("⫽",),
     '⃪': ("←",),
}
rbs_maps = _rbs_maps.copy()

def breakup(i):
    if i in namedata.canonical_decomp:
        return namedata.canonical_decomp[i]
    elif i in namedata.compat_decomp:
        candidate = namedata.compat_decomp[i]
        if candidate[0] == "compat":
            if len(candidate[1]) > 1:
                if namedata.get_ucscategory(candidate[1][1]) == "Mn":
                    return candidate[1]
    return None

def recursive_breakup(i):
    stack = []
    while (b := breakup(i)) != None:
        stack.extend(b[1:][::-1])
        i = b[0]
    return "".join([i, *stack[::-1]])

for i in range(0x10FFFF):
    i = chr(i)
    rb = recursive_breakup(i)
    if rb[0] == " " and i != " ":
        rbs_maps.setdefault("".join(rb[1:]), (i,))
        assert i in rbs_maps["".join(rb[1:])], (i, rb)

bs_maps = {}
for compchar, spacchars in rbs_maps.items():
    for spacchar in spacchars:
        bs_maps[spacchar] = compchar
bs_maps[","] = " ̦"[1]
bs_maps["*"] = " ⃰"[1]
bs_maps["~"] = " ̃"[1]

if not os.path.exists(bscachefile):
    bs_deflators = {
        #
        # Mostly in aid of using as part of a larger composition
        ("˙", "."): ":", ("-", "_"): "=", 
        #
        # Cases which aren't decompositions nor APL-ISO-IR-68.TXT compositions, which therefore
        #   need giving manually.
        ('l', '-'): 'ƚ', ('l', '/'): 'ł', ('L', '-'): 'Ł', ('L', '/'): 'Ł', ('D', '-'): 'Ð',
        ('o', '/'): 'ø', ('=', '-'): '≡', ('=', '_'): '≡', (':', '-'): '÷', ('>', '-'): '⪫',
        ('<', '-'): '⪪', ('0', '/'): '∅︀', ('√', '³'): '∛', ('√', '⁴'): '∜', ('∫', '∘'): '∮',
        ('~', '_'): '≃', ('˜', '_'): '≃', ('˜', '-'): '≃', ('~', '-'): '≃', ('≃', '_'): '≅',
        ('≃', '-'): '≅', ('~', '='): '≅', ('˜', '='): '≅', ('˜', '~'): '≈', ('~', '~'): '≈',
        ('≈', '_'): '≊', ('≃', '~'): '≊', ('≃', '˜'): '≊',
        ("˜", "≠"): "≆", # Try to avoid clobbering ≇, which has a decomposition.
        ('≈', '~'): '≋', ('≈', '˜'): '≋', ('~', ':'): '∻', ('"', '.'): '∵', ('=', ':'): '≑',
        ('÷', '-'): '≑', ('∘', '='): '≖', ('*', '='): '≛', ('≡', '_'): '≣', ('<', '_'): '≤',
        ('>', '_'): '≥', ('(', ')'): '≬', ('⊏', '_'): '⊑', ('⊐', '_'): '⊒', ('○', '='): '⊜',
        ('○', '+'): '⊕', ('⎕', '+'): '⊞', ('□', '+'): '⊞', ('⎕', '-'): '⊟', ('□', '-'): '⊟',
        ('⎕', '×'): '⊠', ('□', '×'): '⊠', ('⊲', '_'): '⊴', ('⊳', '_'): '⊵', ('∧', '‾'): '⊼',
        ('∨', '‾'): '⊽', ('∙', '○'): '⊙', ('∨', '|'): '⩛', ('∧', '|'): '⩚', ('∙', '⎕'): '⊡',
        ('∙', '□'): '⊡', ('‖', '='): '⋕', ('∙', '<'): '⋖', ('∙', '>'): '⋗', ('<', '‾'): '⋜',
        ('>', '‾'): '⋝', (':', '.'): '⁝', (':', '˙'): '⁝', (':', '∙'): '⁝', ('∈', '˙'): '⋵',
        ('∈', '‾'): '⋶', ('∊', '‾'): '⋷', ('∋', '‾'): '⋽', ('∍', '‾'): '⋾', ('∧', '∧'): '⩕',
        ('∨', '∨'): '⩖', ('∑', '∘'): '⨊', ('∫', '∑'): '⨋', ('∫', '-'): '⨍', ('∫', '='): '⨎',
        ('∫', '/'): '⨏', ('∫', '×'): '⨘', ('∫', '∩'): '⨙', ('∫', '∪'): '⨚', ('∫', '‾'): '⨛',
        ('∫', '_'): '⨜', ('⮌', '∫'): '⨗', ('↷', '∫'): '∱', ('↺', '∫'): '⨑', ('∫', '⥁'): '∲',
        ('∫', '⥀'): '∳', ('-', '.'): '⨪', ('_', '×'): '⨱', ('×', '×'): '⨳', ('○', '×'): '⊗',
        ('⊗', '^'): '⨶', ('⊗', 'ˆ'): '⨶', ('○', '⊗'): '⨷', ('○', '÷'): '⨸', ('△', '+'): '⨹',
        ('△', '-'): '⨺', ('△', '×'): '⨻', ('∩', '∙'): '⩀', ('∧', '∙'): '⟑', ('∪', '-'): '⩁',
        ('∪', '+'): '⊎', ('∪', '‾'): '⩂', ('∩', '‾'): '⩃', ('∪', '∨'): '⩅', ('∩', '∧'): '⩄',
        ('⩌', '⨳'): '⩐', ('∧', '˙'): '⩑', ('∨', '˙'): '⩒', ('∨', '∧'): '⩙', ('∨', '_'): '⊻',
        ('∧', '_'): '⩟', ('∨', '-'): '⩝', ('∧', '-'): '⩜', ('=', '.'): '⩦', ('≡', '˙'): '⩧',
        ('≐', '-'): '⩧', ('≐', '_'): '⩧', ('≡', '‖'): '⩨', ('~', '˙'): '⩪', ('^', '≈'): '⩯',
        ('ˆ', '≈'): '⩯', ('≅', '˙'): '⩭', ('<', '∘'): '⩹', ('>', '∘'): '⩺', ('˜', '<'): '⪝',
        ('˜', '>'): '⪞', ('⫗', '-'): '⫘', ('⊂', '∙'): '⪽', ('⊃', '∙'): '⪾', ('⊆', '˙'): '⫃',
        ('⊇', '˙'): '⫄', ('|', '\\'): '⫮', ('‖', '-'): '⫲', ('‖', '~'): '⫳', ('|', '-'): '⟊',
        ('⊂', '∘'): '⟃', ('⊃', '∘'): '⟄', ('∨', '∙'): '⟇', ('⌋', '∙'): '⟓', ('⌈', '∙'): '⟔',
        ('(', '<'): '⦓', (')', '>'): '⦔', ('=', '|'): '⧧', ('[', '_'): '⦋', (']', '_'): '⦌',
        ('⦅', '>'): '⦕', ('⦆', '<'): '⦖', ('⁝', '.'): '⦙', ('⁝', '˙'): '⦙', ('≡', '|'): '⯒',
        ('␥', '🖵'): '⎚', ('|', '∙'): '⍿',
    }
    for i in uts39data:
        if len(i) == 2 and i[1] in _rbs_maps:
            for j in _rbs_maps[i[1]]:
                k = (i[0], j)
                if k[::-1] in bs_deflators:
                    k = k[::-1]
                if k not in bs_deflators: # not elif
                    bs_deflators[k] = uts39data[i]
    #
    for i in tuple(bs_deflators.keys()):
        bs_deflators.setdefault(i[::-1], bs_deflators[i])
    #
    for i in range(0x10FFFF):
        i = chr(i)
        bb = breakup(i)
        if not bb:
            continue
        rb = recursive_breakup(i)
        for k in {rb, bb}:
            if len(k) >= 2 and k[1:] in rbs_maps:
                base = k[0]
                combines = rbs_maps[k[1:]]
                for combine in combines:
                    if base == " " and i == combine:
                        continue
                    bs_deflators[(base, combine)] = bs_deflators[(combine, base)] = i
    
    # Clearly wrong:
    # (('-', '⊂'), '⌾'),
    # (('⊂', '-'), '⌾'),
    # APL-ISO-IR-68.TXT lists U+233E as 0x5A085F and 0x5F085A which is wrong.
    # It should be 0x4A084F and 0x4F084A.
    # It also maps 0x2A084C/0x4C082A to both U+2338 and U+236F; the former should be 0x25084C/0x4C0825
    # It maps U+2357 and U+2358 both to 0x46084B/0x4B0846; the former should be 0x4C0855/0x55084C
    
    _multis = []
    _singles = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "singlebyte", "sbmaps", "UTC", "APL-ISO-IR-68.TXT")) as f:
        for line in f:
            if not line.strip() or line[0] == "#":
                continue
            byts, ucs, junk = line.split(None, 2)
            byts = binascii.unhexlify(byts[2:])
            ucs = chr(int(ucs[2:], 16))
            # Corrections for APL-ISO-IR-68.TXT, see above
            if ucs == "\u233E":
                byts = byts.replace(b"\x5A", b"\x4A").replace(b"\x5F", b"\x4F")
            elif ucs == "\u2338":
                byts = byts.replace(b"\x2A", b"\x25")
            elif ucs == "\u2357":
                byts = byts.replace(b"\x46", b"\x4C").replace(b"\x4B", b"\x55")
            if len(byts) == 1:
                _singles[byts[0]] = ucs
            else:
                _multis.append((ucs, tuple(byts)))
    for (target, rawcomp) in _multis:
        comp = tuple(_singles[i] for i in rawcomp if i != 8)
        assert comp not in bs_deflators or bs_deflators[comp] == target, comp
        bs_deflators[comp] = target

    for cset in conformation_sets:
        for i in tuple(bs_deflators.keys()):
            for c1 in cset:
                if i[0] == c1:
                    for c2 in cset - {c1}:
                        bs_deflators.setdefault((c2, i[1]), bs_deflators[i])
                if i[1] == c1: # not elif
                    for c2 in cset - {c1}:
                        bs_deflators.setdefault((i[0], c2), bs_deflators[i])
    
    # Address e.g. =\b/\b-, which won't happen with just =\b- and ≡\b/ but needs a ≠\b- and/or =\b⌿
    _rbsdf = {val: tuple(i for i, j in bs_deflators.items() if j == val) for val in bs_deflators.values()}
    for pair in tuple(bs_deflators.keys()): # tuple to take a copy
        altpairs = []
        if pair[0] in _rbsdf and pair[1] != " ":
            for result in _rbsdf[pair[0]]:
                if " " not in result and (result[1], pair[1]) in bs_deflators:
                    rebracket = bs_deflators[(result[1], pair[1])]
                    altpairs.append((result[0], rebracket))
        if pair[1] in _rbsdf and pair[0] != " ":
            for result in _rbsdf[pair[1]]:
                if " " not in result and (pair[0], result[0]) in bs_deflators:
                    rebracket = bs_deflators[(pair[0], result[0])]
                    altpairs.append((rebracket, result[1]))
        for altpair in altpairs:
            # Note: altpair may already be legitimately used for a different character, e.g. Ṻ, Ǖ
            # Some cases applying diacritics in a different order are correct (e.g. ά\b᾿→ἄ, or ĕ\b,→ḝ),
            #   while some are arguably incorrect (e.g. Ō\b~→Ȭ, which should rather stay as a Ō with a
            #   combining tilde)—this is low priority since it's not like overprinting *hardware* would
            #   have differentiated the two by order of typing anyway.
            if altpair not in bs_deflators:
                bs_deflators[altpair] = bs_deflators[pair]
    
    f = open(bscachefile, "w")
    f.write(json.dumps(list(bs_deflators.items())))
    f.close()
else:
    f = open(bscachefile, "r")
    bs_deflators = dict((tuple(i), j) for i, j in json.load(f))
    f.close()

def test():
    import pyuca, pprint
    collator = pyuca.Collator()
    pprint.pprint(sorted(bs_deflators.items(), key=lambda pair: [collator.sort_key(pair[1]), *pair]))

def bs_handle_left_preference(charses):
    scratch = tuple(charses)
    while len(scratch) > 1:
        if scratch[:2] in bs_deflators:
            scratch = (bs_deflators[scratch[:2]],) + scratch[2:]
        elif scratch[-2:] in bs_deflators:
            scratch = (bs_deflators[scratch[-2:]],) + scratch[:-2]
        else:
            bases = [i for i in scratch if i not in bs_maps] or " "
            combos = [bs_maps[i] for i in scratch if i in bs_maps]
            return "\b".join(bases) + "".join(combos)
    return scratch[0]

def bs_handle_right_preference(charses):
    scratch = tuple(charses)
    while len(scratch) > 1:
        if scratch[-2:] in bs_deflators:
            scratch = (bs_deflators[scratch[-2:]],) + scratch[:-2]
        elif scratch[:2] in bs_deflators:
            scratch = (bs_deflators[scratch[:2]],) + scratch[2:]
        else:
            bases = [i for i in scratch if i not in bs_maps] or " "
            combos = [bs_maps[i] for i in scratch if i in bs_maps]
            return "\b".join(bases) + "".join(combos)
    return scratch[0]

def bs_handle(charses):
    return next(iter(sorted([
        bs_handle_left_preference(charses),
        bs_handle_right_preference(charses)], key=len)))


