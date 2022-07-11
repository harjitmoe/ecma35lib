#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2022.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, itertools
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data import graphdata

main_plane = graphdata.gsets["ir149/mac"][2]
main_plane_nom = graphdata.gsets["ir149/mac-unicode3_2"][2]
side_plane = graphdata.gsets["~mac-elex-extras-semipragmatic"][2]
side_plane_nom = graphdata.gsets["mac-elex-extras-unicode3_2"][2]
side_plane_fontnom = graphdata.gsets["mac-elex-extras-adobe"][2]

collapses_encoder = {}
collapses_decoder = {}

firsts = set(itertools.chain((i[0] for i in main_plane if i and len(i) == 1), (i[0] for i in side_plane if i and len(i) == 1)))

firsts |= set(range(128))
firsts |= {0x00A0, 0x20A9, 0x00A9} # 0x80, 0x81, 0x83

firsts_nom = set(itertools.chain((i[0] for i in main_plane_nom if i and len(i) == 1), (i[0] for i in side_plane_nom if i and len(i) == 1), (i[0] for i in side_plane_fontnom if i and len(i) == 1)))

losses = firsts_nom - firsts

for i, j in zip(itertools.chain(main_plane, side_plane, side_plane), itertools.chain(main_plane_nom, side_plane_nom, side_plane_fontnom)):
    if j and len(j) == 1 and j[0] in losses:
        collapses_encoder[j] = i

ultra = firsts | firsts_nom

numbers = "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿"
minuscules = "⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵"
capitals = "🄐🄑🄒🄓🄔🄕🄖🄗🄘🄙🄚🄛🄜🄝🄞🄟🄠🄡🄢🄣🄤🄥🄦🄧🄨🄩"

for i in itertools.chain(main_plane, side_plane):
    if not i:
        continue
    elif 0xF870 <= i[-1] <= 0xF87F:
        collapses_decoder[i] = i[:-1]
    elif 0xF860 <= i[0] <= 0xF86F:
        strep = "".join(chr(j) for j in i[1:])
        crux = strep.strip("[()].")
        if not crux.strip("0123456789"):
            collapses_decoder[i] = (ord(numbers[int(crux, 10)]),)
        elif len(crux) == 1 and crux in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            collapses_decoder[i] = (ord(capitals[ord(crux) - ord("A")]),)
        elif len(crux) == 1 and crux in "abcdefghijklmnopqrstuvwxyz":
            collapses_decoder[i] = (ord(minuscules[ord(crux) - ord("a")]),)
        else:
            collapses_decoder[i] = i[1:]

decoder_map = {}
encoder_map = {}
temp_map = {}

# 0x41-7D, 0x81-A0, (0xFF)

def to_code(planeno, row, cell):
    if planeno == 1:
        return (0xA0 + row, 0xA0 + cell)
    elif planeno == 2:
        trail = 0x40 + cell
        if trail > 0x7D:
            trail += 3
        if trail == 0xA1:
            trail = 0xFF
        return (0xA0 + row, trail)
    else:
        raise ValueError(f"planeno must be 1 or 2, got {planeno}")

for planeno, plane in [(1, main_plane), (2, side_plane)]:
    for index, mapping in enumerate(plane):
        row = (index // 94) + 1
        cell = (index % 94) + 1
        coded = to_code(planeno, row, cell)
        if mapping in collapses_decoder:
            decoder_map[coded] = collapses_decoder[mapping]
            temp_map[mapping] = coded
        else:
            decoder_map[coded] = mapping
            encoder_map[mapping] = coded

collapses_encoder[(0xF805, 0x20DE)] = (0x1F4A0, 0x20DE)
collapses_encoder[(0xF806, 0x20DF)] = (0x26CB, 0x20DF)

for i in collapses_encoder:
    if collapses_encoder[i] not in encoder_map:
        encoder_map[i] = temp_map[collapses_encoder[i]]
    else:
        encoder_map[i] = encoder_map[collapses_encoder[i]]

allucs = sorted(set(i for i in itertools.chain(encoder_map.keys(), decoder_map.values()) if i))
for ucs in allucs:
    alr = set()
    if ucs in encoder_map:
        kind = "|0" if decoder_map[encoder_map[ucs]] == ucs else "|1"
        print("".join(f"<U{i:04X}>" for i in ucs), "".join(f"\\x{j:02X}" for j in encoder_map[ucs]), kind)
        alr.add(encoder_map[ucs])
    dmks = set(i for i, j in decoder_map.items() if j == ucs) - alr
    if dmks:
        for dmk in sorted(dmks):
            print("".join(f"<U{i:04X}>" for i in ucs), "".join(f"\\x{j:02X}" for j in dmk), "|3")


