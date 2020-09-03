#!/usr/bin/env python3
# -*- mode: python; charset: utf-8 -*-
# Written by HarJIT in 2019, 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, collections, re, sys, binascii
import unicodedata as ucd
from ecma35.data import maxmat
from ecma35.data.multibyte import mbmapparsers as parsers

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

# Older KDDI zodiac signs showing pictures, not symbols
kddizodiacmap = {
    "♈": "🐏",
    "♉": "🐂",
    "♊": "👬", # ...ish (two smiling faces pressed up against each other)
    "♋": "🦀",
    "♌": "🦁",
    "♍": "👧", # ...ish (there isn't really a definitive equivalent)
    "♎": "⚖️",
    "♏": "🦂",
    "♐": "🏹",
    "♑": "🐐",
    "♒": "🏺",
    "♓": "🐟",
}
rkddizodiacmap = dict(zip(kddizodiacmap.values(), kddizodiacmap.keys()))

f = open(os.path.join(parsers.directory, "Perl/Encode-JP-Emoji/lib/Encode/JP/Emoji/Mapping.pm"), "rU", encoding="utf-8")
b = f.read()
f.close()
kddi_microsoft = range(0xE000, 0xE758)

def slurpranges(stuff):
    bits = stuff.split("}\\x{")
    for i in bits:
        if i.startswith("\\x{"):
            i = i[3:]
        elif i[-1] == "}":
            i = i[:-1]
        #
        if "-" in i:
            rang1, rang2 = i.split("}-\\x{", 1)
            rang1 = int(rang1, 16)
            rang2 = int(rang2, 16)
            yield from range(rang1, rang2 + 1)
        else:
            yield int(i, 16)

def remap(dat, rang):
    dat = dat.split("=~", 1)[1].split("[", 1)[1]
    dat, dat2 = dat.split("]", 1)
    dat2 = dat2.split("[", 1)[1].split("]", 1)[0]
    f, t = list(slurpranges(dat)), list(slurpranges(dat2))
    assert len(f) == len(t), (len(f), len(t))
    minidict = dict(zip(f, t))
    for i in rang:
        if (i not in minidict.keys()) and (i not in minidict.values()):
            yield i
        elif (i in minidict.keys()):
            yield minidict[i]
        else:
            yield None

kddi_app = list(remap(b.split("kddi_cp932_to_kddi_unicode {", 1)[1].split("];", 1)[0], kddi_microsoft))
kddi_web = list(remap(b.split("kddiweb_cp932_to_kddiweb_unicode {", 1)[1].split("];", 1)[0], kddi_microsoft))
app2web = dict(zip(kddi_app, kddi_web))

# Row format: <SPUA codepoint>\t<SPUA UTF-16 escape>\t<SPUA UTF-8 escape>\t<name><kddi><docomo><softbank>\t\t\t
# Kddi:     {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS (beyond JIS) hex>\t<PUA hex>\t<JIS hex>\t<Shift_JIS (from JIS) hex>}
# Docomo:   {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS hex>\t<PUA hex>\t<JIS hex>}
# Softbank: {\t<substitute>} || {\t\t<decimal>\t<Shift_JIS hex>\t<PUA hex>\t<JIS hex>}

GoogleAllocation = collections.namedtuple("GoogleAllocation", ["codepoint", "utf8", "utf16", "googlename"])
KddiAllocation = collections.namedtuple("KddiAllocation", ["name", "substitute", "id", "sjis", "pua", "jis", "jis_sjis", "unic", "uniname"])
NonKddiAllocation = collections.namedtuple("NonKddiAllocation", ["name", "substitute", "id", "sjis", "pua", "jis", "unic", "uniname"])

