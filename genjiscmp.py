#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data.multibyte import mbmapparsers as parsers
from ecma35.data.multibyte import japan
from ecma35.data import graphdata, showgraph
import json, os

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

plane1 = (1, ("1978 JIS", "NEC 78JIS", "1983 JIS", "1990 JIS",
              "2000 JIS",  "2004 JIS", 
              "MS / HTML5", "Mac KT6",   "Mac KT7",  "Mac PS",
              "IBM 78JIS", "IBM 90JIS",
              "ARIB<br>JIS", "DoCoMo<br>JIS", "KDDI<br>JIS", "SoftBank<br>JIS"), [
          graphdata.gsets["ir042"][2],
          graphdata.gsets["ir042nec"][2],
          graphdata.gsets["ir087"][2],
          graphdata.gsets["ir168"][2],
          graphdata.gsets["ir228"][2],
          graphdata.gsets["ir233"][2],
          graphdata.gsets["ir168web"][2],
          graphdata.gsets["ir168mackt6"][2],
          graphdata.gsets["ir168mac"][2],
          graphdata.gsets["ir168macps"][2],
          graphdata.gsets["ir042ibm"][2],
          graphdata.gsets["ir168ibm"][2],
          graphdata.gsets["ir168arib"][2],
          graphdata.gsets["ir168docomo"][2],
          graphdata.gsets["ir168kddi"][2],
          graphdata.gsets["ir168sbank"][2],
])

plane2 = (2, ("MS / HTML5<br>SJIS Ext", "DoCoMo<br>SJIS Ext", "KDDI<br>SJIS Ext", "SoftBank<br>SJIS Ext",
              "1990 JIS", "1990 JIS Ext",
              "OSF JIS<br>Plane 2", "OSF JIS<br>Plane 2A", "OSF JIS<br>Plane 2M",
              "IBM 90JIS", "2000/04 JIS"), [
          graphdata.gsets["ibmsjisext"][2],
          graphdata.gsets["docomosjisext"][2],
          graphdata.gsets["kddisjisext"][2],
          graphdata.gsets["sbanksjisext"][2],
          graphdata.gsets["ir159"][2],
          graphdata.gsets["ir159va"][2],
          graphdata.gsets["ir159osf"][2],
          graphdata.gsets["ir159osfa"][2],
          graphdata.gsets["ir159osfm"][2],
          graphdata.gsets["ir159ibm"][2],
          graphdata.gsets["ir229"][2],
])

def planefunc(number, mapname=None):
    if mapname is None:
        return "JIS plane {:d}".format(number)
    elif mapname in ("1978 JIS", "1983 JIS", "Mac KT6", "Mac KT7", "Mac PS", "IBM 78JIS", "NEC 78JIS"):
        return ""
    elif "<br>" in mapname:
        return ""
    else:
        return "<br>Plane {}".format(number)

def kutenfunc(number, row, cell):
    if number == 1:
        euc = "{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    else:
        assert number == 2
        euc = "8f{:02x}{:02x}".format(0xA0 + row, 0xA0 + cell)
    sjis = "" # TODO
    return "{:02d}-{:02d}-{:02d}<br>(<abbr title='Extended Unix Code'>EUC</abbr> {}){}".format(
           number, row, cell, euc, sjis) + to_sjis(number, row, cell)

