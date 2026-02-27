#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020/2021/2022/2023/2024/2025/2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, ast, sys, json, pprint, shutil
from ecma35.data import graphdata, variationhints, deprecated_cjkci
from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte.cns11643_pua_to_standard import cns11643_pua_to_standard
from ecma35.data.multibyte.cns11643_pua_to_standard_loose import cns11643_pua_to_standard_loose
from ecma35.data.multibyte.cns11643_pua_to_standard_semi_loose import cns11643_pua_to_standard_semi_loose

# Charsets originating from Hong Kong or Taiwan (CCCII, CNS 11643, Big 5, HKSCS…).
#   (GB12345 is traditional but Mainland Chinese: see guobiao.py for that one.)
# Bumpy ride here, so brace yourselves.

def cnsmapper_contraspua(pointer, ucs):
    return cns11643_pua_to_standard.get(ucs, ucs)

def cnsmapper_contraspua_semi_thorough(pointer, ucs):
    return cns11643_pua_to_standard_semi_loose.get(ucs, None)

def cnsmapper_contraspua_thorough(pointer, ucs):
    return cns11643_pua_to_standard_loose.get(ucs, None)

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

def cnsmapper_contrabadcjkb(pointer, ucs):
    # U+2420E arguably should never have been added: https://unicode.org/wg2/docs/n2644.pdf
    if ucs == (0x2420E,):
        return (0x3DB7,)
    # U+272F0 is a yuurei-itaiji of U+86D7 with a horizontal dividing line and one insect radical
    #   (sort of a hybrid between U+86D7 and its itaiji U+27499). CNS 11643's 7-496B (07-41-75)
    #   displays identically to U+27499 (with two insect radicals), despite being the only IRG
    #   source for U+272F0:
    #     https://www.cns11643.gov.tw/wordView.jsp?ID=477547
    # The T-source glyph for U+272F0 currently (Unicode 17, since at least 15.1) follows the
    #   UCS2003 glyph, not the CNS 11643 07-41-75 glyph, thus avoiding being a duplicate of
    #   U+27499; note further that it is a Y-variant, not a Z-variant, of U+27499. Thus, the
    #   correct Unicode mapping for EUC-TW \x8E\xA7\xC9\xEB is U+27499.
    # Also note that U+272F0's UCS2003 glyph or recent T-source glyph is properly TB-2347
    #   (11-2347, 11-03-39, \x8E\xAB\xA3\xC7) in CNS 11643, although the reference is still
    #   pending revision, not having been revised at the same time as the glyph. Note that older
    #   mapping tables use U+27499 for 11-03-39, i.e. they've swapped CNS 11643 mappings
    #   (U+27499 had not previously been horizontally extended).
    #     https://www.unicode.org/irg/docs/n2880-TSourceChanges.pdf
    # Further info (note that interlinks between Michael Kaplan's and Andrew West's sites no longer
    #   work due to both having changed URL in the interim):
    #   - https://archives.miloush.net/michkap/archive/2007/11/22/6462768.html (see comments)
    #   - https://www.babelstone.co.uk/Blog/2007/12/cjk-b-case-study-1-u272f0.html
    #   - https://archives.miloush.net/michkap/archive/2007/12/03/6643180.html
    if pointer in (3834, 56850) and ucs == (0x272F0,):
        return (0x27499,)
    if pointer in (226, 88586) and ucs == (0x27499,):
        return (0x272F0,)
    # Two more CNS-11643-to-Unicode mapping swaps/corrections from the same two IRG documents:
    #   - https://www.unicode.org/irg/docs/n2879-TCAHorizontalExtension.pdf
    #   - https://www.unicode.org/irg/docs/n2880-TSourceChanges.pdf
    if pointer in (6066, 23738) and ucs == (0x4A36,):
        return (0x291B9,)
    if pointer in (2261, 90621) and ucs == (0x291B9,):
        return (0x4A36,)
    if pointer in (379, 26887) and ucs == (0x28453,):
        return (0x28456,)
    if pointer in (1210, 89570) and ucs == (0x28456,):
        return (0x28453,)
    # ISO 10646:2020 Annex P says (omitting the ones now unifiable under UCVs #194, #309 and #405):
    # - U+22936: mistakenly unified with T5-6777
    # - U+23EE4: mistakenly unified with T7-243F
    # - U+243BE: T7-2F4B source but should have been unified with U+24381 [both variants of U+70C8]
    # - U+27B1F: mistaken unification with T7-5035 although it's the G-source regarded as at fault
    # - U+28321: mistaken unification with T6-632A [although the two other source glyphs that have
    #            since been added match the T glyph, so it's the G glyph that's the odd one out now]
    # - U+293FB: glyph of T5-7C22 later diverged from G-source glyph
    # - U+29C52: glyph of T7-5666 changed since UCS2003 glyph designed
    # - U+2A0B8: glyph of T7-523A later diverged from G-source glyph
    # - U+2A6C0: mistaken unification with T5-7B5E although it's the G-source regarded as at fault
    if pointer in (1358, 54374) and ucs == (0x243BE,):
        return (0x24381,)
    # U+20B9D (TF-2136) is just U+BBF8 (mis)interpreted as a hanja:
    #   https://www.unicode.org/L2/L2024/24126-comments-cjk-abbrev.pdf
    # Note that T9-3558 is U+C28C (so for TF-2136 to be U+BBF8 is not completely exceptional):
    #   https://www.cns11643.gov.tw/wordView.jsp?ID=603480
    if ucs == (0x20B9D,):
        return (0xBBF8,)
    return deprecated_cjkci.remove_deprecated_cjkci(pointer, ucs)

_components_table = {}
with open(os.path.join(parsers.directory, "Custom/cns11643_components.txt"), "r", encoding="utf-8"
        ) as _f:
    for _line in [j for i in _f for j in [i.split("#", 1)[0].rstrip()] if j]:
        _a, _b = _line.split()
        _components_table[int(_a.removeprefix("TU-"), 16)] = int(_b.removeprefix("U+"), 16)

def cnsmapper_components(pointer, ucs):
    if len(ucs) == 1 and (result := _components_table.get(ucs[0], None)):
        return (result,)
    elif ucs in ((0xF6001,), (0xF8FAA,)):
        return (0x31C0,)
    elif ucs in ((0xF6005,), (0xF8FAB,)):
        return (0xFE45,)
    elif ucs == (0xF8FAC,):
        return (0x200CB,)
    elif ucs in ((0xF600B,), (0xF8FAD,)):
        return (0x200D1,)
    return ucs

