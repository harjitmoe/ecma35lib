#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import korea, cellemojidata
from ecma35.data import graphdata, showgraph
import json

plane1 = (1, ("Original 926<br/>Reconstruct", "IBM 926/944<br/>Main Plane", "IBM 926/944<br/>PUA Roundtrip"), [
          graphdata.gsets["oldibmkorea-excavated"][2],
          graphdata.gsets["oldibmkorea"][2],
          graphdata.gsets["oldibmkorea-withcorppua"][2]
])

def to_shiftkorea(men, ku, ten):
    if men == 2:
        # TODO this shan't be correct: Shift Korea has more allocatable rows than Shift JIS.
        if ku < 16:
            order = (1, 8, 3, 4, 5, 12, 13, 14, 15)
            if ku not in order:
                return ""
            ku = order.index(ku) + 95
        elif ku >= 78:
            ku = (ku - 78) + 104
        else:
            return ""
    sward = (ku - 1) >> 1
    spos = (((ku - 1) & 0x1) * 94) + ten - 1
    lead = sward + 0x81
    trail = spos + 0x40
    if trail >= 0x7F:
        trail += 1
    if men == 2:
        # TODO this shan't be correct, see above
        return "<br>{:02d}-{:02d}<br>(IBM-944 {:02x}{:02x})".format(
                ku, ten, lead, trail)
    else:
        return "<br>(PCData {:02x}{:02x})".format(lead, trail)

titles = [
    "Old IBM Korea PC-Data Main Plane"
]

def planefunc(number, mapname=None):
    if mapname is None:
        return titles[number - 1]
    return ""

subsigla = "_Ω"

def kutenfunc(number, row, cell):
    if cell >= 0:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}-{:02d}-{:02d}</a>".format(
                     number, row, cell, subsigla[number], row, cell)
    else:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}-{:02d}-{}</a>".format(
                     number, row, -cell, subsigla[number], row, 
                     "{:02d}+".format(-cell) if cell != -1 else "*")
    anchorlink += to_shiftkorea(number, row, cell)
    return anchorlink

