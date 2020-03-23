#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, ast, sys, json, pprint
from ecma35.data import graphdata
from ecma35.data.multibyte import mbmapparsers as parsers

# CNS 11643 and Big 5 (not gb12345; see guobiao.py for that one).
# Bumpy ride here, so brace yourselves.

# Punctuation (gov.tw mappings first, then ICU mappings):
#   01-01-23 U+2015 (―)　U+2014 (—)　 -- m-dash vs horiz-bar; tale as old as time for legacy CJK.
#   01-01-25 U+2014 (—)  U+FE58 (﹘)　-- U+FE58 is "small em dash"
#   01-02-36 U+FF5E (～)　U+223C (∼)  -- Fullwidth tilde, tilde operator(, wave dash); old as time.
#   01-02-55 U+2190 (←)  U+2192 (→)  -- odd (ICU, Yasuoka AND ISO-IR-171 agree contra gov.tw)
#   01-02-56 U+2192 (→)  U+2190 (←)  -- odd (ICU, Yasuoka AND ISO-IR-171 agree contra gov.tw)
#     Note: the gov.tw mappings swapping the left and right arrows does regularise the non-kanji
#     mappings between Big5 and CNS 11643 (making EUC-TW a2d6, a2d7, a2d8, a2d9 represent Big5
#     a1f5, a1f6, a1f7, a1f8 rather than a1f5, a1f7, a1f6, a1f8; see appendix A.1 of RFC 1922 for
#     the range map, noting how it makes an explicit exception for those two points).
# Other gov.tw versus Yasuoka from that range (excluding mere use of hankaku counterparts):
#   01-01-06 U+2027 (‧) U+00B7 (·)  -- U+2027 is "hyphenation point"; U+00B7 is from Latin-1
#   01-01-29 U+FE4F (﹏) U+FE4B (﹋)
#   01-01-78 U+FF0A (＊) U+2733 (✳) 　-- U+2733 is "eight spoked asterisk"
#   01-02-06 U+02CD (ˍ) U+005F (_)   -- U+02CD is "modifier letter low macron"
#   01-02-36 U+FF5E (～) U+301C (〜)  -- The "(, wave dash)" mentioned above, just as expected
#   01-02-61 U+2225 (∥) U+2016 (‖) 　-- Parallel versus double vertical bar; old as time.
#   01-02-62 U+2223 (∣) U+007C (|) 　-- "Divides" versus the vertical bar.
#   01-02-63 U+FF0F (／) U+2044 (⁄)   -- Slash versus fraction slash (apparently).
#   01-02-65 U+2215 (∕) U+002F (/) 　-- Division slash versus slash.
# Being as gov.tw and ICU agree for the following, I presume Yasuoka has it mistaken:
#   01-06-04 U+2463 (④) U+2464 (⑤)
#   01-06-05 U+2464 (⑤) U+2465 (⑥)
#   01-06-06 U+2465 (⑥) U+2466 (⑦)
#   01-06-07 U+2466 (⑦) U+2467 (⑧)
#   01-06-08 U+2467 (⑧) U+2468 (⑨)
#   01-06-09 U+2468 (⑨) U+2469 (⑩)
#   01-06-10 U+2469 (⑩) U+246A (⑪)
# No idea (gov.tw mappings first, then ICU mappings):
#   01-05-84 U+312D (ㄭ)  U+E000 (PUA)
#   01-05-85 None      　 U+E001 (PUA)
# Strokes (gov.tw mappings first, then ICU mappings):
#   01-06-48 U+31D0 (㇐) None
#   01-06-50 U+31D1 (㇑) None
#   01-06-51 U+31D2 (㇒) None
#   01-06-52 U+31D3 (㇓) None
#   01-06-53 U+31D4 (㇔) None
#   01-06-55 U+31CF (㇏) None
#   01-06-56 U+31C0 (㇀) None
#   01-06-57 U+31D5 (㇕) None
#   01-06-58 U+31D6 (㇖) None
#   01-06-59 U+31C7 (㇇) None
#   01-06-60 U+31D7 (㇗) None
#   01-06-61 U+31C4 (㇄) None
#   01-06-62 U+31D8 (㇘) None
#   01-06-63 U+31D9 (㇙) None
#   01-06-64 U+31DA (㇚) None
#   01-06-65 U+31C3 (㇃) None
#   01-06-66 U+31C2 (㇂) None
#   01-06-67 U+31C1 (㇁) None
#   01-06-68 U+31DB (㇛) None
#   01-06-70 U+31DC (㇜) None
#   01-06-71 U+31DD (㇝) None
#   01-06-72 U+31C5 (㇅) None
#   01-06-73 U+31CD (㇍) None
#   01-06-74 U+31C6 (㇆) None
#   01-06-75 U+31C8 (㇈) None
#   01-06-76 U+31DE (㇞) None
#   01-06-78 U+31DF (㇟) None
#   01-06-79 U+31CE (㇎) None
#   01-06-80 U+31E0 (㇠) None
#   01-06-81 U+31C9 (㇉) None
#   01-06-82 U+31E1 (㇡) None
# Radicals (gov.tw mappings first, then ICU mappings):
#   01-06-94 None      　U+2F21 (⼡) -- extension rad 34; CNS does not consider rads 34/35 distinct
#   01-07-44 U+2F2C (⼬) U+5C6E (屮)
#   01-08-39 U+2F85 (⾅) U+81FC (臼)
#   01-08-45 U+2F8B (⾋) U+8278 (艸)
# Yasuoka consistently maps these radicals to their main kanji codepoints; I shan't list them all.
# From this point… Yasuoka makes extensive use of many-to-one mappings for best-fit itaiji in the
#   basic multilingual plane (being authored in 1998, the SIP presumably didn't exist yet?). I've
#   only bothered noting these where the gov.tw mappings are to SPUA, i.e. the fit is still "best".
# Plane 4 kanji (gov.tw mappings first, then ICU mappings)
#   04-02-59 U+FFF7A (SPUA)　 U+5B90 (宐) -- compare 04-06-05
#     Note: U+FFF7A has the middle part looking like two interlocking counterrotated Ls.
#   04-03-65 U+FFFFD (SPUA)　 U+5759 (坙) -- seems like a legit duplicate (compare FE 03-68-63).
#   04-04-76 U+2634B (𦍋)     U+8288 (芈)
#   04-06-05  U+5B90 (宐)    None       　-- compare 04-02-59
#   04-06-25 U+221F7 (𢇷)     U+5E9F (废)
#   04-07-74 U+FFFFC (SPUA)　 U+80BB (肻) -- compare FE 03-70-17.
#     Note: U+FFFFC has the lines within the meat radical drawn at angles.
#   04-08-07 U+FFFFB (SPUA)　 U+488C (䢌) -- compare 15-08-82
#     Note: U+FFFFB has the zig-zaggy style of the walking radical, like in handwriting.
#     Can I just ask who the hell thought that deserved its own CNS codepoint?
#   04-08-93 U+FFFFA (SPUA)　 U+5CD5 (峕) -- seems like a legit duplicate (compare FE 03-68-77).
#   04-10-78 U+FFFF9 (SPUA)　 U+79CC (秌) -- compare FE 03-69-44.
#     Note: Seemingly supposed to be a difference in the left dot direction on the fire radical?
#     Tellingly, the text editor font I'm using renders U+79CC like TW Sung renders U+FFFF9.
#     Also tellingly, U+79CC+E0100 using Adobe IVD sequences seems to do the opposite?
#   04-16-34 U+FFFF8 (SPUA)　 U+98E4 (飤) -- compare FE 03-70-80
#     Note: U+FFFF8 has the dot in the top part of the left radical drawn horizontally.
#   04-24-60 U+FFFF7 (SPUA)　 U+6E7C (湼) -- compare FE 03-69-34.
#     Note: U+FFFF7 uses a straight diagonal for the bottom stroke of the water radical.
#     In my text editor font, U+6E7C does that anyway.
#   04-25-38  U+FAD4 (䀹)     U+4039 (䀹)
#   04-34-90 U+21C09 (𡰉)     U+5C32 (尲)
#   04-36-56 U+FFFF6 (SPUA)　 U+7193 (熓) -- compare FE 03-69-59.
#     Similar to U+FFFF9, although this time the text editor font I'm using renders U+7193
#     differently to TW Sung's U+FFFF6. Still an odd quibble.
#   04-51-28 U+FFF7B (SPUA)　 U+8786 (螆) -- compare 15-49-93
#   04-67-25 U+FFFF5 (SPUA)　 U+5E71 (幱) -- compare FE 03-70-87.
#   04-72-47 U+2FA16 (䵖)     U+4D56 (䵖) -- compare 05-79-52
#   05-79-52  U+4D56 (䵖)    U+2FA16 (䵖) -- compare 04-72-47
#   05-90-24  U+4695 (䚕)    U+2F9CB (𧢮)
# Plane 5 kanji (gov.tw mapping first, then Yasuoka mapping):
#   05-03-43 U+FFFF3 (SPUA) U+5324 (匤)
# Plane 6 kanji (gov.tw mapping first, then Yasuoka mapping):
#   06-10-01 U+FFFF1 (SPUA) U+5365 (卥)
#   06-60-15 U+FFFF0 (SPUA) U+5900 (夀)
# Plane 7 kanji (gov.tw mapping first, then Yasuoka mapping):
#   07-33-57 U+FFFEF (SPUA) U+7E64 (繤)
# Plane 15 kanji (gov.tw mappings first, then ICU mappings):
#   15-03-23 None       　U+2F81F (㓟)
#   15-08-82  U+488C (䢌) None       　-- compare 04-08-07
#   15-13-72 None       　U+2F807 (倂)
#   15-16-59 None       　U+2F906 (𣴞)
#   15-27-74  U+692C (椬) None
#   15-28-30  U+6BF6 (毶) None       　-- compare FE 03-69-26 ("14"-69-26; see below) in UTC mapping
#   15-28-69  U+713F (焿) None
#   15-48-22  U+71B4 (熴) None
#   15-49-93  U+8786 (螆) U+2F9BE (螆) -- compare 04-51-28
#   15-67-66 None       　U+27068 (𧁨) -- also in cns-11643-1992.ucm; compare 15-67-74
#   15-67-74 U+27068 (𧁨) None       　-- compare 15-67-66
#   15-69-57  U+7922 (礢) None

