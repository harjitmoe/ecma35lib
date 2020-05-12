#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Detail regarding Apple-compatible versus up-to-date mappings

import os, json, shutil
from ecma35.data import gccdata
from ecma35.data.multibyte import mbmapparsers as parsers

applesinglehints = {
    # Some notes: these should be to Unicode characters postdating the mapping data.
    # For instance, many of the arrows mapped to here are from Unicode 7.0.
    #
    # Heavy white barbed arrows:
    (0x2190, 0xF870): (0x1F880, 0xF87A),
    (0x2191, 0xF870): (0x1F881, 0xF87A),
    (0x2192, 0xF870): (0x1F882, 0xF87A),
    (0x2193, 0xF870): (0x1F883, 0xF87A),
    #
    # U+2190+F871 etc are drafting point arrows like U+297B (no full set exists)
    # U+2190+F872 etc are teardrop-stroked arrows
    #
    # Bold barbed arrows (Zapf U+2794):
    (0x2190, 0xF873): (0x1F870,),
    (0x2191, 0xF873): (0x1F871,),
    (0x2192, 0xF873): (0x1F872,),
    (0x2193, 0xF873): (0x1F873,),
    #
    # White kite-headed arrows:
    (0x2190, 0xF874): (0x1F878, 0xF87A),
    (0x2191, 0xF874): (0x1F879, 0xF87A),
    (0x2192, 0xF874): (0x1F87A, 0xF87A),
    (0x2193, 0xF874): (0x1F87B, 0xF87A),
    #
    # U+2190+F875 etc are white rounded-stroke arrows
    #
    # Bold kite-headed arrows:
    (0x2190, 0xF878): (0x1F878, 0xF87F),
    (0x2191, 0xF878): (0x1F879, 0xF87F),
    (0x2192, 0xF878): (0x1F87A, 0xF87F),
    (0x2193, 0xF878): (0x1F87B, 0xF87F),
    #
    # Heavy barbed arrows:
    (0x2190, 0xF879): (0x1F880,),
    (0x2191, 0xF879): (0x1F881,),
    (0x2192, 0xF879): (0x1F882,),
    (0x2193, 0xF879): (0x1F883,),
    #
    # White barbed arrows:
    (0x2190, 0xF87A): (0x1F870, 0xF87A),
    (0x2191, 0xF87A): (0x1F871, 0xF87A),
    (0x2192, 0xF87A): (0x1F872, 0xF87A),
    (0x2193, 0xF87A): (0x1F873, 0xF87A),
    #
    # U+2190+F87B etc are light barbed arrows
    #
    # Light kite arrows:
    (0x2190, 0xF87C): (0x1F850,),
    (0x2191, 0xF87C): (0x1F851,),
    (0x2192, 0xF87C): (0x1F852,),
    (0x2193, 0xF87C): (0x1F853,),
    #
    # U+2190+F87F etc are black rounded-stroke arrows like U+279C (no full set)
    # U+21E6+F870 is a bold black arrow with detached kite head and stem widening toward head
    # U+21E6+F874 is a bold white arrow with triangular head and stem narrowing away from head
    #
    # Very heavy arrows:
    (0x21e6, 0xf875): (0x1F844,),
    (0x21e7, 0xf875): (0x1F845,),
    (0x21e8, 0xf875): (0x1F846,),
    (0x21e9, 0xf875): (0x1F847,),
    #
    # U+21E6+F879 is a white very heavy arrow
    (0x21e6, 0xf879): (0x1F844, 0xF87A),
    (0x21e7, 0xf879): (0x1F845, 0xF87A),
    (0x21e8, 0xf879): (0x1F846, 0xF87A),
    (0x21e9, 0xf879): (0x1F847, 0xF87A),
    #
    # Bold triangle-headed arrows (Zapf U+27A1):
    # Note: MacKorean (HangulTalk) uses U+27A1 to map the right arrow.
    #   MacJapanese (KanjiTalk 7) doen't by default (so, map it to U+2B95).
    #   Don't map the sequence to U+27A1: it already existed (v1.x).
    (0x21e6, 0xf87a): (0x2b05,), # ⬅
    (0x21e7, 0xf87a): (0x2b06,), # ⬆
    (0x21e8, 0xf87a): (0x2b95,), # ⮕
    (0x21e9, 0xf87a): (0x2b07,), # ⬇
    #
    # Large-headed triangle arrows (Zapf U+279E):
    (0x21e6, 0xf87b): (0x1F808,),
    (0x21e7, 0xf87b): (0x1F809,),
    (0x21e8, 0xf87b): (0x1F80A,),
    (0x21e9, 0xf87b): (0x1F80B,),
    #
    # U+21E6+F87C is a white large-headed triangle arrow
    (0x21e6, 0xf87C): (0x1F808, 0xF87A),
    (0x21e7, 0xf87C): (0x1F809, 0xF87A),
    (0x21e8, 0xf87C): (0x1F80A, 0xF87A),
    (0x21e9, 0xf87C): (0x1F80B, 0xF87A),
    #
    # U+21E6+F87F is a bold triangle-headed arrow with detached head
    #
    # Right-angled bendy arrows (minus the five with standard mappings already):
    (0x21BB, 0xF87B): (0x2B11,), # Left then up
    (0x2934, 0xF87F): (0x2B0F,), # Right then up
    (0x2939, 0xF87F): (0x2B10,), # Left then down
    #
    # Normal bendy arrows (minus the five with standard mappings already):
    (0x21B0, 0xF87F): (0x2BAA, 0xF87F), # Up then left
    (0x21B1, 0xF87F): (0x2BAB, 0xF87F), # Up then right
    (0x21BB, 0xF87F): (0x2BAC, 0xF87F), # Left then up
    #
    # Triangle-headed bendy arrows
    (0x2936, 0xF87C): (0x2BA8,), # Down then left
    (0x2937, 0xF87C): (0x2BA9,), # Down then right
    (0x21B0, 0xF87C): (0x2BAA,), # Up then left
    (0x21B1, 0xF87C): (0x2BAB,), # Up then right
    (0x21BB, 0xF87C): (0x2BAC,), # Left then up
    (0x2934, 0xF87C): (0x2BAD,), # Right then up
    (0x2939, 0xF87C): (0x2BAE,), # Left then down
    (0x2935, 0xF87C): (0x2BAF,), # Right then down
    #
    # White bendy arrows:
    (0x2936, 0xF87A): (0x2BB0,), # Down then left
    (0x2937, 0xF87A): (0x2BB1,), # Down then right
    (0x21B0, 0xF87A): (0x2BB2,), # Up then left
    (0x21B1, 0xF87A): (0x2BB3,), # Up then right
    (0x21BB, 0xF87A): (0x2BB4,), # Left then up 
    (0x2934, 0xF87A): (0x2BB5,), # Right then up
    (0x2939, 0xF87A): (0x2BB6,), # Left then down
    (0x2935, 0xF87A): (0x2BB7,), # Right then down
    #
    # White arrows in black circle (Zapf U+27B2):
    (0x21e6, 0x20DD): (0x2B88,),
    (0x21e7, 0x20DD): (0x2B89,),
    (0x21e8, 0x20DD): (0x2B8A,),
    (0x21e9, 0x20DD): (0x2B8B,),
    #
    # Vertical forms not present when mappings written, but later added from GB 18030:
    (0x2026, 0xf87e): (0xfe19,), # Ellipsis
    (0x3001, 0xf87e): (0xfe11,), # Comma
    (0x3002, 0xf87e): (0xfe12,), # Full stop
    (0xff3b, 0xf87e): (0xfe47,), # Opening hard bracket
    (0xff3d, 0xf87e): (0xfe48,), # Closing hard bracket
    #
    # Keycap numbers 1 through 9:
    (0x0031, 0x20DE, 0xF87B): (0x0031, 0x20E3),
    (0x0032, 0x20DE, 0xF87B): (0x0032, 0x20E3),
    (0x0033, 0x20DE, 0xF87B): (0x0033, 0x20E3),
    (0x0034, 0x20DE, 0xF87B): (0x0034, 0x20E3),
    (0x0035, 0x20DE, 0xF87B): (0x0035, 0x20E3),
    (0x0036, 0x20DE, 0xF87B): (0x0036, 0x20E3),
    (0x0037, 0x20DE, 0xF87B): (0x0037, 0x20E3),
    (0x0038, 0x20DE, 0xF87B): (0x0038, 0x20E3),
    (0x0039, 0x20DE, 0xF87B): (0x0039, 0x20E3),
    #
    # Other MacKorean hint sequences which have since gotten unique codepoints:
    (0x534D, 0xF87F): (0x0FD6,), # Manji as a non-kanji
    (0x2394, 0xF876): (0x2B21,), # White hexagon
    # Some direct PUA mappings used by MacKorean but no longer needed
    (0xF80A,): (0x1F668,), # "Two interwoven eye shapes" (basically a variant quilt square)
    (0xF80B,): (0x1F66A,), # This one really close (narrow-leaf four-petal florette)
    (0xF80B, 0xF87F): (0x1F66B,), # Less so, but may as well commit to it
    (0xF83D,): (0x269C,), # Fleur de lis
    (0xF83D, 0xF87F): (0x269C, 0xF87F), # Alternate fleur de lis
    (0xF842,): (0x2B5A,), # Downward wave arrow
    (0xF844,): (0x2B9C,), # Leftward arrowhead
    (0xF84A,): (0x1F66C,), # "Arrow with bow" but basically a typographical rocket tbh (leftward)
    (0xF84B,): (0x1F66E,), # "Arrow with bow" but basically a typographical rocket tbh (rightward)
    (0xF84C,): (0x2B20,), # White pentagon
    (0xF84D,): (0x23E2,), # Trapezoid
}
# Not sure where to put this observation, but MacKorean's U+25B4+20E4 is basically DPRK's mountain ahead.

def ahmap(pointer, ucs):
    if ucs in applesinglehints:
        return applesinglehints[ucs]
    elif 0xf860 <= ucs[0] < 0xf870:
        ucss = "".join(chr(i) for i in ucs)
        if ucs[0] < 0xF863:
            # Ordinary composition
            return tuple(ord(i) for i in gccdata.gcc_sequences.get(ucss[1:], ucss))
        else:
            # Extra-ordinary composition
            return tuple(ord(i) for i in gccdata.gcc_sequences.get(ucss, ucss))
    return ucs

def read_untracked_mbfile(reader, fn, cachefn, shippedfn, **kwargs):
    if os.path.exists(os.path.join(parsers.directory, fn)):
        data = reader(fn, **kwargs)
        try:
            if os.path.exists(os.path.join(parsers.directory, shippedfn)):
                os.unlink(os.path.join(parsers.directory, shippedfn))
            shutil.copy(os.path.join(parsers.cachedirectory, cachefn),
                        os.path.join(parsers.directory, shippedfn))
        except EnvironmentError:
            pass
    else:
        data = tuple(tuple(i) if i is not None else None for i in json.load(
                     open(os.path.join(parsers.directory, shippedfn), "r")))
    return data




