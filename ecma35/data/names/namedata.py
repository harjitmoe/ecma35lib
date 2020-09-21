#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, json, xml.dom.minidom, re
import unicodedata as ucd

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "namemaps")
_no_default = object() # need a unique featureless object which isn't used anywhere else.
_nonword = re.compile(r"\W+", re.U)
_nonword2 = re.compile(r"[^\w-]+", re.U)

ucsnames = {}
rucsnames = {}
ucscats = {}
canonical_decomp = {} # TODO apparently excludes hangul, which are presumably algorithmic?
compat_decomp = {}
with open(os.path.join(directory, "UCD/UnicodeData.txt"), "r") as f:
    for line in f:
        if not line.strip() or (line[0] == "#"):
            continue
        _ucs, _ucsname, _ucscat, _carenot1, _carenot2, _decompos, _carenot3 = line.split(";", 6)
        _ucs = chr(int(_ucs, 16))
        if _ucsname[0] != "<":
            ucsnames[_ucs] = _ucsname
            rucsnames[_ucsname] = _ucs
        if _decompos:
            if _decompos[0] != "<": # i.e. if it exists and is of canonical type
                _decompos = "".join(chr(int(_j, 16)) for _j in _decompos.split())
                canonical_decomp[_ucs] = _decompos
            else:
                _dectype, _decompos = _decompos[1:].split("> ", 1)
                _decompos = "".join(chr(int(_j, 16)) for _j in _decompos.split())
                compat_decomp[_ucs] = (_dectype, _decompos)
        ucscats[_ucs] = _ucscat
with open(os.path.join(directory, "UCD/NamedSequences.txt"), "r") as f:
    for line in f:
        if not line.strip() or (line[0] == "#"):
            continue
        _ucsname, _ucs = line.split(";", 1)
        _ucs = "".join(chr(int(_i, 16)) for _i in _ucs.split())
        ucsnames[_ucs] = _ucsname
        rucsnames[_ucsname] = _ucs

def get_ucsname(ucs, default=_no_default):
    if ucs in ucsnames:
        return ucsnames[ucs]
    elif default is _no_default:
        raise KeyError("no known UCS name: {!r}".format(ucs))
    else:
        return default

def lookup_ucsname(name, default=_no_default):
    if name in rucsnames:
        return rucsnames[name]
    elif default is _no_default:
        raise KeyError("unrecognised UCS name: {!r}".format(name))
    else:
        return default

def get_ucscategory(ucs, default=_no_default):
    if ucs in ucscats:
        return ucscats[ucs]
    elif default is _no_default:
        raise KeyError("no known UCS category: {!r}".format(ucs))
    else:
        return default

def _make_shortcode(cldrname, preshyph=False):
    # Turn a CLDR name into what will usually match the so-called "Emojipedia" shortcodes, which
    # are generated from CLDR names. The preshyph arg preserves hyphens rather than changing them
    # to underscores, and is intended to be used in UCS name fallback cases, where parsing the
    # resulting shortcode relies on re-obtaining the original UCS name.
    code = cldrname.replace("#", "number_sign").replace("*", "asterisk")
    code = ":" + "_".join((_nonword2 if preshyph else _nonword).split(code.casefold())) + ":"
    code = "".join(canonical_decomp.get(i, i)[0] for i in code) # strip diacritics
    return code

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
rcldrnameseac = dict(zip((_make_shortcode(_i, preshyph=False) for _i in cldrnames.values()),
                         cldrnames.keys()))

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
for _i in _eacraw.values():
    _ucs = "".join(chr(int(_j, 16)) for _j in _i["output"].split("-"))
    _ucss = _ucs.replace("\uFE0F", "")
    eac[_ucss] = _i["alpha_code"]
    for _j in (_i["alpha_code"],) + tuple(_i["aliases"].split("|")):
        reac[_j] = _ucs

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



