#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, binascii, json

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mbmaps")
cachedirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mbmapscache")
_temp = []
def identitymap(pointer, ucs):
    return ucs

applesinglehints = {
    # Bold arrows:
    (0x21e6, 0xf87a): (0x2b05,), # ⬅
    (0x21e7, 0xf87a): (0x2b06,), # ⬆
    (0x21e8, 0xf87a): (0x2b95,), # ⬇
    (0x21e9, 0xf87a): (0x2b07,), # ⬈
    # Vertical forms not present when mappings written, but later added from GB 18030:
    (0x2026, 0xf87e): (0xfe19,), # Ellipsis
    (0x3001, 0xf87e): (0xfe11,), # Comma
    (0x3002, 0xf87e): (0xfe12,), # Full stop
    (0xff3b, 0xf87e): (0xfe47,), # Opening hard bracket
    (0xff3d, 0xf87e): (0xfe48,), # Closing hard bracket
}
def ahmap(pointer, ucs):
    return applesinglehints.get(ucs, ucs)

def read_main_plane(fil, *, whatwgjis=False, eucjp=False, kps=False, plane=None, mapper=identitymap):
    if mapper is identitymap:
        mappername = ""
    elif mapper.__name__ != "<lambda>":
        mappername = "_" + mapper.__name__
    else:
        mappername = "_FIXME"
    cachefn = os.path.join(cachedirectory,
                  os.path.splitext(fil)[0] + ("_plane{:02d}".format(plane) if plane is not None
                                              else "_mainplane") + mappername + ".json")
    if os.path.exists(cachefn):
        # Cache output since otherwise several seconds are spend in here upon importing graphdata
        f = open(cachefn, "r")
        r = json.load(f)
        f.close()
        return tuple(tuple(i) if i is not None else None for i in r)
    for _i in open(os.path.join(directory, fil), "r"):
        if not _i.strip():
            continue
        elif _i[0] == "#":
            continue # is a comment.
        elif _i[0] == "<" and _i[:2] != "<U":
            continue # is ICU metadata or state machine config which isn't relevant to us.
        elif _i.strip() in ("CHARMAP", "END CHARMAP"):
            continue # ICU delimitors we don't care about.
        elif _i[:2] == "0x":
            # Consortium-style format, over GL (or GR with eucjp=1) without transformation.
            byts, ucs = _i.split("\t", 2)[:2]
            if not (eucjp or kps):
                men = 1
                ku = int(byts[2:4], 16) - 0x20
                ten = int(byts[4:6], 16) - 0x20
            else:
                men = 1
                if byts[2].upper() in "01234567": # ASCII
                    continue
                elif eucjp and byts[2:4].upper() == "8E": # Half-width Katakana (via SS2)
                    continue
                elif eucjp and byts[2:4].upper() == "8F":
                    if len(byts) == 4: # i.e. SS3 itself rather than an SS3 sequence
                        continue
                    byts = byts[2:]
                    men = 2
                elif byts[2].upper() in ("8", "9"): # Remaining CR C1 controls
                    continue
                elif not ucs.strip(): # i.e. code not used
                    continue
                elif len(byts) == 4:
                    continue
                ku = int(byts[2:4], 16) - 0xA0
                ten = int(byts[4:6], 16) - 0xA0
                if kps and ((ku < 1) or (ku > 94) or (ten < 1) or (ten > 94)):
                    continue
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
        elif _i[:2] == "<U":
            # ICU-style format, over GL (or EUC-TW) without transformation
            ucs, byts, direction = _i.split(" ", 2)
            assert byts[:2] == "\\x"
            byts = [int(i, 16) for i in byts[2:].split("\\x")]
            if direction.strip() == "|1":
                # i.e. best-fit mapped by the encoder only
                # Whereas, |3 means it's used only by the decoder (usually because duplicate)
                continue
            if len(byts) == 4:
                assert byts[0] == 0x8E
                men = byts[1] - 0xA0
                ku = byts[2] - 0xA0
                ten = byts[3] - 0xA0
            elif len(byts) == 3:
                if 0x80 < byts[0] < 0xA0: # cns-11643-1992.ucm does this for some reason.
                    men = byts[0] - 0x80
                else:
                    men = byts[0] - 0x20
                ku = byts[1] - 0x20
                ten = byts[2] - 0x20
            elif len(byts) == 2:
                men = 1
                if byts[0] >= 0xA0:
                    ku = byts[0] - 0xA0
                    ten = byts[1] - 0xA0
                else:
                    ku = byts[0] - 0x20
                    ten = byts[1] - 0x20
            else:
                assert len(byts) == 1
                continue
            #
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
        elif "-" in _i[:3]: # Maximum possible plane number is 94, so this will remain correct
            # Format of the Taiwanese government supplied CNS 11643 mapping data
            cod, ucs = _i.split("\t", 2)[:2]
            men, byts = cod.split("-")
            men = int(men, 10)
            assert len(byts) == 4
            ku = int(byts[:2], 16) - 0x20
            ten = int(byts[2:], 16) - 0x20
        elif whatwgjis:
            # Format of the WHATWG-supplied indices for Windows-31J and JIS X 0212.
            # Needs an argument since we can't otherwise tell it from the next one.
            byts, ucs = _i.split("\t", 2)[:2]
            pointer = int(byts.strip(), 10)
            men = 1
            ku = (pointer // 94) + 1
            ten = (pointer % 94) + 1
            if ku > 94:
                continue
        else:
            # Format of the WHATWG-supplied indices for UHC and GBK.
            byts, ucs = _i.split("\t", 2)[:2]
            extpointer = int(byts.strip(), 10)
            men = 1
            ku = (extpointer // 190) - 31
            ten = (extpointer % 190) - 95
            if not ((1 <= ku <= 94) and (1 <= ten <= 94)):
                continue
        pointer = ((men - 1) * 94 * 94) + ((ku - 1) * 94) + (ten - 1)
        #
        if ucs[:2] in ("0x", "U+", "<U"):
            ucs = ucs[2:]
        ucs = mapper(pointer, tuple(int(j, 16) for j in ucs.rstrip(">").split("+")))
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
    # Write output cache.
    f = open(cachefn, "w")
    f.write(json.dumps(r))
    f.close()
    return r







