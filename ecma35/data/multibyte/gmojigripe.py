#!/usr/bin/env python3
# -*- mode: python; charset: utf-8 -*-
# Written by HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Row format: <SPUA codepoint>\t<SPUA UTF-16 escape>\t<SPUA UTF-8 escape>\t<name><kddi><docomo><softbank>\t\t\t
# Kddi:     {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS (beyond JIS) hex>\t<PUA? hex>\t<JIS hex>\t<Shift_JIS (from JIS) hex>}
# Docomo:   {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS hex>\t<PUA? hex>\t<JIS hex>}
# Softbank: {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS hex>\t<PUA? hex>\t<JIS hex>}

import os, collections, re
import unicodedata as ucd
from ecma35.data.multibyte import mbmapparsers as parsers

GoogleAllocation = collections.namedtuple("GoogleAllocation", ["codepoint", "utf8", "utf16", "googlename"])
KddiAllocation = collections.namedtuple("KddiAllocation", ["name", "substitute", "id", "sjis", "pua", "jis", "jis_sjis", "unic", "uniname"])
NonKddiAllocation = collections.namedtuple("NonKddiAllocation", ["name", "substitute", "id", "sjis", "pua", "jis", "unic", "uniname"])

sauces = {"docomo": {}, "kddi": {}, "softbank": {}}
forced = {
    "FEE1C": "\U0001F3A5\uF87F", # Lacks own Unicode mapping, bestfitted to 1F3A5 for the other two
    "FEE33": "\u2611\uF87F", # Similarly, ish.
    "FE82B": "\u27BF", # Not in the UCD data, but de-facto supported at 27BF, and 27BF used by ICU.
}
outmap = {}

def pull(line, row, name, *, iskddi = False):
    mystruct = NonKddiAllocation if not iskddi else KddiAllocation
    if not line[0]:
        # i.e. a mapping given
        unic = "".join(sauces[name].get(i, "\uFFFD") for i in line[2].split("+"))
        uniname = "+".join(ucd.name(i) for i in unic)
        if unic == "\uFFFD":
            unic = uniname = ""
        group = line[:5] if not iskddi else line[:6]
        row.append(mystruct(*([name] + group + [unic, uniname])))
        del line[:5]
        if iskddi:
            line.pop(0)
    else:
        # i.e. just a substitute given
        padding = ([""] * 6) if not iskddi else ([""] * 7)
        row.append(mystruct(*([name] + [line[0] if line[0] != "〓" else ""] + padding)))
        line.pop(0)

def andothers_iter(seq):
    for i in range(len(seq)):
        yield seq[i], (seq[:i] + seq[(i+1):])

def getseq(substitute):
    seq = re.compile("([\uf860-\uf86f])").split(substitute)
    if len(seq) == 1:
        seq = ["", ""] + seq
    assert seq[0] == ""
    for (shint, vals) in zip(seq[1::2], seq[2::2]):
        tail = ""
        if len(vals) > 1 and (0xf870 <= ord(vals[-1]) < 0xf880):
            tail = vals[-1]
            vals = vals[:-1]
        yield (shint, vals, tail)

def writehints(substitute, charname = ""):
    if len(substitute) == 1:
        substitute += "\uf87f"
    elif substitute[0] == "[" and substitute[2:] == "]":
        # Single letter emoji → keycaps (as reginds might merge to flags)
        combiner = "\u20e3" if "SQUARE" not in charname else "\u20de"
        substitute = substitute[1] + combiner
    elif substitute[0] == "(" and substitute[2:] == ")":
        # Encircled
        substitute = substitute[1] + "\u20dd"
    else:
        # Sadly only go up to length 4, so may need multiple.
        substin, substout = substitute, ""
        while len(substin) >= 8:
            substout += "\uf862" + substin[:4]
            substin = substin[4:]
        if len(substin) == 2:
            substout += "\uf860" + substin
        elif len(substin) == 3:
            substout += "\uf861" + substin
        elif len(substin) == 4:
            substout += "\uf862" + substin
        elif len(substin) == 5:
            substout += "\uf861" + substin[:3] + "\uf860" + substin[3:]
        elif len(substin) == 6:
            substout += "\uf861" + substin[:3] + "\uf861" + substin[3:]
        elif len(substin) == 7:
            substout += "\uf862" + substin[:4] + "\uf861" + substin[3:]
        substitute = substout
    if "INVERSE" in charname:
        substout = ""
        for (hint, vals, tail) in getseq(substitute):
            if hint == "\uf862":
                hint = "\uf865" # f863 arguably closer to intent but ambiguous
            else:
                tail = "\uf87a"
            substout += hint + vals + tail
        substitute = substout
    return substitute

with open(os.path.join(parsers.directory, "UCD/EmojiSources.txt")) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        unic, docomo, kddi, softbank = line.rstrip().split(";")
        unic = "".join(chr(int(_i, 16)) for _i in unic.split())
        if len(unic) == 2 and unic[1] == "\u20E3":
            unic = unic[0] + "\uFE0F\u20E3"
        sauces["docomo"][docomo] = unic
        sauces["kddi"][kddi] = unic
        sauces["softbank"][softbank] = unic

with open(os.path.join(parsers.directory, "AOSP/gmojiraw.txt")) as f:
    sets = []
    for no, line in enumerate(f):
        row = []
        line = line.rstrip("\n").split("\t")
        row.append(GoogleAllocation(*line[:4]))
        line = line[4:]
        pull(line, row, "kddi", iskddi = True)
        pull(line, row, "docomo")
        pull(line, row, "softbank")
        assert [i.strip() for i in line] == ["", "", ""]
        sets.append(row)

for row in sets:
    google_spua = row[0].codepoint
    # Each row is one GMoji SPUA. "others" is the other two vendors, for whose mappings Google's
    #   substitutes for the emoji of the vendor under scrutiny might be listed.
    for group, others in andothers_iter(row[1:]):
        suboutmap = outmap.setdefault(group.name, [])
        unic = "\uFFFD"
        if group.unic:
            unic = group.unic
        elif google_spua in forced and group.sjis:
            unic = forced[google_spua]
        elif group.sjis:
            for other in others:
                if other.substitute:
                    unic = writehints(other.substitute, row[0].googlename)
                    break
            else: # for...else, i.e. never reached "break"
                if group.pua:
                    unic = chr(int(group.pua, 16))
        for typ in ["sjis", "jis"]:
            byts = getattr(group, typ)
            if byts and ("+" not in byts) and (typ != "jis" or byts != "222E"):
                assert len(byts) == 4
                byts = bytes([int(byts[:2], 16), int(byts[2:], 16)])
                if typ == "sjis":
                    men, ku, ten = parsers._grok_sjis(byts)
                else:
                    men = 1
                    ku = byts[0] - 0x20
                    ten = byts[1] - 0x20
                pointer = ((men - 1) * (94 * 94)) + ((ku - 1) * 94) + (ten - 1)
                if pointer < len(suboutmap):
                    assert suboutmap[pointer] in (None, tuple(ord(i) for i in unic))
                    suboutmap[pointer] = tuple(ord(i) for i in unic)
                else:
                    if pointer > len(suboutmap):
                        suboutmap.extend([None] * (pointer - len(suboutmap)))
                    suboutmap.append(tuple(ord(i) for i in unic))
        # Try to end it on a natural plane boundary.
        suboutmap.extend([None] * (((94 * 94) - (len(suboutmap) % (94 * 94))) % (94 * 94)))

outmap["docomo"] = tuple(outmap["docomo"])
outmap["kddi"] = tuple(outmap["kddi"])
outmap["softbank"] = tuple(outmap["softbank"])

        
