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

fixed_controls = {(0x60,): "DMI", # `
                  (0x61,): "INT", # a
                  (0x62,): "EMI", # b
                  (0x63,): "RIS", # c (this is what the "reset" command does)
                  (0x64,): "CMD", # d
                  #
                  (0x6E,): "LS2", # n
                  (0x6F,): "LS3", # o
                  #
                  (0x7C,): "LS3R", # |
                  (0x7D,): "LS2R", # }
                  (0x7E,): "LS1R"} # ~

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
          "105": (None,)*14 + ("SS2", "SS3") + (None,)*16,
          # The C1 of the infamous RFC 1345 (IR-111 *cough*), whence Unicode's "figment" aliases:
          "rfc": ("PAD", "HOP", "BPH", "NBH", "IND", "NEL", "SSA", "ESA", 
                  "HTS", "HTJ", "VTS", "PLD", "PLU", "RI", "SS2", "SS3",
                  "DCS", "PU1", "PU2", "STS", "CCH", "MW", "SPA", "EPA", 
                  "SOS", "SGCI", "SCI", "CSI", "ST", "OSC", "PM", "APC"),
          "nil": (None,)*16}

c0bytes = {tuple(b"@"): "001",
           tuple(b"G"): "104",
           tuple(b"~"): "nil"}

c1bytes = {tuple(b"C"): "077",
           tuple(b"G"): "105",
           tuple(b"~"): "nil"}






