#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, marginally.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd

initd = {}; voweld = {}; finald = {}
# https://unicode.org/L2/L2017/17081-hangul-filler.pdf
f = open("17081-hangul-filler.txt") # pdftotext -layout 17081-hangul-filler.pdf

for i in f:
    if "“" not in i or "\u3164" not in i:
        continue
    seq = i.split("“", 1)[1].split("”")[0]
    cod = i.rsplit("U+", 1)[0].rstrip().rsplit(None, 1)[1]
    scod = ucd.normalize("NFD", cod)
    assert seq[0] == "\u3164"
    initd.setdefault(seq[1], scod[0])
    assert initd[seq[1]] == scod[0]
    voweld.setdefault(seq[2], scod[1])
    assert voweld[seq[2]] == scod[1]
    finald.setdefault(seq[3], scod[2:])
    assert finald[seq[3]] == scod[2:]

for i in range(0x3165, 0x318F):
    cod = chr(i)
    ncod = ucd.normalize("NFKC", cod)
    if "CHOSEONG" in ucd.name(ncod):
        initd.setdefault(cod, ncod)
        try:
            finald.setdefault(cod, ucd.lookup(ucd.name(ncod).replace("CHOSEONG", "JONGSEONG")))
        except KeyError:
            pass
    elif "JUNGSEONG" in ucd.name(ncod):
        voweld.setdefault(cod, ncod)
    elif "JONGSEONG" in ucd.name(ncod):
        finald.setdefault(cod, ncod)
        try:
            initd.setdefault(cod, ucd.lookup(ucd.name(ncod).replace("JONGSEONG", "CHOSEONG")))
        except KeyError:
            pass
    else:
        raise AssertionError(ucd.name(ncod))

for i in (initd, voweld, finald):
    print(end = "{")
    for j, k in i.items():
        print(ascii(j), ascii(k), sep = ": ", end = ", ")
    print("}")



