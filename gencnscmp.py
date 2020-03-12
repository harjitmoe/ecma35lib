#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import traditional
from ecma35.data import graphdata, showgraph
import json, os

inverse = dict(zip(traditional.big5_to_cns2.values(), traditional.big5_to_cns2.keys()))

# Swap these over so (a) the Gov.TW mapping's way around for the left and right arrows and (b) the
#   ordering of Big5 non-kanji codepoints compared to the ordering of CNS non-kanji codepoints both
#   look less weirdly non-sequitur. I want the output to be as elucidating as possible.
inverse[(1, 2, 55)] = 0xA1F6
inverse[(1, 2, 56)] = 0xA1F7
def swap_arrows(t):
    return t[:148] + (t[149], t[148]) + t[150:]

macbig5 = tuple(tuple(i) if i is not None else None for i in 
                json.load(open(os.path.join(parsers.directory, "Vendor/macBig5.json"), "r")))

plane1 = (1, ("UTC Big5", "UTC CNS", "MS Big5", "Mac Big5", "Yasuoka CNS",
              "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          swap_arrows(traditional.read_big5_planes("UTC/BIG5.TXT", plane=1)),
          parsers.read_main_plane("UTC/CNS11643.TXT", plane=1),
          swap_arrows(traditional.read_big5_planes("Vendor/CP950.TXT", plane=1)),
          swap_arrows(macbig5[:94*94]),
          parsers.read_main_plane("Other/Uni2CNS", plane=1),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=1),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=1),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=1),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=1),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=1)
          )),
          graphdata.gsets["ir171"][2],
])

plane2 = (2, ("UTC Big5", "UTC CNS", "MS Big5", "Mac Big5", "Yasuoka CNS",
              "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          traditional.read_big5_planes("UTC/BIG5.TXT", plane=2),
          parsers.read_main_plane("UTC/CNS11643.TXT", plane=2),
          traditional.read_big5_planes("Vendor/CP950.TXT", plane=2),
          macbig5[94*94:],
          parsers.read_main_plane("Other/Uni2CNS", plane=2),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=2),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=2),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=2),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=2),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=2)
          )),
          graphdata.gsets["ir172"][2],
])

plane3 = (3, ("UTC CNS", "Yasuoka CNS", "ICU CNS 1992",
              "ICU EUC 2014", "GOV-TW CNS", "Output", "Output Alt"), [
          parsers.read_main_plane("UTC/CNS11643.TXT", plane=14), # yes, really.
          parsers.read_main_plane("Other/Uni2CNS", plane=3),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=3),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=3),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=3),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=3),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=3)
          )),
          graphdata.gsets["ir183"][2],
          graphdata.gsets["ir183-1988plus"][2],
])

plane4 = (4, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=4),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=4),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=4),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=4),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=4),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=4)
          )),
          graphdata.gsets["ir184"][2],
])

plane5 = (5, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=5),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=5),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=5),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=5),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=5),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=5)
          )),
          graphdata.gsets["ir185"][2],
])

plane6 = (6, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=6),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=6),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=6),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=6),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=6),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=6)
          )),
          graphdata.gsets["ir186"][2],
])

plane7 = (7, ("Yasuoka CNS", "ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("Other/Uni2CNS", plane=7),
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=7),
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=7),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=7),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=7),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=7)
          )),
          graphdata.gsets["ir187"][2],
])

