#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Korea (both South and North)

import os, json, shutil
import unicodedata as ucd
from ecma35.data import graphdata, variationhints
from ecma35.data.multibyte import mbmapparsers as parsers

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

def read_elexextras(fil, *, altcomments=False, mapper=parsers.identitymap):
    if mapper is parsers.identitymap:
        mappername = ""
    elif mapper.__name__ != "<lambda>":
        mappername = "_" + mapper.__name__
    else:
        mappername = "_FIXME"
    #
    if altcomments:
        mappername += "_altcomments"
    cachefn = os.path.join(parsers.cachedirectory, os.path.splitext(fil)[0].replace("/", "---") 
              + "_elexextras" + mappername + ".json")
    if os.path.exists(cachefn):
        return parsers.LazyJSON(cachefn)
    for _i in open(os.path.join(parsers.directory, fil), "r", encoding="utf-8"):
        if (not _i.strip()) or _i[0] == "#":
            continue
        #
        if altcomments and ("# or for Unicode 4.0," in _i):
            byts, ucs = _i.split("# or for Unicode 4.0,", 1)
            byts = byts.split("\t", 1)[0]
            ucs = ucs.lstrip().split(None, 1)[0].rstrip(",")
        elif altcomments and ("# or" in _i):
            byts, ucs = _i.split("# or", 1)
            byts = byts.split("\t", 1)[0]
            ucs = ucs.lstrip().split(None, 1)[0].rstrip(",")
        else:
            byts, ucs = _i.split("\t", 2)[:2]
        #
        if len(byts) >= 6:
            lead = int(byts[2:4], 16)
            trail = int(byts[4:6], 16)
            if trail >= 0xA1:
                continue
            first = lead - 0xA1
            if trail >= 0x81:
                last = trail - 0x41 - 3
            else:
                last = trail - 0x41
            newpointer = (94 * first) + last
        else:
            continue
        #
        iucs = mapper(newpointer, tuple(int(j, 16) for j in ucs.replace("0x", "").split("+")))
        if len(_temp) > newpointer:
            assert _temp[newpointer] is None, (newpointer, iucs, _temp[newpointer])
            _temp[newpointer] = iucs
        else:
            while len(_temp) < newpointer:
                _temp.append(None)
            _temp.append(iucs)
    # Try to end it on a natural plane boundary.
    _temp.extend([None] * (((94 * 94) - (len(_temp) % (94 * 94))) % (94 * 94)))
    if not _temp:
        _temp.extend([None] * (94 * 94)) # Don't just return an empty tuple.
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    # Write output cache.
    f = open(cachefn, "w")
    f.write(json.dumps(r))
    f.close()
    return r

initials = {'\u3131': '\u1100', '\u3132': '\u1101', '\u3134': '\u1102', '\u3137': '\u1103', '\u3138': '\u1104', '\u3139': '\u1105', '\u3141': '\u1106', '\u3142': '\u1107', '\u3143': '\u1108', '\u3145': '\u1109', '\u3146': '\u110a', '\u3147': '\u110b', '\u3148': '\u110c', '\u3149': '\u110d', '\u314a': '\u110e', '\u314b': '\u110f', '\u314c': '\u1110', '\u314d': '\u1111', '\u314e': '\u1112', '\u3165': '\u1114', '\u3166': '\u1115', '\u3167': '\u115b', '\u316a': '\ua966', '\u316e': '\u111c', '\u316f': '\ua971', '\u3171': '\u111d', '\u3172': '\u111e', '\u3173': '\u1120', '\u3174': '\u1122', '\u3175': '\u1123', '\u3176': '\u1127', '\u3177': '\u1129', '\u3178': '\u112b', '\u3179': '\u112c', '\u317a': '\u112d', '\u317b': '\u112e', '\u317c': '\u112f', '\u317d': '\u1132', '\u317e': '\u1136', '\u317f': '\u1140', '\u3180': '\u1147', '\u3181': '\u114c', '\u3184': '\u1157', '\u3185': '\u1158', '\u3186': '\u1159', '\u3164': '\u115f'}

vowels = {'\u314f': '\u1161', '\u3150': '\u1162', '\u3151': '\u1163', '\u3152': '\u1164', '\u3153': '\u1165', '\u3154': '\u1166', '\u3155': '\u1167', '\u3156': '\u1168', '\u3157': '\u1169', '\u3158': '\u116a', '\u3159': '\u116b', '\u315a': '\u116c', '\u315b': '\u116d', '\u315c': '\u116e', '\u315d': '\u116f', '\u315e': '\u1170', '\u315f': '\u1171', '\u3160': '\u1172', '\u3161': '\u1173', '\u3162': '\u1174', '\u3163': '\u1175', '\u3187': '\u1184', '\u3188': '\u1185', '\u3189': '\u1188', '\u318a': '\u1191', '\u318b': '\u1192', '\u318c': '\u1194', '\u318d': '\u119e', '\u318e': '\u11a1', '\u3164': '\u1160'}

