#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Detail regarding Apple-compatible versus up-to-date mappings

import os, json, shutil
import unicodedata as ucd
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
    # This is a hints-to-hints without any newer codepoints, purely for convenience.
    (0x2192, 0xF875): (0x279C, 0xF87A),
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
    #
    # Bold white arrow with almost triangular head and stem "pointing into" the page:
    (0x21e6, 0xf874): (0x1F8A6,),
    (0x21e8, 0xf874): (0x1F8A7,),
    #
    # Very heavy arrows:
    (0x21e6, 0xf875): (0x1F844,),
    (0x21e7, 0xf875): (0x1F845,),
    (0x21e8, 0xf875): (0x1F846,),
    (0x21e9, 0xf875): (0x1F847,),
    #
    # White very heavy arrows:
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
    # White large-headed triangle arrow:
    (0x21e6, 0xf87C): (0x1F808, 0xF87A),
    (0x21e7, 0xf87C): (0x1F809, 0xF87A),
    (0x21e8, 0xf87C): (0x1F80A, 0xF87A),
    (0x21e9, 0xf87C): (0x1F80B, 0xF87A),
    #
    # Bold triangle-headed arrow with detached head:
    (0x21e6, 0xf87F): (0x1F780, 0x1F89C),
    (0x21e8, 0xf87F): (0x1F89C, 0x1F782),
    #
    # White arrows in black circle (Zapf U+27B2):
    (0x21e6, 0x20DD): (0x2B88,),
    (0x21e7, 0x20DD): (0x2B89,),
    (0x21e8, 0x20DD): (0x2B8A,),
    (0x21e9, 0x20DD): (0x2B8B,),
    #
    # White arrows in black square (_de facto_ used in emoji variation for these codepoints):
    (0x21e6, 0x20DE): (0x2b05, 0xFE0F),
    (0x21e7, 0x20DE): (0x2b06, 0xFE0F),
    (0x21e8, 0x20DE): (0x27a1, 0xFE0F),
    (0x21e9, 0x20DE): (0x2b07, 0xFE0F),
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
    # Typographical rockets (mapped direct to PUA by Apple):
    (0xF848,): (0x1F66C, 0xF87A), # White leftward heavy rocket
    (0xF849,): (0x1F66E, 0xF87A), # White rightward heavy rocket
    (0xF84A,): (0x1F66C,), # Leftward lozenge-tipped rocket
    (0xF84B,): (0x1F66E,), # Rightward lozenge-tipped rocket
    #
    # Broadcast (ripple) arrows (not exactly speakers but close enough darnit)
    (0xF846,): (0x1F56A, 0xF87F), # Pointing and broadcasting to left
    (0xF847,): (0x1F50A, 0xF87F), # Pointing and broadcasting to right
    #
    # ==== NON-ARROWS: ====
    #
    # Kludgy unrenderable combining sequences with properly defined alternatives:
    (0x25B3, 0x20DD): (0x1F7D5,), # White triangle in white circle
    (0x25C7, 0x20DE): (0x26CB,), # Diamond in square (added eventually from ARIB)
    (0x25C7, 0x20DF): (0x1F79C,), # Two-ringed diamond target
    (0x25C7, 0x20DF, 0x20DF): (0x1F79C, 0xF87F), # Three-ringed diamond target
    (0x25C9, 0x20DD): (0x1F78B,), # Circular target (black bullseye)
    (0x25CE, 0x20DD): (0x1F78B, 0xF87F), # Circular target (white bullseye)
    (0x29C8, 0x20DE): (0x1F796,), # Square target
    # The group mark does now exist, although it's a recent (v10) addition:
    (0x2261, 0x20D2): (0x2BD2,), # Group mark
    #
    # MacKorean hint sequences which have since gotten unique representations:
    (0x2394, 0xF876): (0x2B21,),  # White hexagon
    (0x25C8, 0xF87F): (0x1F7A0,), # Outlined black lozenge
    (0x25EF, 0xF87C): (0x1F785,), # Medium-bold white circle
    (0x2610, 0xF87C): (0x1F78F,), # Medium-bold white square
    (0x2610, 0xF87F): (0x2B1A,),  # Dotted square
    (0x534D, 0xF87F): (0x0FD6,),  # Manji as a non-kanji
    (0xFF0A, 0xF87F): (0x3000, 0x20F0), # High asterisk
    (0x2206, 0xF87F): (0x1D71F,), # Medium-bold oblique capital delta
    #
    # Avoid variation hints on the alternate versions of manicules by mapping to
    #   backhand (even though they are usually just shown as bigger versions):
    (0x261C, 0xF87F): (0x1F448,),  # White hexagon
    (0x261D, 0xF87F): (0x1F446,), # Outlined black lozenge
    (0x261E, 0xF87F): (0x1F449,), # Medium-bold white circle
    (0x261F, 0xF87F): (0x1F447,), # Medium-bold white square
    #
    # Special cases
    # Record mark; combining sequence does not render, U+29E7 was already in v3.2.
    (0x3D, 0x20D2): (0x29E7,), 
    # White florette: 0xA67B corresponds to Adobe-Japan1 CID-12228, which maps
    #   to U+2740. Apple maps it to U+273F+F87A since 0xA699 is already mapped to 
    #   U+2740.
    (0x273F, 0xF87A): (0x2740, 0xF87F),
    # Telephone dial. None of the four encoded variants of the ☏ are at all close,
    #   but U+260F is the most likely of the four to display a dial (U+1F57E and
    #   U+1F57F are expressly keyed, while U+260E is often displayed as a keyed
    #   variant).
    (0xF807,): (0x260F, 0xF87F),
    #
    # Some direct PUA mappings used by MacKorean but no longer needed
    (0xF80A,): (0x1F668,), # "Two interwoven eye shapes" (basically a variant quilt square)
    (0xF80B,): (0x1F66A,), # This one really close (narrow-leaf four-petal florette)
    (0xF80B, 0xF87F): (0x1F66B,), # Less so, but may as well commit to it
    (0xF83D,): (0x269C,), # Fleur de lis
    (0xF83D, 0xF87F): (0x269C, 0xF87F), # Alternate fleur de lis
    (0xF842,): (0x2B5A,), # Downward wave arrow (not exactly, but better than PUA)
    (0xF844,): (0x2B9C,), # Leftward arrowhead
    (0xF84C,): (0x2B20,), # White pentagon
    (0xF84D,): (0x23E2,), # Trapezoid
    #
    # Adobe PUA assignments. Apple originally inherited these, though it mostly switched to hints.
    # Hence, it is appropriate to treat these in the same PUA processor.
    # Mapping to the hints alternatives or to standard, as appropriate:
    (0xF8E6,): (0x23D0,), # Vertical arrow extender
    (0xF8E7,): (0x23AF,), # Horizontal arrow extender
    (0xF6DA,): (0x00AE,), # Registered Trademark, Roman
    (0xF6D9,): (0x00A9,), # Copyright, Roman
    (0xF6DB,): (0x2212,), # Trademark, Roman
    (0xF8E8,): (0x00AE, 0xF87F), # Registered Trademark, Gothic
    (0xF8E9,): (0x00A9, 0xF87F), # Copyright, Gothic
    (0xF8EA,): (0x2212, 0xF87F), # Trademark, Gothic
    (0xF8EB,): (0x239B,), # (1
    (0xF8EC,): (0x239C,), # (2
    (0xF8ED,): (0x239D,), # (3
    (0xF8EE,): (0x23A1,), # [1
    (0xF8EF,): (0x23A2,), # [2
    (0xF8F0,): (0x23A3,), # [3
    (0xF8F1,): (0x23A7,), # {1
    (0xF8F2,): (0x23A8,), # {2
    (0xF8F3,): (0x23A9,), # {3
    (0xF8F4,): (0x23AA,), # Brace extender
    (0xF8F5,): (0x23AE,), # Integral extender
    (0xF8F6,): (0x239E,), # )1
    (0xF8F7,): (0x239F,), # )2
    (0xF8F8,): (0x23A0,), # )3
    (0xF8F9,): (0x23A4,), # ]1
    (0xF8FA,): (0x23A5,), # ]2
    (0xF8FB,): (0x23A6,), # ]3
    (0xF8FC,): (0x23AB,), # }1
    (0xF8FD,): (0x23AC,), # }2
    (0xF8FE,): (0x23AD,), # }3
}
# Not sure where to put this observation, but MacKorean's U+25B4+20E4 is basically DPRK's mountain ahead.
#
# MacKorean characters in Nanum Gothic:
#   0xA141 glyph8191
#   (then increments by 1 for every non-unused character, including those
#    overlapping the main plane - last is glyph9329)
#
# Adobe-Japan1 mappings of some of the MacKorean 0xA6xx dingbat characters:
# 0xA656 is CID-12242 (Apple =U+25A0+20DF)
# 0xA657 is CID-12244 (Apple =U+25C7+20DF, HarJIT =U+1F79C)
# 0xA658 is CID-12243 (Apple =PUA+F805)
# 0xA659 is CID-12245 (Apple =U+25A1+20DF)
# 0xA65A is CID-12261 (Apple =U+2039)
# 0xA65B is CID-12262 (Apple =U+203A)
# 0xA65C is CID-12265 (Apple =U+00AB)
# 0xA65D is CID-12266 (Apple =U+00BB)
# 0xA660 is CID-12246 (Apple =PUA+F806+20DF)
# 0xA662 is CID-12233 (Apple =U+25C7+20DE)
# 0xA663 is CID-12231 (Apple =PUA+F806)
# 0xA664 is CID-12232 (Apple =U+29C8)
# 0xA665 is CID-12230 (Apple =U+25C6+20DE)
# 0xA666 is CID-12234 (Apple =PUA+F805+20DE)
# 0xA667 is CID-12235 (Apple =U+29C8+20DE, HarJIT =U+1F796)
# 0xA66C is CID-12241 (Adobe =U+271A, Apple =U+271A)
# 0xA672 is CID-12260 (Apple =U+2723, --a poor match tbh mais shouganai)
# 0xA673 is CID-12259 (Adobe =U+2756, Apple =U+2756)
# 0xA679 is CID-12258 (Apple =U+2723+F87A, --F87A is PUA, U+2723 is still a poor match)
# 0xA67A is CID-12257 (Apple =U+2756+F87A, --F87A is PUA)
# 0xA67B is CID-12228 (Adobe =U+2740, Apple =U+273F+F87A, --F87A is PUA and Apple uses U+2740 for 0xA699)
# 0xA67C is CID-12229 (Adobe =U+273F, Apple =U+273F)
# 0xA68F is CID-12220 (Apple =PUA+F808)

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
    elif (len(ucs) == 2) and ucd.name(chr(ucs[0]), None) and (ucs[1] == 0x20DE):
        try:
            return (ord(ucd.lookup("SQUARED " + ucd.name(chr(ucs[0])))), )
        except KeyError:
            return ucs
    return ucs