# ISO 10646:2017 Annex P says:
# - U+20885: mistakenly unified with T5-3669
# - U+22936: mistakenly unified with T5-6777
# - U+23023: mistakenly unified with T5-6C34
# - U+23EE4: mistakenly unified with T7-243F
# - U+243BE: T7-2F4B mapping, but should have been unified with U+24381
# - U+28321: mistakenly unified with T6-632A

_contraspua = {
    # Alternative mappings per Yasuoka/ICU for some of the ones that otherwise get mapped to SPUA.
    # On the basis that PUA mappings for defined characters are kinda a last resort… since there's
    #   no guarantee it'll show up even legibly (and you can forget about aural rendering).
    (0xFFF7A,): (0x5B90,),
    (0xFFF7B,): (0x8786,),
    (0xFFFEF,): (0x7E64,),
    (0xFFFF0,): (0x5900,),
    (0xFFFF1,): (0x5365,),
    (0xFFFF3,): (0x5324,),
    (0xFFFF5,): (0x5E71,),
    (0xFFFF6,): (0x7193,),
    (0xFFFF7,): (0x6E7C,),
    (0xFFFF8,): (0x98E4,),
    (0xFFFF9,): (0x79CC,),
    (0xFFFFA,): (0x5CD5,),
    (0xFFFFB,): (0x488C,),
    (0xFFFFC,): (0x80BB,),
    (0xFFFFD,): (0x5759,),
    # The Gov-TW mappings seem to insist on SPUA assignments for Roman characters which
    # Unicode represents as combining sequences.
    (0xF91D1,): (0x6D, 0x0302),
    (0xF91D2,): (0x6E, 0x0302),
    (0xF91D3,): (0x6D, 0x030C),
    (0xF91D4,): (0x6D, 0x0304),
    (0xF91D5,): (0x6E, 0x0304),
    (0xF91D6,): (0x6D, 0x030D),
    (0xF91D7,): (0x6E, 0x030D),
    (0xF91D8,): (0x61, 0x030D),
    (0xF91D9,): (0x69, 0x030D),
    (0xF91DA,): (0x75, 0x030D),
    (0xF91DB,): (0x65, 0x030D),
    (0xF91DC,): (0x6F, 0x030D),
    (0xF91DD,): (0x6D, 0x030B),
    (0xF91DE,): (0x6E, 0x030B),
    (0xF91DF,): (0x61, 0x030B),
    (0xF91E0,): (0x69, 0x030B),
    (0xF91F7,): (0x65, 0x030B),
}
def cnsmapper_contraspua(pointer, ucs):
    return _contraspua.get(ucs, ucs)