planesize = 94 * 94
cns_bmp = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
    "CNS2UNICODE_Unicode BMP.txt",
    mapper = lambda pointer, ucs: cnsmapper_swaparrows_thrashscii2(pointer,
        cnsmapper_contrabadcjkb(pointer, ucs)))
cns_bmp_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP (old).txt"),
    "CNS2UNICODE_Unicode BMP (old).txt",
    mapper = lambda pointer, ucs: cnsmapper_swaparrows_thrashscii2(pointer,
        cnsmapper_contrabadcjkb(pointer, ucs)))
cns_sip = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
    "CNS2UNICODE_Unicode 2.txt",
    mapper = cnsmapper_contrabadcjkb)
cns_sip_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2 (old).txt"),
    "CNS2UNICODE_Unicode 2_old.txt",
    mapper = cnsmapper_contrabadcjkb)
cns_tip = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 3.txt"),
    "CNS2UNICODE_Unicode 3.txt")
cns_spuaa = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
    "CNS2UNICODE_Unicode 15.txt",
    mapper = lambda pointer, ucs: cnsmapper_contraspua(
        pointer, cnsmapper_components(pointer, ucs)))
cns_spuaa_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15 (old).txt"),
    "CNS2UNICODE_Unicode 15 (old).txt",
    mapper = lambda pointer, ucs: cnsmapper_contraspua(
        pointer, cnsmapper_components(pointer, ucs)))
cns_spuaa_loose = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
    "CNS2UNICODE_Unicode 15.txt (loose)",
    mapper = lambda pointer, ucs: cnsmapper_contraspua_thorough(
        pointer, cnsmapper_components(pointer, ucs)))
cns_spuaa_loose_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15 (old).txt"),
    "CNS2UNICODE_Unicode 15 (old).txt (loose)",
    mapper = lambda pointer, ucs: cnsmapper_contraspua_thorough(
        pointer, cnsmapper_components(pointer, ucs)))
cns_spuaa_semi_loose = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
    "CNS2UNICODE_Unicode 15.txt (semi-loose)",
    mapper = lambda pointer, ucs: cnsmapper_contraspua_semi_thorough(
        pointer, cnsmapper_components(pointer, ucs)))
cns_spuaa_semi_loose_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15 (old).txt"),
    "CNS2UNICODE_Unicode 15 (old).txt (semi-loose)",
    mapper = lambda pointer, ucs: cnsmapper_contraspua_semi_thorough(
        pointer, cnsmapper_components(pointer, ucs)))

cns_unihan_amended_parts = []
for _i in range(1, 20):
    cns_unihan_amended_parts.append(
        (None,) * (94 * 94 * (_i - 1)) + 
        parsers.read_unihan_planes(
            "UCD/Unihan_IRGSources.txt", "kIRG_TSource", f"T{_i:X}",
            mapper=cnsmapper_contrabadcjkb))
cns_unihan_amended = parsers.fuse(cns_unihan_amended_parts, "Unihan-CNS-11643-Amended.json")

cns_unihan_parts = []
for _i in range(1, 20):
    cns_unihan_parts.append(
        (None,) * (94 * 94 * (_i - 1)) + 
        parsers.read_unihan_planes("UCD/Unihan_IRGSources.txt", "kIRG_TSource", f"T{_i:X}"))
cns_unihan = parsers.fuse(cns_unihan_parts, "Unihan-CNS-11643.json")

irgn2779_amendments = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/csic_updates_from_irgn2779.txt"),
    "csic_updates_from_irgn2779.txt")

misc_amendments = [
    (None,) * (94*94*2 + 94*6 + 7) + ((0x2ED9D,),), # 03-07-08 → U+2ED9D
    (None,) * (94*94*2 + 94*68 + 25) + ((0x6BF5,),), # 03-69-26 → U+6BF5
    #
    # Unicode 17.0:
    (None,) * (94*94*3 + 94*5 + 19) + ((0x2B73A,),), # 04-06-20 → U+2B73A
    (None,) * (94*94*10 + 94*92 + 11) + ((0x2B73C,),), # 11-93-12 → U+2B73C
    (None,) * (94*94*10 + 94*92 + 14) + ((0x2B73D,),), # 11-93-15 → U+2B73D
]

cns_19 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/CSIC_plane_19.txt"),
    "CSIC_plane_19.txt")

cns_misc = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/CSIC_misc_unified.txt"),
    "CSIC_misc_unified.txt")

cns = parsers.fuse([
    *misc_amendments,
    (None,) * (94*94*18) + tuple(cns_19),
    irgn2779_amendments,
    cns_unihan_amended,
    cns_misc,
    cns_bmp,
    cns_sip,
    cns_tip,
    cns_bmp_old,
    cns_sip_old,
    cns_spuaa,
    cns_spuaa_old,
    # https://sign.hakka.gov.tw/File/Attach/47455/File_98707.pdf#page=189
    (None,) * (94*94*10 + 94*92 + 8) + ((0xFFB1B,),), # 11-93-09 → U+FFB1B (SPUA)
], "Unihan-GOV-TW---CNS2UNICODE_etc.json")

cns_govbmp = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP.txt"),
    "CNS2UNICODE_Unicode BMP.txt")
cns_govbmp_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode BMP (old).txt"),
    "CNS2UNICODE_Unicode BMP (old).txt")
cns_govsip = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2.txt"),
    "CNS2UNICODE_Unicode 2.txt")
cns_govsip_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 2 (old).txt"),
    "CNS2UNICODE_Unicode 2 (old).txt")
cns_govspuaa = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15.txt"),
    "CNS2UNICODE_Unicode 15.txt")
cns_govspuaa_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("GOV-TW/CNS2UNICODE_Unicode 15 (old).txt"),
    "CNS2UNICODE_Unicode 15 (old).txt")
cns_gov = parsers.fuse([cns_govbmp, cns_govsip, cns_tip, cns_govspuaa], "GOV-TW---CNS2UNICODE.json")
cns_gov_old = parsers.fuse([cns_govbmp_old, cns_govsip_old, cns_govspuaa_old], "GOV-TW---CNS2UNICODE_old.json")

cns_yasuoka = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/Uni2CNS"), 
    "Uni2CNS")
cns_icu_old = parsers.decode_main_plane_gl(
    parsers.parse_file_format("ICU/cns-11643-1992.ucm"), 
    "cns-11643-1992.ucm")
def no_bmp_pua(pointer, ucs):
    if len(ucs) == 1 and 0xE000 <= ucs[0] < 0xF900:
        return None
    return ucs
cns_icu_2014 = parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
    "euc-tw-2014.ucm")
