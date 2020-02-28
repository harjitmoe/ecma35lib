#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json
import unicodedata as ucd
from ecma35.data import graphdata
from ecma35.data.multibyte import mbmapparsers as parsers

initials = {'\u3131': '\u1100', '\u3132': '\u1101', '\u3134': '\u1102', '\u3137': '\u1103', '\u3138': '\u1104', '\u3139': '\u1105', '\u3141': '\u1106', '\u3142': '\u1107', '\u3143': '\u1108', '\u3145': '\u1109', '\u3146': '\u110a', '\u3147': '\u110b', '\u3148': '\u110c', '\u3149': '\u110d', '\u314a': '\u110e', '\u314b': '\u110f', '\u314c': '\u1110', '\u314d': '\u1111', '\u314e': '\u1112', '\u3165': '\u1114', '\u3166': '\u1115', '\u3167': '\u115b', '\u316a': '\ua966', '\u316e': '\u111c', '\u316f': '\ua971', '\u3171': '\u111d', '\u3172': '\u111e', '\u3173': '\u1120', '\u3174': '\u1122', '\u3175': '\u1123', '\u3176': '\u1127', '\u3177': '\u1129', '\u3178': '\u112b', '\u3179': '\u112c', '\u317a': '\u112d', '\u317b': '\u112e', '\u317c': '\u112f', '\u317d': '\u1132', '\u317e': '\u1136', '\u317f': '\u1140', '\u3180': '\u1147', '\u3181': '\u114c', '\u3184': '\u1157', '\u3185': '\u1158', '\u3186': '\u1159', '\u3164': '\u115f'}

vowels = {'\u314f': '\u1161', '\u3150': '\u1162', '\u3151': '\u1163', '\u3152': '\u1164', '\u3153': '\u1165', '\u3154': '\u1166', '\u3155': '\u1167', '\u3156': '\u1168', '\u3157': '\u1169', '\u3158': '\u116a', '\u3159': '\u116b', '\u315a': '\u116c', '\u315b': '\u116d', '\u315c': '\u116e', '\u315d': '\u116f', '\u315e': '\u1170', '\u315f': '\u1171', '\u3160': '\u1172', '\u3161': '\u1173', '\u3162': '\u1174', '\u3163': '\u1175', '\u3187': '\u1184', '\u3188': '\u1185', '\u3189': '\u1188', '\u318a': '\u1191', '\u318b': '\u1192', '\u318c': '\u1194', '\u318d': '\u119e', '\u318e': '\u11a1', '\u3164': '\u1160'}

finals = {'\u3132': '\u11a9', '\u3133': '\u11aa', '\u3135': '\u11ac', '\u3136': '\u11ad', '\u313c': '\u11b2', '\u313d': '\u11b3', '\u313e': '\u11b4', '\u313f': '\u11b5', '\u3140': '\u11b6', '\u314b': '\u11bf', '\u3137': '\u11ae', '\u313a': '\u11b0', '\u313b': '\u11b1', '\u3144': '\u11b9', '\u3148': '\u11bd', '\u314a': '\u11be', '\u314c': '\u11c0', '\u314d': '\u11c1', '\u314e': '\u11c2', '\u3141': '\u11b7', '\u3142': '\u11b8', '\u3146': '\u11bb', '\u3131': '\u11a8', '\u3145': '\u11ba', '\u3147': '\u11bc', '\u3134': '\u11ab', '\u3139': '\u11af', '\u3165': '\u11ff', '\u3166': '\u11c6', '\u3167': '\u11c7', '\u3168': '\u11c8', '\u3169': '\u11cc', '\u316a': '\u11ce', '\u316b': '\u11d3', '\u316c': '\u11d7', '\u316d': '\u11d9', '\u316e': '\u11dc', '\u316f': '\u11dd', '\u3170': '\u11df', '\u3171': '\u11e2', '\u3173': '\ud7e3', '\u3175': '\ud7e7', '\u3176': '\ud7e8', '\u3178': '\u11e6', '\u317a': '\u11e7', '\u317c': '\u11e8', '\u317d': '\u11ea', '\u317e': '\ud7ef', '\u317f': '\u11eb', '\u3180': '\u11ee', '\u3181': '\u11f0', '\u3182': '\u11f1', '\u3183': '\u11f2', '\u3184': '\u11f4', '\u3186': '\u11f9', '\u3164': ''}

compjamo = set(finals.keys()) | set(vowels.keys()) | set(initials.keys())

def _sort_by_kps(syll):
    deco = ucd.normalize("NFD", chr(syll))
    if len(deco) == 2:
        init, vow = deco
        fin = ""
    else:
        init, vow, fin = deco
    return (i_order[init], v_order[vow], f_order[fin])

# KS C 5601 / KS X 1001 EUC-KR Wansung RHS
graphdata.gsets["ir149"] = wansung = (94, 2, parsers.read_main_plane("WHATWG/index-euc-kr.txt", euckrlike=True))
# Since graphdata.gsets isn't merely a dict, the above line also sets graphdata.codepoint_coverages

# The main-plane part of Apple's Wansung version, as opposed to its sidecarriage or
#   single-byte extensions (mostly C1 replacements)
graphdata.gsets["ir149-mac"] = macwansung = (94, 2, tuple(parsers.ahmap(0, tuple(i)) if i is not None 
    else None for i in json.load(open(os.path.join(parsers.directory, "Vendor/macWansung.json"), "r"))))

# KPS 9566
graphdata.gsets["ir202"] = kps9566 = (94, 2, parsers.read_main_plane("UTC/KPS9566.TXT", euckrlike=True))
i_order = tuple(initials[_i] for _i in "ㄱㄴㄷㄹㅁㅂㅅㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉㅇ")
i_order = dict((_i, i_order.index(_i)) for _i in i_order)
v_order = tuple(vowels[_i] for _i in "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖㅚㅟㅢㅘㅝㅙㅞ")
v_order = dict((_i, v_order.index(_i)) for _i in v_order)
f_order = tuple(finals[_i] for _i in "ㄱㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅇㅈㅊㅋㅌㅍㅎㄲㅆ")
f_order = dict((_i, f_order.index(_i) + 1) for _i in f_order)
f_order[""] = 0

# Amounting to the entirety of the UHC extensions, in order:
non_wangsung_johab = [i for i in range(0xAC00, 0xD7A4) 
                        if i not in graphdata.codepoint_coverages["ir149"]]

# Similarly for the KPS encoding
non_kps9566_johab = [i for i in range(0xAC00, 0xD7A4) 
                       if i not in graphdata.codepoint_coverages["ir202"]]
non_kps9566_johab.sort(key = _sort_by_kps)



