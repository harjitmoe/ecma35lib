#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020/2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, ast, sys, json, pprint, shutil
from ecma35.data import graphdata, variationhints
from ecma35.data.multibyte import mbmapparsers as parsers

# Charsets originating from Hong Kong or Taiwan (CCCII, CNS 11643, Big 5, HKSCS…).
#   (GB12345 is traditional but Mainland Chinese: see guobiao.py for that one.)
# Bumpy ride here, so brace yourselves.

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
    #   no guarantee it'll show up even legibly same (and you can forget about aural rendering).
    (0xFFF7A,): (0x5B90,), (0xFFF7B,): (0x8786,), (0xFFFEF,): (0x7E64,), (0xFFFF0,): (0x5900,),
    (0xFFFF1,): (0x5365,), (0xFFFF3,): (0x5324,), (0xFFFF5,): (0x5E71,), (0xFFFF6,): (0x7193,),
    (0xFFFF7,): (0x6E7C,), (0xFFFF8,): (0x98E4,), (0xFFFF9,): (0x79CC,), (0xFFFFA,): (0x5CD5,),
    (0xFFFFB,): (0x488C,), (0xFFFFC,): (0x80BB,), (0xFFFFD,): (0x5759,),
    # The Gov-TW mappings seem to insist on SPUA assignments for Roman characters which
    #   Unicode represents as combining sequences.
    (0xF91D1,): (0x6D, 0x0302), (0xF91D2,): (0x6E, 0x0302), (0xF91D3,): (0x6D, 0x030C),
    (0xF91D4,): (0x6D, 0x0304), (0xF91D5,): (0x6E, 0x0304), (0xF91D6,): (0x6D, 0x030D),
    (0xF91D7,): (0x6E, 0x030D), (0xF91D8,): (0x61, 0x030D), (0xF91D9,): (0x69, 0x030D),
    (0xF91DA,): (0x75, 0x030D), (0xF91DB,): (0x65, 0x030D), (0xF91DC,): (0x6F, 0x030D),
    (0xF91DD,): (0x6D, 0x030B), (0xF91DE,): (0x6E, 0x030B), (0xF91DF,): (0x61, 0x030B),
    (0xF91E0,): (0x69, 0x030B), (0xF91F7,): (0x65, 0x030B),
}
def cnsmapper_contraspua(pointer, ucs):
    return _contraspua.get(ucs, ucs)

ir184_to_old_ir183 = { 26554: 23820, 26564: 23821, 26588: 23822, 26590: 23823, 26621: 23824, 26633: 23825, 
         26638: 23826, 26655: 23827, 26658: 23828, 26666: 23829, 26682: 23830, 26684: 23831, 26713: 23832, 
         26776: 23833, 26786: 23834, 26806: 23835, 26827: 23836, 26828: 23837, 26910: 23838, 26931: 23839, 
         26978: 23840, 26980: 23841, 26995: 23842, 27043: 23843, 27046: 23844, 27068: 23845, 27070: 23846, 
         27193: 23847, 27195: 23848, 27276: 23849, 27280: 23850, 27281: 23851, 27290: 23852, 27338: 23853, 
         27341: 23854, 27359: 23855, 27377: 23856, 27403: 23857, 27426: 23858, 27431: 23859, 27520: 23860, 
         27571: 23861, 27601: 23862, 27606: 23863, 27663: 23864, 27678: 23865, 27679: 23866, 27680: 23867, 
         27685: 23868, 27694: 23869, 27720: 23870, 27731: 23871, 27746: 23872, 27771: 23873, 27795: 23874, 
         27797: 23875, 27906: 23876, 27929: 23877, 27943: 23878, 27947: 23879, 27950: 23880, 27962: 23881, 
         28087: 23882, 28160: 23883, 28163: 23884, 28191: 23885, 28215: 23886, 28264: 23887, 28289: 23888, 
         28341: 23889, 28376: 23890, 28416: 23891, 28470: 23892, 28472: 23893, 28477: 23894, 28494: 23895, 
         28556: 23896, 28560: 23897, 28562: 23898, 28593: 23899, 28654: 23900, 28655: 23901, 28671: 23902, 
         28684: 23903, 28732: 23904, 28734: 23905, 28735: 23906, 28922: 23907, 28933: 23908, 29000: 23909, 
         29096: 23910, 29101: 23911, 29123: 23912, 29200: 23913, 29276: 23914, 29305: 23915, 29356: 23916, 
         29509: 23917, 29516: 23918, 29622: 23919, 29630: 23920, 29632: 23921, 29679: 23922, 29729: 23923, 
         29751: 23924, 29792: 23925, 29793: 23926, 29814: 23927, 29842: 23928, 30004: 23929, 30053: 23930, 
         30155: 23931, 30156: 23932, 30160: 23933, 30165: 23934, 30193: 23935, 30234: 23936, 30277: 23937, 
         30314: 23938, 30318: 23939, 30320: 23940, 30327: 23941, 30416: 23942, 30433: 23943, 30486: 23944, 
         30543: 23945, 30550: 23946, 30644: 23947, 30647: 23948, 30699: 23949, 30702: 23950, 30764: 23951, 
         30781: 23952, 30795: 23953, 30926: 23954, 30975: 23955, 30993: 23956, 30996: 23957, 31003: 23958, 
         31022: 23959, 31043: 23960, 31219: 23961, 31345: 23962, 31447: 23963, 31551: 23964, 31799: 23965, 
         31824: 23969, 31851: 23966, 32050: 23967, 32137: 23968, 32439: 23970, 32508: 23971, 32606: 23972, 
         32607: 23973, 32760: 23974, 32774: 23975, 32784: 23976, 32852: 23977, 32881: 23978, 32911: 23979, 
         33052: 23980, 33067: 23981, 33114: 23982, 33154: 23983, 33211: 23984, 33333: 23985, 33472: 23986, 
         33547: 23987, 33674: 23988, 33768: 23989, 33804: 23990}

