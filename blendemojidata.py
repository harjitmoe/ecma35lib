#!/usr/bin/env python3
# -*- mode: python; charset: utf-8 -*-
# Written by HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from ecma35.data import maxmat, graphdata
from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import japan
from ecma35.data.multibyte.cellemojidata import all_jcarrier_raw, gspua_to_ucs_possibs
from ecma35.data.names import namedata

data = os.path.join(parsers.directory, "UCD", "emoji-sequences.txt")
data2 = os.path.join(parsers.directory, "UCD", "emoji-sequences.txt")
strictly_counts_as_emoji = set()
add_fe0f = {}
for dfile in (data, data2):
    with open(dfile) as f:
        for i in f:
            if (not i.strip()) or (i[0] == "#"):
                continue
            i = i.split(";", 1)[0].strip()
            if ".." in i:
                frm, to = i.split("..")
                frm = int(frm, 16)
                to = int(to, 16)
                strictly_counts_as_emoji |= set(chr(j) for j in range(frm, to + 1))
            else:
                # The ones we're testing from WDings / ZDings / ARIB won't have U+FE0F included
                myst = "".join(chr(int(j, 16)) for j in i.split())
                strictly_counts_as_emoji |= {myst.replace("\uFE0F", "")}
                add_fe0f[myst.replace("\uFE0F", "")] = myst

# Some emoji fonts expand to cover anything up to these entire blocks...
counts_as_emoji = strictly_counts_as_emoji.copy()
counts_as_emoji |= set(chr(i) for i in range(0x2600, 0x2700)) # Miscellaneous Symbols
counts_as_emoji |= set(chr(i) for i in range(0x1F000, 0x1F02C)) # Mahjong Tiles
counts_as_emoji |= set(chr(i) for i in range(0x1F300, 0x1F600)) # Misc. Sym. & Pictographs
counts_as_emoji |= set(chr(i) for i in range(0x1F680, 0x1F6D8)) # Transport & Map Sym., range 1
counts_as_emoji |= set(chr(i) for i in range(0x1F6E0, 0x1F6ED)) # Transp. & Map Sym., range 2
counts_as_emoji |= set(chr(i) for i in range(0x1F6F0, 0x1F6FD)) # Transp. & Map Sym., range 3
counts_as_emoji |= set(chr(i) for i in range(0x1F900, 0x1FA00)) # Supplemental Sym. & Pict.
counts_as_emoji ^= {"\U0001F979", "\U0001F9CC"} # (not currently allocated in above range)
counts_as_emoji |= {"✎", "✐", "❥"} # Scattered extras in Dingbats block (entire block not covered)

def _get_ref(all_representations, scode):
    scode2 = scode.rstrip("\uFE0F")
    if scode2 in all_representations:
        return all_representations[scode2]
    elif (scode2 + "\uFE0F") in all_representations:
        return all_representations[scode2 + "\uFE0F"]
    else:
        return all_representations.setdefault(scode, {"UCS.Standard": scode})

special_ucsnames = {
    # U+1F92A is Unicode 10 (2017). Somehow, this means Python 3.6 cannot name it.
    "\U0001F92A": "GRINNING FACE WITH ONE LARGE AND ONE SMALL EYE",
    # Similarly:
    "\U0001FA90": "RINGED PLANET",
    # Named Sequences: https://www.unicode.org/Public/UCD/latest/ucd/NamedSequences.txt
    "#\uFE0F\u20E3": "KEYCAP NUMBER SIGN",
    "*\uFE0F\u20E3": "KEYCAP ASTERISK",
    "0\uFE0F\u20E3": "KEYCAP DIGIT ZERO",
    "1\uFE0F\u20E3": "KEYCAP DIGIT ONE",
    "2\uFE0F\u20E3": "KEYCAP DIGIT TWO",
    "3\uFE0F\u20E3": "KEYCAP DIGIT THREE",
    "4\uFE0F\u20E3": "KEYCAP DIGIT FOUR",
    "5\uFE0F\u20E3": "KEYCAP DIGIT FIVE",
    "6\uFE0F\u20E3": "KEYCAP DIGIT SIX",
    "7\uFE0F\u20E3": "KEYCAP DIGIT SEVEN",
    "8\uFE0F\u20E3": "KEYCAP DIGIT EIGHT",
    "9\uFE0F\u20E3": "KEYCAP DIGIT NINE",
}

