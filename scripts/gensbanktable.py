#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys, os
sys.path.append(os.path.abspath(os.pardir))

from ecma35.data.showgraph import show
from ecma35.data.multibyte.cellemojidata import hints2pua_sb2g
images = {(0xE255,): "Planet_-_The_Noun_Project.svg", (0xE256,): "Gnome-document-send.svg",
          (0xE50A,): "Twemoji12_e50a.svg"}
show("sbank2gpageE", wikitext=True, cdispmap=hints2pua_sb2g, images=images, friendly="SoftBank 2G Emoji encoding, page E")
show("sbank2gpageF", wikitext=True, cdispmap=hints2pua_sb2g, images=images, friendly="SoftBank 2G Emoji encoding, page F")
show("sbank2gpageG", wikitext=True, cdispmap=hints2pua_sb2g, images=images, friendly="SoftBank 2G Emoji encoding, page G")
show("sbank2gpageO", wikitext=True, cdispmap=hints2pua_sb2g, images=images, friendly="SoftBank 2G Emoji encoding, page O")
show("sbank2gpageP", wikitext=True, cdispmap=hints2pua_sb2g, images=images, friendly="SoftBank 2G Emoji encoding, page P")
show("sbank2gpageQ", wikitext=True, cdispmap=hints2pua_sb2g, images=images, friendly="SoftBank 2G Emoji encoding, page Q")
