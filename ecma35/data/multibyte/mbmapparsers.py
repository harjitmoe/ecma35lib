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

def read_main_plane(fil, *, eucjp=False, euckrlike=False, twoway=False,
                    plane=None, mapper=identitymap):
    """
    Read a mapping from a file in the directory given by mbmapparsers.directory.
    Only positional argument is the name (including subdirectory) of that file.

    Keyword arguments are as follows:

    - eucjp: (if the file is in UTC format) interpret as EUC format, with planes
      01 and 02 invoked with GR and SS3-over-GR respectively. If neither this nor
      euckrlike is passed, it is interpreted as one plane over GL.
    - euckrlike: interpret as an EUC format with non-EUC extensions; read only
      the main plane. Consulted for UTC and WHATWG formats, else currently ignored.
    - twoway: (if the file is in ICU format) ignore one-way decoder mappings.
      This is ignored for the other supported formats, since they do not annotate
      whether or not a given mapping is also used by the encoder.
    - plane: isolate only one plane of a multi-plane mapping (e.g. CNS 11643).
    """
    if mapper is identitymap:
        mappername = ""
    elif mapper.__name__ != "<lambda>":
        mappername = "_" + mapper.__name__
    else:
        mappername = "_FIXME"
    cachebfn = os.path.splitext(fil)[0].replace("/", "---") + ("_plane{:02d}".format(plane)
               if plane is not None else "_mainplane") + mappername + ".json"
    cachefn = os.path.join(cachedirectory, cachebfn)
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
            if not (eucjp or euckrlike):
                if len(byts) == 6:
                    men = 1
                    ku = int(byts[2:4], 16) - 0x20
                    ten = int(byts[4:6], 16) - 0x20
                else:
                    # Like the Consortium supplied CNS 11643 mappings
                    assert len(byts) == 7
                    men = int(byts[2], 16)
                    ku = int(byts[3:5], 16) - 0x20
                    ten = int(byts[5:7], 16) - 0x20
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
                if euckrlike and ((ku < 1) or (ku > 94) or (ten < 1) or (ten > 94)):
                    continue
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
            mkts = ((men, ku, ten),)
        elif _i[:2] == "<U":
            # ICU-style format, over GL (or EUC-TW) without transformation
            ucs, byts, direction = _i.split(" ", 2)
            assert byts[:2] == "\\x"
            byts = [int(i, 16) for i in byts[2:].split("\\x")]
            if (direction.strip() == "|1") or (twoway and (direction.strip() == "|3")):
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
            mkts = ((men, ku, ten),)
        elif "-" in _i[:3]: # Maximum possible plane number is 94, so this will remain correct
            # Format of the Taiwanese government supplied CNS 11643 mapping data
            cod, ucs = _i.split("\t", 2)[:2]
            men, byts = cod.split("-")
            men = int(men, 10)
            assert len(byts) == 4
            ku = int(byts[:2], 16) - 0x20
            ten = int(byts[2:], 16) - 0x20
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
            mkts = ((men, ku, ten),)
        elif ("\t" in _i) and ("-" in _i.split("\t", 1)[1][:3]):
            # Format of Koichi Yasuoka's CNS 11643 mapping data
            while _i.count("\t") < 4:
                _i += "\t" # the U+5E94 line is missing its tab-tab-tab-hash-CJK at the end.
            ucs, cod1, cod2, cod3 = _i.split("\t", 4)[:4]
            mkts = ()
            for cod in (cod1, cod2, cod3):
                if not cod.strip():
                    continue
                men, byts = cod.rstrip().split("-")
                men = int(men, 10)
                assert len(byts) == 4, repr(byts)
                ku = int(byts[:2], 16) - 0x20
                ten = int(byts[2:], 16) - 0x20
                if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                    if men != plane:
                        continue
                    else:
                        men = 1
                mkts += ((men, ku, ten),)
        elif not euckrlike:
            # Format of the WHATWG-supplied indices for Windows-31J and JIS X 0212.
            byts, ucs = _i.split("\t", 2)[:2]
            pointer = int(byts.strip(), 10)
            men = 1
            ku = (pointer // 94) + 1
            ten = (pointer % 94) + 1
            mkts = ((men, ku, ten),)
            if ku > 94:
                continue
        else:
            # Format of the WHATWG-supplied indices for UHC and GBK.
            byts, ucs = _i.split("\t", 2)[:2]
            extpointer = int(byts.strip(), 10)
            men = 1
            ku = (extpointer // 190) - 31
            ten = (extpointer % 190) - 95
            mkts = ((men, ku, ten),)
            if not ((1 <= ku <= 94) and (1 <= ten <= 94)):
                continue
        if ucs[:2] in ("0x", "U+", "<U"):
            ucs = ucs[2:]
        for men, ku, ten in mkts:
            pointer = ((men - 1) * 94 * 94) + ((ku - 1) * 94) + (ten - 1)
            iucs = mapper(pointer, tuple(int(j, 16) for j in ucs.rstrip(">").split("+")))
            if len(_temp) > pointer:
                assert _temp[pointer] is None
                _temp[pointer] = iucs
            else:
                while len(_temp) < pointer:
                    _temp.append(None)
                _temp.append(iucs)
    # Try to end it on a natural plane boundary.
    _temp.extend([None] * (((94 * 94) - (len(_temp) % (94 * 94))) % (94 * 94)))
    if not _temp:
        _temp.extend([None] * (94 * 94)) # Don't just return an empty tuple.
    r = tuple(_temp) # Making a tuple makes a copy, of course.
    del _temp[:]
    # Write output cache.
    f = open(cachefn, "w")
    f.write(json.dumps(r))
    f.close()
    return r







