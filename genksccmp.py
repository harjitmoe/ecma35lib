#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import korea, cellemojidata
from ecma35.data import graphdata, showgraph
import json, os

plane1 = (1, ("Old UTC<br>Ported", "IBM", "Macintosh", "MS/New UTC<br>Unicode 2.0", "MS/HTML5<br>1998 Update", "2002 Update<br>MS-Style"), [
          graphdata.gsets["ir149-altutc"][2],
          graphdata.gsets["ir149-ibm"][2],
          graphdata.gsets["ir149-mac"][2],
          graphdata.gsets["ir149"][2],
          graphdata.gsets["ir149-1998"][2],
          graphdata.gsets["ir149-2002"][2],
])

plane2 = (2, ("KS X 1002<br>No symbols"), [
          graphdata.gsets["ksx1002"][2],
])

plane3 = (3, ("KS X 1027-1<br>Unihan"), [
          graphdata.gsets["ksx1027_1"][2],
])

plane4 = (4, ("KS X 1027-2<br>Unihan"), [
          graphdata.gsets["ksx1027_2"][2],
])

plane5 = (5, ("Apple<br>Unicode 2.1", "Apple<br>Unicode 3.2", "Apple<br>Unicode 4.0", "Output", "Output<br>Nishiki-teki PUA"), [
          graphdata.gsets["mac-elex-extras-unicode2_1"][2],
          graphdata.gsets["mac-elex-extras-unicode3_2"][2],
          graphdata.gsets["mac-elex-extras-unicode4_0"][2],
          graphdata.gsets["mac-elex-extras"][2],
          graphdata.gsets["mac-elex-extras-nishiki-teki"][2],
])

titles = [
    "KSC plane 1 (Wansung)",
    "KSC plane 2 (KS X 1002)",
    "KSC plane 3 (KS X 1027-1)",
    "KSC plane 4 (KS X 1027-2)",
    "HangulTalk additional plane",
]

def planefunc(number, mapname=None):
    if mapname is None:
        return titles[number - 1]
    else:
        return ""

def kutenfunc(number, row, cell):
    if cell >= 0:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}-{:02d}-{:02d}</a>".format(
                     number, row, cell, f"{number:02d}" if number != 5 else "Ψ", row, cell)
    else:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}-{:02d}-{}</a>".format(
                     number, row, -cell, f"{number:02d}" if number != 5 else "Ψ", row, 
                     "{:02d}+".format(-cell) if cell != -1 else "*")
    #
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
        fmteuc = "<br>(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
    elif number < 5:
        fmteuc = ""
    elif cell < 0:
        cellbyte = 0x40 - cell
        if cellbyte > 0x7D:
            cellbyte += 3
        euc = "{:02X}{:02X}".format(0xA0 + row, cellbyte)
        if cellbyte < 0x70:
            fmteuc = "<br><nobr>(Mac {}_)</nobr><br/>(EUC-ish ".format(euc[:-1])
        elif cellbyte == 0x70:
            fmteuc = "<br>(Mac {}_, {}81-2)<br/>(EUC-ish ".format(euc[:-1], euc[:-2])
        else:
            fmteuc = "<br><nobr>(Mac {}+)</nobr><br/>(EUC-ish ".format(euc)
        fmteuc += "1B4F{:02X}{:X}_)".format(0xa0 + row, (0xA0 - cell) >> 4)
    else:
        cellbyte = 0x40 + cell
        if cellbyte > 0x7D:
            cellbyte += 3
        if cellbyte == 0xA1: # not elif
            cellbyte = 0xFF
        euc = "{:02X}{:02X}".format(0xA0 + row, cellbyte)
        fmteuc = "<br>(MacKR {})".format(euc)
    return "{}{}".format(anchorlink, fmteuc)

cdispmap = {}
for n, i in enumerate(korea.rawmac):
    j = graphdata.gsets["ir149-mac"][2][n]
    if j != i:
        cdispmap[(n, j)] = i
for n, i in enumerate(korea.oldunicodeksc):
    j = graphdata.gsets["ir149-altutc"][2][n]
    if j != i:
        cdispmap[(plane1[1][0], n, j)] = i
