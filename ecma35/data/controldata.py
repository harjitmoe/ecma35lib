#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Transmission controls (aliases TC1 thru TC10):
#    SOH (SOM), STX (EOA), ETX, EOT, ENQ (WRU), ACK, DLE, NAK, SYN, ETB
# These are constrained to appear in their ASCII positions or not at all (whereäs other ASCII 
# controls may not be moved around in the C0 set, but may be moved to the C1 set). Furthermore, 
# they are the only transmission control characters permitted to appear in the C0 set.
# The 1963 version lacked ETB (see below), and additionally had RU (Are You…).

# Format effectors (aliases FE0 thru FE5):
#    BS, HT, LF, VT, FF, CR
# These (in addition to GL bytes) may be used in DCS, OSC, PM and APC sequences or follow SCI.

# Device controls (aliases DC0 thru DC4):
#    DC0, XON, DC2, XOFF, DC4
# DC0 in the 1963 version was already defined as "device control reserved for data link escape"
# DLE was later re-classified as a transmission control (TC7, rather than DC0).

# Information separators (aliases IS8 thru IS1, or S0 thru S7):
#    S0, S1, S2, S3, FS, GS, RS, US
# The first four were in the 1963 version but later removed (see below).

c0_format_effectors = ["BS", "HT", "LF", "VT", "FF", "CR"]

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
          "ir001": ("NUL", # Null
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
                    # The 1963 ASCII had DC0 instead of TC7, though it was still defined as DLE.
                    "DLE", # Data Link Escape, Transmission Control Seven (TC7).
                    # The XON and XOFF mnemonics are conventional.
                    "XON", # Transmit On, Device Control One (DC1)
                    "DC2", # Device Control Two
                    "XOFF", # Transmit Off, Device Control Three (DC3)
                    "DC4", # Device Control Four
                    "NAK", # Negative Acknowledgement, Error (ERR), Transmission Control Eight (TC8)
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
          # Alternative version with newline (NL) for linefeed. This is listed as a prior agreement
          # permitted alternative in ISO-IR-001. NL and LF are Unicode aliases for the same code.
          # This arrangement is used in some versions of Re-mapped EBCDIC.
          "ir001nl": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                      "BS", "HT", "NL", "VT", "FF", "CR", "SO", "SI", 
                      "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                      "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US"), 
          # Scandinavian newspaper (NATS) controls. Particular perculiarities include commandeering
          # FS as a single-shift and GS/RS/US as EOLs which centre/right-align/justify the
          # terminated line, and changing the mnemonics of HT to be vague and CAN to be specific.
          # UR and LR are used for emphasis, seemingly from SO and SI's typewriter rubric senses.
          # VT and FF are changed to demarcate format instructions, but I don't know their format.
          # I presume the single-shift is supposed to be SS2 (assuming 036 to be related), and 
          # for sure my decode_invocations isn't gonna respond to the "SS" mnemonic.
          "ir007": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
                    "BS",
                    "FO", # Formatting (still seems to be basically a tab in normal contexts).
                    "LF",
                    "ECD", # End of Instruction
                    "SCD", # Start of Instruction
                    "QL", # Quad Left
                    "UR", # Upper Rail (i.e. emphasised, or, the older TTY-ribbon sense of SO).
                    "LR", # Lower Rail
                    "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                    "KW", # Kill Word (sense not massively different from CAN, but more specific).
                    "EM", "SUB", "ESC",
                    "SS2", # Calls it "Super Shift (SS)", but descibes single-shift behaviour.
                    "QC", # Quad Centre
                    "QR", # Quad Right
                    "JY"), # Justify
          # International newspaper (IPTC) controls. Very similar to the NATS controls, but 
          # commandeers DC1/DC2/DC3 for (two orthogonal types of) emphasis, instead of SI/SO.
          "ir026": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
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
          "ir036": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                    "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                    "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                    "CAN", "EM", "SUB", "ESC", "SS2", "GS", "RS", "US"),
          # The International Nuclear Information System (INIS)'s subset of ASCII apparently
          # also subsets its controls to only GS, RS and (the mandatory) ESC.
          "ir048": (None,)*27 + ("ESC", None, "GS", "RS", None),
          #
          # ETS 300 706 C0 set (almost the ITU T.101 Data Syntax 2 Serial Version C1 set)
          "ir056c0": ("ABK", # Alpha Black
                  "ANR", # Alpha Red
                  "ANG", # Alpha Green
                  "ANY", # Alpha Yellow
                  "ANB", # Alpha Blue
                  "ANM", # Alpha Magenta
                  "ANC", # Alpha Cyan
                  "ANW", # Alpha White
                  "FSH", # Flashing
                  "STD", # Steady
                  "EBX", # End Box
                  "SBX", # Start Box
                  "NSZ", # Normal Size
                  "DBH", # Double Height
                  "DBW", # Double Width
                  "DBS", # Double Size
                  "MBK", # Mosaic Black
                  "MSR", # Mosaic Red
                  "MSG", # Mosaic Green
                  "MSY", # Mosaic Yellow
                  "MSB", # Mosaic Blue
                  "MSM", # Mosaic Magenta
                  "MSC", # Mosaic Cyan
                  "MSW", # Mosaic White
                  "CDY", # Conceal Display
                  "SPL", # Stop Lining (Contiguous Mosaic Characters)
                  "STL", # Start Lining (Separated Mosaic Characters)
                  "ESC", # Escape or Switch (toggle between Teletext G0 sets)
                  "BBD", # Black Background
                  "NBD", # New Background
                  "HMS", # Hold Mosaic
                  "RMS"), # Release Mosaic
          # JIS C 6225's C0 set, differs by replacing IS4 (that is to say, FS) with CEX.
          "ir074": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                    "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                    "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                    "CAN", "EM", "SUB", "ESC", 
                    "CEX", # Control Extension (see definitions (that I can find) below)
                    "GS", "RS", "US"),
          # Small subset of ASCII controls plus two single-shifts, for CCITT Rec. T.61 Teletex:
          "ir106": (None, None, None, None, None, None, None, None, 
                    "BS", None, "LF", None, "FF", "CR", "SO", "SI",
                    None, None, None, None, None, None, None, None, 
                    None, "SS2", "SUB", "ESC", None, "SS3", None, None),
          "ir106full": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                        "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                        "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB",
                        "CAN", "SS2", "SUB", "ESC", "FS", "SS3", "RS", "US"),
          # ASCII controls minus the shifts, since apparently some standards require that:
          "ir130": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                    "BS", "HT", "LF", "VT", "FF", "CR", None, None,
                    "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                    "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US"),
          # ITU T.101 Data Syntax 1
          "ir132": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                    "APB", # Active Position Backward
                    "APF", # Active Position Forward
                    "APD", # Active Position Down
                    "APU", # Active Position Up
                    "CS",  # Clear Screen
                    "APR", # Active Position Return
                    "SO", "SI",
                    "DLE", "XON", "DC2", "XOFF",
                    "KMC", # Key-in-Monitor Conceal
                    "NAK", "SYN", "ETB", 
                    "CAN", # Cancel (as usual, but referring to macros)
                    "SS2", "SUB", "ESC",
                    "APS", # Active Position Set
                    "SS3",
                    "APH", # Active Position Home
                    "NSR"), # Non-Selective Reset
          # ITU T.101 Data Syntax 2
          "ir134": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                    "APB", "APF", "APD", "APU", "CS",  "APR", "SO",  "SI",
                    "DLE",
                    "CON", # Cursor On
                    "RPT", # Repeat
                    "XOFF",
                    "COF", # Cursor Off
                    "NAK", "SYN", "ETB", 
                    "CAN", # Cancel (as usual, but erasing rest of line)
                    "SS2", "SUB", "ESC", "FS",
                    "SS3",
                    "APH", # Active Position Home
                    "APA"), # Active Position Address
          # ITU T.101 Data Syntax 3
          "ir135": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                    "APB", "APF", "APD", "APU", "CS", "APR", "SO", "SI",
                    "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                    "CAN", # Cancel (as usual, but referring to macros)
                    "SS2",
                    "SDC", # Service Delimitor Character
                    "ESC", "APS", "SS3", "APH", "NSR"),
          # SS2 replacing EM, was apparently used in Czechoslovakia:
          "ir140": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", 
                    "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
                    "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", 
                    "CAN", "SS2", "SUB", "ESC", "FS", "GS", "RS", "US"),
          # SCSU C0 controls in single-byte mode, as defined by UTR 6.
          # SD* designates and invokes a window, SC* locking shifts to it, SQ* single shifts to it.
          # SQ0 is also used to escape the usual ASCII use of the C0 bytes through.
          # *X is for the supplementary region. *U is for modified UTF-16 (or UCS-2 for SQU).
          # Not actually used like this (no ESC), but here for educational reference:
          #"scsu": ("NUL", "SQ0", "SQ1", "SQ2", "SQ3", "SQ4", "SQ5", "SQ6", 
          #         "SQ7", "HT", "LF", "SDX", None, "CR", "SQU", "SCU",
          #         "SC0", "SC1", "SC2", "SC3", "SC4", "SC5", "SC6", "SC7", 
          #         "SD0", "SD1", "SD2", "SD3", "SD4", "SD5", "SD6", "SD7"),
          #
          # ir104 and nil are de facto the same, since ECMA-35 guarantees that ESC is always
          # available at 0x1B, no matter what's designated.
          "ir104": (None,)*27 + ("ESC", None, None, None, None),
          "nil": (None,)*27 + ("ESC", None, None, None, None),
          "Unknown": (None,)*27 + ("ESC", None, None, None, None)} 

