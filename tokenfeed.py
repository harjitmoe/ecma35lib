#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import struct

def tokenise_stream(stream, state):
    state.hasesc = 0x1B
    state.bytewidth = 1
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
        if (state.hasesc >= 0) and (code == state.hasesc):
            # state.hasesc is set by the DOCS filter (for instance, in ECMA-35 itself and in all
            # DOCS syntaces without a forwardslash, it's 0x1B). It may be set to -1 if there isn't
            # an ESC (say, in transparent raw mode).
            yield ("C0", code, "CL")
        else:
            yield ("WORD", code)
    yield ("ENDSTREAM",)