# Since the gov.tw data disagrees with literally every other source I have on the matter
# (ISO-IR-171, UTC mappings, ICU mappings, Yasuoka's mappings, RFC 1922…; although not without
# reason, since it made it the same as Big5 order), change arrow order to match.
def cnsmapper_swaparrows(pointer, ucs):
    if (pointer == 148) and (ucs == (0x2190,)):
        return (0x2192,)
    elif (pointer == 149) and (ucs == (0x2192,)):
        return (0x2190,)
    return ucs
def cnsmapper_swaparrows_thrashscii2(pointer, ucs):
    if (pointer == 148) and (ucs == (0x2190,)):
        return (0x2192,)
    elif (pointer == 149) and (ucs == (0x2192,)):
        return (0x2190,)
    elif (61852 <= pointer < 61947) and (len(ucs) == 1) and (ucs[0] < 0x7F):
        # DBCS halfwidth ASCII (seemingly intended to be contrastive with plane 1 forms)
        # Because of course there are.
        return (ucs[0], 0xF87F)
    return ucs

def cnsmapper_contraredundantcjkb(pointer, ucs):
    # U+2420E arguably should never have been added: https://unicode.org/wg2/docs/n2644.pdf
    if ucs == (0x2420E,):
        return (0x3DB7,)
    return ucs

planesize = 94 * 94
cns_bmp = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
    "CNS2UNICODE_Unicode BMP.txt",
    mapper = cnsmapper_swaparrows_thrashscii2)
cns_sip = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
    "CNS2UNICODE_Unicode 2.txt",
    mapper = cnsmapper_contraredundantcjkb)
cns_spuaa = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
    "CNS2UNICODE_Unicode 15.txt",
    mapper = cnsmapper_contraspua)
cns = parsers.fuse([cns_bmp, cns_sip, cns_spuaa], "GOV-TW---CNS2UNICODE_swar_tsci_cspua_crcb.json")

cns_govbmp = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
    "CNS2UNICODE_Unicode BMP.txt")
cns_govsip = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
    "CNS2UNICODE_Unicode 2.txt")
cns_govspuaa = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
    "CNS2UNICODE_Unicode 15.txt")
cns_gov = parsers.fuse([cns_govbmp, cns_govsip, cns_govspuaa], "GOV-TW---CNS2UNICODE.json")

cns_yasuoka = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/Uni2CNS"), 
    "Uni2CNS")
