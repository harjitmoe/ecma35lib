#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, ast, sys
from ecma35.data import graphdata
from ecma35.data.multibyte import mbmapparsers as parsers

def read_big5_rangemap(fil, appendix, *, plane=None):
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

# Comments: the Kana correspondance of RFC 1922 matches the Big5 Kana encoding in the WHATWG Big5
# mappings, but not the Big5 Kana encoding in the Python Big5 codec.
# Since there exist at least two ways of encoding kana in the same private range of Big5, this is
# not vastly surprising.
big5_to_cns1 = read_big5_rangemap("rfc1922.txt", 1)
big5_to_cns1.update(read_big5_rangemap("rfc1922.txt", 2))
big5_to_cns2 = read_big5_rangemap("rfc1922.txt", 3, plane=2)
big5_to_cns1[0xC94A] = big5_to_cns2[0xC94A][-2:] # Exceptional: level 2 mapped to plane 1
del big5_to_cns2[0xC94A]
big5_to_cns1.update(read_big5_rangemap("rfc1922.txt", 4))
big5_to_cns1.update(read_big5_rangemap("rfc1922.txt", 5))
big5_to_cns2.update(read_big5_rangemap("rfc1922.txt", 6, plane=3))
big5_to_cns2.update(read_big5_rangemap("rfc1922.txt", 7, plane=4))
big5_to_guobiao_fallback = read_big5_rangemap("rfc1922.txt", 8)






