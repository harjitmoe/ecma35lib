#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unicodedata as ucd
import json, re, posixpath
from ecma35.data import graphdata, variationhints, charclass
from ecma35.data.names import namedata

def to_link(maybe_siglum, default_siglum, men, ku, ten):
    siglum = maybe_siglum or default_siglum
    omen, oku, oten = men, ku, ten
    part_zi = int(ku, 10) // 16
    if siglum == "CNS" and men in "ΨΩ":
        basename = "../cnstables/b5xplane"
        if men == "Ψ":
            men = "1"
            if ku <= 65:
                part_zi = (int(ku, 10) - 1) // 16
            elif ku <= 72:
                part_zi = 4
            else:
                part_zi = 5
        if men == "Ψ":
            men = "2"
        else:
            raise AssertionError()
    elif siglum == "KSC" and men == "Ψ":
        basename = "../wansungtables/htxplane"
        men = "1"
    elif siglum == "KSC" and men == "Ω":
        basename = "../wansungtables/ibkplane"
        men = "1"
    else:
        basename = {"CNS": "../cnstables/cnsplane", "JIS": "../jistables2/jisplane",
                    "EACC": "../eacctables/ccciiplane", "CCCII": "../eacctables/ccciiplane",
                    "KSC": "../wansungtables/kscplane"}[siglum]
        men = men.lstrip("0")
    ku = ku.lstrip("0")
    ten = ten.lstrip("0")
    part_letter = chr(0x61 + part_zi)
    if not maybe_siglum:
        basename = posixpath.basename(basename)
    url = f"{basename}{men}{part_letter}.html#{men}.{ku}.{ten}"
    display_siglum = f"{maybe_siglum} " if maybe_siglum else ""
    return f'<a href="{url}">{display_siglum}{omen}-{oku}-{oten}</a>'

