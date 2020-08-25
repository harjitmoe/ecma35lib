#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, binascii, ast, re
import unicodedata as ucd

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sbmaps")
_temp = []
identitymap = lambda pointer, ucs: ucs

def read_single_byte(fil, *, mapper=identitymap, typ="plainext"):
    for _i in open(os.path.join(directory, fil), "r", encoding="utf-8"):
        pointer = None
        if not _i.strip():
            continue
        elif _i[0] == "#":
            continue # is a comment.
        elif _i[0] == "<" and _i[:2] != "<U":
            continue # is ICU metadata or state machine config which isn't relevant to us.
        elif _i.strip() in ("CHARMAP", "END CHARMAP"):
            continue # ICU delimitors we don't care about.
        # TODO fix repeated code here.
        elif _i[:2] == "<U":
            # ICU-style format
            ucs, byts, direction = _i.split(" ", 2)
            assert byts[:2] == "\\x" and len(byts) == 4
            byts = byts[2:4]
            if direction.strip() == "|1":
                # i.e. best-fit mapped by the encoder only
                # Whereas, |3 means it's used only by the decoder (usually because duplicate)
                continue
        elif _i[:2] == "0x":
            # Consortium-style format
            byts, ucs = _i.split("\t", 2)[:2]
            assert len(byts) == 4, byts
            byts = byts[2:4]
        elif typ != "plainext":
            # Adobe-via-UTC-style format
            ucs, byts = _i.split("\t", 2)[:2]
            assert len(byts) == 2, byts
        else:
            # Format of the WHATWG-supplied indices
            byts, ucs = _i.split("\t", 2)[:2]
            pointer = int(byts.strip(), 10)
        #
        if pointer is None:
            if typ == "plainext":
                pointer = int(byts, 16) - 0x80
                if pointer < 0:
                    continue
            elif typ == "GL94":
                pointer = int(byts, 16) - 0x21
                if (pointer < 0) or (pointer > 93):
                    continue
            elif typ == "GR94":
                pointer = int(byts, 16) - 0xA1
                if (pointer < 0) or (pointer > 93):
                    continue
            elif typ == "GR96":
                pointer = int(byts, 16) - 0xA0
                if pointer < 0:
                    continue
            elif typ == "CL33":
                pointer = int(byts, 16)
                if pointer > 32:
                    continue
            else:
                raise ValueError("unknown type {!r}".format(typ))
        #
        if ucs[:2] in ("0x", "U+", "<U"):
            ucs = mapper(pointer, tuple(int(j, 16) for j in ucs[2:].rstrip(">").split("+")))
        else:
            ucs = mapper(pointer, (int(ucs, 16),))
        #
        if len(_temp) > pointer:
            if _temp[pointer]:
                # Favour the earlier listed mapping unless it has a compatibility decomposition
                if chr(_temp[pointer][0]) == ucd.normalize("NFKC", chr(_temp[pointer][0])):
                    continue
            _temp[pointer] = ucs
        else:
            while len(_temp) < pointer:
                _temp.append(None)
            _temp.append(ucs)
    if typ == "CL33":
        _temp.extend([None] * (33 - len(_temp)))
    elif typ in ("GL94", "GR94"):
        _temp.extend([None] * (94 - len(_temp)))
    elif typ == "GR96":
        _temp.extend([None] * (96 - len(_temp)))
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    return r

comments89re = re.compile(r"\s+|\s*/\*(?:[^*]|\*[^/]|\*$)*\*/\s*")
def read_mozilla_ut_file(fil, *, mapper=identitymap, typ="plainext"):
    fd = open(os.path.join(directory, fil), "r", encoding="utf-8")
    dat = fd.read()
    fd.close()
    array = [ast.literal_eval(i) for i in "".join(comments89re.split(dat)).strip(",").split(",")]
    junk = array[0] # item of list
    formoff = array[1] # format array offset
    celloff = array[2] # mapping cells offset
    taboff = array[3] # mapping tables offset
    formats = []
    for ptr in range(formoff, celloff):
        pkd = array[ptr]
        formats.extend([pkd & 0xF, (pkd >> 4) & 0xF, (pkd >> 8) & 0xF, (pkd >> 12) & 0xF])
    formats = formats[:(taboff - celloff) // 3]
    for n, fmt in enumerate(formats):
        cptr = celloff + (n * 3)
        if fmt == 0: # Range mapping
            source_begin, source_end, dest_begin = array[cptr:cptr+3]
            froms = list(range(source_begin, source_end + 1))
            tos = list(range(dest_begin, dest_begin + 1 + (source_end - source_begin)))
        elif fmt == 1: # Table mapping
            source_begin, source_end, tableidx = array[cptr:cptr+3]
            froms = list(range(source_begin, source_end + 1))
            tos = array[taboff + tableidx : taboff + tableidx + 1 + (source_end - source_begin)]
        elif fmt == 2: # Spot mapping
            source, dummy_source_end, dest = array[cptr:cptr+3]
            froms = [source]
            tos = [dest]
        elif fmt == 3: # No idea; I've encountered no examples though they supposedly exist.
            raise NotImplementedError
        else:
            raise ValueError("unrecognised Mozilla .ut file item type: {!r}".format(fmt))
        for frm, ucs in zip(froms, tos):
            if typ == "plainext":
                optr = frm - 0x80
                if optr > 127 or optr < 0:
                    continue
            elif typ == "GL94":
                optr = frm - 0x21
                if optr > 93 or optr < 0:
                    continue
            elif typ == "GR94":
                optr = frm - 0xA1
                if optr > 93 or optr < 0:
                    continue
            elif typ == "GR96":
                optr = frm - 0xA0
                if optr > 95 or optr < 0:
                    continue
            elif typ == "CL33":
                optr = frm
                if optr > 32 or ucs <= 32:
                    continue
            else:
                raise ValueError("unknown type {!r}".format(typ))
            if len(_temp) > optr:
                if _temp[optr] is None: # earlier items trump later items (in e.g. vps.ut)
                    _temp[optr] = (ucs,)
            else:
                _temp.extend([None] * (optr - len(_temp)))
                _temp.append(ucs)
    if typ == "CL33":
        _temp.extend([None] * (33 - len(_temp)))
    elif typ in ("GL94", "GR94"):
        _temp.extend([None] * (94 - len(_temp)))
    elif typ == "GR96":
        _temp.extend([None] * (96 - len(_temp)))
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    return r
    