def print_hints_to_html5(i, outfile, *, lang="ja"):
    sequence_inverse = sequence_big = False
    if i[0] >= 0xF0000:
        print("<span class='codepicture spua' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i)
    elif 0xF860 <= i[0] < 0xF865 and len(i) != 1:
        print("<span class='codepicture' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i[1:]).replace("\uF860", "").replace("\uF861", 
                "").replace("\uF862", "").replace("\uF863", "").replace("\uF864", "")
    elif 0xF865 <= i[0] < 0xF867 and len(i) != 1:
        sequence_inverse = True
        print("<span class='codepicture' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i[1:]).replace("\uF865", "").replace("\uF866", "")
    elif (i[0] == 0xF867) and len(i) != 1:
        sequence_big = True
        print("<span class='codepicture' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i[1:]).replace("\uF867", "")
    elif 0xE000 <= i[0] < 0xF900:
        print("<span class='codepicture pua' lang={}>".format(lang), file=outfile)
        # Object Replacement Character (FFFD is already used by BIG5.TXT)
        strep = "\uFFFC"
    elif (0x10000 <= i[0] < 0x20000) or (0xFE0F in i):
        # SMP best to fall back to applicable emoji (or otherwise applicable) fonts,
        # and not try to push CJK fonts first.
        print("<span class='codepicture smp' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i)
    else:
        strep = "".join(chr(j) for j in i)
        firststrep = ucd.normalize("NFD", strep)[0] # Note: NOT NFKD.
        if (ord(firststrep) < 0x7F) and (strep[1:2] != "\u20E3"): # Don't include keycaps.
            print("<span class='codepicture roman'>", file=outfile)
        elif (ucd.category(firststrep)[0] == "M") and (ord(firststrep) < 0x3000):
            print("<span class='codepicture roman'>", file=outfile)
        else:
            print("<span class=codepicture lang={}>".format(lang), file=outfile)
    strep = strep.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if ucd.category(strep[0])[0] == "M":
        strep = "◌" + strep
    if strep[-1] == "\uF87B": # Apple encoding hint for usually medium bold form
        print("<b>", file=outfile)
        print(strep.rstrip("\uF87B"), file=outfile)
        print("</b>", file=outfile)
    elif strep[-1] == "\uF87C": # Apple encoding hint for usually bold form
        print("<b>", file=outfile)
        strep2 = strep.rstrip("\uF87C")
        # Boxed / circled versions
        if strep2[-1] == "\u20DD":
            print("<svg viewBox='0 0 72 72' class='charwrapper circle lightcircle'>", file=outfile)
            print("<text y='54px' x='36px' text-anchor='middle' class='wrappedtext'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] == "\u20DE":
            print("<svg viewBox='0 0 88 88' class='charwrapper lightsquare'>", file=outfile)
            print("<text y='72px' x='42px' text-anchor='middle' class='wrappedtext'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        else:
            print(strep2, file=outfile)
        print("</b>", file=outfile)
    elif strep[-1] == "\uF87E": # Apple encoding hint for vertical presentation form
        print("<span class=vertical>", file=outfile)
        print(strep.rstrip("\uF87E"), file=outfile)
        print("</span>", file=outfile)
    elif (strep[-1] in "\uF87A\uF875") or sequence_inverse: # Inverse form
        strep2 = strep.replace("\uF87A", "").replace("\uF875", "")
        if strep2[-1] == "\u20DD":
            print("<svg viewBox='0 0 72 72' class='charwrapper circle darkcircle'>", file=outfile)
            print("<text y='54px' x='36px' text-anchor='middle' class='wrappedtext inverse'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] in "\u20DE\u20E3": # The regular inverse rules don't work on keycaps either.
            print("<svg viewBox='0 0 88 88' class='charwrapper darksquare'>", file=outfile)
            print("<text y='72px' x='44px' text-anchor='middle' class='wrappedtext inverse'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif (strep2[0] == "[") and (strep2[-1] == "]"):
            hsf = 0
            for strepc in strep2[1:-1]:
                if ucd.east_asian_width(strepc) not in ("W", "F"):
                    hsf += 1
                else:
                    hsf += 1.618
            sizeclass = " half" if hsf > 7.5 else ""
            print("<svg viewBox='0 0 {1:d} 88' class='charwrapper darksquare{0}'>".format(sizeclass,
                  int(hsf * 48 + 0.5)), file=outfile)
            print("<text y='72px' x='{:d}px' text-anchor='middle' class='wrappedtext inverse'>".format(
                  int(hsf * 24 + 0.5)), file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[0]), end="", file=outfile)
            print(strep2[1:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2 == "\u262F":
            print("<span class='taegeuk taegeuk180'>", file=outfile)
            print(strep2, file=outfile)
            print("</span>", file=outfile)
        else:
            print("<svg viewBox='0 0 {:d} 88' class='charwrapper'>".format(74 * len(i[1:])), file=outfile)
            print("<text y='72px' class='wrappedtext inverse'>", file=outfile)
            print(strep2, file=outfile)
            print("</text></svg>", file=outfile)
    elif strep[-1] == "\uF876": # Apple encoding hint for rotated form
        strep2 = strep.replace("\uF876", "")
        if strep2 == "\u262F":
            print("<span class='taegeuk taegeuk90'>", file=outfile)
            print(strep2, file=outfile)
            print("</span>", file=outfile)
        else:
            print("<span class=rotated>", file=outfile)
            print(strep2, file=outfile)
            print("</span>", file=outfile)
    elif strep[-1] == "\uF877": # Apple encoding hint for superscript form
        print("<sup>", file=outfile)
        print(strep.replace("\uF877", ""), file=outfile)
        print("</sup>", file=outfile)
    elif strep[-1] == "\uF878": # Apple encoding hint for small form
        print("<small>", file=outfile)
        print(strep.rstrip("\uF878"), file=outfile)
        print("</small>", file=outfile)
    elif (strep[-1] == "\uF879") or sequence_big: # Apple encoding hint for large form
        print("<span class=bigform>", file=outfile)
        print(strep.rstrip("\uF879"), file=outfile)
        print("</span>", file=outfile)
    else:
        strep2 = strep.rstrip("\uF870\uF871\uF872\uF873\uF874\uF87D\uF87F")
        # Boxed / circled non-negative forms
        if strep2[-1] == "\u20DD":
            print("<svg viewBox='0 0 72 72' class='charwrapper circle lightcircle'>", file=outfile)
            print("<text y='58px' x='36px' text-anchor='middle' class='wrappedtext'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] == "\u20DE":
            print("<svg viewBox='0 0 88 88' class='charwrapper lightsquare'>", file=outfile)
            print("<text y='72px' x='42px' text-anchor='middle' class='wrappedtext'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] == "\u20DF":
            print("<svg viewBox='-2 -2 80 80' class='charwrapper lightdiamond'>", file=outfile)
            print("<text y='54px' x='36px' text-anchor='middle' class='wrappedtext'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text><polygon points='0,36 36,72 72,36 36,0' class='enclosure' /></svg>", file=outfile)
        elif (strep2[0] == "[") and (strep2[-1] == "]"):
            hsf = 0
            for strepc in strep2[1:-1]:
                if ucd.east_asian_width(strepc) not in ("W", "F"):
                    hsf += 1
                else:
                    hsf += 1.618
            sizeclass = " half" if hsf > 7.5 else ""
            print("<svg viewBox='0 0 {1:d} 88' class='charwrapper lightsquare{0}'>".format(sizeclass,
                  int(hsf * 48 + 0.5)), file=outfile)
            print("<text y='72px' x='{:d}px' text-anchor='middle' class='wrappedtext'>".format(
                  int(hsf * 24 + 0.5)), file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[0]), end="", file=outfile)
            print(strep2[1:-1], end="", file=outfile)
            print("<tspan class='redundant'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2 == "\u262F":
            print("<span class=taegeuk>", file=outfile)
            print(strep2, file=outfile)
            print("</span>", file=outfile)
        else:
            print(strep2, file=outfile)
    print("</span>", file=outfile)




