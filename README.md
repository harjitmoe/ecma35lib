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

Individual files in `ecma35/data/singlebyte/sbmaps`, `ecma35/data/multibyte/mbmaps` and
`ecma35/data/names/namemaps` are (except as otherwise noted) not original to this project and, as 
such, the terms above do not apply. If and where elegible, they may use seperate terms.

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

## Separate coding systems:

|Private assignment|Meaning|
|---|---|
|`DOCS 0`|Shift\_JIS. Actually a frontend on an equivalent EUC-JP model, so variant can be thereby customised.|
|`DOCS 1`|Unified Hangul Code. Also supports the KPS equivalent.|
|`DOCS 2`|GBK (including GB 18030 surrogates).|
|`DOCS 3`|"Plain extended ASCII", i.e. without `0x80-0x9F` as a control character range.|
|`DOCS 4`|Big Five (lead byte range `0x81-0xFE`)|
|`DOCS 5`|Big Five (lead byte range `0xA1-0xFC`)|
|`DOCS 6`|HangulTalk|
|`DOCS 7`|Modified "hybrid" Extended Unix Code (as used by Windows code pages 20000 and 20932, and by Super DEC Kanji)|
|`DOCS / 5`|Standard Compression Scheme for Unicode (SCSU). Was previously `DOCS / 0`; changed to avoid conflict with use of `DOCS / 0` by X11 Compound Text.|
|`DOCS / 6`|EBCDIC.|
|`DOCS / 7`|UTF-EBCDIC.|

## Additional single-byte 94-character G-sets, and additional selectors for particular variants of single-byte 94-character G-sets