# Since the gov.tw data disagrees with literally every other source I have on the matter
# (ISO-IR-171, UTC mappings, ICU mappings, Yasuoka's mappings…; although not without
# reason, see comments about the Big5 order above), change it to match.
def cnsmapper_swaparrows(pointer, ucs):
    if (pointer == 148) and (ucs == (0x2190,)):
        return (0x2192,)
    elif (pointer == 149) and (ucs == (0x2192,)):
        return (0x2190,)
    return ucs

planesize = 94 * 94
cns_bmp = parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt",
        mapper = cnsmapper_swaparrows)
cns_sip = parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt")
cns_spuaa = parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt",
        mapper = cnsmapper_contraspua)
cns = parsers.fuse([cns_bmp, cns_sip, cns_spuaa], "GOV-TW---CNS2UNICODE_swaparrows_contraspua.json")

# Planes present in the original 1986 edition of CNS 11643.
# Closely related to Big5. ISO-IR numbers in the 170s (whereas the 1992 additions are in the 180s).
# ir171 was mostly kept the same until 2007, then extended a bit, due to being the non-kanji plane.
graphdata.gsets["ir171"] = cns1 = (94, 2, cns[planesize * 0 : planesize * 1])
graphdata.gsets["ir171-1986"] = euctw_g2_ibm = (94, 3,
        parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=1))
