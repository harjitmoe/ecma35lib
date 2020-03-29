#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from ecma35.data import graphdata

def _tonumber(s):
    if (len(s) != 2) or (s[0] != "G") or (s[1] not in "01234"):
        return -1
    return ord(s[1]) - ord("0")

def proc_irrset(myset, irrid):
    # This is used both here and in controlsets
    if not isinstance(myset, tuple):
        return myset if not irrid else None
    elif not irrid:
        return myset[0]
    else:
        if irrid == (0x3F,): # i.e. only do this if it's the ONLY byte after the ESC
            # It is private really, but we use it for the faithful original reg, i.e. the first
            # item in the registered versions tuple. ECMA-35 doesn't provide a standard way of
            # doing this (IRRs start at IRR 0x40 for the first registered *update*), but using
            # IRR 0x3F for this (0x3F being private-use, and one less than 0x40) is (a) permitted
            # and (b) sensible.
            private = False
        elif 0x30 <= irrid[-1] <= 0x3F:
            # Used for the unregistered versions tuple. Technically, we're abusing the mechanism
            # with this, since all IRR sets are supposed to be upwardly compatible, and much of
            # what we're doing here plainly is not, but never mind.
            private = True
        else:
            # Used for the rest of the registered versions tuple.
            assert 0x40 <= irrid[-1] <= 0x7E
            private = False
        start = 0 # it's a tuple index here, and they start from zero.
        # First number for N bytes after ESC is one more than the largest number
        # representable with N-1 bytes after ESC.
        # Akin to as if "00" meant 10 so "99" meant 109 so "000" meant 110, etc…
        for i in range(len(irrid)): # i.e. includes 0 but not len(irrid) itself
            if i == 0:
                noatlevel = 0 # There are no IRRs with no trail byte
            elif i == 1:
                if private:
                    noatlevel = 15 # i.e. 16, but excluding IRR 0x3F
                else:
                    noatlevel = 64 # i.e. 63, but with the addition of IRR 0x3F
            else:
                if private:
                    # Sixteen possible I bytes, sixteen possible F bytes
                    noatlevel = 16 ** i
                else:
                    # Sixteen possible I bytes, sixty-three possible F bytes
                    noatlevel = 63 * (16 ** (i - 1))
            start += noatlevel
        if private:
            index = start + (irrid[-1] - 0x30)
            hs = myset[1]
        else:
            index = start + (irrid[-1] - 0x40) + 1
            hs = myset[2]
        if index < len(hs):
            return hs[index]
        else:
            return None

def decode_graphical_sets(stream, state):
    pending = []
    pset = -1
    invrange = None
    reconsume = None
    state.ghwots = [None, None, None, None]
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        tno = _tonumber(token[0])
        # The cur_gsets state prop might not yet be defined if e.g. DOCS % @ hasn't happened yet.
        tgset = state.cur_gsets[tno] if hasattr(state, "cur_gsets") else "Unknown"
        if (tno >= 0) and (pset in (-1, tno)) and (invrange in (token[2], None)) and (
                    graphdata.gsets[tgset][0] == 96 or 1 <= token[1] <= 94):
            if pset == -1:
                pset = tno
                invrange = token[2]
            # NOT else (falls through from first "then" clause)
            size = graphdata.gsets[tgset][1]
            pending.append(token[1])
            assert len(pending) <= size
            if len(pending) == size:
                pointer = 0
                if graphdata.gsets[tgset][0] == 94:
                    for byt in pending:
                        assert 1 <= byt <= 94
                        pointer *= 94
                        pointer += byt - 1
                else:
                    assert graphdata.gsets[tgset][0] == 96
                    for byt in pending:
                        assert 0 <= byt <= 95
                        pointer *= 96
                        pointer += byt
                array = graphdata.gsets[tgset][2]
                ucs = array[pointer] if pointer < len(array) else None
                if ucs is None:
                    if tgset != "Unknown":
                        yield ("ERROR", "UNDEFGRAPH", tgset, tuple(pending), pset, invrange)
                    else:
                        yield ("CHAR?", state.ghwots[tno], tuple(pending), token[0], invrange)
                elif isinstance(ucs, tuple):
                    for iucs in ucs:
                        yield ("CHAR", iucs, tgset, tuple(pending), token[0], invrange)
                else:
                    yield ("CHAR", ucs, tgset, tuple(pending), token[0], invrange)
                pset = -1
                invrange = None
                del pending[:]
        elif pending:
            yield ("ERROR", "TRUNCMB", tgset, tuple(pending), pset, invrange)
            del pending[:]
            pset = -1
            invrange = None
            reconsume = token
        elif (tno >= 0) and (graphdata.gsets[tgset][0] == 94) and token[1] in (0, 95):
            # Should only get here if using 0xA0 or 0xFF when a 94 or 94^n set is in GR.
            assert token[2] in ("GR", "SSGR"), token
            yield ("ERROR", "OUTSIDE94", token[0], token[1], token[2], tgset)
        elif token[0] == "UCS":
            yield ("CHAR", token[1], "UCS", (token[1],), token[2], token[3])
        elif token[0] == "DESIG":
            sump = graphdata.sumps[token[2]]
            try:
                mygset = sump[token[3]]
            except KeyError:
                yield token
                state.cur_gsets[token[1]] = "Unknown"
                state.ghwots[token[1]] = token[2], token[3]
            else:
                sbankpage = "sbank2gpage" + "".join(chr(iii) for iii in token[3])
                if (not token[5]) and token[4] and (token[2] == "94n") and (
                                      state.docsmode == "shift_jis") and (
                                      sbankpage in graphdata.gsets):
                    # ESC / SI format emoji. Totally not ECMA-35 conformant, hence it's only being
                    # done in Shift_JIS mode, and only for the legacy "multibyte" escapes (none of
                    # the F-bytes used are grandfathered, so standard usage shouldn't strictly be 
                    # using that exact escape syntax anyway).
                    state.cur_gsets[4] = sbankpage
                    state.glset = 4
                    continue
                mygseti = proc_irrset(mygset, token[5])
                if mygseti is not None:
                    state.cur_gsets[token[1]] = mygseti
                else:
                    yield ("ERROR", "UNRECIRR", mygset, token[5])
                    state.cur_gsets[token[1]] = mygset[0] if isinstance(mygset, tuple) else mygset
                yield ("RDESIG", "G{}".format(token[1]), sump[token[3]],
                       token[2], token[3], token[4], token[5])
        else:
            yield token