sauces = {"docomo": {}, "kddi": {}, "softbank": {}}
forced = {
    "FE82B": "➿", # Not in the UCD data, despite being added at 27BF, and 27BF used by ICU.
    "FEE12": "Ð\uF87F", # DoCoMo's stylised crossed D logo
    "FEE13": "Ð\u20E3\uF87F", # DoCoMo point
    "FEE14": "𝜶\uF87F", # i-Appli's bold italic alpha logo
    "FEE15": "𝜶\u20E3\uF87F", # i-Appli in enclosure
    "FEE1C": "🎥\uF87F", # Lacks own Unicode mapping, bestfitted to 1F3A5 for the other two
    "FEE26": "◪", # U+25EA is pretty much an exact match, but not in UCD/ICU deployed mapping.
    "FEE27": "⯀", # Later addition to Unicode from Wingdings 2 190(dec); probably closest one not already taken.
    "FEE28": "▿", # Closer match than the other-vendor substitutes.
    "FEE32": "💳\u20E0", # See https://twitter.com/Emojipedia/status/1097962057071095809
    "FEE33": "❎\uFE0E", # Matches text pres, whereas U+274E in emoji pres is U+FEB46. Yes, really.
    "FEE44": "C\uFE0F\u200D✉\uFE0F",
    "FEE47": "🎵\u200D🗨\uFE0F",
    "FEE70": "\uf861[Js",
    "FEE71": "\uf861ky]",
    "FEE77": "🄹",
    "FEE78": "🪐", # Newer emoji similar to this one.
    "FEE7A": "🎵\u200D🔊",
    "FEE7B": "\uf861[J-",
    "FEE7C": "\uf861PHO",
    "FEE7D": "\uf861NE]",
    # Non-JCarrier gmojiraw.txt emoji, some (not all) of which are from the goomoji set:
    "FE35C": "😎", # Google name: COOL FACE
    "FE35D": "🤗", # Google name: HUG FACE
    "FE35E": "🤓", # Google name: GEEK
    "FE35F": "🤔", # Google name: THINKING
    "FE360": "🤣", # Google name: BOUNCING HAPPY
    "FE361": "🙄", # Google name: FACE WITH ROLLING EYES
    "FE362": "😕", # Google name: FACE WITH SLANTED MOUTH
    "FE363": "🤪", # Google name: FACE WITH UNBALANCED EYES
    "FE364": "🙃", # Google name: UPSIDE DOWN FACE
    "FE365": "🤕", # Google name: INJURED FACE
    "FE366": "😬", # Google name: NERVOUS FACE (not much of a grimace; close to the fxemojis glyph)
    "FE367": "😐", # Google name: SYMPATHETIC FACE (shows open eyes, horizontal mouth)
    "FE368": "🙂", # Google name: THIN FACE
    "FE369": "🤖", # Google name: ROBOT
    "FEBA2": "🤘", # Google name: ROCK ON
    "FEEA0": "🄶", # Google name: GOOGLE
}
outmap = {}
hints2pua = {}
hints2pua_sb2g = {}
softbank_pages = ([], [], [], [], [], [])
_all_representations = []
gspua_to_ucs_possibilities = {}

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
        sauces["kddi"][kddi] = kddizodiacmap.get(unic, unic)
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

def _multiucs(hexstring):
    return "".join(chr(int(_i, 16)) for _i in hexstring.split("+"))
def _multinonucs(hexstring):
    return b"".join(binascii.unhexlify(_i) for _i in hexstring.split("+"))

