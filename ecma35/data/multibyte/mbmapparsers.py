#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020/2021/2023/2024.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os, binascii, json, urllib.parse, shutil, itertools, dbm.dumb, collections.abc, re
from ecma35.data import gccdata
from ecma35.data.names import namedata

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mbmaps")
cachedirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mbmapscache.d")
cachedbmfn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mbmapscache")

def identitymap(pointer, ucs):
    return ucs

if (os.environ.get("ECMA35LIBDECACHE", "") == "1") and os.path.exists(cachedirectory):
    shutil.rmtree(cachedirectory)
    os.unlink(cachedbmfn + ".dir")
    os.unlink(cachedbmfn + ".dat")
    os.unlink(cachedbmfn + ".bak")

os.makedirs(cachedirectory, exist_ok=True)
try:
    cachedbm = dbm.dumb.open(cachedbmfn, "c")
except EnvironmentError:
    cachedbm = {}

def return_to_list(f):
    def inner(*args, **kwargs):
        return list(f(*args, **kwargs))
    return inner

def return_to_tuple(f):
    def inner(*args, **kwargs):
        return tuple(f(*args, **kwargs))
    return inner

def with_caching(f):
    def inner(*args, **kwargs):
        filtargs = [i for i in args if not isinstance(i, collections.abc.Generator)]
        filtkwargs = {}
        for key in kwargs:
            if hasattr(kwargs[key], "__call__"):
                filtkwargs[key] = kwargs[key].__name__
            else:
                filtkwargs[key] = kwargs[key]
        token = json.dumps([f.__name__, filtargs, filtkwargs])
        if token in cachedbm:
            return LazyJSON(token, isfilecache=False)
        ret = f(*args, **kwargs)
        try:
            cachedbm[token] = json.dumps(ret)
        except EnvironmentError:
            pass
        return ret
    return inner

class LazyJSON(list):
    def __init__(self, filename, iscache=True, isfilecache=True):
        if iscache and not isfilecache:
            assert filename[0] != "/"
            self._key = filename
            self._filename = None
        elif iscache and isfilecache:
            self._filename = os.path.join(cachedirectory, filename)
            self._key = None
        else:
            self._filename = os.path.join(directory, filename)
            self._key = None
    def _load(self):
        if not super().__len__():
            if self._filename:
                f = open(self._filename)
                super().extend(tuple(i) if isinstance(i, list) else i for i in json.load(f))
                f.close()
            else:
                super().extend(tuple(i) if isinstance(i, list) else i
                    for i in json.loads(cachedbm[self._key]))
    def __iter__(self):
        self._load()
        return super().__iter__()
    def __len__(self):
        self._load()
        return super().__len__()
    def __hash__(self):
        self._load()
        return hash(tuple(self))
    def __eq__(self, i):
        self._load()
        return tuple(self) == tuple(i)
    def __bool__(self, i):
        self._load()
        return super().__bool__()
    def __add__(self, i):
        self._load()
        return tuple(self) + i
    def __radd__(self, i):
        self._load()
        return i + tuple(self)
    def __iadd__(self, i):
        return NotImplemented
    def __getitem__(self, i):
        self._load()
        if not isinstance(i, slice):
            return super().__getitem__(i)
        else:
            return tuple(super().__getitem__(i))
    def __setitem__(self, i, j):
        raise TypeError("immutable")
    def __delitem__(self, i):
        raise TypeError("immutable")
    def append(self, i):
        raise TypeError("immutable")
    def extend(self, i):
        raise TypeError("immutable")
    def insert(self, n, i):
        raise TypeError("immutable")
    def pop(self, n=None):
        raise TypeError("immutable")

@return_to_tuple
def parse_ucs_codepoints(string):
    for point in string.lstrip("<U+").rstrip(">").split(
            None if " " in string.strip()
            else "><" if "><" in string
            else "," if "," in string
            else "+"):
        yield int(point.lstrip("0xU+") or "0", 16)

