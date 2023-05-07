#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2023, as a refactor extracting earlier work from various parts of ecma35lib.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from ecma35.data import graphdata

# The 1B 25 40 sequence will indeed switch to ECMA-35, and cannot occur coincidentally since C0/CL
# bytes are not used as trail bytes, so it is in fact "with standard return".
shiftjisdocs = ("DOCS", False, (0x30,))
uhcdocs = ("DOCS", False, (0x31,))
gbkdocs = ("DOCS", False, (0x32,))
plainextasciidocs = ("DOCS", False, (0x33,))
bigfivedocs = ("DOCS", False, (0x34,))
bigfivenarrowdocs = ("DOCS", False, (0x35,))
elexdocs = ("DOCS", False, (0x36,))

# Switch to ECMA-35 is 01 1B 25 40 in single-byte mode, and 00 1B 00 25 00 40 in "Unicode" mode.
# In either case, just 1B 25 40 will not switch to ECMA-35, so SCSU is "without standard return".
scsudocs = ("DOCS", True, (0x35,))
ebcdicdocs = ("DOCS", True, (0x36,))

ecma35docs = ("DOCS", False, (0x40,))
utf1docs = ("DOCS", False, (0x42,))
utf8docs = (("DOCS", False, (0x47,)), # Current (still in ISO/IEC 10646 for UTF-8)
            ("DOCS", True, (0x47,)),  # Deprecated (UTF-8 level 1)
            ("DOCS", True, (0x48,)),  # Deprecated (UTF-8 level 2)
            ("DOCS", True, (0x49,)))  # Current (still in ISO/IEC 10646 for UTF-8)
utf16docs = (("DOCS", True, (0x40,)), # Deprecated (UCS-2 level 1)
             ("DOCS", True, (0x43,)), # Deprecated (UCS-2 level 2)
             ("DOCS", True, (0x45,)), # Deprecated (UCS-2 level 3)
             ("DOCS", True, (0x4A,)), # Deprecated (UTF-16 level 1)
             ("DOCS", True, (0x4B,)), # Deprecated (UTF-16 level 2)
             ("DOCS", True, (0x4C,))) # Current (still in ISO/IEC 10646 for UTF-16be)
utf32docs = (("DOCS", True, (0x41,)), # Deprecated (UCS-4 level 1)
             ("DOCS", True, (0x44,)), # Deprecated (UCS-4 level 2)
             ("DOCS", True, (0x46,))) # Current (still in ISO/IEC 10646 for UTF-32be)
rawdocs = ("DOCS", True, (0x42,))

def decode_docs_sequences(stream, state):
    for token in stream:
        if token == shiftjisdocs:
            yield ("RDOCS", "shift_jis", token[1], token[2])
        elif token == uhcdocs:
            yield ("RDOCS", "uhc", token[1], token[2])
        elif token == gbkdocs:
            yield ("RDOCS", "gbk", token[1], token[2])
        elif token == plainextasciidocs:
            yield ("RDOCS", "plainextascii", token[1], token[2])
        elif token == bigfivedocs:
            yield ("RDOCS", "bigfive", token[1], token[2])
        elif token == bigfivenarrowdocs:
            yield ("RDOCS", "bigfivenarrow", token[1], token[2])
        elif token == elexdocs:
            yield ("RDOCS", "elex", token[1], token[2])
        elif token == scsudocs:
            yield ("RDOCS", "scsu", token[1], token[2])
        elif token == ebcdicdocs:
            yield ("RDOCS", "ebcdic", token[1], token[2])
        elif token == ecma35docs:
            yield ("RDOCS", "ecma-35", token[1], token[2])
        elif token == utf1docs:
            yield ("RDOCS", "utf-1", token[1], token[2])
        elif token in utf8docs:
            yield ("RDOCS", "utf-8", token[1], token[2])
        elif token in utf16docs:
            yield ("RDOCS", "utf-16", token[1], token[2])
        elif token in utf32docs:
            yield ("RDOCS", "utf-32", token[1], token[2])
        elif token == rawdocs:
            yield ("RDOCS", "raw", token[1], token[2])
        else:
            yield token