cns_icu_2014_nobmppua = parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/euc-tw-2014.ucm"), 
    "euc-tw-2014.ucm",
    mapper = no_bmp_pua)
cns_ibm = parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/ibm-964_P110-1999.ucm"), 
    "ibm-964_P110-1999.ucm")

cns_fullplane3 = list(cns) # Conversion from tuple creates a copy
for index in ir184_to_old_ir183:
    cns_fullplane3[ir184_to_old_ir183[index]] = cns_fullplane3[index]

# Planes present in the original 1986 edition of CNS 11643.
# Closely related to Big5. ISO-IR numbers in the 170s (whereas the 1992 additions are in the 180s).
# ir171 was mostly kept the same until 2007, then extended a bit, due to being the non-kanji plane.
graphdata.gsets["ir171/full"] = (94, 2, parsers.fuse([
    cns[planesize * 0 : planesize * 1],
    cns_icu_2014[planesize * 0 : planesize * 1]
], "CSIC1-Full.json"))
# 1992: 01-01 thru 05-80, 06-01 thru 06-30, 07-01 thru 09-25, 34-01 thru 34-33, 36-01 onward
graphdata.gsets["ir171"] = cns1_1992 = (94, 2,
    tuple(i if n <= (4 * 94 + 79)
            or (5 * 94) <= n <= (5 * 94 + 29)
            or (6 * 94) <= n <= (8 * 94 + 24)
            or (33 * 94) <= n <= (33 * 94 + 32)
            or (35 * 94) <= n
            else None
          for n, i in enumerate(cns[planesize * 0 : planesize * 1])
    )
)
graphdata.gsets["ir171/govtw"] = (94, 2, cns_gov[planesize * 0 : planesize * 1])
graphdata.gsets["ir171/ibm"] = (94, 2, parsers.decode_main_plane_euc(
    parsers.parse_file_format("ICU/ibm-964_P110-1999.ucm"),
    "ibm-964_P110-1999.ucm",
    plane = 1))
graphdata.gsets["ir171/utc"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/CNS11643.TXT"),
    "CNS11643.TXT",
    plane = 1))
graphdata.gsets["ir171/yasuoka"] = (94, 2, cns_yasuoka[planesize * 0 : planesize * 1])
graphdata.gsets["ir171/icu"] = (94, 2, cns_icu_old[planesize * 0 : planesize * 1])
graphdata.gsets["ir171/icu-2014"] = (94, 2, cns_icu_2014[planesize * 0 : planesize * 1])

# ir172/govtw/old, ir172/icu, ir172/icu/2014, ir172/utc, ir172/yasuoka are all same
graphdata.gsets["ir172"] = (94, 2, cns_gov_old[planesize * 1 : planesize * 2])
# ir172/unihan, ir172/govtw are the same
graphdata.gsets["ir172/unihan"] = (94, 2, cns_gov[planesize * 1 : planesize * 2])

graphdata.chcpdocs["20000"] = "modified-euc"
graphdata.defgsets["20000"] = ("ir006", "ir171/full", "nil", "nil", "ir172")

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
graphdata.gsets["ir183/govtw"] = (94, 2, cns_gov[planesize * 2 : planesize * 3])
graphdata.gsets["ir183/govtw/old"] = (94, 2, cns_gov_old[planesize * 2 : planesize * 3])
graphdata.gsets["ir183/unihan"] = (94, 2, cns_unihan[planesize * 2 : planesize * 3])
_ir183oldirg = parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/CNS11643.TXT"),
    "CNS11643.TXT",
    plane = 14)
_ir183nearfull = tuple(cns_fullplane3[planesize * 2 : planesize * 3])
_ir183full = parsers.fuse([_ir183nearfull, _ir183oldirg], "ir183fullnew.json")
_ir183fullalt = parsers.fuse([_ir183oldirg, _ir183nearfull], "ir183fullalt.json")
cns3_1988_array = tuple(_ir183fullalt)[:6319] + (None,) * (len(_ir183fullalt) - 6319)
graphdata.gsets["ir183/1988"] = (94, 2, cns3_1988_array)
graphdata.gsets["ir183/1988plus"] = (94, 2, tuple(_ir183fullalt))
cns3_1992_array = tuple(_ir183fullalt)[:6148] + (None,) * (len(_ir183fullalt) - 6148)
graphdata.gsets["ir183"] = (94, 2, cns3_1992_array)
graphdata.gsets["ir183/full"] = (94, 2, tuple(_ir183full))
graphdata.gsets["ir183/utc"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("UTC/CNS11643.TXT"), 
    "CNS11643.TXT", 
    plane = 14)) # yes, this is correct.
graphdata.gsets["ir183/yasuoka"] = (94, 2, cns_yasuoka[planesize * 2 : planesize * 3])
graphdata.gsets["ir183/icu"] = (94, 2, cns_icu_old[planesize * 2 : planesize * 3])
graphdata.gsets["ir183/icu-2014"] = (94, 2, cns_icu_2014[planesize * 2 : planesize * 3])

def remove_placeholder_space(pointer, ucs):
    if ucs == (0x3000,) and pointer > 0:
        return None
    return ucs

# Subsets of CNS 11643 that X11 supports for older-file-format fonts.
# This omits the Kangxi Radicals section from plane 1, and omits the first character (01-01) from
#   planes 1 and 2 for some reason, as well as supporting only a subset of plane 3.
graphdata.gsets["ir171/x11"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/xfonts-encodings/large/cns11643-1.enc"),
    "cns11643-1.enc",
    mapper=remove_placeholder_space))
graphdata.gsets["ir172/x11"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/xfonts-encodings/large/cns11643-2.enc"),
    "cns11643-2.enc",
    mapper=remove_placeholder_space))
graphdata.gsets["ir183/x11"] = (94, 2, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/xfonts-encodings/large/cns11643-3.enc"),
    "cns11643-3.enc",
    mapper=remove_placeholder_space))

graphdata.gsets["ir184"] = (94, 2, cns[planesize * 3 : planesize * 4])
graphdata.gsets["ir184/govtw"] = (94, 2, cns_gov[planesize * 3 : planesize * 4])
graphdata.gsets["ir184/govtw/old"] = (94, 2, cns_gov_old[planesize * 3 : planesize * 4])
graphdata.gsets["ir184/unihan"] = (94, 2, cns_unihan[planesize * 3 : planesize * 4])
graphdata.gsets["ir184/yasuoka"] = (94, 2, cns_yasuoka[planesize * 3 : planesize * 4])
graphdata.gsets["ir184/icu"] = (94, 2, cns_icu_old[planesize * 3 : planesize * 4])
graphdata.gsets["ir184/icu-2014"] = (94, 2, cns_icu_2014[planesize * 3 : planesize * 4])

