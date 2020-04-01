An experimental implementation of ECMA-35 (correspending to ISO/IEC 2022, JIS X 0202) aspiring to
support the mechanisms defined by it and related specifications (ECMA-6, ECMA-43, ECMA-48 and 
others) in their entirety, even those which are not supposed to be used together.

I do not claim conformance with any standard: where standards are named, this is by way of sourcing
a specification consulted and/or identifying a format codified by that specification, and should
not be taken as a claim of compliance.

# Warnings

This is intended to serve an experimental and potentially educational purpose; it is not expected
to become anything which is sensible to include in production.

ECMA-35 has the inherent property that it is basically impossible to sanitise a text in the full 
encoding system (as opposed to a secure subset). Please do not use this facing the internet. If 
you do, it's on you, but don't say I didn't warn you precisely why you shouldn't.

Also, this has not been professionally vetted for security and may contain security-relevant 
bugs. The complexity compared to restricted code versions such as ISO-8859-7, EUC-JP or even 
ISO-2022-JP only makes this all the more likely. This is another very good reason not to use this 
implementation facing the internet.

# Copying

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/

# Structure

The `ecma35` package contains the library itself. The `data` subpackage contains mapping data for
the various variants of the various sets to Unicode (for graphical sets) or mnemonics (for control
code sets). It also contains code for previewing and comparing these data. It includes mapping
data for most of the two-byte codes (except for Blissymbolics, which lacks a Unicode representation
whatsoever), and for several common one-byte codes, but there are many one-byte codes which it does
not currently support.

The `decoder` subpackage contains code for decoding the ECMA-35 stream. However, it also includes
code for handling other formats which conform only partially, or not at all, to ECMA-35. Several of
these are available using ECMA-35 DOCS sequences: for instance, it includes decoders for UTF-8,
UTF-16, SCSU and Shift\_JIS. The decoder is implemented using a stack of generator functions, all
with access to a common state.

An `encoder` subpackage is to be expected to be much more involved. It is not clear what an encoder
for the entirety of ECMA-35, leave alone the other DOCS filters, would look like: generally
speaking, an encoder is written for a particular code version / subset of ECMA-35.

Currently, `test.py` runs a test on the `decoder` subpackage. It writes its output to stdout;
however, I'm usually directing its output to `out.txt` as a manner of rudimentary regression
testing: if a change makes `out.txt` differ from its previous Git revision, this could be
indicative of an introduced problem. Its test input is highly artificial, and makes use of several
features which would not usually be used in the same document.

