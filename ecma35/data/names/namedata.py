#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, xml.dom.minidom, re

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "namemaps")
_no_default = object() # need a unique featureless object which isn't used anywhere else.
_nonword = re.compile(r"\W+", re.U)
_nonword2 = re.compile(r"[^\w-]+", re.U)

def _is_cjkui(ucs):
    # Note: excludes the Dirty Dozen
    if len(ucs) != 1:
        return False
    code = ord(ucs)
    if (0x4E00 <= code < 0xA000) or (0x3400 <= code < 0x4DC0) or (0x20000 <= code < 0x2F800) or (
                                     0x30000 <= code < 0x3FFFE):
        return True
    return False

def _is_cjkci(ucs):
    # Note: includes the Dirty Dozen
    if len(ucs) != 1:
        return False
    code = ord(ucs)
    if (0xF900 <= code < 0xFB00) or (0x2F800 <= code < 0x2FFFE):
        return True
    return False

def _is_tangut(ucs):
    if len(ucs) != 1:
        return False
    code = ord(ucs)
    if (0x17000 <= code < 0x18800) or (0x18D00 <= code < 0x18D90):
        return True
    return False

def _is_pua(ucs):
    if len(ucs) > 1:
        return False
    code = ord(ucs)
    if (0xE000 <= code < 0xF900) or (0xF0000 <= code < 0xFFFFE) or (0x100000 <= code < 0x10FFFE):
        return True
    return False

ucsnames = {}
rucsnames = {}
ucscats = {}
canonical_decomp = {} # TODO apparently excludes hangul, which are presumably algorithmic?
compat_decomp = {}
with open(os.path.join(directory, "UCD/UnicodeData.txt"), "r") as f:
    for line in f:
        if not line.strip() or (line[0] == "#"):
            continue
        _ucs, _ucsname, _ucscat, _carenot1, _carenot2, _decompos, _carenot3, _carenot4, \
            _carenot5, _carenot6, _oldname, _carenot7 = line.split(";", 11)
        _ucs = chr(int(_ucs, 16))
        if _ucsname[0] != "<":
            ucsnames[_ucs] = _ucsname
            rucsnames[_ucsname] = _ucs
        if _decompos:
            if _decompos[0] != "<" and not _is_cjkci(_ucs):
                _decompos = "".join(chr(int(_j, 16)) for _j in _decompos.split())
                canonical_decomp[_ucs] = _decompos
            elif _decompos[0] == "<":
                _dectype, _decompos = _decompos[1:].split("> ", 1)
                _decompos = "".join(chr(int(_j, 16)) for _j in _decompos.split())
                compat_decomp[_ucs] = (_dectype, _decompos)
            else:
                _decompos = "".join(chr(int(_j, 16)) for _j in _decompos.split())
                compat_decomp[_ucs] = ("", _decompos)
        if _oldname and (_oldname not in rucsnames): # be overwritten but don't overwrite.
            # Unicode 1 names
            rucsnames[_oldname] = _ucs
        ucscats[_ucs] = _ucscat
with open(os.path.join(directory, "UCD/NamedSequences.txt"), "r") as f:
    for line in f:
        if not line.strip() or (line[0] == "#"):
            continue
        _ucsname, _ucs = line.split(";", 1)
        _ucs = "".join(chr(int(_i, 16)) for _i in _ucs.split())
        ucsnames[_ucs] = _ucsname
        rucsnames[_ucsname] = _ucs
with open(os.path.join(directory, "UCD/NameAliases.txt"), "r") as f:
    for line in f:
        if not line.strip() or (line[0] == "#"):
            continue
        _ucs, _ucsname, status = line.split(";", 2)
        _ucs = "".join(chr(int(_i, 16)) for _i in _ucs.split())
        rucsnames[_ucsname] = _ucs
        if status.strip() != "abbreviation":
            # Generally prefer these ones.
            ucsnames[_ucs] = _ucsname

