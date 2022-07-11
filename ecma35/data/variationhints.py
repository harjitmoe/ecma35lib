#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Detail regarding Apple-compatible versus up-to-date mappings

import os, json, shutil, math
import unicodedata as ucd
from ecma35.data import gccdata
from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.names import namedata

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
    # Bold kite-headed arrows (closer approximation):
    (0x2190, 0xF878): (0x1F878,),
    (0x2191, 0xF878): (0x1F879,),
    (0x2192, 0xF878): (0x1F87A,),
    (0x2193, 0xF878): (0x1F87B,),
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
    # Bold triangle-headed arrow, with detached head IFF vertical:
    (0x21e6, 0xf87F): (0x1F780, 0x1F89C),
    (0x21e7, 0xf87F): (0x1F829,),
    (0x21e8, 0xf87F): (0x1F89C, 0x1F782),
    (0x21e9, 0xf87F): (0x1F82B,),
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
    (0xF84A,): (0x1F66C,), # Leftward lozenge-tipped rocket or bowed arrow
    (0xF84B,): (0x1F66E,), # Rightward lozenge-tipped rocket or bowed arrow
    #
    # Broadcast (ripple) arrows (not exactly speakers but close enough darnit)
    (0xF846,): (0x1F56A, 0xF87F), # Pointing and broadcasting to left
    (0xF847,): (0x1F50A, 0xF87F), # Pointing and broadcasting to right
    #
    # White left-right arrow (is blatantly U+2B04, though not commented as a Unicode 4.0 alt)
    (0x21D4, 0xF879): (0x2B04,),
    #
    # ==== NON-ARROWS: ====
    #
    # MacKorean hint sequences which have since gotten unique representations:
    (0x2394, 0xF876): (0x2B21,),  # White hexagon
    # Lozenges
    (0x25C6, 0xF879): (0x2BC1,), # Another black diamond besides the Wansung one
    (0x25C7, 0xF879): (0x2B26,), # Another white diamond besides the Wansung one
    (0x25C7, 0xF87B): (0x1FBAE,), # Yet another white diamond, bolder
    (0x25C7, 0xF87C): (0x1F754,), # Small diamond
    (0x25C7, 0xF87F): (0x2B2B,), # Lozenge as a member of a series of small-ish geometry icons
    (0x25C8, 0xF87F): (0x1F7A0,), # Outlined black lozenge
    # Circles
    (0x25EF, 0xF87C): (0x1F785,), # Medium-bold white circle
    (0x25CB, 0xF87B): (0x1F786,), # Bold white circle
    (0x25CF, 0xF879): (0x2B24,), # Black large circle
    (0x25CB, 0xF879): (0x2B55, 0xFE0E),
    # Squares
    (0x2610, 0xF87C): (0x1F78F,), # Medium-bold white square
    (0x25A1, 0xF879): (0x2B1C, 0xFE0E), # Big white square
    (0x25A1, 0xF87B): (0x1F790,), # Bold white square
    (0x2610, 0xF87F): (0x2B1A,),  # Dotted square
    # Others
    (0x534D, 0xF87F): (0x0FD6,),  # Manji as a non-kanji
    (0xFF0A, 0xF87F): (0x3000, 0x20F0), # High asterisk
    (0x2206, 0xF87F): (0x1D71F,), # Medium-bold oblique capital delta
    (0x0021, 0xF87F): (0x2757,), # Emphasised exclamation mark
    #
    # Avoid transcoding hints on the alternate versions of manicules by mapping to
    #   backhand (even though they are usually just shown as bigger versions):
    (0x261C, 0xF87F): (0x1F448, 0xFE0E),
    (0x261D, 0xF87F): (0x1F446, 0xFE0E),
    (0x261E, 0xF87F): (0x1F449, 0xFE0E),
    (0x261F, 0xF87F): (0x1F447, 0xFE0E),
    #
    # Special cases
    # Small white square: was already present so unclear why it wasn't used anywhere in the mapping
    (0x25A1, 0xF87C): (0x25AB,),
    # Weight-unbalanced vertical lines, added in Unicode 3.1 but not used by the mapping to 3.2.
    (0x2016, 0xF87B): (0x1D102,), # Double vertical, bold on right
    (0x2016, 0xF87C): (0x1D103,), # Double vertical, bold on left
    # Telephone dial. None of the four encoded variants of the ☏ are at all close,
    #   but U+260F is the most likely of the four to display a dial (U+1F57E and
    #   U+1F57F are expressly keyed, while U+260E is often displayed as a keyed
    #   variant).
    (0xF807,): (0x260F, 0xF87F),
    (0x203C, 0xF87F): (0x203C, 0xFE0F), # Honestly that's good enough.
    (0xFF01, 0xF874): (0xFF01, 0xFE00), # Later gained an SVS
    (0x3002, 0xF87D): (0x3002, 0xFE00), # Later gained an SVS
    # Ideographic circular zero. Appears in a range of rotated Chinese numerals, but the circular
    #   zero is rotationally symmetric (and no other U+3007 appears anywhere else in MacKorean).
    (0x3007, 0xF876): (0x3007,),
    (0x24EA, 0xF87F): (0x24EA,), # It's the only circled zero, the other set starts at one.
    #
    # Some direct PUA mappings used by MacKorean but no longer needed
    (0xF806,): (0x26CB, 0xF87A),
    (0xF808,): (0x1D36D,), # Five vertical lines
    (0xF809, 0xF87A): (0x169B2, 0xF87F), # Like a flipped version of U+169B2 (itself like an MOT sign)
    (0xF809,): (0x169B2, 0xF87A), # Like a filled and flipped version of U+169B2
    (0xF80A,): (0x1F668,), # "Two interwoven eye shapes" (basically a variant quilt square)
    (0xF80B,): (0x1F66A,), # This one really close (narrow-leaf four-petal florette)
    (0xF80B, 0xF87F): (0x1F66B,), # Less so, but may as well commit to it
    (0xF83D,): (0x269C,), # Fleur de lis
    (0xF83D, 0xF87F): (0x269C, 0xF87F), # Alternate fleur de lis
    (0xF840,): (0x2051, 0x20F0), # Three vertical asterisks
    (0xF842,): (0x2B4D,), # Downward wave arrow (not exactly, but better than PUA)
    (0xF844,): (0x2B9C,), # Leftward arrowhead
    (0xF84C,): (0x2B20,), # White pentagon
    (0xF84D,): (0x23E2,), # Trapezoid
    #
    # Absolute kludges
    (0xF841,): (0x21F9, 0x0302, 0x032C),
    (0xF843,): (0x1F898, 0xF87A),
    (0xF845,): (0x21A2, 0xF87F),
    #
    # Adobe PUA assignments. Apple originally inherited these, though it mostly switched to hints.
    # Hence, it is appropriate to treat these in the same PUA processor.
    # Mapping to the hints alternatives or to standard, as appropriate:
    (0xF8E6,): (0x23D0,), # Vertical arrow extender
    (0xF8E7,): (0x23AF,), # Horizontal arrow extender
    (0xF6DA,): (0x00AE,), # Registered Trademark, Roman
    (0xF6D9,): (0x00A9,), # Copyright, Roman
    (0xF6DB,): (0x2122,), # Trademark, Roman
    (0xF8E8,): (0x00AE, 0xF87F), # Registered Trademark, Gothic
    (0xF8E9,): (0x00A9, 0xF87F), # Copyright, Gothic
    (0xF8EA,): (0x2122, 0xF87F), # Trademark, Gothic
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