graphdata.gsets["ir172"] = cns2 = (94, 2, cns[planesize * 1 : planesize * 2])

# ISO-IR-183 deserves particular mention.
# It was first published in 1988, containing 6319 characters, as an extension to CNS 11643
#   occupying plane 14. The main block within that plane, being the first 6148 characters,
#   became plane 3 in 1992, with the rest distributed throughout plane 4 (this is what the
#   ISO-IR registrations themselves are based on).
# The version of CNS 11643 submitted to the IRG, and therefore represented by the Consortium
#   mappings, is actually the 1986 version, plus the IR-183 plane as plane 14, plus additions
#   to the end of the IR-183 plane (meaning it contains more than even the 1988 version)
#   representing other desired characters.
# In 2007, 128 characters were added to plane 3, mostly corresponding to and at the same
#   locations as those added to the IRG submission's plane 14 (comparing the mappings, and
#   insofar as CNS11643.TXT has a lot more gaps for some reason, the only difference seems to
#   be the current 毵 versus the CNS11643.TXT 毶 at 69-26). Note that an unrelated plane 14
#   was added in 2007.
graphdata.gsets["ir183"] = cns3 = (94, 2, cns[planesize * 2 : planesize * 3])
_ir183oldirg = parsers.read_main_plane("UTC/CNS11643.TXT", plane=14)
_ir183fullalt = parsers.fuse([_ir183oldirg, cns3[2]], "ir183fullalt.json")
_ir183full = parsers.fuse([cns3[2], _ir183oldirg], "ir183full.json")
graphdata.gsets["ir183-1988"] = cns3_1988 = (94, 2, tuple(_ir183fullalt)[:6319])
graphdata.gsets["ir183-1988plus"] = cns3plus = (94, 2, tuple(_ir183fullalt))
graphdata.gsets["ir183-1992"] = cns3_1988 = (94, 2, tuple(_ir183full)[:6148])
graphdata.gsets["ir183-full"] = cns3_1988 = (94, 2, tuple(_ir183full))

graphdata.gsets["ir184"] = cns4 = (94, 2, cns[planesize * 3 : planesize * 4])
graphdata.gsets["ir185"] = cns5 = (94, 2, cns[planesize * 4 : planesize * 5])
graphdata.gsets["ir186"] = cns6 = (94, 2, cns[planesize * 5 : planesize * 6])
graphdata.gsets["ir187"] = cns7 = (94, 2, cns[planesize * 6 : planesize * 7])
# Plane 7 is the last one to be registered with ISO-IR.

# The entirety does also exist as an unregistered 94^n set, used by EUC-TW:
graphdata.gsets["cns-eucg2"] = euctw_g2 = (94, 3, cns)
# The version of EUC-TW used by ICU, with standard assignments in planes 1-7 and 15,
#   a user-defined area in plane 12, and IBM corporate assignments in plane 13.
#   Note that this is incompatible with the current standard's use of planes 12 and 13.
# Special mention is warrented for plane 15: it was published as an extension in 1990,
#   but was only integrated into the standard proper in 2007, by which point several
#   assignments were redundant and were skipped. Actually, the early full versions of
#   cns-11643-1992.ucm include it as plane 9 for some reason (later versions remove
#   it due to limiting that mapping's scope to ISO-2022-CN-EXT, then to ISO-2022-CN).
graphdata.gsets["cns-eucg2-ibm"] = euctw_g2_ibm = (94, 3,
        parsers.read_main_plane("ICU/euc-tw-2014.ucm"))