# Sort out the Korean syllables (which are not listed individually)
# These romanisation tables match those used by, for example, the unicodedata module for syllables,
#   and are presumed to be normative for character names (see below).
_koinit = ("G", "GG", "N", "D", "DD", "R", "M", "B", "BB", "S", "SS",
           "", "J", "JJ", "C", "K", "T", "P", "H")
_komed = ("A", "AE", "YA", "YAE", "EO", "E", "YEO", "YE", "O", "WA", 
          "WAE", "OE", "YO", "U", "WEO", "WE", "WI", "YU", "EU", "YI", "I")
_kofin = ("", "G", "GG", "GS", "N", "NJ", "NH", "D", "L", "LG", "LM", "LB", "LS", 
          "LT", "LP", "LH", "M", "B", "BS", "S", "SS", "NG", "J", "C", "K", "T", "P", "H")
for _initial in range(19):
    for _medial in range(21):
        for _final in range(28):
            _syllcode = chr(_initial * (28 * 21) + _medial * 28 + _final + 0xAC00)
            _initcode = chr(0x1100 + _initial)
            _medialcode = chr(0x1161 + _medial)
            _finalcode = chr(0x11A7 + _final) if _final else None
            if _finalcode:
                canonical_decomp[_syllcode] = _initcode + _medialcode + _finalcode
            else:
                canonical_decomp[_syllcode] = _initcode + _medialcode
            _initname = ucsnames[_initcode].rsplit("CHOSEONG", 1)[1]
            _medialname = ucsnames[_medialcode].rsplit("JUNGSEONG", 1)[1]
            _finalname = ucsnames[_finalcode].rsplit("JONGSEONG", 1)[1] if _finalcode else ""
            # Names used in JOHAB.TXT:
            _name1 = "HANGUL SYLLABLE" + _initname + _medialname + _finalname.replace("-", "")
            # Names used in KSC5601.TXT:
            _name2 = _name1.replace(" ", "-").replace("-SYLLABLE-", " SYLLABLE ")
            # Names used in OLD5601.TXT (though obviously the codepoints have changed).
            # These presumably amount to the Unicode 1 names.
            _name3 = "HANGUL SYLLABLE" + _initname + _medialname + _finalname
            # unicodedata module compatible; presumably normative, but not in NamesList.txt:
            _name5 = "HANGUL SYLLABLE " + _koinit[_initial] + _komed[_medial] + _kofin[_final]
            rucsnames[_name1] = _syllcode
            rucsnames[_name2] = _syllcode
            rucsnames[_name3] = _syllcode
            rucsnames[_name5] = _syllcode
            ucsnames[_syllcode] = _name5
            ucscats[_syllcode] = "Lo"

def get_ucsname(ucs, default=_no_default):
    if ucs in ucsnames:
        return ucsnames[ucs]
    elif _is_cjkui(ucs):
        return "CJK UNIFIED IDEOGRAPH-{:04X}".format(ord(ucs))
    elif _is_cjkci(ucs):
        return "CJK COMPATIBILITY IDEOGRAPH-{:04X}".format(ord(ucs))
    elif _is_tangut(ucs):
        return "TANGUT IDEOGRAPH-{:04X}".format(ord(ucs))
    elif default is _no_default:
        raise KeyError("no known UCS name: {!r}".format(ucs))
    else:
        return default

def lookup_ucsname(name, default=_no_default):
    if name in rucsnames:
        return rucsnames[name]
    elif "IDEOGRAPH-" in name:
        carenot, ucs = name.rsplit("IDEOGRAPH-", 1)
        return chr(int(ucs, 16))
    elif default is _no_default:
        raise KeyError("unrecognised UCS name: {!r}".format(name))
    else:
        return default

