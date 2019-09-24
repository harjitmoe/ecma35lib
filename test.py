#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# DONE:
# - Tokenisation of ECMA-35 streams with DOCS-integrated ISO 10646 streams.
# - Processing of UTF-8 sections to codepoints.
# - Processing of UTF-16 sections to codepoints.
# - Processing of UTF-32 sections to codepoints.
# STILL TO DO IN THAT ORDER:
# - Fixed control processing (at very least LS1R, LS2, LS2R, LS3, LS3R).
# - Invocation processing (i.e. resolving GL/GR tokens to G0/G1/G2/G3).
# - Graphical set processing.
# STILL TO DO AT SOME POINT:
# - Processing of UTF-1 sections to codepoints.
# - More control sets.

import io, pprint
import tokenfeed, utf8filter, utf16filter, utf32filter, controlsets

teststr = "かFoo\nらら¥~¥𐐈𐐤𐐓𐐀¥"

dat = (b"\x1B%G" + teststr.encode("utf-8-sig") +
       b"\xa4\xed\xa0\xc1\x80\xed\xa0\x81\xed\xb0\xa4" + 
       b"\x1B%/L" + teststr.encode("utf-16be") + b"\xDC\x20\xD8\x20" +
       "\x1B%/L\uFFFE".encode("utf-16be") + teststr.encode("utf-16le") + 
       "\x1B%/F".encode("utf-16le") + teststr.encode("utf-32be") + 
       "\x1B%/F\uFFFE".encode("utf-32be") + teststr.encode("utf-32le") + 
       "\x1B%@".encode("utf-32le") + teststr.encode("iso-2022-jp-ext", errors="replace") +
       b"\x1B-A" + "FrançaisFran\x0Eg\x0Fais".encode("latin-1") + 
       b"\x1BA\x81\x1B%/B\x1B%@HAHA_AS_IF\xA1" # i.e. the last DOCS @ should not switch back.
)

x = io.BytesIO(dat)

for f in [tokenfeed.tokenfeed, utf8filter.utf8filter, utf16filter.utf16filter,
          utf32filter.utf32filter, controlsets.controlsfilter,
          list, pprint.pprint]:
    x = f(x)