The scripts `genjiscmp.py` and `gencnscmp.py` use only the `data` subpackage. They generate HTML
comparison files for JIS (X 0208 / X 0212 / X 0213) and CNS 11643 in various vendor versions,
editions and mapping variations. See [CNS comparison](https://harjit.moe/cns-conc.html), 
[JIS comparison](https://harjit.moe/jis-conc.html).

# Private assignments (incomplete)

Separate coding systems:

|Private assignment|Meaning|
|---|---|
|`DOCS 0`|Shift\_JIS. Actually a frontend on an equivalent EUC-JP model, so variant can be thereby customised.|
|`DOCS 1`|Unified Hangul Code. Also supports the KPS equivalent.|
|`DOCS 2`|GBK (including GB 18030 surrogates).|
|`DOCS 3`|"Plain extended ASCII", i.e. without `0x80-0x9F` as a control character range.|
|`DOCS 4`|Big Five (lead byte range `0x81-0xFE`)|
|`DOCS 5`|Big Five (lead byte range `0xA1-0xFC`)|
|`DOCS / 0`|Standard Compression Scheme for Unicode (SCSU)|

Regarding World System Teletext:

|Private assignment|Meaning|
|---|---|
|`IRR 1 G*D4 ! B`|World System Teletext Latin G0, invariant subset|
|`IRR 0 G*D4 Y`|World System Teletext Latin G0 for Italy|
|`G*D4 # 1`|World System Teletext Latin G0 for France|
|`G*D4 # 2`|World System Teletext Latin G0 for Spain and Portugal|
|`G*D4 # 3`|World System Teletext Latin G0 for Estonia|
|`G*D4 # 4`|World System Teletext Latin G0 for Latvia and Lithuania|
|`G*D4 # 5`|World System Teletext Latin G0 for Serbia, Bosnia, Croatia and Slovenia|
|`IRR 0 G*D4 # 5`|World System Teletext Latin G0 for Serbia, Slovenia _et al._ with the Dollar sign|
|`G*D4 # 6`|World System Teletext Latin G0 for Czech and Slovak|
|`G*D4 # 7`|World System Teletext Latin G0 for Poland|
|`G*D4 # 8`|World System Teletext Latin G0 for Romania|
|`G*D4 # 9`|World System Teletext Latin G0 for Turkey|

Miscellaneous single-byte assignments:

|Private assignment|Meaning|
|---|---|
|`IRR 0 G*D4 @`|Old IRV with tilde (rather than overscore)|
|``IRR 0 G*D4 [ACEH`g]``|DEC NRCS, where they differ from standard|
|``IRR 0 G*D4 B``|ASCII with overscore (rather than tilde)|
|`IRR [*] G*D4 I`|With `IRR 0`, IBM's 4992 (used for its counterparts in IBM's 1041 where applicable). With `IRR 1`, an equivalent extraction from MacJapanese. With `IRR 2` or `IRR 3`, much the same treatment of Windows-31J and friends (in some non-ECMA35 DOCS filters, `IRR 3` will suppress the 0x80 control mapping in favour of the Euro while `IRR 2` will not; otherwise, they are the same).|
|`IRR 0 G*D4 J`|JIS-Roman with tilde (rather than overscore)|
|`IRR 0 G*D4 ! B`|DEC NRCS, invariant subset|
|`G*D4 # 0`|KS X 1003|
|`IRR 0 G*D4 # 0`|KS X 1003 with tilde|
|`G*D4 $ 1`|DEC NRCS for Switzerland (corresponding to DEC's (not ARIB's) `G*D4 4`)|
|`G*D4 $ 2`|DEC NRCS for the Netherlands (corresponding to DEC's `G*D4 =`)|
|``IRR 1 G*D4 ` ``|Danish equivalent to NS 4551 (IBM's 1017)|
|`G*D6 ! 0`|RFC 1345's so-called ISO-IR-111/ECMA-Cyrillic (incompatible with ISO-IR-111 itself).|

Double-byte assignments:

|Private assignment|Meaning|
|---|---|
|`IRR ? G*DM4 @`|JIS C 6226-1978|
|`IRR 0 G*DM4 @`|JIS C 6226, version encoded by IBM-942|
|`IRR 1 G*DM4 @`|JIS C 6226, version used by NEC PC98 (default for this F-byte)|
|`IRR ? G*DM4 A`|GB/T 2312-1980, with half of the GB 6345.1-1986 corrigienda, as shown in the ISO-IR-58 registration itself|
|`IRR 0 G*DM4 A`|GB/T 12345|
|`IRR 1 G*DM4 A`|GB 18030-2000 (only levels 1 and 2 unless in GBK DOCS)|
|`IRR 2 G*DM4 A`|GB 18030-2005 (default; only levels 1 and 2 unless in GBK DOCS)|
|`IRR 3 G*DM4 A`|GB 18030, WHATWG variant (only differs from GB 18030-2005 when in GBK DOCS)|
|`IRR 4 G*DM4 A`|GB 18030, favouring duplicate mappings over PUA mappings for standard characters|
|`IRR 5 G*DM4 A`|GB/T 2312, variant used on classic Mac OS|
|`IRR 6 G*DM4 A`|GB/T 2312-1980, without GB 6345.1-1986 corrigienda (including script g, rather than fullwidth or standard g)|
|`IRR 7 G*DM4 A`|GB/T 2312-1980, with corrigienda but not extensions from GB 6345.1-1986|
|`IRR ? G*DM4 B`|JIS C 6226 / X 0208-1983|
|`IRR @ G*DM4 B`|JIS X 0208-1990 (standard sequence, listed here for completeness)|
|`IRR 0 G*DM4 B`|JIS X 0208, WHATWG variant (default; synchronised with Windows-31J)|
|`IRR 1 G*DM4 B`|JIS X 0208, "KanjiTalk 7" variant used on classic Mac OS|
|`IRR 2 G*DM4 B`|JIS X 0208, "PostScript" variant used on classic Mac OS|
|`IRR 3 G*DM4 B`|JIS X 0208, "KanjiTalk 6" variant used on classic Mac OS|
|`IRR 4 G*DM4 B`|JIS X 0208, with UTC-style mapping of em dash / horizontal bar character|
|`IRR 5 G*DM4 B`|JIS X 0208, Open Group version for JIS-Roman based EUC-JP|
|`IRR 6 G*DM4 B`|JIS X 0208, Open Group version for ASCII-based EUC-JP|
|`IRR 7 G*DM4 B`|JIS X 0208, Open Group version for Microsoft-style EUC-JP|
|`IRR 8 G*DM4 D`|JIS X 0208, version encoded by IBM-954|
|`IRR 9 G*DM4 D`|JIS X 0208, DoCoMo JIS emoji|
|`IRR : G*DM4 D`|JIS X 0208, KDDI JIS emoji|
|`IRR ; G*DM4 D`|JIS X 0208, SoftBank JIS emoji|
|`IRR ? G*DM4 D`|JIS X 0212:1990|
|`IRR 0 G*DM4 D`|JIS X 0212 with va/vi/ve/vo|
|`IRR 1 G*DM4 D`|JIS X 0212, Open Group version for JIS-Roman based EUC-JP|
|`IRR 2 G*DM4 D`|JIS X 0212, Open Group version for ASCII-based EUC-JP|
|`IRR 3 G*DM4 D`|JIS X 0212, Open Group version for Microsoft-style EUC-JP|
|`IRR 4 G*DM4 D`|JIS X 0212, version encoded by IBM-954|
|`IRR ? G*DM4 E`|CCITT Hanzi Code (GB 2312 variant), as shown in ISO-IR-165 itself|
|`IRR 0 G*DM4 E`|CCITT Hanzi Code (GB 2312 variant), amended to follow GB 6345.1-1986 where applicable|
|`IRR ? G*DM4 I`|CNS 11643-1992 plane 3|
|`IRR 0 G*DM4 I`|CNS 11643-1988 plane 14 (some gaps due to lack of source material available to me)|
|`IRR 1 G*DM4 I`|CNS 11643-1988 plane 14 with extensions, as submitted to the IRG (some gaps due to lack of source material available to me)|
|`IRR 2 G*DM4 I`|CNS 11643-2007 plane 3|
|`IRR 3 G*DM4 I`|CNS 11643-2007 plane 3, with as many of the since-removed 1988 assignments as I have mappings for (default)|
|`G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as used in EUC-TW|
|`G*DM4 ! 2`|Hong Kong Supplementary Character Set, including ETEN characters (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`G*DM4 ! 3`|Non-ETEN Big5 kana and Cyrillic (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`G*DM4 ! 4`|IBM extensions for Shift\_JIS (accepted by Shift\_JIS filter in G3 slot, mapped to/from Shift\_JIS by the same mapping scheme as JIS X 0213 plane 2)|
|`G*DM4 ! 5`|DoCoMo Emoji extensions for Shift\_JIS (as above)|
|`G*DM4 ! 6`|KDDI Emoji extensions for Shift\_JIS (as above)|
|`G*DM4 ! 7`|SoftBank Emoji extensions for Shift\_JIS (as above)|
|`IRR ? G*DM4 ! 8`|GB 13131 (supplementary traditional)|
|`IRR 0 G*DM4 ! 8`|GB 7589 (supplementary simplified)|
|`IRR ? G*DM4 ! 9`|GB 13132 (further supplementary traditional)|
|`IRR 0 G*DM4 ! 9`|GB 7590 (further supplementary simplified)|

# Carried out

- Tokenisation of ECMA-35 streams with DOCS-integrated ISO 10646 streams.
- Processing of UTF-8 sections to codepoints.
- Processing of UTF-16 sections to codepoints.
- Processing of UTF-32 sections to codepoints.
- Processing of UTF-1 sections to codepoints (not thoroughly tested).
- Processing of SCSU sections to codepoints (not thoroughly tested).
- Opcoding C0 and C1 control characters.
- Opcoding the fixed controls.
- Parsing designator sequences.
- Invocation processing (i.e. resolving GL/GR tokens to G0/G1/G2/G3).
- Graphical set processing.
- Some sort of output.
- Mnemonic parsing for CSI sequences, and CEX sequences for which I can get enough info.
- Hangul composition sequences.
- IRR codes.
- Support for general extended ASCII (i.e. only the LHS follows ECMA-35) as a DOCS set.
- Support for Big5 as a DOCS set, including both incompatible maps of the Kana/Cyrillic.
- Support for GCC CSI sequences

# Still to do

- More graphical sets.
- More general RHS sets.
- Support for JOHAB as a DOCS set.
- Support for LMBCS as a DOCS set.
- Dynamically allocating sets, IRR codes, DOCS codes (e.g. Shift_JIS) in some configurable way.
- Proper handling of the T.51 / T.61 and ANSEL combining sequences. Probably don't need to stick to
  any hardcoded repertoire though, since (a) we're not trying to implement ISO/IEC 6937, but rather
  T.51 (which confines the entire ISO 6937 repertoire definition (rather than just one of the 
  charts as in ISO/IEC 6937) to an annex which isn't referenced from the main text), and (b) we're 
  mapping to ISO/IEC 10646, not to ISO/IEC 10367 or 8859, so combining marks aren't a problem.
- Functionality of CSI, CEX, C1 _et cetera_ controls.
  - Rich or annotated output of some sort.
- Backspace composition sequences.
- Figure out how the relevant parts of Videotex work:
  - The rest of the control sets.
  - The rest of the DOCS codes.
- Announcements, and some means of verifying them. Preferably by generating ERROR tokens.
- Some sort of encoder.
- Some sort of decent API for using it from outside.


