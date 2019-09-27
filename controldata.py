#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# Transmission controls (aliases TC1 thru TC10):
#    SOH (SOM), STX (EOA), ETX, EOT, ENQ (WRU), ACK, DLE, NAK, SYN, ETB
# These are constrained to appear in their ASCII positions or not at all (whereäs other ASCII 
# controls may not be moved around in the C0 set, but may be moved to the C1 set). Furthermore, 
# they are the only transmission control characters permitted to appear in the C0 set.
# The 1963 version lacked DLE and ETB (see below), and additionally had RU (Are You…).

# Format effectors (aliases FE0 thru FE5):
#    BS, HT, LF, VT, FF, CR
# These (in addition to GL bytes) may be used in DCS, OSC, PM and APC sequences or follow SCI.

# Device controls (aliases DC0 thru DC4):
#    DC0, XON, DC2, XOFF, DC4
# DC0 in the 1963 version was later removed in favour of DLE (TC7).

# Information separators (aliases IS8 thru IS1, or S0 thru S7):
#    S0, S1, S2, S3, FS, GS, RS, US
# The first four were in the 1963 version but later removed (see below).

format_effectors = ["BS", "HT", "LF", "VT", "FF", "CR"]

fixed_controls = {(0x60,): "DMI", # Disable Manual Input, `
                  (0x61,): "INT", # Interrupt, a
                  (0x62,): "EMI", # Enable Manual Input, b
                  (0x63,): "RIS", # Reset to Initial State, c (what the "reset" command does)
                  (0x64,): "CMD", # Coding Method Delimiter, d
                  #
                  (0x6E,): "LS2", # Locking Shift Two, n
                  (0x6F,): "LS3", # Locking Shift Three, o
                  #
                  (0x7C,): "LS3R", # Locking Shift Three Right, |
                  (0x7D,): "LS2R", # Locking Shift Two Right, }
                  (0x7E,): "LS1R"} # Locking Shift One Right, ~