annots = {
    (1, 1, 0): 'Row 1 partly overlaps, and possibly predates, row 1 in KS X 1001.&ensp;But '
               'KS X 1001 changes 01-42 (Ω-01-42 is Kelvin, 01-01-42 is Ångström) and 01-46 '
               'through 01-54 (Ω-01-46 through Ω-01-54 get scattered through row 7, whereäs '
               '01-01-46 through 01-01-54 are entirely different).</p><p>From 01-76 onward they '
               'do not correspond, 01-78 onward actually infill characters from KS X 1001, '
               'in KS X 1001 order, that aren\'t otherwise included.&ensp;This infilling does not '
               'entirely fit in this row, and re-commences at Ω-09-01.&ensp;IBM-933 (HostData) mostly '
               'follows this (where cell 1 is 0x41) but makes some swaps.</p><p>The row starts off '
               'with KS X 1001 temporarily coupled.',
    (1, 1, 33): 'Mapping notwithstanding, Ω-01-33 is a not-equals sign with a slash as opposed to '
                'backslash; contrast Ω-01-78.',
    (1, 1, 42): 'Turned from Kelvin to Ångström in KS X 1001.',
    (1, 1, 43): 'Ω-01-43 is changed to a fullwidth caret (fullwidth ASCII circumflex) in IBM-933 '
                '(since its row 2 EBCDIC has a cent but not a caret).',
    (1, 1, 45): 'KS X 1001 temporarily decouples after here.',
    (1, 1, 54): 'KS X 1001 temporarily recouples after here.',
    (1, 1, 75): 'KS X 1001 permanently decouples after here.',
    (1, 1, 77): 'Ω-01-76 and Ω-01-77 are changed to fullwidth square brackets in IBM-933 (since '
                'its row 2 EBCDIC has a broken bar and not-sign, but not square brackets).</p><p>'
                'The characters in this row following this point are infilled from the subset of the '
                'repertoire of KS X 1001 row 1, in KS X 1001 order, which isn\'t included in this '
                'row before this point.&ensp;However, Ω-01-78, Ω-01-79 and Ω-01-80 are doublets of '
                'Ω-01-33, Ω-01-34 and Ω-01-35, since the latter three evidently weren\'t seen as '
                'close enough matches to the KS X 1001 characters, despite being in a range where '
                'KS X 1001 is actually following this row.',
    (1, 1, 78): 'Mapping notwithstanding, Ω-01-78 is a not-equals sign with a backslash; contrast '
                'Ω-01-33.',
    (1, 2, 0): 'Row 2 is fullwidth KS X 1003, thus the same as KS X 1001\'s row 3 '
               '(01-03-01).&ensp;IBM-933 (HostData) uses an EBCDIC-based layout instead.',
    (1, 3, 0): 'Row 3 is basically fullwidth KS X 1001-1974, but with empty space infilled with '
               'the obsolete jamo from KS X 1001 01-04-53 through 01-04-94.&ensp;IBM-933 (HostData) '
               'includes the obsolete jamo consecutively instead, since it encodes the modern jamo '
               'as Johab.',
    (1, 4, 0): 'Row 4 matches JIS X 0208 and GB 2312 (see JIS 01-04-01) and therefore row 10 in '
               'KS X 1001 (see 01-10-01).&ensp;IBM-933 concords.',
    (1, 5, 0): 'Row 5 matches JIS X 0208 and GB 2312 (see JIS 01-05-01) and therefore row 11 in '
               'KS X 1001 (see 01-11-01).&ensp;IBM-933 concords.',
    (1, 6, 0): 'Row 6 matches row 5 in KS X 1001 (see 01-05-01), without the arrangement reflowing '
               'that were done to the Cyrillic, which suggests the textual dependency is earlier '
               'rather than simultaneous with the Cyrillic (i.e. KS X 1001 row 5 probably '
               'copied this row, not <i>vice versa</i>).&ensp;IBM-933 concords.',
    (1, 7, 0): 'Row 7 matches row 6 in KS X 1001 (see 01-06-01).&ensp;The direction of this '
               'dependency is unclear.&ensp;IBM-933 concords.',
    (1, 8, 0): 'Row 8 includes the portion of the repertoire from row 7 in KS X 1001 (see 01-07-01) '
               'that did not appear in row 1, preserving KS X 1001 order but with arrangement '
               'reflowed to avoid gaps.&ensp;IBM-933 concords.',
    (1, 9, 0): 'Row 8 includes the portion of the repertoire from rows 1 and 2 of KS X 1001 that did '
               'not appear in row 1 (beginning with KS X 1001 01-01-80), preserving KS X 1001 order '
               'but with arrangement reflowed.&ensp;After these is appended Ω-09-84, which is similar '
               'to Ω-01-40 and is of unclear purpose for inclusion, but was clearly added after the '
               'infill.&ensp;IBM-933 concords.',
    (1, 10, 0): 'Row 8 includes the Cyrillic repertoire from row 12 of KS X 1001 (starting 01-12-01), '
                'preserving KS X 1001 order but with arrangement reflowed to avoid gaps.&ensp;Contrast '
                'how the Greek characters were handled in row 6.&ensp;IBM-933 concords.',
    (1, 11, 0): 'Here commences IBM\'s original pre-1987 selection of pre-composed syllables.&ensp;'
                'No other code page still preserves this information, since IBM-933 uses Johab for '
                'syllables (so those that were in from the start cannot be distinguished using '
                'IBM-933 alone from those that were added from KS X 1001-1987, except those that '
                'aren\'t in the latter).',
    (1, 37, 0): 'This block of syllables contains those which were included in KS X 1001-1987 but '
                'not in IBM\'s original selection.&ensp;IBM-933 uses Johab for syllables.',
    (1, 41, 0): 'This block of hanja matches 0x5041 through 0x67C2 (shift out) in IBM-933.&ensp;'
                'Mappings to the Private Use Area (IBM\'s PUA scheme defined in code page 1449) '
                'mostly consist of duplicate characters that aren\'t duplicate (or have fewer '
                'duplicates) in KS X 1001, though some are unique and some of the favoured duplicates '
                'are in the extension range rather than the main plane (i.e. were themselves added '
                'from the KS X 1001 repertoire).&ensp;Most cases are IBM having two while KS X 1001 '
                'has one; IBM has three of 契 while KS X 1001 has two, whereäs 射 stands out very '
                'prominently by appearing in no fewer than four instances, in contrast to only one '
                'in KS X 1001.</p><p>Any KS X 1001 hanja (including Compatibility Ideographs) that '
                'either don\'t appear here or only appear here with a PUA mapping (in the applicable '
                'column) are encoded consecutively in IBM-944 as 115-01 through 123-13, i.e. beyond '
                'the main plane, and also in 0x6841 through 0x6C45 in IBM-933.',
    (1, 93, 1): 'Row 93 matches and is presumably taken from KS X 1001 row 8 (see 01-08-01).&ensp;It '
                'is also 0x4B41 through 0x4B9E in IBM-933 shift-out.',
    (1, 94, 1): 'Row 94 matches and is presumably taken from KS X 1001 row 9 (see 01-09-01).&ensp;It '
                'is also 0x4BA0 through 0x4BFD in IBM-933 shift-out.',
}

for n, p in enumerate([plane1]):
    for q in range(1, 7):
        bn = n + 1
        f = open("ibkplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        currentbit = titles[n]
        #
        if q > 1:
            lasturl = "ibkplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = f"{currentbit}, part {q-1:d}"
        elif bn > 1:
            lasturl = "ibkplane{:X}f.html".format(bn - 1)
            lastname = titles[n - 1] + ", part 6"
        else:
            lasturl = "htxplane1f.html"
            lastname = "HangulTalk additional plane, part 6"
        #
        if q < 6:
            nexturl = "ibkplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = f"{currentbit}, part {q+1:d}"
        elif bn < 1:
            nexturl = "ibkplane{:X}a.html".format(bn + 1)
            nextname = titles[n + 1] + ", part 1"
        #
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KR", part=q, css="../css/codechart.css",
                             menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, selfhandledanchorlink=True, siglum="KSC",
                             pua_collides=True)
        f.close()









