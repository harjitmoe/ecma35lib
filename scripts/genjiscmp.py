#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021, 2023, 2024.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import japan, cellemojidata
from ecma35.data import graphdata, showgraph
import json

def to_sjis(men, ku, ten):
    if men == 2:
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
    if lead >= 0xA0:
        lead += 0x40
    trail = spos + 0x40
    if trail >= 0x7F:
        trail += 1
    if men == 2:
        return "<br>{:02d}-{:02d}<br>(<abbr title='Shift JIS'>SJIS</abbr> {:02x}{:02x})".format(
                ku, ten, lead, trail)
    else:
        return "<br>(<abbr title='Shift JIS'>SJIS</abbr> {:02x}{:02x})".format(lead, trail)

plane1 = (1, ("1978 JIS<br>Illustrative",  "1978 JIS<br>90JIS Pivot",  "1983 JIS",  "1990 JIS<br>Plane 1",
              "2000 JIS<br>Plane 1",  "2004 JIS<br>Plane 1",  "NEC 78JIS<br>Illustrative", 
              "IBM 78JIS", "IBM 90JIS<br>Plane 1", "Fujitsu", "MS / HTML5", 
              "Apple<br>Row + 10", "Apple<br>PostScript", "Apple<br>KanjiTalk7", 
              "ARIB<br>JIS Emoji", "DoCoMo<br>JIS Emoji", "au by KDDI<br>JIS Emoji", "SoftBank<br>JIS Emoji"), [
          graphdata.gsets["ir042"][2],
          graphdata.gsets["ir042/1990pivot"][2],
          graphdata.gsets["ir087"][2],
          graphdata.gsets["ir168"][2],
          graphdata.gsets["ir228"][2],
          graphdata.gsets["ir233"][2],
          graphdata.gsets["ir042/nec"][2],
          graphdata.gsets["ir042/ibm"][2],
          graphdata.gsets["ir168/ibm"][2],
          graphdata.gsets["ir087/fujitsu"][2],
          #graphdata.gsets["ir168/icueuc"][2], # same as web.
          graphdata.gsets["ir168/web"][2],
          graphdata.gsets["ir168/mackt6"][2],
          graphdata.gsets["ir168/macps"][2],
          graphdata.gsets["ir168/mac"][2],
          graphdata.gsets["ir168/arib"][2],
          graphdata.gsets["ir168/docomo"][2],
          graphdata.gsets["ir168/kddipict"][2],
          graphdata.gsets["ir168/sbank"][2],
])

plane2 = (2, ("IBM SJIS Ext<br>78JIS Ver.", "IBM SJIS Ext<br>MS / HTML5", "DoCoMo<br>SJIS Emoji",
              "au by KDDI<br>SJIS Emoji", "SoftBank<br>SJIS Emoji",
              "1990 JIS<br>Plane 2", "IRG N2722<br>Plane 2", "Va Extension<br>Plane 2",
              "OSF EUC<br>Plane 2M",
              "IBM 90JIS<br>Plane 2", "ICU EUC<br>Plane 2", "2000/04 JIS<br>Plane 2"), [
          graphdata.gsets["ibmsjisextold"][2],
          graphdata.gsets["ibmsjisextpua"][2],
          graphdata.gsets["docomosjisext"][2],
          graphdata.gsets["kddipictsjisext"][2],
          graphdata.gsets["sbanksjisext"][2],
          graphdata.gsets["ir159"][2],
          graphdata.gsets["ir159/irgn2722"][2],
          graphdata.gsets["ir159/va"][2],
          graphdata.gsets["ir159/osfm"][2],
          graphdata.gsets["ir159/ibm"][2],
          graphdata.gsets["ir159/icueuc"][2],
          graphdata.gsets["ir229"][2],
])