graphdata.gsets["ir185"] = (94, 2, cns[planesize * 4 : planesize * 5])
graphdata.gsets["ir185/govtw"] = (94, 2, cns_gov[planesize * 4 : planesize * 5])
graphdata.gsets["ir185/govtw/old"] = (94, 2, cns_gov_old[planesize * 4 : planesize * 5])
graphdata.gsets["ir185/unihan"] = (94, 2, cns_unihan[planesize * 4 : planesize * 5])
graphdata.gsets["ir185/yasuoka"] = (94, 2, cns_yasuoka[planesize * 4 : planesize * 5])
graphdata.gsets["ir185/icu"] = (94, 2, cns_icu_old[planesize * 4 : planesize * 5])
graphdata.gsets["ir185/icu-2014"] = (94, 2, cns_icu_2014[planesize * 4 : planesize * 5])

graphdata.gsets["ir186"] = (94, 2, cns[planesize * 5 : planesize * 6])
graphdata.gsets["ir186/govtw"] = (94, 2, cns_gov[planesize * 5 : planesize * 6])
graphdata.gsets["ir186/govtw/old"] = (94, 2, cns_gov_old[planesize * 5 : planesize * 6])
graphdata.gsets["ir186/unihan"] = (94, 2, cns_unihan[planesize * 5 : planesize * 6])
graphdata.gsets["ir186/yasuoka"] = (94, 2, cns_yasuoka[planesize * 5 : planesize * 6])
graphdata.gsets["ir186/icu"] = (94, 2, cns_icu_old[planesize * 5 : planesize * 6])
graphdata.gsets["ir186/icu-2014"] = (94, 2, cns_icu_2014[planesize * 5 : planesize * 6])

graphdata.gsets["ir187"] = (94, 2, cns[planesize * 6 : planesize * 7])
graphdata.gsets["ir187/govtw"] = (94, 2, cns_gov[planesize * 6 : planesize * 7])
graphdata.gsets["ir187/govtw/old"] = (94, 2, cns_gov_old[planesize * 6 : planesize * 7])
graphdata.gsets["ir187/unihan"] = (94, 2, cns_unihan[planesize * 6 : planesize * 7])
graphdata.gsets["ir187/yasuoka"] = (94, 2, cns_yasuoka[planesize * 6 : planesize * 7])
graphdata.gsets["ir187/icu"] = (94, 2, cns_icu_old[planesize * 6 : planesize * 7])
graphdata.gsets["ir187/icu-2014"] = (94, 2, cns_icu_2014[planesize * 6 : planesize * 7])
# Plane 7 is the last one to be registered with ISO-IR.

graphdata.gsets["csic8"] = (94, 2, cns[planesize * 7 : planesize * 8])
graphdata.gsets["csic8/govtw"] = (94, 2, cns_gov[planesize * 7 : planesize * 8])
graphdata.gsets["csic8/govtw/old"] = (94, 2, cns_gov_old[planesize * 7 : planesize * 8])

graphdata.gsets["csic9"] = (94, 2, cns[planesize * 8 : planesize * 9])
graphdata.gsets["csic9/govtw"] = (94, 2, cns_gov[planesize * 8 : planesize * 9])
graphdata.gsets["csic9/govtw/old"] = (94, 2, cns_gov_old[planesize * 8 : planesize * 9])

graphdata.gsets["csic10"] = (94, 2, cns[planesize * 9 : planesize * 10])
graphdata.gsets["csic10/govtw/old"] = (94, 2, cns_gov_old[planesize * 9 : planesize * 10])

graphdata.gsets["csic11"] = (94, 2, cns[planesize * 10 : planesize * 11])
graphdata.gsets["csic11/govtw"] = (94, 2, cns_gov[planesize * 10 : planesize * 11])
graphdata.gsets["csic11/govtw/old"] = (94, 2, cns_gov_old[planesize * 10 : planesize * 11])

graphdata.gsets["csic12"] = (94, 2, cns[planesize * 11 : planesize * 12])
graphdata.gsets["csic12/govtw"] = (94, 2, cns_gov[planesize * 11 : planesize * 12])
graphdata.gsets["csic12/govtw/old"] = (94, 2, cns_gov_old[planesize * 11 : planesize * 12])

graphdata.gsets["user-defined/6204"] = (94, 2, cns_ibm[planesize * 11 : planesize * 12])

graphdata.gsets["csic13-2007"] = (94, 2, cns[planesize * 12 : planesize * 13])
graphdata.gsets["csic13-2007/govtw"] = (94, 2, cns_gov[planesize * 12 : planesize * 13])
graphdata.gsets["csic13-2007/govtw/old"] = (94, 2, cns_gov_old[planesize * 12 : planesize * 13])

graphdata.gsets["ibm-euctw-extension-plane"] = (94, 2, cns_ibm[planesize * 12 : planesize * 13])

graphdata.gsets["csic14-2007"] = (94, 2, cns[planesize * 13 : planesize * 14])
graphdata.gsets["csic14-2007/govtw"] = (94, 2, cns_gov[planesize * 13 : planesize * 14])
graphdata.gsets["csic14-2007/govtw/old"] = (94, 2, cns_gov_old[planesize * 13 : planesize * 14])

# Special mention is warrented for plane 15: it was published as an extension in 1990,
#   but was only integrated into the standard proper in 2007, by which point several
#   assignments were redundant and were skipped. Actually, the early full versions of
#   cns-11643-1992.ucm include it as plane 9 for some reason (later versions remove
#   it due to limiting that mapping's scope to ISO-2022-CN-EXT, then to ISO-2022-CN).
graphdata.gsets["csic15"] = (94, 2, cns[planesize * 14 : planesize * 15])
graphdata.gsets["csic15/govtw"] = (94, 2, cns_gov[planesize * 14 : planesize * 15])
graphdata.gsets["csic15/govtw/old"] = (94, 2, cns_gov_old[planesize * 14 : planesize * 15])
graphdata.gsets["csic15/unihan"] = (94, 2, cns_unihan[planesize * 14 : planesize * 15])
graphdata.gsets["csic15/icu"] = (94, 2,
    cns_icu_old[planesize * 8 : planesize * 9]) # yes, this is correct.
graphdata.gsets["csic15/icu-2014"] = (94, 2, cns_icu_2014[planesize * 14 : planesize * 15])

graphdata.gsets["csic17"] = (94, 2, cns[planesize * 16 : planesize * 17])

