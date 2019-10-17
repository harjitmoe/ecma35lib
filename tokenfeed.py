#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import struct

def tokenise_stream(stream, state):
    state.mode = "normal"
    state.bytewidth = 1
    state.firstchar = True
    state.feedback = []
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
        yield from iter(state.feedback)
        del state.feedback[:]
        structmode = state.endian + [..., "B", "H", ..., "L"][state.bytewidth]
        code = stream.read(state.bytewidth)
        if not code:
            break
        code, = struct.unpack(structmode, code)
        if state.mode == "raw":
            state.firstchar = False
            yield ("BYTE", code)
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












