#!/usr/bin/env python3
# -*- mode: python; charset: utf-8 -*-
# Written by HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd
from ecma35.data import maxmat, graphdata
from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte.cellemojidata import all_jcarrier_raw, gspua_to_ucs_possibs

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
            arp["Name.Unicode"] = ucd.name(_i["UCS.Pictorial"][0])
    return all_representations