graphdata.gsets["csic19"] = (94, 2, cns[planesize * 18 : planesize * 19])

# The entirety does also exist as an unregistered 94^n set, used by EUC-TW:
graphdata.gsets["cns-eucg2"] = (94, 3, parsers.fuse([
    cns,
    cns_icu_2014,
], "CSIC-All.json"))
graphdata.gsets["cns-eucg2/lax-matching"] = (94, 3, parsers.fuse([
    *misc_amendments,
    (None,) * (94*94*18) + tuple(cns_19),
    irgn2779_amendments,
    cns_unihan_amended,
    cns_misc,
    cns_bmp,
    cns_sip,
    cns_icu_2014_nobmppua,
    cns_spuaa_loose,
    cns_spuaa_loose_old,
], "CSIC-Lax-Matching.json"))
graphdata.gsets["cns-eucg2/semi-lax-matching"] = (94, 3, parsers.fuse([
    *misc_amendments,
    (None,) * (94*94*18) + tuple(cns_19),
    irgn2779_amendments,
    cns_unihan_amended,
    cns_misc,
    cns_bmp,
    cns_sip,
    cns_icu_2014_nobmppua,
    cns_spuaa_semi_loose,
    cns_spuaa_semi_loose_old,
], "CSIC-Semi-Lax-Matching.json"))
graphdata.gsets["cns-eucg2/yasuoka"] = (94, 3, cns_yasuoka)
graphdata.gsets["cns-eucg2/govtw"] = (94, 3, cns_gov)
graphdata.gsets["cns-eucg2/govtw/old"] = (94, 3, cns_gov_old)
graphdata.gsets["cns-eucg2/unihan"] = (94, 3, cns_unihan)
# The version of EUC-TW used by ICU, with standard assignments in planes 1-7 and 15,
#   a user-defined area in plane 12, and IBM corporate assignments in plane 13.
#   Note that this is incompatible with the current standard's use of planes 12 and 13.
graphdata.gsets["cns-eucg2/icu/2014/full"] = (94, 3, cns_icu_2014)
graphdata.gsetflags["cns-eucg2/icu/2014/full"] |= {"BIG5:IBMCOMPATKANJI"}
graphdata.gsets["cns-eucg2/icu/2014/noplane1"] = (94, 3, (None,) * (94 * 94) + cns_icu_2014[94*94:])
graphdata.gsetflags["cns-eucg2/icu/2014/noplane1"] |= {"BIG5:IBMCOMPATKANJI"}
graphdata.gsets["cns-eucg2/icu/old"] = (94, 3, cns_icu_old)
graphdata.gsets["cns-eucg2/ibm/full"] = (94, 3, cns_ibm)
graphdata.gsetflags["cns-eucg2/ibm/full"] |= {"BIG5:IBMCOMPATKANJI"}
graphdata.gsets["cns-eucg2/ibm/noplane1"] = (94, 3, (None,) * (94 * 94) + cns_ibm[94*94:])
graphdata.gsetflags["cns-eucg2/ibm/noplane1"] |= {"BIG5:IBMCOMPATKANJI"}

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

_hkscs2008_to_hkscs2016 = {(0x514C,): (0x5151,), (0x544A,): (0x543F,), (0x5ABC,): (0x5AAA,), (0x6085,): (0x60A6,), (0x614D,): (0x6120,), (0x6329,): (0x635D,), (0x6553,): (0x655A,), (0x68B2,): (0x68C1,), (0x6C33,): (0x6C32,), (0x6D97,): (0x6D9A,), (0x7185,): (0x7174,), (0x7A05,): (0x7A0E,), (0x7E15,): (0x7DFC,), (0x812B,): (0x8131,), (0x8183,): (0x817D,), (0x860A,): (0x85F4,), (0x86FB,): (0x8715,), (0x8AAA,): (0x8AAC,), (0x8F40,): (0x8F3C,), (0x919E,): (0x9196,), (0x92B3,): (0x92ED,), (0x95B1,): (0x95B2,)}

def hkscs2008_to_hkscs2016(pointer, ucs):
    return _hkscs2008_to_hkscs2016.get(ucs, ucs)

# Now that big5_to_cns2 is defined, we can do this:
graphdata.gsets["ir171/ms"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/windows-950-2000.ucm"),
    "windows-950-2000.ucm",
    "big5_to_cns2",
    plane=1))
# IBM-950 uses a considerably different mapping to Windows-950 (though the rough identity of the
#   characters doesn't differ besides no euro and added control pictures, the mapping does differ).
graphdata.gsets["ir171/ibm950"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/ibm-950_P110-1999.ucm"),
    "ibm-950_P110-1999.ucm",
    "big5_to_cns2",
    plane=1))
# IBM-1373 mapping differs from MS-950 in whether C255 (01-86-33, 1-7641) maps to U+5F5E or U+5F5D
#   (differing only in the version of the snout radical used)
graphdata.gsets["ir171/ibm1373"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/ibm-1373_P100-2002.ucm"),
    "ibm-1373_P100-2002.ucm",
    "big5_to_cns2",
    plane=1))
graphdata.gsets["ir171/utcbig5"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("UTC/BIG5.TXT"),
    "BIG5.TXT",
    "big5_to_cns2",
    plane=1))
graphdata.gsets["ir171/1984moz"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("Mozilla/big5_1984.txt"),
    "big5_1984.txt",
    "big5_to_cns2",
    plane=1))
# Basically the Windows one, but with the addition of the control pictures:
graphdata.gsets["ir171/web"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("WHATWG/index-big5.txt"),
    "index-big5.txt",
    "big5_to_cns2",
    plane=1))
graphdata.gsets["ir171/hkscs2016"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("WHATWG/index-big5.txt"),
    "index-big5.txt",
    "big5_to_cns2",
    plane=1,
    mapper=hkscs2008_to_hkscs2016))
# "Mozilla 1.5" one's main plane matches Microsoft, while the "Mozilla 1.8" one's matches WHATWG.
#
# For IR-172 (unlike IR-171), MS, Mac, Web, Moz1984 and UTC-BIG5 actually match (while UTC-CNS differs)
graphdata.gsets["ir172/big5"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("UTC/BIG5.TXT"),
    "BIG5.TXT",
    "big5_to_cns2",
    plane=2))
graphdata.gsets["ir172/hkscs2016"] = (94, 2, parsers.decode_main_plane_big5(
    parsers.parse_file_format("UTC/BIG5.TXT"),
    "BIG5.TXT",
    "big5_to_cns2",
    plane=2,
    mapper=hkscs2008_to_hkscs2016))

