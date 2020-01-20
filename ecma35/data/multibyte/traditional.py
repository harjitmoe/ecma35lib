#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, ast, sys
from ecma35.data import graphdata
from ecma35.data.multibyte import mbmapparsers as parsers

# CNS 11643
graphdata.gsets["ir171"] = cns1 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=1))
graphdata.gsets["ir172"] = cns2 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=2))
# ISO-IR numbers jump by ten here (between the Big-5 and non-Big-5 planes).
graphdata.gsets["ir183"] = cns3 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=3))
graphdata.gsets["ir184"] = cns4 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=4))
graphdata.gsets["ir185"] = cns5 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=5))
graphdata.gsets["ir186"] = cns6 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=6))
graphdata.gsets["ir187"] = cns7 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=7))
# Plane 7 is the last one to be registered with ISO-IR. Plane 8 is unused.
graphdata.gsets["cns-9"] = cns9 = (94, 2, parsers.read_main_plane("cns-11643-1992.ucm", plane=9))
# The entirety does also exist as an unregistered 94^n set, used by EUC-TW:
graphdata.gsets["cns-eucg2"] = euctw_g2 = (94, 3, parsers.read_main_plane("cns-11643-1992.ucm"))

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
            _temp[newpointer] = int(ucs[2:], 16)
        else:
            while len(_temp) < newpointer:
                _temp.append(None)
            _temp.append(int(ucs[2:], 16))
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
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
big5_to_cns1 = read_big5_rangemap("rfc1922.txt", 1)
big5_to_cns1.update(read_big5_rangemap("rfc1922.txt", 2))
big5_to_cns2 = read_big5_rangemap("rfc1922.txt", 3, plane=2)
big5_to_cns1[0xC94A] = big5_to_cns2[0xC94A][-2:] # Exceptional: level 2 mapped to plane 1
del big5_to_cns2[0xC94A]

graphdata.gsets["hkscs"] = hkscs_extras = (94, 2, read_big5extras("index-big5.txt"))
graphdata.gsets["etenexts"] = eten_extras = (94, 2, 
    ((None,) * (32 * 188)) + hkscs_extras[2][(32 * 188):])
graphdata.gsets["ms950exts"] = ms_big5_extras = (94, 2, read_big5extras("CP950.TXT"))
graphdata.gsets["utcbig5exts"] = utc_big5_extras = (94, 2, read_big5extras("BIG5.TXT"))
graphdata.gsets["ms950utcexts"] = msutc_big5_extras = (94, 2,
    utc_big5_extras[2] + ms_big5_extras[2][len(utc_big5_extras[2]):])

def show(x):
    for (n, i) in enumerate(x[2]):
        if not (n % 47):
            print()
            print((n // 188) + 1, (n // 47) % 4, sep = ":", end = " ")
        print(end = chr(i) if i is not None else "\uFFFD")
    print()







