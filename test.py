#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# DONE:
# - Tokenisation of ECMA-35 streams with DOCS-integrated ISO 10646 streams.
# - Processing of UTF-8 sections to codepoints.
# - Processing of UTF-16 sections to codepoints.
# - Processing of UTF-32 sections to codepoints.
# - Opcoding C0 and C1 control characters.
# - Opcoding the fixed controls.
# - Parsing designator sequences.
# - Invocation processing (i.e. resolving GL/GR tokens to G0/G1/G2/G3).
# - Graphical set processing.
# - Some sort of output.
# STILL TO DO:
# - More graphical sets.
# - Rich or annotated output of some sort.
# - Composition sequences (Hangul ones, also backspace ones).
# - CSI and (ideally) CEX sequences. CSI sequences are open-access in ECMA-48, and fairly well
#   documented besides, so they should be doable. CEX sequences are defined in JIS C 6225 a.k.a.
#   JIS X 0207, which is withdrawn and also not open-access (ISO-IR-74 gives only a vague overview,
#   which could just as validly apply to CSI), so likely unattainable.
#   - Documentation for an implementation of CEX is available here, actually (doesn't seem to be
#     all the codes, and those it includes are not in enough detail to understand arg format):
#     http://printronix.com/wp-content/uploads/manuals/PTX_PRM_OKI_N7_256482A.pdf
# - Processing of UTF-1 sections to codepoints.
# - More control sets.
# - Announcements, and some means of verifying them.

import io, pprint
import tokenfeed, utf8filter, utf16filter, utf32filter, controlsets, fixedcontrols, invocations, \
       designations, graphsets, simpleprinter

teststr = "\nかFoo\x7fら侅ら¥a~염盐塩鹽｜걈 ~¥𐐈𐐤𐐓𐐀¥\n"
test2 = "\nНаш благодетель знает своё высокое призвание и будет верен ему.\n"

dat = (b"\x1B%G" + teststr.encode("utf-8-sig") +
       b"\xa4\xed\xa0\xc1\x80\xed\xa0\x81\xed\xb0\xa4" + # Deliberately invalid UTF-8
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
       b"\x1BB\x82\x1B%/B\x1B%@HAHA_AS_IF\xA1" # i.e. the last DOCS @ should not switch back.
)

x = io.BytesIO(dat)

for f in [tokenfeed.tokenise_stream, utf8filter.decode_utf8, utf16filter.decode_utf16,
          utf32filter.decode_utf32, controlsets.decode_control_sets,
          fixedcontrols.decode_fixed_controls, designations.decode_designations,
          invocations.decode_invocations, graphsets.decode_graphical_sets,
          simpleprinter.simple_print, list]:
    x = f(x)

print()