finals = {'\u3132': '\u11a9', '\u3133': '\u11aa', '\u3135': '\u11ac', '\u3136': '\u11ad', '\u313c': '\u11b2', '\u313d': '\u11b3', '\u313e': '\u11b4', '\u313f': '\u11b5', '\u3140': '\u11b6', '\u314b': '\u11bf', '\u3137': '\u11ae', '\u313a': '\u11b0', '\u313b': '\u11b1', '\u3144': '\u11b9', '\u3148': '\u11bd', '\u314a': '\u11be', '\u314c': '\u11c0', '\u314d': '\u11c1', '\u314e': '\u11c2', '\u3141': '\u11b7', '\u3142': '\u11b8', '\u3146': '\u11bb', '\u3131': '\u11a8', '\u3145': '\u11ba', '\u3147': '\u11bc', '\u3134': '\u11ab', '\u3139': '\u11af', '\u3165': '\u11ff', '\u3166': '\u11c6', '\u3167': '\u11c7', '\u3168': '\u11c8', '\u3169': '\u11cc', '\u316a': '\u11ce', '\u316b': '\u11d3', '\u316c': '\u11d7', '\u316d': '\u11d9', '\u316e': '\u11dc', '\u316f': '\u11dd', '\u3170': '\u11df', '\u3171': '\u11e2', '\u3173': '\ud7e3', '\u3175': '\ud7e7', '\u3176': '\ud7e8', '\u3178': '\u11e6', '\u317a': '\u11e7', '\u317c': '\u11e8', '\u317d': '\u11ea', '\u317e': '\ud7ef', '\u317f': '\u11eb', '\u3180': '\u11ee', '\u3181': '\u11f0', '\u3182': '\u11f1', '\u3183': '\u11f2', '\u3184': '\u11f4', '\u3186': '\u11f9', '\u3164': ''}

compjamo = set(finals.keys()) | set(vowels.keys()) | set(initials.keys())

# KS C 5601 / KS X 1001 EUC-KR Wansung RHS
graphdata.gsets["ir149-1998"] = wansung = (94, 2, parsers.read_main_plane("WHATWG/index-euc-kr.txt", euckrlike=True))
graphdata.gsetflags["ir149-1998"] |= {"UHC:IS_WANSUNG"}
# Pre Euro-sign update (also lacking the registered trademark sign)
# Note that the post-Unicode-2.0 UTC mappings are harmonious with MS/HTML5 besides those characters:
graphdata.gsets["ir149"] = wansung87 = (94, 2, parsers.read_main_plane("UTC/KSC5601.TXT", euckrlike=True))
graphdata.gsetflags["ir149"] |= {"UHC:IS_WANSUNG"}
# Further updated (most recent?) version:
_wansung_temp = parsers.fuse([
            ((None,) * 165) + ((0x327E,),), # South Korean Postal Mark
            wansung[2]], "Wansung_KRPM.json")
graphdata.gsets["ir149-2002"] = wansung02 = (94, 2, _wansung_temp)
graphdata.gsetflags["ir149-2002"] |= {"UHC:IS_WANSUNG"}
# Pre-Unicode-2.0 UTC mapping file: uses MS's greedy-zenkaku approach but is otherwise closer to Apple,
#   plus its own ideosyncracies (unifying the Korean interpunct with the Japanese one rather than with the
#   Catalan one, and using U+2236 rather than U+02D0 for the alternative colon)
# Note that we basically have to dispose of its own hangul syllables section since they all correspond to
#   codepoints now used for entirely different purposes (the event which prompted the Stability Policy)
oldunicodeksc = parsers.read_main_plane("UTC/OLD5601.TXT")
_wansung_syllables = parsers.fuse([
            (((-1,),) * 1410) + ((None,) * 2350) + (((-1,),) * 5076),
            wansung[2]], "Wansung_SyllablesOnly.json")
_wansung_temp = parsers.fuse([_wansung_syllables, oldunicodeksc], "Wansung_AltUTC.json")
graphdata.gsets["ir149-altutc"] = wansung_utcalt = (94, 2, _wansung_temp)
graphdata.gsetflags["ir149-altutc"] |= {"UHC:IS_WANSUNG"}

# Apple and Elex's (Illekseu's) Wansung version, and its secondary plane (collectively HangulTalk)
macwansungdata = parsers.read_untracked_mbfile(
                 parsers.read_main_plane, "Mac/KOREAN.TXT", "Mac---KOREAN_mainplane_ahmap.json", 
                 "Mac/macWansung.json", euckrlike=True, mapper=variationhints.ahmap)
