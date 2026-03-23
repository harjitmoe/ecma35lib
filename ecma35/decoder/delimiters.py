#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2026.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import controldata

def decode_delimiters(stream, state):
    for token in stream:
        if token[:2] != ("CTRL", "CMD"):
            yield token
        else:
            state.feedback.append(("POPDOCS", token))