planeF = (15, ("ICU CNS 1992", "ICU EUC 2014", "GOV-TW CNS", "Output"), [
          parsers.read_main_plane("ICU/cns-11643-1992.ucm", plane=9), # yes, really.
          parsers.read_main_plane("ICU/euc-tw-2014.ucm", plane=15),
          tuple(map(lambda a, b, c: a or b or c,
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode BMP.txt", plane=15),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 2.txt", plane=15),
              parsers.read_main_plane("GOV-TW/CNS2UNICODE_Unicode 15.txt", plane=15)
          )),
          graphdata.gsets["cns-eucg2"][2][94*94*14:94*94*15],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "CNS 11643 plane {:d}".format(number)
    else:
        if (mapname == "UTC CNS") and (number == 3):
            return '<br>Plane "14"'
        elif (mapname == "ICU CNS 1992") and (number == 15):
            return '<br>Plane "9"'
        elif "Big5" in mapname:
            return "<br>Level {}".format(number) if number <= 2 else "(beyond)"
        else:
            return "<br>Plane {}".format(number)

def kutenfunc(number, row, cell):
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    else:
        euc = "8e{:02x}{:02x}{:02x}".format(0xA0 + number, 0xA0 + row, 0xA0 + cell)
    big5 = ""
    if (number, row, cell) in inverse:
        big5 = "<br>(Big5 {:04x})".format(inverse[number, row, cell])
    return "{:02d}-{:02d}-{:02d}<br>(<abbr title='Extended Unix Code'>EUC</abbr> {}){}".format(
           number, row, cell, euc, big5)

annots = {
 (1, 2, 36): 'Various mappings of various legacy CJK sets map this character to either U+223C '
             '(tilde operator), U+301C (wave dash), or U+FF5E (fullwidth tilde).\u2002Of these: '
             'U+301C was allocated specifically for the character as it appears in JIS (at '
             'JIS 01-01-33), but was displayed in the Unicode charts with curvature inverted '
             'relative to the JIS charts for a considerable time (and is still displayed as '
             'such by some older fonts such as MS PMincho); U+223C is primarily intended as a '
             "mathematical operator (perhaps justifiable in this specific case, since it's in "
             "the middle of several mathematical operaters), and usually shorter; U+FF5E is just "
             'the fullwidth version of the ASCII character and might therefore be rendered '
             'as either a tilde dash or a spacing tilde accent, of any glyph width, within a '
             'roughly 1em advance—although a wave dash is the most common by far.',
 (1, 2, 51): 'U+2641 is the astrological symbol for the earth, and is usually rendered as a globus '
             'cruciger (upside-down Venus); if the version with cross inside the circle is '
             'desired specifically, U+1F728 (🜨, verdigris) is probably more semantically relevant '
             'than U+2295 (⨁, a mathematical symbol), although the latter is often substituted.',
 (1, 2, 52): 'U+2609 is the astrological symbol for the sun, and U+2299 is a mathematical symbol. '
             'Besides that, they are visually much the same symbol.',
 (1, 2, 56): "Although which way around the arrows are in Big5 is not particularly controversial, "
             "their order within CNS 11643 seems to have changed to match Big5 relatively "
             "recently.\u2002Indeed, current data (as of March 2020) from the National Development "
             "Council in Taiwan (also the source for the GOV-TW column) map 01-02-55 and 01-02-56 "
             "to Big5 A1F6 and A1F7 respectively, in contrast to older sources such as RFC 1922 "
             "(which ecma35lib uses as its primary concordance of Big5 to CNS), which go out of "
             "their way to interrupt their neat range mappings to swap them.\u2002Both the code "
             "chart registered as ISO-IR-171, and all older CNS mappings, show these arrows in the "
             "opposite order to Big5.\u2002I've deliberately deviated from the RFC 1922 "
             "correspondance for this chart only (not the ecma35lib internals) here since that way "
             "seems more self-explanatory in this light.",
 (1, 2, 61): 'For JIS sets, U+2225 is used by Microsoft-influenced mappings where U+2016 is used '
             'by others. This pattern does not seem to hold up for variation in CNS / Big5 '
             'mappings, besides that Microsoft are indeed using U+2225. Graphically, the '
             'difference is that U+2016 is necessarily two straight vertical lines, whereas U+2225 '
             'is often shown slanted.',
 (1, 2, 89): 'The first of a sequence of nine Chinese characters created as unit symbols, which '
             'Big5 and CNS organise in their unit symbols section, not their Chinese character '
             'section.',
 (1, 6, 10): "The older ICU mapping file counts Yasuoka amongst its attributed sources, so this "
             "seems to be an error on Yasuoka's part.\u2002Indeed, ISO-IR-171 includes the circled "
             "numbers 1 through 10 here, like the other mappings.",
 (1, 6, 94): "CNS uses a slightly modified classical radical system, in which ⼡ is not included, "
             "and its characters are listed under ⼢ instead (see 01-07-34 below).\u2002This is "
             "presumably an extension to allow all of Unicode's classical radicals to be encoded.",
 (1, 7, 0): "Regarding the next two-and-a-bit rows: mappings too old to have made use of Unicode's "
            "classical radical codepoints either miss these out altogether (they're outside Big5, "
            "so arguably expendable), or many-to-one map them to their ordinary Chinese character "
            "codepoints from the URO.",
 (1, 11, 45): "The CNS encoding for kana is outside of Big5; confusingly, there are actually two "
              "overlapping and incompatible / collisive ways of representing kana in Big5 "
              "(BIG5.TXT versus ETEN).\u2002For interoperability's sake, don't encode kana in Big5 "
              "if you can possibly help it.</p><p>On a more positive note, the CNS kana encoding "
              "remembers the vowel extender (<em>cough</em> GB 2312 <em>cough</em>).",
 (1, 21, 0): "Series of private use (i.e. not standard Unicode) mappings for various positional "
             "forms of various strokes, characters and components in brush script.\u2002This being "
             "additional to the strokes section, the radicals section, and the Chinese character "
             "section.\u2002I do not know what they are for.",
 (1, 34, 35): "The Euro sign and circle were added in 2007.",
 (1, 34, 52): "Using private use assignments for grapheme clusters which have standard Unicode "
              "representations just (presumably) because they don't have single codepoints… why?",
 (3, 66, 38): "Between 1992 and 2007, this was the last <i>de jure</i> codepoint on this "
              "plane.\u200203-66-39 through 03-68-21 were removed and distributed amongst plane 4 "
              "in 1992 (at the same time this plane was moved from an extension in plane 14 to a "
              "standard inclusion in plane 3).\u200203-68-40 onward were included as fictitious "
              "extensions in the version of CNS submitted for incorporating into the original URO, "
              "and only standardised beyond the <i>de facto</i> level in 2007.",
 (3, 68, 63): 'Compare 04-03-65.',
 (3, 68, 77): 'Compare 04-08-93.',
 (3, 69, 26): "Compare 15-28-30.",
 (3, 69, 34): 'Compare 04-24-60.',
 (3, 69, 44): 'Compare 04-10-78.',
 (3, 69, 59): 'Compare 04-36-56.',
 (3, 70, 17): 'Compare 04-07-74.',
 (3, 70, 80): 'Compare 04-16-34.',
 (3, 70, 87): 'Compare 04-67-25.',
 (4, 2, 59): "Compare 04-06-05",
 (4, 3, 65): 'Compare 03-68-63.',
 (4, 6, 5): "Compare 04-02-59",
 (4, 7, 74): 'Compare 03-70-17.',
 (4, 8, 7): "Compare 15-08-82",
 (4, 8, 93): 'Compare 03-68-77.',
 (4, 10, 78): 'Compare 03-69-44.',
 (4, 16, 34): 'Compare 03-70-80.',
 (4, 24, 60): 'Compare 03-69-34.',
 (4, 36, 56): 'Compare 03-69-59.',
 (4, 51, 28): "Compare 15-49-93",
 (4, 67, 25): 'Compare 03-70-87.',
 (4, 72, 47): "Compare 05-79-52",
 (5, 79, 52): "Compare 04-72-47",
 (15, 8, 82): "Compare 04-08-07",
 (15, 28, 30): "Compare 03-69-26.",
 (15, 49, 93): "Compare 04-51-28",
 (15, 67, 66): "Compare 15-67-74",
 (15, 67, 74): "Compare 15-67-66",
}

for n, p in enumerate([plane1, plane2, plane3, plane4, plane5, plane6, plane7, planeF]):
    for q in range(1, 7):
        bnx = (1, 2, 3, 4, 5, 6, 7, 15)
        bn = bnx[n]
        f = open("cnsplane{:X}{}.html".format(bn, chr(0x60 + q)), "w")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "cnsplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "CNS 11643 plane {:d}, part {:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "cnsplane{:X}f.html".format(bnx[n - 1])
            lastname = "CNS 11643 plane {:d}, part 6".format(bnx[n - 1])
        if q < 6:
            nexturl = "cnsplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "CNS 11643 plane {:d}, part {:d}".format(bn, q + 1)
        elif bn < 15:
            nexturl = "cnsplane{:X}a.html".format(bnx[n + 1])
            nextname = "CNS 11643 plane {:d}, part 1".format(bnx[n + 1])
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="zh-TW", part=q, css="/css/cns.css",
                             menuurl="/cns-conc.html", menuname="CNS 11643 and Big5 comparison tables",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots)
        f.close()








