#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io, pprint
from ecma35.decoder import tokenfeed

teststr = "\nかFoo\x7fら侅ら¥a~염盐塩鹽䝼/丽/〒｜“걈 ~¥”\x1b[A\x1b[B\x1b]0;𐐈𐐤𐐓𐐀\x1b\\𐐈𐐤𐐓𐐀\x1b[\x20_kg¥\n"
test2 = "\nНаш благодетель знает своё высокое призвание и будет верен ему.\n"
scsutest = (b"\xD6\x6C\x20\x66\x6C\x69\x65\xDF\x74\x20\x12\x9C\xBE\xC1\xBA\xB2\xB0" +
            b"\x08\x00\x1B\x4C\xEA\x16\xCA\xD3\x94\x0F\x53\xEF\x61\x1B\xE5\x84\xC4" + 
            b"\x0F\x53\xEF\x61\x1B\xE5\x84\xC4\x16\xCA\xD3\x94\x08\x02\x0F\x53\x4A" +
            b"\x4E\x16\x7D\x00\x30\x82\x52\x4D\x30\x6B\x6D\x41\x88\x4C\xE5\x97\x9F" +
            b"\x08\x0C\x16\xCA\xD3\x94\x15\xAE\x0E\x6B\x4C\x08\x0D\x8C\xB4\xA3\x9F" +
            b"\xCA\x99\xCB\x8B\xC2\x97\xCC\xAA\x84\x08\x02\x0E\x7C\x73\xE2\x16\xA3" + 
            b"\xB7\xCB\x93\xD3\xB4\xC5\xDC\x9F\x0E\x79\x3E\x06\xAE\xB1\x9D\x93\xD3" + 
            b"\x08\x0C\xBE\xA3\x8F\x08\x88\xBE\xA3\x8D\xD3\xA8\xA3\x97\xC5\x17\x89" + 
            b"\x08\x0D\x15\xD2\x08\x01\x93\xC8\xAA\x8F\x0E\x61\x1B\x99\xCB\x0E\x4E" + 
            b"\xBA\x9F\xA1\xAE\x93\xA8\xA0\x08\x02\x08\x0C\xE2\x16\xA3\xB7\xCB\x0F" + 
            b"\x4F\xE1\x80\x05\xEC\x60\x8D\xEA\x06\xD3\xE6\x0F\x8A\x00\x30\x44\x65" + 
            b"\xB9\xE4\xFE\xE7\xC2\x06\xCB\x82")

dat = (b"\x1B[m\x1B%G\x1B!F" + teststr.encode("utf-8-sig") + "\x1CJ염盐塩鹽\x1CK".encode("utf-8") +
       b"\xa4\xed\xa0\xc1\x80\xed\xa0\x81\xed\xb0\xa4" + # Deliberately invalid UTF-8
       '\nDisplay test: "Muhammad \x1B[1\x20_صلى الله عليه وسلم\x1B[2\x20_"\n'.encode("utf-8") +
       '\n\x1B[1\x20_2/3\x1B[1\x20_2\u20443\x1B[2\x20_\n'.encode("utf-8") +
       b"\x1Bc\x1B%9unrecdata" + # Unrecognised WSR DOCS, should stay as WORD ops in output.
       b"\x1B%/L" + teststr.encode("utf-16be") + 
       b"\xDC\x20\xD8\x20" +                             # Deliberately invalid UTF-16BE
       "\x1B%/L\uFFFE".encode("utf-16be") + teststr.encode("utf-16le") + 
       "\x1B%/F".encode("utf-16le") + teststr.encode("utf-32be") + 
       "\x1B%/F\uFFFE".encode("utf-32be") + teststr.encode("utf-32le") + 
       "\x1B%@".encode("utf-32le") + teststr.encode("iso-2022-jp-ext", errors="replace") +
       "\x1B-A\x1B.BFrançaisFran\x0Eg\x0FaisÐð\x1B}Ðð\x1B~\x1b#//5".encode("latin-1") + 
       b"\x1B&@\x1B$)B\x1B$+D" + teststr.encode("euc-jp", errors="replace") + b"\xA0\xA0\xFE\xFE" + 
       b"\x1B$)Q\x1B$+P" + teststr.encode("euc-jis-2004", errors="replace") + b"\x8F\xA0\xA0" + 
       b"\x1B$)A\x1B$+~" + teststr.encode("euc-cn", errors="replace") +
       b"\x1B&0\x1B$)A" + teststr.encode("euc-cn", errors="replace") +
       b"\x1B$)C" + teststr.encode("euc-kr", errors="replace") +
       b"\x1B%1" + teststr.encode("uhc", errors="replace") +
       b"\xc0\x79\x1B$)N\x1B$+~\n\xc0\x79\xae\xf0\n" +
       b"\x1B%2" + teststr.encode("gb18030", errors="replace") + b"\x80" +
       b"\x1B&1\x1B*I" + teststr.encode("cp936", errors="replace") + b"\x80" +
       b"\x1B&2\x1B*I" + teststr.encode("cp936", errors="replace") + b"\x80" +
       b"\n\x815\xF47\x1B&2\x1B$)A\x1B&0\x1B$/!0\xa3\xa0\x1B&4\x1B$)A\x1B&1\x1B$/!0\xA6\xF3\xFE\x6C\x815\xF47" +
       b"\x1B%4" + (teststr + "糎兀嗀兀嗀").encode("big5hkscs", errors="replace") +
       b"\x1B$+!3" + (teststr + "糎兀嗀兀嗀").encode("big5", errors="replace") +
       b"\x1B%@\x1B-@" + test2.encode("koi8-r") + 
       b"\x1B-L" + test2.encode("iso-8859-5") + 
       b"\x1B$)G\x1B$*!1\x8E\xA3\xC0\xDA\xFC\xFC" + # i.e. 塩鹽 in EUC-TW
       b"\x1BB\x82\x1B[?25h\x1B(0unrecdata" +
       "\x1B%BFran\xA0çais//".encode("latin-1") + b"\xA1\x7E\xF6\x21\x21\n" + # i.e. "ŝ䀖" in UTF-1
       b"\x1B%@\x1B(!2\x1B)!2\x1B*!2\x1B+!2undefinedset\x8Editto\n" +
       "\x1B%0⑨/⑨ちるの ＇ﾁﾙﾉ".encode("ms-kanji") + b"\xFA\x56\n\x1B$G`\x1B$QEW\x0Fbandbugs\n" +
       "\x1B$)Q\x1B$+P⑨/⑨ちるの ＇ﾁﾙﾉ＇\n".encode("shift_jis-2004") +
       b"\x1B&1\x1B$)B\x1B&1\x1B*I\xFE\x87\xE8\x86\xCD\x86\xCE\x87\xFA\x87\xFB\xEB\x6E\n" + # MacJapanese
       b"\x1B&0foo \x1B%/0" + scsutest + b"\n\x01" + 
       b"\x1B%3\x1B[437*p\x1B[4)p\n\x7f\v\x1B[2)p\f\x1B[)p" + 
       teststr.encode("cp437", errors="replace") + 
       b"\x1B[1252*p" + teststr.encode("cp1252", errors="replace") + 
       b"\x1B%@\x1B)!EWenn ich nur nichts von Nachwelt h\xE8oren sollte. Gesetzt da\xC7 ich von Nachwelt reden wollte, Wer machte denn der Mitwelt Spa\xCF?" + 
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







