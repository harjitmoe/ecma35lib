#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2021/2022/2023/2024/2025/2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Korea (both South and North)

import os, json, shutil
from ecma35.data import graphdata, variationhints, deprecated_cjkci
from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.names import namedata

_temp = []
def read_kps9566extras(fil):
    cachefn = os.path.join(parsers.cachedirectory,
              os.path.splitext(fil)[0].replace("/", "---") + "_kps9566extras2.json")
    if os.path.exists(cachefn):
        return parsers.LazyJSON(cachefn)
    for _i in open(os.path.join(parsers.directory, fil), "r", encoding="utf-8"):
        if (not _i.strip()) or _i[0] == "#":
            continue
        byts, ucs = _i.split("\t", 2)[:2]
        if len(byts) >= 6:
            lead = int(byts[2:4], 16)
            trail = int(byts[4:6], 16)
            if (lead < 0xC8) or (trail > 0xA0):
                continue
            first = lead - 0xA1
            if trail >= 0x81:
                last = trail - 0x41 - 12
            elif trail >= 0x61:
                last = trail - 0x41 - 6
            else:
                last = trail - 0x41
            newpointer = (94 * first) + last
        else:
            continue
        #
        if len(_temp) > newpointer:
            assert _temp[newpointer] is None, (newpointer, int(ucs[2:], 16), _temp[newpointer])
            _temp[newpointer] = (int(ucs[2:], 16),)
        else:
            while len(_temp) < newpointer:
                _temp.append(None)
            _temp.append((int(ucs[2:], 16),))
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    # Write output cache.
    f = open(cachefn, "w")
    f.write(json.dumps(r))
    f.close()
    return r

initials = {'\u3131': '\u1100', '\u3132': '\u1101', '\u3134': '\u1102', '\u3137': '\u1103', '\u3138': '\u1104', '\u3139': '\u1105', '\u3141': '\u1106', '\u3142': '\u1107', '\u3143': '\u1108', '\u3145': '\u1109', '\u3146': '\u110a', '\u3147': '\u110b', '\u3148': '\u110c', '\u3149': '\u110d', '\u314a': '\u110e', '\u314b': '\u110f', '\u314c': '\u1110', '\u314d': '\u1111', '\u314e': '\u1112', '\u3165': '\u1114', '\u3166': '\u1115', '\u3167': '\u115b', '\u316a': '\ua966', '\u316e': '\u111c', '\u316f': '\ua971', '\u3171': '\u111d', '\u3172': '\u111e', '\u3173': '\u1120', '\u3174': '\u1122', '\u3175': '\u1123', '\u3176': '\u1127', '\u3177': '\u1129', '\u3178': '\u112b', '\u3179': '\u112c', '\u317a': '\u112d', '\u317b': '\u112e', '\u317c': '\u112f', '\u317d': '\u1132', '\u317e': '\u1136', '\u317f': '\u1140', '\u3180': '\u1147', '\u3181': '\u114c', '\u3184': '\u1157', '\u3185': '\u1158', '\u3186': '\u1159', '\u3164': '\u115f'}

for i in "ᄼ", "ᄽ", "ᄾ", "ᄿ", "ᅎ", "ᅏ", "ᅐ", "ᅑ", "ᅔ", "ᅕ":
    initials[i] = i

