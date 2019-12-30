#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import controldata

def decode_control_strings(stream, state):
    active = []
    idbytes = []
    parbytes = []
    mode = "normal"
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if mode == "normal":
            if (token[0] == "CTRL") and (token[1] in ("DCS", "SOS", "OSC", "PM", "APC")):
                active.append(token)
                mode = "string"
            else:
                yield token # Pass everything else through
        else:
            assert mode == "string"
            if token[0] == "CTRL" and (token[1] == "ST" or
                    (token[1] == "BEL" and active[0][1] == "OSC" and state.osc_bel_term)):
                active.append(token)
                yield ("CTRLSTRING", active[0][1], tuple(active))
                del active[:]
                mode = "normal"
            elif token[0] == "ENDSTREAM":
                # String was never terminated.
                yield ("ERROR", "TRUNCSEQ", tuple(active))
                yield token
                return
            else:
                active.append(token)
            
            







                