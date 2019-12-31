#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

scsudocs = ("DOCS", True, (0x30,))

def _get_offset(window):
    if window < 0:
        return ((~window) * 0x80) + 0x10000 # Reverse the one's complement applied in decode_scsu.
    elif 0x01 <= window <= 0x67:
        return window * 0x80
    elif 0x68 <= window <= 0xA7:
        return (window * 0x80) + 0xAC00
    elif window >= 0xF9:
        return {0xF9: 0xC0, 0xFA: 0x250, 0xFB: 0x370, 0xFC: 0x530, 0xFD: 0x3040, 
                0xFE: 0x30A0, 0xFF: 0xFF60}[window]
    else:
        return None

_staticoffset = [0x00, 0x80, 0x100, 0x300, 0x2000, 0x2080, 0x2100, 0x3000]

def decode_scsu(stream, state):
    pending = None
    for token in stream:
        if (token[0] == "DOCS"):
            if token == scsudocs:
                state.bytewidth = 1
                state.docsmode = "scsu-1byte"
                state.cur_dynwindows = [0x1, 0xF9, 0x8, 0xC, 0x12, 0xFD, 0xFE, 0xA6]
                state.cur_windex = 0
            else:
                yield token
        elif state.docsmode == "scsu-1byte" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if pending is None:
                if token[1] in (0x0, 0x9, 0xA, 0xD):
                    yield ("UCS", token[1], "SCSU", "SCSU-ASCII")
                elif token[1] < 0x9: # SQn
                    pending = ("SQ", token[1] - 1)
                elif token[1] == 0xB: # SDX
                    pending = ("SDX", None)
                elif token[1] == 0xC: # reserved
                    yield ("ERROR", "SCSUONEBYTEUNDEFCTRL", token[1])
                elif token[1] == 0xE: # SQU
                    pending = ("SQU", None)
                elif token[1] == 0xF: # SCU
                    yield ("SCSUSHIFT", -1)
                    # Can't use 2, since there are 1-byte controls mixed in.
                    state.bytewidth = 1
                    state.docsmode = "scsu-2byte"
                elif token[1] < 0x18: # SCn
                    yield ("SCSUSHIFT", token[1] - 16)
                    state.cur_windex = token[1] - 16
                elif token[1] < 0x20: # SDn
                    pending = ("SD", token[1] - 24)
                elif 0x20 <= token[1] < 0x80:
                    yield ("UCS", token[1], "SCSU", "SCSU-ASCII")
                else:
                    window = state.cur_dynwindows[state.cur_windex]
                    offset = _get_offset(window)
                    if offset is None:
                        yield ("ERROR", "SCSUINVALIDWINDOW", (window, token[1] - 0x80))
                    else:
                        yield ("UCS", token[1] - 0x80 + offset, "SCSU", "SCSU-LDW")
            elif pending[0] == "SQ":
                window = state.cur_dynwindows[pending[1]]
                offset = _get_offset(window)
                if token[1] >= 0x80 and offset is not None:
                    yield ("UCS", token[1] - 0x80 + offset, "SCSU", "SCSU-SDW")
                elif token[1] < 0x80:
                    offset = _staticoffset[pending[1]]
                    yield ("UCS", token[1] + offset, "SCSU", "SCSU-SW")
                else:
                    yield ("ERROR", "SCSUINVALIDWINDOW", (pending[1], token[1] - 0x80))
                pending = None
            elif pending[0] == "SQU":
                if pending[1] is None:
                    pending = (pending[0], token[1])
                else:
                    word = (pending[1] << 8) | token[1]
                    if word < 0xD800 or word >= 0xE000:
                        yield ("UCS", word, "SCSU", "SCSU-SUCS")
                    else:
                        # No surrogates in SQU.
                        yield ("ERROR", "SCSUSQUSURROGATE", word)
                        yield ("UCS", word, "SCSU", "WTF-SCSU-SUCS")
                    pending = None
            elif pending[0] == "SD":
                yield ("SCSUDESIG", pending[1], token[1])
                state.cur_dynwindows[pending[1]] = token[1]
                state.cur_windex = pending[1]
                pending = None
            elif pending[0] == "SDX":
                if pending[1] is None:
                    pending = (pending[0], token[1])
                else:
                    windex = pending[1] >> 5
                    window = ((pending[1] & 0x1F) << 8) | token[1]
                    # One's complement it to distinguish it from the positive ones, even zero.
                    yield ("SCSUDESIG", windex, ~window)
                    state.cur_dynwindows[windex] = ~window
                    state.cur_windex = windex
                    pending = None
            else:
                raise AssertionError(pending)
        elif state.docsmode == "scsu-2byte" and token[0] == "WORD":
            assert (token[1] < 0x100), token
            if pending is None:
                if token[1] <= 0xDF or token[1] >= 0xF3:
                    # i.e. start of a directly encoded UTF-16 representation
                    pending = ("UTF-16", token[1])
                elif 0xE0 <= token[1] < 0xE8: # UCn
                    yield ("SCSUSHIFT", token[1] - 0xE0)
                    state.cur_windex = token[1] - 0xE0
                    state.bytewidth = 1
                    state.docsmode = "scsu-1byte"
                elif 0xE8 <= token[1] < 0xF0: # UDn
                    pending = ("UD", token[1] - 0xE8)
                elif token[1] == 0xF0: # UQU
                    pending = ("UQU", None)
                elif token[1] == 0xF1: # UDX
                    pending = ("UDX", None)
                else:
                    yield ("ERROR", "SCSUTWOBYTEUNDEFCTRL", token[1])
            elif pending[0] == "UTF-16":
                word = (pending[1] << 8) | token[1]
                if word < 0xD800 or word >= 0xE000:
                    yield ("UCS", word, "SCSU", "SCSU-DUCS")
                else:
                    # Pass through to UTF-16 filter.
                    yield ("PAIR", word, "SCSU", "SCSU-DUCS")
                pending = None
            elif pending[0] == "UQU":
                if pending[1] is None:
                    pending = (pending[0], token[1])
                else:
                    word = (pending[1] << 8) | token[1]
                    if 0xD800 <= word < 0xE000:
                        yield ("ERROR", "SCSUUQUSURROGATE", word)
                        yield ("UCS", word, "SCSU", "WTF-SCSU-DUCS")
                    elif 0xE000 <= word < 0xF300:
                        yield ("UCS", word, "SCSU", "SCSU-DUCS")
                    else:
                        yield ("ERROR", "SCSUREDUNDANTUQU", word)
                        yield ("UCS", word, "SCSU", "SCSU-DUCS")
                    pending = None
            elif pending[0] == "UD":
                yield ("SCSUDESIG", pending[1], token[1])
                state.cur_dynwindows[pending[1]] = token[1]
                state.cur_windex = pending[1]
                state.bytewidth = 1
                state.docsmode = "scsu-1byte"
                pending = None
            elif pending[0] == "UDX":
                if pending[1] is None:
                    pending = (pending[0], token[1])
                else:
                    windex = pending[1] >> 5
                    window = ((pending[1] & 0x1F) << 8) | token[1]
                    # One's complement it to distinguish it from the positive ones, even zero.
                    yield ("SCSUDESIG", windex, ~window)
                    state.cur_dynwindows[windex] = ~window
                    state.cur_windex = windex
                    pending = None
            else:
                raise AssertionError(pending)
        else:
            yield token
        #
    #
#