c0sets = {# The ECMA-6 controls, i.e. originating from 1967 edition ASCII:
          "001": ("NUL", # Null
                  "SOH", # Start of Header, Start of Message (SOM), Transmission Control One (TC1)
                  "STX", # Start of Text, End of Address (EOA), Transmission Control Two (TC2)
                  "ETX", # End of Text, Transmission Control Three (TC3)
                  "EOT", # End of Transmission, Transmission Control Four (TC4)
                  "ENQ", # Enquiry, Who Are You (WRU), Transmission Control Five (TC5)
                  # RU (Are You…) was included in the 1963 ASCII over where ACK is now placed.
                  # ACK was at 0x7C, outside the current control character range.
                  "ACK", # Acknowledgement, Transmission Control Six (TC6)
                  "BEL", # Bell, Alert
                  "BS", # Backspace, Format Effector Zero (FE0)
                  "HT", # Character [Horizontal] Tabulation, Tab, Format Effector One (FE1)
                  "LF", # Line Feed, Format Effector Two (FE2)
                  "VT", # Line [Vertical] Tabulation (VTAB), Format Effector Three (FE3)
                  "FF", # Form Feed, Format Effector Four (FE4)
                  "CR", # Carriage Return, Format Effector Five (FE5)
                  # ECMA-35 and ECMA-48 insist that the exact same control codes be called
                  # SO and SI in 7-bit environments, and LS1 and LS0 in 8-bit environments.
                  # To the point of wording things as if they were different pairs of controls,
                  # one used in 7-bit environments and the other in 8-bit environments, despite
                  # both the representation and the behaviour being identical.
                  # I'm just using SO and SI as the mnemonics since otherwise is overcomplicated.
                  "SO", # Shift Out, Locking Shift One (LS1)
                  "SI", # Shift In, Locking Shift Two (LS0)
                  # The 1963 ASCII had DC0 instead of TC7 (DLE).
                  "DLE", # Data Link Escape, Transmission Control Seven (TC7)
                  # The XON and XOFF mnemonics are conventional.
                  "XON", # Transmit On, Device Control One (DC1)
                  "DC2", # Device Control Two
                  "XOFF", # Transmit Off, Device Control Three (DC3)
                  "DC4", # Device Control Four
                  "NAK", # Negative Acknowledgement, Transmission Control Eight (TC8)
                  "SYN", # Synchronous Idle (SYNC), Transmission Control Nine (TC9)
                  "ETB", # End of Transmission Block, Transmission Control Ten (TC10)
                  "CAN", # Cancel
                  "EM", # End of Medium, Logical End of Media (LEM)
                  "SUB", # Substitute
                  "ESC", # Escape
                  # S0 through S3 were included in the 1963 ASCII over where CAN/EM/SUB/ESC now
                  # are. ESC was at 0x7E, and EM was where ETB now is. CAN/SUB/ETB were absent.
                  "FS", # File Separator, Information Separator Four (IS4), Separator Four (S4)
                  "GS", # Group Separator, Information Separator Three (IS3), Separator Five (S5)
                  "RS", # Record Separator, Information Separator Two (IS2), Separator Six (S6)
                  "US"), # Unit Separator, Information Separator One (IS1), Separator Seven (S7)
          # Scandinavian newspaper (NATS) controls. Particular perculiarities include commandeering
          # FS as a single-shift and GS/RS/US as EOLs which centre/right-align/justify the
          # terminated line, and changing the mnemonics of HT to be vague and CAN to be specific.
          # I presume the "SS" is supposed to be SS2 (assuming 036 to be related somewhat), and 
          # for sure my decode_invocations isn't gonna respond to the "SS" mnemonic.
          "007": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
                  "BS",
                  "FO", # Formatting (still seems to be basically a tab in normal contexts though).
                  "LF",
                  "ECD", # End of Instruction
                  "SCD", # Start of Instruction
                  "QL", # Quad Left
                  "UR", # Upper Rail (i.e. emphasised, or, the older TTY-ribbon sense of SO).
                  "LR", # Lower Rail
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                  "KW", # Kill Word (sense not massively different from CAN, but more specific).
                  "EM", "SUB", "ESC", # Escape
                  "SS2", # Calls it "Super Shift (SS)", but means a single shift.
                  "QC", # Quad Centre
                  "QR", # Quad Right
                  "JY"), # Justify
          # International newspaper (IPTC) controls. Very similar to the NATS controls, but 
          # commandeers DC1/DC2/DC3 for (two orthogonal types of) emphasis, instead of SI/SO.
          "026": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
                  "BS", "FO", "LF", "ECD", "SCD", "QL", "SO", "SI",
                  "DLE",
                  "FT1", # Font 1 (normal)
                  "FT2", # Font 2 (italic)
                  "FT3", # Font 3 (bold)
                  "DC4", "NAK", "SYN", "ETB", 
                  # Similarly calling the single-shift "Super Shift (SS)"
                  "KW", "EM", "SUB", "ESC", "SS2", "QC", "QR", "JY"),
          # Closer to ASCII, but still with SS2 over FS, this time calling it SS2. Document seems  
          # to be a Q&D scissors-and-photocopier edit of 001.
          # Apparently submitted by ISO/TC97/SC2/WG1 (ISO/TC97 = ISO/IEC JTC1).
          "036": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                  "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                  "CAN", "EM", "SUB", "ESC", "SS2", "GS", "RS", "US"),
          # The International Nuclear Information System (INIS)'s subset of ASCII apparently
          # also subsets its controls to only GS, RS and (the mandatory) ESC.
          "048": (None,)*27 + ("ESC",) + (None, "GS", "RS", None),
          # JIS C 6225's C0 set, differs by replacing IS4 (that is to say, FS) with CEX.
          "074": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                  "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                  "CAN", "EM", "SUB", "ESC", 
                  "CEX", # Control Extension
                  "GS", "RS", "US"),
          # 104 and nil are de facto the same, since (a) ECMA-35 guarantees that ESC is always
          # available at 0x1B, no matter what's designated, and (b) ESC was already processed by
          # tokenfeed (it has to be, for to be able to parse through DOCS regions), so a C0 token
          # will never contain an ESC. Including both here anyway for the sake of academic utility.
          "104": (None,)*27 + ("ESC",) + (None,)*4,
          # Small subset of ASCII controls plus two single-shifts, for CCITT Rec. T.61 Teletex:
          "106": (None, None, None, None, None, None, None, None, 
                  "BS", None, "LF", None, "FF", "CR", "SO", "SI",
                  None, None, None, None, None, None, None, None, 
                  None, "SS2", "SUB", "ESC", None, "SS3", None, None),
          # ASCII controls minus the shifts, since apparently some standards require that:
          "130": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                  "BS", "HT", "LF", "VT", "FF", "CR", None, None,
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                  "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US"),
          # SS2 replacing EM, was apparently used in Czechoslovakia:
          "140": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                  "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                  "CAN", "SS2", "SUB", "ESC", "FS", "GS", "RS", "US"),
          "nil": (None,)*16} 