# Contains updating changes to sequences without hints, hence it is specific
#   to the intention of MacKorean rather than for all things with hints.
applesinglehints_mackorean = applesinglehints.copy()
applesinglehints_mackorean.update({
    # U+2939 is rarely shown pointing in the intended direction (per FileFormat, PragmataPro is an
    #   exception to this). Usually it transitions from SW to point SE, not the intended W to S.
    (0x2939,): (0x2BAE, 0xF87F),
    # Rightward arrows where the rightward member of the later-added full set is disunified from
    #   rightward-only Zapf arrow that Apple maps to:
    (0x279E,): (0x1F80A,),
    (0x27B2,): (0x2B8A,),
    (0x2794,): (0x1F872,),
    (0x27A1,): (0x2B95,),
    (0x27A4,): (0x2B9E,),
    # The newer ⯎ is a more appropriate relative size than ⟡
    (0x27E1, 0x20DD): (0x2BCE, 0x20DD),
    #
    # Kludgy unrenderable combining sequences with properly defined alternatives:
    (0x25B3, 0x20DD): (0x1F7D5,), # White triangle in white circle
    (0x25C7, 0x20DE): (0x26CB,), # Diamond in square (added eventually from ARIB)
    (0x25C7, 0x20DF): (0x1F79C,), # Two-ringed diamond target
    (0x25C7, 0x20DF, 0x20DF): (0x1F79C, 0x20DF), # Three-ringed diamond target
    (0x25C9, 0x20DD): (0x1F78B,), # Circular target (black bullseye)
    (0x29C8, 0x20DE): (0x1F796,), # Square target
    # The group mark does now exist, although it's a recent (v10) addition:
    (0x2261, 0x20D2): (0x2BD2,), # Group mark
    #
    # (0x5370, 0x20DD) vs (0x329E,) are a special case (used for different duplicates)
    # (0x329E, 0xF87F) is already used for the dotted one.
    #
    # Poorly chosen combining sequences unlikely to show correctly, to better ones:
    # - Is 0xA1AB (U+2016), not U+2225 (0xA755), with long double underline not short equals below
    (0x2225, 0x0347): (0x2016, 0x0333),
    # - Is 0xA755 (U+2225) plus long double underline (not short equals below)
    (0x2AFD, 0x0347): (0x2225, 0x0333),
    #
    # Special case for flowers: 0xA67B corresponds to Adobe-Japan1 CID-12228, which maps to U+2740.
    #   As such, U+2740 in Adobe-Japan1-based fonts (like Source Han/Noto CJK) corresponds closely
    #   to 0xA67B's glyph.
    # Apple maps 0xA67B to U+273F+F87A since 0xA699 is already mapped to U+2740. However, 0xA699
    #   is a four-petalled flower, while both 0xA699 and U+2740 (either when in its Unicode
    #   reference glyph, or in its Adobe glyph) have five petals, as a pair with U+273F or 0xA67C.
    # Worth noting though is that Adobe-Korea1 does not map 0xA67B and 0xA67C to Unicode, despite
    #   very closely matching the Adobe-Japan1 characters mapped to U+2740 and U+273F.
    # U+1F33C (which postdates Apple's mapping) does not have a fixed number of petals, (it can
    #   show up with anywhere between 5 and 28 rayflorets or petals depending on font), so it is
    #   a more suitable updated mapping for 0xA699 methinks.
    (0x273F, 0xF87A): (0x2740,),
    (0x2740,): (0x1F33C,),
    #
    # Special cases of characters that were *already in Unicode 3.2 as it transpires*
    (0x3D, 0x20D2): (0x29E7,), # Record mark (⧧)
    (0x6CE8, 0x20DD): (0x329F,), # ㊟
    (0x2314, 0xF87F): (0x29A1,), # Angle or sector opening upward, not a white closed sector shape
})

