#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, binascii, json, urllib.parse, shutil
from ecma35.data import gccdata

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mbmaps")
cachedirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mbmapscache")
_temp = []
def identitymap(pointer, ucs):
    return ucs

if (os.environ.get("ECMA35LIBDECACHE", "") == "1") and os.path.exists(cachedirectory):
    shutil.rmtree(cachedirectory)
    os.makedirs(cachedirectory)

def _grok_sjis(byts):
    if not isinstance(byts, int):
        pku = byts[0]
        if pku > 0xA0:
            pku -= 0x40
        pku -= 0x81
        pten = byts[1]
        if pten > 0x7F:
            pten -= 1
        pten -= 0x40
        if pten >= 94:
            ku = (pku * 2) + 2
            ten = pten - 93
        else:
            ku = (pku * 2) + 1
            ten = pten + 1
    else: # i.e. it's a pointer from a WHATWG file (still needs this, to process the SJIS trailer)
        ku = (byts // 94) + 1
        ten = (byts % 94) + 1
    #
    if ku <= 94:
        men = 1
    elif ku <= 103:
        men = 2
        ku = (1, 8, 3, 4, 5, 12, 13, 14, 15)[ku - 95]
    else:
        men = 2
        ku = ku + 78 - 104
    return men, ku, ten

def read_main_plane(fil, *, eucjp=False, euckrlike=False, twoway=False, sjis=False,
                    skipstring=None, plane=None, altcomments=False, mapper=identitymap):
    """
    Read a mapping from a file in the directory given by mbmapparsers.directory.
    Only positional argument is the name (including subdirectory) of that file.

    Keyword arguments are as follows:

    - eucjp: interpret as EUC format, with planes 01 and 02 invoked with GR and
      SS3-over-GR respectively. (If neither this nor euckrlike is passed, UTC
      format is interpreted as one plane over GL, and ICU format is interpreted
      as the format used for ICU's CNS 11643 mappings.)
    - euckrlike: interpret as an EUC format with non-EUC extensions; read only
      the main plane.
    - altcomments: prefer mappings in "# or" comments over nominal.
    - sjis: interpret (a UTC or ICU format mapping) as Shift_JIS encoded.
    - skipstring: particular substring denoting a line must be skipped.
    - twoway: (if the file is in ICU format) ignore one-way decoder mappings.
      This is ignored for the other supported formats, since they do not
      annotate which mappings are also used by the encoder.
    - plane: isolate only one plane of a multi-plane mapping (e.g. CNS 11643).
    """
    if mapper is identitymap:
        mappername = ""
    elif mapper.__name__ != "<lambda>":
        mappername = "_" + mapper.__name__
    else:
        mappername = "_FIXME"
    #
    if altcomments:
        mappername += "_altcomments"
    #
    if skipstring:
        mappername += "_skip" + urllib.parse.quote(skipstring)
    if twoway:
        mappername += "_twoway"
    cachebfn = os.path.splitext(fil)[0].replace("/", "---") + ("_plane{:02d}".format(plane)
               if plane is not None else "_mainplane") + mappername + ".json"
    cachefn = os.path.join(cachedirectory, cachebfn)
    if os.path.exists(cachefn):
        # Cache output since otherwise several seconds are spend in here upon importing graphdata
        f = open(cachefn, "r")
        r = json.load(f)
        f.close()
        return tuple(tuple(i) if i is not None else None for i in r)
    for _i in open(os.path.join(directory, fil), "r", encoding="utf-8"):
        if not _i.strip():
            continue
        elif (skipstring is not None) and (skipstring in _i):
            continue
        elif _i[0] == "#":
            continue # is a comment.
        elif _i[0] == "<" and _i[:2] != "<U":
            continue # is ICU metadata or state machine config which isn't relevant to us.
        elif _i.strip() in ("CHARMAP", "END CHARMAP"):
            continue # ICU delimitors we don't care about.
        elif _i[:2] == "0x":
            # Consortium-style format, over GL (or GR with eucjp=1) without transformation.
            if _i.split("#", 1)[0].replace("+0x", "+").count("0x") == 3:
                # Consortium-style format for JIS X 0208 (just skip the SJIS column)
                if not sjis:
                    _i = _i.split("\t", 1)[1]
                else:
                    _i = "\t".join(_i.split("\t", 2)[1::2])
            assert "\t" in _i, _i
            if altcomments and ("# or for Unicode 4.0," in _i):
                byts, ucs = _i.split("# or for Unicode 4.0,", 1)
                byts = byts.split("\t", 1)[0]
                ucs = ucs.lstrip().split(None, 1)[0].rstrip(",")
            elif altcomments and ("# or" in _i):
                byts, ucs = _i.split("# or", 1)
                byts = byts.split("\t", 1)[0]
                ucs = ucs.lstrip().split(None, 1)[0].rstrip(",")
            else:
                byts, ucs = _i.split("\t", 2)[:2]
            #
            if sjis:
                if len(byts) == 6:
                    men, ku, ten = _grok_sjis([int(byts[2:4], 16), int(byts[4:], 16)])
                else:
                    continue
            elif not (eucjp or euckrlike):
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
            # ICU-style format, over GL or as EUC
            ucs, byts, direction = _i.split(" ", 2)
            assert byts[:2] == "\\x"
            byts = [int(i, 16) for i in byts[2:].split("\\x")]
            if (direction.strip() == "|1") or (twoway and (direction.strip() == "|3")):
                # |0 means a encoder/decoder two-way mapping
                # |1 appears to mean an encoder-only mapping, e.g. fallback ("best fit")
                # |3 appears to mean a decoder-only mapping (disfavoured duplicate)
                continue
            if len(byts) == 4:
                assert byts[0] == 0x8E
                assert not eucjp
                men = byts[1] - 0xA0
                ku = byts[2] - 0xA0
                ten = byts[3] - 0xA0
            elif len(byts) == 3:
                if eucjp:
                    if byts[0] == 0x8F: # SS3
                        men = 2
                    else:
                        continue
                else:
                    if 0x80 < byts[0] < 0xA0: # cns-11643-1992.ucm does this for some reason.
                        men = byts[0] - 0x80
                    else:
                        men = byts[0] - 0x20
                #
                if eucjp:
                    ku = byts[1] - 0xA0
                    ten = byts[2] - 0xA0
                    assert sjis or 1 <= ku <= 94, (_i, byts[1], byts[2])
                    assert sjis or 1 <= ten <= 94, (_i, byts[1], byts[2])
                else:
                    ku = byts[1] - 0x20
                    ten = byts[2] - 0x20
            elif len(byts) == 2:
                if sjis:
                    men, ku, ten = _grok_sjis(byts)
                else:
                    men = 1
                    if byts[0] >= 0xA0:
                        ku = byts[0] - 0xA0
                        ten = byts[1] - 0xA0
                    elif eucjp and byts[0] == 0x8E: # SS2
                        continue
                    else:
                        ku = byts[0] - 0x20
                        ten = byts[1] - 0x20
                    assert sjis or 1 <= ten <= 94, (_i, byts[0], byts[1])
                    if euckrlike and ((ku < 1) or (ku > 94) or (ten < 1) or (ten > 94)):
                        continue
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
            men, ku, ten = _grok_sjis(pointer)
            if men != 1 and not sjis:
                continue
            if plane is not None: # i.e. if we want a particular plane's two-byte mapping.
                if men != plane:
                    continue
                else:
                    men = 1
            mkts = ((men, ku, ten),)
            if ku > 94:
                continue
        elif _i == "\x1a":
            # EOF on an older (MS-DOS) text file
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
            assert (1 <= ten <= 94) and (ku >= 1), (men, ku, ten)
            pointer = ((men - 1) * 94 * 94) + ((ku - 1) * 94) + (ten - 1)
            iucs = mapper(pointer, tuple(int(j, 16) for j in ucs.rstrip(">").split("+")))
            if len(_temp) > pointer:
                assert _temp[pointer] is None, (men, ku, ten, pointer, _temp[pointer], iucs)
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

def read_unihan_source(fil, region, source):
    cachebfn = os.path.splitext(fil)[0].replace("/", "---") + ("_{}_{}".format(region, source)
               ) + ".json"
    cachefn = os.path.join(cachedirectory, cachebfn)
    if os.path.exists(cachefn):
        f = open(cachefn, "r")
        r = json.load(f)
        f.close()
        return tuple(tuple(i) if i is not None else None for i in r)
    wantkey = "kIRG_" + region + "Source"
    wantsource = source + "-"
    f = open(os.path.join(directory, fil), "r")
    for i in f:
        if i[0] == "#":
            continue
        elif not i.strip():
            continue
        ucs, prop, data = i.strip().split("\t", 2)
        if (prop != wantkey) or (not data.startswith(wantsource)):
            continue
        assert ucs[:2] == "U+"
        ucs = int(ucs[2:], 16)
        dat = data[len(wantsource):]
        assert (len(dat) == 4)
        ku = int(dat[:2], 16) - 0x20
        ten = int(dat[2:], 16) - 0x20
        pointer = ((ku - 1) * 94) + (ten - 1)
        if len(_temp) > pointer:
            assert _temp[pointer] is None, (i, ku, ten, pointer, _temp[pointer], (ucs,))
            _temp[pointer] = (ucs,)
        else:
            while len(_temp) < pointer:
                _temp.append(None)
            _temp.append((ucs,))
    # Try to end it on a natural plane boundary.
    _temp.extend([None] * (((94 * 94) - (len(_temp) % (94 * 94))) % (94 * 94)))
    if not _temp:
        _temp.extend([None] * (94 * 94)) # Don't just return an empty tuple.
    ret = tuple(_temp)
    del _temp[:]
    # Write output cache.
    f = open(cachefn, "w")
    f.write(json.dumps(ret))
    f.close()
    return ret

def read_unihan_kuten(fil, wantkey):
    cachebfn = os.path.splitext(fil)[0].replace("/", "---") + ("_{}".format(wantkey)) + ".json"
    cachefn = os.path.join(cachedirectory, cachebfn)
    if os.path.exists(cachefn):
        f = open(cachefn, "r")
        r = json.load(f)
        f.close()
        return tuple(tuple(i) if i is not None else None for i in r)
    f = open(os.path.join(directory, fil), "r")
    for i in f:
        if i[0] == "#":
            continue
        elif not i.strip():
            continue
        ucs, prop, data = i.strip().split("\t", 2)
        if prop != wantkey:
            continue
        assert ucs[:2] == "U+"
        ucs = int(ucs[2:], 16)
        assert (len(data) == 4), i
        ku = int(data[:2], 10)
        ten = int(data[2:], 10)
        pointer = ((ku - 1) * 94) + (ten - 1)
        if len(_temp) > pointer:
            assert _temp[pointer] is None, (i, ku, ten, pointer, _temp[pointer], (ucs,))
            _temp[pointer] = (ucs,)
        else:
            while len(_temp) < pointer:
                _temp.append(None)
            _temp.append((ucs,))
    # Try to end it on a natural plane boundary.
    _temp.extend([None] * (((94 * 94) - (len(_temp) % (94 * 94))) % (94 * 94)))
    if not _temp:
        _temp.extend([None] * (94 * 94)) # Don't just return an empty tuple.
    ret = tuple(_temp)
    del _temp[:]
    # Write output cache.
    f = open(cachefn, "w")
    f.write(json.dumps(ret))
    f.close()
    return ret

def fuse(arrays, filename):
    if not os.path.exists(os.path.join(cachedirectory, filename)):
        out = []
        for n in range(max(*tuple(len(i) for i in arrays))):
            for array in arrays:
                if n < len(array) and (array[n] is not None):
                    out.append(array[n])
                    break
            else: # for...else, i.e. if the loop finishes without encountering break
                out.append(None)
        _f = open(os.path.join(cachedirectory, filename), "w")
        _f.write(json.dumps(out))
        _f.close()
        return tuple(out)
    else:
        _f = open(os.path.join(cachedirectory, filename), "r")
        out = tuple(tuple(i) if i is not None else None for i in json.load(_f))
        _f.close()
        return out

def parse_variants(fil):
    f = open(os.path.join(directory, fil), "r")
    cods = {}
    for i in f:
        if i[0] == "#" or not i.strip():
            continue
        unic, key, vals = i.strip().split("\t")
        vals = vals.split()
        if key == "kTraditionalVariant":
            for val in vals:
                val = val.split("<", 1)[0]
                cods.setdefault((int(unic[2:], 16),), [[], []])[0].append((int(val[2:], 16),))
        elif key == "kSimplifiedVariant":
            for val in vals:
                val = val.split("<", 1)[0]
                cods.setdefault((int(unic[2:], 16),), [[], []])[1].append((int(val[2:], 16),))
    f.close()
    return cods

def read_untracked_mbfile(reader, fn, cachefn, shippedfn, **kwargs):
    if os.path.exists(os.path.join(directory, fn)):
        data = reader(fn, **kwargs)
        try:
            if os.path.exists(os.path.join(directory, shippedfn)):
                os.unlink(os.path.join(directory, shippedfn))
            shutil.copy(os.path.join(cachedirectory, cachefn),
                        os.path.join(directory, shippedfn))
        except EnvironmentError:
            pass
    else:
        data = tuple(tuple(i) if i is not None else None for i in json.load(
                     open(os.path.join(directory, shippedfn), "r")))
    return data