compinitials = {('ᄼ', 'ᄼ'): 'ᄽ', ('ᄾ', 'ᄾ'): 'ᄿ', ('ᅎ', 'ᅎ'): 'ᅏ', ('ᅐ', 'ᅐ'): 'ᅑ', ('ㄱ', 'ㄱ'): 'ᄁ', ('ㄱ', 'ㄷ'): 'ᅚ', ('ㄴ', 'ㄱ'): 'ᄓ', ('ㄴ', 'ㄴ'): 'ᄔ', ('ㄴ', 'ㄷ'): 'ᄕ', ('ㄴ', 'ㅂ'): 'ᄖ', ('ㄴ', 'ㅅ'): 'ᅛ', ('ㄴ', 'ㅈ'): 'ᅜ', ('ㄴ', 'ㅎ'): 'ᅝ', ('ㄷ', 'ㄱ'): 'ᄗ', ('ㄷ', 'ㄷ'): 'ᄄ', ('ㄷ', 'ㄹ'): 'ᅞ', ('ㄷ', 'ㅁ'): 'ꥠ', ('ㄷ', 'ㅂ'): 'ꥡ', ('ㄷ', 'ㅅ'): 'ꥢ', ('ㄷ', 'ㅈ'): 'ꥣ', ('ㄹ', '̥'): 'ᄛ', ('ㄹ', '∘'): 'ᄛ', ('ㄹ', '◦'): 'ᄛ', ('ㄹ', 'ㄱ'): 'ꥤ', ('ㄹ', 'ㄱ', 'ㄱ'): 'ꥥ', ('ㄹ', 'ㄲ'): 'ꥥ', ('ㄹ', 'ㄴ'): 'ᄘ', ('ㄹ', 'ㄷ'): 'ꥦ', ('ㄹ', 'ㄷ', 'ㄷ'): 'ꥧ', ('ㄹ', 'ㄸ'): 'ꥧ', ('ㄹ', 'ㄹ'): 'ᄙ', ('ㄹ', 'ㅁ'): 'ꥨ', ('ㄹ', 'ㅂ'): 'ꥩ', ('ㄹ', 'ㅂ', '̥'): 'ꥫ', ('ㄹ', 'ㅂ', '∘'): 'ꥫ', ('ㄹ', 'ㅂ', '◦'): 'ꥫ', ('ㄹ', 'ㅂ', 'ㅂ'): 'ꥪ', ('ㄹ', 'ㅃ'): 'ꥪ', ('ㄹ', 'ㅅ'): 'ꥬ', ('ㄹ', 'ㅈ'): 'ꥭ', ('ㄹ', 'ㅋ'): 'ꥮ', ('ㄹ', 'ㅎ'): 'ᄚ', ('ㄹ', 'ㅸ'): 'ꥫ', ('ㄺ', 'ㄱ'): 'ꥥ', ('ㄼ', '̥'): 'ꥫ', ('ㄼ', '∘'): 'ꥫ', ('ㄼ', '◦'): 'ꥫ', ('ㄼ', 'ㅂ'): 'ꥪ', ('ㅁ', '̥'): 'ᄝ', ('ㅁ', '∘'): 'ᄝ', ('ㅁ', '◦'): 'ᄝ', ('ㅁ', 'ㄱ'): 'ꥯ', ('ㅁ', 'ㄷ'): 'ꥰ', ('ㅁ', 'ㅂ'): 'ᄜ', ('ㅁ', 'ㅅ'): 'ꥱ', ('ㅂ', '̥'): 'ᄫ', ('ㅂ', '∘'): 'ᄫ', ('ㅂ', '◦'): 'ᄫ', ('ㅂ', 'ㄱ'): 'ᄞ', ('ㅂ', 'ㄴ'): 'ᄟ', ('ㅂ', 'ㄷ'): 'ᄠ', ('ㅂ', 'ㅂ'): 'ᄈ', ('ㅂ', 'ㅂ', '̥'): 'ᄬ', ('ㅂ', 'ㅂ', '∘'): 'ᄬ', ('ㅂ', 'ㅂ', '◦'): 'ᄬ', ('ㅂ', 'ㅅ'): 'ᄡ', ('ㅂ', 'ㅅ', 'ㄱ'): 'ᄢ', ('ㅂ', 'ㅅ', 'ㄷ'): 'ᄣ', ('ㅂ', 'ㅅ', 'ㅂ'): 'ᄤ', ('ㅂ', 'ㅅ', 'ㅅ'): 'ᄥ', ('ㅂ', 'ㅅ', 'ㅈ'): 'ᄦ', ('ㅂ', 'ㅅ', 'ㅌ'): 'ꥲ', ('ㅂ', 'ㅆ'): 'ᄥ', ('ㅂ', 'ㅈ'): 'ᄧ', ('ㅂ', 'ㅊ'): 'ᄨ', ('ㅂ', 'ㅋ'): 'ꥳ', ('ㅂ', 'ㅌ'): 'ᄩ', ('ㅂ', 'ㅍ'): 'ᄪ', ('ㅂ', 'ㅎ'): 'ꥴ', ('ㅂ', 'ㅸ'): 'ᄬ', ('ㅂ', 'ㅺ'): 'ᄢ', ('ㅂ', 'ㅼ'): 'ᄣ', ('ㅂ', 'ㅽ'): 'ᄤ', ('ㅂ', 'ㅾ'): 'ᄦ', ('ㅃ', '̥'): 'ᄬ', ('ㅃ', '∘'): 'ᄬ', ('ㅃ', '◦'): 'ᄬ', ('ㅄ', 'ㄱ'): 'ᄢ', ('ㅄ', 'ㄷ'): 'ᄣ', ('ㅄ', 'ㅂ'): 'ᄤ', ('ㅄ', 'ㅅ'): 'ᄥ', ('ㅄ', 'ㅈ'): 'ᄦ', ('ㅄ', 'ㅌ'): 'ꥲ', ('ㅅ', 'ㄱ'): 'ᄭ', ('ㅅ', 'ㄴ'): 'ᄮ', ('ㅅ', 'ㄷ'): 'ᄯ', ('ㅅ', 'ㄹ'): 'ᄰ', ('ㅅ', 'ㅁ'): 'ᄱ', ('ㅅ', 'ㅂ'): 'ᄲ', ('ㅅ', 'ㅂ', 'ㄱ'): 'ᄳ', ('ㅅ', 'ㅅ'): 'ᄊ', ('ㅅ', 'ㅅ', 'ㅂ'): 'ꥵ', ('ㅅ', 'ㅅ', 'ㅅ'): 'ᄴ', ('ㅅ', 'ㅆ'): 'ᄴ', ('ㅅ', 'ㅇ'): 'ᄵ', ('ㅅ', 'ㅈ'): 'ᄶ', ('ㅅ', 'ㅊ'): 'ᄷ', ('ㅅ', 'ㅋ'): 'ᄸ', ('ㅅ', 'ㅌ'): 'ᄹ', ('ㅅ', 'ㅍ'): 'ᄺ', ('ㅅ', 'ㅎ'): 'ᄻ', ('ㅅ', 'ㅲ'): 'ᄳ', ('ㅅ', 'ㅽ'): 'ꥵ', ('ㅆ', 'ㅂ'): 'ꥵ', ('ㅆ', 'ㅅ'): 'ᄴ', ('ㅇ', 'ㄱ'): 'ᅁ', ('ㅇ', 'ㄷ'): 'ᅂ', ('ㅇ', 'ㄹ'): 'ꥶ', ('ㅇ', 'ㅁ'): 'ᅃ', ('ㅇ', 'ㅂ'): 'ᅄ', ('ㅇ', 'ㅅ'): 'ᅅ', ('ㅇ', 'ㅇ'): 'ᅇ', ('ㅇ', 'ㅈ'): 'ᅈ', ('ㅇ', 'ㅊ'): 'ᅉ', ('ㅇ', 'ㅌ'): 'ᅊ', ('ㅇ', 'ㅍ'): 'ᅋ', ('ㅇ', 'ㅎ'): 'ꥷ', ('ㅇ', 'ㅿ'): 'ᅆ', ('ㅈ', 'ㅇ'): 'ᅍ', ('ㅈ', 'ㅈ'): 'ᄍ', ('ㅈ', 'ㅈ', 'ㅎ'): 'ꥸ', ('ㅉ', 'ㅎ'): 'ꥸ', ('ㅊ', 'ㅋ'): 'ᅒ', ('ㅊ', 'ㅎ'): 'ᅓ', ('ㅌ', 'ㅌ'): 'ꥹ', ('ㅍ', '̥'): 'ᅗ', ('ㅍ', '∘'): 'ᅗ', ('ㅍ', '◦'): 'ᅗ', ('ㅍ', 'ㅂ'): 'ᅖ', ('ㅍ', 'ㅎ'): 'ꥺ', ('ㅎ', 'ㅅ'): 'ꥻ', ('ㅎ', 'ㅎ'): 'ᅘ', ('ㅪ', 'ㄷ'): 'ꥧ', ('ㅽ', 'ㄱ'): 'ᄳ', ('ㆆ', 'ㆆ'): 'ꥼ'}

vowels = {'\u314f': '\u1161', '\u3150': '\u1162', '\u3151': '\u1163', '\u3152': '\u1164', '\u3153': '\u1165', '\u3154': '\u1166', '\u3155': '\u1167', '\u3156': '\u1168', '\u3157': '\u1169', '\u3158': '\u116a', '\u3159': '\u116b', '\u315a': '\u116c', '\u315b': '\u116d', '\u315c': '\u116e', '\u315d': '\u116f', '\u315e': '\u1170', '\u315f': '\u1171', '\u3160': '\u1172', '\u3161': '\u1173', '\u3162': '\u1174', '\u3163': '\u1175', '\u3187': '\u1184', '\u3188': '\u1185', '\u3189': '\u1188', '\u318a': '\u1191', '\u318b': '\u1192', '\u318c': '\u1194', '\u318d': '\u119e', '\u318e': '\u11a1', '\u3164': '\u1160'}