c1sets = {# NOTE: decode_control_strings assumes OSC is the ANSI OSC, NOT the unrelated DIN OSC.
          #
          # The "ANSI escape" codes (ECMA-48) which occupy the C1 area:
          "077": (None, # Vacant
                  None, # Vacant
                  "BPH", # Break Permitted Here (basically ZWSP)
                  "NBH", # No Break Here (basically WJ)
                  "IND", # Index (meaning a pure line feed)
                  "NEL", # New Line (used mainly in converted EBCDIC data)
                  "SSA", # Start of Selected Area
                  "ESA", # End of Selected Area
                  "HTS", # Character [Horizontal] Tabulation Set
                  "HTJ", # Character [Horizontal] Tabulation with Justification
                  "VTS", # Line [Vertical] Tabulation Set
                  "PLD", # Partial Line Down
                  "PLU", # Partial Line Up
                  "RI", # Reverse Index, Reverse Line Feed
                  "SS2", # Single Shift Two
                  "SS3", # Single Shift Three
                  "DCS", # Device Control String
                  "PU1", # Private Use One
                  "PU2", # Private Use Two
                  "STS", # Set Transmit State
                  "CCH", # Cancel Character (meaning a destructive backspace)
                  "MW", # Message Waiting
                  "SPA", # Start of Protected Area
                  "EPA", # End of Protected Area
                  "SOS", # Start of String
                  None, # Vacant
                  "SCI", # Single Character Introducer
                  "CSI", # Control Sequence Introducer
                  "ST", # String Terminator
                  "OSC", # Operating System Command
                  "PM", # Privacy Message
                  "APC"), # Application Program Command
          # Registered due to being the minimal C1 set for ECMA-43 levels 2 and 3, but is also
          # the _de facto_ C1 set of EUC-JP in terms of what decoders see as valid:
          "105": (None,)*14 + ("SS2", "SS3") + (None,)*16,
          # Small subset, but includes CSI, for CCITT Rec. T.61 Teletex (i.e. accompanies 106 C0):
          "107": (None, None, None, None, None, None, None, None, 
                  None, None, None, "PLD", "PLU", None, None, None,
                  None, None, None, None, None, None, None, None, 
                  None, None, None, "CSI", None, None, None, None),
          # The C1 of the infamous RFC 1345 (IR-111 *cough*), whence Unicode's "figment" aliases:
          "RFC1345": ("PAD", # Padding Character
                  "HOP", # High Octet Preset
                  "BPH", "NBH", "IND", "NEL", "SSA", "ESA", 
                  "HTS", "HTJ", "VTS", "PLD", "PLU", "RI", "SS2", "SS3",
                  "DCS", "PU1", "PU2", "STS", "CCH", "MW", "SPA", "EPA", 
                  "SOS", 
                  "SGCI", # Single Graphical Character Introducer
                  "SCI", "CSI", "ST", "OSC", "PM", "APC"),
          "nil": (None,)*16}

c0bytes = {tuple(b"@"): "001",
           tuple(b"F"): "074",
           tuple(b"G"): "104",
           tuple(b"~"): "nil"}

c1bytes = {tuple(b"C"): "077",
           tuple(b"G"): "105",
           tuple(b"~"): "nil"}