def get_all_representations():
    all_representations = {}
    ucs_possibs_to_gspua = dict(zip([frozenset(i) for i in gspua_to_ucs_possibs.values()],
                                 gspua_to_ucs_possibs.keys()))
    for _i in gspua_to_ucs_possibs:
        # Due to both the KDDI and DoCoMo Shinkansen emoji mapping to both the Google ones (since
        #   the SoftBank set has two and the other two have one), but them mapping to different
        #   Unicode emoji, both Unicode ones finish up mapped to both Google ones. So to a maximum
        #   matching between just the Google and Unicode representations, which way around they go
        #   is essentially arbitrary—bad, since they end up the wrong way around for the Softbank
        #   ones' mappings not to become contradicted between the Google and Unicode mappings.
        # So if any of these "both map to both" instances come up, limit one of them to the most
        #   frequent mapping only (e.g. used by both DoCoMo *and* Softbank).
        _froz = frozenset(gspua_to_ucs_possibs[_i])
        if len(_froz) == 2 and ucs_possibs_to_gspua[_froz] != _i:
            s = gspua_to_ucs_possibs[_i]
            s = sorted(s, key = s.count)
            gspua_to_ucs_possibs[_i] = [s[-1]]
        gspua_to_ucs_possibs[_i] = set(gspua_to_ucs_possibs[_i])
    # Sadly, these ones just have to be specified otherwise it assigns the Google codes the wrong 
    #   way around (the non-Google bits work fine).
    # Since there's no reason from the inter-JCarrier mappings themselves that they shouldn't be 
    #   the other way around, and the "wrong" is solely in the semantics of the two Google codes:
    gspua_to_ucs_possibs['\U000FE4F7'] = {"🔮"} # Google name: FORTUNE TELLING, versus
    gspua_to_ucs_possibs['\U000FE4F8'] = {"🔯"} # Google name: CONSTELLATION.
    gspua_to_ucs_possibs['\U000FE027'] = {"🕙"} # Google name: 10 OCLOCK, versus
    gspua_to_ucs_possibs['\U000FE02A'] = {"⏰"} # Google name: CLOCK SYMBOL.
    gspua_to_ucs = maxmat.maximum_matching(gspua_to_ucs_possibs)
    ucs_to_gspua = dict(zip(gspua_to_ucs.values(), gspua_to_ucs.keys()))
    _by_kddiid = {}
    _by_nttid = {}
    _by_sbid = {}
    for _i in all_jcarrier_raw:
        if "UCS.Key" in _i:
            if _i["UCS.PUA.Google"] not in gspua_to_ucs:
                # A handful of separate Google ones which cannot correspond to unique Unicode.
                # Caught, amongst others, by the testing of IDs getting included below.
                pass
            elif _i["UCS.Key"] == gspua_to_ucs[_i["UCS.PUA.Google"]]: # i.e. if isn't mere bestfit
                all_representations.setdefault(_i["UCS.Key"], {}).update(_i)
                if "ID.au" in _i:
                    _by_kddiid[_i["ID.au"]] = _i
                if "ID.DoCoMo" in _i:
                    _by_nttid[_i["ID.DoCoMo"]] = _i
                if "ID.SoftBank" in _i:
                    _by_sbid[_i["ID.SoftBank"]] = _i
        else:
            # Multiple-character best fit.
            pass # for now
    for _i in all_jcarrier_raw:
        # To wit (listed by Google name where possible):
        #   CRAB: already handled specially above. Google disunified them: CANCER gets mapped to
        #     all three vendor zodiacs, while CRAB gets mapped only to the au by KDDI one (which,
        #     before Unicode emoji, used pictorial, not symbolic, zodiacs) and substituted
        #     with "[カニ]" otherwise. Unicode eventually also disunified them, but only after au
        #     had changed their newer model glyphs to show the symbols like the other vendors.
        #   I-MODE WITH FRAME: no standard Unicode, substitute is the same as frameless one.
        #   EZ NAVI: similarly (substitute is the same as EZ NAVIGATION).
        #   HAPPY FACE 8: a Softbank emoji, which Unicode unifies with HAPPY FACE 7, which is an
        #     au by KDDI emoji (both get mapped to the OEM-437 smiley at U+263A).
        #   The Softbank character at SJIS 0xF7BA (U+1F532): it solely gets mapped to several KDDI
        #     characters, none of which get mapped to the same Unicode character as it. Basically, 
        #     Google unified 🔲 with e.g. ⬛️, but Unicode didn't.
        #   Oddly, 🔲 (Softbank) gets mapped from e.g. ⬛️ (au), while 🔳 (Softbank) is mapped from
        #     e.g. ⬜️ (au). The original glyphs seem to have included colours other than black or
        #     white though, so this is arguably a mismatch of arbitrary colour assignments by
        #     Unicode rather than anything more profound. Additionally, 🔲 is assigned to the same 
        #     7-bit code as 🔵 (au), which indeed gets mapped to Softbank as 🔲.
        #   🔳 gets mapped to a Google OCTAGON emoji as well as the au ones, by the way, hence it
        #     has an unambiguous Google PUA mapping even when 🔲 doesn't. And yes, 🔲 and 🔳 were
        #     originally octagonal in shape.
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
                # i.e. doesn't have a unique Unicode mapping but can be given a unique Google one
                all_representations.setdefault(_i["UCS.PUA.Google"], {}).update(_i)
            else:
                # i.e. doesn't have a unique Google mapping but can be given a unique Unicode one
                del _i["Name.Google"]
                del _i["UCS.PUA.Google"]
                all_representations.setdefault(_i["UCS.Key"], {}).update(_i)
    for _i in all_representations.copy().values():
        if "UCS.Key" in _i:
            del _i["UCS.Key"] # Has served its purpose now
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
        if "UCS.Pictorial" in _i:
            pictorial = _i["UCS.Pictorial"]
            if pictorial not in all_representations:
                all_representations[pictorial] = {"UCS.Standard": pictorial}
            arp = all_representations[pictorial]
            arp["HREF.au"] = _i["HREF.au"]
            arp["ID.au"] = _i["ID.au"]
            arp["JIS.au"] = _i["JIS.au"]
            arp["Shift_JIS.au.afterjis"] = _i["Shift_JIS.au.afterjis"]
            arp["Shift_JIS.au.withinjis"] = _i["Shift_JIS.au.withinjis"]
            arp["UCS.PUA.au.app"] = _i["UCS.PUA.au.app"]
            arp["UCS.PUA.au.web"] = _i["UCS.PUA.au.web"]
            arp["UCS.Pictorial"] = _i["UCS.Pictorial"]
            arp["UCS.Symbolic"] = _i["UCS.Symbolic"]
    for (myset, u, ofst) in ((graphdata.gsets["zdings_g0"][2], "SBCS.ZapfDingbats", 0x21),
                       (graphdata.rhses["998000"], "SBCS.ZapfDingbats", 0x80),
                       (graphdata.gsets["webdings_g0"][2], "SBCS.Webdings", 0x21),
                       (graphdata.rhses["999000"], "SBCS.Webdings", 0x80),
                       (graphdata.gsets["wingdings1_g0"][2], "SBCS.Wingdings_1", 0x21),
                       (graphdata.rhses["999001"], "SBCS.Wingdings_1", 0x80),
                       (graphdata.gsets["wingdings2_g0"][2], "SBCS.Wingdings_2", 0x21),
                       (graphdata.rhses["999002"], "SBCS.Wingdings_2", 0x80),
                       (graphdata.gsets["wingdings3_g0"][2], "SBCS.Wingdings_3", 0x21),
                       (graphdata.rhses["999003"], "SBCS.Wingdings_3", 0x80)):
        for code in myset:
            if not code:
                continue
            scode = "".join(chr(i) for i in code)
            if scode not in counts_as_emoji:
                continue
            scode = add_fe0f.get(scode, scode)
            _get_ref(all_representations, scode)[u] = bytes([ofst + myset.index(code)])
    for (myset, u, ofst) in ((graphdata.gsets["ir233"][2], "JIS.2004", 0x20),
                             (japan.arib_extonly, "JIS.ARIB", 0x20),
                             (graphdata.gsets["ir149-2002"][2], "MBCS_EUC.Wansung", 0xA0),
                             (graphdata.gsets["ir202-full"][2], "MBCS_EUC.KPS", 0xA0)):
        for code in myset:
            if not code:
                continue
            scode = "".join(chr(i) for i in code)
            if scode not in counts_as_emoji:
                continue
            scode = add_fe0f.get(scode, scode)
            pointer = myset.index(code)
            ku = (pointer // 94) + 1
            ten = (pointer % 94) + 1
            _get_ref(all_representations, scode)[u] = bytes([ku + ofst, ten + ofst])
    for (myset, u, ofst) in ((graphdata.gsets["ir168mac"][2], "Shift_JIS.KanjiTalk7", 0x20),
                             (graphdata.gsets["ir233"][2], "Shift_JIS.2004", 0x20),
                             (japan.arib_extonly, "Shift_JIS.ARIB", 0x20)):
        for code in myset:
            if not code:
                continue
            scode = "".join(chr(i) for i in code)
            if scode not in counts_as_emoji:
                continue
            scode = add_fe0f.get(scode, scode)
            pointer = myset.index(code)
            lead = (pointer // 188)
            lead += (0x81 if lead < 0x1F else 0xC1)
            trail = (pointer % 188)
            trail += (0x40 if trail < 0x3F else 0x41)
            _get_ref(all_representations, scode)[u] = bytes([lead, trail])
    for _i in all_representations.copy().values():
        if "UCS.Standard" in _i:
            ucsname = namedata.get_ucsname(_i["UCS.Standard"].rstrip("\uFE0E\uFE0F"), None)
            if ucsname:
                _i["Name.Unicode"] = ucsname
            #
            cldrname = namedata.get_cldrname(_i["UCS.Standard"], None, fallback=False)
            if cldrname:
                _i["Name.CLDR"] = cldrname
    return all_representations

def tabulate_pua(all_representations, specific_pua, f):
    by_pua = {}
    for _i in all_representations.values():
        if specific_pua in _i:
            if "UCS.Standard" in _i:
                by_pua[_i[specific_pua]] = _i["UCS.Standard"]
            elif "UCS.Suggested" in _i:
                by_pua[_i[specific_pua]] = _i["UCS.Suggested"]
            elif "UCS.Substitute" in _i:
                by_pua[_i[specific_pua]] = _i["UCS.Substitute"]
            else:
                by_pua[_i[specific_pua]] = _i[specific_pua]
    lines = sorted(list(set(ord(i) >> 4 for i in by_pua.keys())))
    f.write("<!DOCTYPE html>")
    f.write("""\
<style>
table, th, td {
    border: 1px solid black;
}
th {
    background: papayawhip;
}
td {
    width: 5vw;
}</style>""")
    f.write("<table style=' border-collapse: collapse;'><tr><th></th>")
    for cell in range(16):
        f.write("<th>_{:X}</th>".format(cell))
    last = lines[0] - 1
    for line in lines:
        if line != (last + 1):
            f.write("<tr><td colspan=17 style='text-align: center; background: dimgray;'>. . .</td></tr>")
        f.write("<tr><th>U+{:03X}_</th>".format(line))
        for cell in range(16):
            puapoint = chr((line << 4) | cell)
            if puapoint in by_pua:
                f.write("<td>{}</td>".format(by_pua[puapoint]))
            else:
                f.write("<td style='background: dimgray;'></td>")
        last = line
    f.write("</table>")

if __name__ == "__main__":
    from pprint import pformat, pprint
    all_representations = get_all_representations()
    open("BlendedEmojiData.txt", "w").write(pformat(all_representations))
    tabulate_pua(all_representations, "UCS.PUA.au.app", open("KDDIapp.html", "w"))
    tabulate_pua(all_representations, "UCS.PUA.au.web", open("KDDIweb.html", "w"))
    tabulate_pua(all_representations, "UCS.PUA.DoCoMo", open("docomo.html", "w"))
    tabulate_pua(all_representations, "UCS.PUA.SoftBank", open("softbank.html", "w"))
    tabulate_pua(all_representations, "UCS.PUA.Google", open("google.html", "w"))