compvowels = {('ㅏ', 'ㅗ'): 'ᅶ', ('ㅏ', 'ㅜ'): 'ᅷ', ('ㅏ', 'ㅡ'): 'ᆣ', ('ㅑ', 'ㅗ'): 'ᅸ', ('ㅑ', 'ㅛ'): 'ᅹ', ('ㅑ', 'ㅜ'): 'ᆤ', ('ㅓ', 'ㅗ'): 'ᅺ', ('ㅓ', 'ㅜ'): 'ᅻ', ('ㅓ', 'ㅡ'): 'ᅼ', ('ㅕ', 'ㅑ'): 'ᆥ', ('ㅕ', 'ㅗ'): 'ᅽ', ('ㅕ', 'ㅜ'): 'ᅾ', ('ㅗ', 'ㅑ'): 'ᆦ', ('ㅗ', 'ㅒ'): 'ᆧ', ('ㅗ', 'ㅓ'): 'ᅿ', ('ㅗ', 'ㅔ'): 'ᆀ', ('ㅗ', 'ㅕ'): 'ힰ', ('ㅗ', 'ㅖ'): 'ᆁ', ('ㅗ', 'ㅗ'): 'ᆂ', ('ㅗ', 'ㅗ', 'ㅣ'): 'ힱ', ('ㅗ', 'ㅜ'): 'ᆃ', ('ㅛ', 'ㅏ'): 'ힲ', ('ㅛ', 'ㅐ'): 'ힳ', ('ㅛ', 'ㅑ'): 'ᆄ', ('ㅛ', 'ㅒ'): 'ᆅ', ('ㅛ', 'ㅓ'): 'ힴ', ('ㅛ', 'ㅕ'): 'ᆆ', ('ㅛ', 'ㅗ'): 'ᆇ', ('ㅛ', 'ㅣ'): 'ᆈ', ('ㅜ', 'ㅏ'): 'ᆉ', ('ㅜ', 'ㅐ'): 'ᆊ', ('ㅜ', 'ㅓ', 'ㅡ'): 'ᆋ', ('ㅜ', 'ㅕ'): 'ힵ', ('ㅜ', 'ㅖ'): 'ᆌ', ('ㅜ', 'ㅜ'): 'ᆍ', ('ㅜ', 'ㅣ', 'ㅣ'): 'ힶ', ('ㅠ', 'ㅏ'): 'ᆎ', ('ㅠ', 'ㅐ'): 'ힷ', ('ㅠ', 'ㅓ'): 'ᆏ', ('ㅠ', 'ㅔ'): 'ᆐ', ('ㅠ', 'ㅕ'): 'ᆑ', ('ㅠ', 'ㅖ'): 'ᆒ', ('ㅠ', 'ㅗ'): 'ힸ', ('ㅠ', 'ㅜ'): 'ᆓ', ('ㅠ', 'ㅣ'): 'ᆔ', ('ㅡ', 'ㅏ'): 'ힹ', ('ㅡ', 'ㅓ'): 'ힺ', ('ㅡ', 'ㅔ'): 'ힻ', ('ㅡ', 'ㅗ'): 'ힼ', ('ㅡ', 'ㅜ'): 'ᆕ', ('ㅡ', 'ㅡ'): 'ᆖ', ('ㅢ', 'ㅜ'): 'ᆗ', ('ㅣ', 'ㅏ'): 'ᆘ', ('ㅣ', 'ㅑ'): 'ᆙ', ('ㅣ', 'ㅑ', 'ㅗ'): 'ힽ', ('ㅣ', 'ㅒ'): 'ힾ', ('ㅣ', 'ㅕ'): 'ힿ', ('ㅣ', 'ㅖ'): 'ퟀ', ('ㅣ', 'ㅗ'): 'ᆚ', ('ㅣ', 'ㅗ', 'ㅣ'): 'ퟁ', ('ㅣ', 'ㅛ'): 'ퟂ', ('ㅣ', 'ㅜ'): 'ᆛ', ('ㅣ', 'ㅠ'): 'ퟃ', ('ㅣ', 'ㅡ'): 'ᆜ', ('ㅣ', 'ㅣ'): 'ퟄ', ('ㅣ', 'ㆍ'): 'ᆝ', ('ㆍ', 'ㅏ'): 'ퟅ', ('ㆍ', 'ㅓ'): 'ᆟ', ('ㆍ', 'ㅔ'): 'ퟆ', ('ㆍ', 'ㅜ'): 'ᆠ', ('ㆍ', 'ㅣ'): 'ᆡ', ('ㆍ', 'ㆍ'): 'ᆢ'}

finals = {'\u3132': '\u11a9', '\u3133': '\u11aa', '\u3135': '\u11ac', '\u3136': '\u11ad', '\u313c': '\u11b2', '\u313d': '\u11b3', '\u313e': '\u11b4', '\u313f': '\u11b5', '\u3140': '\u11b6', '\u314b': '\u11bf', '\u3137': '\u11ae', '\u313a': '\u11b0', '\u313b': '\u11b1', '\u3144': '\u11b9', '\u3148': '\u11bd', '\u314a': '\u11be', '\u314c': '\u11c0', '\u314d': '\u11c1', '\u314e': '\u11c2', '\u3141': '\u11b7', '\u3142': '\u11b8', '\u3146': '\u11bb', '\u3131': '\u11a8', '\u3145': '\u11ba', '\u3147': '\u11bc', '\u3134': '\u11ab', '\u3139': '\u11af', '\u3165': '\u11ff', '\u3166': '\u11c6', '\u3167': '\u11c7', '\u3168': '\u11c8', '\u3169': '\u11cc', '\u316a': '\u11ce', '\u316b': '\u11d3', '\u316c': '\u11d7', '\u316d': '\u11d9', '\u316e': '\u11dc', '\u316f': '\u11dd', '\u3170': '\u11df', '\u3171': '\u11e2', '\u3173': '\ud7e3', '\u3175': '\ud7e7', '\u3176': '\ud7e8', '\u3178': '\u11e6', '\u317a': '\u11e7', '\u317c': '\u11e8', '\u317d': '\u11ea', '\u317e': '\ud7ef', '\u317f': '\u11eb', '\u3180': '\u11ee', '\u3181': '\u11f0', '\u3182': '\u11f1', '\u3183': '\u11f2', '\u3184': '\u11f4', '\u3186': '\u11f9', '\u3164': ''}