cns_icu_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
    "cns-11643-1992.ucm")
cns_icu_2014 = parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
    "euc-tw-2014.ucm")

cns_fullplane3 = list(cns) # Conversion from tuple creates a copy
for index in ir184_to_old_ir183:
    cns_fullplane3[ir184_to_old_ir183[index]] = cns_fullplane3[index]

# Planes present in the original 1986 edition of CNS 11643.
# Closely related to Big5. ISO-IR numbers in the 170s (whereas the 1992 additions are in the 180s).
# ir171 was mostly kept the same until 2007, then extended a bit, due to being the non-kanji plane.
graphdata.gsets["ir171"] = cns1 = (94, 2, cns[planesize * 0 : planesize * 1])
graphdata.gsets["ir171-govtw"] = cns1_gov = (94, 2, cns_gov[planesize * 0 : planesize * 1])
graphdata.gsets["ir171-ibm"] = euctw_g1_ibm = (94, 3, parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/euc-tw-2014.ucm"),
    "euc-tw-2014.ucm",
    plane = 1))
graphdata.gsets["ir171-utc"] = (94, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/CNS11643.TXT"), 
    "CNS11643.TXT", 
    plane = 1))
graphdata.gsets["ir171-yasuoka"] = (94, 2, cns_yasuoka[planesize * 0 : planesize * 1])
graphdata.gsets["ir171-icu"] = (94, 2, cns_icu_old[planesize * 0 : planesize * 1])
graphdata.gsets["ir171-icu-2014"] = (94, 2, cns_icu_2014[planesize * 0 : planesize * 1])

# ir172, ir172-govtw, ir172-icu, ir172-icu-2014, ir172-utc, ir172-yasuoka are all same
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
#   be the current 毵 versus the CNS11643.TXT 毶 at 69-26, both being itaiji of 02-49-32 毿).
#   Note that an unrelated plane 14 was added in 2007.
graphdata.gsets["ir183"] = cns3 = (94, 2, cns[planesize * 2 : planesize * 3]) # == ir183-govtw
_ir183oldirg = parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/CNS11643.TXT"),
    "CNS11643.TXT",
    plane = 14)
_ir183nearfull = tuple(cns_fullplane3[planesize * 2 : planesize * 3])
_ir183full = parsers.fuse([_ir183nearfull, _ir183oldirg], "ir183fullnew.json")
_ir183fullalt = parsers.fuse([_ir183oldirg, _ir183nearfull], "ir183fullalt.json")
graphdata.gsets["ir183-1988"] = cns3_1988 = (94, 2, tuple(_ir183fullalt)[:6319])
graphdata.gsets["ir183-1988plus"] = cns3plus = (94, 2, tuple(_ir183fullalt))
graphdata.gsets["ir183-1992"] = cns3_1988 = (94, 2, tuple(_ir183full)[:6148])
graphdata.gsets["ir183-full"] = cns3_1988 = (94, 2, tuple(_ir183full))
graphdata.gsets["ir183-utc"] = (94, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/CNS11643.TXT"), 
    "CNS11643.TXT", 
    plane = 14)) # yes, this is correct.
graphdata.gsets["ir183-yasuoka"] = (94, 2, cns_yasuoka[planesize * 2 : planesize * 3])
graphdata.gsets["ir183-icu"] = (94, 2, cns_icu_old[planesize * 2 : planesize * 3])
graphdata.gsets["ir183-icu-2014"] = (94, 2, cns_icu_2014[planesize * 2 : planesize * 3])

graphdata.gsets["ir184"] = cns4 = (94, 2, cns[planesize * 3 : planesize * 4])
graphdata.gsets["ir184-govtw"] = cns4_gov = (94, 2, cns_gov[planesize * 3 : planesize * 4])
graphdata.gsets["ir184-yasuoka"] = (94, 2, cns_yasuoka[planesize * 3 : planesize * 4])
graphdata.gsets["ir184-icu"] = (94, 2, cns_icu_old[planesize * 3 : planesize * 4])
graphdata.gsets["ir184-icu-2014"] = (94, 2, cns_icu_2014[planesize * 3 : planesize * 4])

