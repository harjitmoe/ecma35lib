#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import struct

def tokenise_stream(stream, state):
    state.mode = "normal"
    state.bytewidth = 1
    state.firstchar = True
    # DOCS are stipulated in ISO 10646 as big-endian (>). Actually, ISO 10646 does not provide for
    # any means of embedding little-endian UTF data in ECMA-35 (i.e. our regard_bom=0). However,
    # it isn't the last word on this matter (WHATWG stipulates that unmarked UTF-16 is little-
    # endian, for example). Regarding a byte-order mark at the start of the UTF stream (i.e. our
    # regard_bom=1) seems reasonable. However, regarding the designated noncharacter U+FFFE as a
    # generic "switch byte order" control probably isn't, except on trusted data containing
    # misconcatenated UTF-16 (our regard_bom=2).
    state.endian = state.default_endian
    assert state.endian in "<>"
    if state.start_in_utf8:
        yield ("DOCS", False, tuple(b"G"))
        state.mode = "wsr"
    while 1:
        structmode = state.endian + [..., "B", "H", ..., "L"][state.bytewidth]
        code = stream.read(state.bytewidth)
        if not code:
            break
        code, = struct.unpack(structmode, code)
        if state.mode == "raw":
            state.firstchar = False
            yield ("BYTE", code)
            continue
        if state.mode in ("normal", "wsr") and code == 0x1B:
            # 0x1B is guaranteed by ECMA-35 to always be ESC and vice versa.
            r = _procesc(stream, state)
            yield r
            if state.firstchar:
                state.endian = state.default_endian
            continue
        if state.mode == "wsr" and code == 0xFFFE and (
                (state.firstchar and state.regard_bom) or (state.regard_bom > 1)):
            # Note that this part will not affect UTF-8 (which will never have a FFFE codeword).
            state.firstchar = False
            state.endian = {">": "<", "<": ">"}[state.endian] # Requires the other byte order.
            yield ("BOM", state.endian)
            continue
        if state.mode == "wsr" and code == 0xFEFF and state.firstchar and state.regard_bom:
            # Note that this will not handle the UTF-8 BOM (which is a downstream task).
            state.firstchar = False
            yield ("BOM", state.endian) # Confirms the assumed byte order.
            continue
        state.firstchar = False
        if state.mode == "wsr":
            yield ("WORD", code)
            continue
        assert code < 0x100
        if code < 0x20:
            yield ("C0", code, "CL")
        elif code < 0x80:
            yield ("GL", code - 0x20)
        elif code < 0xA0:
            yield ("C1", code - 0x80, "CR")
        else:
            yield ("GR", code - 0xA0)
    yield ("ENDSTREAM",)

def _procesc(stream, state):
    inums = []
    while 1:
        structmode = state.endian + [..., "B", "H", ..., "L"][state.bytewidth]
        code = stream.read(state.bytewidth)
        if not code:
            state.firstchar = False
            return ("ERROR", "TRUNCESC", tuple(inums))
        code, = struct.unpack(structmode, code)
        if (code < 0x20) or (code > 0x7E):
            stream.seek(-state.bytewidth, 1)
            state.firstchar = False
            return ("ERROR", "TRUNCESC", tuple(inums))
        elif code < 0x30:
            inums.append(code)
        else:
            ret = ("ESC", inums[0] if inums else None, tuple(inums[1:]), code)
            break
    # Note that it's not tokenfeed's job to parse the UTF-1/8/16/32 except to the extent needed
    # for to recognise their escape sequences (and thus when to switch back to ECMA-35).
    # Identifying (other) C0 codes, C1-via-CR codes and UCS codepoints is a downstream job.
    if ret[1] == b"%"[0]:
        # DOCS ought to be opcoded before UTF processing, which needs to happen before
        # opcoding of C0 and C1-via-CR since they're not processed from the UTFs here.
        # Since we need to respond to DOCS here anyway, may as well opcode it here.
        if ret[2] and (ret[2][0] == b"/"[0]):
            ret2 = ("DOCS", True, ret[2][1:] + (ret[3],))
        else:
            ret2 = ("DOCS", False, ret[2] + (ret[3],))
        # Deal with byte-width changes, mode changes and raw mode instigation.
        if (not ret2[1]) and (ret2[2] == (b"@"[0],)):
            # Standard return to ECMA-35 (DOCS @)
            state.mode, state.bytewidth, state.firstchar = "normal", 1, True
            return ret2
        elif not ret2[1]:
            # UTF-8 (DOCS G), UTF-1 (DOCS B), or otherwise bytewise with standard return.
            state.mode, state.bytewidth, state.firstchar = "wsr", 1, True
            return ret2
        elif (not ret[2][1:]) and (ret[3] in tuple(b"GHI")):
            # UTF-8 (DOCS / I preferred, others deprecated)
            # Afaict, ISO 10646 doesn't actually distinguish DOCS / I from DOCS G.
            state.mode, state.bytewidth, state.firstchar = "wsr", 1, True
            return ret2
        elif (not ret[2][1:]) and (ret[3] in tuple(b"@CEJKL")):
            # UTF-16 (DOCS / L preferred, others deprecated)
            # Not a WSR sequence due to different word size, but WSR once we know the size.
            state.mode, state.bytewidth, state.firstchar = "wsr", 2, True
            return ret2
        elif (not ret[2][1:]) and (ret[3] in tuple(b"ADF")):
            # UTF-32 (DOCS / F preferred, others deprecated)
            # Not a WSR sequence due to different word size, but WSR once we know the size.
            state.mode, state.bytewidth, state.firstchar = "wsr", 4, True
            return ret2
        else:
            # Either raw pass-through (DOCS / B), or as-good-as so far as we can know.
            state.mode, state.bytewidth, state.firstchar = "raw", 1, True
            return ret2
    elif (not ret[1]) and (not ret[2]) and (0x40 <= ret[3] < 0x60):
        # C1 control characters in 7-bit escape form.
        state.firstchar = False
        return ("C1", ret[3] - 0x40, "ESC")
    else:
        state.firstchar = False
        return ret