compfinals = {('ㄱ', 'ㄱ'): 'ᆩ', ('ㄱ', 'ㄴ'): 'ᇺ', ('ㄱ', 'ㄹ'): 'ᇃ', ('ㄱ', 'ㅂ'): 'ᇻ', ('ㄱ', 'ㅅ'): 'ᆪ', ('ㄱ', 'ㅅ', 'ㄱ'): 'ᇄ', ('ㄱ', 'ㅊ'): 'ᇼ', ('ㄱ', 'ㅋ'): 'ᇽ', ('ㄱ', 'ㅎ'): 'ᇾ', ('ㄱ', 'ㅺ'): 'ᇄ', ('ㄳ', 'ㄱ'): 'ᇄ', ('ㄴ', 'ㄱ'): 'ᇅ', ('ㄴ', 'ㄴ'): 'ᇿ', ('ㄴ', 'ㄷ'): 'ᇆ', ('ㄴ', 'ㄹ'): 'ퟋ', ('ㄴ', 'ㅅ'): 'ᇇ', ('ㄴ', 'ㅈ'): 'ᆬ', ('ㄴ', 'ㅊ'): 'ퟌ', ('ㄴ', 'ㅌ'): 'ᇉ', ('ㄴ', 'ㅎ'): 'ᆭ', ('ㄴ', 'ㅿ'): 'ᇈ', ('ㄷ', 'ㄱ'): 'ᇊ', ('ㄷ', 'ㄷ'): 'ퟍ', ('ㄷ', 'ㄷ', 'ㅂ'): 'ퟎ', ('ㄷ', 'ㄹ'): 'ᇋ', ('ㄷ', 'ㅂ'): 'ퟏ', ('ㄷ', 'ㅅ'): 'ퟐ', ('ㄷ', 'ㅅ', 'ㄱ'): 'ퟑ', ('ㄷ', 'ㅈ'): 'ퟒ', ('ㄷ', 'ㅊ'): 'ퟓ', ('ㄷ', 'ㅌ'): 'ퟔ', ('ㄷ', 'ㅺ'): 'ퟑ', ('ㄸ', 'ㅂ'): 'ퟎ', ('ㄹ', '̥'): 'ퟝ', ('ㄹ', '∘'): 'ퟝ', ('ㄹ', '◦'): 'ퟝ', ('ㄹ', 'ㄱ'): 'ᆰ', ('ㄹ', 'ㄱ', 'ㄱ'): 'ퟕ', ('ㄹ', 'ㄱ', 'ㅅ'): 'ᇌ', ('ㄹ', 'ㄱ', 'ㅎ'): 'ퟖ', ('ㄹ', 'ㄲ'): 'ퟕ', ('ㄹ', 'ㄳ'): 'ᇌ', ('ㄹ', 'ㄴ'): 'ᇍ', ('ㄹ', 'ㄷ'): 'ᇎ', ('ㄹ', 'ㄷ', 'ㅎ'): 'ᇏ', ('ㄹ', 'ㄹ'): 'ᇐ', ('ㄹ', 'ㄹ', 'ㅋ'): 'ퟗ', ('ㄹ', 'ㅁ'): 'ᆱ', ('ㄹ', 'ㅁ', 'ㄱ'): 'ᇑ', ('ㄹ', 'ㅁ', 'ㅅ'): 'ᇒ', ('ㄹ', 'ㅁ', 'ㅎ'): 'ퟘ', ('ㄹ', 'ㅂ'): 'ᆲ', ('ㄹ', 'ㅂ', '̥'): 'ᇕ', ('ㄹ', 'ㅂ', '∘'): 'ᇕ', ('ㄹ', 'ㅂ', '◦'): 'ᇕ', ('ㄹ', 'ㅂ', 'ㄷ'): 'ퟙ', ('ㄹ', 'ㅂ', 'ㅅ'): 'ᇓ', ('ㄹ', 'ㅂ', 'ㅍ'): 'ퟚ', ('ㄹ', 'ㅂ', 'ㅎ'): 'ᇔ', ('ㄹ', 'ㅄ'): 'ᇓ', ('ㄹ', 'ㅅ'): 'ᆳ', ('ㄹ', 'ㅅ', 'ㅅ'): 'ᇖ', ('ㄹ', 'ㅆ'): 'ᇖ', ('ㄹ', 'ㅋ'): 'ᇘ', ('ㄹ', 'ㅌ'): 'ᆴ', ('ㄹ', 'ㅍ'): 'ᆵ', ('ㄹ', 'ㅎ'): 'ᆶ', ('ㄹ', 'ㅯ'): 'ᇒ', ('ㄹ', 'ㅳ'): 'ퟙ', ('ㄹ', 'ㅸ'): 'ᇕ', ('ㄹ', 'ㅿ'): 'ᇗ', ('ㄹ', 'ㆁ'): 'ퟛ', ('ㄹ', 'ㆆ'): 'ᇙ', ('ㄹ', 'ㆆ', 'ㅎ'): 'ퟜ', ('ㄺ', 'ㄱ'): 'ퟕ', ('ㄺ', 'ㅅ'): 'ᇌ', ('ㄺ', 'ㅎ'): 'ퟖ', ('ㄻ', 'ㄱ'): 'ᇑ', ('ㄻ', 'ㅅ'): 'ᇒ', ('ㄻ', 'ㅎ'): 'ퟘ', ('ㄼ', '̥'): 'ᇕ', ('ㄼ', '∘'): 'ᇕ', ('ㄼ', '◦'): 'ᇕ', ('ㄼ', 'ㄷ'): 'ퟙ', ('ㄼ', 'ㅅ'): 'ᇓ', ('ㄼ', 'ㅍ'): 'ퟚ', ('ㄼ', 'ㅎ'): 'ᇔ', ('ㄽ', 'ㅅ'): 'ᇖ', ('ㅁ', '̥'): 'ᇢ', ('ㅁ', '∘'): 'ᇢ', ('ㅁ', '◦'): 'ᇢ', ('ㅁ', 'ㄱ'): 'ᇚ', ('ㅁ', 'ㄴ'): 'ퟞ', ('ㅁ', 'ㄴ', 'ㄴ'): 'ퟟ', ('ㅁ', 'ㄹ'): 'ᇛ', ('ㅁ', 'ㅁ'): 'ퟠ', ('ㅁ', 'ㅂ'): 'ᇜ', ('ㅁ', 'ㅂ', 'ㅅ'): 'ퟡ', ('ㅁ', 'ㅄ'): 'ퟡ', ('ㅁ', 'ㅅ'): 'ᇝ', ('ㅁ', 'ㅅ', 'ㅅ'): 'ᇞ', ('ㅁ', 'ㅆ'): 'ᇞ', ('ㅁ', 'ㅈ'): 'ퟢ', ('ㅁ', 'ㅊ'): 'ᇠ', ('ㅁ', 'ㅎ'): 'ᇡ', ('ㅁ', 'ㅥ'): 'ퟟ', ('ㅁ', 'ㅿ'): 'ᇟ', ('ㅂ', '̥'): 'ᇦ', ('ㅂ', '∘'): 'ᇦ', ('ㅂ', '◦'): 'ᇦ', ('ㅂ', 'ㄷ'): 'ퟣ', ('ㅂ', 'ㄹ'): 'ᇣ', ('ㅂ', 'ㄹ', 'ㅍ'): 'ퟤ', ('ㅂ', 'ㄿ'): 'ퟤ', ('ㅂ', 'ㅁ'): 'ퟥ', ('ㅂ', 'ㅂ'): 'ퟦ', ('ㅂ', 'ㅅ'): 'ᆹ', ('ㅂ', 'ㅅ', 'ㄷ'): 'ퟧ', ('ㅂ', 'ㅈ'): 'ퟨ', ('ㅂ', 'ㅊ'): 'ퟩ', ('ㅂ', 'ㅍ'): 'ᇤ', ('ㅂ', 'ㅎ'): 'ᇥ', ('ㅂ', 'ㅼ'): 'ퟧ', ('ㅄ', 'ㄷ'): 'ퟧ', ('ㅅ', 'ㄱ'): 'ᇧ', ('ㅅ', 'ㄷ'): 'ᇨ', ('ㅅ', 'ㄹ'): 'ᇩ', ('ㅅ', 'ㅁ'): 'ퟪ', ('ㅅ', 'ㅂ'): 'ᇪ', ('ㅅ', 'ㅂ', '̥'): 'ퟫ', ('ㅅ', 'ㅂ', '∘'): 'ퟫ', ('ㅅ', 'ㅂ', '◦'): 'ퟫ', ('ㅅ', 'ㅅ'): 'ᆻ', ('ㅅ', 'ㅅ', 'ㄱ'): 'ퟬ', ('ㅅ', 'ㅅ', 'ㄷ'): 'ퟭ', ('ㅅ', 'ㅈ'): 'ퟯ', ('ㅅ', 'ㅊ'): 'ퟰ', ('ㅅ', 'ㅌ'): 'ퟱ', ('ㅅ', 'ㅎ'): 'ퟲ', ('ㅅ', 'ㅸ'): 'ퟫ', ('ㅅ', 'ㅺ'): 'ퟬ', ('ㅅ', 'ㅼ'): 'ퟭ', ('ㅅ', 'ㅿ'): 'ퟮ', ('ㅆ', 'ㄱ'): 'ퟬ', ('ㅆ', 'ㄷ'): 'ퟭ', ('ㅇ', 'ㄱ'): 'ᇬ', ('ㅇ', 'ㄱ', 'ㄱ'): 'ᇭ', ('ㅇ', 'ㄲ'): 'ᇭ', ('ㅇ', 'ㅇ'): 'ᇮ', ('ㅇ', 'ㅋ'): 'ᇯ', ('ㅈ', 'ㅂ'): 'ퟷ', ('ㅈ', 'ㅂ', 'ㅂ'): 'ퟸ', ('ㅈ', 'ㅃ'): 'ퟸ', ('ㅈ', 'ㅈ'): 'ퟹ', ('ㅍ', '̥'): 'ᇴ', ('ㅍ', '∘'): 'ᇴ', ('ㅍ', '◦'): 'ᇴ', ('ㅍ', 'ㅂ'): 'ᇳ', ('ㅍ', 'ㅅ'): 'ퟺ', ('ㅍ', 'ㅌ'): 'ퟻ', ('ㅎ', 'ㄴ'): 'ᇵ', ('ㅎ', 'ㄹ'): 'ᇶ', ('ㅎ', 'ㅁ'): 'ᇷ', ('ㅎ', 'ㅂ'): 'ᇸ', ('ㅪ', 'ㅎ'): 'ᇏ', ('ㅭ', 'ㅎ'): 'ퟜ', ('ㅮ', 'ㅅ'): 'ퟡ', ('ㅯ', 'ㅅ'): 'ᇞ', ('ㅽ', '̥'): 'ퟫ', ('ㅽ', '∘'): 'ퟫ', ('ㅽ', '◦'): 'ퟫ', ('ㅿ', 'ㅂ'): 'ퟳ', ('ㅿ', 'ㅂ', '̥'): 'ퟴ', ('ㅿ', 'ㅂ', '∘'): 'ퟴ', ('ㅿ', 'ㅂ', '◦'): 'ퟴ', ('ㅿ', 'ㅸ'): 'ퟴ', ('ㆁ', 'ㅁ'): 'ퟵ', ('ㆁ', 'ㅅ'): 'ᇱ', ('ㆁ', 'ㅎ'): 'ퟶ', ('ㆁ', 'ㅿ'): 'ᇲ'}