macelexdata =    parsers.read_untracked_mbfile(
                 read_elexextras, "Mac/KOREAN.TXT", "Mac---KOREAN_elexextras_ahmap.json", 
                 "Mac/macElex.json", mapper=variationhints.ahmap)
rawmac =         parsers.read_untracked_mbfile(
                 parsers.read_main_plane, "Mac/KOREAN.TXT", "Mac---KOREAN_mainplane.json", 
                 "Mac/macWansung-raw.json", euckrlike=True)
rawelex =        parsers.read_untracked_mbfile(
                 read_elexextras, "Mac/KOREAN.TXT", "Mac---KOREAN_elexextras.json", 
                 "Mac/macElex-raw.json")
rawmac4 =        parsers.read_untracked_mbfile(
                 parsers.read_main_plane, "Mac/KOREAN.TXT", "Mac---KOREAN_mainplane_altcomments.json", 
                 "Mac/macWansung4.json", euckrlike=True, altcomments=True)
rawelex4 =       parsers.read_untracked_mbfile(
                 read_elexextras, "Mac/KOREAN.TXT", "Mac---KOREAN_elexextras_altcomments.json", 
                 "Mac/macElex4.json", altcomments=True)
macwansung = graphdata.gsets["ir149-mac"] = (94, 2, macwansungdata)
graphdata.gsetflags["ir149-mac"] |= {"UHC:IS_WANSUNG"}
macelexextras = graphdata.gsets["mac-elex-extras"] = (94, 2, macelexdata)
macelexextras32 = graphdata.gsets["mac-elex-extras-unicode3_2"] = (94, 2, rawelex)
macelexextras40 = graphdata.gsets["mac-elex-extras-unicode4_0"] = (94, 2, rawelex4)

# KPS 9566
graphdata.gsets["ir202-2011"] = kps9566_2011 = (94, 2, parsers.read_main_plane("Other/AppendixA_KPS9566-2011-to-Unicode.txt", euckrlike=True))
graphdata.gsetflags["ir202-2011"] |= {"UHC:IS_KPS"}
graphdata.gsets["ir202-2003"] = kps9566_2003 = (94, 2, parsers.read_main_plane("UTC/KPS9566.TXT", euckrlike=True))
graphdata.gsetflags["ir202-2003"] |= {"UHC:IS_KPS"}
graphdata.gsetflags["ir202-2003"] |= {"UHC:Y_TREMA"}
_kps_temp = parsers.fuse([
            ((None,) * 1080) + ((0x2B97,),), # Finally exists in Unicode.
            kps9566_2011[2], kps9566_2003[2]], "KPS_2011and2003_PM.json")
graphdata.gsets["ir202-full"] = (94, 2, _kps_temp)
graphdata.gsetflags["ir202-full"] |= {"UHC:IS_KPS"}
graphdata.gsetflags["ir202-full"] |= {"UHC:Y_TREMA"}
_kps_temp = parsers.fuse([
            ((None,) * 663) + ((0x212A,),), # Kelvin sign (versus Euro)
            ((None,) * 416) + ((0x2B97,),), # Category A mark
            ((None,) * 141) + (((-1,),) * 141), # Remove Latin-1 part
            kps9566_2003[2]], "KPS_1997.json")
graphdata.gsets["ir202"] = kps9566_1997 = (94, 2, _kps_temp)
graphdata.gsetflags["ir202"] |= {"UHC:IS_KPS"}
graphdata.gsets["2011kpsextras"] = (94, 2, read_kps9566extras("Other/AppendixA_KPS9566-2011-to-Unicode.txt"))
# KPS 10721 doesn't appear to be ECMA-35 structured.

# KS X 1002. I can't find charts, leave alone mappings, which aren't restricted to hanja.
graphdata.gsets["ksx1002-hanja"] = (94, 2, parsers.read_unihan_source("UCD/Unihan_IRGSources.txt", "K", "K1"))

# KS X 1027. Part 1 seems complete, part 2 has a lot of holes. Other parts are not ECMA-35 structured.
graphdata.gsets["ksx1027_1"] = (94, 2, parsers.read_unihan_source("UCD/Unihan_IRGSources.txt", "K", "K2"))
graphdata.gsets["ksx1027_2"] = (94, 2, parsers.read_unihan_source("UCD/Unihan_IRGSources.txt", "K", "K3"))

# Amounting to the entirety of the UHC extensions, in order:
non_wangsung_johab = [i for i in range(0xAC00, 0xD7A4) 
                        if i not in graphdata.codepoint_coverages["ir149"]]

# Similarly for the KPS encoding:
def _sort_by_kps(syll):
    deco = ucd.normalize("NFD", chr(syll))
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



