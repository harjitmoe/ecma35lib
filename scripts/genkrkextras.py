#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2021, 2022.

# This file is made available under the CC0 Public Domain Dedication.  To the extent possible
#   under law, the author(s) have dedicated all copyright and related and neighboring rights to
#   this file to the public domain worldwide. This file is distributed without any warranty.
#   This provision applies to this file specifically, not to mdplay as a whole.
#
# You may have received a copy of the CC0 Public Domain Dedication along with this file.
#   If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 

# NOTE: extradata.krk is not the verbatim output of this file: it has some additions from other
#   sources and some redundency-removal via tools/codectools/extradatadeltas.krk

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data import graphdata

def smartrepr(data):
    if isinstance(data, dict):
        out = ""
        scratch = "{"
        for i in data.keys():
            scratch += repr(i) + ": " + repr(data[i]) + ","
            if len(scratch) > 4000:
                out += scratch + "\n"
                scratch = ""
            else:
                scratch += " "
        return out + scratch + "}"
    elif isinstance(data, list):
        out = ""
        scratch = "["
        for i in data:
            scratch += repr(i) + ","
            if len(scratch) > 4000:
                out += scratch + "\n"
                scratch = ""
            else:
                scratch += " "
        return out + scratch + "]"
    return repr(data)

encode_lat1supp = {}
decode_lat1supp = {}
encode_greksupp = {}
decode_greksupp = {}
encode_jis78 = {}
decode_jis78 = {}
encode_jis90p2 = {}
decode_jis90p2 = {}
encode_jis00 = {}
decode_jis00 = {}
encode_jis00p2 = {}
decode_jis00p2 = {}
encode_jis04 = {}
decode_jis04 = {}
encode_gb7 = {}
decode_gb7 = {}
encode_ksc7 = {}
decode_ksc7 = {}
encode_jis7katakana = {}
encode_csic1 = {}
decode_csic1 = {}
encode_csic2 = {}
decode_csic2 = {}


for pointer, ucs in enumerate(graphdata.gsets["ir100"][2]):
    byte = 0x20 + pointer
    assert isinstance(ucs, int)
    decode_lat1supp[byte] = ucs
    encode_lat1supp[ucs] = byte


for pointer, ucs in enumerate(graphdata.gsets["ir227"][2]):
    byte = 0x20 + pointer
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_greksupp[byte] = ucs
    encode_greksupp[ucs] = byte


for pointer, (nec, ibm) in enumerate(zip(graphdata.gsets["ir042/nec"][2], graphdata.gsets["ir042/ibm"][2])):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ibm and not nec:
        continue
    elif not ibm:
        go_with = nec
    elif not nec:
        if first == 0x74 and second == 0x26:
            go_with = (0x7199,)
        else:
            go_with = ibm
    elif first in (0x21, 0x22):
        go_with = ibm
    else:
        go_with = nec
    decode_only = False
    if go_with[-1] == 0xF87F:
        go_with = go_with[:-1]
        decode_only = True
    if first == 0x28:
        decode_only = True
    if len(go_with) == 1:
        go_with, = go_with
    decode_jis78[(first, second)] = go_with
    if not decode_only:
        encode_jis78[go_with] = (first, second)


for pointer, ucs in enumerate(graphdata.gsets["ir159/icueuc"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_jis90p2[(first, second)] = ucs
    encode_jis90p2[ucs] = (first, second)


for pointer, ucs in enumerate(graphdata.gsets["ir228"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_jis00[(first, second)] = ucs
    encode_jis00[ucs] = (first, second)


for pointer, ucs in enumerate(graphdata.gsets["ir229"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_jis00p2[(first, second)] = ucs
    encode_jis00p2[ucs] = (first, second)


for pointer, ucs in enumerate(graphdata.gsets["ir233"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_jis04[(first, second)] = ucs
    encode_jis04[ucs] = (first, second)


for pointer, ucs in enumerate(graphdata.gsets["ir058/full"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_gb7[(first, second)] = ucs
    encode_gb7[ucs] = (first, second)


for pointer, ucs in enumerate(graphdata.gsets["ir149/2002"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_ksc7[(first, second)] = ucs
    encode_ksc7[ucs] = (first, second)


for pointer, (ucs, ucsms) in enumerate(zip(graphdata.gsets["ir171/full"][2], graphdata.gsets["ir171/ms"][2])):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    decode_only = False
    if (0x3040 <= ucs[0] <= 0x30FF) and ucs in graphdata.gsets["ir058/full"][2]:
        # Encode kana to GB 2312 (as explicitly recommended by RFC 1922) where possible.
        # Kana hadn't yet been added to CNS 11643 at the time RFC 1922 was written and cannot be
        #   assumed to be supported by all ISO-2022-CN implementations.
        decode_only = True
    if len(ucs) == 1:
        ucs, = ucs
    decode_csic1[(first, second)] = ucs
    if not decode_only:
        encode_csic1[ucs] = (first, second)
        if ucsms and ucsms not in graphdata.gsets["ir171"][2]:
            if len(ucsms) == 1:
                ucsms, = ucsms
            encode_csic1[ucsms] = (first, second)
            decode_csic1[(first, second)] = ucsms

for pointer, ucs in enumerate(graphdata.gsets["ir172"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    decode_csic2[(first, second)] = ucs
    encode_csic2[ucs] = (first, second)


for i in range(63): encode_jis7katakana[0xFF61 + i] = 0x21 + i


for i in sorted(dir(), key=lambda i:(i.rsplit("_", 1)[-1], i)):
    if i[3:7] == "ode_":
        print("let {} = {}".format(i, smartrepr(globals()[i])))
        print()