compsimple = {('ㄱ', 'ㄱ'): 'ㄲ', ('ㄱ', 'ㅅ'): 'ㄳ', ('ㄴ', 'ㄴ'): 'ㅥ', ('ㄴ', 'ㄷ'): 'ㅦ', ('ㄴ', 'ㅅ'): 'ㅧ', ('ㄴ', 'ㅈ'): 'ㄵ', ('ㄴ', 'ㅎ'): 'ㄶ', ('ㄴ', 'ㅿ'): 'ㅨ', ('ㄷ', 'ㄷ'): 'ㄸ', ('ㄹ', 'ㄱ'): 'ㄺ', ('ㄹ', 'ㄱ', 'ㅅ'): 'ㅩ', ('ㄹ', 'ㄷ'): 'ㅪ', ('ㄹ', 'ㅁ'): 'ㄻ', ('ㄹ', 'ㅂ'): 'ㄼ', ('ㄹ', 'ㅂ', 'ㅅ'): 'ㅫ', ('ㄹ', 'ㅅ'): 'ㄽ', ('ㄹ', 'ㅌ'): 'ㄾ', ('ㄹ', 'ㅍ'): 'ㄿ', ('ㄹ', 'ㅎ'): 'ㅀ', ('ㄹ', 'ㅿ'): 'ㅬ', ('ㄹ', 'ㆆ'): 'ㅭ', ('ㅁ', '̥'): 'ㅱ', ('ㅁ', '∘'): 'ㅱ', ('ㅁ', '◦'): 'ㅱ', ('ㅁ', 'ㅂ'): 'ㅮ', ('ㅁ', 'ㅅ'): 'ㅯ', ('ㅁ', 'ㅿ'): 'ㅰ', ('ㅂ', '̥'): 'ㅸ', ('ㅂ', '∘'): 'ㅸ', ('ㅂ', '◦'): 'ㅸ', ('ㅂ', 'ㄱ'): 'ㅲ', ('ㅂ', 'ㄷ'): 'ㅳ', ('ㅂ', 'ㅂ'): 'ㅃ', ('ㅂ', 'ㅂ', '̥'): 'ㅹ', ('ㅂ', 'ㅂ', '∘'): 'ㅹ', ('ㅂ', 'ㅂ', '◦'): 'ㅹ', ('ㅂ', 'ㅅ'): 'ㅄ', ('ㅂ', 'ㅅ', 'ㄱ'): 'ㅴ', ('ㅂ', 'ㅅ', 'ㄷ'): 'ㅵ', ('ㅂ', 'ㅈ'): 'ㅶ', ('ㅂ', 'ㅌ'): 'ㅷ', ('ㅅ', 'ㄱ'): 'ㅺ', ('ㅅ', 'ㄴ'): 'ㅻ', ('ㅅ', 'ㄷ'): 'ㅼ', ('ㅅ', 'ㅂ'): 'ㅽ', ('ㅅ', 'ㅅ'): 'ㅆ', ('ㅅ', 'ㅈ'): 'ㅾ', ('ㅇ', 'ㅇ'): 'ㆀ', ('ㅈ', 'ㅈ'): 'ㅉ', ('ㅍ', '̥'): 'ㆄ', ('ㅍ', '∘'): 'ㆄ', ('ㅍ', '◦'): 'ㆄ', ('ㅎ', 'ㅎ'): 'ㆅ', ('ㅛ', 'ㅑ'): 'ㆇ', ('ㅛ', 'ㅒ'): 'ㆈ', ('ㅛ', 'ㅣ'): 'ㆉ', ('ㅠ', 'ㅕ'): 'ㆊ', ('ㅠ', 'ㅖ'): 'ㆋ', ('ㅠ', 'ㅣ'): 'ㆌ', ('ㆁ', 'ㅅ'): 'ㆂ', ('ㆁ', 'ㅿ'): 'ㆃ'}