def get_ucscategory(ucs, default=_no_default):
    if ucs in ucscats:
        return ucscats[ucs]
    elif _is_cjkui(ucs) or _is_cjkci(ucs) or  _is_tangut(ucs):
        return "Lo"
    elif _is_pua(ucs):
        return "Co"
    elif default is _no_default:
        raise KeyError("no known UCS category: {!r}".format(ucs))
    else:
        return default

cldrnames = {}
_document = xml.dom.minidom.parse(os.path.join(directory, "CLDR/annotations/en.xml"))
for _i in _document.getElementsByTagName("annotation"):
    if _i.hasAttribute("type") and _i.getAttribute("type") == "tts":
        cldrnames[_i.getAttribute("cp")] = _i.firstChild.wholeText
_document = xml.dom.minidom.parse(os.path.join(directory, "CLDR/annotationsDerived/en.xml"))
for _i in _document.getElementsByTagName("annotation"):
    if _i.hasAttribute("type") and _i.getAttribute("type") == "tts":
        cldrnames[_i.getAttribute("cp")] = _i.firstChild.wholeText
rcldrnames = dict(zip(cldrnames.values(), cldrnames.keys()))
rcldrnamesi = dict(zip((_i.casefold() for _i in cldrnames.values()), cldrnames.keys()))

def get_cldrname(ucs, default=_no_default, *, fallback=True):
    ucss = ucs.replace("\uFE0F", "")
    if ucss in cldrnames:
        return cldrnames[ucss]
    if fallback:
        altname = get_ucsname(ucss, None)
        if altname:
            altname = altname.title()
            if altname.casefold() in rcldrnames:
                # i.e. UCS name collides with another character's CLDR name
                altname = "Unicode " + altname
            return altname
    if default is _no_default:
        raise KeyError("no CLDR name: {!r}".format(ucs))
    return default

def lookup_cldrname(name, default=_no_default, *, fallback=True, insensitive=True):
    try:
        if insensitive:
            return rcldrnames.get(name, rcldrnamesi[name.casefold()])
        else:
            return rcldrnames[name]
    except KeyError:
        if fallback:
            tryucs = lookup_ucsname(name.casefold().upper().replace("UNICODE ", ""), None)
            if tryucs:
                return tryucs
    if default is _no_default:
        raise KeyError("unrecognised CLDR name: {!r}".format(name))
    return default

with open(os.path.join(directory, "emoji-toolkit/extras/alpha-codes/eac.json"), "r") as f:
    _eacraw = json.load(f)
eac = {}
reac = {}
fe0f_decor = {}
for _i in _eacraw.values():
    _ucs = "".join(chr(int(_j, 16)) for _j in _i["output"].split("-"))
    _ucss = _ucs.replace("\uFE0F", "")
    _i["_ucs"] = _ucs
    _i["_ucss"] = _ucss
    if _ucss != _ucs:
        fe0f_decor[_ucss] = _ucs
    _shortcode = _i["alpha_code"]
    if _ucss in cldrnames:
        if (_i["name"] != cldrnames[_ucss]) and ("person" in cldrnames[_ucss]):
            # Sort out gender-neutral naming that the emoji-toolkit data is too old to encorporate.
            _shortcode = _shortcode.replace("bride_", "person_").replace("man_",
                         "person_").replace("woman_", "person_")
    eac[_ucss] = _shortcode
    reac[_shortcode] = _ucs
