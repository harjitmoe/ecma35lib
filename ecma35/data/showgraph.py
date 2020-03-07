#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd

from ecma35.data import graphdata

def formatcode(tpl):
    if tpl is None:
        return "None"
    return "U+{} ({})".format("+".join("{:04X}".format(i) for i in tpl),
                              "".join(chr(i) if i < 0xF0000 else (chr(i) + " ") for i in tpl))

def show(name, *, plane=None):
    if isinstance(name, tuple):
        x = name
    elif name in graphdata.rhses:
        if name in graphdata.c0graphics:
            c0list = graphdata.c0graphics[name]
        else:
            c0list = graphdata.c0graphics["437"]
        assert len(c0list) == 33
        if name in defcsets:
            g0set = defcsets[name][0]
        else:
            g0set = "ir006"
        if graphdata.gsets[g0set][0] == 94:
            x = (256, 1, c0list[:-1] + (0x20,) + graphdata.gsets[g0set][2] + 
                         c0list[-1:] + graphdata.rhses[name])
        else:
            assert graphdata.gsets[g0set][0] == 96
            x = (256, 1, c0list[:-1] + graphdata.gsets[g0set][2] + graphdata.rhses[name])
    elif name in graphdata.gsets:
        x = graphdata.gsets[name]
    else:
        raise ValueError("unknown set: {!r}".format(name))
    #
    if x[1] == 1:
        sz = 0
        hs = 16
        ofs = 2 if x[0] <= 96 else (8 if x[0] <= 128 else 0)
        series = ((0x20,) if x[0] < 96 else ()) + x[2]
    elif x[1] == 2:
        sz = x[0]
        hs = sz // 2
        ofs = (8 - (hs % 8)) % 8
        series = x[2]
    elif x[1] == 3:
        if plane is None:
            raise ValueError("must specify a single plane to display a multi-plane set")
        elif (plane < 1) and (x[0] <= 94):
            raise ValueError("plane number for a 94^n-set must be at least 1")
        elif plane < 0:
            raise ValueError("plane number for a 96^n-set must be at least 0")
        sz = x[0]
        hs = sz // 2
        ofs = (8 - (hs % 8)) % 8
        series = x[2][(sz * sz) * ((plane - 1) if x[0] <= 94 else plane):][:(sz * sz)]
    else:
        raise ValueError("unsupported set byte length size")
    for (n, i) in enumerate(series):
        if not (n % hs):
            print()
            if sz:
                if not ((n // hs) % 2):
                    print(end = "{:2d}: ".format((n // sz) + ofs))
                else:
                    print(end = " " * 4)
            else:
                print(end = "{:2d}: ".format((n // hs) + ofs))
        #
        if i is None:
            curchar = "\uFFFD"
            zenkaku = False
        elif isinstance(i, tuple) and (ucd.category(chr(i[0])) == "Co"):
            if len(i) == 1:
                curchar = "\x1B[35m\uFFFC\x1B[m"
            else:
                curchar = "\x1B[33m\uFFFC\x1B[m"
            zenkaku = False
        elif isinstance(i, tuple) and (0x80 <= i[0] <= 0x9F):
            curchar = "\x1B[31m\uFFFC\x1B[m"
            zenkaku = False
        elif isinstance(i, tuple):
            curchar = "".join(chr(j) for j in i)
            if 0xF870 <= ord(curchar[-1]) <= 0xF87F:
                if curchar[-1] == "\uF874":
                    # Left position (red).
                    curchar = "\x1B[91m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF875":
                    # Low left position (darker red).
                    curchar = "\x1B[31m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF876":
                    # Rotated (turquoise).
                    curchar = "\x1B[36m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF877":
                    # Superscript (yellow).
                    curchar = "\x1B[93m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF878":
                    # Small (dim grey)
                    curchar = "\x1B[90m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF879":
                    # Large (bright blue)
                    curchar = "\x1B[94m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF87A":
                    # Negative (inverse video)
                    curchar = "\x1B[7m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF87B":
                    # Medium bold (bright white)
                    curchar = "\x1B[97m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF87C":
                    # Bold
                    curchar = "\x1B[1m" + curchar[:-1] + "\x1B[m"
                elif curchar[-1] == "\uF87E":
                    # VERTical forms not in Unicode: show in green.
                    curchar = "\x1B[32m" + curchar[:-1] + "\x1B[m"
                else:
                    curchar = "\x1B[33m" + curchar[:-1] + "\x1B[m"
            zenkaku = (ucd.east_asian_width(chr(i[0])) in ("W", "F"))
        elif ucd.category(chr(i)) == "Co":
            curchar = "\x1B[32m\uFFFC\x1B[m"
            zenkaku = False
        elif 0x80 <= i <= 0x9F:
            curchar = "\x1B[31m\uFFFC\x1B[m"
            zenkaku = False
        else:
            curchar = chr(i)
            zenkaku = (ucd.east_asian_width(chr(i)) in ("W", "F"))
        print(curchar, end = " " if not zenkaku else "")
    for i in range((hs - (n % hs) - 1) % hs):
        print(end = "\uFFFD ")
    print()

def _isbmppua(tpl):
    return (len(tpl) == 1) and 0xE000 <= tpl[0] < 0xF900

def _navbar(outfile, menuurl, menuname, lasturl, lastname, nexturl, nextname):
    print("<hr><nav><ul class=navbar>", file=outfile)
    if lasturl:
        print("<li><span class=navlabel>Previous:</span>", file=outfile)
        print("<a href='{}' rel=prev class=sectref>{}</a></li>".format(lasturl, lastname), file=outfile)
    if menuurl:
        print("<li><span class=navlabel>Up:</span>", file=outfile)
        print("<a href='{}' rel=parent class=sectref>{}</a></li>".format(menuurl, menuname), file=outfile)
    if nexturl:
        print("<li><span class=navlabel>Next:</span>", file=outfile)
        print("<a href='{}' rel=next class=sectref>{}</a></li>".format(nexturl, nextname), file=outfile)
    print("</ul></nav><hr>", file=outfile)

def dump_plane(outfile, planefunc, kutenfunc,
               number, setnames, plarray, *,
               part=0, lang="zh-TW", css=None,
               menuurl=None, menuname="Up to menu",
               lasturl=None, nexturl=None, lastname=None, nextname=None):
    zplarray = tuple(zip(*plarray))
    h = ", part {:d}".format(part) if part else ""
    print("<!DOCTYPE html><title>{}{}</title>".format(planefunc(number), h), file=outfile)
    if css:
        print("<link rel='stylesheet' href='{}'>".format(css), file=outfile)
    print("<h1>{}{}</h1>".format(planefunc(number), h), file=outfile)
    if menuurl or lasturl or nexturl:
        _navbar(outfile, menuurl, menuname, lasturl, lastname, nexturl, nextname)
    print("<table>", file=outfile)
    for row in range(max((part - 1) * 16, 1), min(part * 16, 95)) if part else range(1, 95):
        print("<thead><tr><th>Codepoint</th>", file=outfile)
        for i in setnames:
            print("<th>", i, planefunc(number, i), file=outfile)
        print("</tr></thead>", file=outfile)
        for cell in range(1, 95):
            st = zplarray[((row - 1) * 94) + (cell - 1)]
            if len(set(i for i in st if (i is not None and not _isbmppua(i)))) > 1:
                print("<tr class=collision>", file=outfile)
            else:
                print("<tr>", file=outfile)
            print("<th class=codepoint>", file=outfile)
            print("<a name='{:d}.{:d}.{:d}' class=anchor></a>".format(number, row, cell), file=outfile)
            print("<a href='#{:d}.{:d}.{:d}'>".format(number, row, cell), file=outfile)
            print(kutenfunc(number, row, cell), "</a>", file=outfile)
            print("</th>", file=outfile)
            for i in st:
                if i is None:
                    print("<td class=undefined></td>", file=outfile)
                    continue
                #
                if i[0] >= 0xF0000:
                    print("<td><span class='codepicture spua' lang={}>".format(lang), file=outfile)
                    strep = "".join(chr(j) for j in i)
                elif 0xF860 <= i[0] < 0xF863 and len(i) != 1:
                    print("<td><span class='codepicture' lang={}>".format(lang), file=outfile)
                    strep = "".join(chr(j) for j in i[1:]).replace("\uF860", "").replace("\uF861", 
                                                                   "").replace("\uF862", "")
                elif 0xE000 <= i[0] < 0xF900:
                    print("<td><span class='codepicture pua' lang={}>".format(lang), file=outfile)
                    # Object Replacement Character (FFFD is already used by BIG5.TXT)
                    strep = "\uFFFC"
                elif 0x10000 <= i[0] < 0x20000:
                    # SMP best to fall back to applicable emoji (or otherwise applicable) fonts,
                    # and not try to push CJK fonts first.
                    print("<td><span class='codepicture smp' lang={}>".format(lang), file=outfile)
                    strep = "".join(chr(j) for j in i)
                else:
                    strep = "".join(chr(j) for j in i)
                    firststrep = ucd.normalize("NFD", strep)[0] # Note: NOT NFKD.
                    if ord(firststrep) < 0x7F:
                        print("<td><span class='codepicture roman'>", file=outfile)
                    elif (ucd.category(firststrep)[0] == "M") and (ord(firststrep) < 0x3000):
                        print("<td><span class='codepicture roman'>", file=outfile)
                    else:
                        print("<td><span class=codepicture lang={}>".format(lang), file=outfile)
                #
                strep = strep.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if ucd.category(strep[0])[0] == "M":
                    strep = "◌" + strep
                if i[-1] == 0xF87C: # Apple encoding hint for bold form
                    print("<b>", file=outfile)
                    print(strep.rstrip("\uF87C"), file=outfile)
                    print("</b>", file=outfile)
                elif i[-1] == 0xF87E: # Apple encoding hint for vertical presentation form
                    print("<span class=vertical>", file=outfile)
                    print(strep.rstrip("\uF87E"), file=outfile)
                    print("</span>", file=outfile)
                else:
                    # Horizontal presentation form, alternative form.
                    # Neither of which we can really do anything with here.
                    print(strep.rstrip("\uF87D\uF87F"), file=outfile)
                print("</span>", file=outfile)
                print("<br><span class=codepoint>", file=outfile)
                print("U+" + "<wbr>+".join("{:04X}".format(j) for j in i), file=outfile)
                if len(i) == 1:
                    #####################################
                    # BASIC MULTILINGUAL PLANE
                    if i[0] < 0x80:
                        print("(<abbr title='American Standard Code for " +
                              "Information Interchange'>ASCII</abbr>)", file=outfile)
                    elif 0x80 <= i[0] < 0x100:
                        print("(<abbr title='Latin-1 Supplement'>LAT1S</abbr>)", file=outfile)
                    elif 0x2E80 <= i[0] < 0x2FE0:
                        print("(<abbr title='CJK Radical'>RAD</abbr>)", file=outfile)
                    elif 0x31C0 <= i[0] < 0x31E0:
                        print("(<abbr title='CJK Stroke'>STRK</abbr>)", file=outfile)
                    elif 0x3400 <= i[0] < 0x4DC0:
                        print("(<abbr title='CJK Extension A'>CJKA</abbr>)", file=outfile)
                    elif 0x4E00 <= i[0] < 0x9FA6:
                        print("(<abbr title='Unified Repertoire and Ordering'>URO</abbr>)", file=outfile)
                    elif 0x9FA6 <= i[0] < 0xA000:
                        print("(<abbr title='Appendage to Unified Repertoire and Ordering'>URO+</abbr>)", 
                              file=outfile)
                    elif 0xE000 <= i[0] < 0xF900:
                        print("(<abbr title='Private Use Area'>PUA</abbr>)", file=outfile)
                    elif 0xF900 <= i[0] < 0xFB00: # the BMP's Compatibility Ideographs block
                        if i[0] in (0xFA0E, 0xFA0F, 0xFA11, 0xFA13, 0xFA14, 0xFA1F,
                                    0xFA21, 0xFA23, 0xFA24, 0xFA27, 0xFA28, 0xFA29):
                            print("(<abbr title='Dirty Dozen (of unified ideographs in the "
                                  "Compatibility Ideographs block)'>DD</abbr>)", file=outfile)
                        else:
                            print("(<abbr title='Compatibility Ideograph'>CI</abbr>)", file=outfile)
                    elif 0xFE50 <= i[0] < 0xFE70:
                        print("(<abbr title='Small Form Variant'>SFV</abbr>)", file=outfile)
                    elif (0xFF01 <= i[0] < 0xFF61) or (0xFFE0 <= i[0] < 0xFFE7):
                        print("(<abbr title='Full-Width Form'>FWF</abbr>)", file=outfile)
                    elif i[0] in (0xFFFC, 0xFFFD):
                        print("(<abbr title='Replacement Character'>REPL</abbr>)", file=outfile)
                    elif i[0] < 0x10000:
                        print("(<abbr title='Miscellaneous Basic Multilingual Plane'>BMP</abbr>)", 
                              file=outfile)
                    #####################################
                    # SUPPLEMENTARY MULTILINGUAL PLANE
                    elif 0x10000 <= i[0] < 0x20000:
                        print("(<abbr title='Supplementary Multilingual Plane'>SMP</abbr>)", 
                              file=outfile)
                    #####################################
                    # SUPPLEMENTARY IDEOGRAPHIC PLANE
                    elif 0x20000 <= i[0] < 0x2A6E0:
                        print("(<abbr title='CJK Extension B'>CJKB</abbr>)", file=outfile)
                    elif 0x2A700 <= i[0] < 0x2B740:
                        print("(<abbr title='CJK Extension C'>CJKC</abbr>)", file=outfile)
                    elif 0x2B740 <= i[0] < 0x2B820:
                        print("(<abbr title='CJK Extension D'>CJKD</abbr>)", file=outfile)
                    elif 0x2B820 <= i[0] < 0x2CEB0:
                        print("(<abbr title='CJK Extension E'>CJKE</abbr>)", file=outfile)
                    elif 0x2CEB0 <= i[0] < 0x2EBF0:
                        print("(<abbr title='CJK Extension F'>CJKF</abbr>)", file=outfile)
                    elif 0x2F800 <= i[0] < 0x2FA20:
                        print("(<abbr title='Compatibility Ideographs Supplement'>CIS</abbr>)", 
                              file=outfile)
                    elif 0x20000 <= i[0] < 0x30000:
                        print("(<abbr title='Miscellaneous Supplementary Ideographic Plane'>SIP</abbr>)", 
                              file=outfile)
                    #####################################
                    # TERTIARY IDEOGRAPHIC PLANE
                    elif 0x30000 <= i[0] < 0x40000:
                        print("(<abbr title='Tertiary Ideographic Plane'>TIP</abbr>)", file=outfile)
                    #####################################
                    # SUPPLEMENTARY SPECIAL-PURPOSE PLANE
                    elif 0xE0000 <= i[0] < 0xF0000:
                        print("(<abbr title='Supplementary Special-purpose Plane'>SSP</abbr>)", 
                              file=outfile)
                    #####################################
                    # SUPPLEMENTARY PRIVATE USE AREA
                    elif 0xF0000 <= i[0] < 0x100000:
                        print("(<abbr title='Supplementary Private-Use Area A'>SPUA</abbr>)", file=outfile)
                    elif i[0] >= 0x100000:
                        print("(<abbr title='Supplementary Private-Use Area B'>SPUB</abbr>)", file=outfile)
                print("</span></td>", file=outfile)
            print("</tr>", file=outfile)
    print("</table>", file=outfile)
    if menuurl or lasturl or nexturl:
        _navbar(outfile, menuurl, menuname, lasturl, lastname, nexturl, nextname)