annots = {
    (1, 1, 75): 'This KS C 6501 character is a "bad character mark", i.e. geta mark, although its '
                'rendition in the code chart is significantly less bold than fonts tend to show '
                'it, being closer to an elongated equals sign.&ensp;Compare the nominally bolder, '
                'but still nominally much less bold/tall than typical display, mark at Ψ-06-61.',
    (1, 1, 77): 'Compare these two with Ψ-06-28 and Ψ-06-29.',
    (5, 6, 22): 'This is CID-12242 in Adobe-Japan1.',
    (5, 6, 23): 'This is CID-12244 in Adobe-Japan1.',
    (5, 6, 24): 'This is CID-12243 in Adobe-Japan1.',
    (5, 6, 25): 'This is CID-12245 in Adobe-Japan1.',
    (5, 6, 29): 'These four are CIDs 12261, 12262, 12265 and 12266 in Adobe-Japan1 which, in '
                'spite of their Apple mappings, nominally fill the em square and so are much '
                'larger than a typical guillemet.&ensp;Compare 01-01-76 and 01-01-77.',
    (5, 6, 31): 'These two are not backhand <em>per se</em>, but they are otherwise duplicates of '
                '01-02-48 and 01-02-49 in the Wansung plane so this is a mapping by '
                'elimination.&ensp;See also the four manicules starting Ψ-12-74 (these ones\' '
                'proportions match the second pair).',
    (5, 6, 32): 'This is CID-12246 in Adobe-Japan1.',
    (5, 6, 34): 'This is CID-12233 in Adobe-Japan1.',
    (5, 6, 35): 'This is CID-12231 in Adobe-Japan1.',
    (5, 6, 36): 'This is CID-12232 in Adobe-Japan1.',
    (5, 6, 37): 'This is CID-12230 in Adobe-Japan1.',
    (5, 6, 38): 'This is CID-12234 in Adobe-Japan1.',
    (5, 6, 39): 'This is CID-12235 in Adobe-Japan1.',
    (5, 6, 44): 'This is CID-12241 in Adobe-Japan1.&ensp;Adobe concords with Apple\'s mapping.',
    (5, 6, 50): 'This is CID-12260 in Adobe-Japan1.&ensp;Apple\'s mapping is an approximation, '
                'albeit one where no superior alternative has since arisen&mdash;it is supposed '
                'to be a rotated 3×3 checquerboard; like ❖, but with a fifth, central lozenge.',
    (5, 6, 51): 'This is CID-12259 in Adobe-Japan1.&ensp;Adobe concords with Apple\'s mapping.',
    (5, 6, 57): 'This is CID-12258 in Adobe-Japan1 and is an outline of Ψ-06-50—see there for '
                'comments on mapping and intended appearance.',
    (5, 6, 58): 'This is CID-12257 in Adobe-Japan1 and is an outline of Ψ-06-51.',
    (5, 6, 60): 'The previous two characters correspond to CID-12228 and CID-12229 in Adobe-Japan1 '
                'respectively.&ensp;Adobe maps them to U+2740 and U+273F respectively.&ensp;'
                'Apple uses U+2740 for Ψ-06-86, however.',
    (5, 6, 61): 'This is nominally like an elongated bold equals sign stretching across the mid '
                'line of the whole em square, bolder than the nominal 01-01-75, but still '
                'nominally much less bold/tall than U+3013 is typically shown in fonts.',
    (5, 6, 74): 'This is Caslon Ornament Pica-7, which is a white (i.e. outlined) eight-petal '
                'florette.&ensp;U+2741 (from Zapf Dingbats) is also an eight-petal florette, '
                'but is an "outlined black" one (i.e. filled in, plus a padded outline around '
                'it).&ensp;Bodoni Ornament 642 (Nishiki-teki PUA FEF1F) is also a white '
                'eight-petal florette, but the HangulTalk character is nominally oriented like the '
                'Caslon one (with two petals up), not the Bodoni and Zapf ones (one petal up).',
    (5, 6, 75): 'The top and bottom squares should be filled (like Ψ-06-51), and the left and '
                'right ones should be outlined (like Ψ-06-58).',
    (5, 6, 76): 'This is CID-12220 in Adobe-Japan1, and consists of five vertical lines.',
    (5, 6, 79): 'Apple notes this one to be "Buddhist swastika, duplicate of 0xD8B3".&ensp;The '
                'religious symbol and the hanja have since been disunified by Unicode, so it is '
                'no longer a duplicate mapping as such.',
    (5, 6, 80): 'Nominally this has the light on the top, and the bulbs due anticlockwise of '
                'their tails.&ensp;Dots are nominally omitted.&ensp;This corresponds to the '
                'symbol\'s appearance on the South Korean flag, but in white and black (or whatever '
                'the foreground and background are) rather than red and blue.&ensp;Unicode '
                'unifies all orientations of the symbol.',
    (5, 6, 84): 'Nominally this has the light on the bottom, and the bulbs due anticlockwise of '
                'their tails.&ensp;Dots are nominally omitted.&ensp;See Ψ-06-80 above.',
    (5, 6, 85): 'Nominally this has the light on the right, and the bulbs due anticlockwise of '
                'their tails.&ensp;Dots are nominally omitted.&ensp;See Ψ-06-80 above.',
    (5, 7, 62): 'These two are respectively the horizontal and vertical forms of jusikhoesa, i.e. '
                'are a direct hangul transcription of the ㍿ ligature (Korean reading jusikhoesa, '
                'Japanese reading kabushikikaisha, English UCS name SQUARE CORPORATION).',
    (5, 7, 63): 'Duplicate of Ψ-11-04.&ensp;Means "print".',
    (5, 7, 64): 'Differs from Ψ-07-63 (and Ψ-11-04) in its circle being dashed not solid.',
    (5, 7, 67): 'Emphasised (nominally italicised) version of Ψ-07-65.',
    (5, 8, 73): 'Most fonts show U+2939\'s head pointing SW rather than the south intended here.&ensp;'
                '<a href="https://www.fileformat.info/info/unicode/char/2939/fontsupport.htm">'
                'PragmataPro</a> is apparently one exception.',
    (5, 8, 81): 'This is a cross barby, which has meanings as diverse as a "move window" cursor, '
                'or a symbol of Nazism or white supremacy, amongst other uses.',
    (5, 11, 4): 'Duplicate of Ψ-07-63; the version with affixed PUA FE7F is already used for '
                'Ψ-07-64, so Apple maps to the combining sequence for round tripping.',
    (5, 12, 77): 'The latter two are not backhand <em>per se</em>, but have their palms drawn '
                 'larger.&ensp;Compare with Ψ-06-30 and Ψ-06-31, which match the latter two\'s '
                 'proportions, and where my by-elimination mappings assign the other two backhand '
                 'manicules.',
}

