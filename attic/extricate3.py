#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

stex = """         "nnn": (94, 2, ("""
cod = "euc-jp"
print(end = stex)
for i in range(94**2):
    if i and (not i % 8):
        print()
        print(end = "                         ")
    i1, i2 = (i // 94), (i % 94)
    ucs = ord(bytes([0x8F, i1 + 0xA1, i2 + 0xA1]).decode(cod, errors="replace")[0])
    print(end = ("0x{:04X}, ".format(ucs) if ucs != 0xFFFD else "None, "))
print("\b\b)),")