# Macintosh-compatibility variants
maccnsdata = parsers.read_untracked(
    "Mac/macCNS.json",
    "Mac/CHINTRAD.TXT",
    parsers.decode_main_plane_big5,
    parsers.parse_file_format("Mac/CHINTRAD.TXT"),
    "CHINTRAD.TXT",
    "big5_to_cns2_ibmvar",
    mapper = variationhints.ahmap)
graphdata.gsets["ir171/mac"] = (94, 2, maccnsdata[:94*94])
#graphdata.gsets["ir172/mac"] = (94, 2, maccnsdata[94*94:94*94*2]) # same as ir172-big5

# The most basic subset of EUC-TW supported is basically a transformation format of
#   Big5. Anything more isn't really supported/used nearly as much. So using Big5
#   mappings in EUC-TW implementations is applicable. Expecially since we're using 
#   EUC-TW to underpin the Big5 filter.
graphdata.gsets["cns-eucg2/mac"] = (94, 3, maccnsdata)
graphdata.gsetflags["cns-eucg2/mac"] |= {"BIG5:IBMCOMPATKANJI"}
graphdata.gsets["cns-eucg2/ms"] = (94, 3, parsers.decode_main_plane_big5(
    parsers.parse_file_format("ICU/windows-950-2000.ucm"),
    "windows-950-2000.ucm",
    "big5_to_cns2_ibmvar"))
graphdata.gsetflags["cns-eucg2/ms"] |= {"BIG5:IBMCOMPATKANJI"}

graphdata.gsets["big5exts/eten/chinasea/core"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-core.txt"),
    "ChinaSea-core.txt"))
graphdata.gsets["big5exts/eten/chinasea/gothic"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-gothic.txt"),
    "ChinaSea-gothic.txt"))
graphdata.gsets["big5exts/eten/chinasea/mincho"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-mincho.txt"),
    "ChinaSea-mincho.txt"))
graphdata.gsets["big5exts/eten/chinasea/script"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-script.txt"),
    "ChinaSea-script.txt"))
graphdata.gsets["big5exts/eten/chinasea/fangsong"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-fangsong.txt"),
    "ChinaSea-fangsong.txt"))
graphdata.gsets["big5exts/eten/chinasea/aton/old"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Mozilla/uao241-b2u.txt"),
    "uao241-b2u.txt"))
graphdata.gsets["big5exts/eten/chinasea/aton"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Mozilla/uao250-b2u.txt"),
    "uao250-b2u.txt"))

subset_components = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-components.txt"),
    "ChinaSea-subset-components.txt")
subset_extlatin = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-extlatin-cyrillic.txt"),
    "ChinaSea-subset-extlatin-cyrillic.txt")
subset_hanzi = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-hanzi.txt"),
    "ChinaSea-subset-hanzi.txt")
subset_hanzi2 = parsers.fuse([
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-hanzi2.txt"),
        "ChinaSea-subset-hanzi2.txt"),
    ((None, ) * ((81*94)+44)) + ((0x668E,), (0x9341,), (0x243EA,)),
    subset_hanzi,
], "ChinaSea-Hanzi-AlternativeOrdering.txt")
subset_hanzi3 = parsers.fuse([
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-hanzi3.txt"),
        "ChinaSea-subset-hanzi3.txt"),
    subset_hanzi,
], "ChinaSea-Hanzi-UnicodeAtOn.txt")
subset_jamo = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-jamo.txt"),
    "ChinaSea-subset-jamo.txt")
subset_kana = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-kana.txt"),
    "ChinaSea-subset-kana.txt")
subset_keyboard = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-keyboard.txt"),
    "ChinaSea-subset-keyboard.txt")
subset_letterlike = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-letterlike.txt"),
    "ChinaSea-subset-letterlike.txt")
subset_list = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-list.txt"),
    "ChinaSea-subset-list.txt")
subset_semigraphics = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-semigraphics.txt"),
    "ChinaSea-subset-semigraphics.txt")
subset_superscripts = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-superscripts.txt"),
    "ChinaSea-subset-superscripts.txt")
subset_symbols = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/ChinaSea/ChinaSea-subset-symbols.txt"),
    "ChinaSea-subset-symbols.txt")

graphdata.gsets["big5exts/big5e"] = (94, 2, parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Mozilla/big5e.txt"),
    "big5e.txt"))

_hkscs_extras = parsers.fuse([
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("WHATWG/index-big5.txt"),
        "index-big5_updated.txt",
        mapper=deprecated_cjkci.remove_deprecated_cjkci), 
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs2004.txt", moz2004=True),
        "hkscs2004.txt"),
    ((None,) * ((61*94)+12)) + ((0x32562,),),
    ((None,) * ((61*94)+57)) + ((0x81BA, 0xF87F),),
    ((None,) * ((61*94)+69)) + ((0x240D2, 0xF87F),),
    ((None,) * ((61*94)+78)) + ((0x93BA, 0xF87F),),
    ((None,) * ((62*94)+57)) + ((0x327F2,),),
    ((None,) * ((62*94)+65)) + ((0x2DF3C,),),
    ((None,) * ((63*94)+12)) + ((0x7910, 0xF87F),),
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Custom/Extended_GCCS.txt"),
        "Extended_GCCS.txt"),
], "BIG5-HKSCS2008-updated.json")
graphdata.gsets["big5exts/eten/hkscs/updated"] = (94, 2, _hkscs_extras)

_web_hkscs_extras = parsers.fuse([
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("WHATWG/index-big5.txt"),
        "index-big5.txt"), 
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs2004.txt", moz2004=True),
        "hkscs2004.txt"),
], "BIG5-HKSCS2008.json")
graphdata.gsets["big5exts/eten/hkscs"] = (94, 2, _web_hkscs_extras)

graphdata.gsets["big5exts/eten/hkscs/2004"] = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs2004.txt", moz2004=True),
        "hkscs2004.txt"))

_hkscs_2001_extras = parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs2001.txt", skipstring="<reserved>"),
        "hkscs2001.txt-skipreserved")
graphdata.gsets["big5exts/eten/hkscs/2001"] = (94, 2, _hkscs_2001_extras)
_hkscs_2001_extras_updated = parsers.cut_out(
    _hkscs_2001_extras, 
    _hkscs_extras, 
    "HKSCS-2001-updated.json")
graphdata.gsets["big5exts/eten/hkscs/2001/updated"] = (94, 2, _hkscs_2001_extras_updated)