for n, p in enumerate([plane1, plane2, plane3, plane4, plane5]):
    for q in range(1, 7):
        bn = n + 1
        f = open("kscplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        currentbit = titles[n]
        #
        if q > 1:
            lasturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = f"{currentbit}, part {q-1:d}"
        elif bn > 1:
            lasturl = "kscplane{:X}f.html".format(bn - 1)
            lastname = titles[n - 1] + ", part 6"
        #
        if q < 6:
            nexturl = "kscplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = f"{currentbit}, part {q+1:d}"
        elif bn < 5:
            nexturl = "kscplane{:X}a.html".format(bn + 1)
            nextname = titles[n + 1] + ", part 1"
        #
        noallocatenotice = None
        planewarn = None
        if bn == 2:
            noallocatenotice = ("Established or deployed mappings do not exist for rows 1&ndash;15 "
                                "of KS X 1002, although they are not empty.&ensp;See also "
                                "<a href='https://twitter.com/ken_lunde/status/398651431072575488'>"
                                "this excerpt of row 12 and part of 11</a> and "
                                "<a href='https://charset.fandom.com/ko/wiki/KS_X_1002'>this "
                                "speculative table</a>.")
            planewarn = ("Rows 1&ndash;15 and 37&ndash;54 are not empty, although they are not "
                         "shown since established or deployed mappings do not exist.&ensp;See "
                         "also <a href='https://twitter.com/ken_lunde/status/398651431072575488'>"
                         "this excerpt of row 12 and part of 11</a> and "
                         "<a href='https://charset.fandom.com/ko/wiki/KS_X_1002'>this speculative "
                         "table</a>.")
        if bn == 4:
            planewarn = ("My sole source for the mapping of KS X 1027-2 is the Unihan database; "
                         "the frequent gaps are likely supposed to contain other hanja characters "
                         "which are either absent from Unicode, or where KS X 1027-2 is not "
                         "listed as their South Korean source mapping.")
        #
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ko-KR", part=q, css="codechart.css",
                             menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True,
                             pua_collides=True, showbmppuas=None if (bn != 5) else (0, 0, 0, 0, 1),
                             noallocatenotice=noallocatenotice, planewarn=planewarn,
                             skiprows = range(37, 55) if bn == 2 else None, siglum="KSC")
        f.close()