_hashintsre = re.compile("[\uf860-\uf87f]")
for row in sets:
    google_spua = row[0].codepoint
    # Each row is one GMoji SPUA. "others" is the other two vendors, for whose mappings Google's
    #   substitutes for the emoji of the vendor under scrutiny might be listed.
    if not row[1].sjis and not row[2].sjis and not row[3].sjis:
        all_for_this_one = {"UCS.PUA.Google": chr(int(google_spua, 16)),
                            "Name.Google": row[0].googlename,
                            "UCS.Standard": forced[google_spua],
                            "UCS.Key": forced[google_spua]}
        _all_representations.append(all_for_this_one)
        # Not a set yet, for reasons explained below.
        gspua_to_ucs_possibilities.setdefault(all_for_this_one["UCS.PUA.Google"], 
                                              []).append(all_for_this_one["UCS.Key"])
        continue
    for group, others in andothers_iter(row[1:]):
        # Need to do it separately for now, since one Google SPUA can map to multiple standard UCS
        #   characters depending which vendor it goes through, due to the best fit mappings.
        all_for_this_one = {"UCS.PUA.Google": chr(int(google_spua, 16)),
                            "Name.Google": row[0].googlename}
        if group.name == "kddi" and group.sjis:
            all_for_this_one["ID.au"] = tuple(int(_i, 10) for _i in group.id.split("+"))
            all_for_this_one["UCS.PUA.au.app"] = _t = _multiucs(group.pua)
            all_for_this_one["UCS.PUA.au.web"] = "".join(chr(app2web[ord(_i)]) for _i in _t)
            all_for_this_one["Shift_JIS.au.afterjis"] = _multinonucs(group.sjis)
            all_for_this_one["Shift_JIS.au.withinjis"] = _multinonucs(group.jis_sjis)
            all_for_this_one["JIS.au"] = _multinonucs(group.jis)
        elif group.name == "docomo" and group.sjis:
            all_for_this_one["ID.DoCoMo"] = tuple(int(_i, 10) for _i in group.id.split("+"))
            all_for_this_one["UCS.PUA.DoCoMo"] = _multiucs(group.pua)
            all_for_this_one["Shift_JIS.DoCoMo"] = _multinonucs(group.sjis)
            if group.jis != "222E":
                all_for_this_one["JIS.DoCoMo"] = _multinonucs(group.jis)
        elif group.name == "softbank" and group.sjis:
            all_for_this_one["ID.SoftBank"] = tuple(int(_i, 10) for _i in group.id.split("+"))
            all_for_this_one["UCS.PUA.SoftBank"] = _multiucs(group.pua)
            all_for_this_one["Shift_JIS.SoftBank"] = _multinonucs(group.sjis)
            if group.jis != "222E":
                all_for_this_one["JIS.SoftBank"] = _multinonucs(group.jis)
        suboutmap = suboutmap2 = outmap.setdefault(group.name, [])
        if group.name == "kddi":
            suboutmap2 = outmap.setdefault("kddi_symboliczodiac", [])
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
                    if group.name != kddi:
                        unic = chr(int(group.pua, 16))
                    else:
                        unic = chr(app2web[int(group.pua, 16)])
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
                    if group.name != kddi:
                        puaunic = chr(int(group.pua, 16))
                    else:
                        puaunic = chr(app2web[int(group.pua, 16)])
                    # U+27BF being the only non-EmojiSources.txt non-PUA mapping deployed in codecs afaict.
                    # Afaict it was added with the other emoji, so dunno why it was missed out of
                    #   the sources data.
                    if (unic != puaunic) and (unic != "\u27BF"):
                        key = pointer, tuple(ord(i) for i in unic)
                        if key not in hints2pua:
                            hints2pua[key] = tuple(ord(i) for i in puaunic)
                        else:
                            # Two vendors where they have the same encoding (e.g. the
                            # "JIS" rather than Shift_JIS codes)
                            if not isinstance(hints2pua, list):
                                hints2pua[key] = [hints2pua[key]]
                            hints2pua[key].append(tuple(ord(i) for i in puaunic))
                #
                if group.pua and (group.name == "softbank"):
                    puacode = int(group.pua, 16)
                    pageno = (puacode >> 8) - 0xE0
                    cellno = puacode & 0xFF
                    all_for_this_one["SBCS.SoftBank_Page" + 
                                     "GEFOPQ"[pageno]] = bytes([0x20 + cellno])
                    page = softbank_pages[pageno]
                    if not page:
                        page.extend([None] * 94)
                    page[cellno - 1] = tuple(ord(i) for i in unic)
                    if (not group.unic) and (unic != chr(puacode)) and (unic != "\u27BF"):
                        key = cellno, tuple(ord(i) for i in unic)
                        hints2pua_sb2g[key] = (puacode,)
                #
                if pointer < len(suboutmap):
                    assert suboutmap[pointer] in (None, tuple(ord(i) for i in unic))
                    suboutmap[pointer] = tuple(ord(i) for i in unic)
                else:
                    if pointer > len(suboutmap):
                        suboutmap.extend([None] * (pointer - len(suboutmap)))
                    suboutmap.append(tuple(ord(i) for i in unic))
                #
                if not re.compile("([\uf860-\uf87f\u200d])").search(unic):
                    # i.e. contains no hints and no nonstandard ZWJ sequences
                    all_for_this_one["UCS.Standard"] = unic
                elif not re.compile("([\uf860-\uf87f])").search(unic):
                    # Nonstandard ZWJ but no hints
                    all_for_this_one["UCS.Suggested"] = unic
                else:
                    all_for_this_one["UCS.Substitute"] = unic
                all_for_this_one["UCS.Key"] = unic
                #
                if group.name == "kddi":
                    # With zodiacs mapped to symbols (orthodox, but not faithful for pre-2012)
                    unic2 = rkddizodiacmap.get(unic, unic)
                    if (len(unic2) == 1) and (ord(unic2) in wants_fe0f):
                        unic2 += "\uFE0F"
                    if unic2 != unic:
                        all_for_this_one["UCS.Symbolic"] = unic2
                        all_for_this_one["UCS.Pictorial"] = unic
                        # CRAB: Google disunified them, Unicode didn't, KDDI changed their glyph
                        #   accordingly, and then Unicode belatedly disunified them. "[カニ]".
                        if row[0].googlename != "CRAB":
                            del all_for_this_one["UCS.Standard"]
                            all_for_this_one["UCS.Key"] = unic2
                    if pointer < len(suboutmap2):
                        assert suboutmap2[pointer] in (None, tuple(ord(i) for i in unic2))
                        suboutmap2[pointer] = tuple(ord(i) for i in unic2)
                    else:
                        if pointer > len(suboutmap2):
                            suboutmap2.extend([None] * (pointer - len(suboutmap2)))
                        suboutmap2.append(tuple(ord(i) for i in unic2))
                # Not a set yet, for reasons explained below.
                gspua_to_ucs_possibilities.setdefault(all_for_this_one["UCS.PUA.Google"], 
                                                      []).append(all_for_this_one["UCS.Key"])
        if len(all_for_this_one) > 2: # i.e. not just the shared Google bits alone
            _all_representations.append(all_for_this_one)
        # Try to end it on a natural plane boundary.
        suboutmap.extend([None] * (((94 * 94) - (len(suboutmap) % (94 * 94))) % (94 * 94)))
        suboutmap2.extend([None] * (((94 * 94) - (len(suboutmap2) % (94 * 94))) % (94 * 94)))