@return_to_list
def readhexbytes(byt):
    if "\\x" in byt:
        for i in byt.lstrip("x\\").split("\\x"):
            yield int(i, 16)
    else:
        if byt[:2] == "0x":
            byt = byt[2:]
        while byt:
            yield int(byt[:2], 16)
            byt = byt[2:]

def parse_file_format(fil, *, twoway=False, prefer_sjis=False, skipstring=None, altcomments=False, 
                      libcongress=False, hangulsourcestxt=None, cidmap=None, gb12052=False, moz2004=False):
    cidmapnames = None
    for _i in open(os.path.join(directory, fil), "r", encoding="utf-8"):
        if not _i.strip():
            continue
        elif (skipstring is not None) and (skipstring in _i):
            continue
        elif _i[0] == "#":
            continue # is a comment.
        elif moz2004:
            if _i[0] in "Hi=":
                continue
            _ilist = _i.split()
            byts, ucs = _ilist[0], _ilist[-1]
            yield readhexbytes(byts), parse_ucs_codepoints(ucs)
        elif hangulsourcestxt is not None:
            ucs, johab, wansung, ksx1002, kps, gbko = _i.split("#", 1)[0].strip().split(";")
            if hangulsourcestxt == "wansung":
                if not wansung:
                    continue
                yield readhexbytes(wansung.lstrip("*")), parse_ucs_codepoints(ucs)
            elif hangulsourcestxt == "1002":
                if not ksx1002:
                    continue
                yield readhexbytes(ksx1002), parse_ucs_codepoints(ucs)
            elif hangulsourcestxt == "kps":
                if not kps:
                    continue
                yield readhexbytes(kps.lstrip("*")), parse_ucs_codepoints(ucs)
            elif hangulsourcestxt == "gbko":
                if not gbko:
                    continue
                yield readhexbytes(gbko), parse_ucs_codepoints(ucs)
            else:
                raise ValueError("unrecognised hangulsourcestxt arg: {!r}".format(hangulsourcestxt))
        elif cidmap:
            frm, to = cidmap
            if not cidmapnames:
                cidmapnames = _i.rstrip().split("\t")
                continue
            values = _i.rstrip().split("\t")
            if values[cidmapnames.index(frm)] == "*" or values[cidmapnames.index(to)] == "*":
                continue
            froms = values[cidmapnames.index(frm)].split(",")
            tos = values[cidmapnames.index(to)].split(",")
            while len(tos) < len(froms):
                tos.append(tos[0])
            while len(tos) > len(froms):
                if "v" not in tos[0]:
                    toscp = int(tos[0], 16)
                    if (0x2E80 <= toscp < 0x2FE0) or toscp in (0x2003, 0x2329, 0x232A):
                        tos = tos[1:]
                tos = tos[:len(froms)]
            for (frmv, tov) in zip(froms, tos):
                if "v" in frmv:
                    continue
                elif cidmapnames.index(to) > 0:
                    yield readhexbytes(frmv), parse_ucs_codepoints(tov.replace("v", "+F87E"))
                else:
                    yield readhexbytes(frmv), int(tov, 10)
        elif gb12052:
            kuten, bit7, euc, ucs = _i.split(None, 3)
            ucs = ucs.split("#", 1)[0].strip()
            if "Hunminjeongeum Haerye style" in _i:
                ucs += " U+F87F"
            yield readhexbytes(euc), parse_ucs_codepoints(ucs)
        elif libcongress:
            # CSV of (1) 3-byte GL, (2) UCS or PUA, (3) nothing or geta mark, (4) rubbish
            byts, ucs, rubbish = _i.split(",", 2)
            yield readhexbytes(byts), parse_ucs_codepoints(ucs)
        elif _i[0] == "<" and _i[:2] != "<U":
            continue # is ICU metadata or state machine config which isn't relevant to us.
        elif _i.strip() in ("CHARMAP", "END CHARMAP"):
            continue # ICU delimitors we don't care about.
        elif _i[:2] == "0x":
            # Consortium-style format
            if "\t" not in _i and " " in _i.strip():
                _i = _i.strip().replace(" ", "\t")
            if _i.split("#", 1)[0].replace("+0x", "+").count("0x") == 3: # Note: not U+ (because Mozilla HKSCS)
                # Consortium-style format for JIS X 0208 (just skip the other column)
                if not prefer_sjis:
                    _i = _i.split("\t", 1)[1]
                else:
                    _i = "\t".join(_i.split("\t", 2)[1::2])
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
            if not ucs.strip():
                continue
            if byts.startswith("0x") and len(byts) == 7:
                # Format of UTC mappings of CNS 11643
                yield itertools.chain([int(byts[2], 16)], readhexbytes(byts[3:])), parse_ucs_codepoints(ucs)
            else:
                yield readhexbytes(byts), parse_ucs_codepoints(ucs)
        elif _i[:2] == "<U":
            # ICU-style format
            ucs, byts, direction = _i.split(" ", 2)
            if (direction.strip() == "|1") or (direction.strip() == "|2") or (twoway and (direction.strip() == "|3")):
                # |0 means a encoder/decoder two-way mapping
                # |1 appears to mean an encoder-only mapping, e.g. fallback ("best fit"), graphical mapping for control codes, compatibility with what other vendors decode something to, etc
                # |2 appears to mean a substitute mapping, e.g. to the SUB control.
                # |3 appears to mean a decoder-only mapping (disfavoured duplicate)
                continue
            assert byts[:2] == "\\x"
            yield readhexbytes(byts), parse_ucs_codepoints(ucs)
        elif "-" in _i[:3]: # Maximum possible plane number is 95, so this will remain correct
            # Format of the Taiwanese government supplied CNS 11643 mapping data
            cod, ucs = _i.split("\t", 2)[:2]
            men, byts = cod.split("-")
            men = int(men, 10)
            yield itertools.chain([men], readhexbytes(byts)), parse_ucs_codepoints(ucs)
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
                yield itertools.chain([men], readhexbytes(byts)), parse_ucs_codepoints(ucs)
        elif _i == "\x1a":
            # EOF on an older (MS-DOS) text file
            continue
        else:
            # Format of the WHATWG-supplied indices
            byts, ucs = _i.split("\t", 2)[:2]
            pointer = int(byts.strip(), 10)
            yield pointer, parse_ucs_codepoints(ucs)

