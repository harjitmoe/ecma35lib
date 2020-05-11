#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Handles GB 18030 half-codes, completing support (the first part being decoder.gbkfilter)

from ecma35.data import graphdata
from ecma35.data.multibyte import guobiao

def decode_gbhalfcodes(stream, state):
    halfcode_lead = None
    reconsume = None
    while 1:
        try:
            token = (next(stream) if reconsume is None else reconsume)
        except StopIteration:
            break
        reconsume = None
        if (token[0] == "GBHALFCODE"):
            if halfcode_lead is None:
                halfcode_lead = token
            else:
                index = (halfcode_lead[1] * 1260) + token[1]
                if index > 189000:
                    ucs = (index - 189000) + 0x10000
                    if ucs <= 0x10FFFF:
                        yield ("UCS", ucs, "GBK", "GB18030-Astral")
                    else:
                        # i.e. put the non-UCS codes from after the astral code range
                        # after the non-UCS codes from between the BMP and astral ranges
                        para_ucs = index + (189000 - len(guobiao.non_gbk_bmp))
                        yield ("ERROR", "GB18030BEYOND", para_ucs)
                else:
                    if (index == 7457) and ("GBK:ALT_4BYTE_CODES" in graphdata.gsetflags[state.cur_gsets[1]]):
                        # No longer follows the logical pattern due to changes in 2005.
                        # This only affects this one code (plus the corresponding one in the
                        # main plane), making it anomalously out of order.
                        # Don't do this for ir058-full, since it prefers duplicate over PUA maps.
                        yield ("UCS", 0xE7C7, "GBK", "GB18030-BMP")
                    elif index < len(guobiao.non_gbk_bmp):
                        yield ("UCS", guobiao.non_gbk_bmp[index], "GBK", "GB18030-BMP")
                    else:
                        para_ucs = index - len(guobiao.non_gbk_bmp) + 0x10FFFF
                        yield ("ERROR", "GB18030BEYOND", para_ucs)
                halfcode_lead = None
        elif halfcode_lead is not None:
            yield ("ERROR", "GBHALFTRUNCATE", halfcode_lead[1])
            halfcode_lead = None
            reconsume = token
        else:
            yield token
        #
    #
#








