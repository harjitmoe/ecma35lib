#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io, pprint
import tokenfeed

teststr = "\nかFoo\x7fら侅ら¥a~염盐塩鹽｜걈 ~¥\x1b[A\x1b[B\x1b]0;𐐈𐐤𐐓𐐀\x1b\\𐐈𐐤𐐓𐐀\x1b[\x20_kg¥\n"
test2 = "\nНаш благодетель знает своё высокое призвание и будет верен ему.\n"

dat = (b"\x1B%G\x1B!F" + teststr.encode("utf-8-sig") + "\x1CJ염盐塩鹽\x1CK".encode("utf-8") +
       b"\xa4\xed\xa0\xc1\x80\xed\xa0\x81\xed\xb0\xa4" + # Deliberately invalid UTF-8
       b"\x1Bc\x1B%9unrecdata" + # Unrecognised WSR DOCS, should stay as WORD ops in output.
       b"\x1B%/L" + teststr.encode("utf-16be") + 
       b"\xDC\x20\xD8\x20" +                             # Deliberately invalid UTF-16BE
       "\x1B%/L\uFFFE".encode("utf-16be") + teststr.encode("utf-16le") + 
       "\x1B%/F".encode("utf-16le") + teststr.encode("utf-32be") + 
       "\x1B%/F\uFFFE".encode("utf-32be") + teststr.encode("utf-32le") + 
       "\x1B%@".encode("utf-32le") + teststr.encode("iso-2022-jp-ext", errors="replace") +
       "\x1B-A\x1B.BFrançaisFran\x0Eg\x0FaisÐð\x1B}Ðð\x1B~\x1b#//5".encode("latin-1") + 
       b"\x1B&@\x1B$)B\x1B$+D" + teststr.encode("euc-jp", errors="replace") +
       b"\x1B$)A\x1B$+~" + teststr.encode("euc-cn", errors="replace") +
       b"\x1B$)C" + teststr.encode("euc-kr", errors="replace") +
       b"\x1B-@" + test2.encode("koi8-r") + 
       b"\x1B-L" + test2.encode("iso-8859-5") + 
       b"\x1BB\x82\x1B[?25h\x1B(0unrecdata" +
       "\x1B%BFran\xA0çais//".encode("latin-1") + b"\xA1\x7E\xF6\x21\x21" + # i.e. "ŝ䀖" in UTF-1
       "\x1B%0⑨/⑨ちるの＇ﾁﾙﾉ".encode("ms-kanji") + b"\xFA\x56" +
       b"\x1B%/B\x1B%@HAHA_AS_IF\xA1" # i.e. the last DOCS @ should not switch back.
)

x = io.BytesIO(dat)

print(end = "\x1Bc")

x = tokenfeed.process_stream(x)

# Note: nothing's actually executed yet.

x = list(x)

# Note: now it has.

pprint.pprint(x)
print()