|Private assignment|Meaning|
|---|---|
|`IRR ? G*D4 @`|(Old ISO 646 International Reference Version)|
|`IRR 0 G*D4 @`|Old IRV with tilde (rather than overscore)|
|`IRR ? G*D4 A`|(BS 4730 (7-bit for United Kingdom))|
|`IRR 0 G*D4 A`|DEC NRCS for United Kingdom|
|`IRR 1 G*D4 A`|ISO-646:1967 "sterling" variant for fixed-width old-pence data|
|`IRR ? G*D4 B`|(ASCII)|
|`IRR 0 G*D4 B`|ASCII with overscore (rather than tilde)|
|`IRR 1 G*D4 B`|ASCII-1967 using broken-bar mapping|
|`IRR 2 G*D4 B`|ASCII-1967, PL/I variant|
|`IRR 3 G*D4 B`|Modified ASCII with Florin sign (cross between ASCII and `G*D4 $ 2`)|
|`IRR 4 G*D4 B`|ASCII, alternative Unicode mappings (backtick/apostrophe as quotation mark pair)|
|`IRR 5 G*D4 B`|ASCII, alternative Unicode mappings (mid-line caret, continuous vertical bar, discontinuous underscore)|
|`IRR 6 G*D4 B`|ASCII, alternative Unicode mappings (raised caret/tilde, backtick as grave-accent, continuous vertical bar)|
|`IRR 7 G*D4 B`|ASCII, alternative Unicode mappings (raised caret/tilde, backtick as grave-accent)|
|`IRR 8 G*D4 B`|ASCII, alternative Unicode mappings (raised caret, backtick as grave accent, continuous vertical bar)|
|`IRR 9 G*D4 B`|ASCII 1963/1967 hybrid, unicameral PL/I variant|
|`IRR : G*D4 B`|ASCII-1963 (graphic charset assignments only)|
|`IRR ? G*D4 C`|(7-bit Swedish and Finnish Journalism)|
|`IRR 0 G*D4 C`|DEC NRCS for Finnish|
|`IRR ? G*D4 E`|(7-bit Danish and Norwegian Journalism)
|`IRR 0 G*D4 E`|DEC NRCS for Danish and Norwegian|
|`IRR ? G*D4 G`|(7-bit Swedish and Finnish (SEN 85 02 00 annex B))|
|`IRR 0 G*D4 G`|Variant Swedish and Finnish, projected from EBCDIC WP96|
|`IRR ? G*D4 H`|(7-bit Swedish names or Swedish Teletext (SEN 85 02 00 annex C))|
|`IRR 0 G*D4 H`|DEC NRCS for Swedish|
|`IRR ? G*D4 I`|(JIS X 0201 katakana)|
|`IRR 0 G*D4 I`|JIS X 0201 katakana, with a superset of the extensions included in IBM's code page 4992 (and used for the counterparts from IBM's code page 1041 by the Shift\_JIS filter).|
|`IRR 1 G*D4 I`|JIS X 0201 katakana, an analogous extraction from MacJapanese.|
|`IRR 2 G*D4 I`|JIS X 0201 katakana, an extraction from Windows-31J and friends.|
|`IRR 3 G*D4 I`|JIS X 0201 katakana, an extraction from Windows-31J and friends, suppressing the 0x80 control mapping in some DOCS filters in favour of the Euro.|
|`IRR 4 G*D4 I`|JIS X 0201 katakana with extensions as in IBM's code page 4992.|
|`IRR 5 G*D4 I`|JIS X 0201 katakana with extensions as in IBM's code page 911.|
|`IRR 6 G*D4 I`|JIS X 0201 katakana with a subset of the extensions included in IBM's code page 1041.|
|`IRR 7 G*D4 I`|Hiragana analogue to JIS X 0201.|
|`IRR ? G*D4 J`|(JIS X 0201 Roman set)|
|`IRR 0 G*D4 J`|JIS-Roman with tilde (rather than overscore)|
|`IRR ? G*D4 K`|(DIN 66003 with apostrophe (default))|
|`IRR 0 G*D4 K`|DIN 66003 with acute|
|`IRR 1 G*D4 K`|DIN 66003 variant projected from EBCDIC WP96|
|`IRR ? G*D4 O`|(DIN 31624, possibly-older German relative of ISO 5426-1)|
|`IRR 0 G*D4 O`|DIN 31624, falling thru to T.51 for unallocated cells|
|`IRR ? G*D4 P`|(ISO 5426-1, bibliographic set related to (but incompatible with) T.51)|
|`IRR 0 G*D4 P`|ISO 5426-1, falling thru to T.51 for unallocated cells|
|`IRR ? G*D4 R`|(NF Z 62-010 (7-bit French), 1973 edition (also used by DEC))|
|`IRR 0 G*D4 R`|Variant 7-bit French projected from EBCDIC DP94 for Belgian French|
|`IRR 1 G*D4 R`|Variant 7-bit French projected from EBCDIC WP96 for Belgian French|
|`IRR 2 G*D4 R`|Variant 7-bit French projected from EBCDIC 38xx for Belgian French|
|`IRR ? G*D4 Y`|(Olivetti 7-bit Italian)|
|`IRR 0 G*D4 Y`|ETS 300 706 Latin G0 for Italy|
|`IRR 1 G*D4 Y`|7-bit Italian with not-sign|
|`IRR 2 G*D4 Y`|7-bit Italian projected from EBCDIC DCF Migration encoding|
|``IRR ? G*D4 ` ``|(NS 4551 version 1 (7-bit Norwegian))|
|``IRR 0 G*D4 ` ``|DEC alternate NRCS for Denmark and Norway|
|``IRR 1 G*D4 ` ``|Danish equivalent to NS 4551 (IBM code page 1017)|
|``IRR 2 G*D4 ` ``|Variant Denmark and Norway projected from EBCDIC WP96|
|`IRR ? G*D4 f`|(NF Z 62-010 (7-bit French), 1982 edition)|
|`IRR 0 G*D4 f`|Variant 7-bit French projected from EBCDIC encodings for Maghrebi French|
|`IRR 1 G*D4 f`|Variant 7-bit French projected from EBCDIC 38xx encoding|
|`IRR 2 G*D4 f`|Variant 7-bit French projected from EBCDIC DCF Migration encoding|
|`IRR ? G*D4 g`|(IBM 7-bit Portuguese)|
|`IRR 0 G*D4 g`|DEC NRCS for Portuguese|
|`IRR ? G*D4 k`|(ASMO 449 (ISO 9036) 7-bit Arabic)|
|`IRR 0 G*D4 k`|MARC-8 Basic Arabic|
|`IRR ? G*D4 l`|(ITU T.51-1988 first supplementary set (i.e. older version of the T.51 supplementary set without NBSP, SHY, not sign or brvbar))|
|`IRR 0 G*D4 l`|ITU T.51-1988 first supplementary set with ETS 300 706 extensions (default for this F-byte)|
|`IRR 1 G*D4 l`|ITU T.51-1988 first supplementary set with ETS 300 706 extensions, alternative Unicode mapping|
|`IRR ? G*D4 o`|(JIS X 9010 non-JISCII set for OCR-B.)|
|`IRR 0 G*D4 o`|ISO-8859-1 RHS cropped to 94-set, with backslash replacing yen sign (superset of the non-JISCII set for OCR-B).|
|`IRR ? G*D4 q`|JIS X 9010 backslash-only set for JIS X 9008, mapping to ASCII as strongly implied by registration rubric (subset of the non-JISCII set for OCR-B).|
|`IRR 0 G*D4 q`|JIS X 9010 backslash-only set for JIS X 9008, mapping to OCR DOUBLE BACKSLASH.|
|`IRR ? G*D4 ! B`|(ISO 646 invariant subset)|
|`IRR 0 G*D4 ! B`|DEC NRCS, invariant subset|
|`IRR 1 G*D4 ! B`|ETS 300 706 Latin G0, invariant subset|
|`IRR 2 G*D4 ! B`|IBM version of the invariant set|
|`IRR ? G*D4 ! E`|(ANSEL supplementary set, ANSI standard version (i.e. no eszett))|
|`IRR 0 G*D4 ! E`|ANSEL supplementary set, Library of Congress version (i.e. eszett at 0x47)|
|`IRR 1 G*D4 ! E`|ANSEL supplementary set, combined Library of Congress and Genealogical Society of Utah versions, i.e. duplicate eszetts at 0x47 and 0x4F (default for this F-byte)|
|`G*D4 8`|ARIB-STD-B24-1 single-byte JIS-X-0208-based (as opposed to JIS-X-0201-based) Katakana|
|`G*D4 9`|7-bit Quebec French (same as `G*D4 w`)|
|`G*D4 =`|DEC NRCS for Switzerland (same as `G*D4 $ 1`)|
|`G*D4 >`|DEC Technical Character Set|
|`G*D4 :`|User-defined (left-hand side of Windows code page 42)|
|`G*D4 ;`|ASCII but with Armenian versions of certain punctuation marks|
|`G*D4 ?`|ARIB-STD-B24-1 single-byte Hiragana|
|`G*D4 ! 0`|ASCII with dotted uppercase I|
|`G*D4 ! 1`|IBM 7-bit symbol set|
|`G*D4 ! 2`|Various miscellaneous ASCII subsets selected with `IRR`|
|`G*D4 ! 3`|ISO 5426-2 (mediæval scribal notation supplement)|
|`G*D4 ! 4`|ISO 6826-A (mathematical symbols)|
|`G*D4 ! 5`|ISO 6826-B (mathematical symbols)|
|`G*D4 ! 6`|ISO 10754 (Non-Slavic Cyrillic supplement)|
|`G*D4 ! 7`|IBM 7-bit Hebrew|
|`G*D4 ! 8`|Digits only|
|`G*D4 ! 9`|Machine-readable cheque delimeter marks|
|`IRR ? G*D4 ! :`|ISO 8957-A 7-bit Hebrew|
|`IRR 0 G*D4 ! :`|MARC-8 Hebrew|
|`G*D4 ! ;`|ISO 8957-B Hebrew cantillation marks supplement|
|`G*D4 ! <`|Left-hand side of the code page of the Webdings font|
|`G*D4 ! =`|Left-hand side of the code page of the Wingdings font|
|`G*D4 ! >`|Left-hand side of the code page of the Wingdings 2 font|
|`G*D4 ! ?`|Left-hand side of the code page of the Wingdings 3 font|
|`G*D4 " 0`|ISCII Devanagari|
|`G*D4 " 1`|Korean N-byte Hangul Code (KS C 5601:1974)|
|`G*D4 " 2`|Hewlett-Packard 7-bit legal notation (with e.g. trademark / section signs)|
|`G*D4 " 3`|IBM-PC line drawing|
|`G*D4 " 4`|DEC 8-bit Hebrew|
|`G*D4 " 5`|Hewlett-Packard line drawing|
|`G*D4 " 6`|Hewlett-Packard 8-bit Roman encoding, right-hand side|
|`G*D4 " 7`|IBM additional pseudographics for `troff`|
|`G*D4 " 9`|Adobe Standard / PostScript Standard encoding, right-hand side|
|`IRR ? G*D4 " :`|ASCII but with Arabic versions of certain punctuation marks|
|`IRR 0 G*D4 " :`|Subset of ASCII but with Arabic versions of certain punctuation marks|
|`IRR ? G*D4 " ;`|Subset of Thai TIS-620:1986|
|`IRR @ G*D4 " ;`|Thai TIS-620:1986 (as a 94-character set designatable to G0, unlike `G*D6 T`)|
|`G*D4 " <`|ARIB-STD-B24-1 mosaic set C|
|`IRR ? G*D4 " =`|Galaksija 7-bit Gajica (excluding redundant representations of mosaic characters)|
|`IRR @ G*D4 " =`|Galaksija 7-bit Gajica extended with lowercase letters|
|`G*D4 " >`|DEC 7-bit Greek|
|`G*D4 " ?`|DEC 8-bit Greek, right-hand side|
|`IRR ? G*D4 # 0`|KS X 1003|
|`IRR 0 G*D4 # 0`|KS X 1003 with tilde|
|`G*D4 # 1`|ETS 300 706 Latin G0 for France|
|`G*D4 # 2`|ETS 300 706 Latin G0 for Spain and Portugal|
|`G*D4 # 3`|ETS 300 706 Latin G0 for Estonia|
|`G*D4 # 4`|ETS 300 706 Latin G0 for Latvia and Lithuania|
|`IRR ? G*D4 # 5`|ETS 300 706 Latin G0 for Serbia, Bosnia, Croatia and Slovenia|
|`IRR 0 G*D4 # 5`|ETS 300 706 Latin G0 for Serbia, Slovenia _et al._ with the Dollar sign|
|`G*D4 # 6`|ETS 300 706 Latin G0 for Czech and Slovak|
|`G*D4 # 7`|ETS 300 706 Latin G0 for Poland|
|`G*D4 # 8`|ETS 300 706 Latin G0 for Romania|
|`G*D4 # 9`|ETS 300 706 Latin G0 for Turkey|
|`G*D4 # :`|SoftBank 2G (single-byte) Emoji page E|
|`G*D4 # ;`|SoftBank 2G (single-byte) Emoji page F|
|`G*D4 # <`|SoftBank 2G (single-byte) Emoji page G|
|`G*D4 # =`|SoftBank 2G (single-byte) Emoji page O|
|`G*D4 # >`|SoftBank 2G (single-byte) Emoji page P|
|`G*D4 # ?`|SoftBank 2G (single-byte) Emoji page Q|
|`G*D4 $ 0`|DEC Special Graphics (VT52 version)|
|`G*D4 $ 1`|DEC NRCS for Switzerland (same as `G*D4 =`)|
|`G*D4 $ 2`|DEC NRCS for the Netherlands (corresponding to DEC's (not ARIB's) `G*D4 4`)|
|`G*D4 $ 3`|Marlett encoding|
|`G*D4 $ 4`|Zapf Dingbats, GL range|
|`G*D4 $ 5`|Zapf Dingbats, GR range|
|`G*D4 $ 6`|Symbol font encoding, GL range|
|`G*D4 $ 7`|Symbol font encoding, GR range (no euro)|
|`G*D4 $ 8`|7-bit Maltese|
|`IRR ? G*D4 $ 9`|7-bit Icelandic with octothorpe and universal-currency-sign|
|`IRR 0 G*D4 $ 9`|7-bit Icelandic, following the DP94 set of EBCDIC code page 871|
|`IRR 1 G*D4 $ 9`|7-bit Icelandic with pound-sterling and dollar signs|
|`IRR ? G*D4 $ :`|7-bit Polish (PN⁠-⁠T⁠-⁠42109-02-ZU0 variant with Złoty sign)|
|`IRR 0 G*D4 $ :`|7-bit Polish, following the DP94-range subset (GL set) of EBCDIC code page 252|
|`IRR 1 G*D4 $ :`|7-bit Polish (PN⁠-⁠T⁠-⁠42109-02-ZU0)|
|`IRR 2 G*D4 $ :`|7-bit Polish with complete uppercase and lowercase (PN⁠-⁠T⁠-⁠42109-03-ZU2)|
|`IRR ? G*D4 $ ;`|ISO 11822:1996 Arabic supplementary set|
|`IRR 0 G*D4 $ ;`|MARC-8 Extended Arabic|
|`G*D4 $ <`|ISO 10586:1996 Georgian|
|`G*D4 $ =`|ISO 10585:1996 Armenian|
|`G*D4 $ ?`|Armenian ARMSCII|
|`G*D4 % 0`|DEC 8-bit Turkish, right-hand side|
|`G*D4 % 1`|MARC-8 superscript numbers|
|`G*D4 % 2`|DEC 7-bit Turkish|
|`IRR ? G*D4 % 4`|7-bit Canadian French, projected from EBCDIC DP94|
|`IRR 0 G*D4 % 4`|7-bit Canadian French, projected from EBCDIC WP96|
|`G*D4 % 5`|DEC Multinational Character Set, right-hand side|
|`G*D4 % 6`|DEC 7-bit Portuguese|
|`G*D4 % 7`|7-bit European Portuguese, projected from EBCDIC DP94|
|`G*D4 % 8`|7-bit Turkish, projected from EBCDIC DP94|
|`G*D4 % 9`|7-bit Roman, projected from EBCDIC 38xx|
|`IRR ? G*D4 % :`|7-bit Roman for use with a Greek set, projected from EBCDIC, small version|
|`IRR @ G*D4 % :`|7-bit Roman for use with a Greek set, projected from EBCDIC, large version|
|`IRR ? G*D4 % ;`|7-bit Roman for use with a Cyrillic set, projected from EBCDIC, large version|
|`IRR 0 G*D4 % ;`|7-bit Roman for use with a Cyrillic set, projected from EBCDIC, small version|
|`G*D4 % <`|7-bit Belgium, projected from EBCDIC DCF Migration encoding|
|`IRR ? G*D4 % =`|7-bit Hebrew (SI 960)|
|`IRR 0 G*D4 % =`|7-bit Hebrew (ETS 300 706)|
|`G*D4 % >`|7-bit Roman, projected from EBCDIC DCF Migration encoding|
|`G*D4 % ?`|7-bit Roman, projected from EBCDIC WP96 for Israel|
|`IRR ? G*D4 & 0`|7-bit Roman, projected from EBCDIC DP94 for Japan|
|`IRR 0 G*D4 & 0`|7-bit Roman, projected from EBCDIC for Japan, without Yen sign|
|`IRR 1 G*D4 & 0`|7-bit Roman, projected from EBCDIC for Japan, alternative representation of Yen sign|
|`IRR 2 G*D4 & 0`|7-bit Roman, projected from EBCDIC for Japan, small version|
|`IRR ? G*D4 & 1`|7-bit Roman, projected from EBCDIC for Korea, large version|
|`IRR 0 G*D4 & 1`|7-bit Roman, projected from EBCDIC for Korea, small version|
|`IRR ? G*D4 & 2`|7-bit Roman, projected from EBCDIC Library Character Set for IBM 3800, small version|
|`IRR 0 G*D4 & 2`|7-bit Roman, projected from EBCDIC Library Character Set for IBM 3800, large version|
|`G*D4 & 3`|7-bit Roman for use with a Simplified Chinese set, projected from EBCDIC, small version|
|`G*D4 & 4`|8-bit Cyrillic (plain KOI-8), right-hand side|
|`G*D4 & 5`|7-bit Cyrillic (Short-KOI)|
|`IRR ? G*D4 & 6`|7-bit Spanish, projected from EBCDIC DP94|
|`IRR 0 G*D4 & 6`|7-bit Spanish, projected from EBCDIC 38xx|
|`IRR 1 G*D4 & 6`|7-bit Spanish with Peseta sign, projected from EBCDIC DP94|
|`IRR ? G*D4 & 7`|7-bit British, projected from EBCDIC DP94|
|`IRR 0 G*D4 & 7`|7-bit British, projected from EBCDIC DCF Migration encoding|
|`IRR 1 G*D4 & 7`|7-bit British, projected from EBCDIC DP94-coördinated WP96|
|`IRR ? G*D4 & 8`|7-bit United States, projected from EBCDIC DP94|
|`IRR 0 G*D4 & 8`|7-bit United States excluding non-ASCII, projected from EBCDIC DP94|
|`IRR 1 G*D4 & 8`|7-bit United States excluding non-ASCII, projected from EBCDIC DP94 for POSIX|
|`IRR 2 G*D4 & 8`|7-bit United States, projected from EBCDIC DP94 for POSIX Open Systems|
|`IRR 3 G*D4 & 8`|7-bit United States, projected from subset of EBCDIC DP94|
|`G*D4 & 9`|MARC-8 subscript numbers|
|`G*D4 & :`|7-bit British, projected from EBCDIC WP96|
|`IRR ? G*D4 & ;`|7-bit Brazilian Portuguese, projected from EBCDIC DP94|
|`IRR 0 G*D4 & ;`|7-bit Brazilian Portuguese, projected from EBCDIC 38xx|
|`IRR ? G*D4 & <`|7-bit Danish and Norwegian, projected from EBCDIC DP94|
|`IRR 0 G*D4 & <`|7-bit Danish and Norwegian with Euro, projected from EBCDIC DP94|
|`IRR ? G*D4 & =`|7-bit Swedish and Finnish, projected from EBCDIC DP94|
|`IRR 0 G*D4 & =`|7-bit Swedish and Finnish with Euro, projected from EBCDIC DP94|
|`G*D4 & >`|7-bit barcode text, projected from EBCDIC|
|`IRR ? G*D4 & ?`|DEC Special Graphics (VT100 version)|
|`IRR 0 G*D4 & ?`|DEC Special Graphics (variant)|
|`IRR 1 G*D4 & ?`|DEC Special Graphics (combined)|
|`G*D4 ' 0`|Right-hand side of single-byte component of IBM 5550 Traditional Chinese encoding|
|`G*D4 ' 1`|Subset of the right-hand sides of IBM-PC code pages, containing only the Ñ/ñ letters|
|`G*D4 ' 2`|ICT 1900 character set, standardised in Poland as PN⁠-⁠T⁠-⁠42109-02-ZU1|
|`G*D4 ' 3`|CENELEC supplementary set for characters in Annex A of T.51 but not in the first 9 parts of ISO 8859: same as `G*D6 N`, but as a 94-character set designatable to G0|
|`G*D4 ' 4`|ISO 10367 box-drawing set: same as `G*D6 Q`, but as a 94-character set designatable to G0|
|`IRR ? G*D4 ' 5`|CCITT Hebrew (letters-only subset of right-hand-side of ISO-8859-8): same as `G*D6 S`, but as a 94-character set designatable to G0|
|`IRR @ G*D4 ' 5`|Right-hand side of 1988 edition of ISO-8859-8 (Hebrew), minus the non-breaking space|
|`IRR A G*D4 ' 5`|Right-hand side of 1999 edition of ISO-8859-8 (Hebrew), minus the non-breaking space|
|`IRR B G*D4 ' 5`|Right-hand side of 2002 edition of SI-1311 (Hebrew), minus the non-breaking space|
|`IRR 0 G*D4 ' 5`|Hebrew with box-drawing characters but without the non-breaking space|
|`G*D4 ' 6`|I.S. 434 charset for Ogham: same as `G*D6 g`, but as a 94-character set designatable to G0|
|`G*D4 ' 7`|7-bit Polish with Euro sign|
|`G*D4 ' 8`|7-bit Afrikaans|
|`IRR ? G*D4 ' 9`|7-bit Czech, projected from EBCDIC WP96|
|`IRR 0 G*D4 ' 9`|7-bit Czech, projected from EBCDIC WP96, small version|
|`G*D4 ' :`|7-bit Slovak, projected from EBCDIC WP96|
|`G*D4 ' ;`|7-bit Dutch, projected from EBCDIC WP96|
|`G*D4 ' <`|7-bit for Hong Kong, projected from EBCDIC WP96|
|`IRR ? G*D4 ' =`|7-bit Romanian, projected from EBCDIC WP96|
|`IRR 0 G*D4 ' =`|7-bit Romanian, projected from EBCDIC WP96, small version|
|`G*D4 ' >`|Set containing only square brackets, projected from EBCDIC WP96 supplementary ranges|
|`G*D4 ' ?`|Set containing only ²/³ superscripts, projected from EBCDIC WP96 supplementary ranges|
|`G*D4 , 0`|Set containing only ½ and ¨, projected from EBCDIC WP96 supplementary ranges|
|`G*D4 , 1`|7-bit Danish and Norwegian, projected from EBCDIC for IBM 3270|
|`G*D4 , 2`|7-bit German, projected from EBCDIC for IBM 3270|
|`G*D4 , 3`|7-bit Spanish, projected from EBCDIC for IBM 3270|
|`G*D4 , 4`|7-bit Swedish and Finnish, projected from EBCDIC for IBM 3270|
|`G*D4 , 5`|7-bit Brazilian Portuguese, projected from EBCDIC WP96|
|`G*D4 , 6`|7-bit Canadian English, projected from EBCDIC WP96|
|`G*D4 , 7`|7-bit Roman, projected from EBCDIC WP96 for Greece|
|`G*D4 , 8`|7-bit Icelandic, projected from EBCDIC WP96|
|`IRR ? G*D4 , 9`|7-bit Roman, projected from EBCDIC WP96 for Japan|
|`IRR 0 G*D4 , 9`|7-bit Roman, projected from EBCDIC WP96 for Japan, small version|
|`G*D4 , :`|7-bit Latin American Spanish, projected from EBCDIC WP96|
|`G*D4 , ;`|7-bit Portugal, projected from EBCDIC WP96|
|`G*D4 , <`|7-bit Spain, projected from EBCDIC WP96|
|`G*D4 , =`|7-bit Swedish and Finnish, projected from EBCDIC WP96|
|`G*D4 , >`|7-bit Swiss French, projected from EBCDIC WP96|
|`G*D4 , ?`|7-bit Swiss German, projected from EBCDIC WP96|
|`G*D4 ! " 0`|7-bit Switzerland, projected from EBCDIC WP96|
|`G*D4 ! " 1`|7-bit Turkish, projected from EBCDIC WP96|
|`G*D4 ! " 2`|7-bit United Kingdom, projected from EBCDIC non-DP94-coördinated WP96|
|`G*D4 ! " 3`|7-bit United States, projected from EBCDIC WP96|
|`IRR ? G*D4 ! " 4`|7-bit United States Accounting B (projected from EBCDIC WP96), extended|
|`IRR 0 G*D4 ! " 4`|7-bit United States Accounting A, projected from EBCDIC WP96|
|`IRR 1 G*D4 ! " 4`|7-bit United States Accounting B, projected from EBCDIC WP96|
|`G*D4 ! " 5`|7-bit United States, projected from EBCDIC code page 2|
|`G*D4 ! " 6`|Technical charset for the IBM 5080, projected from EBCDIC supplementary ranges|
|`G*D4 ! " 7`|Line-drawing set for the IBM 3800, projected from EBCDIC Library Character Set|
|`IRR ? G*D4 ! " 8`|Right-hand side of ISO-8859-7:1987 (Greek) minus non-breaking space|
|`IRR @ G*D4 ! " 8`|Right-hand side of ISO-8859-7:1987 plus Euro sign minus non-breaking space|
|`IRR A G*D4 ! " 8`|Right-hand side of ISO-8859-7:2003 (with Euro and Drachma) minus non-breaking space|
|`IRR 0 G*D4 ! " 8`|Right-hand side of ISO-8859-7:2003 with Euro sign with alternative Unicode mappings (what X11 calls `suneu-greek`), minus non-breaking space|
|`G*D4 ! " 9`|Right-hand side of ISO-8859-6 (Arabic) minus non-breaking space|
|`G*D4 ! " :`|IEC-P-1289 technical set number 1 minus non-breaking space|
|`G*D4 ! " ;`|Right-hand side of ABICOMP encoding for Portuguese in Brazil minus non-breaking space|
|`G*D4 ! " <`|Right-hand side of code page 1133 for Lao, minus non-breaking space|
|`G*D4 ! " =`|Right-hand side of code page 1008 for Arabic, minus non-breaking space|
|`IRR ? G*D4 ! " >`|Right-hand side of code page 5142 for Arabic, minus non-breaking space|
|`IRR 0 G*D4 ! " >`|Right-hand side of code page 1029 for Arabic positional forms, minus non-breaking space|
|`IRR ? G*D4 ! " ?`|0xA0–0xFF region of combined code pages 9056, 13152 and 41824 for Arabic, minus non-breaking space|
|`IRR 0 G*D4 ! " ?`|0xA0–0xFF region of code page 9056 for Arabic, minus non-breaking space|
|`IRR 1 G*D4 ! " ?`|0xA0–0xFF region of code page 13152 for Arabic, minus non-breaking space|
|`IRR 2 G*D4 ! " ?`|0xA0–0xFF region of code page 165 for Arabic positional forms, minus non-breaking space|
|`IRR 3 G*D4 ! " ?`|0xA0–0xFF region of code page 41824 for Arabic, minus non-breaking space|
|`G*D4 ! # 0`|"OT1" (7-bit TeX) charset|
|`IRR ? G*D4 ! # 1`|Left-hand side of LaTeX "Storm" charset|
|`IRR @ G*D4 ! # 1`|Left-hand side of LaTeX "Storm" charset, falling through to "OT1"|
|`G*D4 ! # 2`|Left-hand side of LaTeX "ASEXP" charset (supplementary charset for use with PostScript Standard charset)|
|`G*D4 ! # 3`|Left-hand side of LaTeX "TS1" (text symbols) charset|
|`G*D4 ! # 4`|Left-hand side of LaTeX "LGR" (Greek) charset|
|`G*D4 ! # 5`|Left-hand side of LaTeX "X2" (extended Cyrillic) charset|
|`G*D4 ! # 6`|LaTeX "OT2" (7-bit Cyrillic) charset|
|`G*D4 ! # 7`|Greek G0 set from ETS 300 706|
|`G*D4 ! # 8`|Serbian Cyrillic G0 set from ETS 300 706|
|`G*D4 ! # 9`|Russian and Bulgarian Cyrillic G0 set from ETS 300 706|
|`G*D4 ! # :`|Ukrainian Cyrillic G0 set from ETS 300 706|
|`G*D4 ! # ;`|Arabic G0 set from ETS 300 706|
|`G*D4 ! # <`|Arabic G2 set from ETS 300 706|
|`G*D4 ! # =`|G2 set used with the Greek G0 set, from ETS 300 706|
|`G*D4 ! # >`|Left-hand side of the VNI-for-DOS Vietnamese charset|
|`G*D4 ! # ?`|Right-hand side of the VNI-for-Windows-or-Unix Vietnamese charset|
|`G*D4 ! $ 0`|SPTiberian charset for Biblical Hebrew (modified Michigan-Claremont)|
|`G*D4 ! $ 1`|SPIonic charset for Biblical Greek (modified Thesaurus Linguae Graecae)|
|`IRR ? G*D4 ! $ 2`|SPAchmim charset for Sahidic Coptic (modified Thesaurus Linguae Graecae)|
|`IRR 0 G*D4 ! $ 2`|SPAchmim charset for Sahidic Coptic (modified Thesaurus Linguae Graecae) with a few extensions adapted from the SPIonic charset|
|`G*D4 ! $ 3`|SPCaesarea charset for notational symbols for New Testament textual apparatus|
|`G*D4 ! $ 4`|SPAtlantis charset for romanisations of Middle Eastern languages|
|`G*D4 ! $ 5`|SPEdessa charset for Classical Syriac Aramaic (modified Michigan-Claremont)|
|`G*D4 ! $ 6`|"Bee" charset for the Deseret Alphabet|
|`G*D4 ! $ 7`|Left-hand side of LaTeX "T3" (8-bit phonetic notation) charset|
|`G*D4 ! $ 8`|"Bookshelf Symbol 3" charset for astrological symbols and musical accidentals|
|`G*D4 ! $ 9`|Left-hand side of "Bookshelf Symbol 1" charset for superscripts and extended Latin|
|`G*D4 ! $ :`|Left-hand side of "Bookshelf Symbol 2" charset for subscripts and extended Latin|
|`G*D4 ! $ ;`|Left-hand side of "Bookshelf Symbol 7" charset for extended Latin, musical symbols and assorted Japanese characters|
|`G*D4 ! $ <`|94-character part of the right-hand side of the "Georgian Academy" charset for unicameral Georgian|
|`G*D4 ! $ =`|Lao charset which [X11 calls `mulelao`](https://salsa.debian.org/xorg-team/font/xfonts-encodings)|

## Additional single-byte 96-character G-sets, and additional selectors for particular variants of single-byte 96-character G-sets

|Private assignment|Meaning|
|---|---|
|`IRR ? G*D6 A`|Right-hand side of ISO-8859-1, Western European Roman with `×` and `÷`|
|`IRR 0 G*D6 A`|Right-hand side of ECMA-94:1985, Western European Roman, first revision|
|`IRR 1 G*D6 A`|Right-hand side of ABNT NBR-9611, Western European Roman with `Œ` and `œ`|
|`IRR ? G*D6 B`|Right-hand side of ISO-8859-2, Central European Roman|
|`IRR 0 G*D6 B`|Right-hand side of IBM code page 1111 (ISO-8859-2 with overring replacing degrees sign)|
|`IRR ? G*D6 F`|Right-hand side of ISO-8859-7 for Greek, 1987 version|
|`IRR 0 G*D6 F`|Right-hand side of ISO-8859-7 with Euro sign; intermediate between 1987 and 2003 versions|
|`IRR 1 G*D6 F`|Right-hand side of ISO-8859-7 with alternative Unicode mappings (what X11 calls `suneu-greek`)|
|`IRR ? G*D6 J`|ITU T.51 supplementary set for use with old IRV (excludes universal currency sign and hash)|
|`IRR 0 G*D6 J`|Complete ITU T.51 supplementary set (same as `IRR 0 G*D6 R`; default for this F-byte)|
|`IRR ? G*D6 L`|Right-hand side for ISO-8859-5 for Cyrillic|
|`IRR 0 G*D6 L`|Adaptation of ISO-8859-5 for Ukrainian, as in IBM code page 1124|
|`IRR ? G*D6 M`|Right-hand side for ISO-8859-9 for Turkish|
|`IRR 0 G*D6 M`|Adaptation of ISO-8859-9 with the addition of the schwa letter (Ə/ə) for Azeri use|
|`IRR ? G*D6 R`|ITU T.51 supplementary set for use with ASCII (excludes dollar and hash)|
|`IRR 0 G*D6 R`|Complete ITU T.51 supplementary set (same as `IRR 0 G*D6 J`; default for this F-byte)|
|`IRR ? G*D6 S`|CCITT Hebrew (letters-only subset of right-hand-side of ISO-8859-8); same as `G*D4 ' 5`|
|`IRR 0 G*D6 S`|CCITT Hebrew plus box-drawing characters, as in code page 972|
|`IRR ? G*D6 T`|Thai ISO-8859-11 (TIS-620:1986 plus non-breaking space)|
|`IRR 0 G*D6 T`|Thai ISO-8859-11 with IBM extensions|
|`IRR 1 G*D6 T`|Thai ISO-8859-11 with IBM extensions including the Euro sign|
|`IRR ? G*D6 :`|User-defined (right-hand side of Windows code page 42)|
|`IRR 0 G*D6 :`|User-defined (right-hand side of W3C/WHATWG definition of `x-user-defined`)|
|`G*D6 ! 0`|RFC 1345's so-called ISO-IR-111/ECMA-Cyrillic (incompatible with ISO-IR-111 itself).|
|`G*D6 ! 1`|ITU T.101 Annex C mosaic set 1.|
|`G*D6 ! 2`|Right-hand side of ABICOMP encoding for Portuguese in Brazil.|
|`IRR ? G*D6 ! 3`|Right-hand side of code page 1129 for Vietnamese|
|`IRR 0 G*D6 ! 3`|Right-hand side of code page 1163 for Vietnamese with Euro sign|
|`G*D6 ! 4`|Right-hand side of code page 1133 for Lao|
|`IRR ? G*D6 ! 5`|Right-hand side of code page 922 for Estonian (intermediate between ISO-8859-1 and ISO-8859-13)|
|`IRR 0 G*D6 ! 5`|Right-hand side of code page 902 for Estonian with Euro sign|
|`G*D6 ! 6`|Right-hand side of code page 63283 for Lithuanian|
|`IRR ? G*D6 ! 7`|Right-hand side of code page 1008 for Arabic|
|`IRR 0 G*D6 ! 7`|Right-hand side of code page 5104 for Arabic with Euro sign|
|`G*D6 ! 8`|Right-hand side of code page 1006 for Urdu|
|`IRR ? G*D6 ! 9`|Right-hand side of code page 5142 for Arabic|
|`IRR 0 G*D6 ! 9`|Right-hand side of code page 1029 for Arabic positional forms|
|`IRR ? G*D6 ! <`|0xA0–0xFF region of combined code pages 9056, 13152 and 41824 for Arabic|
|`IRR 0 G*D6 ! <`|0xA0–0xFF region of code page 9056 for Arabic|
|`IRR 1 G*D6 ! <`|0xA0–0xFF region of code page 13152 for Arabic|
|`IRR 2 G*D6 ! <`|0xA0–0xFF region of code page 165 for Arabic positional forms|
|`IRR 3 G*D6 ! <`|0xA0–0xFF region of code page 41824 for Arabic|
|`G*D6 ! =`|Right-hand side of LaTeX "ASEXP" charset (supplementary charset for use with PostScript Standard charset)|
|`G*D6 ! >`|ETS 300 706 G3 Line Drawing set|
|`G*D6 ! ?`|G2 set used with the Cyrillic G0 sets, from ETS 300 706|
|`G*D6 " 0`|LaTeX "TS3" (supplementary phonetic notation) charset (0x20–0x7F subset)|
|`G*D6 " 1`|Korean N-byte Hangul Code (KS C 5601:1974) with IBM extensions|
|`G*D6 " ?`|DEC 8-bit Greek, right-hand side with non-breaking space|
|`G*D6 % 0`|DEC 8-bit Turkish, right-hand side with non-breaking space|
|`IRR ? G*D6 $ 7`|Symbol font encoding, GR range (with euro)|
|`IRR 0 G*D6 $ 7`|Symbol font encoding, GR range (with figure space)|
|`G*D6 ' 0`|Right-hand side of single-byte component of IBM 5550 Simplified Chinese (extended `Shift_GB`) encoding|
|`G*D6 ! # 3`|Left-hand side of LaTeX "TS1" (text symbols) charset|
|`G*D6 ! $ 7`|Left-hand side of LaTeX "T3" (8-bit phonetic notation) charset|
|`G*D6 ! $ <`|96-character part of the right-hand side of the "Georgian Academy" charset for unicameral Georgian|

## Additional multiple-byte G-sets, and additional selectors for particular variants of multiple-byte G-sets

|Private assignment|Meaning|
|---|---|
|`IRR ? G*DM4 @`|JIS C 6226-1978, with mappings for characters changed to those suitable for the 1978 edition|
|`IRR 0 G*DM4 @`|JIS C 6226, version encoded by IBM-932 and IBM-942|
|`IRR 1 G*DM4 @`|JIS C 6226, version used by NEC PC98 (default for this F-byte)|
|`IRR 2 G*DM4 @`|JIS C 6226-1978, character mapping changes by 90JIS pivot only|
|`IRR 3 G*DM4 @`|JIS C 6226-1978, character mappings by CID map only, resulting in some gaps (since CID maps are intended to preserve font correctness, not data integrity)|
|`IRR ? G*DM4 A`|GB/T 2312-1980|
|`IRR 0 G*DM4 A`|GB/T 12345 (hybrid approach)|
|`IRR 1 G*DM4 A`|GB 18030-2000 levels 1 and 2|
|`IRR 2 G*DM4 A`|GB 18030-2005 levels 1 and 2|
|`IRR 3 G*DM4 A`|GB 18030-2022 levels 1 and 2 (default)|
|`IRR 4 G*DM4 A`|GB 18030, favouring duplicate mappings over PUA mappings for standard characters|
|`IRR 5 G*DM4 A`|GB/T 2312, variant used on classic Mac OS, updated mappings|
|`IRR 6 G*DM4 A`|GB/T 2312-1980, UTC version|
|`IRR 7 G*DM4 A`|GB/T 2312-1980, with alterations but not extensions from GB 6345.1-1986|
|`IRR 8 G*DM4 A`|GB/T 12345 (strict compliance, including retaining certain simplified characters from GB/T 2312 which are often implemented replaced by traditional versions)|
|`IRR 9 G*DM4 A`|GB/T 12345 (UTC mapping, including additional replacements by traditional versions, and lacking non‑hanzi not present in GB/T 2312)|
|`IRR : G*DM4 A`|GB/T 2312, IBM version with PUA filling empty space and extensions in row 94|
|`IRR ; G*DM4 A`|GB/T 2312, variant used on classic Mac OS, as specified by Apple|
|`IRR < G*DM4 A`|GB/T 2312, variant used on classic Mac OS, mixed mappings|
|`IRR = G*DM4 A`|GB/T 2312, Microsoft version|
|`IRR > G*DM4 A`|GB/T 12345, including what Unihan calls the "Pseudo-GB1" extensions|
|`IRR ? G*DM4 B`|JIS C 6226 / X 0208-1983|
|`IRR @ G*DM4 B`|JIS X 0208-1990 (standard sequence, listed here for completeness)|
|`IRR 0 G*DM4 B`|JIS X 0208, WHATWG variant (default; synchronised with Windows-31J)|
|`IRR 1 G*DM4 B`|JIS X 0208, "KanjiTalk 7" (row+84 verticals, non-NEC gaiji) variant used on classic Mac OS, updated mappings|
|`IRR 2 G*DM4 B`|JIS X 0208, "PostScript" / "KanjiTalk 6 PostScript" (row+84 verticals, NEC gaiji) variant used on classic Mac OS, updated mappings|
|`IRR 3 G*DM4 B`|JIS X 0208, "KanjiTalk 6 non-PostScript" (row+10 verticals, NEC gaiji) variant used on classic Mac OS|
|`IRR 4 G*DM4 B`|JIS X 0208, with UTC-style mapping of em dash / horizontal bar character|
|`IRR 5 G*DM4 B`|JIS X 0208, Open Group version for JIS-Roman based EUC-JP|
|`IRR 6 G*DM4 B`|JIS X 0208, Open Group version for ASCII-based EUC-JP|
|`IRR 7 G*DM4 B`|JIS X 0208, Open Group version for Microsoft-style EUC-JP|
|`IRR 8 G*DM4 B`|JIS X 0208, version encoded by IBM-954|
|`IRR 9 G*DM4 B`|JIS X 0208, DoCoMo JIS emoji|
|`IRR : G*DM4 B`|JIS X 0208, KDDI JIS emoji, symbolic zodiac variant|
|`IRR ; G*DM4 B`|JIS X 0208, SoftBank JIS emoji|
|`IRR < G*DM4 B`|JIS X 0208, KDDI JIS emoji, pictorial zodiac variant|
|`IRR = G*DM4 B`|JIS X 0208, Fujitsu version|
|`IRR > G*DM4 B`|JIS X 0208, ARIB STD-B.24 version|
|`IRR ! 0 G*DM4 B`|JIS X 0208, using later-disunified Unicode codepoints with closer (other-source) glyphs|
|`IRR SP 0 G*DM4 B`|"KanjiTalk 7" variant (row+84 verticals, non-NEC gaiji) used on classic Mac OS, Apple mappings|
|`IRR SP 1 G*DM4 B`|"PostScript" / "KanjiTalk 6 PostScript" variant (row+84 verticals, NEC gaiji) used on classic Mac OS, Apple mappings|
|`IRR ? G*DM4 C`|KS C 5601-1987 Wansung code, using new-UTC mappings (harmonious with Microsoft and WHATWG)|
|`IRR 0 G*DM4 C`|KS C 5601-1987, but using old-UTC mappings for the non-syllables|
|`IRR 1 G*DM4 C`|KS X 1001-1998 Wansung code. The Euro sign update, also adding the registered trademark sign, and matching the WHATWG mapping.|
|`IRR 2 G*DM4 C`|KS X 1001-2002 (adding the South Korean postal mark)|
|`IRR 3 G*DM4 C`|KS X 1001-1987 extended, main plane of Apple/Elex extension (HangulTalk), updated mappings|
|`IRR 4 G*DM4 C`|KS X 1001-1987, using IBM mappings|
|`IRR 5 G*DM4 C`|KS X 1001-1987 extended, main plane of Apple/Elex extension (HangulTalk), old Apple mappings|
|`IRR 6 G*DM4 C`|KS X 1001-1987 extended, main plane of Apple/Elex extension (HangulTalk), Apple mappings|
|`IRR 7 G*DM4 C`|KS X 1001-2002, updated mappings from Unihan database|
|`IRR 8 G*DM4 C`|KS X 1001-2002, updated mappings from Unihan database, plus the changes implied by [the feedback to IRGN2298](https://www.unicode.org/irg/docs/n2298r-IICoreChanges.pdf#page=6)|
|`IRR ? G*DM4 D`|JIS X 0212:1990|
|`IRR 0 G*DM4 D`|JIS X 0212 with va/vi/ve/vo|
|`IRR 1 G*DM4 D`|JIS X 0212, Open Group version for JIS-Roman based EUC-JP|
|`IRR 2 G*DM4 D`|JIS X 0212, Open Group version for ASCII-based EUC-JP|
|`IRR 3 G*DM4 D`|JIS X 0212, Open Group version for Microsoft-style EUC-JP|
|`IRR 4 G*DM4 D`|JIS X 0212, version encoded by IBM-954|
|`IRR 5 G*DM4 D`|JIS X 0212, version encoded by ICU's EUC-JP|
|`IRR 6 G*DM4 D`|JIS X 0212, using later-disunified Unicode codepoints with closer (other-source) glyphs (see [IRGN2722](https://www.unicode.org/irg/docs/n2722-JSourceIssues.pdf)&rpar;|
|`IRR ? G*DM4 E`|CCITT Hanzi Code (GB 2312 variant) from ITU T.101-C, which bases it on GB 6345.1-1986 and GB 8565.2-1988 with further adjustments and expansions|
|`IRR 0 G*DM4 E`|CCITT Hanzi Code, with a more conventional mapping of the lowercase gs (appropriate for their GB 18030 reference glyphs)|
|`IRR 1 G*DM4 E`|CCITT Hanzi Code, combined with an additional hanzi extension in row 8|
|`IRR 2 G*DM4 E`|GB 6345.1-1986|
|`IRR 3 G*DM4 E`|GB 8565.2-1988|
|`IRR 4 G*DM4 E`|Pseudo-G8, an incorrect version of GB 8565.2-1988 which had been referenced by older versions of the Unihan database (incorrectly shifts the actual GB 8565.2 characters 15-90 through 15-93 back by one code point over 15-89, and also includes the row 8 hanzi extensions and most of the CCITT hanzi extensions).|
|`IRR 5 G*DM4 E`|GB 8565.2-1988 with those of the GB 15564-1995 extensions (intended for Hong Kong teletext) that are listed in the Unihan database|
|`IRR 0 G*DM4 G`|CNS 11643 plane 1, recommended version (default)|
|`IRR 1 G*DM4 G`|CNS 11643 plane 1, mapped from Microsoft Big-5|
|`IRR 2 G*DM4 G`|CNS 11643 plane 1, according to UTC mappings|
|`IRR 3 G*DM4 G`|CNS 11643 plane 1, mapped from UTC Big-5|
|`IRR 4 G*DM4 G`|CNS 11643 plane 1, mapped from Macintosh-compatible Big-5|
|`IRR 5 G*DM4 G`|CNS 11643 plane 1, as officially defined in Taiwan|
|`IRR 6 G*DM4 G`|CNS 11643 plane 1, an IBM-related variant|
|`IRR 7 G*DM4 G`|CNS 11643 plane 1, mapped from IBM Big-5|
|`IRR 8 G*DM4 G`|CNS 11643 plane 1, mapped from IBM's Microsoft-style Big-5|
|`IRR 9 G*DM4 G`|CNS 11643 plane 1, mapped from WHATWG/HTML5 Big-5|
|`IRR : G*DM4 G`|CNS 11643 plane 1, mapped from Mozilla Big-5|
|`IRR ; G*DM4 G`|CNS 11643 plane 1, per ICU ISO-2022-CN mappings|
|`IRR < G*DM4 G`|CNS 11643 plane 1, per ICU EUC-TW 2014 mappings|
|`IRR = G*DM4 G`|CNS 11643 plane 1, per Yasuoka's mappings|
|`IRR > G*DM4 G`|CNS 11643 plane 1, alternative mappings for HKSCS-2016 preferred forms|
|`IRR ? G*DM4 H`|CNS 11643 plane 2|
|`IRR 1 G*DM4 H`|CNS 11643 plane 2, Big5 mappings|
|`IRR 5 G*DM4 H`|CNS 11643 plane 2, Unihan mappings|
|`IRR 6 G*DM4 H`|CNS 11643 plane 2, alternative mappings for HKSCS-2016 preferred forms|
|`IRR ? G*DM4 I`|CNS 11643-1992 plane 3|
|`IRR 0 G*DM4 I`|CNS 11643-1988 plane 14|
|`IRR 1 G*DM4 I`|CNS 11643-1988 plane 14 with extensions, as submitted to the IRG|
|`IRR 2 G*DM4 I`|CNS 11643-2007 plane 3, as officially defined in Taiwan as of 2019|
|`IRR 3 G*DM4 I`|CNS 11643-2007 plane 3, plus the additional assignments from CNS 11643-1988 plane 14 (default)|
|`IRR 4 G*DM4 I`|CNS 11643-1988 plane 14, UTC mappings (partial, with extensions)|
|`IRR 5 G*DM4 I`|CNS 11643-1992 plane 3, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 6 G*DM4 I`|CNS 11643-1992 plane 3, per ICU EUC-TW 2014 mappings|
|`IRR 7 G*DM4 I`|CNS 11643-1992 plane 3, per Yasuoka's mappings|
|`IRR 8 G*DM4 I`|CNS 11643-1992 plane 3, per Unihan mappings|
|`IRR 9 G*DM4 I`|CNS 11643-1992 plane 3, as officially defined in Taiwan as of 2025|
|`IRR ? G*DM4 J`|CNS 11643-1992 plane 4|
|`IRR 0 G*DM4 J`|CNS 11643-1992 plane 4, as officially defined in Taiwan as of 2019|
|`IRR 1 G*DM4 J`|CNS 11643-1992 plane 4, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 J`|CNS 11643-1992 plane 4, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 J`|CNS 11643-1992 plane 4, per Yasuoka's mappings|
|`IRR 4 G*DM4 J`|CNS 11643-1992 plane 4, per Unihan mappings|
|`IRR 5 G*DM4 J`|CNS 11643-1992 plane 4, as officially defined in Taiwan as of 2025|
|`IRR ? G*DM4 K`|CNS 11643-1992 plane 5|
|`IRR 0 G*DM4 K`|CNS 11643-1992 plane 5, as officially defined in Taiwan as of 2019|
|`IRR 1 G*DM4 K`|CNS 11643-1992 plane 5, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 K`|CNS 11643-1992 plane 5, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 K`|CNS 11643-1992 plane 5, per Yasuoka's mappings|
|`IRR 4 G*DM4 K`|CNS 11643-1992 plane 5, per Unihan mappings|
|`IRR 5 G*DM4 K`|CNS 11643-1992 plane 5, as officially defined in Taiwan as of 2025|
|`IRR ? G*DM4 L`|CNS 11643-1992 plane 6|
|`IRR 0 G*DM4 L`|CNS 11643-1992 plane 6, as officially defined in Taiwan as of 2019|
|`IRR 1 G*DM4 L`|CNS 11643-1992 plane 6, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 L`|CNS 11643-1992 plane 6, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 L`|CNS 11643-1992 plane 6, per Yasuoka's mappings|
|`IRR 4 G*DM4 L`|CNS 11643-1992 plane 6, per Unihan mappings|
|`IRR 5 G*DM4 L`|CNS 11643-1992 plane 6, as officially defined in Taiwan as of 2025|
|`IRR ? G*DM4 M`|CNS 11643-1992 plane 7|
|`IRR 0 G*DM4 M`|CNS 11643-1992 plane 7, as officially defined in Taiwan as of 2019|
|`IRR 1 G*DM4 M`|CNS 11643-1992 plane 7, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 M`|CNS 11643-1992 plane 7, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 M`|CNS 11643-1992 plane 7, per Yasuoka's mappings|
|`IRR 4 G*DM4 M`|CNS 11643-1992 plane 7, per Unihan mappings|
|`IRR 5 G*DM4 M`|CNS 11643-1992 plane 7, as officially defined in Taiwan as of 2025|
|`IRR ? G*DM4 N`|KPS 9566-97|
|`IRR 0 G*DM4 N`|KPS 9566-2003 (only the main plane unless in the UHC DOCS)|
|`IRR 1 G*DM4 N`|KPS 9566-2011 (only the main plane unless in the UHC DOCS)|
|`IRR 2 G*DM4 N`|All KPS 9566 editions overlayed (but only the main plane unless in the UHC DOCS)|
|`IRR ? G*DM4 Q`|JIS X 0213 plane 1, 2004 edition|
|`IRR 0 G*DM4 Q`|JIS X 0213 plane 1, using later-disunified Unicode codepoints with closer (other-source) glyphs|
|`G*D4 :`|User-defined (plane 12 from IBM's version of EUC-TW)|
|`G*DM4 ! 0`|GB/T 12052 (Korean in Mainland China)|
|`IRR ? G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (recommended version)|
|`IRR 0 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (ICU EUC-2014 version)|
|`IRR 1 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (Microsoft version)|
|`IRR 2 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (Apple version)|
|`IRR 3 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (as officially defined in Taiwan as of 2019)|
|`IRR 4 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (old ICU version)|
|`IRR 5 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (IBM version)|
|`IRR 6 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (Yasuoka version)|
|`IRR 7 G*DM4 ! 1`|Planes 2 and up of CNS 11643 as a 94^3 set, as included by IBM EUC-TW as its G2 set (ICU EUC-2014 version)|
|`IRR 8 G*DM4 ! 1`|Planes 2 and up of CNS 11643 as a 94^3 set, as included by IBM EUC-TW as its G2 set (IBM version)|
|`IRR 9 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, following the Unihan database (thus excluding non-hanzi)|
|`IRR : G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, including some highly approximate Unicode mappings|
|`IRR ; G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (as officially defined in Taiwan as of 2025)|
|`IRR < G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, including a somewhat smaller number of rather approximate Unicode mappings|
|`IRR ? G*DM4 ! 2`|MS-950 Big-5 extensions (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR @ G*DM4 ! 2`|Big5-2003 extension set (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR A G*DM4 ! 2`|Big5-ETEN extension set (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR B G*DM4 ! 2`|Hong Kong GCCS extension set (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR C G*DM4 ! 2`|Hong Kong Supplementary Character Set 1999 extension set (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR D G*DM4 ! 2`|Hong Kong Supplementary Character Set 2001 extension set (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR E G*DM4 ! 2`|Hong Kong Supplementary Character Set 2004 extension set (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR F G*DM4 ! 2`|Hong Kong Supplementary Character Set full (GCCS + 2008) extension set (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR G G*DM4 ! 2`|Hong Kong Supplementary Character Set full (GCCS + 2008) extension set, with some mappings updated due to disunifications within Unicode (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR 0 G*DM4 ! 2`|IBM Big-5 ETEN-based in-plane extensions (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR 1 G*DM4 ! 2`|Big5-ETEN with the subset of GCCS encoded with lead bytes following, not preceeding, the standard Big-5 assignments (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR ? G*DM4 ! 3`|Non-ETEN Big5 kana and Cyrillic (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere)|
|`IRR @ G*DM4 ! 3`|Non-ETEN Big5 kana and Cyrillic (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere) combined with Microsoft non-EUDC extensions, as in Python's built-in `"cp950"` Windows codepage implementation.|
|`IRR ? G*DM4 ! 4`|IBM extensions for Shift\_JIS (accepted by Shift\_JIS filter in G3 slot, mapped to/from Shift\_JIS by the same mapping scheme as JIS X 0213 plane 2); excluding UDC|
|`IRR @ G*DM4 ! 4`|IBM extensions for Shift\_JIS (accepted by Shift\_JIS filter in G3 slot, mapped to/from Shift\_JIS by the same mapping scheme as JIS X 0213 plane 2); including UDC|
|`IRR 0 G*DM4 ! 4`|IBM extensions for Shift\_JIS (accepted by Shift\_JIS filter in G3 slot, mapped to/from Shift\_JIS by the same mapping scheme as JIS X 0213 plane 2); old mappings for use with 78JIS|
|`G*DM4 ! 5`|DoCoMo Emoji extensions for Shift\_JIS (as above)|
|`IRR ? G*DM4 ! 6`|KDDI Emoji extensions for Shift\_JIS (as above), pictorial zodiac variant|
|`IRR 0 G*DM4 ! 6`|KDDI Emoji extensions for Shift\_JIS (as above), symbolic zodiac variant|
|`G*DM4 ! 7`|SoftBank Emoji extensions for Shift\_JIS (as above)|
|`IRR ? G*DM4 ! 8`|Currently same as `IRR 1 G*DM4 ! 8` but may change in future.|
|`IRR 0 G*DM4 ! 8`|Modified GB/T 7589 (supplementary simplified), variant projected from GB/T 13131 with deviations from the GB/T 7589-1987 sequence retained per [IRGN2376](https://www.unicode.org/irg/docs/n2376-GSourceUpdate.pdf).|
|`IRR 1 G*DM4 ! 8`|GB/T 13131 (supplementary traditional), with deviations from the GB/T 7589-1987 sequence retained per [IRGN2376](https://www.unicode.org/irg/docs/n2376-GSourceUpdate.pdf).|
|`IRR 2 G*DM4 ! 8`|GB/T 7589 (supplementary simplified), 1987 edition.|
|`IRR 3 G*DM4 ! 8`|GB/T 13131 (supplementary traditional), without deviations from the GB/T 7589-1987 sequence (as highlighted in [IRGN2302](https://www.unicode.org/irg/docs/n2302-GSourceIssues.pdf)&rpar;.|
|`IRR ? G*DM4 ! 9`|Currently same as `IRR 1 G*DM4 ! 9` but may change in future.|
|`IRR 0 G*DM4 ! 9`|GB/T 7590 (further supplementary simplified), variant projected from GB/T 13132 with deviations from the GB/T 7590-1987 sequence retained per [IRGN2376](https://www.unicode.org/irg/docs/n2376-GSourceUpdate.pdf).|
|`IRR 1 G*DM4 ! 9`|GB/T 13132 (further supplementary traditional), with deviations from the GB/T 7590-1987 sequence retained per [IRGN2376](https://www.unicode.org/irg/docs/n2376-GSourceUpdate.pdf).|
|`IRR 2 G*DM4 ! 9`|GB/T 7590 (further supplementary simplified), 1987 edition.|
|`IRR 3 G*DM4 ! 9`|GB/T 13132 (further supplementary traditional) without deviations from the GB/T 7590-1987 sequence (of which most, but not all, are highlighted in [IRGN2302](https://www.unicode.org/irg/docs/n2302-GSourceIssues.pdf)&rpar;.|
|`IRR ? G*DM4 ! :`|HangulTalk second plane (accepted by HangulTalk filter in G3 slot), Apple mappings|
|`IRR 0 G*DM4 ! :`|HangulTalk second plane (accepted by HangulTalk filter in G3 slot), updated mappings (recommended; default)|
|`IRR 1 G*DM4 ! :`|HangulTalk second plane (accepted by HangulTalk filter in G3 slot), marginally newer (but not *that* up-to-date) Apple mappings given by Apple in mapping file comments|
|`IRR 2 G*DM4 ! :`|HangulTalk second plane (accepted by HangulTalk filter in G3 slot), old Apple mappings|
|`IRR 3 G*DM4 ! :`|HangulTalk second plane (accepted by HangulTalk filter in G3 slot), Adobe CID mappings (very partial)|
|`IRR 4 G*DM4 ! :`|HangulTalk second plane (accepted by HangulTalk filter in G3 slot), mappings taking advantage of the PUA of the Nishiki-teki font where possible|
|`G*DM4 ! ;`|Non-syllable part of KPS 9566-2011 outside the main plane (accepted by UHC filter in G3 slot)|
|`G*DM4 ! <`|Big5-E extensions (for Big-5 filter's G3 slot)|
|`G*DM4 ! =`|KS X 1002 (South Korean first supplementary plane)|
|`G*DM4 ! >`|KS X 1027-1 (South Korean second supplementary plane)|
|`G*DM4 ! ?`|KS X 1027-2 (South Korean third supplementary plane)|
|`IRR ? G*DM4 " 0`|Big5 ChinaSea extensions (for Big-5 filter's G3 slot), Unicode-At-On 2.41 variant|
|`IRR 0 G*DM4 " 0`|Big5 ChinaSea extensions (for Big-5 filter's G3 slot), Unicode-At-On 2.50 variant|
|`IRR 1 G*DM4 " 0`|Big5 ChinaSea extensions (for Big-5 filter's G3 slot), core subset|
|`IRR 2 G*DM4 " 0`|Big5 ChinaSea extensions (for Big-5 filter's G3 slot), 黑體 variant|
|`IRR ? G*DM4 " 1`|IBM-926 (IBM-944)'s 94×94 plane (not KS X 1001 compatible for the most part).&ensp;No DOCS filter exists for it yet though.&ensp;Reconstructed original version.|
|`IRR @ G*DM4 " 1`|IBM-926 (IBM-944)'s 94×94 plane (not KS X 1001 compatible for the most part).&ensp;No DOCS filter exists for it yet though.|
|`IRR 0 G*DM4 " 1`|IBM-926 (IBM-944)'s 94×94 plane (not KS X 1001 compatible for the most part).&ensp;No DOCS filter exists for it yet though.&ensp;IBM mappings including corporate PUA.|
|`IRR ? G*DM4 " 2`|GB 16500 (yet another supplementary set, numbered the seventh in its title though Unihan calls it "GE").|
|`IRR @ G*DM4 " 2`|Extended GB 16500 combined with "General Purpose Hanzi" (do not overlap, both are plane "7").|
|`IRR 0 G*DM4 " 2`|"General Purpose Hanzi" (a small supplement of fewer than 200 characters for use alongside GBs 2312, 7589 and 7590 for Simplified Chinese).|
|`IRR 1 G*DM4 " 2`|Extended GB 16500 without the "General Purpose Hanzi" extension.|
|`G*DM4 " 3`|Big5 DynaLab extensions (for Big-5 filter's G3 slot)|
|`G*DM4 " 4`|Big5 Monotype extensions (for Big-5 filter's G3 slot)|
|`G*DM4 " 5`|Big5-Plus in-plane extensions (for Big-5 filter's G3 slot)|
|`G*DM4 " 6`|Big5-Plus out-of-plane extensions (not currently usable as such)|
|`G*DM4 " 7`|IBM Big5 non-ETEN out-of-plane extensions (not currently usable as such)|
|`IRR ? G*DM4 " 8`|SJ 11239 (yet another supplementary set but labelled SJ rather than GB; numbered the eighth in its title)|
|`IRR 0 G*DM4 " 8`|SJ 11239 making use of the BabelStone Han PUA|
|`G*DM4 " 9`|"Unified Japanese IT Vendors Contemporary Ideographs, 1993", essentially a third JIS plane|
|`IRR ? G*DM4 " :`|TCVN 5773:1993 (Chữ Nôm)|
|`IRR @ G*DM4 " :`|TCVN 5773:1993 combined with TCVN 6056:1995, and VHN 01:1998 up to row 94|
|`IRR ? G*DM4 " ;`|TCVN 6056:1995 (Chữ Hán).&ensp;Consists of some characters that are not present in TCVN 5773, all of which are present in (and presumably selected from) the original Unicode URO, and which include many very common Chinese characters; the rows used by TCVN 5773 are not used, so that the two can be combined.&ensp;This may or may not have anything to do with TCVN 6909:2001.|
|`IRR @ G*DM4 " ;`|TCVN 6056:1995 combined with TCVN 5773:1993, and VHN 01:1998 up to row 94 (same as `IRR @ G*DM4 " :`)|
|`G*DM4 " <`|An offsetting of VHN 01:1998 (Hán Nôm, first supplement) with all allocations moved backward by 19 rows so as to fit within a 94×94 plane (VHN 01:1998 itself doesn't use the rows used by either TCVN 5773 or TCVN 6909 and, consequently, does not otherwise fit within the 94×94 plane).&ensp;This may or may not have anything to do with TCVN 6909:2001.|
|`IRR ? G*DM4 " =`|VHN 02:1998 (Hán Nôm, second supplement).&ensp;This may or may not have anything to do with TCVN 6909:2001.|
|`IRR @ G*DM4 " =`|VHN 02:1998 combined with "Hán Nôm Coded Character Repertoire 2007" (which does not use the rows used by VHN 02:1998, so the two can be combined), and a transformation of VHN 01:1998 rows 95 and up (based on a reverse of the transform applied to JIS X 0213 plane 2 in `Shift_JISx0213`).|
|`G*DM4 " >`|"Hán Nôm Coded Character Repertoire 2007" (Hán Nôm, third supplement)|
|`G*DM4 " ?`|The extension plane 13 that appears in IBM's EUC-TW variant|
|`IRR ? G*DM4 # 0`|CNS 11643-2007 plane 8|
|`IRR 0 G*DM4 # 0`|CNS 11643-2007 plane 8 (as officially defined in Taiwan as of 2019)|
|`IRR 1 G*DM4 # 0`|CNS 11643-2007 plane 8 (as officially defined in Taiwan as of 2025)|
|`IRR ? G*DM4 # 1`|CNS 11643-2007 plane 9|
|`IRR 0 G*DM4 # 1`|CNS 11643-2007 plane 9 (as officially defined in Taiwan as of 2019)|
|`IRR 1 G*DM4 # 1`|CNS 11643-2007 plane 9 (as officially defined in Taiwan as of 2025)|
|`IRR ? G*DM4 # 2`|CNS 11643-2007 plane 10|
|`IRR 0 G*DM4 # 2`|CNS 11643-2007 plane 10 (as officially defined in Taiwan as of 2019)|
|`IRR ? G*DM4 # 3`|CNS 11643-2007 plane 11|
|`IRR 0 G*DM4 # 3`|CNS 11643-2007 plane 11 (as officially defined in Taiwan as of 2019)|
|`IRR 1 G*DM4 # 3`|CNS 11643-2007 plane 11 (as officially defined in Taiwan as of 2025)|
|`IRR ? G*DM4 # 4`|CNS 11643-2007 plane 12|
|`IRR 0 G*DM4 # 4`|CNS 11643-2007 plane 12 (as officially defined in Taiwan as of 2019)|
|`IRR 1 G*DM4 # 4`|CNS 11643-2007 plane 12 (as officially defined in Taiwan as of 2025)|
|`IRR ? G*DM4 # 5`|CNS 11643-2007 plane 13|
|`IRR 0 G*DM4 # 5`|CNS 11643-2007 plane 13 (as officially defined in Taiwan as of 2019)|
|`IRR 1 G*DM4 # 5`|CNS 11643-2007 plane 13 (as officially defined in Taiwan as of 2025)|
|`IRR ? G*DM4 # 6`|CNS 11643-2007 plane 14|
|`IRR 0 G*DM4 # 6`|CNS 11643-2007 plane 14 (as officially defined in Taiwan as of 2019)|
|`IRR 1 G*DM4 # 6`|CNS 11643-2007 plane 14 (as officially defined in Taiwan as of 2025)|
|`IRR ? G*DM4 # 7`|CNS 11643 plane 15|
|`IRR 0 G*DM4 # 7`|CNS 11643 plane 15 (as officially defined in Taiwan as of 2019)|
|`IRR 1 G*DM4 # 7`|CNS 11643 plane 15 (following "plane 9" of the 2000 ICU data)|
|`IRR 2 G*DM4 # 7`|CNS 11643 plane 15 (following 2014 ICU data)|
|`IRR 4 G*DM4 # 7`|CNS 11643 plane 15 (following Unihan data)|
|`IRR 5 G*DM4 # 7`|CNS 11643 plane 15 (as officially defined in Taiwan as of 2025)|
|`G*DM4 # 9`|CNS 11643 plane 17|
|`G*DM4 # ;`|CNS 11643 plane 19|
|`G*DM4 % 0`|The IRG/Unihan source described only as "Singapore Characters"|
|`G*DM4 % 1`|Re-arrangement of TCVN 6056 (Chữ Hán), as was referenced by the Unicode 3.0 Unihan database|
|`G*DM4 % 2`|"Data Statistics Table of Hanzi not included in GB 2312", as converted into a 94×94 set in [IRGN2808](https://www.unicode.org/irg/docs/n2808-GSourceChanges.pdf)|
|`G*DM4 % 3`|The Han'yō Denshi Programme's "IB" charset for characters from names of persons or places|
|`G*DM4 % 4`|The Han'yō Denshi Programme's "FT" charset for characters from the Font Development and Promotion Center (FDPC)|
|`G*DM4 % 5`|The Han'yō Denshi Programme's "HG" charset for additional characters from the Heisei Minchō font|
|`IRR ? G*DM6 ! 0`|GBK extras per GB 18030-2000 or GB 18030-2005 (GBK level 5 with associated UDC zone and non-URO part of level 4; accepted by GBK filter in G3 slot)|
|`IRR 0 G*DM6 ! 0`|GBK extras, WHATWG/HTML5 variant|
|`IRR 1 G*DM6 ! 0`|GBK extras, mapping all characters with defined glyphs to non-PUA|
|`IRR 2 G*DM6 ! 0`|GBK extras per GB 18030-2022|
|`IRR ? G*DM6 ! 1`|EACC / CCCII, Library of Congress version|
|`IRR 0 G*DM6 ! 1`|EACC / CCCII, Koha Taiwan version|
|`IRR 1 G*DM6 ! 1`|EACC / CCCII, Hong Kong Innovative Users Group / Hong Kong University version|
|`IRR 2 G*DM6 ! 1`|EACC / CCCII, aggregate version with Taiwan layout of row 2, favouring Unihan kCCCII for kanji mappings (default)|
|`IRR 3 G*DM6 ! 1`|EACC / CCCII, aggregate version with Hong Kong layout of rows 0–2, favouring Library of Congress for kanji mappings|

## "Plain extended ASCII" mode

Plain extended ASCII mode is switched to by `DOCS 3` as 
mentioned above.&ensp;Once inside, [the DEC-defined DECSPPCS control
sequence](https://vt100.net/docs/vt510-rm/DECSPPCS.html) (i.e. `CSI … * p`) is
used for switching between numbered code pages (e.g. `CSI 1 2 5 2 * p`).&ensp;Numbers above 65535
are used for custom purposes.&ensp;Specifically:

|Private assignment|Meaning|
|---|---|
|`ESC [ 9 9 4 0 0 3 * p`|Switch to the "Hankaku" encoding: an extension of 8-bit JIS X 0201 adding Hiragana.|
|`ESC [ 9 9 4 0 0 5 * p`|Switch to the "WP-Symbol" (presumably, "word processor symbols") encoding.|
|`ESC [ 9 9 5 0 0 1 * p`|Switch to the Bookshelf Symbol 1 (superscripts and extended Latin) encoding.|
|`ESC [ 9 9 5 0 0 2 * p`|Switch to the Bookshelf Symbol 2 (subscripts and extended Latin) encoding.|
|`ESC [ 9 9 5 0 0 7 * p`|Switch to the Bookshelf Symbol 7 (extended Latin, musical symbols and assorted Japanese characters) encoding.|
|`ESC [ 9 9 6 1 1 0 * p`|Switch to the Cork (LaTeX Extended Latin) encoding.|
|`ESC [ 9 9 6 1 1 1 * p`|Switch to an old version of the Cork (LaTeX Extended Latin) encoding.|
|`ESC [ 9 9 6 1 1 2 * p`|Switch to a variant of the Cork (LaTeX Extended Latin) encoding.|
|`ESC [ 9 9 6 1 2 1 * p`|Switch to the T2A (LaTeX Cyrillic) encoding.|
|`ESC [ 9 9 6 1 2 2 * p`|Switch to the T2B (LaTeX Cyrillic) encoding.|
|`ESC [ 9 9 6 1 2 3 * p`|Switch to the T2C (LaTeX Cyrillic) encoding.|
|`ESC [ 9 9 6 1 3 0 * p`|Switch to the T3 (LaTeX 8-bit phonetic notation) encoding.|
|`ESC [ 9 9 6 1 4 0 * p`|Switch to the T4 (LaTeX African Latin) encoding.|
|`ESC [ 9 9 6 1 5 0 * p`|Switch to the T5 (LaTeX Vietnamese) encoding.|
|`ESC [ 9 9 6 2 1 0 * p`|Switch to the TS1 (LaTeX Text Symbols) encoding.|
|`ESC [ 9 9 6 2 3 0 * p`|Switch to the TS3 (LaTeX supplementary phonetic notation) charset over the 0x80–0xFF range.|
|`ESC [ 9 9 6 3 2 0 * p`|Switch to the X2 (LaTeX comprehensive Cyrillic) encoding.|
|`ESC [ 9 9 6 7 2 0 * p`|Switch to the OT2 (LaTeX 7-bit Cyrillic) encoding.|
|`ESC [ 9 9 6 7 2 1 * p`|Switch to a combination of ASCII with the OT2 (LaTeX 7-bit Cyrillic) encoding.|
|`ESC [ 9 9 6 7 3 0 * p`|Switch to the OT3 (LaTeX 7-bit phonetic notation) encoding.|
|`ESC [ 9 9 6 7 4 0 * p`|Swith to the OT4 (LaTeX Polish) encoding.|
|`ESC [ 9 9 6 7 4 1 * p`|Swith to the QX (LaTeX Polish, Extended) encoding.|
|`ESC [ 9 9 6 7 4 2 * p`|Swith to the RM (LaTeX Polish, Extended) encoding.|
|`ESC [ 9 9 6 8 1 2 * p`|Switch to the OML (LaTeX Mathematical Letters) encoding.|
|`ESC [ 9 9 6 8 1 9 * p`|Switch to the OMS (LaTeX Mathematical Symbols) encoding.|
|`ESC [ 9 9 6 8 2 4 * p`|Switch to the OMX (LaTeX Mathematical Brackets) encoding.|
|`ESC [ 9 9 7 0 0 0 * p`|Switch to the VPS encoding.|
|`ESC [ 9 9 7 0 0 1 * p`|Switch to the TCVN (ABC, .VN, VSCII; not VISCII) encoding.|
|`ESC [ 9 9 7 0 0 2 * p`|Switch to the VISCII (not VSCII) encoding.|
|`ESC [ 9 9 7 0 0 3 * p`|Switch to the VNI-for-Macintosh encoding.|
|`ESC [ 9 9 7 0 0 4 * p`|Switch to the VNI-for-DOS encoding.|
|`ESC [ 9 9 8 0 0 0 * p`|Switch to the Zapf Dingbats encoding.|
|`ESC [ 9 9 8 0 0 1 * p`|Switch to the extended Zapf Dingbats encoding.|
|`ESC [ 9 9 8 0 0 2 * p`|Switch to the WordPerfect Iconic Symbols encoding.|
|`ESC [ 9 9 8 1 0 0 * p`|Switch to the LaTeX `wasy10` symbol set encoding.|
|`ESC [ 9 9 9 0 0 0 * p`|Switch to the Webdings encoding.|
|`ESC [ 9 9 9 0 0 1 * p`|Switch to the Wingdings encoding.|
|`ESC [ 9 9 9 0 0 2 * p`|Switch to the Wingdings 2 encoding.|
|`ESC [ 9 9 9 0 0 3 * p`|Switch to the Wingdings 3 encoding.|
|`ESC [ 9 9 9 9 0 1 * p`|Switch to the LaTeX "Storm" encoding.|
|`ESC [ 9 9 9 9 0 2 * p`|Switch to the LaTeX "dvips" encoding.|
|`ESC [ 9 9 9 9 0 3 * p`|Switch to the LGR (LaTeX Greek) encoding.|
|`ESC [ 9 9 9 9 0 4 * p`|Switch to the LaTeX `desalph` encoding for the Deseret Alphabet.|

G-sets can still be used on the left-hand side of the code page (the mode is mostly business as
usual as far as ECMA-35's 7-bit mechanisms are concerned, the only difference is the extra 128
graphical codes which are not governed by ECMA-35, since it does not use ECMA-35's 8-bit
mechanisms).&ensp;G-sets and the GL invocation are reset by the DECSPPCS sequence, however; the
defaults can vary with code page (the default is usually GL=G0=ASCII, for example, whereas 1252
also includes the GR of ISO-8859-1 as its G1 set for fairly obvious reasons).

Hence, by default, all C0 control codes will continue to work as normal.&ensp;However, the 
following sequences can be used to change this (note: this is based on [DEC's approach](https://vt100.net/docs/vt510-rm/DECSDPT.html)&rpar;:

|Private assignment|Meaning|
|---|---|
|`ESC [ ) p`|Reset to implementation default behaviour (in this case, the same as `ESC [ 3 ) p`).|
|`ESC [ 1 ) p`|C0 and C1 control codes work as normal (note: previously incorrectly implemented same as `ESC [ 3 ) p`).|
|`ESC [ 2 ) p`|C0 and C1 control codes work as normal (note: previously incorrectly implemented like the current `ESC [ 5 ) p`).|
|`ESC [ 3 ) p`|C0 control codes work as normal.|
|`ESC [ 4 ) p`|C0 codes are almost all graphical characters, the sole exception being ESC so that reversal is possible.|
|`ESC [ 5 ) p`|C0 codes are mostly interpreted as graphical characters, except for BEL, BS, HT, LF, CR and ESC.|

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
- Proper handling of the T.51 / T.61 and ANSEL combining sequences. Not sticking to any hardcoded
  repertoire though, since (a) we're not trying to implement ISO/IEC 6937, but rather T.51
  (which confines the entire ISO 6937 repertoire definition (rather than just one of the charts
  as in ISO/IEC 6937) to an annex which isn't referenced from the main text), and (b) we're 
  mapping to ISO/IEC 10646, not to ISO/IEC 10367 or 8859, so combining marks aren't a problem.
- All graphical sets (besides Blissymbolics) with registered escapes.
- Backspace composition sequences.
- Support for EBCDIC as a DOCS set.

# Still to do

- More general RHS sets.
- Support for JOHAB as a DOCS set.
- Support for LMBCS as a DOCS set.
- Dynamically allocating sets, IRR codes, DOCS codes (e.g. Shift_JIS) in some configurable way.
- Functionality of CSI, CEX, C1 _et cetera_ controls.
  - Rich or annotated output of some sort.
- Figure out how the relevant parts of Videotex work:
  - The rest of the control sets.
  - The rest of the DOCS codes.
- Announcements, and some means of verifying them. Preferably by generating ERROR tokens.
- Some sort of encoder.
- Some sort of decent API for using it from outside.


