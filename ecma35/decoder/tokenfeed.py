#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2022, 2023, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import struct, types

def _tokenise_stream(stream, state):
    state.bytewidth = 1
    state.feedback = [("DOCS", False, (0x40,))]
    state.endian = state.default_endian
    assert state.endian in "<>"
    while 1:
        yield from iter(state.feedback)
        del state.feedback[:]
        structmode = state.endian + [..., "B", "H", ..., "L"][state.bytewidth]
        code = stream.read(state.bytewidth)
        if not code:
            break
        code, = struct.unpack(structmode, code)
        yield ("WORD", code)
    # End sentinel signals truncation, so the individual filters don't need duplicate handling for
    # encountering the end of the stream as opposed to merely an unexpected token.
    yield ("ENDSTREAM",)

def process_stream(stream, *, lastfilter=None, **kwargs): # The entry point.
    # DOCS are stipulated in ISO 10646 as big-endian (>). Actually, ISO 10646 does not provide for
    # any means of embedding little-endian UTF data in ECMA-35 (i.e. our regard_bom=0). However,
    # it isn't the last word on this matter (WHATWG stipulates that unmarked UTF-16 is little-
    # endian, for example). Regarding a byte-order mark at the start of the UTF stream (i.e. our
    # regard_bom=1) seems reasonable. However, regarding the designated noncharacter U+FFFE as a
    # generic "switch byte order" control probably isn't, except on trusted data containing
    # misconcatenated UTF-16 (our regard_bom=2).
    statedict = {"osc_bel_term": True, "default_endian": ">", "regard_bom": 1, "bs_compose": True,
                 "docsmode": None}
    statedict.update(kwargs)
    state = types.SimpleNamespace(**statedict)
    from ecma35.decoder import utf8filter, utf16filter, utf32filter, formateffectors, \
       controlsets, fixedcontrols, invocations, gccsequences, elexfilter, prefixdiacritics, \
       designations, graphsets, simpleprinter, escsequences, csisequences, controlstrings, \
       rawfilter, unkdocsfilter, ecma35docsfilter, hangulfillers, utf1filter, shiftjisfilter, \
       scsufilter, uhcfilter, gbkfilter, gbhalfcodes, plainextasciifilter, bigfivefilter, \
       bssequences, ebcdicfilter, docssequences, chcpsequences, utfebcdicfilter, modeucfilter
    for f in [_tokenise_stream, docssequences.decode_docs_sequences, chcpsequences.decode_chcp,
              ecma35docsfilter.decode_ecma35docs, utf8filter.decode_utf8, 
              utf1filter.decode_utf1, shiftjisfilter.decode_shiftjis, utf32filter.decode_utf32, 
              scsufilter.decode_scsu, uhcfilter.decode_uhc, gbkfilter.decode_gbk,
              elexfilter.decode_elex, plainextasciifilter.decode_plainextascii,
              bigfivefilter.decode_bigfive, ebcdicfilter.decode_ebcdic, 
              utfebcdicfilter.decode_utfebcdic, utf16filter.decode_utf16, 
              rawfilter.decode_raw, modeucfilter.decode_modeuc, unkdocsfilter.decode_remaining_docs, 
              #
              designations.decode_designations, 
              gbhalfcodes.decode_gbhalfcodes, controlsets.decode_control_sets, 
              fixedcontrols.decode_fixed_controls, escsequences.decode_esc_sequences, 
              csisequences.decode_csi_sequences, controlstrings.decode_control_strings, 
              invocations.decode_invocations, graphsets.decode_graphical_sets, 
              formateffectors.format_effectors, prefixdiacritics.handle_prefix_diacritics,
              gccsequences.proc_gcc_sequences, hangulfillers.proc_hangul_fillers,  
              bssequences.proc_bs_sequences, lastfilter or simpleprinter.simple_print]:
        stream = f(stream, state)
    yield from stream