graphdata.gsets["ir185"] = cns5 = (94, 2, cns[planesize * 4 : planesize * 5])
graphdata.gsets["ir185-govtw"] = cns5_gov = (94, 2, cns_gov[planesize * 4 : planesize * 5])
graphdata.gsets["ir185-yasuoka"] = (94, 2, cns_yasuoka[planesize * 4 : planesize * 5])
graphdata.gsets["ir185-icu"] = (94, 2, cns_icu_old[planesize * 4 : planesize * 5])
graphdata.gsets["ir185-icu-2014"] = (94, 2, cns_icu_2014[planesize * 4 : planesize * 5])

graphdata.gsets["ir186"] = cns6 = (94, 2, cns[planesize * 5 : planesize * 6])
graphdata.gsets["ir186-govtw"] = cns6_gov = (94, 2, cns_gov[planesize * 5 : planesize * 6])
graphdata.gsets["ir186-yasuoka"] = (94, 2, cns_yasuoka[planesize * 5 : planesize * 6])
graphdata.gsets["ir186-icu"] = (94, 2, cns_icu_old[planesize * 5 : planesize * 6])
graphdata.gsets["ir186-icu-2014"] = (94, 2, cns_icu_2014[planesize * 5 : planesize * 6])

graphdata.gsets["ir187"] = cns7 = (94, 2, cns[planesize * 6 : planesize * 7])
graphdata.gsets["ir187-govtw"] = cns7_gov = (94, 2, cns_gov[planesize * 6 : planesize * 7])
graphdata.gsets["ir187-yasuoka"] = (94, 2, cns_yasuoka[planesize * 6 : planesize * 7])
graphdata.gsets["ir187-icu"] = (94, 2, cns_icu_old[planesize * 6 : planesize * 7])
graphdata.gsets["ir187-icu-2014"] = (94, 2, cns_icu_2014[planesize * 6 : planesize * 7])
# Plane 7 is the last one to be registered with ISO-IR.

# The entirety does also exist as an unregistered 94^n set, used by EUC-TW:
graphdata.gsets["cns-eucg2"] = euctw_g2 = (94, 3, cns)
graphdata.gsets["cns-eucg2-yasuoka"] = (94, 3, cns_yasuoka)
graphdata.gsets["cns-eucg2-icu-old"] = (94, 3, cns_icu_old)
graphdata.gsets["cns-eucg2-icu-2014"] = (94, 3, cns_icu_2014)
graphdata.gsets["cns-eucg2-govtw"] = euctw_g2_gov = (94, 3, cns_gov)
# The version of EUC-TW used by ICU, with standard assignments in planes 1-7 and 15,
#   a user-defined area in plane 12, and IBM corporate assignments in plane 13.
#   Note that this is incompatible with the current standard's use of planes 12 and 13.
# Special mention is warrented for plane 15: it was published as an extension in 1990,
#   but was only integrated into the standard proper in 2007, by which point several
#   assignments were redundant and were skipped. Actually, the early full versions of
#   cns-11643-1992.ucm include it as plane 9 for some reason (later versions remove
#   it due to limiting that mapping's scope to ISO-2022-CN-EXT, then to ISO-2022-CN).
graphdata.gsets["cns-eucg2-ibm"] = euctw_g2_ibm = (94, 3, parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/euc-tw-2014.ucm"),
    "euc-tw-2014.ucm"))
graphdata.gsetflags["cns-eucg2-ibm"] |= {"BIG5:IBMCOMPATKANJI"}

# # # # # # # # # #
# Big Five

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

def read_big5_plainmap(fil, *, plane=None):
    # For the CNS 11643 open data
    mapping = {}
    reading = False
    for _i in open(os.path.join(parsers.directory, fil), "r"):
        cns, big5 = _i.strip().split(None, 1)
        men, sevenbit = cns.split("-", 1)
        men = int(men, 10)
        ku = int(sevenbit[:2], 16) - 0x20
        ten = int(sevenbit[2:], 16) - 0x20
        if plane not in (men, None):
            continue
        mapping[int(big5, 16)] = (men, ku, ten)
    return mapping

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
parsers.big5_to_cns_maps["big5_to_cns1"] = big5_to_cns1
big5_to_cns2 = read_big5_rangemap("Other/rfc1922.txt", 3, plane=2)
# The two duplicate kanji. RFC 1922 includes mappings to the same CNS codepoints as the other ones,
# (and confusingly lists a single plane 1 mapping in the appendix which maps to plane 2, hmm…).
big5_to_cns2[0xC94A] = (1, 36, 34)
big5_to_cns2[0xDDFC] = (2, 33, 86)

