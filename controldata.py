#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# Transmission controls (aliases TC1 thru TC10):
#    SOH, STX, ETX, EOT, ENQ,
#    ACK, DLE, NAK, SYN, ETB
# These are constrained to appear in their ASCII positions or not at all (whereäs other ASCII 
# controls may not be moved around in the C0 set, but may be moved to the C1 set). Furthermore, 
# they are the only transmission control characters permitted to appear in the C0 set.

# Format effectors (aliases FE0 thru FE5):
#    BS, HT, LF,
#    VT, FF, CR
# These (in addition to GL bytes) may be used in DCS, OSC, PM and APC sequences or follow SCI.

# Device controls (aliases DC1 thru DC4):
#    XON, DC2, XOFF, DC4

# Information separators (aliases IS1 thru IS4):
#    US, RS, GS, FS

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

c0sets = {"001": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                  "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                  "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US"),
          # JIS C 6225's C0 set, differs by replacing IS4 (that is to say, FS) with CEX.
          "074": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                  "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                  "CAN", "EM", "SUB", "ESC", "CEX", "GS", "RS", "US"),
          # 104 and nil are de facto the same, since (a) ECMA-35 guarantees that ESC is always
          # available at 0x1B, no matter what's designated, and (b) ESC was already processed by
          # tokenfeed (it has to be, for to be able to parse through DOCS regions), so ESC will
          # not reach us here anyway. Include both here anyway for the sake of academic utility.
          "104": (None,)*27 + ("ESC",) + (None,)*4,
          "nil": (None,)*16} 

c1sets = {"077": (None, None, "BPH", "NBH", "IND", "NEL", "SSA", "ESA", 
                  "HTS", "HTJ", "VTS", "PLD", "PLU", "RI", "SS2", "SS3",
                  "DCS", "PU1", "PU2", "STS", "CCH", "MW", "SPA", "EPA", 
                  "SOS", None, "SCI", "CSI", "ST", "OSC", "PM", "APC"),
          # Registered due to being the minimal C1 set for ECMA-43 levels 2 and 3, but is also
          # the _de facto_ C1 set of EUC-JP in terms of what decoders see as valid:
          "105": (None,)*14 + ("SS2", "SS3") + (None,)*16,
          # The C1 of the infamous RFC 1345 (IR-111 *cough*), whence Unicode's "figment" aliases:
          "rfc": ("PAD", "HOP", "BPH", "NBH", "IND", "NEL", "SSA", "ESA", 
                  "HTS", "HTJ", "VTS", "PLD", "PLU", "RI", "SS2", "SS3",
                  "DCS", "PU1", "PU2", "STS", "CCH", "MW", "SPA", "EPA", 
                  "SOS", "SGCI", "SCI", "CSI", "ST", "OSC", "PM", "APC"),
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
          tuple(b"U"): "NP", # Next Page
          tuple(b"V"): "PP", # Previous Page
          tuple(b"W"): "CTC", # Cursor Tabulation Control
          tuple(b"X"): "ECH", # Erase Character
          tuple(b"Y"): "CVT", # Cursor Line [Vertical] Tabulation
          tuple(b"Z"): "CBT", # Cursor Backward Tabulation
          tuple(b"["): "SRS", # Start Reversed String
          tuple(b"\\"): "PTX", # Parallel Texts
          tuple(b"]"): "SDS", # Start Directed String
          tuple(b"^"): "SIMD", # Select Implicit Movement Direction
          tuple(b"`"): "HPA", # Character [Horizontal] Position Absolute
          tuple(b"a"): "HPR", # Character [Horizontal] Position Forward [Relative]
          tuple(b"b"): "REP", # Repeat
          tuple(b"c"): "DA", # Device Attributes
          tuple(b"d"): "VPA", # Line [Vertical] Position Absolute
          tuple(b"e"): "VPR", # Line [Vertical] Position Forward [Relative]
          tuple(b"f"): "HVP", # Horizontal and Vertical Position
          tuple(b"g"): "TBC", # Tabulation Clear
          tuple(b"h"): "SM", # Set Mode
          tuple(b"i"): "MC", # Media Copy
          tuple(b"j"): "HPB", # Character [Horizontal] Position Backward
          tuple(b"k"): "VPB", # Line [Vertical] Position Backward
          tuple(b"l"): "RM", # Reset Mode
          tuple(b"m"): "SGR", # Select Graphic Rendition
          tuple(b"n"): "DSR", # Device Status Report
          tuple(b"o"): "DAQ", # Define Area Qualification
          #
          tuple(b"p"): "XTPUSHSGR", # XTerm Push Select Graphic Rendition
          tuple(b"q"): "DECLL", # DEC Load LEDs
          tuple(b"s"): "SCOSC", # SCO Save Cursor Position
          tuple(b"u"): "SCORC", # SCO Restore Cursor Position
          tuple(b"x"): "DECREQTPARM", # DEC Request Terminal Parameters
          #
          tuple(b"\x20@"): "SL", # Scroll Left
          tuple(b"\x20A"): "SR", # Scroll Right
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
          tuple(b"\x20q"): "DECSCUSR", # DEC Set Cursor Style
          tuple(b"\x20t"): "DECSWBV", # DEC Set Warning Bell Volume
          tuple(b"\x20u"): "DECSMBV", # DEC Set Margin Bell Volume
          tuple(b"\"q"): "DECSCA", # DEC Select Character Protection Attribute
          tuple(b"$t"): "DECRARA", # DEC Reverse Attributes in Rectangular Area
          tuple(b"$v"): "DECCRA", # DEC Copy Rectangular Area
          tuple(b"$w"): "DECRQPSR", # DEC Request Presentation State Report
          tuple(b"$x"): "DECFRA", # DEC Fill Rectangular Area
          tuple(b"#q"): "XTPOPSGR", # XTerm Pop Select Graphic Rendition
          tuple(b"#y"): "XTCHECKSUM", # XTerm Select Checksum Extension
          tuple(b"'w"): "DECEFR", # DEC Enable Filter Rectangle
          tuple(b"'z"): "DECELR", # DEC Enable Locator Reporting
          tuple(b"*x"): "DECSACE", # DEC Select Attribute Change Extent
          tuple(b"*y"): "DECRQCRA", # DEC Request Checksum of Rectangular Area
          }

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

# Not supposed to be an exhaustive list per se, nor follow any specific cat:
formats = {0x00AD: 'SHY', 0x061C: 'ALM', 0x180E: 'MVS', 0x200B: 'ZWSP', 0x200C: 'ZWNJ', 
           0x200D: 'ZWJ', 0x200E: 'LRM', 0x200F: 'RLM', 0x2028: 'LSEP', 0x2029: 'PSEP', 
           0x202A: 'LRE', 0x202B: 'RLE', 0x202C: 'PDF', 0x202D: 'LRO', 0x202E: 'RLO', 
           0x2060: 'WJ', 0x2061: 'AF', 0x2062: 'IT', 0x2063: 'IC', 0x2064: 'IP', 
           0x2066: 'LRI', 0x2067: 'RLI', 0x2068: 'FSI', 0x2069: 'PDI', 0x3164: 'HF', 
           0xFEFF: 'ZWNBSP', 0xFFF9: 'IAA', 0xFFFA: 'IAS', 0xFFFB: 'IAT'}