compatjamo = set(finals.keys()) | set(vowels.keys()) | set(initials.keys()) | {"∘", "◦", '̥'}

# KS C 5601 / KS X 1001 EUC-KR Wansung RHS
graphdata.gsets["ir149/ibm"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/ibm-949_P110-1999.ucm"),
    "ibm-949_P110-1999.ucm",
    gbklike=True))
graphdata.gsetflags["ir149/ibm"] |= {"UHC:IS_WANSUNG"}
graphdata.gsets["ir149/1998"] = wansung = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("WHATWG/index-euc-kr.txt"),
    "index-euc-kr.txt", 
    gbklike=True))
graphdata.gsetflags["ir149/1998"] |= {"UHC:IS_WANSUNG"}
# Pre Euro-sign update (also lacking the registered trademark sign)
# Note that the post-Unicode-2.0 UTC mappings are harmonious with MS/HTML5 besides those characters:
graphdata.gsets["ir149"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("UTC/KSC5601.TXT"),
    "KSC5601.TXT",
    gbklike=True))
graphdata.gsetflags["ir149"] |= {"UHC:IS_WANSUNG"}
# Further updated (most recent?) version:
_wansung_temp = parsers.fuse([
            ((None,) * 165) + ((0x327E,),), # South Korean Postal Mark
            wansung[2]], "Wansung_KRPM.json")
graphdata.gsets["ir149/2002"] = (94, 2, _wansung_temp)
graphdata.gsetflags["ir149/2002"] |= {"UHC:IS_WANSUNG"}
graphdata.gsets["ir149/unihan"] = (94, 2, parsers.fuse([
    parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_KSource", "K0"),
    _wansung_temp,
], "Wansung_Updated.json"))
graphdata.gsetflags["ir149/unihan"] |= {"UHC:IS_WANSUNG"}
# Pre-Unicode-2.0 UTC mapping file: uses MS's greedy-zenkaku approach but is otherwise closer to Apple,
#   plus its own ideosyncracies (unifying the Korean interpunct with the Japanese one rather than with the
#   Catalan one, and using U+2236 rather than U+02D0 for the alternative colon)
# Note that we basically have to dispose of its own hangul syllables section since they all correspond to
#   codepoints now used for entirely different purposes (the event which prompted the Stability Policy)
oldunicodeksc = parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/OLD5601.TXT"),
    "OLD5601.TXT")
_wansung_syllables = parsers.fuse([
            (((-1,),) * 1410) + ((None,) * 2350) + (((-1,),) * 5076),
            wansung[2]], "Wansung_SyllablesOnly.json")
_wansung_utcalt = parsers.fuse([_wansung_syllables, oldunicodeksc], "Wansung_AltUTC.json")
graphdata.gsets["ir149/altutc"] = wansung_utcalt = (94, 2, _wansung_utcalt)
graphdata.gsetflags["ir149/altutc"] |= {"UHC:IS_WANSUNG"}

# https://www.unicode.org/irg/docs/n2298r-IICoreChanges.pdf#page=6
_irgn2298feedback_table = {
    0x596C: 0x734E,
    0x6E17: 0x6EF2,
    0x8009: 0x8008,
    0x80C4: 0x5191,
    0x9ED8: 0x9ED9,
}
def irgn2298feedback_convert(pointer, ucs):
    if len(ucs) == 1 and (target := _irgn2298feedback_table.get(ucs[0], None)):
        return (target,)
    return deprecated_cjkci.remove_deprecated_cjkci(pointer, ucs)
graphdata.gsets["ir149/irgn2298feedback"] = (94, 2, parsers.fuse([
    parsers.decode_main_plane_whatwg(
        parsers.parse_file_format("WHATWG/index-euc-kr.txt"),
        "index-euc-kr.txt", 
        gbklike=True,
        mapper=irgn2298feedback_convert),
    _wansung_temp,
], "Wansung_IRGN2298_feedback.json"))
graphdata.gsetflags["ir149/irgn2298feedback"] |= {"UHC:IS_WANSUNG"}

ibm_korea_pua = {0xF843: 0x5580, 0xF844: 0x91B5, 0xF845: 0x7A27, 0xF846: 0x6677, 0xF847: 0x8987, 0xF848: 0x551C, 0xF849: 0x7370, 0xF84A: 0x9B27, 0xF84B: 0x797F, 0xF84C: 0x5BE5, 0xF84D: 0x63D0, 0xF84E: 0x5A46, 0xF84F: 0x6F58, 0xF850: 0x904D, 0xF851: 0x541F, 0xF852: 0x5DFF, 0xF853: 0x6C99, 0xF854: 0x8D07, 0xF855: 0x9E9D, 0xF856: 0x9F5F, 0xF857: 0x5C04, 0xF858: 0x55AE, 0xF859: 0x6D17, 0xF85A: 0x9730, 0xF85B: 0xF909, 0xF85C: 0x5BBF, 0xF85D: 0x96CE, 0xF85E: 0x5BFA, 0xF85F: 0x745F, 0xF860: 0x5C04, 0xF861: 0x5C04, 0xF862: 0x7FA8, 0xF863: 0x540A, 0xF864: 0x5247, 0xF865: 0x6E4C, 0xF866: 0x6578, 0xF867: 0x69CC, 0xF868: 0x677B, 0xF869: 0x8D05, 0xF86A: 0x5E40, 0xF86B: 0x5206, 0xF86C: 0x90AF, 0xF86D: 0x614A, 0xF86E: 0x965C}