for _i in big5_to_cns1:
    big5_to_cns2[_i] = (1,) + big5_to_cns1[_i]
# Update for the Euro sign (which merely extends one of the existing ranges mapping between the two
#   of them, but postdates RFC 1922). This correspondance matches all three of Windows-950, WHATWG
#   and the Big5E quoted on the CNS website itself, so it is more or less entirely agreed upon.
big5_to_cns2[0xA3E1] = (1, 34, 34)
parsers.big5_to_cns_maps["big5_to_cns2"] = big5_to_cns2

# IBM's plane 13 contains codes mainly for round-trip compatibility with Big5 variants.
# It is not compatible with the standard plane 13 (introduced 2007).
big5_to_cns2_ibmvar = big5_to_cns2.copy()
big5_to_cns2_ibmvar[0xC94A] = (13, 4, 40)
big5_to_cns2_ibmvar[0xDDFC] = (13, 4, 42)
parsers.big5_to_cns_maps["big5_to_cns2_ibmvar"] = big5_to_cns2_ibmvar

# Now that big5_to_cns2 is defined, we can do this:
graphdata.gsets["ir171-ms"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/windows-950-2000.ucm"),
    "windows-950-2000.ucm",
    "big5_to_cns2",
    plane=1))
# IBM-950 uses a considerably different mapping to Windows-950 (though the rough identity of the
#   characters doesn't differ besides no euro and added control pictures, the mapping does differ).
graphdata.gsets["ir171-ibm950"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/ibm-950_P110-1999.ucm"),
    "ibm-950_P110-1999.ucm",
    "big5_to_cns2",
    plane=1))
# IBM-1373 mapping differs from MS-950 in whether C255 (01-86-33, 1-7641) maps to U+5F5E or U+5F5D
#   (differing only in the version of the snout radical used)
graphdata.gsets["ir171-ibm1373"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/ibm-1373_P100-2002.ucm"),
    "ibm-1373_P100-2002.ucm",
    "big5_to_cns2",
    plane=1))
graphdata.gsets["ir171-utcbig5"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("UTC/BIG5.TXT"),
    "BIG5.TXT",
    "big5_to_cns2",
    plane=1))
graphdata.gsets["ir171-utc"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/CNS11643.TXT"),
    "CNS11643.TXT",
    plane=1))
graphdata.gsets["ir171-1984moz"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("Mozilla/big5_1984.txt"),
    "big5_1984.txt",
    "big5_to_cns2",
    plane=1))
# Basically the Windows one, but with the addition of the control pictures:
graphdata.gsets["ir171-web"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("WHATWG/index-big5.txt"),
    "index-big5.txt",
    "big5_to_cns2",
    plane=1))
# "Mozilla 1.5" one's main plane matches Microsoft, while the "Mozilla 1.8" one's matches WHATWG.
#
# For IR-172 (unlike IR-171), MS, Mac, Web, Moz1984 and UTC-BIG5 actually match (while UTC-CNS differs)
graphdata.gsets["ir172-big5"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("UTC/BIG5.TXT"),
    "BIG5.TXT",
    "big5_to_cns2",
    plane=2))

# Macintosh-compatibility variants
maccnsdata = parsers.read_untracked(
    "Mac/macCNS.json",
    "Mac/CHINTRAD.TXT",
    parsers.decode_main_plane_big5,
    parsers.parse_file_format("Mac/CHINTRAD.TXT"),
    "CHINTRAD.TXT",
    "big5_to_cns2_ibmvar",
    mapper = variationhints.ahmap)
graphdata.gsets["ir171-mac"] = (94, 2, maccnsdata[:94*94])
#graphdata.gsets["ir172-mac"] = (94, 2, maccnsdata[94*94:94*94*2]) # same as ir172-big5

