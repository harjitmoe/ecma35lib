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

plane = (1, ("Adobe-Korea1<br>KSCpc-EUC", "Apple for<br>Unicode 2.1", "Apple for<br>Unicode 3.2", "Apple for<br>Unicode 4.0", "Suggested<br>My choices", "PUA Scheme<br>Nishiki-teki"), [
          graphdata.gsets["mac-elex-extras-adobe"][2],
          graphdata.gsets["mac-elex-extras-unicode2_1"][2],
          graphdata.gsets["mac-elex-extras-unicode3_2"][2],
          graphdata.gsets["mac-elex-extras-unicode4_0"][2],
          graphdata.gsets["mac-elex-extras"][2],
          graphdata.gsets["mac-elex-extras-nishiki-teki"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "HangulTalk additional plane"
    return ""

def kutenfunc(number, row, cell):
    cellbyte = 0x40 + cell
    if cellbyte > 0x7D:
        cellbyte += 3
    if cellbyte == 0xA1: # not elif
        cellbyte = 0xFF
    euc = "0x{:02X}{:02X}".format(0xA0 + row, cellbyte)
    anchorlink = "<a href='#{:d}.{:d}.{:d}'>{}</a>".format(number, row, cell, euc)
    pseudokuten = "(Ψ-{:02d}-{:02d})".format(row, cell)
    pointer = (row - 1) * 94 + cell - 1
    cid = korea.elex2cid[pointer]
    ciddisplay = ""
    if cid:
        ciddisplay = f"<br>CID-{cid}"
    return f"{anchorlink}<br>{pseudokuten}{ciddisplay}"

annots = {
    (1, 4, 85): 'Unlike Ψ-07-40, the radii are not supposed to extend beyond the arc.&ensp;However, '
                'the arc is still supposed to extend beyond the radii.&ensp;Unlike Ψ-07-58, this '
                'is supposed to open rightward, i.e. with the arc due right of the radii.',
    (1, 6, 22): 'This is also included in Adobe-Japan1 as CID-12242.',
    (1, 6, 23): 'This is also included in Adobe-Japan1 as CID-12244.',
    (1, 6, 24): 'This is also included in Adobe-Japan1 as CID-12243.',
    (1, 6, 25): 'This is also included in Adobe-Japan1 as CID-12245.',
    (1, 6, 29): 'These four are also in Adobe-Japan1 as CIDs 12261, 12262, 12265 and 12266; in'
                'spite of their Apple mappings, they nominally fill the em square and so are much '
                'larger than a typical guillemet.&ensp;Compare 01-01-76 and 01-01-77.',
    (1, 6, 31): 'These two are not backhand <em>per se</em>, but they are otherwise duplicates of '
                '01-02-48 and 01-02-49 in the Wansung plane so this is a mapping by '
                'elimination.&ensp;See also the four manicules starting Ψ-12-74 (these ones\' '
                'proportions match the second pair).',
    (1, 6, 32): 'This is also included in Adobe-Japan1 as CID-12246.',
    (1, 6, 34): 'This is also included in Adobe-Japan1 as CID-12233.',
    (1, 6, 35): 'This is also included in Adobe-Japan1 as CID-12231.',
    (1, 6, 36): 'This is also included in Adobe-Japan1 as CID-12232.',
    (1, 6, 37): 'This is also included in Adobe-Japan1 as CID-12230.',
    (1, 6, 38): 'This is also included in Adobe-Japan1 as CID-12234.',
    (1, 6, 39): 'This is also included in Adobe-Japan1 as CID-12235.',
    (1, 6, 44): 'This is also included in Adobe-Japan1 as CID-12241.&ensp;'
                'Adobe concords with Apple\'s mapping.',
    (1, 6, 50): 'This is also in Adobe-Japan1 as CID-12260.&ensp;Apple\'s mapping is an approximation, '
                'albeit one where no superior alternative has since arisen&mdash;it is supposed '
                'to be a rotated 3×3 chequerboard; like ❖, but with a fifth, central lozenge.',
    (1, 6, 51): 'This is also included in Adobe-Japan1 as CID-12259.&ensp;'
                'Adobe concords with Apple\'s mapping.',
    (1, 6, 57): 'This is also in Adobe-Japan1 as CID-12258 and is an outline of Ψ-06-50—see there '
                'for comments on mapping and intended appearance.',
    (1, 6, 58): 'This is also in Adobe-Japan1 as CID-12257 and is an outline of Ψ-06-51.',
    (1, 6, 60): 'The previous two characters are five-petal florettes which are also in '
                'Adobe-Japan1, as CID-12228 and CID-12229 respectively.&ensp;The former is nominally '
                'an outline of the latter.&ensp;Adobe does not map them in Adobe-Korea1, but maps '
                'them in Adobe-Japan1 to U+2740 and U+273F, respectively; the Source Han (Noto '
                'CJK) glyphs for those codepoints correspond well with to the Adobe-Korea1 and '
                'Adobe-Japan1 reference glyphs.</p><p>Apple uses U+2740 for Ψ-06-86, '
                'however.&ensp;Rendering of U+2740 and U+273F '
                'varies across fonts; however, both are usually shown with five petals, as '
                'opposed to Ψ-06-86\'s four.&ensp;U+2740\'s reference glyph isn\'t purely an '
                'outline, but both reference glyphs have five petals.',
    (1, 6, 61): 'This is nominally like an elongated bold equals sign stretching across the mid '
                'line of the whole em square, bolder than the nominal 01-01-75, but still '
                'nominally much less bold/tall than U+3013 is typically shown in fonts.',
    (1, 6, 67): 'This is supposed to have four outlined petals partly obscuring a filled square '
                'in lozenge alignment.&ensp;No closer mapping exists that I know of.&ensp;Compare '
                'Ψ-06-52 and Ψ-06-83.',
    (1, 6, 74): 'This is Caslon Ornament Pica-7, which is a white (i.e. outlined) eight-petal '
                'florette.&ensp;U+2741 (from Zapf Dingbats) is also an eight-petal florette, '
                'but is an "outlined black" one (i.e. filled in, plus a padded outline around '
                'it).&ensp;Bodoni Ornament 642 (Nishiki-teki PUA FEF1F) is also a white '
                'eight-petal florette, but the HangulTalk character is nominally oriented like the '
                'Caslon one (with two petals up), not the Bodoni and Zapf ones (one petal up).',
    (1, 6, 75): 'The top and bottom squares should be filled (like Ψ-06-51), and the left and '
                'right ones should be outlined (like Ψ-06-58).',
    (1, 6, 76): 'This is also in Adobe-Japan1 as CID-12220, and consists of five vertical lines.',
    (1, 6, 79): 'Apple notes this one to be "Buddhist swastika, duplicate of 0xD8B3".&ensp;The '
                'religious symbol and the hanja have since been disunified by Unicode, so it is '
                'no longer a duplicate mapping as such.',
    (1, 6, 80): 'Nominally this has the BG colour on the top, and the bulbs due anticlockwise of '
                'their tails.&ensp;Dots are nominally omitted.&ensp;This corresponds to the '
                'symbol\'s appearance on the South Korean flag, but in background and foreground '
                'rather than red and blue.&ensp;Contrast Ψ-06-84 and Ψ-06-85 below.&ensp;Unicode '
                'unifies all orientations of the symbol.',
    (1, 6, 84): 'Nominally this has the BG colour on the bottom, and the bulbs due anticlockwise '
                'of their tails.&ensp;Dots are nominally omitted.&ensp;See Ψ-06-80 above.',
    (1, 6, 85): 'Nominally this has the BG colour on the right, and the bulbs due anticlockwise of '
                'their tails.&ensp;Dots are nominally omitted.&ensp;See Ψ-06-80 above.',
    (1, 6, 86): 'Contrast with Ψ-06-59 above.&ensp;Unlike that one, this one is expected to have '
                'four petals rather than five, and five central dots (four anthers, one on each '
                'petal, and a stigma) rather than being purely an outline.',
    (1, 7, 33): 'This differs from Ψ-07-58, in that it is merely a sector as an outlined plane '
                'shape, with neither the radii nor the arc crossing or extending beyond one '
                'another.',
    (1, 7, 37): 'U+29E7 was added in Unicode 3.2, hence it is unclear why Apple didn\'t use it.&ensp;'
                'It is named THERMODYNAMIC, but has been given the informative alias "record mark" '
                'at some point.&ensp;Compare the group mark (Ψ-07-46), which was added in Unicode '
                '10.',
    (1, 7, 40): 'This differs from Ψ-04-85, in that the radii extend beyond the arc.',
    (1, 7, 58): 'Unlike Ψ-07-33, this is supposed to have the arc extending beyond the radii.&ensp;'
                'Unlike Ψ-04-85, it is supposed to open upward (i.e. with the arc above the '
                'radii).&ensp;U+29A1 isn\'t exactly the same (its radii usually extend beyond the '
                'arc, while the arc may or may not cross the radii, depending on font) but it '
                'avoids a lossy mapping—although it was added in Unicode 3.2 and so that raises '
                'the question of why Apple didn\'t switch to it.&ensp;Compare the issue with '
                'Ψ-07-40 versus Ψ-04-85.',
    (1, 7, 62): 'These two are respectively the horizontal and vertical forms of jusikhoesa, i.e. '
                'are a direct hangul transcription of the ㍿ ligature (Korean reading jusikhoesa, '
                'Japanese reading kabushikikaisha, English UCS name SQUARE CORPORATION).&ensp;'
                'Hence, compare KanjiTalk 7\'s JIS 01-14-92.',
    (1, 7, 63): 'Duplicate of Ψ-11-04.&ensp;Means "print".',
    (1, 7, 64): 'Differs from Ψ-07-63 (and Ψ-11-04) in its circle being dashed not solid.',
    (1, 7, 67): 'Emphasised (nominally italicised) version of Ψ-07-65.',
    (1, 8, 73): 'Most fonts show U+2939\'s head pointing SW rather than the south intended here.&ensp;'
                '<a href="https://www.fileformat.info/info/unicode/char/2939/fontsupport.htm">'
                'PragmataPro is apparently one exception.</a>',
    (1, 8, 81): 'This is a cross barby, which has meanings as diverse as a "move window" cursor, '
                'or a symbol of Nazism or white supremacy, amongst other uses.',
    (1, 11, 4): 'Duplicate of Ψ-07-63; the version with affixed PUA F87F is already used for '
                'Ψ-07-64, so Apple maps to the combining sequence for round tripping.',
    (1, 11, 36): 'U+329F has existed since Unicode 1.x and is not mapped elsewhere, so it is '
                 'thoroughly unclear why Apple did not map to it.&ensp;It already existing is why '
                 'it is absent from the Nishiki-teki PUA range covering the others.',
    (1, 12, 77): 'The latter two are not backhand <em>per se</em>, but have their palms drawn '
                 'larger.&ensp;Compare with Ψ-06-30 and Ψ-06-31, which match the latter two\'s '
                 'proportions, and where my by-elimination mappings assign the other two backhand '
                 'manicules.',
}

warning = """\
All HangulTalk extension characters with trail bytes in the range 0x41–0x5A, 0x61–0x7A or \
0x81–0xA0 (i.e. all except those with trail bytes 0x5B–0x60 or 0x7B–0x7D) collide with \
Unified Hangul Code extended syllables.&ensp;This is not shown below since it is regular, \
affects most of the table, would make the areas of the table which are actually of note harder \
to spot, and would misrepresent Unified Hangul Code since their ranges only partly overlap."""

for q in range(1, 7):
    f = open("htxplane1{}.html".format(chr(0x60 + q)), "w", encoding="utf-8")
    lasturl = lastname = nexturl = nextname = None
    if q > 1:
        lasturl = "htxplane1{}.html".format(chr(0x60 + q - 1))
        lastname = f"HangulTalk additional plane, part {q-1:d}"
    else:
        lasturl = "kscplane4f.html"
        lastname = "KSC plane 4 (KS X 1027-2), part 6"
    if q < 6:
        nexturl = "htxplane1{}.html".format(chr(0x60 + q + 1))
        nextname = f"HangulTalk additional plane, part {q+1:d}"
    showgraph.dump_plane(f, planefunc, kutenfunc, *plane, lang="ko-KR", part=q, css="/css/codechart.css",
                         menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                         lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                         annots=annots, selfhandledanchorlink=True, planewarn=warning,
                         pua_collides=True, showbmppuas=(0, 0, 0, 0, 0, 1), siglum="KSC")
    f.close()