# Version avoiding mapping to variation sequences when the base character isn't otherwise mapped,
#   or combining sequences when the base character isn't otherwise mapped and is good enough, so
#   encoder will accept hint-stripped or selector-stripped version.
applesinglehints_mackorean_pragmatic = applesinglehints_mackorean.copy()
applesinglehints_mackorean_pragmatic.update({
    (0x261C, 0xF87F): (0x1F448,),
    (0x261D, 0xF87F): (0x1F446,),
    (0x261E, 0xF87F): (0x1F449,),
    (0x261F, 0xF87F): (0x1F447,),
    (0xF809, 0xF87A): (0x169B2,),
    (0x2748, 0x20D8): (0x2748,),
    (0x25CB, 0xF879): (0x2B55,),
    (0x25A1, 0xF879): (0x2B1C,),
    (0xF805, 0x20DE): (0x1F4A0, 0x20DE),
    (0xF806, 0x20DF): (0x26CB, 0x20DF),
    (0xF843,): (0x1F898,),
    (0xF845,): (0x21A2,),
    (0xF846,): (0x1F56A,),
    (0xF847,): (0x1F50A,),
    #
    # Really not the right shape/character, but better than PUA
    (0xF805,): (0x1F4A0,),
    (0xF80C,): (0x0CA3,),
    (0xF84E,): (0x1FB4D,), # declining tetragon
    (0xF84F,): (0x1FB42,), # inclining tetragon
    #
    # Map dot-after capitals to squared capitals (by elimination to some extent)
    (0xF860, 0x0041, 0x002E): (0x1F130,), # 🄰
    (0xF860, 0x0042, 0x002E): (0x1F131,), # 🄱
    (0xF860, 0x0043, 0x002E): (0x1F132,), # 🄲
    (0xF860, 0x0044, 0x002E): (0x1F133,), # 🄳
    (0xF860, 0x0045, 0x002E): (0x1F134,), # 🄴
    (0xF860, 0x0046, 0x002E): (0x1F135,), # 🄵
    (0xF860, 0x0047, 0x002E): (0x1F136,), # 🄶
    (0xF860, 0x0048, 0x002E): (0x1F137,), # 🄷
    (0xF860, 0x0049, 0x002E): (0x1F138,), # 🄸
    (0xF860, 0x004A, 0x002E): (0x1F139,), # 🄹
    (0xF860, 0x004B, 0x002E): (0x1F13A,), # 🄺
    (0xF860, 0x004C, 0x002E): (0x1F13B,), # 🄻
    (0xF860, 0x004D, 0x002E): (0x1F13C,), # 🄼
    (0xF860, 0x004E, 0x002E): (0x1F13D,), # 🄽
    (0xF860, 0x004F, 0x002E): (0x1F13E,), # 🄾
    (0xF860, 0x0050, 0x002E): (0x1F13F,), # 🄿
    (0xF860, 0x0051, 0x002E): (0x1F140,), # 🅀
    (0xF860, 0x0052, 0x002E): (0x1F141,), # 🅁
    (0xF860, 0x0053, 0x002E): (0x1F142,), # 🅂
    (0xF860, 0x0054, 0x002E): (0x1F143,), # 🅃
    (0xF860, 0x0055, 0x002E): (0x1F144,), # 🅄
    (0xF860, 0x0056, 0x002E): (0x1F145,), # 🅅
    (0xF860, 0x0057, 0x002E): (0x1F146,), # 🅆
    (0xF860, 0x0058, 0x002E): (0x1F147,), # 🅇
    (0xF860, 0x0059, 0x002E): (0x1F148,), # 🅈
    (0xF860, 0x005A, 0x002E): (0x1F149,), # 🅉
    #
    # Grumble grumble grumble (if stripping hint sequences after decode, don't want a round-trip
    #   indirect zigzag convergence for non-PUA)
    (0x2939,): (0x2939,),
})