# The most basic subset of EUC-TW supported is basically a transformation format of
#   Big5. Anything more isn't really supported/used nearly as much. So using Big5
#   mappings in EUC-TW implementations is applicable. Expecially since we're using 
#   EUC-TW to underpin the Big5 filter.
graphdata.gsets["cns-eucg2-mac"] = euctw_g2 = (94, 3, maccnsdata)
graphdata.gsetflags["cns-eucg2-mac"] |= {"BIG5:IBMCOMPATKANJI"}
graphdata.gsets["cns-eucg2-ms"] = euctw_g2 = (94, 3, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/windows-950-2000.ucm"),
    "windows-950-2000.ucm",
    "big5_to_cns2_ibmvar"))
graphdata.gsetflags["cns-eucg2-ms"] |= {"BIG5:IBMCOMPATKANJI"}

graphdata.gsets["aton-exts"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Mozilla/uao241-b2u.txt"),
    "uao241-b2u.txt"))
graphdata.gsets["aton-exts2"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Mozilla/uao250-b2u.txt"),
    "uao250-b2u.txt"))
graphdata.gsets["big5e-exts"] = big5e_extras = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Mozilla/big5e.txt"),
    "big5e.txt"))
graphdata.gsets["hkscs"] = hkscs_extras = (94, 2, parsers.fuse([
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("WHATWG/index-big5.txt"),
        "index-big5.txt"), 
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs2004.txt", moz2004=True),
        "hkscs2004.txt"),
], "BIG5-HKSCS2004.json"))
graphdata.gsets["hkscs2004"] = hkscs04_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs2004.txt", moz2004=True),
        "hkscs2004.txt"))
graphdata.gsets["hkscs2001"] = hkscs01_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs2001.txt", skipstring="<reserved>"),
        "hkscs2001.txt-skipreserved"))
graphdata.gsets["hkscs1999"] = hkscs99_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs1999.txt", skipstring="<reserved>"),
        "hkscs1999.txt-skipreserved"))
graphdata.gsets["gccs"] = gccs_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/gccs.txt"),
        "gccs.txt"))
# ETEN exts, plus the handful of HKSCS ones which follow, rather than preceeding, the standard
#   assignments. Used by WHATWG's encoder (as opposed to decoder, which is full HKSCS):
graphdata.gsets["etenextsplus"] = eten_extras_plus = (94, 2, 
    ((None,) * (32 * 188)) + hkscs_extras[2][(32 * 188):])
graphdata.gsets["etenexts"] = eten_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/eten.txt"),
        "eten.txt"))
graphdata.gsets["big5-2003-exts"] = big5_2003_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/big5_2003-b2u.txt"),
        "big5_2003-b2u.txt"))
graphdata.gsets["big5-plus-exts1"] = big5_plus_extras1 = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/big5plus-obsolete.txt"),
        "big5plus-obsolete.txt"))
graphdata.gsets["big5-plus-exts2"] = big5_plus_extras2 = (94, 2, parsers.decode_second_extra_plane_big5(
        parsers.parse_file_format("Mozilla/big5plus-obsolete.txt"),
        "big5plus-obsolete.txt"))
graphdata.gsets["ms950exts"] = ms_big5_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("ICU/windows-950-2000.ucm"),
        "windows-950-2000.ucm"))
graphdata.gsets["ibmbig5exts"] = ibm_big5_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("ICU/ibm-950_P110-1999.ucm"),
        "ibm-950_P110-1999.ucm"))
graphdata.gsets["ibmbig5exts2"] = ibm_big5_extras2 = (94, 2, parsers.decode_second_extra_plane_big5(
        parsers.parse_file_format("ICU/ibm-950_P110-1999.ucm"),
        "ibm-950_P110-1999.ucm"))
# IBM-1373 has the same Big5 exts mapping as MS-950. IBM-950 exts is also a subset of ETEN exts,
#   but a different (and non-overlapping) one, for some reason.
graphdata.gsets["utcbig5exts"] = utc_big5_extras = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("UTC/BIG5.TXT"),
        "BIG5.TXT"))
graphdata.gsets["ms950utcexts"] = msutc_big5_extras = (94, 2,
    parsers.fuse([utc_big5_extras[2], ms_big5_extras[2]], "BIG5-MSUTC.json"))