_sakura_extras = parsers.decode_extra_plane_big5(
    parsers.parse_file_format("Custom/SakuraExtensions.txt"),
    "SakuraExtensions.txt")
graphdata.gsets["big5exts/eten/hkscs/2001/sakura"] = (94, 2, parsers.fuse([
    _sakura_extras,
    _hkscs_2001_extras_updated,
], "Big5-HKSCS2001-Sakura.json"))
graphdata.gsets["big5exts/eten/hkscs/sakura"] = (94, 2, parsers.fuse([
    _sakura_extras,
    _hkscs_extras,
], "Big5-HKSCS-Sakura.json"))

_hkscs_1999_extras = parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/hkscs1999.txt", skipstring="<reserved>"),
        "hkscs1999.txt-skipreserved")
graphdata.gsets["big5exts/eten/hkscs/1999"] = (94, 2, _hkscs_1999_extras)
graphdata.gsets["big5exts/eten/hkscs/1999/updated"] = (94, 2, parsers.cut_out(
    _hkscs_1999_extras, 
    _hkscs_extras, 
    "HKSCS-1999-updated.json"))

_gccs = parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/gccs.txt"),
        "gccs.txt")
graphdata.gsets["big5exts/eten/hkscs/gccs"] = (94, 2, _gccs)
graphdata.gsets["big5exts/eten/hkscs/gccs/ext"] = (94, 2, parsers.fuse([
    parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Custom/Extended_GCCS.txt"),
        "Extended_GCCS.txt"),
    _gccs,
    ((None,) * (18*94)) + _hkscs_extras[(18*94):(19*94)+69],
    ((None,) * ((20*94)+32)) + (
        _hkscs_extras[(20*94)+32],
        _hkscs_extras[(20*94)+33],
        None, None,
        _hkscs_extras[(20*94)+36],
        None,
        _hkscs_extras[(20*94)+38],
        None,
        _hkscs_extras[(20*94)+40],
        None,
        _hkscs_extras[(20*94)+42],
        None,
        _hkscs_extras[(20*94)+44],
        _hkscs_extras[(20*94)+45],
        _hkscs_extras[(20*94)+46],
        _hkscs_extras[(20*94)+47],
        None, None, None, None, None, None, None,
        _hkscs_extras[(20*94)+55],
        None,
        _hkscs_extras[(20*94)+57]),
], "GCCS-Extended.json"))

# ETEN exts, plus the handful of HKSCS ones which follow, rather than preceeding, the standard
#   assignments. Used by WHATWG's encoder (as opposed to decoder, which is full HKSCS):
graphdata.gsets["big5exts/eten/web"] = (94, 2, 
    ((None,) * (32 * 188)) + _web_hkscs_extras[(32 * 188):])
graphdata.gsets["big5exts/eten"] = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/eten.txt"),
        "eten.txt"))
graphdata.gsets["big5exts/eten/2003"] = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/big5_2003-b2u.txt"),
        "big5_2003-b2u.txt"))
graphdata.gsets["big5exts/eten/plus"] = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Mozilla/big5plus-obsolete.txt"),
        "big5plus-obsolete.txt"))
graphdata.gsets["big5additional/plus"] = (94, 2, parsers.decode_second_extra_plane_big5(
        parsers.parse_file_format("Mozilla/big5plus-obsolete.txt"),
        "big5plus-obsolete.txt"))
graphdata.gsets["big5exts/ms"] = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("ICU/windows-950-2000.ucm"),
        "windows-950-2000.ucm"))
graphdata.gsets["big5exts/eten/ibm"] = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("ICU/ibm-950_P110-1999.ucm"),
        "ibm-950_P110-1999.ucm"))
graphdata.gsets["big5additional/ibm"] = (94, 2, parsers.decode_second_extra_plane_big5(
        parsers.parse_file_format("ICU/ibm-950_P110-1999.ucm"),
        "ibm-950_P110-1999.ucm"))
# IBM-1373 has the same Big5 exts mapping as MS-950. IBM-950 exts is also a subset of ETEN exts,
#   but a different (and non-overlapping) one, for some reason.
graphdata.gsets["big5exts/utc"] = (94, 2, parsers.decode_extra_plane_big5(
        parsers.parse_file_format("UTC/BIG5.TXT"),
        "BIG5.TXT"))
graphdata.gsets["big5exts/utc/ms"] = (94, 2,
    parsers.fuse([graphdata.gsets["big5exts/utc"][2], graphdata.gsets["big5exts/ms"][2]], "BIG5-MSUTC.json"))
#
dynalab_a = parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Adobe/AdobeCNS.txt", cidmap=("HKdla-B5", "UniCNS-UTF32")),
        "AdobeCNS.txt-HKdla-B5-UniCNS-UTF32")
dynalab_b = parsers.decode_extra_plane_big5(
        parsers.parse_file_format("Adobe/AdobeCNS.txt", cidmap=("HKdlb-B5", "UniCNS-UTF32")),
        "AdobeCNS.txt-HKdlb-B5-UniCNS-UTF32")
graphdata.gsets["big5exts/dynalab"] = (94, 2, parsers.fuse([
    dynalab_a,
    dynalab_b,
], "Big5-Dynalab-Exts.json"))
graphdata.gsets["big5exts/monotype"] = (94, 2, parsers.fuse([
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

cccii_unihan = parsers.read_unihan_planes("UCD/Unihan_OtherMappings.txt", "kCCCII", set96=True)
graphdata.gsets["cccii/eacc/loc"] = (96, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("LoC/eacc2uni.txt", libcongress=True),
    "eacc2uni.txt",
    set96=True))
graphdata.gsets["cccii/koha"] = (96, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Perl/Encode-HanExtra/ucm/cccii.ucm"),
    "cccii.ucm",
    set96=True,
    skip_invalid_kuten=True))
graphdata.gsets["cccii/eacc/hk"] = (96, 3, parsers.decode_main_plane_gl(
    parsers.parse_file_format("Other/eacc-hongkonguni.txt"),
    "eacc-hongkonguni.txt",
    set96=True, 
    ignore_later_altucs=True,
    skip_invalid_kuten=True))

maxmat1 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/cccii-maxmat.txt"),
    "cccii-maxmat.txt",
    set96=True,
    mapper=deprecated_cjkci.remove_deprecated_cjkci)
maxmat2 = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/eacc-maxmat.txt"),
    "eacc-maxmat.txt",
    set96=True,
    mapper=deprecated_cjkci.remove_deprecated_cjkci)
cccii_korean_syllables = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/cccii-korean-syllables.txt"),
    "cccii-korean-syllables.txt",
    set96=True)