csiseq = {tuple(b"@"): "ICH", # Insert Character
          tuple(b"A"): "CUU", # Cursor Up
          tuple(b"B"): "CUD", # Cursor Down
          tuple(b"C"): "CUF", # Cursor Right [Forward]
          tuple(b"D"): "CUB", # Cursor Left [Backward]
          tuple(b"E"): "CNL", # Cursor Next Line
          tuple(b"F"): "CPL", # Cursor Previous Line
          tuple(b"G"): "CHA", # Cursor Horizontal Absolute
          tuple(b"H"): "CUP", # Cursor Position
          tuple(b"I"): "CHT", # Cursor Forward [Horizontal] Tabulation
          tuple(b"J"): "ED", # Erase in Page [Display]
          tuple(b"K"): "EL", # Erase in Line
          tuple(b"L"): "IL", # Insert Line
          tuple(b"M"): "DL", # Delete Line
          tuple(b"N"): "EF", # Erase in Field
          tuple(b"O"): "EA", # Erase in Area
          tuple(b"P"): "DCH", # Delete Character
          tuple(b"Q"): "SEE", # Select Editing Extent
          tuple(b"R"): "CPR", # Active [Cursor] Position Report
          tuple(b"S"): "SU", # Scroll Up
          tuple(b"T"): "SD", # Scroll Down
          # XTerm initiate highlight mouse tracking seems (per its docs) arg-overloaded on SD?
          tuple(b"U"): "NP", # Next Page
          tuple(b"V"): "PP", # Previous Page
          tuple(b"W"): "CTC", # Cursor Tabulation Control
          tuple(b"X"): "ECH", # Erase Character
          tuple(b"Y"): "CVT", # Cursor Line [Vertical] Tabulation
          tuple(b"Z"): "CBT", # Cursor Backward Tabulation
          tuple(b"["): "SRS", # Start Reversed String
          tuple(b"\\"): "PTX", # Parallel Texts
          tuple(b"]"): "SDS", # Start Directed String
          # XTerm apparantly treats SIMD as an alternative SD syntax due to errors in the 1991
          # printing of ECMA-48?
          tuple(b"^"): "SIMD", # Select Implicit Movement Direction
          tuple(b"`"): "HPA", # Character [Horizontal] Position Absolute
          tuple(b"a"): "HPR", # Character [Horizontal] Position Forward [Relative]
          tuple(b"b"): "REP", # Repeat
          tuple(b"c"): "DA", # Device Attributes (has DEC extensions also)
          tuple(b"d"): "VPA", # Line [Vertical] Position Absolute
          tuple(b"e"): "VPR", # Line [Vertical] Position Forward [Relative]
          tuple(b"f"): "HVP", # Horizontal and Vertical Position
          tuple(b"g"): "TBC", # Tabulation Clear
          tuple(b"h"): "SM", # Set Mode
          tuple(b"i"): "MC", # Media Copy (has DEC extensions also)
          tuple(b"j"): "HPB", # Character [Horizontal] Position Backward
          tuple(b"k"): "VPB", # Line [Vertical] Position Backward
          tuple(b"l"): "RM", # Reset Mode
          tuple(b"m"): "SGR", # Select Graphic Rendition
          tuple(b"n"): "DSR", # Device Status Report (has DEC extensions also)
          tuple(b"o"): "DAQ", # Define Area Qualification
          tuple(b"\x20@"): "SL", # Scroll [Shift] Left
          tuple(b"\x20A"): "SR", # Scroll [Shift] Right
          tuple(b"\x20B"): "GSM", # Graphic Size Modification
          tuple(b"\x20C"): "GSS", # Graphic Size Selection
          tuple(b"\x20E"): "TSS", # Thin Space Specification
          tuple(b"\x20F"): "JFY", # Justify
          tuple(b"\x20G"): "SPI", # Spacing Increment
          tuple(b"\x20H"): "QUAD", # Quad
          tuple(b"\x20I"): "SSU", # Select Size Unit
          tuple(b"\x20J"): "PFS", # Page Format Selection
          tuple(b"\x20K"): "SHS", # Select Character [Horizontal] Spacing
          tuple(b"\x20L"): "SVS", # Select Line [Vertical] Spacing
          tuple(b"\x20M"): "IGS", # Identify Graphic Subrepertoire
          tuple(b"\x20O"): "IDCS", # Identify Device Control String
          tuple(b"\x20P"): "PPA", # Page Position Absolute
          tuple(b"\x20Q"): "PPR", # Page Position Forward [Right]
          tuple(b"\x20R"): "PPB", # Page Position Backward
          tuple(b"\x20S"): "SPD", # Select Presentation Directions
          tuple(b"\x20T"): "DTA", # Dimension Text Area
          tuple(b"\x20U"): "SLH", # Set Line Home
          tuple(b"\x20V"): "SLL", # Set Line Limit
          tuple(b"\x20W"): "FNK", # Function Key
          tuple(b"\x20X"): "SPQR", # Select Print Quality and Rapidity
          tuple(b"\x20Y"): "SEF", # Sheet Eject and Feed
          tuple(b"\x20Z"): "PEC", # Presentation Expand or Contract
          tuple(b"\x20["): "SSW", # Set Space Width
          tuple(b"\x20\\"): "SACS", # Set Additional Character Separation
          tuple(b"\x20]"): "SAPV", # Set Additional Presentation Variants
          tuple(b"\x20^"): "STAB", # Selective Tabulation
          tuple(b"\x20_"): "GCC", # Graphic Character Combination
          tuple(b"\x20`"): "TATE", # Tabulation Aligned Trailing Edge (i.e. set a normal tab stop)
          tuple(b"\x20a"): "TALE", # Tabulation Aligned Leading Edge (i.e. set a "right tab" stop)
          tuple(b"\x20b"): "TAC", # Tabulation Aligned Centred
          tuple(b"\x20c"): "TCC", # Tabulation Centred on Character
          tuple(b"\x20d"): "TSR", # Tabulation Stop Remove
          tuple(b"\x20e"): "SCO", # Select Character Orientation
          tuple(b"\x20f"): "SRCS", # Set Reduced Character Separation
          tuple(b"\x20g"): "SCS", # Select Character Spacing
          tuple(b"\x20h"): "SLS", # Select Line Spacing
          tuple(b"\x20i"): "SPH", # Set Page Home
          tuple(b"\x20j"): "SPL", # Set Page Limit
          tuple(b"\x20k"): "SCP", # Select Character Path
          #
          # Generally recognised corporate-use CSIs
          tuple(b"J?"): "DECSED", # DEC Selective Erase in Display
          tuple(b"K?"): "DECSEL", # DEC Selective Erase in Line
          tuple(b"S?"): "XTCGRP", # XTerm configure graphics (no standard name/mnemonic?)
          tuple(b"T>"): "XTRSTM", # XTerm reset title mode (no standard name/mnemonic?)
          tuple(b"h?"): "DECSET", # DEC Private Mode Set
          tuple(b"l?"): "DECRST", # DEC Private Mode Reset
          tuple(b"m>"): "XTSMR", # XTerm set modifier resource (no standard name/mnemonic?)
          tuple(b"n>"): "XTUMR", # XTerm unset modifier resource (no standard name/mnemonic?)
          tuple(b"p>"): "XTSPM", # XTerm set pointer mode (no standard name/mnemonic?)
          tuple(b"q"): "DECLL", # DEC Load LEDs
          tuple(b"s"): "SCOSC", # SCO Save Cursor Position (collisive with DECSLRM)
          tuple(b"u"): "SCORC", # SCO Restore Cursor Position
          tuple(b"x"): "DECREQTPARM", # DEC Request Terminal Parameters
          tuple(b"\x20q"): "DECSCUSR", # DEC Set Cursor Style
          tuple(b"\x20t"): "DECSWBV", # DEC Set Warning Bell Volume
          tuple(b"\x20u"): "DECSMBV", # DEC Set Margin Bell Volume
          tuple(b"!p"): "DECSTR", # DEC Soft Terminal Reset
          tuple(b"\"p"): "DECSCL", # DEC Set Conformance Level
          tuple(b"\"q"): "DECSCA", # DEC Select Character Protection Attribute
          tuple(b"#p"): "XTPUSHSGR2", # XTerm Push Select Graphic Rendition
          tuple(b"#q"): "XTPOPSGR2", # XTerm Pop Select Graphic Rendition
          tuple(b"#y"): "XTCHECKSUM", # XTerm Select Checksum Extension
          tuple(b"#{"): "XTPUSHSGR", # XTerm Push Select Graphic Rendition
          tuple(b"#|"): "XTREPORTSGR", # XTerm Report Selected Graphic Rendition
          tuple(b"#}"): "XTPOPSGR", # XTerm Pop Select Graphic Rendition
          tuple(b"$p"): "DECRQM", # DEC Request Mode
          tuple(b"$t"): "DECRARA", # DEC Reverse Attributes in Rectangular Area
          tuple(b"$v"): "DECCRA", # DEC Copy Rectangular Area
          tuple(b"$w"): "DECRQPSR", # DEC Request Presentation State Report
          tuple(b"$x"): "DECFRA", # DEC Fill Rectangular Area
          tuple(b"$z"): "DECERA", # DEC Erase Rectangular Area
          tuple(b"${"): "DECSERA", # DEC Selective Erase Rectangular Area
          tuple(b"$|"): "DECSCPP", # DEC Select Columns Per Page
          tuple(b"'w"): "DECEFR", # DEC Enable Filter Rectangle
          tuple(b"'z"): "DECELR", # DEC Enable Locator Reporting
          tuple(b"'{"): "DECSLE", # DEC Select Locator Events
          tuple(b"'|"): "DECRQLP", # DEC Request Locator Position
          tuple(b"'}"): "DECIC", # DEC Insert Columns
          tuple(b"'~"): "DECDC", # DEC Delete Columns
          tuple(b"*x"): "DECSACE", # DEC Select Attribute Change Extent
          tuple(b"*y"): "DECRQCRA", # DEC Request Checksum of Rectangular Area
          tuple(b"*|"): "DECSNLS"} # DEC Select Number of Lines per Screen

