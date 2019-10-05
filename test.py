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
# - Mnemonic parsing for CSI sequences, and CEX sequences for which I can get enough info.
# STILL TO DO:
# - More graphical sets.
# - Rich or annotated output of some sort.
# - Composition sequences (Hangul ones, also backspace ones).
# - Functionality of CSI, CEX, C1 _et cetera_ controls.
# - Processing of UTF-1 sections to codepoints.
# - More control sets.
# - Announcements, and some means of verifying them.

import io, pprint, types
import tokenfeed, utf8filter, utf16filter, utf32filter, controlsets, fixedcontrols, invocations, \
       designations, graphsets, simpleprinter, controlsequences, rawfilter, unkdocsfilter

teststr = "\nかFoo\x7fら侅ら¥a~염盐塩鹽｜걈 ~¥\x1b[A\x1b[B\x1b]0;𐐈𐐤𐐓𐐀\x1b\\𐐈𐐤𐐓𐐀\x1b[\x20_kg¥\n"
test2 = "\nНаш благодетель знает своё высокое призвание и будет верен ему.\n"

state = types.SimpleNamespace(pedantic_overlong=True, overlong_null=False, pass_cesu=False,
    pedantic_surrogates=True, osc_bel_term=True, cur_c0="ir001", cur_c1="RFC1345",
    glset=0, grset=1, default_endian=">", regard_bom=1, start_in_utf8=False,
    cur_gsets=["ir006", "ir100", "nil", "nil"])

dat = (b"\x1B%G\x1B!F" + teststr.encode("utf-8-sig") + "\x1CJ염盐塩鹽\x1CK".encode("utf-8") +
       b"\xa4\xed\xa0\xc1\x80\xed\xa0\x81\xed\xb0\xa4" + # Deliberately invalid UTF-8
       b"\x1Bc\x1B%0unrecdata" + # Unrecognised WSR DOCS, should stay as WORD ops in output.
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
       b"\x1B%/B\x1B%@HAHA_AS_IF\xA1" # i.e. the last DOCS @ should not switch back.
)

x = io.BytesIO(dat)

print(end = "\x1Bc")

for f in [tokenfeed.tokenise_stream, utf8filter.decode_utf8, utf16filter.decode_utf16,
          utf32filter.decode_utf32, rawfilter.decode_raw, unkdocsfilter.decode_remaining_docs,
          designations.decode_designations, controlsets.decode_control_sets,
          fixedcontrols.decode_fixed_controls, controlsequences.decode_control_strings, 
          invocations.decode_invocations, graphsets.decode_graphical_sets,
          simpleprinter.simple_print]:
    x = f(x, state)

# Note: nothing's actually executed yet.

x = list(x)

# Note: now it has.

pprint.pprint(x)
print()