c1sets = {# German bibliographic controls used in DIN 31626
          "ir040": (None, None, None, None, None, None, None,
                  "CUS", # Close-up for Sorting
                  "NSB", # Non-sorting Characters Begin
                  "NSE", # Non-sorting Characters End
                  "FIL", # Filler Character
                  "TCI", # Tag in Context Identifier
                  "ICI", # Identification in Context Identifier
                  # NOTE: decode_control_strings assumes "OSC" is the ANSI OSC, not the DIN OSC:
                  "DINOSC", # Optional Syllabi[fi]cation Control (a "print control", basically SHY)
                  "SS2", # Single Shift Two
                  "SS3", # Single Shift Three
                  None,
                  "EAB", # Embedded Annotation Beginning
                  "EAE", # Embedded Annotation End
                  "ISB", # Item Specification Beginning
                  "ISE", # Item Specification End
                  None, None, None,
                  None,
                  "INC", # Indicator for Nonstandard Character
                  None, None,
                  "KWB", # Keyword Beginning
                  "KWE", # Keyword End
                  "PSB", # Permutation String Beginning
                  "PSE"), # Permutation String End
          # ITU T.101 Data Syntax 2 Serial Version
          "ir056": ("ABK", # Alpha Black
                  "ANR", # Alpha Red
                  "ANG", # Alpha Green
                  "ANY", # Alpha Yellow
                  "ANB", # Alpha Blue
                  "ANM", # Alpha Magenta
                  "ANC", # Alpha Cyan
                  "ANW", # Alpha White
                  "FSH", # Flashing
                  "STD", # Steady
                  "EBX", # End Box
                  "SBX", # Start Box
                  "NSZ", # Normal Size
                  "DBH", # Double Height
                  "DBW", # Double Width
                  "DBS", # Double Size
                  "MBK", # Mosaic Black
                  "MSR", # Mosaic Red
                  "MSG", # Mosaic Green
                  "MSY", # Mosaic Yellow
                  "MSB", # Mosaic Blue
                  "MSM", # Mosaic Magenta
                  "MSC", # Mosaic Cyan
                  "MSW", # Mosaic White
                  "CDY", # Conceal Display
                  "SPL", # Stop Lining
                  "STL", # Start Lining
                  "CSI", # Control Sequence Introducer (see definitions below)
                  "BBD", # Black Background
                  "NBD", # New Background
                  "HMS", # Hold Mosaic
                  "RMS"), # Release Mosaic
          # Bibliographic controls from pre-1985 ISO 6630; closely related to the DIN controls but 
          # omits several, and adds four more controls in space unused by the DIN controls.
          # As such doesn't collide with DIN at any point, unlike its IRR replacement ir124.
          "ir067": (None, None, None, None, None, None, None, "CUS",
                  "NSB", "NSE", None, None, None, None, None, None,
                  None, "EAB", "EAE", None, None,
                  "SIB", # Sorting Interpolation Beginning
                  "SIE", # Sorting Interpolation End
                  "SSB", # Secondary Sorting Value Beginning
                  "SSE", # Secondary Sorting Value End
                  None, None, None, "KWB", "KWE", "PSB", "PSE"),
          # WIP ITU T.101 Data Syntax 2 Parallel Version
          "ir073": ("BKF", # Black Foreground
                  "RDF", # Red Foreground
                  "GRF", # Green Foreground
                  "YLF", # Yellow Foreground
                  "BLF", # Blue Foreground
                  "MGF", # Magenta Foreground
                  "CNF", # Cyan Foreground
                  "WHF", # White Foreground
                  "FSH", # Flashing
                  "STD", # Steady
                  "EBX", # End Box
                  "SBX", # Start Box
                  "NSZ", # Normal Size
                  "DBH", # Double Height
                  "DBW", # Double Width
                  "DBS", # Double Size
                  "BKB", # Black Background
                  "RDB", # Red Background
                  "GRB", # Green Background
                  "YLB", # Yellow Background
                  "BLB", # Blue Background
                  "MGB", # Magenta Background
                  "CNB", # Cyan Background
                  "WHB", # White Background
                  "CDY", # Conceal Display
                  "SPL", # Stop Lining
                  "STL", # Start Lining
                  "CSI", # Control Sequence Introducer (see definitions below)
                  "NPO", # Normal Polarity
                  "IPO", # Inverse Polarity
                  "TRB", # Transparent Background
                  "SCD"), # Stop Conceal
          # Those of the "ANSI escape" codes (ECMA-48) which occupy the C1 area:
          "ir077": (None, # Vacant
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
                  "SS2", "SS3", 
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
                  "CSI", # Control Sequence Introducer (see definitions below)
                  "ST", # String Terminator
                  "OSC", # Operating System Command
                  "PM", # Privacy Message
                  "APC"), # Application Program Command
          # Registered due to being the minimal C1 set for ECMA-43 levels 2 and 3, but is also
          # the _de facto_ C1 set of EUC-JP in terms of what decoders see as valid:
          "ir105": (None,)*14 + ("SS2", "SS3") + (None,)*16,
          # Small subset, but includes CSI, for CCITT Rec. T.61 Teletex (i.e. accompanies 106 C0):
          "ir107": (None, None, None, None, None, None, None, None, 
                  None, None, None, "PLD", "PLU", None, None, None,
                  None, None, None, None, None, None, None, None, 
                  None, None, None, "CSI", None, None, None, None),
          # Bibliographic controls from ISO 6630:1985; adds PLD and PLU in their ANSI locations
          # (corresponding to TCI and ICI in DIN, and as such breaking the earlier ir067 property 
          # of not colliding with DIN on any control code).
          "ir124": (None, None, None, None, None, None, None, "CUS",
                  "NSB", "NSE", None, "PLD", "PLU", None, None, None,
                  None, "EAB", "EAE", None, None, "SIB", "SIE", "SSB",
                  "SSE", None, None, None, "KWB", "KWE", "PSB", "PSE"),
          # MARC-8 control codes. Or rather, NSB, NSE, ZWJ and ZWNJ are. The rest are just included
          #   so that this can be validly be treated as an alternative for the ir124 escape seq.
          "ir124-marc": (None, None, None, None, None, None, None, "CUS",
                  "NSB", "NSE", None, "PLD", "PLU", "ZWJ", "ZWNJ", None,
                  None, "EAB", "EAE", None, None, "SIB", "SIE", "SSB",
                  "SSE", None, None, None, "KWB", "KWE", "PSB", "PSE"),
          # ITU T.101 Data Syntax 1
          "ir133": ("BKF", # Black Foreground
                  "RDF", # Red Foreground
                  "GRF", # Green Foreground
                  "YLF", # Yellow Foreground
                  "BLF", # Blue Foreground
                  "MGF", # Magenta Foreground
                  "CNF", # Cyan Foreground
                  "WHF", # White Foreground
                  "SSZ", # Small Size
                  "MSZ", # Medium Size
                  "NSZ", # Normal Size
                  "SZX", # Size Control
                  None, # Vacant
                  None, # Vacant
                  "CON", # Cursor On
                  "COF", # Cursor Off
                  "COL", # Background or Foreground Colour
                  "FLC", # Flashing Control
                  "CDC", # Concel Display Control
                  None, # Vacant
                  None, # Vacant
                  "P-MACRO", # Photo Macro
                  None, # Vacant
                  None, # Vacant
                  "RPC", # Repeat Control
                  "SPL", # Stop Lining
                  "STL", # Start Lining
                  None, # Vacant
                  None, # Vacant
                  None, # Vacant
                  "UNP", # Unprotected
                  "PRT"), # Protected
          # ITU T.101 Data Syntax 3
          "ir136": ("DEFM", # Define Macro
                  "DEFP", # Define P-Macro
                  "DEFT", # Define Transmit-Macro
                  "DEFD", # Define DRCS
                  "DEFX", # Define Textrue
                  "END", # End
                  "REP", # Repeat
                  "REPE", # Repeat to End of Line
                  "REVV", # Reverse Video
                  "NORV", # Normal Video
                  "SMTX", # Small Text
                  "METX", # Medium Text
                  "NOTX", # Normal Text
                  "DBH", # Double Height
                  "BSTA", # Blink Start
                  "DBS", # Double Size
                  "PRO", # Protect
                  None, # Vacant (EDC1)
                  None, # Vacant (EDC2)
                  None, # Vacant (EDC3)
                  None, # Vacant (EDC4)
                  "WWON", # Word Wrap On
                  "WWOF", # Word Wrap Off
                  "SCON", # Scroll On
                  "SCOF", # Scroll Off
                  "USTA", # Underline Start
                  "USTO", # Underline Stop
                  "FLC", # Flash Cursor
                  "STC", # Steady Cursor
                  "COF", # Cursor Off
                  "BSTO", # Blink Stop
                  "UNP"), # Unprotect
          # The C1 of the infamous RFC 1345 (IR-111 *cough*), whence Unicode's "figment" aliases:
          "RFC1345": ("PAD", # Padding Character
                  "HOP", # High Octet Preset
                  "BPH", "NBH", "IND", "NEL", "SSA", "ESA", 
                  "HTS", "HTJ", "VTS", "PLD", "PLU", "RI", "SS2", "SS3",
                  "DCS", "PU1", "PU2", "STS", "CCH", "MW", "SPA", "EPA", 
                  "SOS", 
                  "SGCI", # Single Graphical Character Introducer
                  "SCI", "CSI", "ST", "OSC", "PM", "APC"),
          # EBCDIC, as translated using the EBCDIC bytes table from UTR 16 and/or others.
          # Names and mnemonics: 
          # IA 20180911044845 https://www-01.ibm.com/software/globalization/cdra/appendix_g1.html
          "c1ebcdic": ("DS", # Digit Select
                       "IBMSOS", # Start of Significance
                       "IBMFS", # Field Separator
                       "WUS", # Word Underscore (i.e. underline previous word)
                       "BYP/INP", # Bypass or Inhibit Presentation (i.e. ignore printing chars)
                       "NL/LF", # NL or LF, whichever isn't being mapped to the C0 set.
                       "RNL", # Required Newline (i.e. cancelling indent)
                       "POC", # Program Operator Communication (takes two bytes: action, effector)
                       "SA", # Set Attribute (deprecated in favour of CSP)
                       "SFE", # Start Field Extended (deprecated in favour of CSP)
                       "SM/SW", # Set Mode or Switch
                       "CSP", # Ctrl Seq Prefx (bytes: class, len (inc. len byte), type, params)
                       "MFA", # Modify Field Attribute (deprecated in favour of CSP)
                       "SPS", # Superscript (fractional linefeed up, pretty much PLU)
                       "RPT", # Repeat
                       "CU1", # Customer Use One
                       None, None, 
                       "UBS", # Unit Backspace (i.e. partial backspace)
                       "IR", # Index Return (functions as either NL or US; name evokes IND+CR)
                       "PP", # Presentation Position
                       "TRN", # Transparant (takes len byte (not counting len byte) then raw data)
                       "NBS", # Numeric Backspace (i.e. negative figure-space)
                       "GE", # Graphic Escape (EBCDIC single shift)
                       "SBS", # Subscript (fractional linefeed down, pretty much PLD)
                       "IT", # Indent Tab (i.e. HT now and after every NL until a RNL or RFF)
                       "RFF", # Required Form Feed (i.e. cancelling indent)
                       "CU3", # Customer Use Three (apparently no CU2)
                       "SEL", # Select (followed by one byte to command a device)
                       "RES/ENP", # Restore or Enable Presentation (i.e. end a BYP/INP)
                       None, 
                       "EO"), # Eight Ones
          "nil": (None,)*16,
          "Unknown": (None,)*16}