_uplus_regex = re.compile(r"\bU[+][0-9A-Fa-f]+\b")
def read_babelstone_update_file(fil):
    def reader():
        for _i in open(os.path.join(directory, fil), "r", encoding="utf-8-sig"):
            if not _i.strip():
                continue
            frm, to = _uplus_regex.findall(_i)
            yield (parse_ucs_codepoints(frm), parse_ucs_codepoints(to))
    data = None
    def puatostandardmap(pointer, ucs):
        nonlocal data
        data = data or dict(reader())
        return data.get(ucs, ucs)
    return puatostandardmap

def parse_sjt11239_mapping_file(fil, *,
        include_variation_selectors=True,
        include_uncertain_mappings=False,
        fallback_preferencer=None,
        fallback_nothing_selector=None):
    for _i in open(os.path.join(directory, fil), "r", encoding="utf-8-sig"):
        if _i.startswith("#") or not _i.strip():
            continue
        columns = _i.rstrip().split("\t", 6)
        ucs, vs, preview, kuten, radstridx, ids, uncertain = columns + [""] * (7 - len(columns))
        ku, ten = tuple(int(j, 10) for j in kuten.split("-", 1))
        pointer = ((ku - 1) * 94) + (ten - 1)
        if uncertain.endswith("?") and include_uncertain_mappings:
            ucs, vs = uncertain.split(None, 1)[0].split("+", 1)
        ucs = int(ucs, 16) if ucs else None
        ids = ids.lstrip("^").rstrip("$")
        is_pua = ucs and (0xE000 <= ucs < 0xF900 or ucs >= 0xF0000)
        if (not ucs) or (ids and "-" not in ids and "?" not in ids and "(" not in ids and is_pua and fallback_preferencer and fallback_preferencer((ucs,))):
            if fallback_nothing_selector and fallback_nothing_selector((ucs,)):
                continue
            yield pointer, tuple(ord(i) for i in ids)
        elif is_pua and fallback_nothing_selector and fallback_nothing_selector((ucs,)):
            continue
        else:
            ucsvs = (ucs,)
            if vs and include_variation_selectors:
                vsno = int(vs.lstrip("VS"), 10)
                if vsno <= 16:
                    ucsvs = (ucs, 0xFE00 + (vsno - 1))
                else:
                    ucsvs = (ucs, 0xE0100 + (vsno - 17))
            yield pointer, ucsvs

