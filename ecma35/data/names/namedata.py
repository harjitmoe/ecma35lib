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
_nonword = re.compile(r"[^\w-]+")

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
rcldrnameseac = dict(zip(((":" + "_".join(_nonword.split(_i.casefold())) + ":"
                           if ("#" not in _i) and ("*" not in _i) else None
                          ) for _i in cldrnames.values()
                         ), cldrnames.keys()))

def get_cldrname(ucs, default=_no_default, *, fallback=True):
    if ucs.replace("\uFE0F", "") in cldrnames:
        return cldrnames[ucs.replace("\uFE0F", "")]
    if fallback and (len(ucs) == 1):
        altname = ucd.name(ucs, None)
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
    if ucs.replace("\uFE0F", "") in eac:
        return eac[ucs.replace("\uFE0F", "")]
    if fallback:
        cldrname = get_cldrname(ucs, None, fallback=True, insensitive=True)
        if cldrname:
            return ":" + "_".join(_nonword.split(cldrname.casefold())) + ":"
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