siglumre = re.compile("(?:(JIS|CNS|CCCII|EACC|KSC) )?(\d\d|Ψ|Ω)-(\d\d)-(\d\d)")
def inject_links(text, default_siglum=None):
    def callback(m):
        if m.group(1) == None and default_siglum == None:
            return m.group(0)
        return to_link(m.group(1), default_siglum, m.group(2), m.group(3), m.group(4))
    return siglumre.sub(callback, text)

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
        if name in graphdata.defgsets:
            g0set = graphdata.defgsets[name][0]
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
    #
    for (n, i) in enumerate(series):
        if not (n % hs):
            print()
            tplat = "{:2d}: "
            #
            if sz:
                if not ((n // hs) % 2):
                    print(end = tplat.format((n // sz) + ofs))
                else:
                    print(end = " " * 4)
            else:
                print(end = tplat.format((n // hs) + ofs))
        #
        if i is None:
            curchar = "\uFFFD"
            zenkaku = False
        elif isinstance(i, tuple) and (len(i) == 1) and (i[0] < 0):
            curchar = "\u25CC" + chr(-i[0])
            zenkaku = False
        elif (not isinstance(i, tuple)) and (i < 0):
            curchar = "\u25CC" + chr(-i)
            zenkaku = False
        elif isinstance(i, tuple) and (namedata.get_ucscategory(chr(i[0])) == "Co"):
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
        elif namedata.get_ucscategory(chr(i)) == "Co":
            curchar = "\x1B[32m\uFFFC\x1B[m"
            zenkaku = False
        elif 0x80 <= i <= 0x9F:
            curchar = "\x1B[31m\uFFFC\x1B[m"
            zenkaku = False
        else:
            curchar = chr(i)
            zenkaku = (ucd.east_asian_width(chr(i)) in ("W", "F"))
        #
        print(curchar, end = " " if not zenkaku else "")
    for i in range((hs - (n % hs) - 1) % hs):
        print(end = "\uFFFD ")
    print()

def _isbmppua(tpl):
    assert not tpl or not isinstance(tpl[0], str), tpl
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

def _codepfmt(j, oflength):
    ret = f"{j:04X}"
    if (0xFE00 <= j < 0xFE10) or (0xE0100 <= j < 0xE01F0) or (
                                  (oflength > 1) and (0xF850 <= j < 0xF880) ):
        ret = f"({ret})"
    if (0xE000 <= j < 0xF900) or (0xF0000 <= j):
        ret = f"<span class=puacdpt>{ret}</span>"
    return ret

# Using an annoyingly old version of JS here for compatibility's sake
_abbreviation_script = """\
<script>
var abbreviations = """ + json.dumps(charclass.abbreviations) + """;
window.onload = function () {
    var abbrs = document.getElementsByTagName("abbr");
    for (var i = 0; i < abbrs.length; i += 1) {
        var e = abbrs[i];
        var itx = (e.innerText || e.textContent).replace(/^\s+|\s+$/g, '');
        if (typeof abbreviations[itx] != "undefined") {
            e.setAttribute("title", abbreviations[itx]);
        }
    }
};
</script>
"""

# Would rather use this but less compatible
_abbreviation_script_newbrowsers = """\
<script>
var abbreviations = """ + json.dumps(charclass.abbreviations) + """;
window.addEventListener("load", () =>
    [...document.getElementsByTagName("abbr")].filter(e => 
        typeof abbreviations[e.innerText.trim()] != "undefined" 
    ).map(e =>
        e.setAttribute("title", abbreviations[e.innerText.trim()])
    )
);
</script>
"""

def _classify(cdisplayi, outfile):
    print("(<abbr>{}</abbr>)".format(charclass.initialism(cdisplayi[0])), file=outfile)

def is_kanji(cdisplayi):
    if not cdisplayi:
        return None
    elif (len(cdisplayi) > 1) and not ((len(cdisplayi) == 2) and 
                              namedata.get_ucsname(chr(cdisplayi[1]), "").startswith("VARIATION SELECTOR")):
        return False
    elif 0x3400 <= cdisplayi[0] < 0x4DC0:
        return True
    elif 0x4E00 <= cdisplayi[0] < 0xA000:
        return True
    elif 0xF900 <= cdisplayi[0] < 0xFB00:
        return True
    elif 0x20000 <= cdisplayi[0] < 0x30000:
        return True
    elif 0x30000 <= cdisplayi[0] < 0x40000:
        return True
    else:
        return False

def categorise(codept, *, no_ext_punct = True):
    cat = namedata.get_ucscategory(codept)
    if cat[0] == "L":
        colour = "-letter"
    elif cat[0] == "N":
        colour = "-digit"
    elif cat[0] == "P":
        if (ord(codept) < 0x7F) or no_ext_punct:
            colour = "-punct"
        else:
            colour = "-ext-punct"
    elif cat[0] == "S":
        colour = "-graph"
    elif cat[0] == "C" and cat != "Co":
        colour = "-ctrl"
    else:
        colour = "-misc"
    return colour

def _dump_wikitable_row(outfile, typ, array, name="", plane=-1, row=-1, euc=0, nonkanji=False, cdispmap={}, images={}):
    prefix = rowdat = None
    if plane>0 and row>0:
        if euc == 0:
            prefix = "0x{:02X}{:02X}".format(plane+0x20, row+0x20)
        elif euc == 1:
            prefix = "0x{:02X}{:02X}".format(plane+0xA0, row+0xA0)
        else:
            prefix = "0x{:02X}{:02X}/0x{:02X}{:02X}".format(plane+0x20, row+0x20, 
                     plane+0xA0, row+0xA0)
        rowdat = "plane {:d}, row {:d}".format(plane, row)
    elif row>0:
        if euc == 0:
            prefix = "0x{:02X}".format(row+0x20)
        elif euc == 1:
            prefix = "0x{:02X}".format(row+0xA0)
        else:
            prefix = "0x{:02X}/0x{:02X}".format(row+0x20, row+0xA0)
        rowdat = "row {:d}".format(row)
    #
    if nonkanji and (False not in [is_kanji(i) for i in array]):
        return
    if array == ((None,) * len(array)):
        return
    #
    if prefix:
        print("=== {{anchor|%s}}Character set %s (%s) ===" % (
              prefix, prefix, rowdat), file=outfile)
    maybe_prefix = " (prefixed with {})".format(prefix) if prefix else ""
    print("{| {{chset-tableformat}}", file=outfile)
    print("{{chset-table-header|%s%s}}" % (name, maybe_prefix), file=outfile)
    arr2 = array if typ == 96 else (None,) + array + (None,)
    for n in range(6):
        arr3 = arr2[n*16:(n+1)*16]
        print("|-", file=outfile)
        if euc == 0:
            print("!{{chset-left|%X}}" % (n + 2), file=outfile)
        elif euc == 1:
            print("!{{chset-left|%X}}" % (n + 0xA), file=outfile)
        else:
            print("!{{chset-left|%X|%X}}" % (n + 2, n + 0xA), file=outfile)
        for m, i in enumerate(arr3):
            ten = (n * 16) + m
            maybe_kuten = ""
            if plane>0 and row>0:
                maybe_kuten = "|kuten={:d}-{:d}-{:d}".format(plane, row, ten)
            elif row>0:
                maybe_kuten = "|kuten={:d}-{:d}".format(row, ten)
            if (typ == 94) and ((n == 0 and m == 0) or (n == 5 and m == 15)):
                print("|{{chset-color-undef}}|", file=outfile)
                continue
            elif not i:
                if maybe_kuten:
                    print("|{{chset-color-undef}}|{{chset-cell||%s}}" % maybe_kuten, file=outfile)
                else:
                    print("|{{chset-color-undef}}|", file=outfile)
                continue
            dispi = cdispmap.get((n, i), i)
            hexes = " ".join("{:04X}".format(j) for j in dispi) if isinstance(dispi, tuple) \
                                                                 else "{:04X}".format(dispi)
            hexes = hexes.replace(" FE0F ", " ")
            if hexes.endswith(" FE0F"):
                hexes = points[:-5]
            strep = "".join(chr(j) for j in i)
            cat = categorise(strep[0])
            if images and (dispi in images):
                strep = "[[File:" + images[dispi] + "|14px|" + "".join(chr(i) for i in dispi) + "]]"
            elif namedata.get_ucscategory(strep[0]) == "Co":
                strep = "\uFFFD"
            else:
                strep = strep.replace("\uF860", "").replace("\uF861", "").replace("\uF862", "")
                strep = strep.replace("[", "&#x5B;").replace("]", "&#x5D;")
                if (n, i) not in cdispmap:
                    strep = "[[" + strep + "]]"
            print("|{{chset-color%s}}|{{chset-cell|%s|%s%s}}" % (
                  cat, hexes, strep, maybe_kuten), file=outfile)
    print("|}", file=outfile)
    print(file=outfile)

def dump_wikitables(outfile, setname, name="", euc=0, nonkanji=False, cdispmap={}, images={}):
    typ, byts, array = graphdata.gsets[setname]
    assert typ in (94, 96), typ
    if byts == 3:
        for plane in range(1, 95) if typ == 94 else range(96):
            for row in range(1, 95) if typ == 94 else range(96):
                if typ == 94:
                    start = ((plane - 1) * 94 * 94) + ((row - 1) * 94)
                else:
                    start = (plane * 96 * 96) + (row * 96)
                subarray = array[start:start+typ]
                _dump_wikitable_row(outfile, typ, subarray, name, plane, row, euc, nonkanji, cdispmap, images)
    elif byts == 2:
        for row in range(1, 95) if typ == 94 else range(96):
            if typ == 94:
                start = ((row - 1) * 94)
            else:
                start = (row * 96)
            subarray = array[start:start+typ]
            _dump_wikitable_row(outfile, typ, subarray, name, -1, row, euc, nonkanji)
    elif byts == 1:
        _dump_wikitable_row(outfile, typ, array, name, -1, -1, euc)
    else:
        raise AssertionError("unrecognised number of bytes: {!r}".format(byts))

def dump_cccii_wiktionary(outfile, setname="eacc"):
    typ, byts, array = graphdata.gsets[setname]
    print("__NOTOC__", file=outfile)
    print("{{wikipedia|Chinese Character Code for Information Interchange}}", file=outfile)
    print("{{-}}", file=outfile)
    rplanes = [1, 2, 3, 4, 5, 6, 73, 79]
    if "EACC:ONLY3PLANESPERLEVEL" in graphdata.gsetflags[setname]:
        rplanes = [1, 2, 3, 73, 79]
    for rplane in rplanes:
        print("== Plane {:d} ==".format(rplane), file=outfile)
        if rplane < 7:
            planes = [rplane + ((layer - 1) * 6) for layer in range(1, 13)]
        else:
            planes = [rplane]
        for row in range(1, 95):
            starts = [((plane - 1) * 94 * 94) + ((row - 1) * 94) for plane in planes]
            subarrays = [array[start:start+94] for start in starts]
            occupied = len([i for i in zip(*subarrays) if [j for j in i if j]])
            if not occupied:
                continue
            print("=== Plane {:d}, Row {:d} ===".format(rplane, row), file=outfile)
            for redten, i in enumerate(zip(*subarrays)):
                n = len(i)
                while not i[n-1] and n > 1:
                    n -= 1
                i = i[:n]
                streps = [("[[" + "".join(chr(k) for k in j) + "]]") if j else "\uFFFD" for j in i]
                if not "".join(streps).strip("\uFFFD"):
                    continue
                print(end="{{nobr|", file=outfile)
                print(end="{:d}: ".format(redten + 1), file=outfile)
                if (streps[0] == "\uFFFD") or (namedata.get_ucscategory(streps[0][2]) == "Co"):
                    print(end="(〓)", file=outfile)
                else:
                    print(end=streps[0], file=outfile)
                alts = []
                for m, j in enumerate(streps[1:]):
                    if j in ("\uFFFD", streps[0]):
                        continue
                    alts.append("L{:d}:{}".format(m + 2, j))
                if alts:
                    print(end="<sup> (", file=outfile)
                    print(*alts, sep="･", end=")</sup>", file=outfile)
                print(end="}}", file=outfile) # nobr}}
                if redten < 93:
                    print(end=",\u3000", file=outfile)
            print(file=outfile)
            print(file=outfile)

def dump_plane_wiktionary(outfile, setname="eacc"):
    typ, byts, array = graphdata.gsets[setname]
    print("__NOTOC__", file=outfile)
    print("{{wikipedia|Chinese Character Code for Information Interchange}}", file=outfile)
    print("{{-}}", file=outfile)
    for row in range(1, 95):
        start = ((row - 1) * 94)
        subarray = array[start:start+94]
        if not len(subarray):
            continue
        print("=== Row {:d} ===".format(row), file=outfile)
        for redten, i in enumerate(zip(*subarrays)):
            n = len(subarray)
            while not subarray[n-1] and n > 1:
                n -= 1
            i = subarray[:n]
            streps = [("[[" + "".join(chr(k) for k in j) + "]]") if j else "\uFFFD" for j in subarray]
            if not "".join(streps).strip("\uFFFD"):
                continue
            print(end="{{nobr|", file=outfile)
            print(end="{:d}: ".format(redten + 1), file=outfile)
            if (streps[0] == "\uFFFD") or (namedata.get_ucscategory(streps[0][2]) == "Co"):
                print(end="(〓)", file=outfile)
            else:
                print(end=streps[0], file=outfile)
            if redten < 93:
                print(end=",\u3000", file=outfile)
        print(file=outfile)
        print(file=outfile)

def _default_unicodefunc(cdisplayi, outfile, i=None, jlfunc=None, number=None, row=None, cell=None):
    print("<br><span class=cpt>", file=outfile)
    if not isinstance(cdisplayi, list):
        if jlfunc:
            # Note: assumes the URL given won't contain apostrophe
            print("<a href='{:s}'>".format(jlfunc(number, row, cell)), file=outfile)
        print("U+" + "<wbr>+".join(_codepfmt(j, len(cdisplayi))
                               for j in cdisplayi), file=outfile)
        if jlfunc:
            print("</a>", file=outfile)
        if len(cdisplayi) == 1:
            _classify(cdisplayi, outfile)
    else:
        print("???", file=outfile) # TODO work out what to do here.
    #
    if (i is not None) and (not (0xF860 <= i[0] < 0xF870)) and (i != cdisplayi):
        # Single codepoint substituting for a PUA or hint sequence worth displaying
        print("<br>→U+" + "<wbr>+".join(_codepfmt(j, len(i)) for j in i), file=outfile)
        if len(i) == 1:
            _classify(i, outfile)
    print(end="</span>", file=outfile)

def dump_plane(outfile, planefunc, kutenfunc,
               number, setnames, plarray, *, selfhandledanchorlink=False,
               part=0, lang="zh-TW", css=None, annots={}, cdispmap={}, 
               menuurl=None, menuname="Up to menu", jlfunc=None, 
               lasturl=None, nexturl=None, lastname=None, nextname=None,
               is_96=False, is_sbcs=False, pua_collides=False, blot="",
               unicodefunc=_default_unicodefunc, big5ext_mode=False, skiprows=None,
               siglum=None, showbmppuas=None, noallocatenotice=None, planewarn=None):
    """Dump an HTML mapping comparison."""
    if showbmppuas == None:
        showbmppuas = (False,) * len(plarray)
    stx, edx = (1, 95) if not is_96 else (0, 96)
    if is_sbcs:
        stx = 1 if not is_96 else 0
        edx = 2 if not is_96 else 1
    elif part:
        if big5ext_mode:
            bounds = ((1, 17), (17, 33), (33, 49), (49, 65), (66, 73), (73, 83))
            stx, edx = bounds[part - 1]
        else:
            stx, edx = max((part - 1) * 16, stx), min(part * 16, edx)
    stpt = (stx - 1) * 94 if not is_96 else stx * 96
    edpt = (edx - 1) * 94 if not is_96 else edx * 96
    nonvacant_sets = [(i, j) for (i, j) in zip(setnames, plarray) if j[stpt:edpt] != (
                  (None,) * len(j[stpt:edpt]))]
    if len(nonvacant_sets) == 1:
        return dump_preview(outfile, planefunc(number), kutenfunc, number, 
               nonvacant_sets[0][1], lang = lang, css = css, part = part, jlfunc = jlfunc,
               menuurl = menuurl, menuname = menuname, lasturl = lasturl, 
               nexturl = nexturl, lastname = lastname, nextname = nextname,
               is_96 = is_96, is_sbcs = is_sbcs, blot = blot, showbmppua = showbmppuas[0],
               planewarn = planewarn, skiprows = skiprows)
    setnames2 = tuple(zip(*nonvacant_sets))[0] if nonvacant_sets else ()
    zplarray = tuple(zip(*tuple(zip(*nonvacant_sets))[1])) if nonvacant_sets else ()
    h = ", part {:d}".format(part) if part else ""
    print("<!DOCTYPE html><title>{}{}</title>".format(planefunc(number), h), file=outfile)
    print(_abbreviation_script, file=outfile)
    if css:
        print("<link rel='stylesheet' href='{}'>".format(css), file=outfile)
    if blot:
        print(blot, file=outfile)
    print("<h1>{}{}</h1>".format(planefunc(number), h), file=outfile)
    if menuurl or lasturl or nexturl:
        _navbar(outfile, menuurl, menuname, lasturl, lastname, nexturl, nextname)
    if not nonvacant_sets:
        notice = noallocatenotice or "There are no allocated codepoints in this range."
        print(f"<p>{notice}</p>", file=outfile)
        return
    if planewarn:
        print(f"<p>Warning: {planewarn}</p>", file=outfile)
    # Sparse mode is for large sections with barely any allocations, such as the higher planes
    #   of CCCII. Including all the blank space to scroll makes the table barely usable.
    allocated_slots = 0
    sparse = False
    for testpointer in range(stpt, edpt):
        for i, j in nonvacant_sets:
            if testpointer < len(j) and j[testpointer]:
                allocated_slots += 1
                break # break the inner loop
    if allocated_slots < 200:
        sparse = True
    print("<table>", file=outfile)
    if skiprows:
        while stx < edx and stx in skiprows:
            stx += 1
    for row in range(stx, edx):
        if big5ext_mode:
            if row in (65, 71) or row > 82:
                continue
        elif skiprows and row in skiprows:
            continue
        if (not sparse) or (row == stx):
            if row == stx:
                print("<thead>", file=outfile)
            print("<tr><th>Codepoint", file=outfile)
            for i in setnames2:
                print("<th>", i, planefunc(number, i), file=outfile)
            if row == stx:
                print("</thead>", file=outfile)
        if annots.get((number, row, 0), None):
            print("<tr class=annotation><td colspan={:d}><p>".format(len(plarray) + 1), file=outfile)
            print("Note:", inject_links(annots[(number, row, 0)], siglum), file=outfile)
        for cell in (range(1, 95) if not is_96 else range(0, 96)):
            if big5ext_mode:
                if ((row % 2) and (cell < 32)) or ((row == 72) and (cell < 54)):
                    continue
            st = zplarray[((row - 1) * 94) + (cell - 1)] if not is_96 else zplarray[(row * 96) + cell]
            if (sparse or (cell in (0, 95))) and (len(set(i for i in st if i is not None)) == 0) \
                      and not annots.get((number, row, cell), None):
                continue
            elif len(set(i for i in st if (i is not None and not _isbmppua(i)))) > 1:
                print("<tr class=cln>", file=outfile)
            elif pua_collides and (len(set(st) | {None}) > 2):
                print("<tr class=cln>", file=outfile)
            else:
                print("<tr>", file=outfile)
            print("<th class=cpt>", file=outfile)
            print("<a id='{:d}.{:d}.{:d}' class=anchor></a>".format(number, row, cell), file=outfile)
            if selfhandledanchorlink:
                print(kutenfunc(number, row, cell), file=outfile)
            else:
                print("<a href='#{:d}.{:d}.{:d}'>".format(number, row, cell), file=outfile)
                print(kutenfunc(number, row, cell), "</a>", file=outfile)
            for colno, i in enumerate(st):
                showbmppua = showbmppuas[colno]
                if i is None:
                    print("<td class=udf>", file=outfile)
                    continue
                #
                if not is_96:
                    pointer = ((number - 1) * (94 * 94)) + ((row - 1) * 94) + (cell - 1)
                else:
                    pointer = ((number - 1) * (96 * 96)) + (row * 96) + cell
                cdisplayi = cdispmap.get((setnames2[colno], pointer, i), cdispmap.get((pointer, i), i))
                #
                print("<td>", end="", file=outfile)
                if (i != cdisplayi) and isinstance(cdisplayi, tuple) and (
                            cdisplayi[-1] not in range(0xF870, 0xF880)) and (
                            i[0] not in range(0xAC00, 0xD7B0)) and not (
                            0xE000 <= cdisplayi[0] < 0xF900):
                    variationhints.print_hints_to_html5(cdisplayi, outfile, lang=lang, showbmppua=showbmppua)
                    print(" / ", file=outfile)
                variationhints.print_hints_to_html5(i, outfile, lang=lang, showbmppua=showbmppua)
                unicodefunc(cdisplayi, outfile, i)
            if annots.get((number, row, cell), None):
                print("<tr class=annotation><td colspan={:d}><p>".format(len(plarray) + 1), file=outfile)
                print("Note:", inject_links(annots[(number, row, cell)], siglum), file=outfile)
    print("</table>", file=outfile)
    if menuurl or lasturl or nexturl:
        _navbar(outfile, menuurl, menuname, lasturl, lastname, nexturl, nextname)

def dump_preview(outfile, planename, kutenfunc, number, array, *, lang="zh-TW", planeshift="",
               css=None, part=None, menuurl=None, menuname="Up to menu", jlfunc=None, 
               lasturl=None, nexturl=None, lastname=None, nextname=None, showbmppua=False,
               is_96=False, is_sbcs=False, blot="", unicodefunc=_default_unicodefunc,
               planewarn=None, skiprows=None):
    """Dump an HTML single-mapping table."""
    stx, edx = (1, 95) if not is_96 else (0, 96)
    if is_sbcs:
        stx = 1 if not is_96 else 0
        etx = 2 if not is_96 else 1
    elif part:
        stx, edx = max((part - 1) * 16, stx), min(part * 16, edx)
    stpt = (stx - 1) * 94 if not is_96 else stx * 96
    edpt = (edx - 1) * 94 if not is_96 else edx * 96
    h = ", part {:d}".format(part) if part else ""
    print("<!DOCTYPE html><title>{}{}</title>".format(planename, h), file=outfile)
    print(_abbreviation_script, file=outfile)
    if css:
        print("<link rel='stylesheet' href='{}'>".format(css), file=outfile)
    if blot:
        print(blot, file=outfile)
    print("<h1>{}{}</h1>".format(planename, h), file=outfile)
    if menuurl or lasturl or nexturl:
        _navbar(outfile, menuurl, menuname, lasturl, lastname, nexturl, nextname)
    if planewarn:
        print(f"<p>Warning: {planewarn}</p>", file=outfile)
    print("<table class=chart>", file=outfile)
    if skiprows:
        while stx < edx and stx in skiprows:
            stx += 1
    for row in range(stx, edx):
        if skiprows and row in skiprows:
            continue
        if row == stx:
            print("<thead>", file=outfile)
        print("<tr><th>Code", file=outfile)
        print("".join("<th>_{:1X}".format(i) for i in range(0x10)), file=outfile)
        if row == stx:
            print("</thead>", file=outfile)
        print("<tr><th class=cpt>", file=outfile)
        print("<a id='{:d}.{:d}.1' class=anchor></a>".format(number, row), file=outfile)
        print(kutenfunc(number, row, -1), file=outfile)
        print("<td class=udf>", file=outfile)
        for cell in range(1, 95) if not is_96 else range(0, 96):
            if not (cell % 16):
                print("<tr><th class=cpt>", file=outfile)
                print("<a id='{:d}.{:d}.{:d}' class=anchor></a>".format(number, 
                            row, cell), file=outfile)
                print(kutenfunc(number, row, -cell), file=outfile)
            i = array[((row - 1) * 94) + (cell - 1)] if not is_96 else array[(row * 96) + cell]
            if i is None:
                print("<td class=udf>", file=outfile)
                continue
            #
            print("<td>", end="", file=outfile)
            variationhints.print_hints_to_html5(i, outfile, lang=lang, showbmppua=showbmppua)
            unicodefunc(i, outfile, None, jlfunc, number, row, cell)
        print("<td class=udf>", file=outfile)
    print("</table>", file=outfile)
    if menuurl or lasturl or nexturl:
        _navbar(outfile, menuurl, menuname, lasturl, lastname, nexturl, nextname)

def stat(verbose=False):
    for name, i in graphdata.sumps.items():
        print("Sump", name)
        tot = atot = btot = 0
        miss = []
        for esc, k in i.items():
            if isinstance(k, tuple):
                k = k[0]
            if k not in graphdata.gsets:
                tot += 1
                miss.append(k)
            elif esc[-1] < 0x40:
                btot += 1
            elif esc[-1] == 0x7E:
                pass # The nil F-byte
            else:
                atot += 1
        print("Missing:", tot)
        if verbose:
            print(miss)
        print("Present:", atot)
        print("Total standard:", tot + atot)
        print("Custom (private use):", btot)
        print("Total:", tot + atot + btot)
        print()

def dump_maptable(name):
    array = graphdata.gsets[name][2]
    for n, ucses in enumerate(array):
        if ucses == None:
            continue
        ku = (n // 94) + 1
        ten = (n % 94) + 1
        first = ku + 0x20
        second = ten + 0x20
        start = "0x{:02X}{:02X}".format(first, second)
        middle = "U+" + "+".join("{:04X}".format(i) for i in ucses)
        end = "# " + " + ".join(ucd.name(chr(i), "<{:04X}>".format(i)) for i in ucses)
        print(start, middle, end, sep = "\t")

if __name__ == "__main__":
    import sys
    stat("-v" in sys.argv[1:])