applesinglehints_mackorean_nishikiteki = applesinglehints_mackorean.copy()
applesinglehints_mackorean_nishikiteki.update({
    #
    # White arrows in black square:
    (0x21e6, 0x20DE): (0xE3F6,),
    (0x21e7, 0x20DE): (0xE3F7,),
    (0x21e8, 0x20DE): (0xE3F5,),
    (0x21e9, 0x20DE): (0xE3F8,),
    #
    # White arrows in black circle:
    (0x21e6, 0x20DD): (0xE3F2,),
    (0x21e7, 0x20DD): (0xE3F3,),
    (0x27B2,): (0xE3F1,),
    (0x21e9, 0x20DD): (0xE3F4,),
    #
    (0x25B4, 0x20E4): (0xF6E8,), # Black triangle in triangle
    (0x25B2, 0x20DD): (0xF6ED,), # Black triangle in circle
    (0x29C8, 0x20DE): (0xE3D9,), # Square target (better than U+1F796 since latter has black bullseye)
    (0x25C6, 0x20DE): (0xE3D4,), # Black lozenge in square
    #
    # Apple PUA actually included in Nishiki-teki (override inferior approximations in the other dict)
    (0xF806,): (0xF806,),
    (0xF807,): (0xF807,), # Telephone dial
    (0xF808,): (0xF808,), # Five vertical lines
    (0xF809,): (0xF809,), # Like a filled and flipped version of the MOT Test symbol
    (0xF80A,): (0xF80A,), # Two interwoven eye shapes
    (0xF80B,): (0xF80B,), # Four pointed flower or quilt square
    (0xF840,): (0xF840,), # Three vertical asterisks
    (0xF841,): (0xF841,), # Cardinal points arrow / move cursor / cross barby
    (0xF842,): (0xF842,), # Downward wave arrow
    (0xF843,): (0xF843,),
    (0xF845,): (0xF845,),
    (0xF846,): (0xF846,), # Pointing and broadcasting to left
    (0xF847,): (0xF847,), # Pointing and broadcasting to right
    (0xF848,): (0xF848,), # White leftward heavy rocket
    (0xF849,): (0xF849,), # White rightward heavy rocket
    (0xF84A,): (0xF84A,), # Leftward lozenge-tipped rocket or bowed arrow
    (0xF84B,): (0xF84B,), # Rightward lozenge-tipped rocket or bowed arrow
    #
    (0xF8FF, 0xF87F): (0xF89E,), # White Apple logo
    (0x203C, 0xF87F): (0xF007B,),
    #
    # White rounded-stroke arrows
    (0x2190, 0xF875): (0xF00CD,),
    (0x2191, 0xF875): (0xF00CE,),
    (0x2192, 0xF875): (0xF00CA,),
    (0x2193, 0xF875): (0xF00CF,),
    #
    # Boxed West-Arabic Numerals
    (0x0030, 0x20DE): (0xF06E0,),
    (0x0030, 0x20DE, 0xF87F): (0x0030, 0x20DE,),
    (0x0031, 0x20DE): (0xF06E1,),
    (0x0031, 0x20DE, 0xF87F): (0x0031, 0x20DE,),
    (0x0032, 0x20DE): (0xF06E2,),
    (0x0032, 0x20DE, 0xF87F): (0x0032, 0x20DE,),
    (0x0033, 0x20DE): (0xF06E3,),
    (0x0033, 0x20DE, 0xF87F): (0x0033, 0x20DE,),
    (0x0034, 0x20DE): (0xF06E4,),
    (0x0034, 0x20DE, 0xF87F): (0x0034, 0x20DE,),
    (0x0035, 0x20DE): (0xF06E5,),
    (0x0035, 0x20DE, 0xF87F): (0x0035, 0x20DE,),
    (0x0036, 0x20DE): (0xF06E6,),
    (0x0036, 0x20DE, 0xF87F): (0x0036, 0x20DE,),
    (0x0037, 0x20DE): (0xF06E7,),
    (0x0037, 0x20DE, 0xF87F): (0x0037, 0x20DE,),
    (0x0038, 0x20DE): (0xF06E8,),
    (0x0038, 0x20DE, 0xF87F): (0x0038, 0x20DE,),
    (0x0039, 0x20DE): (0xF06E9,),
    (0x0039, 0x20DE, 0xF87F): (0x0039, 0x20DE,),
    #
    # Boxed West-Arabic Numerals (negative)
    (0x0030, 0x20DE, 0xF87A): (0xF0740,),
    (0x0031, 0x20DE, 0xF87A): (0xF0741,),
    (0x0032, 0x20DE, 0xF87A): (0xF0742,),
    (0x0033, 0x20DE, 0xF87A): (0xF0743,),
    (0x0034, 0x20DE, 0xF87A): (0xF0744,),
    (0x0035, 0x20DE, 0xF87A): (0xF0745,),
    (0x0036, 0x20DE, 0xF87A): (0xF0746,),
    (0x0037, 0x20DE, 0xF87A): (0xF0747,),
    (0x0038, 0x20DE, 0xF87A): (0xF0748,),
    (0x0039, 0x20DE, 0xF87A): (0xF0749,),
    #
    # Boxed Chinese numerals
    (0x56DB, 0x20DE): (0xF07C9,),
    (0x56DB, 0x20DE, 0xF87A): (0xF07C9, 0xF87A),
    (0x4E94, 0x20DE): (0xF07CA,),
    (0x4E94, 0x20DE, 0xF87A): (0xF07CA, 0xF87A),
    (0x516D, 0x20DE): (0xF07CB,),
    (0x516D, 0x20DE, 0xF87A): (0xF07CB, 0xF87A),
    (0x4E03, 0x20DE): (0xF07CC,),
    (0x4E03, 0x20DE, 0xF87A): (0xF07CC, 0xF87A),
    (0x516B, 0x20DE): (0xF07CD,),
    (0x516B, 0x20DE, 0xF87A): (0xF07CD, 0xF87A),
    (0x4E5D, 0x20DE): (0xF07CE,),
    (0x4E5D, 0x20DE, 0xF87A): (0xF07CE, 0xF87A),
    (0x5341, 0x20DE): (0xF07CF,),
    (0x5341, 0x20DE, 0xF87A): (0xF07CF, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x4E00, 0x005D): (0xF07D0,),
    (0xF863, 0x005B, 0x5341, 0x4E00, 0x005D): (0xF07D0, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x4E8C, 0x005D): (0xF07D1,),
    (0xF863, 0x005B, 0x5341, 0x4E8C, 0x005D): (0xF07D1, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x4E09, 0x005D): (0xF07D2,),
    (0xF863, 0x005B, 0x5341, 0x4E09, 0x005D): (0xF07D2, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x56DB, 0x005D): (0xF07D3,),
    (0xF863, 0x005B, 0x5341, 0x56DB, 0x005D): (0xF07D3, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x4E94, 0x005D): (0xF07D4,),
    (0xF863, 0x005B, 0x5341, 0x4E94, 0x005D): (0xF07D4, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x516D, 0x005D): (0xF07D5,),
    (0xF863, 0x005B, 0x5341, 0x516D, 0x005D): (0xF07D5, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x4E03, 0x005D): (0xF07D6,),
    (0xF863, 0x005B, 0x5341, 0x4E03, 0x005D): (0xF07D6, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x516B, 0x005D): (0xF07D7,),
    (0xF863, 0x005B, 0x5341, 0x516B, 0x005D): (0xF07D7, 0xF87A),
    (0xF862, 0x005B, 0x5341, 0x4E5D, 0x005D): (0xF07D8,),
    (0xF863, 0x005B, 0x5341, 0x4E5D, 0x005D): (0xF07D8, 0xF87A),
    (0xF862, 0x005B, 0x4E8C, 0x5341, 0x005D): (0xF07D9,),
    (0xF863, 0x005B, 0x4E8C, 0x5341, 0x005D): (0xF07D9, 0xF87A),
    #
    # Encircled hanzi
    (0x5927, 0x20DD): (0xF0A32,),
    (0x5C0F, 0x20DD): (0xF0A33,),
    (0x63A7, 0x20DD): (0xF0A34,),
    (0x8ABF, 0x20DD): (0xF0A35,),
    (0x526F, 0x20DD): (0xF0A36,),
    (0x6E1B, 0x20DD): (0xF0A37,),
    (0x6A19, 0x20DD): (0xF0A38,),
    (0x6B20, 0x20DD): (0xF0A39,),
    (0x57FA, 0x20DD): (0xF0A3A,),
    (0x51FA, 0x20DD): (0xF0A3B,),
    (0x6E08, 0x20DD): (0xF0A3C,),
    (0x5897, 0x20DD): (0xF0A3D,),
    (0x7B54, 0x20DD): (0xF0A3E,),
    (0x4F8B, 0x20DD): (0xF0A3F,),
    (0x96FB, 0x20DD): (0xF0A40,),
    (0x5E74, 0x20DD): (0xF0A41,),
    (0x51A0, 0x20DD): (0xF0A42,),
    (0x8863, 0x20DD): (0xF0A43,),
    (0x672B, 0x20DD): (0xF0A44,),
    (0x611F, 0x20DD): (0xF0A45,),
    (0x6163, 0x20DD): (0xF0A46,),
    (0x4EE3, 0x20DD): (0xF0A47,),
    (0x52D5, 0x20DD): (0xF0A48,),
    (0x53CD, 0x20DD): (0xF0A49,),
    (0x81EA, 0x20DD): (0xF0A4A,),
    (0x524D, 0x20DD): (0xF0A4B,),
    (0x63A5, 0x20DD): (0xF0A4C,),
    (0x52A9, 0x20DD): (0xF0A4D,),
    (0x53C3, 0x20DD): (0xF0A4E,),
    (0x672C, 0x20DD): (0xF0A4F,),
    (0x65B0, 0x20DD): (0xF0A50,),
    (0x73FE, 0x20DD): (0xF0A51,),
    (0x5F62, 0x20DD): (0xF0A52,),
    (0x9593, 0x20DD): (0xF0A53,),
    (0x570B, 0x20DD): (0xF0A54,),
    (0x4ED6, 0x20DD): (0xF0A55,),
    (0x329E, 0xF87F): (0xF0A56,), # Dotted circled "print" kanji
    #
    (0xF861, 0x2020, 0x2020, 0x2020): (0xFEE2A,), # Three daggers
    (0xF860, 0x2020, 0x2020): (0xFEE2B,), # Two daggers
    (0x2741,): (0xFEFB4,), # Eight-petalled white flower (Nishiki-teki chart notes correspondance)
    (0x2748, 0x20D8): (0xFEFCF,), # Starburst/rayburst with central ring
    (0xF809, 0xF87A): (0xFF0D3,), # "Symbol for the Fates", like a flipped MOT Test symbol; Chrysanthi apparently encodes it over ♼
})

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