annots = {
    (1, 1, 17): "U+FFE3 (￣) is the fullwidth counterpart of both U+00AF (¯) and U+203E (‾); the latter is the one typically used when mapping JIS C 6220 / JIS X 0201. Mapping the double-byte character to U+203E in contexts where 0x7E is mapped to U+007E (~) is done by OSF and by JIS X 0213 (2000 JIS / 2004 JIS).",
    (1, 1, 29): "U+2014 (em dash) and U+2015 (horizontal bar) both correspond to the same JIS character.\u2002UTC mappings generally favoured U+2015, and Microsoft and consequently WHATWG (HTML5) follow this.\u2002JIS generally esteem it to be U+2014, and Apple follows suit.\u2002OSF maps it as U+2015 in their MS-based version and as U+2014 otherwise.",
    (1, 1, 32): "U+005C (backslash) is sometimes rendered the same as U+00A5 (¥), especially when it's used to map the 7-bit code 0x5C (backslash in ASCII, yen sign in JIS C 6220 / JIS X 0201).\u2002Generally speaking, the double byte character is only mapped to U+005C if is is not used as the mapping for 0x5C: OSF map it as U+005C in JIS-Roman-based EUC but not the other versions, and JIS X 0213 (2000 JIS / 2004 JIS) maps the double byte character to U+005C in Shift_JIS but to U+FF3C in EUC.",
    (1, 1, 33): "Various mappings of various legacy CJK sets map this character to either U+223C (tilde operator), U+301C (wave dash) and U+FF5E (fullwidth tilde).\u2002Of these: U+301C was allocated specifically for the JIS character but was displayed in the Unicode charts with curvature inverted relative to the JIS charts for a considerable time, U+223C is primarily intended as a mathematical operator, U+FF5E is just the fullwidth version of the ASCII character and might therefore be rendered as as either a dash or a spacing accent (and actually has a separate mapping in JIS X 0213, shown as a spacing accent in its chart).",
    (1, 1, 34): "U+2225 is used by Microsoft-influenced mappings, U+2016 is used by others. U+2225 has a separate mapping in JIS X 0213. U+2016 is necessarily straight vertical, whereas U+2225 is often shown slanted.",
    (1, 1, 61): "Microsoft-influenced mappings use U+FF0D for the minus sign (making the JIS minus sign, as opposed to the JIS hyphen, the definitive fullwidth form of the ASCII hyphen-minus). Others use the definitive minus sign codepoint (U+2212).</p><p>Also: WHATWG's (HTML5) encoders actually exceptionally treat both U+2212 and U+FF0D the same (while its decoders use U+FF0D), since doing otherwise was breaking Japanese postcode forms on Macintoshes.",
    (1, 1, 79): "Mapping the double-byte character to U+00A5 is only done when that mapping isn't already used for 0x5C, e.g. JIS X 0213 (2000 JIS / 2004 JIS) does so for EUC but not Shift_JIS.\u2002OSF use U+00A5 here in their ASCII-based EUC mappings, but not in their MS-based or JIS-Roman-based EUC mappings.",
    (1, 1, 82): "Microsoft-influenced mappings use fullwidth characters for the pound and cent sign, because they exist.\u2002Some others don't, because they aren't necessary (separate encoded representations for the regular variants don't exist).",
    (1, 2, 44): "Microsoft-influenced mappings use a fullwidth character for the not sign, because it exists.\u2002Some others don't, because it isn't necessary (a separate encoded representations for the regular variant doesn't exist).</p><p>That being said, a duplicate also exists in the IBM extensions at 02-89-21 (and consequently another in the NEC selection at 01-92-91), predating the allocation of the standard codepoint in 1983.\u2002Accordingly, this codepoint is not allocated in IBM's extended 78JIS (unlike most of the 1983 additions).",
    (1, 2, 72): "The because sign is included three times in the Microsoft and HTML5 version: here (in the 1983 additions), in the NEC row 13 (01-13-90) and in the IBM extensions (02-89-28).\u2002Unlike most of the 1983 additions, this codepoint is not allocated in IBM's extended 78JIS, due to it already existing in the IBM extension section.",
    (1, 9, 0): "NEC apparently tries to incorporate JIS X 0201 (JIS C 6220) here, somewhat like an inverse Shift_JIS. How much Macintosh PostScript follows the NEC extensions apparently varied between font versions; the repertoire shown for it here is the one handled by Apple's ConvertFromTextToUnicode in response to either flag.\u2002KanjiTalk 7 goes off doing its own thing here.",
    (1, 11, 0): "KanjiTalk 6 encodes the vertical forms ten rows (instead of 84 rows) down.",
    (1, 13, 0): "NEC's row 13 seems to have become somewhat of a <i>de facto</i> standard… until it became official standard with the 2000 release of JIS X 0213.\u2002Several of its mathematical symbols duplicate 1983 additions to row 2.\u2002KanjiTalk 7 is still off doing its own thing.",
    (1, 13, 63): "NEC row 13 predates the Heisei era, hence this one isn't present in the Macintosh variants besides KanjiTalk 7, which includes it elsewhere (01-14-74).",
    (1, 13, 90): "Compare 01-02-72.",
    (1, 14, 0): "JIS X 0213 starts the kanji section at row 14, rather than row 16 as in JIS X 0208.\u2002KanjiTalk 6 and KanjiTalk 7 both already use it for their own purposes though.",
    (1, 63, 70): "Compare 01-84-06.",
    (1, 89, 0): "In the NEC and Windows / HTML5 versions, this is the start of the so-called NEC Selection (rows 89–92 inclusive): an alternative encoding within the JIS X 0208 bounds of all the characters in the IBM Extensions block except for those also in NEC row 13.</p><p>Hence in the context of the Windows or HTML5 Shift_JIS variant, all of its allocations are duplicates.\u2002Encoders of that Shift_JIS variant (Windows-31J) vary as to whether they favour the IBM Extensions over the NEC Selection (Windows, WHATWG) or <i>vice versa</i> (Python).",
    (1, 92, 91): "Compare 01-02-44.",
    (1, 93, 70): "01-93-70 (or 02-92-12) is Softbank's Shibuya 109 emoji, U+E50A () in the Unicode Private Use Area.",
    (2, 89, 21): "Compare 01-02-44.",
    (2, 89, 28): "Compare 01-02-72.",
    (2, 92, 12): "02-92-12 (or 01-93-70) is Softbank's Shibuya 109 emoji, U+E50A () in the Unicode Private Use Area.",
    (2, 93, 27): "For some reason, Python's 2000 JIS codecs (unlike its 2004 JIS codecs) map 02-93-27 to U+9B1D (鬝), not to U+9B1C. The ISO-IR-229 registration (registered for the second plane of 2000 JIS, but not superseded upon 2004 JIS) visibly shows a 鬜 (U+9B1C) though.",
}

for n, p in enumerate([plane1, plane2]):
    for q in range(1, 7):
        bn = n + 1
        f = open("jisplane{:X}{}.html".format(bn, chr(0x60 + q)), "w")
        lasturl = lastname = nexturl = nextname = None
        if q > 1:
            lasturl = "jisplane{:X}{}.html".format(bn, chr(0x60 + q - 1))
            lastname = "JIS plane {:d}, part {:d}".format(bn, q - 1)
        elif bn > 1:
            lasturl = "jisplane{:X}f.html".format(bn - 1)
            lastname = "JIS plane {:d}, part 6".format(bn - 1)
        if q < 6:
            nexturl = "jisplane{:X}{}.html".format(bn, chr(0x60 + q + 1))
            nextname = "JIS plane {:d}, part {:d}".format(bn, q + 1)
        elif bn < 2:
            nexturl = "jisplane{:X}a.html".format(bn + 1)
            nextname = "JIS plane {:d}, part 1".format(bn + 1)
        showgraph.dump_plane(f, planefunc, kutenfunc, *p, lang="ja", part=q, css="/css/jis.css",
                             menuurl="/jis-conc.html", menuname="JIS character set variant comparison",
                             lasturl=lasturl, lastname=lastname, nexturl=nexturl, nextname=nextname,
                             annots=annots)
        f.close()








