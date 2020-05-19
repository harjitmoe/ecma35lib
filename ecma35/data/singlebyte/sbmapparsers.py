#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, binascii

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sbmaps")
_temp = []
identitymap = lambda pointer, ucs: ucs

def read_single_byte(fil, *, mapper=identitymap, typ="plainext"):
    for _i in open(os.path.join(directory, fil), "r", encoding="utf-8"):
        if not _i.strip():
            continue
        elif _i[0] == "#":
            continue # is a comment.
        elif _i[0] == "<" and _i[:2] != "<U":
            continue # is ICU metadata or state machine config which isn't relevant to us.
        elif _i.strip() in ("CHARMAP", "END CHARMAP"):
            continue # ICU delimitors we don't care about.
        elif _i[:2] == "0x":
            # Consortium-style format
            byts, ucs = _i.split("\t", 2)[:2]
            assert len(byts) == 4
            if typ == "plainext":
                pointer = int(byts[2:4], 16) - 0x80
                if pointer < 0:
                    continue
            elif typ == "GL94":
                pointer = int(byts[2:4], 16) - 0x21
                if (pointer < 0) or (pointer > 93):
                    continue
            elif typ == "GR94":
                pointer = int(byts[2:4], 16) - 0xA1
                if (pointer < 0) or (pointer > 93):
                    continue
            elif typ == "GR96":
                pointer = int(byts[2:4], 16) - 0xA0
                if pointer < 0:
                    continue
            else:
                raise ValueError("unknown type {!r}".format(typ))
        elif _i[:2] == "<U":
            # ICU-style format
            ucs, byts, direction = _i.split(" ", 2)
            assert byts[:2] == "\\x" and len(byts) == 4
            if typ == "plainext":
                pointer = int(byts[2:4], 16) - 0x80
                if pointer < 0:
                    continue
            elif typ == "GL94":
                pointer = int(byts[2:4], 16) - 0x21
                if (pointer < 0) or (pointer > 93):
                    continue
            elif typ == "GR94":
                pointer = int(byts[2:4], 16) - 0xA1
                if (pointer < 0) or (pointer > 93):
                    continue
            elif typ == "GR96":
                pointer = int(byts[2:4], 16) - 0xA0
                if pointer < 0:
                    continue
            else:
                raise ValueError("unknown type {!r}".format(typ))
            if direction.strip() == "|1":
                # i.e. best-fit mapped by the encoder only
                # Whereas, |3 means it's used only by the decoder (usually because duplicate)
                continue
        else:
            # Format of the WHATWG-supplied indices
            byts, ucs = _i.split("\t", 2)[:2]
            pointer = int(byts.strip(), 10)
        #
        assert ucs[:2] in ("0x", "U+", "<U"), ucs
        ucs = mapper(pointer, tuple(int(j, 16) for j in ucs[2:].rstrip(">").split("+")))
        #
        if len(_temp) > pointer:
            assert _temp[pointer] is None
            _temp[pointer] = ucs
        else:
            while len(_temp) < pointer:
                _temp.append(None)
            _temp.append(ucs)
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    return r