def _sjis_xkt_to_mkt(ku, ten):
    if ku <= 94:
        men = 1
    elif ku <= 103:
        men = 2
        ku = (1, 8, 3, 4, 5, 12, 13, 14, 15)[ku - 95]
    else:
        men = 2
        ku = ku + 78 - 104
    return men, ku, ten

def _parse_sjis(byts):
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
    return _sjis_xkt_to_mkt(ku, ten)

def _parse_whatwg_jispointer(pointer):
    ku = (pointer // 94) + 1
    ten = (pointer % 94) + 1
    return _sjis_xkt_to_mkt(ku, ten)

def _fill_to_plane_boundary(planelist, SZ):
    planelist.extend([None] * (((SZ * SZ) - (len(planelist) % (SZ * SZ))) % (SZ * SZ)))
    if not planelist:
        planelist.extend([None] * (SZ * SZ))

def _put_at(planelist, pointer, iucs, ignore_later_altucs):
    if len(planelist) > pointer:
        if ignore_later_altucs and planelist[pointer] is not None:
            return
        assert planelist[pointer] is None, (pointer, planelist[pointer], iucs)
        planelist[pointer] = iucs
    else:
        planelist.extend([None] * (pointer - len(planelist)))
        planelist.append(iucs)

def _limits(set96):
    return (1, 94, 94) if not set96 else (0, 95, 96)

def _main_plane_pointer(men, ku, ten, plane_wanted, set96):
    ST, ED, SZ = _limits(set96)
    if plane_wanted is not None: # i.e. if we want a particular plane's two-byte mapping.
        if men != plane_wanted:
            return None
        else:
            men = 1
    assert (ST <= ten <= ED) and (ku >= ST), (men, ku, ten)
    pointer = ((men - ST) * SZ * SZ) + ((ku - ST) * SZ) + (ten - ST)
    assert pointer >= 0, (men, ku, ten, plane_wanted, ST, ED, SZ, set96)
    return pointer

@with_caching
def decode_main_plane_euc(parsed_stream, filenamekey, *, eucjp=False, gbklike=False, plane=None, 
                          mapper=identitymap, ignore_later_altucs=False, set96=False):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    ST, ED, SZ = _limits(set96)
    _temp = []
    for coded, ucs in parsed_stream:
        if len(coded) == 4:
            # EUC-TW four-byte codes
            assert coded[0] == 0x8E
            assert not eucjp
            men = coded[1] - 0xA0
            ku = coded[2] - 0xA0
            ten = coded[3] - 0xA0
        else:
            men = 1
            if coded[0] < 0x80: # ASCII
                continue
            elif eucjp and coded[0] == 0x8E: # Half-width Katakana (via SS2)
                continue
            elif eucjp and coded[0] == 0x8F:
                if len(coded) == 1: # i.e. SS3 itself rather than an SS3 sequence
                    continue
                coded = coded[1:]
                men = 2
            elif 0x80 <= coded[0] < 0xA0: # Remaining CR C1 controls
                continue
            elif len(coded) == 1:
                continue
            ku = coded[0] - 0xA0
            ten = coded[1] - 0xA0
            if gbklike and ((ku < ST) or (ku > ED) or (ten < ST) or (ten > ED)):
                continue # Not in the main plane
        pointer = _main_plane_pointer(men, ku, ten, plane, set96)
        if pointer == None:
            continue
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, ignore_later_altucs)
    _fill_to_plane_boundary(_temp, SZ)
    return tuple(_temp)

