#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.decoder.videotex import read_checkdata

etsdocs = ("DOCS", False, (0x31,))

g0sets = ["ir047", # British
          "ir021", # German
          "ir011", # Swedish
          "ir015ets", # Italian
          "etsfrench",
          "etsiberian",
          "etsczechoslovak",
          None,
          #
          "etspolish",
          "ir021", # German
          "ir011", # Swedish
          "ir015ets", # Italian
          "etsfrench",
          None,
          "etsczechoslovak",
          None,
          #
          "ir047", # British
          "ir021", # German
          "ir011", # Swedish
          "ir015ets", # Italian
          "etsfrench",
          "etsiberian",
          "etsturkish",
          None,
          #
          None,
          None,
          None,
          None,
          None,,
          "etsgajica",
          None,
          "etsromanian",
          #
          "etsserbian", # TODO
          "ir021", # German
          "etsestonian",
          "etsbaltic",
          "etsfrench",
          "etsrussian", # TODO
          "etsukrainian", # TODO
          None,
          #
          None,
          None,
          None,
          None,
          None,,
          None,
          "etsturkish",
          "etsgreek",
          #
          "ir047", # British
          None,
          None,
          None,
          "etsfrench",
          None,
          None,
          "etsarabic", # TODO
          #
          ]

def decode_ets(stream, state):
    ets_packet = []
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if (token[0] == "DOCS"):
            if ets_packet:
                yield ("ERROR", "ETSTRUNC", tuple(ets_packet))
                del ets_packet[:]
            if token == utf8docs:
                yield ("RDOCS", "ETS-300-706", token[1], token[2])
                state.bytewidth = 1
                state.docsmode = "ets"
                state.cur_c0 = "ir001" # FIXME
                state.cur_c1 = "RFC1345" # FIXME
                state.glset = 0
                state.grset = 1
                state.cur_gsets = ["ir006", "nil", "nil", "nil"] # FIXME
                state.is_96 = [0, 0, 0, 0]
                state.magazine_active_pages = {}
            else:
                yield token
        elif state.docsmode == "ets":
            if token[0] != "WORD":
                # ESC passing through
                yield token
                continue
            elif not ets_packet:
                if token[1] == 0x55:
                    ets_packet.append(token)
                else:
                    yield token
            elif len(ets_packet) == 1:
                if token[1] == 0x55:
                    ets_packet.append(token)
                else:
                    yield ("ERROR", "ETS_TRUNC_SYNC")
                    yield ets_packet[0]
                    del ets_packet[:]
                    reconsume = token
            elif len(ets_packet) == 2:
                if token[1] == 0x27:
                    ets_packet.append(token)
                else:
                    yield ("ERROR", "NOT_ETS_MAGIC", token)
                    yield ets_packet[0]
                    yield ets_packet[1]
                    del ets_packet[:]
                    reconsume = token
            elif len(ets_packet) < 44:
                ets_packet.append(token)
            else:
                ets_packet.append(token)
                number_low, lowerror = read_checkdata.read_eighttofour(ets_packet[3])
                number_high, higherror = read_checkdata.read_eighttofour(ets_packet[4])
                if lowerror or higherror:
                    yield ("ERROR", "ETS_CORRUPT_PACKET", ets_packet)
                    del ets_packet[:]
                    continue
                number = (number_high << 4) | number_low
                magazine_number = number & 0x8
                packet_number = number >> 3
                if packet_number == 0: # Header packet
                    # TODO do what with error values?
                    page_number, e = read_checkdata.read_eighttofour(ets_packet[6]) << 4
                    page_number |= read_checkdata.read_eighttofour(ets_packet[5])[0]
                    state.magazine_active_pages[magazine_number] = page_number
                    read_checkdata.read_eighttofour(ets_packet[6])
                    subcode_low = read_checkdata.read_eighttofour(ets_packet[8])[0] << 4
                    subcode_low |= read_checkdata.read_eighttofour(ets_packet[7])[0]
                    subcode_high = read_checkdata.read_eighttofour(ets_packet[10])[0] << 4
                    subcode_high |= read_checkdata.read_eighttofour(ets_packet[9])[0]
                    wipe_flag = not not (subcode_low & 0x80)
                    is_newsflash = not not (subcode_high & 0x40)
                    is_subtitles = not not (subcode_high & 0x80)
                    subcode = (subcode_low & 0x7F) | ((subcode_high & 0x3F) << 7)
                    byte_12, e = read_checkdata.read_eighttofour(ets_packet[11])
                    heading_hidden = not not (byte_12 & 0x1)
                    is_update = not not (byte_12 & 0x2)
                    out_of_order = not not (byte_12 & 0x4)
                    body_hidden = not not (byte_12 & 0x8)
                    byte_13, e = read_checkdata.read_eighttofour(ets_packet[12])
                    is_serial = not not (byte_13 & 0x1)
                    if not is_serial:
                        raise NotImplementedError("parallel mode teletext not implemented")
                    charset_narrow = ((byte_13 & 0x2) << 1) | ((byte_13 & 0x4) >> 1) |\
                                     ((byte_13 & 0x8) >> 3)
                    charset_wide = charset_narrow # For now
                    state.cur_gsets[0] = g0sets[charset_wide] or "nil" # For now
                    if wipe_flag:
                        yield ("WIPEPAGE", magazine_number, page_number)
                    yield ("NEWPAGE", magazine_number, page_number, subcode, (wipe_flag, is_newsflash, is_subtitles, heading_hidden, is_update, out_of_order, body_hidden, is_serial))
                    for rawtextbyte in ets_packet[13:]:
                        textbyte, e = read_checkdata.read_eighttoseven(rawtextbyte)
                        if textbyte < 0x20:
                            yield ("C0", textbyte)
                        else:
                            yield ("GL", textbyte - 0x20)
                raise NotImplementedError
                #
            #
        else: # i.e. isn't a DOCS, nor an ETS part of the stream
            yield token
        #
    #
#