plane3 = (3, ("Plane 3",), [
          graphdata.gsets["japan-plane-3"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        if number == 3:
            return "Unified Japanese IT Vendors 1993"
        return "JIS plane {:d}".format(number)
    return ""

def kutenfunc(number, row, cell):
    fmteuc = sjis = jis = ""
    if number in (1, 2):
        if number == 1:
            euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
            jis = "(JIS {:02x}{:02x})<br>".format(0x20 + row, 0x20 + cell)
        else:
            assert number == 2
            euc = "8f{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
            jis = ""
        fmteuc = "(<abbr title='Extended Unix Code'>EUC</abbr> {})".format(euc)
        if number == 2:
            fmteuc += "<br>(<abbr title='Microsoft Extended Unix Code'>MSEUC</abbr> {:02x}{:02x})".format(0xA0 + row, 0x20 + cell)
        sjis = to_sjis(number, row, cell)
    if cell >= 0:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{:02d}</a>".format(
                     number, row, cell, number, row, cell)
    else:
        anchorlink = "<a href='#{:d}.{:d}.{:d}'>{:02d}-{:02d}-{}</a>".format(
                     number, row, -cell, number, row, 
                     "{:02d}+".format(-cell) if cell != -1 else "*")
    return "{}<br>{}{}{}".format(anchorlink, jis, fmteuc, sjis)

cdispmap = cellemojidata.hints2pua.copy()
for n, i in enumerate(japan.rawmac):
    j = japan.jisx0208_applekt7[2][n]
    cdispmap[(n, j)] = i
    if n >= (84 * 94):
        cdispmap[(n - (74 * 94), j)] = i
for n, i in enumerate(graphdata.gsets["ir168/kddipict"][2]):
    j = graphdata.gsets["ir168/kddisym"][2][n]
    if i != j and j:
        cdispmap[(n, i)] = j
for n, i in enumerate(graphdata.gsets["kddipictsjisext"][2]):
    j = graphdata.gsets["kddisymsjisext"][2][n]
    if i != j and j:
        cdispmap[(n + (94 * 94), i)] = j

cdispmap[("au by KDDI<br>JIS Emoji", 8092, (0x1F140,))] = (0xF048,)
cdispmap[("DoCoMo<br>JIS Emoji", 8092, (0x1F140,))] = (0xE6E1,)

annots = {
 (1, 1, 6): 'Compare behaviour of GB 01-04.',
 (1, 1, 17): 'U+FFE3 (￣) is the fullwidth counterpart of both U+00AF (¯) and '
             'U+203E (‾); the latter is the one typically used when mapping '
             'JIS C 6220 / JIS X 0201.\u2002Mapping the double-byte character to '
             'U+203E in contexts where 0x7E is mapped to U+007E (~) is done by '
             'OSF in ASCII-based EUC-JP only, and by JIS X 0213 (2000 JIS / '
             '2004 JIS) in EUC-JP only (and then not by all encoders).\u2002Compare '
             'GB 00-03-94.',
 (1, 1, 29): 'U+2014 (em dash) and U+2015 (horizontal bar) both correspond to '
             "the same JIS character.\u2002UTC's mappings generally favoured "
             'U+2015, and Microsoft and consequently WHATWG (HTML5) follow '
             'this.\u2002JIS (JIS X 0221, JIS X 0213) consider it to be U+2014, '
             'and Apple follows suit; Python apparently considers it to be U+2015 '
             'even in its JIS X 0213 codecs.\u2002OSF maps it as U+2015 in their '
             'MS-based version and as U+2014 otherwise.\u2002Compare behaviour of '
             'GB 00-01-10.</p><p>The codepoint selected to display in the NEC '
             'column is arbitrary.',
 (1, 1, 32): 'U+005C (backslash) is sometimes rendered the same as U+00A5 (¥), '
             "especially when it's used to map the 7-bit code 0x5C (backslash "
             'in ASCII, yen sign in JIS C 6220 / JIS X 0201).\u2002Generally '
             'speaking, the double byte character is only mapped to U+005C if '
             'is is not used as the mapping for 0x5C: OSF map it as U+005C in '
             'JIS-Roman-based EUC but not the other versions, and JIS X 0213 '
             '(2000 JIS / 2004 JIS) maps the double byte character to U+005C '
             'in Shift_JIS but to U+FF3C in EUC.',
 (1, 1, 33): 'Various mappings of various legacy CJK sets map this character '
             'to either U+223C (tilde operator), U+301C (wave dash), or U+FF5E '
             '(fullwidth tilde).\u2002Of these: U+301C was allocated specifically '
             'for the JIS character but was displayed in the Unicode charts with '
             'curvature inverted relative to the JIS charts for a considerable '
             'time (and is still displayed as such by some older fonts such as '
             'MS PMincho).\u2002U+223C is primarily intended as a mathematical '
             'operator, and usually shorter</p>'
             '<p>U+FF5E is just the fullwidth '
             'version of the ASCII character and might therefore be rendered '
             'as either a tilde dash or a spacing tilde accent, of any glyph '
             'width, within a roughly 1em advance—although a wave dash is the '
             'most common by far (however, U+FF5E actually has a separate mapping '
             'at 02-02-23 in JIS X 0212 and 01-02-18 in JIS X 0213, which is shown '
             'as a spacing accent in their respective charts).</p>'
             '<p>Compare, and especially contrast, the behaviour of GB 01-11 and KSC 01-01-13.</p>'
             '<p>The codepoint selected to display in the NEC column is arbitrary.',
 (1, 1, 34): 'U+2225 is used by Microsoft-influenced mappings, U+2016 is used '
             'by others.\u2002U+2225 has a separate mapping in JIS X 0213 (01-02-52). '
             'U+2016 is necessarily straight vertical, whereas U+2225 is often '
             'shown slanted.\u2002Compare GB 01-12 and GB 01-46.</p><p>The codepoint '
             'selected to display in the NEC column is arbitrary.',
 (1, 1, 36): 'Apple initially mapped this to U+22EF and the single-byte Shift JIS 0xFF '
             'to U+2026.\u2002Since this apparently created interoperability issues, '
             'they (Apple) revised these mapping to U+2026 and U+2026+(F87F) respectively, '
             'where U+F87F is a private use character used for round tripping.\u2002Compare '
             'GB 00-01-13, for which Apple apparently retained the U+22EF mapping.',
 (1, 1, 61): 'Microsoft-influenced mappings use U+FF0D for the minus sign '
             '(making the JIS minus sign, as opposed to the JIS hyphen, the '
             'definitive fullwidth form of the ASCII hyphen-minus). Others use '
             'the definitive minus sign codepoint (U+2212).\u2002Also: '
             "WHATWG's (HTML5) encoders exceptionally treat "
             'U+2212 and U+FF0D the same (while its decoders use U+FF0D), '
             'since doing otherwise was breaking Japanese postcode forms on '
             'Macintoshes.\u2002Note a JIS X 0213 mapping for U+FF0D at '
             '01-02-17.\u2002Compare/contrast GB 03-13.</p><p>The codepoint '
             'selected to display in the NEC column is arbitrary.',
 (1, 1, 79): 'Mapping the double-byte character to U+00A5 is only done when '
             "that mapping isn't already used for 0x5C, e.g. JIS X 0213 (2000 "
             'JIS / 2004 JIS) does so for EUC but not Shift_JIS.\u2002OSF use '
             'U+00A5 here in their ASCII-based EUC mappings, but not in their '
             'MS-based or JIS-Roman-based EUC mappings.',
 (1, 1, 82): 'Microsoft-influenced mappings use fullwidth characters for the '
             "pound and cent sign, because they exist, thus arguably making "
             "the regular ones halfwidth codepoints.\u2002Some others don't, "
             "because they aren't necessary (separate encoded representations "
             "for the regular variants don't exist).",
 (1, 2, 15): "Compare 01-92-93 (NEC Selection) and 02-89-23 (IBM SJIS Extensions).",
 (1, 2, 16): "Compare 01-92-94 (NEC Selection) and 02-89-24 (IBM SJIS Extensions).",
 (1, 2, 17): "Compare 01-01-61 and GB 03-13.",
 (1, 2, 18): "Compare 01-01-33 and 02-02-23.\u2002Mapped to U+007E in Shift_JIS "
             "if 0x7E is mapped to U+203E (refer to notes at 01-01-17).\u2002"
             'Shown as a spacing accent in the code chart; however, I know of no '
             'context which maps it to U+02DC (˜).\u2002Also, note that the '
             "addition of these four characters (01-02-15 through 01-02-18) makes "
             "it possible to round-trip map ASCII to JIS-Kanji and back (i.e. if "
             "ASCII mappings are used in place of any fullwidth mappings).",
 (1, 2, 44): 'Microsoft-influenced mappings use a fullwidth character for the '
             "not sign, because it exists, thus arguably making  the regular "
             "one a halfwidth codepoint.\u2002Some others don't, because it "
             "isn't necessary (a separate encoded representation for the "
             "regular variant doesn't exist).</p><p>That being said, a "
             'duplicate also exists in the IBM extensions at 02-89-21 (and '
             'consequently another in the NEC selection at 01-92-91), '
             'predating the allocation of the standard codepoint in 1983.\u2002'
             "Accordingly, this codepoint is not allocated in IBM's extended "
             '78JIS (unlike most of the 1983 additions).',
 (1, 2, 52): 'Compare 01-01-34 and GB 01-46.',
 (1, 2, 55): 'Some codecs map 01-02-54 to U+2985 and 01-02-55 to U+2986.\u2002'
             'Python, for example, does that in both its 2000 JIS and 2004 JIS '
             'codecs.\u2002The Unicode codepoints U+FF5F and U+FF60 were added '
             'in 2001–2002, since the appropriate rendering of these '
             'characters in CJK contexts does not correspond to their rendering '
             'in mathematical contexts.\u2002See <a href="https://www.unicode.org/L2/L2001/01157-N2345R-brackets.pdf">UTC L2/01-157 (WG2 N2345)</a> '
             'and <a href="https://www.unicode.org/L2/L2001/01317-bracket.htm">UTC L2/01-317</a>.',
 (1, 2, 72): 'The because sign is included three times in the Microsoft and '
             'HTML5 version: here (in the 1983 additions), in the NEC row 13 '
             '(01-13-90) and in the IBM extensions (02-89-28).\u2002Unlike '
             'most of the 1983 additions, this codepoint is not allocated in '
             "IBM's extended 78JIS, due to it already existing in the IBM "
             'extension section.',
 (1, 9, 0): 'NEC apparently tries to incorporate JIS X 0201 (JIS C 6220) here, '
            'somewhat like an inverse Shift_JIS. How much Macintosh PostScript '
            'follows the NEC extensions apparently varied between font '
            'versions; the subset of the NEC extension rows shown for it here '
            '(i.e. rows 12 and 13 only) is the subset which can be handled by '
            "Apple's ConvertFromTextToUnicode in response to either flag.\u2002"
            'KanjiTalk 7 goes off doing its own thing here.',
 (1, 9, 92): 'Adobe\'s CID maps, while not mapping most of the NEC characters in this row (they '
             'after all duplicate single-byte characters), maps the pipe to U+FFE8.',
 (1, 11, 0): 'The vertical forms are ten rows down in some older variants on the Macintosh, '
             'versus 84 rows down in the most recent variants.',
 (1, 12, 23): 'I am not sure what is going on with au here (I am including these '
              'only on the authority of the KDDI Shift JIS codec from earlier '
              'versions of ICU, since these four alternative encodings are not '
              'mentioned in EmojiSources.txt, gmojiraw.txt or the UTC documents).'
              '</p><p>The alignment of the telephone with KanjiTalk 7 may or may '
              'not be significant.',
 (1, 13, 0): "NEC's row 13 seems to have become somewhat of a <i>de facto</i> "
             'standard (also being included in the OSF definitions of EUC-JP)… '
             'until it became official standard with the 2000 release of '
             'JIS X 0213.\u2002Several of its mathematical symbols duplicate '
             '1983 additions to row 2, and were thus omitted (but reserved) in '
             'JIS X 0213.\u2002KanjiTalk 7 is still off doing its own thing.',
 (1, 13, 63): "NEC row 13 predates the Heisei era, hence this one isn't "
              'present in the Macintosh variants besides KanjiTalk 7, which '
              'includes it elsewhere (01-14-74).',
 (1, 13, 90): 'Compare 01-02-72.',
 (1, 14, 0): 'JIS X 0213 starts the kanji section at row 14, rather than row '
             '16 as in JIS X 0208.\u2002Multiple Macintosh encoding variants '
             'already use it for their own purposes though.',
 (1, 14, 26): 'Compare 01-22-02 and 02-17-34.',
 (1, 15, 8): 'Compare 01-16-02 and 02-21-64.',
 (1, 15, 26): 'Compare 01-19-90 and 02-22-58.',
 (1, 15, 32): 'Compare 01-39-25 and 02-22-76.',
 (1, 15, 56): 'Compare 01-37-22 and 02-24-20.',
 (1, 15, 94): 'Compare 01-39-77.',
 (1, 16, 2): 'Compare 01-15-08 and 02-21-64.',
 (1, 16, 19): 'Compare 01-82-45.',
 (1, 17, 28): 'For some reason, Adobe\'s CID map lists NEC as having U+28CDD 𨳝 rather than U+958F '
              'here.&ensp;They differ in which end the upper stroke of the inner component '
              'is drawn from.&ensp;The PC98 font is not nearly high resolution enough '
              'for this detail to actually be distinguishable.',
 (1, 17, 75): 'Compare 01-87-49 and 02-41-79.',
 (1, 18, 9): 'Compare 01-82-84.',
 (1, 18, 10): 'Compare 01-94-69 and 02-76-31.',
 (1, 19, 34): 'Compare 01-73-58.',
 (1, 19, 41): 'Compare 01-57-88.',
 (1, 19, 86): 'Compare 01-67-62.',
 (1, 19, 90): 'Compare 01-15-26 and 02-22-58.',
 (1, 20, 35): 'Compare 01-62-85.',
 (1, 20, 50): 'Compare 01-75-61.',
 (1, 22, 2): 'Compare 01-14-26 and 02-17-34.',
 (1, 22, 38): 'Compare 01-84-01.',
 (1, 22, 77): 'Compare 01-92-42 and 02-64-52.',
 (1, 23, 50): 'Compare 01-94-94 and 02-52-58.',
 (1, 23, 59): 'Compare 01-80-84.',
 (1, 24, 20): 'Compare 01-94-74 and 02-76-59.',
 (1, 25, 23): 'Compare 01-90-22 and 02-90-50.',
 (1, 25, 60): 'Compare 01-66-72.',
 (1, 25, 77): 'Compare 01-94-79 and 02-76-79.',
 (1, 28, 40): 'Compare 01-47-64 and 02-26-90.',
 (1, 28, 41): 'Compare 01-73-02.',
 (1, 29, 11): 'Compare 01-90-22 and 02-52-55.',
 (1, 30, 53): 'Compare 01-91-22 and 02-57-22.',
 (1, 30, 63): 'Compare 01-92-89 and 02-66-83.',
 (1, 31, 57): 'Compare 01-80-55.',
 (1, 32, 70): 'Compare 01-91-66.',
 (1, 33, 8): 'Compare 01-76-45.',
 (1, 33, 63): 'Compare 01-84-86 and 02-32-43.',
 (1, 33, 73): 'Compare 01-94-93 and 02-45-87.',
 (1, 34, 45): 'Compare 01-94-20.',
 (1, 35, 29): 'Compare 01-89-73.',
 (1, 36, 47): 'Compare 01-84-89 and 02-32-59.',
 (1, 36, 59): 'Compare 01-52-68.',
 (1, 37, 22): 'Compare 01-15-56 and 02-24-20.',
 (1, 37, 31): 'Compare 01-94-03 and 02-72-19.',
 (1, 37, 55): 'Compare 01-66-74.',
 (1, 37, 78): 'Compare 01-59-77.',
 (1, 37, 83): 'Compare 01-62-25.',
 (1, 37, 88): 'Compare 01-89-35 and 02-48-80.',
 (1, 38, 34): 'Compare 01-87-29 and 02-41-12.',
 (1, 38, 86): 'Compare 01-77-78.',
 (1, 39, 25): 'Compare 01-15-32 and 02-22-76.',
 (1, 39, 72): 'Compare 01-74-04.',
 (1, 39, 77): 'Compare 01-15-94.',
 (1, 40, 14): 'Compare 01-87-09 and 02-40-53.',
 (1, 40, 16): 'Compare 01-92-90 and 02-66-87.',
 (1, 41, 16): 'Compare 01-59-56.',
 (1, 43, 43): 'Compare 01-93-90 and 02-72-04.',
 (1, 43, 74): 'Compare 01-84-02.',
 (1, 43, 89): 'Compare 01-48-54.',
 (1, 44, 45): 'Compare 01-94-80 and 02-76-80.',
 (1, 44, 89): 'Compare 01-73-14.',
 (1, 45, 58): 'Compare 01-84-03.',
 (1, 45, 73): 'Compare 01-91-06 and 02-56-39.',
 (1, 47, 22): 'Compare 01-68-38.',
 (1, 47, 25): 'Compare 01-91-71 and 02-59-88.',
 (1, 47, 64): 'Compare 01-28-40 and 02-26-90.',
 (1, 48, 54): 'Compare 01-43-89.',
# (1, 49, 59): 'Compare 01-84-05.',
 (1, 52, 68): 'Compare 01-36-59.',
 (1, 54, 2): 'Compare 01-94-91.',
 (1, 57, 88): 'Compare 01-19-41.',
 (1, 58, 25): 'Compare 01-85-06 and 02-33-34.',
 (1, 59, 56): 'Compare 01-41-16.',
 (1, 59, 77): 'Compare 01-37-78.',
 (1, 62, 25): 'Compare 01-37-83.',
 (1, 62, 85): 'Compare 01-20-35.',
 (1, 63, 70): 'Compare 01-84-06.',
 (1, 63, 83): 'For some reason, Adobe\'s CID map lists NEC as having U+243D0 rather than U+71D7 '
              'here.&ensp;It differs in having a sun component rather than a moon component in the '
              'enclosure.&ensp;The PC98 font I\'m double-checking against does not do this, '
              'however.&ensp;I\'m taking the CID map\'s word for it for Fujitsu for the time being.',
 (1, 64, 86): 'Compare 01-84-04.',
 (1, 66, 72): 'Compare 01-25-60.',
 (1, 66, 74): 'Compare 01-37-55.',
 (1, 67, 62): 'Compare 01-19-86.',
 (1, 68, 38): 'Compare 01-47-22.',
 (1, 73, 2): 'Compare 01-28-41.',
 (1, 73, 14): 'Compare 01-44-89.',
 (1, 73, 28): 'For some reason, Adobe\'s CID map lists NEC as having U+853E 蔾 rather than U+85DC '
              'here.&ensp;It differs in replacing the lower component with a tree.&ensp;The PC98 '
              'font I\'m double-checking against does not do this, however.',
 (1, 73, 58): 'Compare 01-19-34.',
 (1, 74, 4): 'Compare 01-39-72.',
 (1, 75, 61): 'Compare 01-20-50.',
 (1, 76, 45): 'Compare 01-33-08.',
 (1, 77, 78): 'Compare 01-38-86.',
 (1, 80, 19): 'For some reason, Adobe\'s CID map lists NEC as having U+7762 睢 rather than U+96Ce '
              'here.&ensp;It differs in that it has a 目, not a 且.&ensp;The PC98 '
              'font I\'m double-checking against does not do this, however.',
 (1, 80, 55): 'Compare 01-31-57.',
 (1, 80, 84): 'Compare 01-23-59.',
 (1, 82, 45): 'Compare 01-16-19.',
 (1, 82, 84): 'Compare 01-18-09.',
 (1, 84, 1): 'Compare 01-22-38.',
 (1, 84, 2): 'Compare 01-43-74.',
 (1, 84, 3): 'Compare 01-45-58.',
 (1, 84, 4): 'Compare 01-64-86.',
 (1, 84, 5): 'Compare 01-49-59.',
 (1, 84, 6): 'Compare 01-63-70.',
 (1, 84, 86): 'Compare 01-33-63 and 02-32-43.',
 (1, 84, 89): 'Compare 01-36-47 and 02-32-59.',
 (1, 85, 0): 'Rows 85 through 91 contain the bulk of the "JIS" representations of emoji, in a '
             'layout defined by au by KDDI.\u2002In contrast to the beyond-JIS Shift_JIS '
             'representations of the emoji, which make no '
             'attempt to be compatible with one another (well, au avoids DoCoMo, but SoftBank '
             'collides with both, and none of them line up), the JIS representations from DoCoMo '
             'and SoftBank seem to endeavour to approximately match au where possible.',
 (1, 85, 6): 'RE 2000 JIS / 2004 JIS: compare 01-58-25 and 02-33-34.',
 (1, 87, 9): 'RE 2000 JIS / 2004 JIS: compare 01-40-14 and 02-40-53.',
 (1, 87, 29): 'RE 2000 JIS / 2004 JIS: compare 01-38-34 and 02-41-12.',
 (1, 87, 49): 'RE 2000 JIS / 2004 JIS: compare 01-17-75 and 02-41-79.',
 (1, 88, 24): 'Despite its name FLAG IN HOLE, U+26F3 actually unifies two symbols: a head of a '
              'golf club with a ball used by pre-2013 DoCoMo, post-2012 au and Noto Jelly Bean and '
              'KitKat, and a flag in a golf hole, used by pre-2012 au, SoftBank, ARIB, DoCoMo since '
              '2013, and others.\u2002See 01-91-26 for where ARIB encodes this character.\u2002'
              'The UCS name (FLAG IN HOLE) reflects the ARIB glyph, due to having first '
              'been added from the ARIB set (where it is a map symbol for a golf course).</p><p>'
              '<a href="https://emojipedia.org/flag-in-hole/">Some glyph history on Emojipedia.</a>',
 (1, 89, 0): 'In the NEC and Windows / HTML5 versions, this is the start of '
             'the so-called NEC Selection (rows 89–92 inclusive): an '
             'alternative encoding within the JIS X 0208 bounds of all the '
             'characters in the IBM Extensions block except for those also in '
             'NEC row 13.</p><p>Hence in the context of the Windows or HTML5 '
             'Shift_JIS variant, all of its allocations are duplicates.\u2002'
             'Encoders of that Shift_JIS variant (Windows-31J) vary as to '
             'whether they favour the IBM Extensions over the NEC Selection '
             '(Windows, WHATWG) or <i>vice versa</i> (Python).',
 (1, 89, 35): 'RE 2000 JIS / 2004 JIS: compare 01-37-88 and 02-48-80.',
 (1, 89, 73): 'RE 2000 JIS / 2004 JIS: compare 01-35-29.',
 (1, 90, 22): 'RE 2000 JIS / 2004 JIS: compare 01-29-11 and 02-52-55.\u2002RE NEC, compare 01-25-23 and 02-90-50.',
 (1, 91, 6): 'RE 2000 JIS / 2004 JIS: compare 01-45-73 and 02-56-39.',
 (1, 91, 22): 'RE 2000 JIS / 2004 JIS: compare 01-30-53 and 02-57-22.',
 (1, 91, 66): 'RE 2000 JIS / 2004 JIS: compare 01-32-70.',
 (1, 91, 71): 'RE 2000 JIS / 2004 JIS: compare 01-47-25 and 02-59-88.',
 (1, 92, 42): 'RE 2000 JIS / 2004 JIS: compare 01-22-77 and 02-64-52.',
 (1, 92, 89): 'RE 2000 JIS / 2004 JIS: compare 01-30-63 and 02-66-83.',
 (1, 92, 90): 'RE 2000 JIS / 2004 JIS: compare 01-40-16 and 02-66-87.',
 (1, 92, 91): 'RE 2000 JIS / 2004 JIS: compare 01-02-44.',
 (1, 93, 0): 'Row 93 contains SoftBank emoji without au mappings (excluding the J-Phone logos but '
             'including the Vodafone logo), in a layout defined by, presumably, Vodafone Japan '
             '(which later became SoftBank).\u2002DoCoMo mostly doesn\'t use this range, but with '
             'two inadventently-collisive exceptions noted below.',
 (1, 93, 55): 'DoCoMo seems to try to match SoftBank\'s encoding here, but off-by-ones (oops).',
 (1, 93, 61): 'DoCoMo seems to try to match SoftBank\'s encoding here, but off-by-ones (oops).',
 (1, 93, 70): "Softbank's 01-93-70 (or 02-92-12) is their Shibuya 109 emoji, U+E50A "
              'in the Unicode Private Use Area.\u2002See <a href='
              '"https://emojipedia.org/shibuya/">documentation on Emojipedia</a>.',
 (1, 93, 87): "Softbank's 01-93-83 through 01-93-87 (or 02-92-60 through 02-92-64) "
              "are Vodafone logo variants, the latter three being slices of a single logo.",
 (1, 93, 90): 'RE 2000 JIS / 2004 JIS: compare 01-43-43 and 02-72-04.',
 (1, 94, 0): 'Row 94 contains DoCoMo emoji with neither au mappings nor off-by-one-SoftBank '
             'mappings.\u2002Curiously, this doesn\'t include all the DoCoMo-specific emoji from '
             'the TRON and DoCoMo Shift JIS encodings.\u2002Those omitted tend to also be the '
             'ones without canonical Unicode representations, though not all those included have '
             'canonical Unicode representations either (since six are logos).',
 (1, 94, 3): 'RE 2000 JIS / 2004 JIS: compare 01-37-31 and 02-72-19.',
 (1, 94, 20): 'RE 2000 JIS / 2004 JIS: compare 01-34-45.',
 (1, 94, 69): 'RE 2000 JIS / 2004 JIS: compare 01-18-10 and 02-76-31.',
 (1, 94, 74): 'RE 2000 JIS / 2004 JIS: compare 01-24-20 and 02-76-59.',
 (1, 94, 79): 'RE 2000 JIS / 2004 JIS: compare 01-25-77 and 02-76-79.',
 (1, 94, 80): 'RE 2000 JIS / 2004 JIS: compare 01-44-45 and 02-76-80.',
 (1, 94, 91): 'RE 2000 JIS / 2004 JIS: compare 01-54-02.',
 (1, 94, 93): 'RE 2000 JIS / 2004 JIS: compare 01-33-73 and 02-45-87.',
 (1, 94, 94): 'RE 2000 JIS / 2004 JIS: compare 01-23-50 and 02-52-58.',
 (2, 1, 0): "Regarding the codepoint column from here onwards: the plane 2 codepoints "
            "for the SJIS codes after the end of the JIS X 0208 section are "
            "defined by the requisite appendix of JIS X 0213.\u2002Of course, "
            "this has only existed since 2000.\u2002Regarding older SJIS variants, "
            "which is to say, almost all other SJIS variants, row numbers are "
            "more commonly allocated sequentially as if the JIS X 0208 plane "
            "hadn't ended at row 94.\u2002Of course, the plane 2 system was used "
            "by EUC-JP, but this means that any extensions for EUC-JP before JIS X 0213 will "
            "collide with any extensions for SJIS from the same period.</p>"
            "<p>JIS X 0212 rows are represented in EUC-JP only.\u2002The orders of the remaining "
            "rows aren't entirely identical: row 96 (02-08-*) gets put between rows 99 (02-05-*) and "
            "100 (02-12-*), preserving the alternating odd/even rows, and meaning that "
            "the trail byte range can still be correctly identified from whether "
            "the row number is even.",
 (2, 2, 23): 'Compare 01-01-33 and 01-02-18.\u2002'
             'Might be mapped to U+007E in OSF or JIS X 0213 contexts which don\'t use that as '
             'the mapping for single-byte 0x7E (i.e. Shift_JIS, or JIS-Roman based EUC).\u2002'
             'Included amongst a set of spacing accents, and very clearly shown as a spacing '
             'accent in the code chart; however, I know of no context which maps it to U+02DC (˜).',
 (2, 2, 35): 'Mapped to U+FFE4 by OSF in its Microsoft-based variant only (i.e. mapping to the '
             'fullwidth codepoint when one exists, not only when needed for round-trip '
             'reasons), otherwise to U+00A6.\u2002Compare 01-01-81 and 01-01-82.',
 (2, 17, 0): 'Compare 02-17-34 with 01-14-26 and 01-22-02.',
 (2, 21, 0): 'Compare 02-21-64 with 01-15-08 and 01-16-02.',
 (2, 22, 0): 'Compare 02-22-58 with 01-15-26 and 01-19-90.\u2002Compare 02-22-76 with 01-15-32 and 01-39-25.',
 (2, 24, 0): 'Compare 02-24-20 with 01-15-56 and 01-37-22.',
 (2, 26, 0): 'Compare 02-26-90 with 01-28-40 and 01-47-64.',
 (2, 32, 0): 'Compare 02-32-43 with 01-33-63 and 01-84-86.\u2002Compare 02-32-59 with 01-36-47 and 01-84-89.',
 (2, 33, 0): 'Compare 02-33-34 with 01-58-25 and 01-85-06.',
 (2, 40, 0): 'Compare 02-40-53 with 01-40-14 and 01-87-09.',
 (2, 41, 0): 'Compare 02-41-12 with 01-38-34 and 01-87-29.\u2002Compare 02-41-79 with 01-17-75 and 01-87-49.',
 (2, 45, 0): 'Compare 02-45-87 with 01-33-73 and 01-94-93.',
 (2, 48, 80): 'Compare 01-37-88 and 01-89-35.',
 (2, 52, 55): 'Compare 01-29-11 and 01-90-22.',
 (2, 52, 58): 'Compare 01-23-50 and 01-94-94.',
 (2, 56, 39): 'Compare 01-45-73 and 01-91-06.',
 (2, 57, 22): 'Compare 01-30-53 and 01-91-22.',
 (2, 59, 88): 'Compare 01-47-25 and 01-91-71.',
 (2, 64, 52): 'Compare 01-22-77 and 01-92-42.',
 (2, 66, 83): 'Compare 01-30-63 and 01-92-89.',
 (2, 66, 87): 'Compare 01-40-16 and 01-92-90.',
 (2, 72, 4): 'Compare 01-43-43 and 01-93-90.',
 (2, 72, 19): 'Compare 01-37-31 and 01-94-03.',
 (2, 76, 31): 'Compare 01-18-10 and 01-94-69.',
 (2, 76, 59): 'Compare 01-24-20 and 01-94-74.',
 (2, 76, 79): 'Compare 01-25-77 and 01-94-79.',
 (2, 76, 80): 'Compare 01-44-45 and 01-94-80.',
 (2, 83, 0): 'This row\'s content is invoked over GL (without re-designating G0) by <code>ESC $ E'
             '</code> in SoftBank\'s 2G emoji encoding (which does not conform to JIS X 0202 / '
             'ECMA-35).\u2002It is positioned such that the first emoji (cell 2 here) is over '
             '0x21 (<code>!</code>).',
 (2, 84, 0): 'This row\'s content is invoked over GL (without re-designating G0) by <code>ESC $ F'
             '</code> in SoftBank\'s 2G emoji encoding (which does not conform to JIS X 0202 / '
             'ECMA-35).\u2002It is positioned such that the first emoji (cell 3 here) is over '
             '0x21 (<code>!</code>).',
 (2, 84, 24): 'Despite its name FLAG IN HOLE, U+26F3 actually unifies two symbols, see 01-88-24 for details.',
 (2, 84, 86): 'SoftBank\'s 02-84-86 is named "J-PHONE SHOP".',
 (2, 84, 87): 'SoftBank\'s 02-84-87 is named "SKY WEB", and <a href="https://mail.google.com/mail/e/softbank_ne_jp/E78">depicts a body orbiting a planet</a>.\u2002The displayed substitution is newer and somewhat similar, but <a href="https://commons.wikimedia.org/wiki/File:Planet_-_The_Noun_Project.svg">something like this</a> would be closer.',
 (2, 84, 88): 'SoftBank\'s 02-84-88 is named "SKY WALKER", and <a href="https://mail.google.com/mail/e/softbank_ne_jp/E79">depicts a paper aeroplane</a>.\u2002Interestingly, no current Unicode-defined emoji (as of Unicode 13) depicts one, although it\'s U+F1D8 (BMP PUA) or U+10F1D8 (SPUB) in Font Awesome.\u2002<a href="https://commons.wikimedia.org/wiki/File:Gnome-document-send.svg">A possible higher-resolution colour presentation, from the GNOME icon set.</a>',
 (2, 84, 89): 'SoftBank\'s 02-84-89 is named "SKY MELODY", and <a href="https://mail.google.com/mail/e/softbank_ne_jp/E7A">depicts a musical note and waves</a>.',
# (2, 84, 92): 'Softbank\'s 02-84-90 through 02-84-92 is named "J-PHONE".',
 (1, 85, 39): "The zodiac signs following this point were implemented as images of the actual "
              "animals, <i>et cetera</i>, by au by KDDI prior to 2012.&ensp;Most of these today "
              "have considerably closer Unicode mappings than just the signs.&ensp;See <a href='https://www.au.com/content/dam/au-com/static/designs/extlib/pdf/mobile/service/featurephone/communication/emoji/taiohyo_03.pdf'>au's own chart</a> for the changes and cross-vendor issues.",
 (1, 85, 42): "The old au-by-KDDI glyph is two smiling faces (Castor and Pollux, presumably) pressed together.",
 (1, 85, 52): "The old au-by-KDDI glyph is a herculean figure wrestling a snake.",
 (2, 81, 39): "The zodiac signs following this point were implemented as images of the actual "
              "animals, <i>et cetera</i>, by au by KDDI prior to 2012.&ensp;Most of these today "
              "have considerably closer Unicode mappings than just the signs.&ensp;See <a href='https://www.au.com/content/dam/au-com/static/designs/extlib/pdf/mobile/service/featurephone/communication/emoji/taiohyo_03.pdf'>au's own chart</a> for the changes and cross-vendor issues.",
 (2, 81, 42): "The old au-by-KDDI glyph is two smiling faces (Castor and Pollux, presumably) pressed together.",
 (2, 81, 52): "The old au-by-KDDI glyph is a herculean figure wrestling a snake.",
 (2, 86, 0): 'This DoCoMo row is coded at 9-9121 through 9-917E by TRON.',
 (2, 86, 23): 'Despite its name FLAG IN HOLE, U+26F3 actually unifies two symbols, see 01-88-24 for details.',
 (2, 87, 0): 'RE DoCoMo: this row is coded at 9-9221 through 9-927E by TRON.</p><p>'
             'RE SoftBank: This row\'s content is invoked over GL (without re-designating G0) by '
             '<code>ESC $ G</code> in the 2G emoji encoding (which does not conform to JIS X 0202 / '
             'ECMA-35).\u2002It is positioned such that the first emoji (cell 2 here) is over 0x21 '
             '(<code>!</code>).</p><p>This SoftBank row comprises the oldest emoji characters in that '
             'set, <a href="https://blog.emojipedia.org/correcting-the-record-on-the-first-emoji-set/">'
             'dating back to J-Phone\'s 1997 SkyWalker DP-211 SW</a>.',
 (2, 87, 20): '<a href="https://mail.google.com/mail/e/docomo_ne_jp/E1C">DoCoMo\'s 02-87-20</a> '
              'has a featureless texture, without the dots / markings present in their 02-86-58 '
              '(<a href="https://emojipedia.org/docomo/2002/movie-camera/">for comparison</a>).',
 (2, 87, 36): 'DoCoMo\'s 02-87-32 through 02-87-36 appear as boxed letters F, D, S, C, R with '
              'drop shadows (food, décor, service, cost and recommendation).',
 (2, 87, 47): 'DoCoMo\'s 02-87-44 through 02-87-47 appear as boxed letters I, M, E, VE with '
              'drop shadows (inexpensive, moderately priced, expensive and very expensive).',
 (2, 87, 48): 'DoCoMo\'s 02-87-48 <a href="https://umihotaru.work/nishiki-teki_pua.pdf#page=60">is '
              'a crescent-on-circle "open late" symbol</a>, yet it is a separate character from '
              'their 02-87-04.\u2002Google misinterpreted it as a depth-shaded sphere, and gave '
              'it the name SPHERE in their emoji PUA scheme, using just ● as the substitute.',
 (2, 87, 58): 'DoCoMo\'s 02-87-57 and 02-87-58 display a DoCoMo logo, which resembles a Ð.',
 (2, 88, 0): 'RE DoCoMo: this row is coded at 9-9321 through 9-937E by TRON.</p><p>'
             'RE SoftBank: This row\'s content is invoked over GL (without re-designating G0) by '
             '<code>ESC $ O</code> in the 2G emoji encoding (which does not conform to JIS X 0202 / '
             'ECMA-35).\u2002It is positioned such that the first emoji (cell 3 here) is over '
             '0x21 (<code>!</code>).',
 (2, 89, 21): 'Compare 01-02-44.',
 (2, 89, 28): 'Compare 01-02-72.',
 (2, 90, 50): 'Compare 01-25-23 and 01-90-22.',
 (2, 91, 0): 'This row\'s content is invoked over GL (without re-designating G0) by <code>ESC $ P'
             '</code> in Softbank\'s 2G emoji encoding (which does not conform to JIS X 0202 / '
             'ECMA-35).\u2002It is positioned such that the first emoji (cell 2 here) is over '
             '0x21 (<code>!</code>).',
 (2, 92, 0): 'This row\'s content is invoked over GL (without re-designating G0) by <code>ESC $ Q'
             '</code> in Softbank\'s 2G emoji encoding (which does not conform to JIS X 0202 / '
             'ECMA-35).\u2002It is positioned such that the first emoji (cell 3 here) is over '
             '0x21 (<code>!</code>).',
 (2, 92, 12): "Softbank's 02-92-12 (or 01-93-70) is their Shibuya 109 emoji, U+E50A "
              'in the Unicode Private Use Area.\u2002See <a href='
              '"https://emojipedia.org/shibuya/">documentation on Emojipedia</a>.',
# (2, 92, 59): 'Softbank\'s 02-92-58 through 02-92-59 is named "J-SKY".',
 (2, 92, 64): "Softbank's 02-92-60 through 02-92-64 (or 01-93-83 through 01-93-87) "
              "are Vodafone logo variants, the latter three being slices of a single logo.",
 (2, 93, 27): "For some reason, Python's 2000 JIS codecs (unlike its 2004 JIS "
              'codecs) map 02-93-27 to U+9B1D (鬝), not to U+9B1C. The '
              'ISO-IR-229 registration (registered for the second plane of '
              '2000 JIS, but not superseded upon 2004 JIS) visibly shows a 鬜 '
              '(U+9B1C) though.',
 (3, 1, 0):
    "Best as I can ascertain, this is a largely artifical or fictitious ISO/IEC 2022 (ECMA-35) "
    "based charset, i.e. one which was never used anywhere (it has no ISO-IR registration, "
    "and EUC-JP uses all four G-sets already so there's no provision for using it from there "
    "either).</p><p>It may have been created purely as an impetus for getting these characters "
    "into Unicode; they appear in CJK Extension A, except for two which were already present as "
    '"compatibility" ideographs sourced from IBM Japan (they are two of the twelve that are '
    "actually CJK Unified Ideographs despite being in the CJK Compatibility Ideographs block).",
}

blot = ""
if os.path.exists("__analyt__"):
    blot = open("__analyt__").read()

for n, p in enumerate([plane1, plane2, plane3]):
    for q in range(1, 7):
        bn = n + 1
        f = open("jisplane{:X}{}.html".format(bn, chr(0x60 + q)), "w", encoding="utf-8")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "jisplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "JIS plane {:d}, part {:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "jisplane{:X}f.html".format(bn - 1)
            lastname = "JIS plane {:d}, part 6".format(bn - 1)
        else:
            lasturl = "jisx0201.html"
            lastname = "JIS X 0201"
        if q < 6:
            nexturl = "jisplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "JIS plane {:d}, part {:d}".format(bn, q + 1)
        elif bn < 3:
            nexturl = "jisplane{:X}a.html".format(bn + 1)
            nextname = "JIS plane {:d}, part 1".format(bn + 1)
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ja", part=q, css="../css/codechart.css",
                             menuurl="../jis-conc.html", menuname="JIS character set variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots, cdispmap=cdispmap, selfhandledanchorlink=True, blot=blot, siglum="JIS")
        f.close()








