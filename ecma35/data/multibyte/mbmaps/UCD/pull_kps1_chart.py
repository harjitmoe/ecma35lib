#!/usr/bin/env python3
# -*- mode: python; charset: utf-8 -*-
# Written by HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

fs = ["Unihan_IRGSources.txt", "Unihan_OtherMappings.txt"]

maps = [None] * 65536

for f in fs:
    for line in open(f):
        if "\tkIRG_KPSource\tKP1-" in line:
            ucs, kps1 = line.strip().split("\tkIRG_KPSource\tKP1-")
        elif "\tkKPS1\t" in line:
            ucs, kps1 = line.strip().split("\tkKPS1\t")
        else:
            continue
        assert ucs[:2] == "U+"
        ucs = int(ucs[2:], 16)
        kps1 = int(kps1, 16)
        maps[kps1] = ucs

print("<!DOCTYPE html>")
print("<style>table, tr, th, td { border-collapse: collapse; border: 1px solid black; }</style>")
print("<table>")
print("<thead><tr>")
print("<th>-</th>")
for xcell in range(256):
    print("<th>{:02X}</th>".format(xcell))
print("</tr></thead><tbody>")
for xrow in range(256):
    print("<tr>")
    print("<th>{:02X}</th>".format(xrow))
    for xcell in range(256):
        pointer = (xrow * 256) + xcell
        val = maps[pointer]
        print("<td>{}</td>".format(chr(val) if val else ""))
    print("</tr>")
print("</tbody></table>")
        



