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

plane = (1, ("Adobe-Korea1<br>KSCpc-EUC", "Apple for<br>Unicode 2.1", "Apple for<br>Unicode 3.2", "Apple for<br>Unicode 4.0", "Updated<br>Illustrative", "PUA Scheme<br>Nishiki-teki"), [
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
    (1, 6, 20): 'The above\'s Adobe reference glyph has eight spokes, but which extend to an '
                'invisible bounding square rather than being equal length.&ensp;This is well '
                'within <a href="https://www.fileformat.info/info/unicode/char/2747/fontsupport.htm">'
                'the established glyph variation for U+2747</a>, which is usually but not always '
                'shown with eight spokes.&ensp;Contrast Ψ-06-88.',
    (1, 6, 22): 'The character above is also included in Adobe-Japan1 as CID-12242.',
    (1, 6, 23): 'The character above is also included in Adobe-Japan1 as CID-12244.',
    (1, 6, 24): 'The character above is also included in Adobe-Japan1 as CID-12243.',
    (1, 6, 25): 'The character above is also included in Adobe-Japan1 as CID-12245.',
    (1, 6, 29): 'The above four are also in Adobe-Japan1 as CIDs 12261, 12262, 12265 and 12266; in '
                'spite of their Apple mappings, they nominally fill the em square and so are much '
                'larger than a typical guillemet.&ensp;Compare 01-01-76 and 01-01-77.',
    (1, 6, 31): 'These two are not backhand <em>per se</em>, but they are otherwise duplicates of '
                '01-02-48 and 01-02-49 in the Wansung plane so this is a mapping by '
                'elimination.&ensp;See also the four manicules starting Ψ-12-74 (these ones\' '
                'proportions match the second pair).',
    (1, 6, 32): 'The character above is also included in Adobe-Japan1 as CID-12246.',
    (1, 6, 34): 'The character above is also included in Adobe-Japan1 as CID-12233.',
    (1, 6, 35): 'The character above is also included in Adobe-Japan1 as CID-12231.',
    (1, 6, 36): 'The character above is also included in Adobe-Japan1 as CID-12232.',
    (1, 6, 37): 'The character above is also included in Adobe-Japan1 as CID-12230.',
    (1, 6, 38): 'The character above is also included in Adobe-Japan1 as CID-12234.',
    (1, 6, 39): 'The character above is also included in Adobe-Japan1 as CID-12235.',
    (1, 6, 44): 'The character above is also included in Adobe-Japan1 as CID-12241.&ensp;'
                'Adobe concords with Apple\'s mapping.',
    (1, 6, 50): 'The above is also in Adobe-Japan1 as CID-12260.&ensp;Apple\'s mapping is an '
                'approximation, albeit one where no superior alternative has since arisen (some '
                'glyphs for U+1F4A0 💠 are also somewhat similar, but not vastly moreso, not '
                'consistently so between fonts, and not so when looking at its reference '
                'glyph).&ensp;It is supposed to be a rotated 3×3 chequerboard: like ❖, but with '
                'a fifth, central lozenge.',
    (1, 6, 51): 'The character above is also included in Adobe-Japan1 as CID-12259.&ensp;'
                'Adobe concords with Apple\'s mapping.',
    (1, 6, 57): 'The above is also in Adobe-Japan1 as CID-12258 and is an outline of Ψ-06-50—see there '
                'for comments on mapping and intended appearance.',
    (1, 6, 58): 'The above is also in Adobe-Japan1 as CID-12257 and is an outline of Ψ-06-51.',
    (1, 6, 60): 'These two characters\' reference glyphs are flowers drawn as five separated '
                'heart-shaped petals, the former outlined, the latter filled.&ensp;Besides '
                'Adobe-Korea1, they are also included in Adobe-Japan1, as CID-12228 and CID-12229 '
                'respectively.&ensp;Adobe does not map them in Adobe-Korea1, but maps them in '
                'Adobe-Japan1 to U+2740 and U+273F, respectively; consequently, the Source Han '
                '(Noto CJK) glyphs for those codepoints correspond to the intended appearance of '
                'these characters.</p><p>Apple uses U+2740 for Ψ-06-86, however.&ensp;'
                'Rendering of U+2740 and U+273F varies across fonts; however, both are usually '
                'shown with five petals even in fonts that aren\'t influenced by Adobe-Japan1 '
                '(<a href="https://www.fileformat.info/info/unicode/char/2740/fontsupport.htm">'
                'though a small minority of fonts show U+2740 with ten, in two sets of five</a>), '
                'as opposed to Ψ-06-86\'s four.&ensp;U+2740\'s reference glyph isn\'t purely an '
                'outline, but both reference glyphs have five petals.',
    (1, 6, 61): 'This is nominally like an elongated bold equals sign stretching across the mid '
                'line of the whole em square, bolder than the nominal 01-01-75, but still '
                'nominally much less bold/tall than U+3013 is typically shown in fonts.',
    (1, 6, 67): 'This is supposed to have four outlined narrow diagonal petals partly obscuring a '
                'filled square in lozenge alignment.&ensp;No closer mapping exists that I know '
                'of.&ensp;Compare Ψ-06-52 and Ψ-06-83.',
    (1, 6, 70): 'The outer lozenge is nominally supposed to be pinched, similarly to ⯎.&ensp;'
                'Mapping to the newer U+1F7A0 is by elimination.',
    (1, 6, 74): 'The above is Caslon Ornament Pica-7, which is a white (i.e. outlined) eight-petal '
                'florette.&ensp;U+2741 (from Zapf Dingbats) is also an eight-petal florette, '
                'but is an "outlined black" one (i.e. filled in, plus a padded outline around '
                'it).&ensp;Bodoni Ornament 642 (Nishiki-teki PUA FEF1F) is also a white '
                'eight-petal florette, but the HangulTalk character is nominally oriented like the '
                'Caslon one (with two petals up), not the Bodoni and Zapf ones (one petal up).',
    (1, 6, 75): 'The top and bottom squares should be filled (like Ψ-06-51), and the left and '
                'right ones should be outlined (like Ψ-06-58).',
    (1, 6, 76): 'The above is also in Adobe-Japan1 as CID-12220, and consists of five vertical lines.',
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
    (1, 6, 86): 'Compare the mappings for Ψ-06-59 above.&ensp;Unlike that one, this one\'s nominal '
                'glyph is shown with four petals rather than five, and five central dots (four '
                'anthers, one on each petal, and a stigma) rather than being purely an '
                'outline.</p><p>U+2740 usually has five petals, and some Adobe-Japan1-influenced '
                'glyphs for it correspond closely to Ψ-06-59 (see commentary there).&ensp;By '
                'contrast, the newer U+1F33C has an unspecified number of petals (or ray florets), '
                'with the number varying widely between fonts, making it a better match on that '
                'basis alone.',
    (1, 6, 88): 'Ψ-06-88 can best be described as a starburst effect, though it also bears a '
                'certain resemblence to the helm wheel (U+2388 ⎈).&ensp;In its Adobe reference '
                'glyph, two concentric rings, four broad triangular rays in cardinal directions, '
                'and four narrower teardrop-shaped rays toward the corners of the character cell, '
                'radiate from the centre of the character.</p><p>Apple\'s Unicode mapping takes '
                'a sparkle character with a similar pattern of spoke widths, and superimposes one '
                'combining ring.&ensp;However, U+2748 is not mapped anywhere else (the character '
                'mapped at Ψ-06-20 is the related but distinct sparkle at U+2747) and, similarly '
                'to U+2747, glyphs for U+2748 '
                '<a href="https://www.fileformat.info/info/unicode/char/2748/fontsupport.htm">can '
                'and do vary</a>, so rendering U+2748 itself with concentric rings is not out of '
                'the question for a reasonable font.</p><p>The Nishiki-teki mapping shown is '
                'to a similar Caslon ornament (Long Primer 3), which shows the concentric rings '
                'but uses only one type of ray (and doesn\'t show the rays within the rings '
                'themselves).&ensp;No exact match exists in the Nishiki-teki PUA.',
    (1, 6, 92): 'Ψ-06-92 is supposed to be a classic rotary telephone dial, without the rest of '
                'the telephone.',
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
    (1, 7, 73): 'U+25AB dates from Unicode 1.x.&ensp;It is not mapped from elsewhere in MacKorean, '
                'hence it is unclear why it was not used as the mapping for the small outlined '
                'square here (avoiding the hint sequence).',
    (1, 8, 73): 'Most fonts show U+2939\'s head pointing SE rather than the south intended here.&ensp;'
                '<a href="https://www.fileformat.info/info/unicode/char/2939/fontsupport.htm">'
                'PragmataPro is apparently one exception.</a>',
    (1, 8, 81): 'This is a cross barby (arrowheads in all cardinals), which has meanings as diverse as '
                '<a href="https://docs.microsoft.com/en-us/dotnet/api/system.windows.input.cursors.sizeall">'
                'a "move window" cursor</a>, or a symbol of Nazism or white supremacy, amongst '
                'other uses.',
    (1, 8, 86): 'These two were switched in the earlier Apple mappings, as with Ψ-12-12 and '
                'Ψ-12-13.&ensp;The blurb for Apple\'s mapping file acknowledges these changes as '
                'being a fix of "switched mappings".',
    (1, 11, 4): 'Duplicate of Ψ-07-63; the version with affixed PUA F87F is already used for '
                'Ψ-07-64, so Apple maps to the combining sequence for round tripping.',
    (1, 11, 36): 'U+329F has existed since Unicode 1.x and is not mapped elsewhere, so it is '
                 'thoroughly unclear why Apple did not map to it.&ensp;It already existing is why '
                 'it is absent from the Nishiki-teki PUA range covering the others.',
    (1, 12, 13): 'These two were switched in the earlier Apple mappings, as with Ψ-08-85 and '
                 'Ψ-08-86.&ensp;The blurb for Apple\'s mapping file acknowledges these changes as '
                 'being a fix of "switched mappings".',
    (1, 12, 17): 'Ψ-12-16 and Ψ-12-17 nominally have longer stems on the non-arrow side of the '
                 'arc compared to the conventional appearance of their Unicode mappings.',
    (1, 12, 19): 'Ψ-12-18 and Ψ-12-19 are supposed to take the form of an S and a backward S '
                 'respectively, with the arrows in the upper corners pointing rightward and '
                 'leftward respectively.&ensp;Their Unicode mappings, rather, nominally have the '
                 'form of a tilde and reversed tilde respectively&mdash;though they are likewise '
                 '"wave arrows", and they point toward the same corner of the character cell.',
    (1, 12, 20): 'Ψ-12-20 points downward toward the bottom-left corner of the character cell, '
                 'after following a curvature resembling a ∿.&ensp;No especially close Unicode '
                 'character exists; U+2B4D is probably the closest, although the similar U+21AF ↯ '
                 'was presumably passed over by Apple\'s mapping, since the latter dates to '
                 'Unicode 1.x.</p><p>U+2B5A ⭚ and U+2B5B ⭛ are specialised signs for transcribing '
                 'intonation in Lithuanian dialects, and neither is especially close (actually, '
                 'U+2B5A resembles an oblique version of Ψ-12-17).',
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
    else:
        nexturl = "ibkplane1a.html"
        nextname = "Old IBM Korea PC-Data Main Plane, part 1"
    showgraph.dump_plane(f, planefunc, kutenfunc, *plane, lang="ko-KR", part=q, css="../css/codechart.css",
                         menuurl="/ksc-conc.html", menuname="Wansung code variant comparison",
                         lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                         annots=annots, selfhandledanchorlink=True, planewarn=warning,
                         pua_collides=True, showbmppuas=(0, 0, 0, 0, 0, 1, 0), siglum="KSC")
    f.close()