def ahmap(pointer, ucs, applesinglehints=applesinglehints):
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
    elif (len(ucs) == 2) and namedata.get_ucsname(chr(ucs[0]), None) and (ucs[1] == 0x20DE):
        try:
            return (ord(namedata.lookup_ucsname("SQUARED " + namedata.get_ucsname(chr(ucs[0])))),)
        except KeyError:
            return ucs
    return ucs

def is_filled_character(ucs):
    name = namedata.get_ucsname(ucs, "")
    if "BLACK" in name or "NEGATIVE" in name:
        return True
    elif "WHITE" in name or "RIBBON" in name:
        return False
    elif "SQUARED" in name or "CIRCLED" in name:
        return False
    elif 0xF0620 <= ord(ucs) <= 0xF067F or 0xF06E0 <= ord(ucs) <= 0xF06E9 or 0xF06F0 <= ord(ucs) <= 0xF073F or 0xF07A2 <= ord(ucs) <= 0xF07D9 or 0xF07E7 <= ord(ucs) <= 0xF07FE or 0xF0A00 <= ord(ucs) <= 0xF0A55:
        return False
    else:
        return True

def invert_rotate(display_string, rotate_by, flip, selectable_string, invert, outfile):
    assert len(display_string) == 1 or not (rotate_by or flip)
    xforms = []
    if rotate_by:
        xforms.append(f"rotate({rotate_by} 38 44)")
    if flip:
        xforms.append("translate(72)")
        xforms.append("scale(-1 1)")
    rot = " transform='{}'".format(" ".join(xforms)) if xforms else ""
    separate_sel = display_string != selectable_string 
    maybe_nosel = " aria-hidden='true'" if separate_sel else ""
    print("<svg viewBox='0 0 {:d} 88' class='charwrapper{}'>".format(
        74 * len(display_string),
        " taegeuk" if display_string == "\u262F" else ""
    ), file=outfile)
    if not invert:
        print(f"<text y='72px' font-size='72px'{rot}{maybe_nosel}>", file=outfile)
        print(display_string, file=outfile)
        print("</text>", file=outfile)
        if separate_sel:
            print(f"<text y='72px' fill='none' stroke='none'>", file=outfile)
            print(selectable_string, file=outfile)
            print("</text>", file=outfile)
    elif is_filled_character(display_string[0]):
        print(f"<text y='72px' class='inverse' font-size='72px'{rot}{maybe_nosel}>", file=outfile)
        print(display_string, file=outfile)
        print("</text>", file=outfile)
        if separate_sel:
            print(f"<text y='72px' fill='none' stroke='none'>", file=outfile)
            print(selectable_string, file=outfile)
            print("</text>", file=outfile)
    else:
        cpts = "".join(f"u{ord(jj):04X}" for jj in display_string)
        print(f"<filter id='silhouette{cpts}'>", file=outfile)
        print("<feMorphology operator='dilate' radius='8'/>", file=outfile)
        print("<feMorphology operator='erode' radius='7'/>", file=outfile)
        print("</filter>", file=outfile)
        print(f"<mask id='letter{cpts}'>", file=outfile)
        print("<polygon points='0,0 0,88 74,88 74,0' fill='white'/>", file=outfile)
        print(f"<text y='72px' fill='black' aria-hidden='true' font-size='72px'{rot}>", file=outfile)
        print(display_string, file=outfile)
        print("</text>", file=outfile)
        print("</mask>", file=outfile)
        print(f"<text y='72px' filter='url(#silhouette{cpts})' mask='url(#letter{cpts})' font-size='72px'{rot}{maybe_nosel}>", file=outfile)
        print(display_string, file=outfile)
        print("</text>", file=outfile)
        if separate_sel:
            print(f"<text y='72px' font-size='72px' fill='none' stroke='none'>", file=outfile)
            print(selectable_string, file=outfile)
            print("</text>", file=outfile)
    print("</svg>", file=outfile)