@with_caching
def decode_main_plane_gl(parsed_stream, filenamekey, *, plane=None, mapper=identitymap,
                         ignore_later_altucs=False, set96=False, skip_invalid_kuten=True):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    ST, ED, SZ = _limits(set96)
    _temp = []
    for coded, ucs in parsed_stream:
        coded = list(coded)
        if len(coded) == 2:
            # 7-bit two-byte codes
            men = 1
            ku = coded[0] - 0x20
            ten = coded[1] - 0x20
        elif len(coded) == 3 and coded[0] < 0x1B:
            # Like the Consortium supplied CNS 11643 mappings
            men = coded[0]
            ku = coded[1] - 0x20
            ten = coded[2] - 0x20
        elif len(coded) == 3 and 0x80 < coded[0] < 0xA0:
            # cns-11643-1992.ucm does this for some reason.
            men = coded[0] - 0x80
            ku = coded[1] - 0x20
            ten = coded[2] - 0x20
        else:
            # 7-bit three-byte codes
            assert len(coded) == 3
            men = coded[0] - 0x20
            ku = coded[1] - 0x20
            ten = coded[2] - 0x20
        if skip_invalid_kuten and (not (ST <= ku <= ED) or not (ST <= ten <= ED)):
            continue
        pointer = _main_plane_pointer(men, ku, ten, plane, set96)
        if pointer == None:
            continue
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, ignore_later_altucs)
    _fill_to_plane_boundary(_temp, SZ)
    return tuple(_temp)

@with_caching
def decode_main_plane_sjis(parsed_stream, filenamekey, *, plane=None, mapper=identitymap,
                           ignore_later_altucs=False):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    _temp = []
    for coded, ucs in parsed_stream:
        if len(coded) == 2:
            men, ku, ten = _parse_sjis(coded)
        else:
            continue
        pointer = _main_plane_pointer(men, ku, ten, plane, False)
        if pointer == None:
            continue
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, ignore_later_altucs)
    _fill_to_plane_boundary(_temp, 94)
    return tuple(_temp)

@with_caching
def decode_extra_plane_elex(parsed_stream, filenamekey, *, mapper=identitymap, ignore_later_altucs=False):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    _temp = []
    for coded, ucs in parsed_stream:
        if len(coded) != 2:
            continue
        lead, trail = coded
        if trail >= 0xA1:
            continue
        first = lead - 0xA1
        if trail >= 0x81:
            last = trail - 0x41 - 3
        else:
            last = trail - 0x41
        pointer = (94 * first) + last
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, ignore_later_altucs)
    _fill_to_plane_boundary(_temp, 94)
    return tuple(_temp)

big5_to_cns_maps = {}

@with_caching
def decode_main_plane_big5(parsed_stream, filenamekey, map_key, *, plane=None, mapper=identitymap):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    _temp = []
    for coded, ucs in parsed_stream:
        if isinstance(coded, int):
            # WHATWG format
            first, last = coded // 157, coded % 157
            lead = first + 0x81
            trail = (last - 63 + 0xA1) if last >= 63 else (last + 0x40)
        elif len(coded) != 1:
            assert len(coded) == 2
            lead, trail = coded
        else:
            continue
        #
        key = (lead << 8) | trail
        if key not in big5_to_cns_maps[map_key]:
            continue
        men, ku, ten = big5_to_cns_maps[map_key][key]
        pointer = _main_plane_pointer(men, ku, ten, plane, False)
        if pointer == None:
            continue
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, ignore_later_altucs=True)
    _fill_to_plane_boundary(_temp, 94)
    return tuple(_temp)

# Origin is at 0x8140. Trail bytes are 0x40-0x7E (63) and 0xA1-0xFE (94) fairly seamlessly.
hkscs_start = 942
special_start = 5024
kanji1_start = 5495
corporate1_start = 10896
kanji2_start = 11304
corporate2_start = 18956

