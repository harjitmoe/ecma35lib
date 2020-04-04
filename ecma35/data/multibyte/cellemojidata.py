#!/usr/bin/env python3
# -*- mode: python; charset: utf-8 -*-
# Written by HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# softbank (2, 84, 86) J-PHONE SHOP
# softbank (2, 84, 87) SKY WEB
# softbank (2, 84, 88) SKY WALKER
# softbank (2, 84, 89) SKY MELODY
# softbank (2, 84, 90) J-PHONE 1
# softbank (2, 84, 91) J-PHONE 2
# softbank (2, 84, 92) J-PHONE 3
# softbank (2, 92, 58) J-SKY1
# softbank (2, 92, 59) J-SKY2
# 
# softbank (1, 93, 70) BOUTIQUE 109
# softbank (1, 93, 83) VODAFONE1
# softbank (1, 93, 84) VODAFONE2
# 
# softbank (2, 92, 12) BOUTIQUE 109
# softbank (2, 92, 60) VODAFONE1
# softbank (2, 92, 61) VODAFONE2

# Row format: <SPUA codepoint>\t<SPUA UTF-16 escape>\t<SPUA UTF-8 escape>\t<name><kddi><docomo><softbank>\t\t\t
# Kddi:     {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS (beyond JIS) hex>\t<PUA hex>\t<JIS hex>\t<Shift_JIS (from JIS) hex>}
# Docomo:   {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS hex>\t<PUA hex>\t<JIS hex>}
# Softbank: {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS hex>\t<PUA hex>\t<JIS hex>}

import os, collections, re, sys
import unicodedata as ucd
from ecma35.data.multibyte import mbmapparsers as parsers

GoogleAllocation = collections.namedtuple("GoogleAllocation", ["codepoint", "utf8", "utf16", "googlename"])
KddiAllocation = collections.namedtuple("KddiAllocation", ["name", "substitute", "id", "sjis", "pua", "jis", "jis_sjis", "unic", "uniname"])
NonKddiAllocation = collections.namedtuple("NonKddiAllocation", ["name", "substitute", "id", "sjis", "pua", "jis", "unic", "uniname"])

sauces = {"docomo": {}, "kddi": {}, "softbank": {}}
forced = {
    "FE82B": "\u27BF", # Not in the UCD data, but de-facto supported at 27BF, and 27BF used by ICU.
    "FEE12": "\xD0\uF87F", # DoCoMo's stylised crossed D logo
    "FEE13": "\xD0\u20E3\uF87F", # DoCoMo point
    "FEE14": "\U0001D736\uF87F", # i-Appli's bold italic alpha logo
    "FEE15": "\U0001D736\u20E3\uF87F", # i-Appli in enclosure
    "FEE1C": "\U0001F3A5\uF87F", # Lacks own Unicode mapping, bestfitted to 1F3A5 for the other two
    "FEE26": "\u25EA", # U+25EA is pretty much an exact match, but not in UCD/ICU deployed mapping.
    "FEE27": "\u2BC0", # Later addition to Unicode from Wingdings 2 190(dec); probably closest one not already taken.
    "FEE28": "\u25BF", # Closer match than the other-vendor substitutes.
    "FEE32": "\U0001F4B3\u200D\U0001F6AB",
    "FEE33": "\u2612\uF87A",
    "FEE44": "C\uFE0F\u200D\u2709\uFE0F",
    "FEE47": "\U0001F3B5\u200D\U0001F5E8\uFE0F",
    "FEE70": "\uf861[Js",
    "FEE71": "\uf861ky]",
    "FEE77": "\U0001F139",
    "FEE78": "\U0001FA90", # Newer emoji similar to this one.
    "FEE7A": "\U0001F3B5\u200D\U0001F50A",
    "FEE7B": "\uf861[J-",
    "FEE7C": "\uf861PHO",
    "FEE7D": "\uf861NE]",
}
outmap = {}
hints2pua = {}
softbank_pages = ([], [], [], [], [], [])

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
        if ord("A") <= ord(substitute[1]) <= ord("Z"):
            if "INVERSE" not in charname:
                return chr(ord(substitute[1]) + 0x1F130 - 0x41)
            else:
                return chr(ord(substitute[1]) + 0x1F170 - 0x41)
        else:
            combiner = "\u20e3" if "SQUARE" not in charname else "\u20de"
            substitute = substitute[1] + combiner
    elif substitute[0] == "(" and substitute[2:] == ")":
        # Encircled
        if ord("A") <= ord(substitute[1]) <= ord("Z"):
            if "INVERSE" not in charname:
                return chr(ord(substitute[1]) + 0x24B6 - 0x41)
            else:
                return chr(ord(substitute[1]) + 0x1F150 - 0x41)
        else:
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
            substout += "\uf862" + substin[:4] + "\uf861" + substin[4:]
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

wants_fe0f = set()
for fn in ("ICU/docomo-sjis.ucm", "ICU/kddi-sjis.ucm", "ICU/softbank-sjis.ucm"):
    with open(os.path.join(parsers.directory, fn)) as f:
        for line in f:
            if ("<UFE0F>" in line) and (line.count("<U") == 2):
                wants_fe0f |= {int(line.split("<U", 1)[1].split(">", 1)[0], 16)}

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

with open(os.path.join(parsers.directory, "AOSP/gmojiraw.txt"), encoding="utf-8") as f:
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

_hashintsre = re.compile("[\uf860-\uf87f]")
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
        #
        if (len(unic) == 1) and (ord(unic) in wants_fe0f):
            unic += "\uFE0F"
        #
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
                if not group.unic:
                    puaunic = chr(int(group.pua, 16))
                    # 0x27BF being the only non-EmojiSources.txt non-PUA mapping deployed in codecs afaict.
                    if (unic != puaunic) and (unic != "\u27BF"):
                        # TODO this merges two vendors where they have the same encoding (e.g. the
                        # "JIS" rather than Shift_JIS codes)
                        key = pointer, tuple(ord(i) for i in unic)
                        if key not in hints2pua:
                            hints2pua[key] = tuple(ord(i) for i in puaunic)
                        else:
                            if not isinstance(hints2pua, list):
                                hints2pua[key] = [hints2pua[key]]
                            hints2pua[key].append(tuple(ord(i) for i in puaunic))
                if group.pua and (group.name == "softbank"):
                    puacode = int(group.pua, 16)
                    pageno = (puacode >> 8) - 0xE0
                    cellno = puacode & 0xFF
                    page = softbank_pages[pageno]
                    if not page:
                        page.extend([None] * 94)
                    page[cellno - 1] = tuple(ord(i) for i in unic)
                #
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

        