def ibmpuamap_korea(pointer, ucs):
    if len(ucs) == 1 and ucs[0] in ibm_korea_pua:
        return (ibm_korea_pua[ucs[0]],)
    return ucs 

# The non-KS 94×94 plane encoded by the old IBM code page 944
graphdata.gsets["oldibmkorea/withcorppua"] = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("Custom/index-oldibmkorea-withcorppua.txt"),
    "index-oldibmkorea-withcorppua.txt",
    plane = 1))
graphdata.gsets["oldibmkorea"] = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("Custom/index-oldibmkorea-withcorppua.txt"),
    "index-oldibmkorea-withcorppua.txt",
    plane = 1,
    mapper = ibmpuamap_korea))
graphdata.gsets["oldibmkorea/excavated"] = (94, 2, parsers.decode_main_plane_whatwg(
    parsers.parse_file_format("Custom/index-oldibmkorea-cleaned.txt"),
    "index-oldibmkorea-cleaned.txt",
    plane = 1))

def ahmap_mk(pointer, ucs):
    return variationhints.ahmap(pointer, ucs, variationhints.applesinglehints_mackorean)

def ahmap_pr(pointer, ucs):
    return variationhints.ahmap(pointer, ucs, variationhints.applesinglehints_mackorean_pragmatic)

def ahmap_nt(pointer, ucs):
    return variationhints.ahmap(pointer, ucs, variationhints.applesinglehints_mackorean_nishikiteki)

# Apple and Elex's (Illekseu's) HangulTalk Wansung version
rawmac2 = parsers.read_untracked(
    "Mac/macWansung21.json",
    "Mac/KOREAN_b02.TXT",
    parsers.decode_main_plane_euc,
    parsers.parse_file_format("Mac/KOREAN_b02.TXT"),
    "KOREAN_b02.TXT",
    gbklike=True)
graphdata.gsets["ir149/mac-unicode2_1"] = (94, 2, rawmac2)
graphdata.gsetflags["ir149/mac-unicode3_2"] |= {"UHC:IS_WANSUNG"}
rawmac = parsers.read_untracked(
    "Mac/macWansung32.json",
    "Mac/KOREAN.TXT",
    parsers.decode_main_plane_euc,
    parsers.parse_file_format("Mac/KOREAN.TXT"),
    "KOREAN.TXT",
    gbklike=True)
graphdata.gsets["ir149/mac-unicode3_2"] = (94, 2, rawmac)
graphdata.gsetflags["ir149/mac-unicode3_2"] |= {"UHC:IS_WANSUNG"}
# No ir149-mac-unicode4_0 (same as ir149-mac-unicode3_2; altcomments only in sidecarriage then?)
macwansungdata = parsers.read_untracked(
    "Mac/macWansung.json",
    "Mac/KOREAN.TXT",
    parsers.decode_main_plane_euc,
    parsers.parse_file_format("Mac/KOREAN.TXT"),
    "KOREAN.TXT",
    gbklike=True,
    mapper=ahmap_mk)
graphdata.gsets["ir149/mac"] = (94, 2, macwansungdata)
graphdata.gsetflags["ir149/mac"] |= {"UHC:IS_WANSUNG"}

# Apple and Elex's (Illekseu's) secondary HangulTalk plane
rawelex21 = parsers.read_untracked(
    "Mac/macElex21.json",
    "Mac/KOREAN_b02.TXT",
    parsers.decode_extra_plane_elex,
    parsers.parse_file_format("Mac/KOREAN_b02.TXT"),
    "KOREAN_b02.TXT")
graphdata.gsets["mac-elex-extras/unicode2_1"] = (94, 2, rawelex21)
rawelex = parsers.read_untracked(
    "Mac/macElex32.json",
    "Mac/KOREAN.TXT",
    parsers.decode_extra_plane_elex,
    parsers.parse_file_format("Mac/KOREAN.TXT"),
    "KOREAN.TXT")
graphdata.gsets["mac-elex-extras/unicode3_2"] = (94, 2, rawelex)
rawelex4 = parsers.read_untracked(
    "Mac/macElex40.json",
    "Mac/KOREAN.TXT",
    parsers.decode_extra_plane_elex,
    parsers.parse_file_format("Mac/KOREAN.TXT", altcomments=True),
    "KOREAN.TXT-altcomments-True")
graphdata.gsets["mac-elex-extras/unicode4_0"] = (94, 2, rawelex4)
macelexdata = parsers.read_untracked(
    "Mac/macElex.json",
    "Mac/KOREAN.TXT",
    parsers.decode_extra_plane_elex,
    parsers.parse_file_format("Mac/KOREAN.TXT"),
    "KOREAN.TXT",
    mapper=ahmap_mk)
graphdata.gsets["mac-elex-extras"] = (94, 2, macelexdata)
macelexdata_nt = parsers.read_untracked(
    "Mac/macElexNT.json",
    "Mac/KOREAN.TXT",
    parsers.decode_extra_plane_elex,
    parsers.parse_file_format("Mac/KOREAN.TXT"),
    "KOREAN.TXT",
    mapper=ahmap_nt)
graphdata.gsets["mac-elex-extras/nishiki-teki"] = (94, 2, macelexdata_nt)
macelexdata_pr = parsers.read_untracked(
    "Mac/macElexPR.json",
    "Mac/KOREAN.TXT",
    parsers.decode_extra_plane_elex,
    parsers.parse_file_format("Mac/KOREAN.TXT"),
    "KOREAN.TXT",
    mapper=ahmap_pr)
graphdata.gsets["~mac-elex-extras/semipragmatic"] = (94, 2, macelexdata_pr)
macelexdata_adobe = parsers.decode_extra_plane_elex(
    parsers.parse_file_format("Adobe/AdobeKorea.txt", cidmap=("KSCpc-EUC", "UniKS-UTF32")),
    "AdobeKorea.txt-KSCpc-EUC-UniKS-UTF32"
)
elex2cid = parsers.decode_extra_plane_elex(
    parsers.parse_file_format("Adobe/AdobeKorea.txt", cidmap=("KSCpc-EUC", "CID")),
    "AdobeKorea.txt-KSCpc-EUC-CID"
)
graphdata.gsets["mac-elex-extras/adobe"] = (94, 2, macelexdata_adobe)

# KPS 9566
graphdata.gsets["ir202/2011"] = kps9566_2011 = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("UTCDocs/AppendixA_KPS9566-2011-to-Unicode.txt"),
    "AppendixA_KPS9566-2011-to-Unicode.txt",
    gbklike=True))