def get_all_representations():
    from ecma35.data import graphdata
    all_representations = {}
    ucs_possibilities_to_gspua = dict(zip([frozenset(i) for i in gspua_to_ucs_possibilities.values()],
                                 gspua_to_ucs_possibilities.keys()))
    for _i in gspua_to_ucs_possibilities:
        # Due to both the KDDI and DoCoMo Shinkansen emoji mapping to both the Google ones (since the
        #   SoftBank set has two and the other two have one), but them mapping to different Unicode
        #   emoji, both Unicode ones finish up mapped to both Google ones. So to a maximum matching
        #   between the Google and Unicode representations, which way around they go is essentially
        #   arbitrary—not good, since they end up the wrong way around for the Softbank ones' mappings
        #   not to become contradicted between the Google and Unicode mappings.
        # So if any of these "both map to both" instances come up, limit one of them to the most
        #   frequent mapping only (e.g. used by both DoCoMo *and* Softbank).
        _froz = frozenset(gspua_to_ucs_possibilities[_i])
        if len(_froz) == 2 and ucs_possibilities_to_gspua[_froz] != _i:
            s = gspua_to_ucs_possibilities[_i]
            s = sorted(s, key = s.count)
            gspua_to_ucs_possibilities[_i] = [s[-1]]
        gspua_to_ucs_possibilities[_i] = set(gspua_to_ucs_possibilities[_i])
    # Sadly, these ones just have to be specified otherwise it assigns the Google codes the wrong way
    #   around (the non-Google bits work fine).
    # Since there's no reason by the mappings themselves that they shouldn't be the other way
    #   around, and the "wrong way around" is solely in the semantics of the two Google codes:
    gspua_to_ucs_possibilities['\U000FE4F7'] = {"🔮"} # Google name: FORTUNE TELLING
    gspua_to_ucs_possibilities['\U000FE4F8'] = {"🔯"} # Google name: CONSTELLATION
    gspua_to_ucs_possibilities['\U000FE027'] = {"🕙"} # Google name: 10 OCLOCK
    gspua_to_ucs_possibilities['\U000FE02A'] = {"⏰"} # Google name: CLOCK SYMBOL
    gspua_to_ucs = maxmat.maximum_matching(gspua_to_ucs_possibilities)
    _by_kddiid = {}
    _by_nttid = {}
    _by_sbid = {}
    for _i in _all_representations:
        if "UCS.Key" in _i:
            if _i["UCS.PUA.Google"] not in gspua_to_ucs:
                # A handful of separate Google ones which cannot correspond to unique Unicode.
                # Caught, amongst others, by the testing of IDs getting included below.
                pass
            elif _i["UCS.Key"] == gspua_to_ucs[_i["UCS.PUA.Google"]]: # i.e. if isn't merely bestfit
                all_representations.setdefault(_i["UCS.PUA.Google"], {}).update(_i)
                if "ID.au" in _i:
                    _by_kddiid[_i["ID.au"]] = _i
                if "ID.DoCoMo" in _i:
                    _by_nttid[_i["ID.DoCoMo"]] = _i
                if "ID.SoftBank" in _i:
                    _by_sbid[_i["ID.SoftBank"]] = _i
        else:
            # Multiple-character best fit.
            pass # for now
    for _i in _all_representations:
        # To wit:
        #   I-MODE WITH FRAME: no standard Unicode, substitute is the same as frameless one.
        #   EZ NAVI: similarly (substitute is the same as EZ NAVIGATION).
        #   HAPPY FACE 8: a Softbank emoji, which Unicode unifies with HAPPY FACE 7, which is an
        #     au by KDDI emoji (both get mapped to OEM-437 smiley U+263A).
        #   The Softbank character at SJIS 0xF7BA (U+1F532): it gets mapped to several KDDI characters,
        #     none of which get mapped to the same Unicode character as it. Basically, Google unified
        #     🔲 with (say) ◽, but Unicode didn't.
        _is_missing = False
        if "ID.au" in _i and len(_i["ID.au"]) == 1 and _i["ID.au"] not in _by_kddiid:
            _is_missing = True
        elif "ID.DoCoMo" in _i and len(_i["ID.DoCoMo"]) == 1 and _i["ID.DoCoMo"] not in _by_nttid:
            _is_missing = True
        elif "ID.SoftBank" in _i and len(_i["ID.SoftBank"]) == 1 and _i["ID.SoftBank"] not in _by_sbid:
            _is_missing = True
        #
        if _is_missing:
            if _i["UCS.PUA.Google"] not in gspua_to_ucs:
                # i.e. doesn't have a unique Unicode mapping but can be given a unique Google mapping
                all_representations.setdefault(_i["UCS.PUA.Google"], {}).update(_i)
            else:
                # i.e. doesn't have a unique Google mapping but can be given a unique Unicode mapping
                del _i["Name.Google"]
                del _i["UCS.PUA.Google"]
                all_representations.setdefault(_i["UCS.Key"], {}).update(_i)
    for _i in all_representations.values():
        if "UCS.Key" in _i:
            del _i["UCS.Key"] # Has served its purpose now
        if "UCS.Standard" in _i:
            if len(_i["UCS.Standard"].rstrip("\uFE0E\uFE0F")) == 1:
                code = (ord(_i["UCS.Standard"][0]),)
                if code in graphdata.gsets["zdings_g0"][2]:
                    _i["SBCS.ZapfDingbats"] = bytes([0x21 + graphdata.gsets["zdings_g0"][2].index(code)])
                if code in graphdata.rhses["998000"]:
                    _i["SBCS.ZapfDingbats"] = bytes([0x80 + graphdata.rhses["998000"].index(code)])
                if code in graphdata.gsets["webdings_g0"][2]:
                    _i["SBCS.Webdings"] = bytes([0x21 + graphdata.gsets["webdings_g0"][2].index(code)])
                if code in graphdata.rhses["999000"]:
                    _i["SBCS.Webdings"] = bytes([0x80 + graphdata.rhses["999000"].index(code)])
                if code in graphdata.gsets["wingdings1_g0"][2]:
                    _i["SBCS.Wingdings_1"] = bytes([0x21 + 
                        graphdata.gsets["wingdings1_g0"][2].index(code)])
                if code in graphdata.rhses["999001"]:
                    _i["SBCS.Wingdings_1"] = bytes([0x80 + graphdata.rhses["999001"].index(code)])
                if code in graphdata.gsets["wingdings2_g0"][2]:
                    _i["SBCS.Wingdings_2"] = bytes([0x21 + 
                        graphdata.gsets["wingdings2_g0"][2].index(code)])
                if code in graphdata.rhses["999002"]:
                    _i["SBCS.Wingdings_2"] = bytes([0x80 + 
                        graphdata.rhses["999002"].index(code)])
                if code in graphdata.gsets["wingdings3_g0"][2]:
                    _i["SBCS.Wingdings_3"] = bytes([0x21 + 
                        graphdata.gsets["wingdings3_g0"][2].index(code)])
                if code in graphdata.rhses["999003"]:
                    _i["SBCS.Wingdings_3"] = bytes([0x80 + graphdata.rhses["999003"].index(code)])
                #
                if ucd.name(_i["UCS.Standard"][0], ""):
                    _i["Name.Unicode"] = ucd.name(_i["UCS.Standard"][0])
                elif _i["UCS.Standard"] == "\U0001F92A":
                    # U+1F92A is Unicode 10 (2017). Somehow, this means Python 3.6 cannot name it.
                    _i["Name.Unicode"] = "GRINNING FACE WITH ONE LARGE AND ONE SMALL EYE"
                elif _i["UCS.Standard"] == "\U0001FA90":
                    # Similarly
                    _i["Name.Unicode"] = "RINGED PLANET"
                elif ucd.category(_i["UCS.Standard"]) == "Co": # i.e. PUA
                    del _i["UCS.Standard"]
                else:
                    print(_i)
        if "ID.au" in _i and len(_i["ID.au"]) == 1:
            _i["HREF.au"] = "http://www001.upp.so-net.ne.jp/hdml/emoji/e/{:d}.gif".format(
                            _i["ID.au"][0])
        if "ID.DoCoMo" in _i and len(_i["ID.DoCoMo"]) == 1:
            if _i["ID.DoCoMo"][0] < 300:
                _i["HREF.DoCoMo"] = ("https://www.nttdocomo.co.jp/service/developer/make/" + 
                      "content/pictograph/basic/images/{:d}.gif".format(_i["ID.DoCoMo"][0]))
            else:
                _i["HREF.DoCoMo"] = ("https://www.nttdocomo.co.jp/service/developer/make/" + 
                  "content/pictograph/extention/images/{:d}.gif".format(_i["ID.DoCoMo"][0] - 300))
            # Encoding of emoji under Multibyte-Plane 9, Zone B of TRON code. Supposedly.
            pua = ord(_i["UCS.PUA.DoCoMo"])
            offset = pua - 0xE63E
            cell = (offset % 94) + 1
            rowbyte = (offset // 94) + 0x91
            tron = bytes([rowbyte, cell + 0x20])
            _i["TRON_PlaneMB9.DoCoMo"] = tron # i.e. shifted to by 0xFE, 0x29
        if "UCS.PUA.SoftBank" in _i and len(_i["UCS.PUA.SoftBank"]) == 1:
            _i["HREF.SoftBank"] = ("http://creation.mb.SoftBank.jp/mc/tech/tech_pic/img/" + 
                                   "{:04X}_20.gif".format(ord(_i["UCS.PUA.SoftBank"][0])))
        if "UCS.PUA.Google" in _i and len(_i["UCS.PUA.Google"]) == 1:
            # Google was collaborating more with au by KDDI than the others, so the kddi_ne_jp
            #   versions of the URLs might rationally be seen as the "default" of the three.
            # All three schemes fall back to other sets if there isn't a glyph in that one
            _i["HREF.Google"] = "https://mail.google.com/mail/e/kddi_ne_jp/{:03X}".format(
                                    ord(_i["UCS.PUA.Google"][0]) & 0xFFF)
    return all_representations

outmap["docomo"] = tuple(outmap["docomo"])
outmap["kddi"] = tuple(outmap["kddi"])
outmap["kddi_symboliczodiac"] = tuple(outmap["kddi_symboliczodiac"])
outmap["softbank"] = tuple(outmap["softbank"])

