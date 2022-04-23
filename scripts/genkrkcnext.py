#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2021.

# This file is made available under the CC0 Public Domain Dedication.  To the extent possible
#   under law, the author(s) have dedicated all copyright and related and neighboring rights to
#   this file to the public domain worldwide. This file is distributed without any warranty.
#   This provision applies to this file specifically, not to mdplay as a whole.
#
# You may have received a copy of the CC0 Public Domain Dedication along with this file.
#   If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 

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

diffencode_t101chinese = {}
diffdecode_t101chinese = {}
exclencode_t101chinese = []
excldecode_t101chinese = []
encode_csic3 = {}
decode_csic3 = {}
encode_csic4 = {}
decode_csic4 = {}
encode_csic5 = {}
decode_csic5 = {}
encode_csic6 = {}
decode_csic6 = {}
encode_csic7 = {}
decode_csic7 = {}
csic_ucs_seen = {}


for pointer, (ucsgb, ucsitu) in enumerate(zip(graphdata.gsets["ir058/full"][2], graphdata.gsets["ir165"][2])):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    save_ucsgb = ucsgb
    if ucsgb and (len(ucsgb) == 1):
        ucsgb, = ucsgb
    if ucsitu and (len(ucsitu) == 1):
        ucsitu, = ucsitu
    if not ucsitu:
        if ucsgb and ucsgb not in range(0xE000, 0xF900):
            print("Cutting", hex(first), hex(second), chr(ucsgb), file=sys.stderr)
            excldecode_t101chinese.append((first, second))
            if save_ucsgb not in graphdata.gsets["ir165"][2]:
                print("  Both ways", file=sys.stderr)
                exclencode_t101chinese.append(ucsgb)
    elif (not ucsgb) or (ucsgb != ucsitu):
        diffdecode_t101chinese[(first, second)] = ucsitu
        diffencode_t101chinese[ucsitu] = (first, second)


for pointer, ucs in enumerate(graphdata.gsets["ir184"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    csic_ucs_seen[ucs] = (0x24, first, second)
    decode_csic4[(first, second)] = ucs
    encode_csic4[ucs] = (first, second)

for pointer, ucs in enumerate(graphdata.gsets["ir185"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    csic_ucs_seen[ucs] = (0x25, first, second)
    decode_csic5[(first, second)] = ucs
    encode_csic5[ucs] = (first, second)

for pointer, ucs in enumerate(graphdata.gsets["ir186"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    csic_ucs_seen[ucs] = (0x26, first, second)
    decode_csic6[(first, second)] = ucs
    encode_csic6[ucs] = (first, second)

for pointer, ucs in enumerate(graphdata.gsets["ir187"][2]):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    csic_ucs_seen[ucs] = (0x27, first, second)
    decode_csic7[(first, second)] = ucs
    encode_csic7[ucs] = (first, second)

for pointer, (ucs, ucsalt) in enumerate(zip(graphdata.gsets["ir183/full"][2], graphdata.gsets["ir183/1988plus"][2])):
    first = 0x21 + (pointer // 94)
    second = 0x21 + (pointer % 94)
    if not ucs:
        continue
    if len(ucs) == 1:
        ucs, = ucs
    if ucsalt and len(ucsalt) == 1:
        ucsalt, = ucsalt
    decode_csic3[(first, second)] = ucs
    if ucs not in csic_ucs_seen:
        encode_csic3[ucs] = (first, second)
    else:
        a, b, c = csic_ucs_seen[ucs]
        print("0x23", hex(first), hex(second), "/", hex(a), hex(b), hex(c), hex(ucs), file=sys.stderr)
    if ucsalt and (ucsalt not in csic_ucs_seen):
        encode_csic3[ucsalt] = (first, second)

print("from collections import xraydict")
print("from codecs.extradata import encode_gb7, decode_gb7")
print()
print("let encode_t101chinese = xraydict(encode_gb7, {}, {})".format(
        smartrepr(diffencode_t101chinese), exclencode_t101chinese))
print()
print("let decode_t101chinese = xraydict(decode_gb7, {}, {})".format(
        smartrepr(diffdecode_t101chinese), excldecode_t101chinese))
print()

for i in sorted(dir(), key=lambda i:(i.rsplit("_", 1)[-1], i)):
    if i[3:7] == "ode_":
        print("let {} = {}".format(i, smartrepr(globals()[i])))
        print()