@with_caching
def decode_extra_plane_big5(parsed_stream, filenamekey, *, mapper=identitymap):
    """This is for the extension regions within the normal trail byte range."""
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    _temp = []
    for coded, ucs in parsed_stream:
        if isinstance(coded, int):
            extpointer = coded
        elif len(coded) >= 2:
            assert len(coded) == 2
            if 0x7F <= coded[1] <= 0xA0:
                # IBM-950 includes expanded trail byte range similarly to Big5+ but with
                #   PUA assignments. They cannot currently be processed by this system.
                continue
            first = coded[0] - 0x81
            last = (coded[1] - 0xA1 + 63) if coded[1] >= 0xA1 else (coded[1] - 0x40)
            extpointer = (157 * first) + last
        else:
            continue
        #
        if extpointer >= corporate2_start:
            newextpointer = extpointer
            # Subtract a whole number of rows, but "empty" space at the start is fine.
            newextpointer -= ((corporate2_start - kanji2_start) // 157) * 157
            newextpointer -= ((corporate1_start - special_start) // 157) * 157
        elif extpointer >= kanji2_start:
            continue
        elif extpointer >= corporate1_start:
            newextpointer = extpointer
            newextpointer -= ((corporate1_start - special_start) // 157) * 157
        elif extpointer >= special_start:
            continue
        else:
            newextpointer = extpointer
        pseudoku = (newextpointer // 157) + 1
        pseudoten = (newextpointer % 157) + 1
        if pseudoten <= 63:
            ku = (pseudoku * 2) - 1
            ten = (pseudoten - 63) + 94
        else:
            ku = pseudoku * 2
            ten = pseudoten - 63
        newpointer = ((ku - 1) * 94) + (ten - 1)
        iucs = mapper(newpointer, ucs)
        _put_at(_temp, newpointer, iucs, ignore_later_altucs=False)
    _fill_to_plane_boundary(_temp, 94)
    return tuple(_temp)

@with_caching
def decode_second_extra_plane_big5(parsed_stream, filenamekey, *, mapper=identitymap):
    """This is for the extension regions outside the normal trail byte range (that is,
    much of Big5+, as well as areas 5 and 9 of IBM-950."""
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    _temp = []
    for coded, ucs in parsed_stream:
        if isinstance(coded, int):
            extpointer = coded
        elif len(coded) >= 2:
            assert len(coded) == 2
            if not (0x80 <= coded[1] <= 0xA0): # Big5+ uses 0x80 although IBM-950 does not.
                continue
            first = coded[0] - 0x81
            last = coded[1] - 0x80
            pointer = (47 * first) + last # 47, not 33, so the rows line up nicely.
        else:
            continue
        #
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, ignore_later_altucs=False)
    _fill_to_plane_boundary(_temp, 94)
    return tuple(_temp)

@with_caching
def decode_main_plane_whatwg(parsed_stream, filenamekey, *, gbklike=False, plane=None, 
                             mapper=identitymap, ignore_later_altucs=False, set96=False):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    ST, ED, SZ = (1, 94, 94) if not set96 else (0, 95, 96)
    _temp = []
    for coded, ucs in parsed_stream:
        if gbklike:
            # Like WHATWG-supplied indices for UHC and GBK.
            men = 1
            ku = (coded // 190) - 31
            ten = (coded % 190) - 95
            if not ((ST <= ku <= ED) and (ST <= ten <= ED)):
                continue
        else:
            # Like WHATWG-supplied indices for Windows-31J and JIS X 0212.
            men, ku, ten = _parse_whatwg_jispointer(coded)
        pointer = _main_plane_pointer(men, ku, ten, plane, set96)
        if pointer == None:
            continue
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, ignore_later_altucs)
    _fill_to_plane_boundary(_temp, SZ)
    return tuple(_temp)

@with_caching
def decode_gbk_non_uro_extras(parsed_stream, filenamekey):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    #
    # Read GBK/5 and the non-URO part of GBK/4 to an array. Since this part of the
    # mapping cannot be generated automatically from the GB 2312 mapping.
    _temp = []
    for coded, ucs in parsed_stream:
        if not isinstance(coded, int):
            byts = list(coded)
            if len(byts) == 1:
                continue
            assert len(byts) == 2
            pseudoku = byts[0] - 0x81
            pseudoten = byts[1] - 0x40
            if byts[1] >= 0x7F:
                assert byts[1] != 0x7F
                pseudoten -= 1
        else:
            pseudoku = (coded // 190)
            pseudoten = (coded % 190)
        if pseudoku <= 0x1F or ((pseudoku == 0x7C) and (pseudoten <= 90)) or (0x29 <= pseudoku < 0x7C):
            continue
        elif pseudoten > 95:
            continue
        pseudoku2 = pseudoku - 0x1F
        _put_at(_temp, (pseudoku2 * 96) + pseudoten, ucs, False)
    _fill_to_plane_boundary(_temp, 96)
    return tuple(_temp)

@with_caching
def decode_main_plane_dbebcdic(parsed_stream, filenamekey, *, mapper=identitymap):
    # The filenamekey argument is absolutely needed for the @with_caching since the parsed_stream
    #   is not incorporated into the memo key for obvious reasons—it is otherwise unused.
    # It does not have to be a filename, but must be unique for every different parse_file_format invocation
    #   even for the same filename.
    _temp = []
    for coded, ucs in parsed_stream:
        if len(coded) != 2:
            continue
        pointer = ((coded[0] - 0x41) * 190) + (coded[1] - 0x41)
        if pointer == None:
            continue
        iucs = mapper(pointer, ucs)
        _put_at(_temp, pointer, iucs, False)
    _fill_to_plane_boundary(_temp, 190)
    return tuple(_temp)

@with_caching
def read_unihan_planes(fil, wantkey, wantsource=None, set96=False, kutenform=False, *, mapper=identitymap):
    #wantkey = "kIRG_" + region + "Source"
    ST, ED, SZ = (1, 94, 94) if not set96 else (0, 95, 96)
    f = open(os.path.join(directory, fil), "r")
    if wantsource:
        wantsource += "-"
    _temp = []
    for i in f:
        if i[0] == "#":
            continue
        elif not i.strip():
            continue
        ucs, prop, data = i.strip().split("\t", 2)
        if (prop != wantkey) or (wantsource and not data.startswith(wantsource)):
            continue
        assert ucs[:2] == "U+"
        ucs = int(ucs[2:], 16)
        if (ucs == 0x4EBE) and (wantkey == "kCCCII"):
            # CCCII 0x2D305B is mapped to both U+4EBE 亾 (also EACC 0x2D305B) and
            #   U+5166 兦 (which matches cccii.ucm, which uses CCCII 0x33305B for U+4EBE).
            # Both are apparently y-variants of U+4EA1 (亡, CCCII 0x21305B)
            # Kludge to get this to work.
            continue
        if wantsource:
            data = data[len(wantsource):]
        if kutenform:
            assert len(data) == 4
            men = 1
            ku = int(data[:2], 10)
            ten = int(data[2:], 10)
        elif len(data) == 6:
            men = int(data[:2], 16) - 0x20
            ku = int(data[2:4], 16) - 0x20
            ten = int(data[4:], 16) - 0x20
        else:
            assert len(data) == 4
            men = 1
            ku = int(data[:2], 16) - 0x20
            ten = int(data[2:], 16) - 0x20
        if (not 0 <= ten <= 95) and (ucs == 0x9C0C):
            # U+9C0C → kCCCII 2358CF (not 94^n or even 7-bit)
            # U+9C0C → kEACC 2D6222
            # Being as non-94^3 codes in other CCCII mapping sources are mostly either 
            #   (a) Non-kanji using 0x20 as a lead or continuation byte, or
            #   (b) Extra URO or CJKA kanji encoded using prefixed 0x7F to escape a UCS-2BE code,
            # I suspect this is an error in Unihan?
            continue
        pointer = _main_plane_pointer(men, ku, ten, None, set96)
        _put_at(_temp, pointer, mapper(pointer, (ucs,)), False)
    _fill_to_plane_boundary(_temp, SZ)
    return tuple(_temp)

def fuse(arrays, filename):
    if not os.path.exists(os.path.join(cachedirectory, filename)):
        out = []
        for n in range(max(*tuple(len(i) for i in arrays))):
            for array in arrays:
                if n < len(array) and (array[n] is not None):
                    if array[n] == (-1,):
                        # Allow an earlier listed array to override later ones in undefining a
                        #   code point (e.g. when forming the mapping for 1998 KPS).
                        # U+0001 (usually SOH) is not a combining mark so this special case is fine
                        out.append(None)
                    else:
                        out.append(array[n])
                    break
            else: # for...else, i.e. if the loop finishes without encountering break
                out.append(None)
        _f = open(os.path.join(cachedirectory, filename), "w")
        _f.write(json.dumps(out))
        _f.close()
        return tuple(out)
    else:
        return LazyJSON(filename)

def without_compat(array, filename):
    if not os.path.exists(os.path.join(cachedirectory, filename)):
        out = []
        for n, i in enumerate(array):
            if (not i) or len(i) != 1 or chr(i[0]) not in namedata.compat_decomp:
                out.append(i)
            else:
                out.append(tuple(ord(j) for j in namedata.compat_decomp[chr(i[0])][1]))
        _f = open(os.path.join(cachedirectory, filename), "w")
        _f.write(json.dumps(out))
        _f.close()
        return tuple(out)
    else:
        return LazyJSON(filename)

def without_ideocompat(array, filename):
    if not os.path.exists(os.path.join(cachedirectory, filename)):
        out = []
        for n, i in enumerate(array):
            if (not i) or len(i) != 1 or not (namedata._is_cjkci(chr(i[0])) or (0x2E80 <= i[0] < 0x2FE0)) or chr(i[0]) not in namedata.compat_decomp:
                out.append(i)
            else:
                out.append(tuple(ord(j) for j in namedata.compat_decomp[chr(i[0])][1]))
        _f = open(os.path.join(cachedirectory, filename), "w")
        _f.write(json.dumps(out))
        _f.close()
        return tuple(out)
    else:
        return LazyJSON(filename)

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

def read_untracked(shippedfn, fn, reader, *args, **kwargs):
    if os.path.exists(os.path.join(directory, fn)):
        data = reader(*args, **kwargs)
        if not os.path.exists(os.path.join(directory, shippedfn)):
            try:
                _f = open(os.path.join(directory, shippedfn), "w")
                _f.write(json.dumps(data))
                _f.close()
            except EnvironmentError:
                pass
    else:
        data = LazyJSON(shippedfn, iscache=False)
    return data

def to_96(dat):
    """Convert a 94^n set array to a 96^n set array.
    Note that this function will not prepend an empty plane."""
    first = 0
    outwrite = 0
    out = [None] + ([None] * int(len(dat) * (96/94)**2))
    while first < len(dat):
        if not (first % (94 * 94)):
            outwrite += 96 # Extra row at start of plane
        out[outwrite+1:outwrite+95] = dat[first:first+94]
        first += 94
        outwrite += 96
        if not (first % (94 * 94)):
            outwrite += 96 # Extra row at end of plane
    return tuple(out[:outwrite])

def to_94(dat):
    """Convert a 96^n set array to a 94^n set array. Of course, can be lossy.
    Note that this function will not strip an initial plane."""
    first = 0
    outwrite = 0
    out = [None] * len(dat)
    while first < len(dat):
        if not (outwrite % (94 * 94)):
            first += 96 # Extra row at start of plane
        out[outwrite:outwrite+94] = dat[first+1:first+95]
        outwrite += 94
        first += 96
        if not (outwrite % (94 * 94)):
            first += 96 # Extra row at end of plane
    return tuple(out[:outwrite])




