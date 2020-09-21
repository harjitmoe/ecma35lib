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

def _make_shortcode(cldrname, preshyph=False):
    code = cldrname.replace("#", "number_sign").replace("*", "asterisk")
    code = ":" + "_".join((_nonword2 if preshyph else _nonword).split(code.casefold())) + ":"
    code = "".join(i for i in ucd.normalize("NFD", code) if ucd.category(i)[0] != "M")
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
    if fallback and (len(ucss) == 1):
        altname = ucd.name(ucss, None)
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
            tryucs = ucd.lookup(name.casefold().upper().replace("UNICODE ", ""), None)
            if tryucs:
                return tryucs
    if default is _no_default:
        raise KeyError("unrecognised CLDR name: {!r}".format(name))
    return default

with open(os.path.join(directory, "emoji-toolkit/extras/alpha-codes/eac.json"), "r") as f:
    _eacraw = json.load(f)
eac = {}
eacs = {}
reac = {}
for _i in _eacraw.values():
    _ucs = _i["output"].replace("-fe0f", "")
    _ucs = "".join(chr(int(_j, 16)) for _j in _ucs.split("-"))
    eac[_ucs] = _i["alpha_code"]
    eacs[_ucs] = (_i["alpha_code"],) + tuple(_i["aliases"].split("|"))
for _i, _js in eacs.items():
    for _j in _js:
        reac[_j] = _i

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
            try:
                return ucd.lookup(name.casefold().upper().replace("_", " ").strip(":").replace("UNICODE ", ""))
            except KeyError:
                pass
    if default is _no_default:
        raise KeyError("unrecognised shortcode: {!r}".format(name))
    return default



