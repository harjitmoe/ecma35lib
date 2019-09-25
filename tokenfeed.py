#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import struct

def tokenise_stream(stream, *, default_endian=">", regard_bom=1, start_in_utf8=False):
    mode = "normal"
    bytewidth = 1
    firstchar = True
    # DOCS are stipulated in ISO 10646 as big-endian (>). Actually, ISO 10646 does not provide for
    # any means of embedding little-endian UTF data in ECMA-35 (i.e. our regard_bom=0). However,
    # it isn't the last word on this matter (WHATWG stipulates that unmarked UTF-16 is little-
    # endian, for example). Regarding a byte-order mark at the start of the UTF stream (i.e. our
    # regard_bom=1) seems reasonable. However, regarding the designated noncharacter U+FFFE as a
    # generic "switch byte order" control probably isn't, except on trusted data containing
    # misconcatenated UTF-16 (our regard_bom=2).
    endian = default_endian
    assert default_endian in "<>"
    if start_in_utf8:
        yield ("DOCS", False, tuple(b"G"))
        mode = "wsr"
    while 1:
        structmode = endian + [..., "B", "H", ..., "L"][bytewidth]
        code = stream.read(bytewidth)
        if not code:
            return
        code, = struct.unpack(structmode, code)
        if mode == "raw":
            firstchar = False
            yield ("RAWBYTE", code)
            continue
        if mode in ("normal", "wsr") and code == 0x1B:
            # 0x1B is guaranteed by ECMA-35 to always be ESC and vice versa.
            r, mode, bytewidth, firstchar = _procesc(stream, mode, bytewidth, structmode)
            if firstchar:
                # Don't persist a BOM from a previous Unicode stream.
                endian = default_endian
            yield r
            continue
        if mode == "wsr" and code == 0xFFFE and ((firstchar and regard_bom) or (regard_bom > 1)):
            # Note that this part will not affect UTF-8 (which will never have a FFFE codeword).
            firstchar = False
            endian = {">": "<", "<": ">"}[endian] # Requires the other byte order.
            yield ("BOM", endian)
            continue
        if mode == "wsr" and code == 0xFEFF and firstchar and regard_bom:
            # Note that this will not handle the UTF-8 BOM (which is a downstream task).
            firstchar = False
            yield ("BOM", endian) # Confirms the assumed byte order.
            continue
        firstchar = False
        if mode == "wsr":
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

def _procesc(stream, mode, bytewidth, structmode):
    inums = []
    while 1:
        code = stream.read(bytewidth)
        if not code:
            return ("ERROR", "TRUNCESC", tuple(inums)), mode, bytewidth, False
        code, = struct.unpack(structmode, code)
        if (code < 0x20) or (code > 0x7E):
            stream.seek(-bytewidth, 1)
            return ("ERROR", "TRUNCESC", tuple(inums)), mode, bytewidth, False
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
            return ret2, "normal", 1, True
        elif not ret2[1]:
            # UTF-8 (DOCS G), UTF-1 (DOCS B), or otherwise bytewise with standard return.
            return ret2, "wsr", 1, True
        elif (not ret[2][1:]) and (ret[3] in tuple(b"GHI")):
            # UTF-8 (DOCS / I preferred, others deprecated)
            # Afaict, ISO 10646 doesn't actually distinguish DOCS / I from DOCS G.
            return ret2, "wsr", 1, True
        elif (not ret[2][1:]) and (ret[3] in tuple(b"@CEJKL")):
            # UTF-16 (DOCS / L preferred, others deprecated)
            return ret2, "wsr", 2, True
        elif (not ret[2][1:]) and (ret[3] in tuple(b"ADF")):
            # UTF-32 (DOCS / F preferred, others deprecated)
            return ret2, "wsr", 4, True
        else:
            # Either raw pass-through (DOCS / B), or as-good-as so far as we can know.
            return ret2, "raw", 1, True
    elif (not ret[1]) and (not ret[2]) and (0x40 <= ret[3] < 0x60):
        # C1 control characters in 7-bit escape form.
        return ("C1", ret[3] - 0x40, "ESC"), mode, bytewidth, False
    else:
        return ret, mode, bytewidth, False