cccii_additional = parsers.decode_main_plane_gl(
    parsers.parse_file_format("Custom/cccii-additional-not-in-other-tables.txt"),
    "cccii-additional-not-in-other-tables.txt",
    set96=True)

# The tilde sets (~cccii and ~eacc) are used in the process of (re)generating the maxmat files.
graphdata.gsets["~cccii"] = (96, 3, parsers.fuse([
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/cccii-nonkanji.txt"),
        "cccii-nonkanji.txt",
        set96=True),
    cccii_unihan,
    # Appears as U+BF01 in some tables but this is probably a typo for U+B701, given that U+BF01
    #   has the wrong initial consonant for the CCCII codepoint range this codepoint appears in.
    ((None,) * ((79*96*96)+(46*96)+49)) + ((0xB701,),),
    # Glyphs are similar but they are completely different syllables; considering that U+C655 is in
    #   all three of KS X 1001, KPS 9566 and GB/T 12052, while U+C78F isn't (it's in KS X 1002),
    #   U+C655 is somewhat more likely to be the intended syllable. Like, 79-48-75, 79-54-87 seems
    #   to have been appended to its initial-consonant group (hence, neither follows the usual
    #   ordering within the initial-consonant group, and both are followed by only one unallocated
    #   position before the next initial-consonant group instead of two), so the fact that U+C78F
    #   follows the usual codepoint ordering is less relevant here.
    ((None,) * ((79*96*96)+(54*96)+87)) + ((0xC655,),),
    # Tables differ on whether 79-60-49 is U+D494 or U+D4CC, but both of them are in all three of
    #   KS X 1001, KPS 9566 and GB/T 12052, so it's not clear which is intended. Their glyphs are,
    #   again, similar, and the syllables differ only in the second vowel in the cluster.
    graphdata.gsets["cccii/koha"][2],
    graphdata.gsets["cccii/eacc/loc"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["cccii/eacc/hk"][2][96*99:],
    cccii_korean_syllables,
    cccii_additional,
], "CCCII-Full-Raw.json"))

graphdata.gsetflags["~cccii/eacc"] |= {"EACC:ONLY3PLANESPERLEVEL"}
graphdata.gsets["~cccii/eacc"] = (96, 3, parsers.fuse([
    graphdata.gsets["cccii/eacc/loc"][2],
    graphdata.gsets["cccii/eacc/hk"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["~cccii"][2][96*99:],
], "EACC-Full-Raw.json"))

graphdata.gsets["cccii"] = (96, 3, parsers.fuse([
    parsers.decode_main_plane_gl(
        parsers.parse_file_format("Custom/cccii-nonkanji.txt"),
        "cccii-nonkanji.txt",
        set96=True),
    maxmat1,
    cccii_unihan,
    # Appears as U+BF01 in some tables but this is probably a typo for U+B701, given that U+BF01
    #   has the wrong initial consonant for the CCCII codepoint range this codepoint appears in.
    ((None,) * ((79*96*96)+(46*96)+49)) + ((0xB701,),),
    # Glyphs are similar but they are completely different syllables; considering that U+C655 is in
    #   all three of KS X 1001, KPS 9566 and GB/T 12052, while U+C78F isn't (it's in KS X 1002),
    #   U+C655 is somewhat more likely to be the intended syllable. Like 79-48-75, 79-54-87 seems
    #   to have been appended to its initial-consonant group (hence, neither follows the usual
    #   ordering within the initial-consonant group, and both are followed by only one unallocated
    #   position before the next initial-consonant group instead of two), so the fact that U+C78F
    #   follows the usual codepoint ordering is less relevant here.
    ((None,) * ((79*96*96)+(54*96)+87)) + ((0xC655,),),
    # Tables differ on whether 79-60-49 is U+D494 or U+D4CC, but both of them are in all three of
    #   KS X 1001, KPS 9566 and GB/T 12052, so it's not clear which is intended. Their glyphs are,
    #   again, similar, and the syllables differ only in the second vowel in the cluster.
    graphdata.gsets["cccii/koha"][2],
    graphdata.gsets["cccii/eacc/loc"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["cccii/eacc/hk"][2][96*99:],
    cccii_korean_syllables,
    cccii_additional,
], "CCCII-Full4.json"))

graphdata.gsetflags["cccii/eacc"] |= {"EACC:ONLY3PLANESPERLEVEL"}
graphdata.gsets["cccii/eacc"] = (96, 3, parsers.fuse([
    maxmat2,
    graphdata.gsets["cccii/eacc/loc"][2],
    graphdata.gsets["cccii/eacc/hk"][2],
    ((None,) * (96 * 99)) + graphdata.gsets["cccii"][2][96*99:],
], "EACC-Full4.json"))

graphdata.gsets["ebcdic-traditional-chinese/1992"] = (190, 2, parsers.decode_main_plane_dbebcdic(parsers.parse_file_format("ICU/ibm-937_X110-1999.ucm"), "ibm-937_X110-1999.ucm"))
graphdata.gsets["ebcdic-traditional-chinese/1999"] = (190, 2, parsers.decode_main_plane_dbebcdic(parsers.parse_file_format("ICU/ibm-1371_X100-1999.ucm"), "ibm-1371_X100-1999.ucm"))
graphdata.gsets["ebcdic-traditional-chinese/2016"] = (190, 2, parsers.decode_main_plane_dbebcdic(parsers.parse_file_format("Other/T1K835U.ucm"), "T1K835U.ucm"))
graphdata.ebcdicdbcs["835"] = graphdata.ebcdicdbcs["937"] = graphdata.ebcdicdbcs["5033"] = "ebcdic-traditional-chinese/1992"
graphdata.ebcdicdbcs["5467"] = graphdata.ebcdicdbcs["13123"] = "ebcdic-traditional-chinese/1999"
graphdata.ebcdicdbcs["1371"] = graphdata.ebcdicdbcs["9027"] = "ebcdic-traditional-chinese/2016"
graphdata.chcpdocs["835"] = graphdata.chcpdocs["937"] = graphdata.chcpdocs["1371"] = graphdata.chcpdocs["5033"] = graphdata.chcpdocs["5467"] = graphdata.chcpdocs["9027"] = graphdata.chcpdocs["13123"] = "ebcdic"
graphdata.defgsets["937"] = ("alt646/ibmusa", "gr24613", "gl310", "gr310")
graphdata.defgsets["5033"] = ("alt646/ibmusa", "nil", "gl310", "gr310")
graphdata.defgsets["1371"] = graphdata.defgsets["5467"] = ("alt646/ibmusa", "gr1159", "gl310", "gr310")