# # # # # # # # # #
# Big Five

# Origin is at 0x8140. Trail bytes are 0x40-0x7E (63) and 0xA1-0xFE (94) fairly seamlessly.
hkscs_start = 942
special_start = 5024
kanji1_start = 5495
corporate1_start = 10896
kanji2_start = 11304
corporate2_start = 18956

_temp = []
def read_big5extras(fil):
    cachefn = os.path.join(parsers.cachedirectory,
              os.path.splitext(fil)[0].replace("/", "---") + "_big5extras.json")
    if os.path.exists(cachefn):
        # Cache output since otherwise several seconds are spend in here upon importing graphdata
        f = open(cachefn, "r")
        r = json.load(f)
        f.close()
        return tuple(tuple(i) if i is not None else None for i in r)
    for _i in open(os.path.join(parsers.directory, fil), "r"):
        if (not _i.strip()) or _i[0] == "#":
            continue
        byts, ucs = _i.split("\t", 2)[:2]
        if not byts.startswith("0x"):
            extpointer = int(byts.strip(), 10)
        elif len(byts) >= 6:
            lead = int(byts[2:4], 16)
            trail = int(byts[4:6], 16)
            first = lead - 0x81
            last = (trail - 0xA1 + 63) if trail >= 0xA1 else (trail - 0x40)
            extpointer = (157 * first) + last
        else:
            continue
        #
        if extpointer >= corporate2_start:
            newextpointer = extpointer
            # Subtract a whole number of rows, but "empty" space at the start is fine.
            newextpointer -= ((corporate2_start - kanji2_start) // 157) * 157
            newextpointer -= ((corporate1_start - special_start) // 157) * 157
        elif extpointer >= kanji2_start:
            continue
        elif extpointer >= corporate1_start:
            newextpointer = extpointer
            newextpointer -= ((corporate1_start - special_start) // 157) * 157
        elif extpointer >= special_start:
            continue
        else:
            newextpointer = extpointer
        pseudoku = (newextpointer // 157) + 1
        pseudoten = (newextpointer % 157) + 1
        if pseudoten <= 63:
            ku = (pseudoku * 2) - 1
            ten = (pseudoten - 63) + 94
        else:
            ku = pseudoku * 2
            ten = pseudoten - 63
        newpointer = ((ku - 1) * 94) + (ten - 1)
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

def read_big5_rangemap(fil, appendix, *, plane=None):
    # For RFC 1922
    mapping = {}
    reading = False
    for _i in open(os.path.join(parsers.directory, fil), "r"):
        if _i.startswith("A.{:d}.  ".format(appendix)) and not reading:
            reading = True
        elif _i.startswith("A.") and reading:
            return mapping
        elif reading and "<->" in _i:
            frm, to = _i.split("(", 1)[0].split("#", 1)[0].split("<->")
            if to.strip() == "none":
                continue
            #
            if "-" in frm:
                frms, frme = frm.split("-")
            else:
                frms = frme = frm
            #
            if "-" in to:
                tos, toe = to.split("-")
            else:
                tos = toe = to
            frms = ast.literal_eval(frms.strip())
            frmslead = (frms >> 8)
            frmstrail = (frms & 0xFF)
            frme = ast.literal_eval(frme.strip())
            frmelead = (frme >> 8)
            frmetrail = (frme & 0xFF)
            tos = ast.literal_eval(tos.strip())
            tosku = ((tos >> 8) & 0x7F) - 0x20
            tosten = (tos & 0x7F) - 0x20
            toe = ast.literal_eval(toe.strip())
            toeku = ((toe >> 8) & 0x7F) - 0x20
            toeten = (toe & 0x7F) - 0x20
            fw, ft, tk, tt = frmslead, frmstrail, tosku, tosten
            while 1:
                #print(hex(fw), hex(ft), tk, tt, file=sys.stderr)
                mapping[(fw << 8) | ft] = (tk, tt) if plane is None else (plane, tk, tt)
                if (fw, ft) == (frmelead, frmetrail):
                    # Don't do this as a "while" conditional since we need this one too.
                    # Think of this as quasi-"do".
                    break
                elif ft == 0x7E:
                    # Big5 avoids all control bytes as trails.
                    ft = 0xA1
                elif ft == 0xFE:
                    ft = 0x40
                    fw += 1
                else:
                    ft += 1
                #
                if (tk, tt) == (toeku, toeten):
                    raise AssertionError("destination ran out before source in range mapping.")
                elif tt == 94:
                    tk += 1
                    tt = 1
                else:
                    tt += 1
                #
            #
        #
    return mapping

def read_big5_planes(fil, *, plane=None, mapper=parsers.identitymap):
    if mapper is parsers.identitymap:
        mappername = ""
    elif mapper.__name__ != "<lambda>":
        mappername = "_" + mapper.__name__
    else:
        mappername = "_FIXME"
    cachebfn = os.path.splitext(fil)[0].replace("/", "---") + ("_plane{:02d}".format(plane)
               if plane is not None else "_mainplane") + mappername + ".json"
    cachefn = os.path.join(parsers.cachedirectory, cachebfn)
    if os.path.exists(cachefn):
        # Cache output since otherwise several seconds are spend in here upon importing graphdata
        f = open(cachefn, "r")
        r = json.load(f)
        f.close()
        return tuple(tuple(i) if i is not None else None for i in r)
    for _i in open(os.path.join(parsers.directory, fil), "r"):
        if not _i.strip():
            continue
        elif _i[0] == "#":
            continue # is a comment..
        elif _i[:2] == "0x":
            # Consortium-style format, over GL (or GR with eucjp=1) without transformation.
            byts, ucs = _i.split("\t", 2)[:2]
            byts = int(byts[2:], 16)
            if byts not in big5_to_cns2:
                continue
            men, ku, ten = big5_to_cns2[byts]
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
        else:
            raise AssertionError(line)
        assert ucs[:2] in ("0x", "U+")
        ucs = ucs[2:]
        pointer = ((men - 1) * 94 * 94) + ((ku - 1) * 94) + (ten - 1)
        iucs = mapper(pointer, tuple(int(j, 16) for j in ucs.rstrip(">").split("+")))
        if len(_temp) > pointer:
            if _temp[pointer] == None:
                _temp[pointer] = iucs
        else:
            while len(_temp) < pointer:
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

# Comments: the Kana correspondance of RFC 1922 matches the Big5 Kana encoding in the WHATWG Big5
# mappings, but not the Big5 Kana encoding in the Python Big5 codec (although it does match the
# Python Big5-HKSCS codec). Since there exist at least two ways of encoding kana in the same 
# corporate range of Big5, this is not vastly surprising.
# Big5-HKSCS is an extension of Big5-ETEN. Unicode's supplied (semi-withdrawn) BIG5.TXT includes
# the non-ETEN Kana and Cyrillic mappings.
# What it does mean is that the codecs Python uses for "Big5" and "CP950" actually includes some
# allocations collisive with Big5-ETEN; notably, CP950 itself per CP950.TXT appears only to contain
# a very small subset of the ETEN extensions (碁銹裏墻恒粧嫺 and box drawing). The difference between
# Python's "Big5" and "CP950" codecs seems to be the incorporation of these extensions.
# Moral: don't encode Kana and Cyrillic in Big5. Pretty much.
big5_to_cns1 = read_big5_rangemap("Other/rfc1922.txt", 1)
big5_to_cns1.update(read_big5_rangemap("Other/rfc1922.txt", 2))
big5_to_cns2 = read_big5_rangemap("Other/rfc1922.txt", 3, plane=2)
# The two duplicate kanji. RFC 1922 includes mappings to the same CNS codepoints as the other ones,
# (and confusingly lists a single plane 1 mapping in Appendix 2 which maps to plane 2, hmm…).
big5_to_cns2[0xC94A] = (1, 36, 34) # IBM's (13, 4, 40)
big5_to_cns2[0xDDFC] = (2, 33, 86) # IBM's (13, 4, 42)

for _i in big5_to_cns1:
    big5_to_cns2[_i] = (1,) + big5_to_cns1[_i]

graphdata.gsets["hkscs"] = hkscs_extras = (94, 2, read_big5extras("WHATWG/index-big5.txt"))
graphdata.gsets["etenexts"] = eten_extras = (94, 2, 
    ((None,) * (32 * 188)) + hkscs_extras[2][(32 * 188):])
graphdata.gsets["ms950exts"] = ms_big5_extras = (94, 2, read_big5extras("Vendor/CP950.TXT"))
graphdata.gsets["utcbig5exts"] = utc_big5_extras = (94, 2, read_big5extras("UTC/BIG5.TXT"))
graphdata.gsets["ms950utcexts"] = msutc_big5_extras = (94, 2,
    utc_big5_extras[2] + ms_big5_extras[2][len(utc_big5_extras[2]):])







