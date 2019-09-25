#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

stex = """         "x{:02d}": (96, 1, ("""
for i in range(1, 17):
    if i == 12:
        continue
    cod = "iso-8859-{}".format(i)
    print(end = stex.format(i))
    for i in range(96):
        if i and (not i % 8):
            print()
            print(end = "                         ")
        ucs = ord(bytes([i + 0xA0]).decode(cod, errors="replace"))
        print(end = ("0x{:04X}, ".format(ucs) if ucs != 0xFFFD else "None, "))
    print("\b\b)),")