c0bytes = {tuple(b"@"): ("ir001", ("ir001nl",), ("ir001",)),
           tuple(b"A"): "ir007",
           tuple(b"B"): "ir048",
           tuple(b"C"): "ir026",
           tuple(b"D"): "ir036",
           tuple(b"E"): "ir105",
           tuple(b"F"): "ir074",
           tuple(b"G"): "ir104",
           tuple(b"H"): "ir130",
           tuple(b"I"): "ir132",
           tuple(b"J"): "ir134",
           tuple(b"K"): "ir135",
           tuple(b"L"): "ir140",
           tuple(b"~"): "nil"}

c1bytes = {tuple(b"@"): "ir056",
           tuple(b"A"): "ir073",
           tuple(b"B"): ("ir124-marc", # Preferred version
                         ("ir124-marc",), # Private versions
                         ("ir067", "ir124")), # Original followed by any registered revisions
           tuple(b"C"): ("RFC1345", ("RFC1345",), ("ir077",)),
           tuple(b"D"): "ir133",
           tuple(b"E"): "ir040",
           tuple(b"F"): "ir136",
           tuple(b"G"): "ir105",
           tuple(b"H"): "ir107",
           tuple(b"!1"): "c1ebcdic",
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
          # Some deployed corporate-use CSIs
          tuple(b"J?"): "DECSED", # DEC Selective Erase in Display
          tuple(b"K?"): "DECSEL", # DEC Selective Erase in Line
          tuple(b"S?"): "XTCGPH", # XTerm configure graphics (no standard name/mnemonic?)
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
          tuple(b"\x20p"): "DECSSCLS", # DEC Set Scroll Speed
          tuple(b"\x20q"): "DECSCUSR", # DEC Set Cursor Style
          tuple(b"\x20r"): "DECSKCV", # DEC Set Key Click Volume
          tuple(b"\x20t"): "DECSWBV", # DEC Set Warning Bell Volume
          tuple(b"\x20u"): "DECSMBV", # DEC Set Margin Bell Volume
          tuple(b"\x20v"): "DECSLCK", # DEC Set Lock Key Style
          tuple(b"!p"): "DECSTR", # DEC Soft Terminal Reset
          tuple(b"\"p"): "DECSCL", # DEC Set Conformance Level
          tuple(b"\"q"): "DECSCA", # DEC Select Character Protection Attribute
          tuple(b"\"t"): "DECSRFR", # DEC Select Refresh Rate
          tuple(b"#p"): "XTPUSHSGR2", # XTerm Push Select Graphic Rendition
          tuple(b"#q"): "XTPOPSGR2", # XTerm Pop Select Graphic Rendition
          tuple(b"#y"): "XTCHECKSUM", # XTerm Select Checksum Extension
          tuple(b"#{"): "XTPUSHSGR", # XTerm Push Select Graphic Rendition
          tuple(b"#|"): "XTREPORTSGR", # XTerm Report Selected Graphic Rendition
          tuple(b"#}"): "XTPOPSGR", # XTerm Pop Select Graphic Rendition
          tuple(b"$p"): "DECRQM", # DEC Request Mode
          tuple(b"$q"): "DECSDDT", # DEC (Set?) Disconnect Delay Time
          tuple(b"$r"): "DECCARA", # DEC Change Attribute in Rectangle
          tuple(b"$s"): "DECSPRTT", # DEC Select Printer Type
          tuple(b"$t"): "DECRARA", # DEC Reverse Attributes in Rectangular Area
          tuple(b"$u"): "DECRQTSR", # DEC Request Terminal State Report
          tuple(b"$v"): "DECCRA", # DEC Copy Rectangular Area
          tuple(b"$w"): "DECRQPSR", # DEC Request Presentation State Report
          tuple(b"$x"): "DECFRA", # DEC Fill Rectangular Area
          tuple(b"$y"): "DECRPRTMDE", # DEC Report Mode (no standard name/mnemonic?)
          tuple(b"$z"): "DECERA", # DEC Erase Rectangular Area
          tuple(b"${"): "DECSERA", # DEC Selective Erase Rectangular Area
          tuple(b"$|"): "DECSCPP", # DEC Select Columns Per Page
          tuple(b"$}"): "DECSASD", # DEC Select Active Status Display
          tuple(b"$~"): "DECSSDT", # DEC Select Status Display (Line) Type
          tuple(b"'w"): "DECEFR", # DEC Enable Filter Rectangle
          tuple(b"'z"): "DECELR", # DEC Enable Locator Reporting
          tuple(b"'{"): "DECSLE", # DEC Select Locator Events
          tuple(b"'|"): "DECRQLP", # DEC Request Locator Position
          tuple(b"'}"): "DECIC", # DEC Insert Columns
          tuple(b"'~"): "DECDC", # DEC Delete Columns
          tuple(b")p"): "DECSDPT", # DEC Select Digital Printed Data Type
          tuple(b"*p"): "DECSPPCS", # DEC Select ProPrinter Character Set [i.e. IBM codepage]
          tuple(b"*r"): "DECSCS", # DEC Select Communication Speed
          tuple(b"*u"): "DECSCP", # DEC Select Communication Port
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

# https://www.unicode.org/L2/L2020/20007-abbreviations.pdf
# https://www.unicode.org/L2/L2020/20010-charts-text.pdf
#   These are obviously provisional, but I do not expect them to be redefined for other uses.
# Note: don't include C0s and C1s here. SP and DEL are not strictly C0s or C1s since ECMA-35 does 
#   not delegate them to the C0 and C1 sets. Although ESC isn't delegated either.
formats = { 0x0020: 'SP', # Space
            0x007F: 'DEL', # Delete
            0x00A0: 'NBSP', # Non-Breaking Space, No-Break Space, Required Space (RSP)
            0x00AD: 'SHY', # Soft Hyphen
            0x034F: 'CGJ', # Combining Grapheme "Joiner"
            # TODO: U+0601, U+0603, U+0604
            0x0600: 'ANS', # Arabic Number Sign
            0x0602: 'AFM', # Arabic Footnote Marker
            0x0605: 'ANMA', # Arabic Number Mark Above
            0x061C: 'ALM', # Arabic Letter Mark
            0x06DD: 'AEOA', # Arabic End Of Ayah
            0x070F: 'SAM', # Syriac Abbreviation Mark
            0x08E2: 'ADEOA', # Arabic Disputed End Of Ayah
            0x1680: 'OGSP', # Ogham Space Mark
            0x180E: 'MVS', # Mongolian Vowel Separator
            0x2000: 'NQSP', # En Quad Space, En Quad
            0x2001: 'MQSP', # Em Quad Space, Em Quad
            0x2002: 'ENSP', # En Space
            0x2003: 'EMSP', # Em Space
            0x2004: 'EMSP13', # 1/3 Em Space, Three Per Em Space (THPMSP)
            0x2005: 'EMSP14', # 1/4 Em Space, Four Per Em Space (FPMSP)
            0x2006: 'EMSP16', # 1/6 Em Space, Six Per Em Space (SPMSP)
            0x2007: 'FSP', # Figure Space, Numeric Space (NSP, NUMSP)
            0x2008: 'PSP', # Punctuation Space
            0x2009: 'THSP', # Thin Space
            0x200A: 'HSP', # Hair Space
            0x200B: 'ZWSP', # Zero Width Space
            0x200C: 'ZWNJ', # Zero Width Non Joiner
            0x200D: 'ZWJ', # Zero Width Joiner
            0x200E: 'LRM', # Left to Right Mark
            0x200F: 'RLM', # Right to Left Mark
            0x2028: 'LSEP', # Line Separator (also LS)
            0x2029: 'PSEP', # Paragraph Separator (also PS)
            0x202A: 'LRE', # Left to Right Embedding
            0x202B: 'RLE', # Right to Left Embedding
            0x202C: 'PDF', # Pop Directional Formatting
            0x202D: 'LRO', # Left to Right Override
            0x202E: 'RLO', # Right to Left Override
            0x202F: 'NNBSP', # Narrow Non-Breaking Space, Narrow No-Break Space
            0x205F: 'MMSP', # Medium Mathematical Space
            0x2060: 'WJ', # Word Joiner
            0x2061: 'FA', # Function Application
            0x2062: 'IMS', # Invisible Times
            0x2063: 'IS', # Invisible Separator
            0x2064: 'IPS', # Invisible Plus
            0x2066: 'LRI', # Left to Right Isolate
            0x2067: 'RLI', # Right to Left Isolate
            0x2068: 'FSI', # First Strong Isolate
            0x2069: 'PDI', # Pop Directional Isolate 
            0x206A: 'ISS', # Inhibit Symmetric Swapping
            0x206B: 'ASS', # Activate Symmetric Swapping 
            0x206C: 'IAFS', # Inhibit Arabic Form Shaping
            0x206D: 'AAFS', # Activate Arabic Form Shaping
            0x206E: 'NADS', # National Digit Shapes
            0x206F: 'NODS', # Nominal Digit Shapes
            0x3000: 'IDSP', # Ideographic Space
            0x3164: 'HF', # Hangul Filler
            0xFEFF: 'BOM', # Byte-Order Mark, Zero Width Non-Breaking Space (ZWNBSP)
            0xFFA0: 'HWHF', # Halfwidth Hangul Filler
            0xFFF9: 'IAA', # Interlinear Annotation Anchor
            0xFFFA: 'IAS', # Interlinear Annotation Separator
            0xFFFB: 'IAT', # Interlinear Annotation Terminator
            0x110BD: 'KNS', # Kaithi Number Sign
            0x13430: 'EHVJ', # Egyptian Hieroglyph Vertical Joiner
            0x13431: 'EHHJ', # Egyptian Hieroglyph Horizontal Joiner
            0x13432: 'EHITS', # Egyptian Hieroglyph Insert-at-Top Start
            0x13433: 'EHIBS', # Egyptian Hieroglyph Insert-at-Bottom Start
            0x13434: 'EHITE', # Egyptian Hieroglyph Insert-at-Top End (EHITJ is likely a typo)
            0x13435: 'EHIBE', # Egyptian Hieroglyph Insert-at-Bottom ENd
            0x13436: 'EHOM', # Egyptian Hieroglyph Overlay Middle
            0x13437: 'EHBS', # Egyptian Hieroglyph Begin Segment
            0x13438: 'EHES', # Egyptian Hieroglyph End Segment
            0x1BCA0: 'SHLO', # Shorthand Format Letter Overlap
            0x1BCA1: 'SHCO', # Shorthand Format Continuing Overlap
            0x1BCA2: 'SHDS', # Shorthand Format Down Step
            0x1BCA3: 'SHUS', # Shorthand Format Up Step
            0x1D173: 'MNBB', # Musical Symbol Begin Beam
            0x1D174: 'MNEB', # Musical Symbol End Beam
            0x1D175: 'MNBT', # Musical Symbol Begin Tie
            0x1D176: 'MNET', # Musical Symbol End Tie
            0x1D177: 'MNBS', # Musical Symbol Begin Slur
            0x1D178: 'MNES', # Musical Symbol End Slur
            0x1D179: 'MNBP', # Musical Symbol Begin Phrase
            0x1D17A: 'MNEP', # Musical Symbol End Phrase
            # Tag characters
            0xE0001: 'TAG{BEGIN}',
            0xE0020: 'TAG{SP}', 0xE0021: 'TAG{EXCL}', 0xE0022: 'TAG{QUOT}', 0xE0023: 'TAG{NUM}',
            0xE0024: 'TAG{DOLLAR}', 0xE0025: 'TAG{PERCNT}', 0xE0026: 'TAG{AMP}',
            0xE0027: 'TAG{APOS}', 0xE0028: 'TAG{LPAR}', 0xE0029: 'TAG{RPAR}', 0xE002A: 'TAG{AST}',
            0xE002B: 'TAG{PLUS}', 0xE002C: 'TAG{COMMA}', 0xE002D: 'TAG{-}', 0xE002E: 'TAG{PERIOD}',
            0xE002F: 'TAG{SOL}', 0xE0030: 'TAG{0}', 0xE0031: 'TAG{1}', 0xE0032: 'TAG{2}',
            0xE0033: 'TAG{3}', 0xE0034: 'TAG{4}', 0xE0035: 'TAG{5}', 0xE0036: 'TAG{6}',
            0xE0037: 'TAG{7}', 0xE0038: 'TAG{8}', 0xE0039: 'TAG{9}', 0xE003A: 'TAG{COLON}',
            0xE003B: 'TAG{SEMI}', 0xE003C: 'TAG{LT}', 0xE003D: 'TAG{EQUALS}', 0xE003E: 'TAG{GT}',
            0xE003F: 'TAG{QUEST}', 0xE0040: 'TAG{COMMAT}', 0xE0041: 'TAG{A}', 0xE0042: 'TAG{B}',
            0xE0043: 'TAG{C}', 0xE0044: 'TAG{D}', 0xE0045: 'TAG{E}', 0xE0046: 'TAG{F}',
            0xE0047: 'TAG{G}', 0xE0048: 'TAG{H}', 0xE0049: 'TAG{I}', 0xE004A: 'TAG{J}',
            0xE004B: 'TAG{K}', 0xE004C: 'TAG{L}', 0xE004D: 'TAG{M}', 0xE004E: 'TAG{N}',
            0xE004F: 'TAG{O}', 0xE0050: 'TAG{P}', 0xE0051: 'TAG{Q}', 0xE0052: 'TAG{R}',
            0xE0053: 'TAG{S}', 0xE0054: 'TAG{T}', 0xE0055: 'TAG{U}', 0xE0056: 'TAG{V}',
            0xE0057: 'TAG{W}', 0xE0058: 'TAG{X}', 0xE0059: 'TAG{Y}', 0xE005A: 'TAG{Z}',
            0xE005B: 'TAG{LSQB}', 0xE005C: 'TAG{BSOL}', 0xE005D: 'TAG{RSQB}', 0xE005E: 'TAG{HAT}',
            0xE005F: 'TAG{UNDERBAR}', 0xE0060: 'TAG{GRAVE}', 0xE0061: 'TAG{a}',
            0xE0062: 'TAG{b}', 0xE0063: 'TAG{c}', 0xE0064: 'TAG{d}', 0xE0065: 'TAG{e}',
            0xE0066: 'TAG{f}', 0xE0067: 'TAG{g}', 0xE0068: 'TAG{h}', 0xE0069: 'TAG{i}',
            0xE006A: 'TAG{j}', 0xE006B: 'TAG{k}', 0xE006C: 'TAG{l}', 0xE006D: 'TAG{m}',
            0xE006E: 'TAG{n}', 0xE006F: 'TAG{o}', 0xE0070: 'TAG{p}', 0xE0071: 'TAG{q}',
            0xE0072: 'TAG{r}', 0xE0073: 'TAG{s}', 0xE0074: 'TAG{t}', 0xE0075: 'TAG{u}',
            0xE0076: 'TAG{v}', 0xE0077: 'TAG{w}', 0xE0078: 'TAG{x}', 0xE0079: 'TAG{y}',
            0xE007A: 'TAG{z}', 0xE007B: 'TAG{LBRACE}', 0xE007C: 'TAG{VERT}',
            0xE007D: 'TAG{RBRACE}', 0xE007E: 'TAG{~}',
            0xE007F: 'TAG{END}',
}
rformats = dict(zip(formats.values(), formats.keys()))