def arrow_to_angle(arrow):
    if arrow in "\u2190\u21e6":
        return 0, True
    elif arrow in "\u2191\u21e7":
        return 90, True
    elif arrow in "\u2193\u21e9":
        return 90, False
    return 0, False

def print_hints_to_html5(i, outfile, *, lang="ja", showbmppua=False):
    sequence_inverse = sequence_big = sequence_small = sequence_bold = False
    if i[0] >= 0xF0000:
        print("<span class='cpc spua' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i)
    elif 0xF860 <= i[0] < 0xF865 and len(i) != 1:
        strep = "".join(chr(j) for j in i[1:]).replace("\uF860", "").replace("\uF861", 
                "").replace("\uF862", "").replace("\uF863", "").replace("\uF864", "")
        classes = "cpc"
        if len(strep) > 2:
            classes += " nosuff"
        print("<span class='{}' lang={}>".format(classes, lang), file=outfile)
    elif 0xF865 <= i[0] < 0xF867 and len(i) != 1:
        sequence_inverse = True
        print("<span class='cpc' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i[1:]).replace("\uF865", "").replace("\uF866", "")
    elif (i[0] == 0xF867) and len(i) != 1:
        sequence_big = True
        print("<span class='cpc' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i[1:]).replace("\uF867", "")
    elif (i[0] == 0xF868) and len(i) != 1:
        sequence_small = True
        print("<span class='cpc' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i[1:]).replace("\uF868", "")
    elif (i[0] == 0xF869) and len(i) != 1:
        sequence_small = sequence_bold = True
        print("<span class='cpc' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i[1:]).replace("\uF869", "")
    elif 0xE000 <= i[0] < 0xF900:
        # Object Replacement Character (FFFD is already used by BIG5.TXT)
        if not showbmppua:
            print("<span class='cpc pua' lang={}>".format(lang), file=outfile)
            strep = "\uFFFC"
        else:
            print("<span class='cpc spua' lang={}>".format(lang), file=outfile)
            strep = "".join(chr(j) for j in i)
    elif ((0x10000 <= i[0] < 0x20000) or (0xFE0F in i)) and (0xFE0E not in i):
        # SMP best to fall back to applicable emoji (or otherwise applicable) fonts,
        # and not try to push CJK fonts first.
        print("<span class='cpc smp' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i)
    elif len(i) > 1 and 0xFE0E in i:
        print("<span class='cpc fe0e' lang={}>".format(lang), file=outfile)
        strep = "".join(chr(j) for j in i)
    else:
        strep = "".join(chr(j) for j in i)
        firststrep = strep[0]
        while firststrep in namedata.canonical_decomp:
            firststrep = namedata.canonical_decomp[firststrep][0]
        if (ord(firststrep) < 0x7F) and (strep[1:2] != "\u20E3"): # Don't include keycaps.
            print("<span class='cpc roman'>", file=outfile)
        elif (namedata.get_ucscategory(firststrep)[0] == "M") and (ord(firststrep) < 0x3000):
            print("<span class='cpc roman'>", file=outfile)
        elif strep.endswith("\u20E3"): # i.e. without a VS16 after
            print("<span class='cpc nishiki' lang={}>".format(lang), file=outfile)
        elif strep == "\u2B21":
            print("<span class='cpc nobast' lang={}>".format(lang), file=outfile)
        else:
            print("<span class=cpc lang={}>".format(lang), file=outfile)
    strep = strep.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if namedata.get_ucscategory(strep[0])[0] == "M":
        strep = "◌" + strep
    not_in_unicode3pt2_arrows_blocks = (
        ord(strep[0]) not in range(0x2190, 0x2200) and
        ord(strep[0]) not in range(0x27F0, 0x2800) and
        ord(strep[0]) not in range(0x2900, 0x2980)
    )
    # Arrow styles (don't always use transcoding hints for their usual meanings)
    if len(strep) == 2 and 0x2190 <= ord(strep[0]) <= 0x2193 and strep[1] == "\uF871":
        rot, flip = arrow_to_angle(strep[0])
        invert_rotate("\u279B", rot, flip, strep[0], False, outfile) 
    elif len(strep) == 2 and 0x2190 <= ord(strep[0]) <= 0x2193 and strep[1] == "\uF875":
        rot, flip = arrow_to_angle(strep[0])
        invert_rotate("\u279C", rot, flip, strep[0], True, outfile) 
    elif len(strep) == 2 and 0x2190 <= ord(strep[0]) <= 0x2193 and strep[1] == "\uF87F":
        rot, flip = arrow_to_angle(strep[0])
        invert_rotate("\u279C", rot, flip, strep[0], False, outfile) 
    elif strep == "\uF843":
        invert_rotate("\u21F0", 0, True, "←", False, outfile) 
    elif strep == "\uF845":
        invert_rotate("\u27B5", 0, True, "←", False, outfile) 
    # Other uses
    elif strep[-1] == "\uF87B" and not_in_unicode3pt2_arrows_blocks:
        # Apple encoding hint for usually medium bold form
        print("<b>", file=outfile)
        print(strep.rstrip("\uF87B"), file=outfile)
        print("</b>", file=outfile)
    elif strep[-1] == "\uF87C" and not_in_unicode3pt2_arrows_blocks:
        # Apple encoding hint for usually bold form
        print("<b>", file=outfile)
        strep2 = strep.rstrip("\uF87C")
        # Boxed / circled versions
        if strep2[-1] == "\u20DD":
            print("<svg viewBox='0 0 72 72' class='charwrapper circle lightcircle'>", file=outfile)
            print("<text y='54px' x='36px' text-anchor='middle' font-size='64px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] == "\u20DE":
            print("<svg viewBox='0 0 88 88' class='charwrapper lightsquare'>", file=outfile)
            print("<text y='72px' x='42px' text-anchor='middle' font-size='72px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
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
            print("<text y='54px' x='36px' text-anchor='middle' class='inverse' font-size='48px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] in "\u20DE\u20E3": # The regular inverse rules don't work on keycaps either.
            print("<svg viewBox='0 0 88 88' class='charwrapper darksquare'>", file=outfile)
            print("<text y='72px' x='44px' text-anchor='middle' class='inverse' font-size='72px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
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
            print("<text y='72px' x='{:d}px' text-anchor='middle' class='inverse' font-size='72px'>".format(
                  int(hsf * 24 + 0.5)), file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[0]), end="", file=outfile)
            print(strep2[1:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2 == "\u262F":
            invert_rotate(strep2, 180, True, strep2, False, outfile)
        else:
            invert_rotate(strep2, 0, False, strep2, True, outfile)
    elif strep[-1] == "\uF876": # Apple encoding hint for rotated form
        strep2 = strep.replace("\uF876", "")
        if strep2 == "\u262F":
            invert_rotate(strep2, 90, True, strep2, False, outfile)
        else:
            invert_rotate(strep2, -90, False, strep2, False, outfile)
    elif strep[-1] == "\uF877": # Apple encoding hint for superscript form
        print("<sup>", file=outfile)
        print(strep.replace("\uF877", ""), file=outfile)
        print("</sup>", file=outfile)
    elif strep[-1] == "\uF878" or sequence_small: # Apple encoding hint for small form
        print("<small>", file=outfile)
        if sequence_bold:
            print("<b>", file=outfile)
        print(strep.rstrip("\uF878"), file=outfile)
        if sequence_bold:
            print("</b>", file=outfile)
        print("</small>", file=outfile)
    elif (strep[-1] == "\uF879") or sequence_big: # Apple encoding hint for large form
        print("<span class=bigform>", file=outfile)
        print(strep.rstrip("\uF879"), file=outfile)
        print("</span>", file=outfile)
    else:
        strep2 = strep.rstrip("\uF870\uF871\uF872\uF873\uF874\uF87B\uF87C\uF87D\uF87F")
        # Boxed / circled non-negative forms
        if strep2[-1] == "\u20DD":
            print("<svg viewBox='0 0 72 72' class='charwrapper circle lightcircle'>", file=outfile)
            if strep2[0] not in "\u2BCE\u25C6\uF805":
                print("<text y='58px' x='36px' text-anchor='middle' font-size='64px'>", file=outfile)
            else:
                print("<text y='69px' x='35px' text-anchor='middle' font-family='Nishiki-teki' font-size='96px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] == "\u20DE":
            print("<svg viewBox='0 0 88 88' class='charwrapper lightsquare'>", file=outfile)
            if strep2[0] not in "\u27E1\u25C6\uF805":
                print("<text y='72px' x='36px' text-anchor='middle' font-size='72px'>", file=outfile)
            else:
                print("<text y='86px' x='42px' text-anchor='middle' font-family='Nishiki-teki' font-size='118px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2[-1] == "\u20DF":
            print("<svg viewBox='-2 -2 80 80' class='charwrapper lightdiamond'>", file=outfile)
            print("<text y='54px' x='36px' text-anchor='middle' font-size='48px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text><polygon points='0,36 36,72 72,36 36,0' class='enclosure' /></svg>", file=outfile)
        elif strep2[-1] == "\u20E4" and strep2[0] != "\u25B4":
            print("<svg viewBox='0 0 88 88' class='charwrapper lighttriangle'>", file=outfile)
            print("<text y='76px' x='42px' text-anchor='middle' font-size='42px'>", file=outfile)
            print(strep2[:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text><polygon points='2,82 86,82 44,6' class='enclosure' /></svg>", file=outfile)
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
            print("<text y='72px' x='{:d}px' text-anchor='middle' font-size='72px'>".format(
                  int(hsf * 24 + 0.5)), file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[0]), end="", file=outfile)
            print(strep2[1:-1], end="", file=outfile)
            print("<tspan font-size='0px'>{}</tspan>".format(strep2[-1]), file=outfile)
            print("</text></svg>", file=outfile)
        elif strep2 == "\u262F":
            invert_rotate(strep2, 0, True, strep2, False, outfile)
        elif ucd.normalize("NFC", strep2) != strep2:
            # Not strictly supposed to have non-NFC verbatim characters in HTML (escape them).
            print(strep2.encode("ascii", errors="xmlcharrefreplace").decode("ascii"), file=outfile)
        elif len(strep2) >= 3 and all(namedata.east_asian_width(ii) == "W" for ii in strep2):
            halflen = math.ceil(len(strep2) / 2)
            maybe_vertical = " vertical" if i[0] == 0xF863 else ""
            print(f"<span class='fourwideliga{maybe_vertical}' style='font-size: {1.5 / halflen}rem;'>", file=outfile)
            print(strep2[:halflen] + "<br aria-hidden=true>" + strep2[halflen:], file=outfile)
            print("</span>", file=outfile)
        elif strep != strep2 and len(strep2) == 1:
            print(f"<span class=ivind>〾</span>{strep2}", file=outfile)
        else:
            print(strep2, file=outfile)
    print("</span>", file=outfile)




