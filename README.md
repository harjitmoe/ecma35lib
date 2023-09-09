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
|`DOCS / 5`|Standard Compression Scheme for Unicode (SCSU). Was previously `DOCS / 0`; changed to avoid conflict with use of `DOCS / 0` by X11 Compound Text.|
|`DOCS / 6`|EBCDIC.|
|`DOCS / 7`|UTF-EBCDIC.|

## Additional single-byte G-sets, and additional selectors for particular variants of single-byte G-sets

|Private assignment|Meaning|
|---|---|
|`IRR 0 G*D4 @`|Old IRV with tilde (rather than overscore)|
|``IRR 0 G*D4 [ACEH`g]``|DEC NRCS, where they differ from standard|
|`IRR 0 G*D4 B`|ASCII with overscore (rather than tilde)|
|`IRR 1 G*D4 B`|ASCII-1967 using broken-bar mapping|
|`IRR 2 G*D4 B`|ASCII-1967, PL/I variant|
|`IRR 3 G*D4 B`|Modified ASCII with Florin sign (cross between ASCII and `G*D4 $ 2`)|
|`IRR 0 G*D4 G`|Variant Swedish and Finnish, projected from EBCDIC WP96|
|`IRR 0 G*D4 I`|JIS X 0201 katakana, IBM's 4992 (used for its counterparts from IBM's 1041 in the Shift\_JIS filter).|
|`IRR 1 G*D4 I`|JIS X 0201 katakana, an analogous extraction from MacJapanese.|
|`IRR 2 G*D4 I`|JIS X 0201 katakana, an extraction from Windows-31J and friends.|
|`IRR 3 G*D4 I`|JIS X 0201 katakana, an extraction from Windows-31J and friends, suppressing the 0x80 control mapping in some DOCS filters in favour of the Euro.|
|`IRR 0 G*D4 J`|JIS-Roman with tilde (rather than overscore)|
|`IRR ? G*D4 K`|DIN 66003 with apostrophe (default)|
|`IRR 0 G*D4 K`|DIN 66003 with acute|
|`IRR ? G*D4 O`|DIN 31624, possibly-older German relative of ISO 5426-1|
|`IRR 0 G*D4 O`|DIN 31624, falling thru to T.51 for unallocated cells|
|`IRR ? G*D4 P`|ISO 5426-1, bibliographic set related to (but incompatible with) T.51|
|`IRR 0 G*D4 P`|ISO 5426-1, falling thru to T.51 for unallocated cells|
|`IRR ? G*D4 R`|NF Z 62-010 (7-bit French), 1973 edition (also used by DEC)|
|`IRR 0 G*D4 R`|Variant 7-bit French projected from EBCDIC DP94 for Belgian French|
|`IRR 1 G*D4 R`|Variant 7-bit French projected from EBCDIC WP96 for Belgian French|
|`IRR 2 G*D4 R`|Variant 7-bit French projected from EBCDIC 38xx for Belgian French|
|`IRR 0 G*D4 Y`|ETS 300 706 Latin G0 for Italy|
|`IRR 1 G*D4 Y`|7-bit Italian with not-sign|
|``IRR 0 G*D4 ` ``|DEC alternate NRCS for Denmark and Norway|
|``IRR 1 G*D4 ` ``|Danish equivalent to NS 4551 (IBM's 1017)|
|``IRR 2 G*D4 ` ``|Variant Denmark and Norway projected from EBCDIC WP96|
|`IRR ? G*D4 f`|NF Z 62-010 (7-bit French), 1982 edition|
|`IRR 0 G*D4 f`|Variant 7-bit French projected from EBCDIC encodings for Maghrebi French|
|`IRR 1 G*D4 f`|Variant 7-bit French projected from EBCDIC 38xx encoding|
|`IRR 2 G*D4 f`|Variant 7-bit French projected from EBCDIC DCF Migration encoding|
|`IRR ? G*D4 k`|ASMO 449 (ISO 9036) 7-bit Arabic|
|`IRR 0 G*D4 k`|MARC-8 Basic Arabic|
|`IRR ? G*D4 l`|ITU T.51-1988 first supplementary set (i.e. older version of the T.51 supplementary set without NBSP, SHY, not sign or brvbar)|
|`IRR 0 G*D4 l`|ITU T.51-1988 first supplementary set with ETS 300 706 extensions (default for this F-byte)|
|`IRR 1 G*D4 l`|ITU T.51-1988 first supplementary set with ETS 300 706 extensions, alternative mapping|
|`IRR ? G*D4 o`|JIS X 9010 non-JISCII set for OCR-B.|
|`IRR 0 G*D4 o`|ISO-8859-1 RHS cropped to 94-set, with backslash replacing yen sign (superset of the non-JISCII set for OCR-B).|
|`IRR ? G*D4 q`|JIS X 9010 backslash-only set for JIS X 9008, mapping to ASCII as strongly implied by registration rubric (subset of the non-JISCII set for OCR-B).|
|`IRR 0 G*D4 q`|JIS X 9010 backslash-only set for JIS X 9008, mapping to OCR DOUBLE BACKSLASH.|
|`IRR 0 G*D4 ! B`|DEC NRCS, invariant subset|
|`IRR 1 G*D4 ! B`|ETS 300 706 Latin G0, invariant subset|
|`IRR 2 G*D4 ! B`|IBM version of the invariant set|
|`IRR ? G*D4 ! E`|ANSEL supplementary set, ANSI standard version (i.e. no eszett)|
|`IRR 0 G*D4 ! E`|ANSEL supplementary set, Library of Congress version (i.e. eszett at 0x47)|
|`IRR 1 G*D4 ! E`|ANSEL supplementary set, combined Library of Congress and Genealogical Society of Utah versions, i.e. duplicate eszetts at 0x47 and 0x4F (default for this F-byte)|
|`G*D4 # 0`|KS X 1003|
|`IRR 0 G*D4 # 0`|KS X 1003 with tilde|
|`G*D4 # 1`|ETS 300 706 Latin G0 for France|
|`G*D4 # 2`|ETS 300 706 Latin G0 for Spain and Portugal|
|`G*D4 # 3`|ETS 300 706 Latin G0 for Estonia|
|`G*D4 # 4`|ETS 300 706 Latin G0 for Latvia and Lithuania|
|`G*D4 # 5`|ETS 300 706 Latin G0 for Serbia, Bosnia, Croatia and Slovenia|
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
|`G*D4 $ 1`|DEC NRCS for Switzerland (corresponding to DEC's (not ARIB's) `G*D4 4`)|
|`G*D4 $ 2`|DEC NRCS for the Netherlands (corresponding to DEC's `G*D4 =`)|
|`G*D4 $ 3`|Marlett encoding|
|`G*D4 $ 4`|Zapf Dingbats, GL range|
|`G*D4 $ 5`|Zapf Dingbats, GR range|
|`G*D4 $ 6`|Symbol font encoding, GL range|
|`G*D4 $ 7`|Symbol font encoding, GR range (no euro)|
|`G*D4 $ 8`|7-bit Maltese|
|`IRR ? G*D4 $ 9`|7-bit Icelandic|
|`IRR 0 G*D4 $ 9`|7-bit Icelandic, following the DP94 set of EBCDIC code page 871|
|`IRR ? G*D4 $ :`|7-bit Polish, ostensibly (unverified) following BN-74/3101-01|
|`IRR 0 G*D4 $ :`|7-bit Polish, following the DP94-range subset (GL set) of EBCDIC code page 252|
|`IRR 1 G*D4 $ :`|7-bit Polish, compromise between the two above (default for these I/F bytes)|
|`IRR ? G*D4 $ ;`|ISO 11822:1996 Arabic supplementary set|
|`IRR 0 G*D4 $ ;`|MARC-8 Extended Arabic|
|`G*D4 $ <`|ISO 10586:1996 Georgian|
|`G*D4 $ =`|ISO 10585:1996 Armenian|
|`G*D4 $ >`|MARC-8 Hebrew|
|~~`G*D4 $ ?`~~|~~MARC-8 Extended Arabic~~ changed to `IRR 0 G*D4 $ ;`|
|~~`G*D4 % 0`~~|~~MARC-8 subscript numbers~~ collides with use elsewhere, changed to `G*D4 & 9`|
|`G*D4 % 1`|MARC-8 superscript numbers|
|`G*D4 % 4`|7-bit Canadian French, projected from EBCDIC DP94|
|`G*D4 % 7`|7-bit European Portugese, projected from EBCDIC DP94|
|`G*D4 % 8`|7-bit Turkish, projected from EBCDIC DP94|
|`G*D4 % 9`|7-bit Roman, projected from EBCDIC 38xx|
|`IRR ? G*D4 % :`|7-bit Roman for use with a Greek set, projected from EBCDIC, small version|
|`IRR @ G*D4 % :`|7-bit Roman for use with a Greek set, projected from EBCDIC, large version|
|`IRR ? G*D4 % :`|7-bit Roman for use with a Cyrillic set, projected from EBCDIC, large version|
|`IRR 0 G*D4 % :`|7-bit Roman for use with a Cyrillic set, projected from EBCDIC, small version|
|`G*D4 & :`|7-bit British, projected from EBCDIC WP96|
|`IRR ? G*D4 & ;`|7-bit Brazilian Portugese, projected from EBCDIC DP94|
|`IRR 0 G*D4 & ;`|7-bit Brazilian Portugese, projected from EBCDIC 38xx|
|`IRR ? G*D4 & <`|7-bit Danish and Norwegian, projected from EBCDIC DP94|
|`IRR 0 G*D4 & <`|7-bit Danish and Norwegian with Euro, projected from EBCDIC DP94|
|`IRR ? G*D4 & =`|7-bit Swedish and Finnish, projected from EBCDIC DP94|
|`IRR 0 G*D4 & =`|7-bit Swedish and Finnish with Euro, projected from EBCDIC DP94|
|`G*D4 & 9`|MARC-8 subscript numbers|
|`IRR ? G*D6 J`|ITU T.51 supplementary set for use with old IRV (excludes universal currency sign and hash)|
|`IRR 0 G*D6 J`|Complete ITU T.51 supplementary set (same as `IRR 0 G*D6 R`; default for this F-byte)|
|`IRR ? G*D6 R`|ITU T.51 supplementary set for use with ASCII (excludes dollar and hash)|
|`IRR 0 G*D6 R`|Complete ITU T.51 supplementary set (same as `IRR 0 G*D6 J`; default for this F-byte)|
|`G*D6 ! 0`|RFC 1345's so-called ISO-IR-111/ECMA-Cyrillic (incompatible with ISO-IR-111 itself).|
|`IRR ? G*D6 $ 7`|Symbol font encoding, GR range (with euro)|
|`IRR 0 G*D6 $ 7`|Symbol font encoding, GR range (with figure space)|

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
|`IRR 2 G*DM4 A`|GB 18030-2005 levels 1 and 2 (default)|
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
|`IRR ? G*DM4 D`|JIS X 0212:1990|
|`IRR 0 G*DM4 D`|JIS X 0212 with va/vi/ve/vo|
|`IRR 1 G*DM4 D`|JIS X 0212, Open Group version for JIS-Roman based EUC-JP|
|`IRR 2 G*DM4 D`|JIS X 0212, Open Group version for ASCII-based EUC-JP|
|`IRR 3 G*DM4 D`|JIS X 0212, Open Group version for Microsoft-style EUC-JP|
|`IRR 4 G*DM4 D`|JIS X 0212, version encoded by IBM-954|
|`IRR 5 G*DM4 D`|JIS X 0212, version encoded by ICU's EUC-JP|
|`IRR ? G*DM4 E`|CCITT Hanzi Code (GB 2312 variant) from ITU T.101-C, which bases it on GB 6345.1-1986 and GB 8565.2-1988 with further adjustments and expansions|
|`IRR 0 G*DM4 E`|CCITT Hanzi Code, with a more conventional mapping of the lowercase gs (appropriate for their GB 18030 reference glyphs)|
|`IRR 1 G*DM4 E`|CCITT Hanzi Code, combined with an additional hanzi extension in row 8|
|`IRR 2 G*DM4 E`|GB 6345.1-1986|
|`IRR 3 G*DM4 E`|GB 8565.2-1988|
|`IRR 4 G*DM4 E`|Pseudo-G8, an incorrect version of GB 8565.2-1988 which had been referenced by older versions of the Unihan database (incorrectly shifts the actual GB 8565.2 characters 15-90 through 15-93 back by one code point over 15-89, and also includes the row 8 hanzi extensions and most of the CCITT hanzi extensions).|
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
|`IRR ? G*DM4 H`|CNS 11643 plane 2|
|`IRR 1 G*DM4 H`|CNS 11643 plane 2, Big5 mappings|
|`IRR 5 G*DM4 H`|CNS 11643 plane 2, Unihan mappings|
|`IRR ? G*DM4 I`|CNS 11643-1992 plane 3|
|`IRR 0 G*DM4 I`|CNS 11643-1988 plane 14|
|`IRR 1 G*DM4 I`|CNS 11643-1988 plane 14 with extensions, as submitted to the IRG|
|`IRR 2 G*DM4 I`|CNS 11643-2007 plane 3|
|`IRR 3 G*DM4 I`|CNS 11643-2007 plane 3, plus the additional assignments from CNS 11643-1988 plane 14 (default)|
|`IRR 4 G*DM4 I`|CNS 11643-1988 plane 14, UTC mappings (partial, with extensions)|
|`IRR 5 G*DM4 I`|CNS 11643-1992 plane 3, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 6 G*DM4 I`|CNS 11643-1992 plane 3, per ICU EUC-TW 2014 mappings|
|`IRR 7 G*DM4 I`|CNS 11643-1992 plane 3, per Yasuoka's mappings|
|`IRR 8 G*DM4 I`|CNS 11643-1992 plane 3, per Unihan mappings|
|`IRR ? G*DM4 J`|CNS 11643-1992 plane 4|
|`IRR 0 G*DM4 J`|CNS 11643-1992 plane 4, as officially defined in Taiwan|
|`IRR 1 G*DM4 J`|CNS 11643-1992 plane 4, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 J`|CNS 11643-1992 plane 4, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 J`|CNS 11643-1992 plane 4, per Yasuoka's mappings|
|`IRR 4 G*DM4 J`|CNS 11643-1992 plane 4, per Unihan mappings|
|`IRR ? G*DM4 K`|CNS 11643-1992 plane 5|
|`IRR 0 G*DM4 K`|CNS 11643-1992 plane 5, as officially defined in Taiwan|
|`IRR 1 G*DM4 K`|CNS 11643-1992 plane 5, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 K`|CNS 11643-1992 plane 5, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 K`|CNS 11643-1992 plane 5, per Yasuoka's mappings|
|`IRR 4 G*DM4 K`|CNS 11643-1992 plane 5, per Unihan mappings|
|`IRR ? G*DM4 L`|CNS 11643-1992 plane 6|
|`IRR 0 G*DM4 L`|CNS 11643-1992 plane 6, as officially defined in Taiwan|
|`IRR 1 G*DM4 L`|CNS 11643-1992 plane 6, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 L`|CNS 11643-1992 plane 6, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 L`|CNS 11643-1992 plane 6, per Yasuoka's mappings|
|`IRR 4 G*DM4 L`|CNS 11643-1992 plane 6, per Unihan mappings|
|`IRR ? G*DM4 M`|CNS 11643-1992 plane 7|
|`IRR 0 G*DM4 M`|CNS 11643-1992 plane 7, as officially defined in Taiwan|
|`IRR 1 G*DM4 M`|CNS 11643-1992 plane 7, per former ICU ISO-2022-CN-EXT mappings|
|`IRR 2 G*DM4 M`|CNS 11643-1992 plane 7, per ICU EUC-TW 2014 mappings|
|`IRR 3 G*DM4 M`|CNS 11643-1992 plane 7, per Yasuoka's mappings|
|`IRR 4 G*DM4 M`|CNS 11643-1992 plane 7, per Unihan mappings|
|`IRR ? G*DM4 N`|KPS 9566-97|
|`IRR 0 G*DM4 N`|KPS 9566-2003 (only the main plane unless in the UHC DOCS)|
|`IRR 1 G*DM4 N`|KPS 9566-2011 (only the main plane unless in the UHC DOCS)|
|`IRR 2 G*DM4 N`|All KPS 9566 editions overlayed (but only the main plane unless in the UHC DOCS)|
|`G*DM4 ! 0`|GB/T 12052 (Korean in Mainland China)|
|`IRR ? G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (recommended version)|
|`IRR 0 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (ICU EUC-2014 version)|
|`IRR 1 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (Microsoft version)|
|`IRR 2 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (Apple version)|
|`IRR 3 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (GOV-TW version)|
|`IRR 4 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (old ICU version)|
|`IRR 5 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (IBM version)|
|`IRR 6 G*DM4 ! 1`|All planes of CNS 11643 as a 94^3 set, as included by EUC-TW as its G2 set (Yasuoka version)|
|`IRR 7 G*DM4 ! 1`|Planes 2 and up of CNS 11643 as a 94^3 set, as included by IBM EUC-TW as its G2 set (ICU EUC-2014 version)|
|`IRR 5 G*DM4 ! 1`|Planes 2 and up of CNS 11643 as a 94^3 set, as included by IBM EUC-TW as its G2 set (IBM version)|
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
|`IRR @ G*DM4 ! 3`|Non-ETEN Big5 kana and Cyrillic (accepted by Big-5 filter in G3 slot, not expected to be used elsewhere) combined with Microsoft non-EUDC extensions, as in Python's built-in (used when not on Windows or when MS-950 is not the ACP) version of "cp950".|
|`IRR ? G*DM4 ! 4`|IBM extensions for Shift\_JIS (accepted by Shift\_JIS filter in G3 slot, mapped to/from Shift\_JIS by the same mapping scheme as JIS X 0213 plane 2); excluding UDC|
|`IRR @ G*DM4 ! 4`|IBM extensions for Shift\_JIS (accepted by Shift\_JIS filter in G3 slot, mapped to/from Shift\_JIS by the same mapping scheme as JIS X 0213 plane 2); including UDC|
|`IRR 0 G*DM4 ! 4`|IBM extensions for Shift\_JIS (accepted by Shift\_JIS filter in G3 slot, mapped to/from Shift\_JIS by the same mapping scheme as JIS X 0213 plane 2); old mappings for use with 78JIS|
|`G*DM4 ! 5`|DoCoMo Emoji extensions for Shift\_JIS (as above)|
|`IRR ? G*DM4 ! 6`|KDDI Emoji extensions for Shift\_JIS (as above), pictorial zodiac variant|
|`IRR 0 G*DM4 ! 6`|KDDI Emoji extensions for Shift\_JIS (as above), symbolic zodiac variant|
|`G*DM4 ! 7`|SoftBank Emoji extensions for Shift\_JIS (as above)|
|`IRR ? G*DM4 ! 8`|GB 13131 (supplementary traditional).|
|`IRR 0 G*DM4 ! 8`|GB 7589 (supplementary simplified)&mdash;This is generated from the GB 13131 mappings, and may be minorly inaccurate in places.|
|`IRR ? G*DM4 ! 9`|GB 13132 (further supplementary traditional)&ensp;This is based on Unihan source data, and has several gaps.|
|`IRR 0 G*DM4 ! 9`|GB 7590 (further supplementary simplified)&mdash;This is generated from the GB 13132 mappings, and may be minorly inaccurate in places.|
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
|`IRR ? G*DM4 " 0`|Big5 AtOn/ChinaSea extensions (for Big-5 filter's G3 slot)|
|`IRR 0 G*DM4 " 0`|Big5 AtOn/ChinaSea extensions (for Big-5 filter's G3 slot), alternate version|
|`IRR ? G*DM4 " 1`|IBM-926 (IBM-944)'s 94×94 plane (not KS X 1001 compatible for the most part).&ensp;No DOCS filter exists for it yet though.&ensp;Reconstructed original version.|
|`IRR @ G*DM4 " 1`|IBM-926 (IBM-944)'s 94×94 plane (not KS X 1001 compatible for the most part).&ensp;No DOCS filter exists for it yet though.|
|`IRR 0 G*DM4 " 1`|IBM-926 (IBM-944)'s 94×94 plane (not KS X 1001 compatible for the most part).&ensp;No DOCS filter exists for it yet though.&ensp;IBM mappings including corporate PUA.|
|`IRR ? G*DM4 " 2`|GB 16500 (yet another supplementary set, numbered the seventh in its title though Unihan calls it "GE").|
|`IRR @ G*DM4 " 2`|GB 16500 combined with "General Purpose Hanzi" (do not overlap, both are plane "7").|
|`IRR 0 G*DM4 " 2`|"General Purpose Hanzi" (a small supplement of fewer than 200 characters for use alongside GBs 2312, 7589 and 7590 for Simplified Chinese).|
|`G*DM4 " 3`|Big5 DynaLab extensions (for Big-5 filter's G3 slot)|
|`G*DM4 " 4`|Big5 Monotype extensions (for Big-5 filter's G3 slot)|
|`G*DM4 " 5`|Big5-Plus in-plane extensions (for Big-5 filter's G3 slot)|
|`G*DM4 " 6`|Big5-Plus out-of-plane extensions (not currently usable as such)|
|`G*DM4 " 7`|IBM Big5 non-ETEN out-of-plane extensions (not currently usable as such)|
|`IRR ? G*DM6 ! 0`|GBK extras (GB 18030, level 5 with associated UDC zone and non-URO part of level 4; accepted by GBK filter in G3 slot)|
|`IRR 0 G*DM6 ! 0`|GBK extras, WHATWG/HTML5 variant|
|`IRR 1 G*DM6 ! 0`|GBK extras, mapping all characters with defined glyphs to non-PUA|
|`IRR ? G*DM6 ! 1`|EACC / CCCII, Library of Congress version|
|`IRR 0 G*DM6 ! 1`|EACC / CCCII, Koha Taiwan version|
|`IRR 1 G*DM6 ! 1`|EACC / CCCII, Hong Kong Innovative Users Group / Hong Kong University version|
|`IRR 2 G*DM6 ! 1`|EACC / CCCII, aggregate version with Taiwan layout of row 2, favouring Unihan kCCCII for kanji mappings (default)|
|`IRR 3 G*DM6 ! 1`|EACC / CCCII, aggregate version with Hong Kong layout of rows 0–2, favouring Library of Congress for kanji mappings|

## "Plain extended ASCII" mode

Plain extended ASCII mode is switched to by `DOCS 3` as 
mentioned above.&ensp;Once inside, the DEC-defined DECSPPCS control sequence (i.e. `CSI … * p`) is
used for switching between numbered code pages (e.g. `CSI 1 2 5 2 * p`).&ensp;Numbers above 65535
are used for custom purposes.&ensp;Specifically:

|Private assignment|Meaning|
|---|---|
|`ESC [ 9 9 7 0 0 0 * p`|Switch to the VPS encoding.|
|`ESC [ 9 9 7 0 0 1 * p`|Switch to the TCVN (ABC, .VN, VSCII; not VISCII) encoding.|
|`ESC [ 9 9 7 0 0 2 * p`|Switch to the VISCII (not VSCII) encoding.|
|`ESC [ 9 9 8 0 0 0 * p`|Switch to the Zapf Dingbats encoding.|
|`ESC [ 9 9 9 0 0 0 * p`|Switch to the Webdings encoding.|
|`ESC [ 9 9 9 0 0 1 * p`|Switch to the Wingdings encoding.|
|`ESC [ 9 9 9 0 0 2 * p`|Switch to the Wingdings 2 encoding.|
|`ESC [ 9 9 9 0 0 3 * p`|Switch to the Wingdings 3 encoding.|

.. Pending are VNI-Mac, VNI-DOS, SP-Tiberian (modified Michigan-Claremont), Bee Fonts

G-sets can still be used on the left-hand side of the code page (the mode is mostly business as
usual as far as ECMA-35's 7-bit mechanisms are concerned, the only difference is the extra 128
graphical codes which are not governed by ECMA-35, since it does not use ECMA-35's 8-bit
mechanisms).&ensp;G-sets and the GL invocation are reset by the DECSPPCS sequence, however; the
defaults can vary with code page (the default is usually GL=G0=ASCII, for example, whereas 1252
also includes the GR of ISO-8859-1 as its G1 set for fairly obvious reasons).

Hence, by default, all C0 control codes will continue to work as normal.&ensp;However, the 
following sequences can be used to change this:

|Private assignment|Meaning|
|---|---|
|`ESC [ 1 ) p`|C0 control codes work as normal.|
|`ESC [ 2 ) p`|C0 codes are mostly interpreted as graphical characters, except for BEL, BS, HT, LF, CR and ESC.|
|`ESC [ 4 ) p`|C0 codes are almost all graphical characters, the sole exception being ESC so that reversal is possible.|

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