def _make_shortcode(cldrname, preshyph=False):
    # Turn a CLDR name into what will usually match the so-called "Emojipedia" shortcodes, which
    # are generated from CLDR names. The preshyph arg preserves hyphens rather than changing them
    # to underscores, and is intended to be used in UCS name fallback cases, where parsing the
    # resulting shortcode relies on re-obtaining the original UCS name.
    # In cases where collisions occur with emoji-toolkit data, the prefix cldr_ or unicode_
    # is prepended.
    code = cldrname.replace("#", "number_sign").replace("*", "asterisk")
    code = ":" + "_".join((_nonword2 if preshyph else _nonword).split(code.casefold())) + ":"
    code = "".join(canonical_decomp.get(i, i)[0] for i in code) # strip diacritics
    if cldrname in rcldrnames:
        decor = fe0f_decor.get(rcldrnames[cldrname], rcldrnames[cldrname])
        if code in reac and (reac[code] != decor):
            newcode = ":cldr_" + code[1:]
            #print(decor, code, "→", newcode)
            code = newcode
    else:
        plain = cldrname.casefold().upper().replace("_", " ").strip(":")
        if plain in rucsnames:
            if code in reac and (reac[code].replace("\uFE0F", "") != rucsnames[plain]):
                newcode = ":unicode_" + code[1:]
                #print(rucsnames[plain], code, "→", newcode)
                code = newcode
    return code
rcldrnameseac = dict(zip((_make_shortcode(_i, preshyph=False) for _i in cldrnames.values()),
                         (fe0f_decor.get(_i, _i) for _i in cldrnames.keys())))
for _i in _eacraw.values():
    # This does a number of things:
    # (1) emoji-toolkit seem to neglect to include the ZWJ characters in the "output" field of 
    #     several (not all) of the handshakes, and this fixes it.
    # (2) Fixes the "man_in_tuxedo" collision (emoji-toolkit names predate that ones gender marking).
    for _j in (_i["alpha_code"],) + tuple(_i["aliases"].split("|")):
        if _j not in reac:
            # We should just keep :om: as :flag_om:, not change it to :om_symbol:
            if (_i["_ucs"] == rcldrnameseac.get(_j, _i["_ucs"])) or (_j == ":om:"):
                reac[_j] = _i["_ucs"]
            elif _j in rcldrnameseac:
                #print("overriding", _j, repr(_i["_ucs"]), "→", repr(rcldrnameseac[_j]))
                reac[_j] = rcldrnameseac[_j]

def get_shortcode(ucs, default=_no_default, *, fallback=True):
    ucss = ucs.replace("\uFE0F", "")
    if ucss in eac:
        return eac[ucss]
    if fallback:
        cldrname = get_cldrname(ucs, None, fallback=False)
        if cldrname:
            return _make_shortcode(cldrname, preshyph=False)
        ucsname = get_cldrname(ucs, None, fallback=True)
        if ucsname:
            return _make_shortcode(ucsname, preshyph=True)
    if default is _no_default:
        raise KeyError("no shortcode name: {!r}".format(ucs))
    return default

def lookup_shortcode(name, default=_no_default, *, fallback=True):
    try:
        return reac[name.casefold()]
    except KeyError:
        if fallback:
            trycldr = rcldrnameseac.get(name.casefold(), None)
            if trycldr:
                return trycldr
            if name[0] == name[-1] == ":":
                tryucs = lookup_ucsname(name.casefold().upper().replace("_", " ").strip(":"
                                        ).replace("UNICODE ", ""), None)
                if tryucs:
                    return tryucs
    if default is _no_default:
        raise KeyError("unrecognised shortcode: {!r}".format(name))
    return default

def test():
    for i in range(0x30000):
        c = chr(i)
        sc = get_shortcode(c, None)
        if sc:
            rt = lookup_shortcode(sc)
            if rt.strip("\uFE0F") != c:
                print(c + "\uFE0F", "→", sc, "→", rt, "→", get_shortcode(rt, None))
        cl = get_cldrname(c, None)
        if cl:
            rt = lookup_cldrname(cl)
            if rt.strip("\uFE0F") != c:
                print(c + "\uFE0F", "→", cl, "→", rt, "→", lookup_cldrname(rt, None))
        uc = get_ucsname(c, None)
        if uc:
            rt = lookup_ucsname(uc)
            if rt != c:
                print(c + "\uFE0F", "→", uc, "→", rt, "→", lookup_ucsname(rt, None))