#
dynalab_a = parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Adobe/AdobeCNS.txt", cidmap=("HKdla-B5", "UniCNS-UTF32")),
        "AdobeCNS.txt-HKdla-B5-UniCNS-UTF32")
dynalab_b = parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Adobe/AdobeCNS.txt", cidmap=("HKdlb-B5", "UniCNS-UTF32")),
        "AdobeCNS.txt-HKdlb-B5-UniCNS-UTF32")
graphdata.gsets["dynalabexts"] = dynalab_big5_extras = (94, 2, parsers.fuse([
    dynalab_a,
    dynalab_b,
], "Big5-Dynalab-Exts.json"))
graphdata.gsets["monotypeexts"] = monotype_big5_extras = (94, 2, parsers.fuse([
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Adobe/AdobeCNS.txt", cidmap=("HKm314-B5", "UniCNS-UTF32")),
        "AdobeCNS.txt-HKm314-B5-UniCNS-UTF32"),
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Adobe/AdobeCNS.txt", cidmap=("HKm471-B5", "UniCNS-UTF32")),
        "AdobeCNS.txt-HKm471-B5-UniCNS-UTF32"),
], "Big5-Monotype-Exts.json"))


# # # # # # # # # #
# CCCII and EACC

# Note: kEACC does not add additional characters relative to or contradict the LoC mapping at any
#   point and is therefore not referenced (the LoC mapping also includes non-kanji).
# I'm treating kCCCII as the best source for CCCII insofar as it covers.

cccii_unihan = parsers.read_unihan_planes("UCD/Unihan_OtherMappings-14.txt", "kCCCII", set96=True)
graphdata.gsets["eacc-pure"] = (96, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("LoC/eacc2uni.txt", libcongress=True),
    "eacc2uni.txt",
    set96=True))
graphdata.gsets["cccii-koha"] = (96, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Perl/Encode-HanExtra/ucm/cccii.ucm"),
    "cccii.ucm",
    set96=True,
    skip_invalid_kuten=True))
graphdata.gsets["eacc-hongkong"] = (96, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/eacc-hongkonguni.txt"),
    "eacc-hongkonguni.txt",
    set96=True, 
    ignore_later_altucs=True,
    skip_invalid_kuten=True))
maxmat1 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/cccii-maxmat.txt"),
    "cccii-maxmat.txt",
    set96=True)
maxmat2 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/eacc-maxmat.txt"),
    "eacc-maxmat.txt",
    set96=True)
# The tilde sets (~cccii and ~eacc) are used in the process of (re)generating the maxmat files.
graphdata.gsets["~cccii"] = (96, 3, parsers.fuse([
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/cccii-nonkanji.txt"),
        "cccii-nonkanji.txt",
        set96=True),
    cccii_unihan,
    graphdata.gsets["cccii-koha"][2],
    graphdata.gsets["eacc-pure"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["eacc-hongkong"][2][96*99:],
], "CCCII-Full-Raw.json"))
graphdata.gsetflags["eacc-pure"] |= {"EACC:ONLY3PLANESPERLEVEL"}
graphdata.gsets["~eacc"] = (96, 3, parsers.fuse([
    graphdata.gsets["eacc-pure"][2],
    graphdata.gsets["eacc-hongkong"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["~cccii"][2][96*99:],
], "EACC-Full-Raw.json"))
graphdata.gsets["cccii"] = (96, 3, parsers.fuse([
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/cccii-nonkanji.txt"),
        "cccii-nonkanji.txt",
        set96=True),
    maxmat1,
    cccii_unihan,
    graphdata.gsets["cccii-koha"][2],
    graphdata.gsets["eacc-pure"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["eacc-hongkong"][2][96*99:],
], "CCCII-Full4.json"))
graphdata.gsetflags["eacc-pure"] |= {"EACC:ONLY3PLANESPERLEVEL"}
graphdata.gsets["eacc"] = (96, 3, parsers.fuse([
    maxmat2,
    graphdata.gsets["eacc-pure"][2],
    graphdata.gsets["eacc-hongkong"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["cccii"][2][96*99:],
], "EACC-Full4.json"))




