#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# DONE:
# - Tokenisation of ECMA-35 streams with DOCS-integrated ISO 10646 streams.
# - Processing of UTF-8 sections to codepoints.
# - Processing of UTF-16 sections to codepoints.
# - Processing of UTF-32 sections to codepoints.
# - Opcoding the fixed-controls LS1R, LS2, LS2R, LS3 and LS3R.
# - Parsing graphical set designator sequences.
# - Invocation processing (i.e. resolving GL/GR tokens to G0/G1/G2/G3).
# STILL TO DO:
# - Graphical set processing.
# - Some sort of output.
# - Other fixed controls.
# - Processing of UTF-1 sections to codepoints.
# - More control sets.
# - Announcements, and some means of verifying them.

import io, pprint
import tokenfeed, utf8filter, utf16filter, utf32filter, controlsets, controlsfixed, invocations, \
       settypes

teststr = "かFoo\nら侅ら¥~¥𐐈𐐤𐐓𐐀¥"

dat = (b"\x1B%G" + teststr.encode("utf-8-sig") +
       b"\xa4\xed\xa0\xc1\x80\xed\xa0\x81\xed\xb0\xa4" + 
       b"\x1B%/L" + teststr.encode("utf-16be") + b"\xDC\x20\xD8\x20" +
       "\x1B%/L\uFFFE".encode("utf-16be") + teststr.encode("utf-16le") + 
       "\x1B%/F".encode("utf-16le") + teststr.encode("utf-32be") + 
       "\x1B%/F\uFFFE".encode("utf-32be") + teststr.encode("utf-32le") + 
       "\x1B%@".encode("utf-32le") + teststr.encode("iso-2022-jp-ext", errors="replace") +
       "\x1B-A\x1B.BFrançaisFran\x0Eg\x0FaisÐð\x1B}Ðð\x1B~".encode("latin-1") + 
       b"\x1B&@\x1B$)B\x1B$+D\x1b#//5" + teststr.encode("euc-jp", errors="replace") +
       b"\x1BA\x81\x1B%/B\x1B%@HAHA_AS_IF\xA1" # i.e. the last DOCS @ should not switch back.
)

x = io.BytesIO(dat)

for f in [tokenfeed.tokenfeed, utf8filter.utf8filter, utf16filter.utf16filter,
          utf32filter.utf32filter, controlsets.controlsfilter, controlsfixed.fixedcontrolsfilter,
          settypes.typesfilter, invocations.invocationfilter,
          list, pprint.pprint]:
    x = f(x)