graphdata.gsetflags["ir202/2011"] |= {"UHC:IS_KPS"}
graphdata.gsets["ir202/2003"] = kps9566_2003 = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("UTC/KPS9566.TXT"),
    "KPS9566.TXT",
    gbklike=True))
graphdata.gsetflags["ir202/2003"] |= {"UHC:IS_KPS"}
graphdata.gsetflags["ir202/2003"] |= {"UHC:Y_TREMA"}
_kps_temp = parsers.fuse([
            ((None,) * 175) + ((0x1CC81,),), # Added in Unicode 16.0
            parsers.decode_main_plane_gl(parsers.parse_file_format("Custom/kps-override.txt"), "kps-override.txt"),
            ((None,) * 6400) + ((0x67FF,),), # Correct mapping per UTC L2/21-059 (IRG N2479), differs from deployed.
            kps9566_2011[2], kps9566_2003[2]], "KPS_FullMapping.json")
graphdata.gsets["ir202/full"] = (94, 2, _kps_temp)
graphdata.gsetflags["ir202/full"] |= {"UHC:IS_KPS"}
graphdata.gsetflags["ir202/full"] |= {"UHC:Y_TREMA"}
_kps_temp = parsers.fuse([
            ((None,) * 663) + ((0x212A,),), # Kelvin sign (versus Euro)
            ((None,) * 1080) + ((0x2B97,),), # Category A mark
            ((None,) * 1222) + (((-1,),) * 141), # Remove Latin-1 part
            kps9566_2003[2]], "KPS_1997.json")
graphdata.gsets["ir202"] = (94, 2, _kps_temp)
graphdata.gsetflags["ir202"] |= {"UHC:IS_KPS"}
kpsext = read_kps9566extras("UTCDocs/AppendixA_KPS9566-2011-to-Unicode.txt")
graphdata.gsets["2011kpsextras"] = (94, 2, kpsext + (None,) * (94*94 - len(kpsext)))
# KPS 10721 doesn't appear to be ECMA-35 structured.

# KS X 1002.
ksx1002_hanja = parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_KSource", "K1")
ksx1002_syllables = parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTCDocs/HangulSources.txt", hangulsourcestxt = "1002"),
    "HangulSources.txt-1002")
ksx1002_symbols = parsers.decode_main_plane_gl(parsers.parse_file_format("Custom/ksx1002_1_14.txt"), "ksx1002_1_14.txt")
ksx1002_oldsyllables = parsers.decode_main_plane_gl(parsers.parse_file_format("Custom/ksx1002_37_54.txt"), "ksx1002_37_54.txt")
graphdata.gsets["ksx1002"] = (94, 2, parsers.fuse([ksx1002_symbols, ksx1002_hanja, ksx1002_syllables, ksx1002_oldsyllables], "KSX1002.json"))

# KS X 1027. Part 1 (horizontal extensions) is more or less complete as expected of a set of
#   horizontal extensions, while part 2 (vertical extensions) has a lot of holes (although these
#   "holes" are indeed skipped in at least the most recent few editions of KS X 1027-2 itself).
#   Other parts are not ECMA-35 structured.
ksx1027_1_unihan = parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_KSource", "K2")
ksx1027_1 = parsers.fuse([
            # K2-6557 Unihan source reference removed from U+8FD6 in Unicode 3.1.1 per request
            #   in IRGN0405. KS X 1027-1:2011 and KS X 1027-1:2021 both skip it.
            # As highlighted in IRGN0400, a K-source glyph was never provided for U+8FD6.
            # https://www.unicode.org/irg/docs/n0400-ErrorReportHQPv1.pdf
            # https://www.unicode.org/irg/docs/n0405-IRGN400Feedback.txt
            ((None,) * 6446) + ((0x8FD6,),),
            ksx1027_1_unihan], "KSX1027-1.json")
graphdata.gsets["ksx1027_1"] = (94, 2, ksx1027_1)
ksx1027_2_hanja = parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_KSource", "K3")
graphdata.gsets["ksx1027_2"] = (94, 2, ksx1027_2_hanja)

# Amounting to the entirety of the UHC extensions, in order:
non_wangsung_johab = [i for i in range(0xAC00, 0xD7A4) 
                        if i not in graphdata.codepoint_coverages["ir149"]]

# Similarly for the KPS encoding:
def _sort_by_kps(syll):
    deco = namedata.canonical_decomp[chr(syll)]
    if len(deco) == 2:
        init, vow = deco
        fin = ""
    else:
        init, vow, fin = deco
    return (i_order[init], v_order[vow], f_order[fin])
i_order = tuple(initials[_i] for _i in "ㄱㄴㄷㄹㅁㅂㅅㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉㅇ")
i_order = dict((_i, i_order.index(_i)) for _i in i_order)
v_order = tuple(vowels[_i] for _i in "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖㅚㅟㅢㅘㅝㅙㅞ")
v_order = dict((_i, v_order.index(_i)) for _i in v_order)
f_order = tuple(finals[_i] for _i in "ㄱㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅇㅈㅊㅋㅌㅍㅎㄲㅆ")
f_order = dict((_i, f_order.index(_i) + 1) for _i in f_order)
f_order[""] = 0
non_kps9566_johab = [i for i in range(0xAC00, 0xD7A4) 
                       if i not in graphdata.codepoint_coverages["ir202"]]
non_kps9566_johab.sort(key = _sort_by_kps)

graphdata.gsets["johab/ibmkorea"] = (190, 2, parsers.decode_main_plane_dbebcdic(parsers.parse_file_format("ICU/ibm-933_P110-1995.ucm"), "ibm-933_P110-1995.ucm", mapper = ibmpuamap_korea))
graphdata.ebcdicdbcs["834"] = graphdata.ebcdicdbcs["933"] = graphdata.ebcdicdbcs["5029"] = "johab/ibmkorea"
graphdata.chcpdocs["834"] = graphdata.chcpdocs["933"] = graphdata.chcpdocs["5029"] = "ebcdic"
graphdata.defgsets["933"] = ("alt646/ibmkorea", "gr833", "gl310", "gr310")
graphdata.defgsets["5029"] = ("alt646/ibmkorea", "gr4929", "gl310", "gr310")

graphdata.gsets["johab/ibmkorea/full"] = (190, 2, parsers.decode_main_plane_dbebcdic(parsers.parse_file_format("ICU/ibm-1364_P110-2007.ucm"), "ibm-1364_P110-2007.ucm", mapper = ibmpuamap_korea))
graphdata.ebcdicdbcs["1364"] = graphdata.ebcdicdbcs["4930"] = "johab/ibmkorea/full"
graphdata.chcpdocs["1364"] = graphdata.chcpdocs["4930"] = "ebcdic"
graphdata.defgsets["1364"] = ("alt646/ibmkorea", "gr833", "gl310", "gr310")