# Since the JIS standard behind them is withdrawn, documentation for CEX sequences is pauce.
# Only thing I've been able to find is the "OKI® Programmer’s Reference Manual" released by
# Printronix Inc., which has its own issues, in particular a complete lack of detail on what the
# format of those with parameters is. It also seems to list an incomplete set of CEX sequences
# including only the ones it supports (and not how the 78JIS/83JIS/90JIS diacritic composites were
# supposed to be formed). I'm listing the documented ones without parameters below, insofar as
# I can decipher what it's saying. Mnemonics are made up for this software.
cexseq = {b"J"[0]: "SVP", # Select Vertical Printing
          b"K"[0]: "SHP", # Select Horizontal Printing
          b"N"[0]: "SSP", # Select Superscript Printing
          b"O"[0]: "CSP", # Cancel Superscript Printing
          b"P"[0]: "SSBP", # Select Subscript Printing
          b"Q"[0]: "CSBP", # Cancel Subscript Printing
          b"R"[0]: "SSSP", # Select Super/Subscript Printing (i.e. both on one space, super first)
          b"S"[0]: "CSSP", # Cancel Super/Subscript Printing
          b"-"[0]: "PTAC", # Pair Two ASCII Characters in Vertical Print Mode
          b"p"[0]: "DDWP", # DBCS Double-Width Print
          b"q"[0]: "CDDW", # Cancel DBCS Double-Width Print
          b"r"[0]: "SDHW", # Set DBCS Half-Width Mode
          b"s"[0]: "CDHW", # Cancel DBCS Half-Width Mode
          b"t"[0]: "DSVP", # Disable DBCS ASCII [SBCS???] Vertical Printing Mode 
          b"u"[0]: "ESVP"} # Enable SBCS Vertical Printing Mode (i.e. puts them upright?)

# Not supposed to be an exhaustive list _per se_, nor to follow any specific category:
formats = {0x00AD: 'SHY', 0x061C: 'ALM', 0x180E: 'MVS', 0x200B: 'ZWSP', 0x200C: 'ZWNJ', 
           0x200D: 'ZWJ', 0x200E: 'LRM', 0x200F: 'RLM', 0x2028: 'LSEP', 0x2029: 'PSEP', 
           0x202A: 'LRE', 0x202B: 'RLE', 0x202C: 'PDF', 0x202D: 'LRO', 0x202E: 'RLO', 
           0x2060: 'WJ', 0x2061: 'AF', 0x2062: 'IT', 0x2063: 'IC', 0x2064: 'IP', 
           0x2066: 'LRI', 0x2067: 'RLI', 0x2068: 'FSI', 0x2069: 'PDI', 0x3164: 'HF', 
           0xFEFF: 'ZWNBSP', 0xFFF9: 'IAA', 0xFFFA: 'IAS', 0xFFFB: 'IAT'}






