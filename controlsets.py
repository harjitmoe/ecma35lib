#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

# Transmission controls (aliases TC1 thru TC10):
#    SOH, STX, ETX, EOT, ENQ,
#    ACK, DLE, NAK, SYN, ETB
# These are constrained to appear in their ASCII positions or not at all.

# Format effectors (aliases FE0 thru FE5):
#    BS, HT, LF,
#    VT, FF, CR

# Device controls (aliases DC1 thru DC4):
#    XON, DC2, XOFF, DC4

# Information separators (aliases IS1 thru IS4):
#    US, RS, GS, FS

c0sets = {"001": ("NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", "BS", "HT", "LF", "VT",
                  "FF", "CR", "SO", "SI",
                  "DLE", "XON", "DC2", "XOFF", "DC4", "NAK", "SYN", "ETB", "CAN", "EM", "SUB", 
                  "ESC", "FS", "GS", "RS", "US"),
          # 104 and nil are de facto the same, since (a) ECMA-35 guarantees that ESC is always
          # available at 0x1B, no matter what's designated, and (b) ESC was already processed by
          # tokenfeed (it has to be, for to be able to parse through DOCS regions), so ESC will
          # not reach us here anyway. Include both here anyway for the sake of academic utility.
          "104": (None,)*27 + ("ESC",) + (None,)*4,
          "nil": (None,)*16} 

c1sets = {"105": (None,)*14 + ("SS2", "SS3") + (None,)*16,
          "nil": (None,)*16}

c0bytes = {tuple(b"@"): "001",
           tuple(b"G"): "104",
           tuple(b"~"): "nil"}

c1bytes = {tuple(b"G"): "105",
           tuple(b"~"): "nil"}

def decode_control_sets(stream, *, def_c0="001", def_c1="105"):
    cur_c0 = def_c0, c0sets[def_c0]
    cur_c1 = def_c1, c1sets[def_c1]
    for token in stream:
        if token[0] == "UCS" and token[1] < 0x20:
            token = ("C0", token[1], "UCS")
        elif token[0] == "UCS" and 0x80 <= token[1] < 0xA0:
            token = ("C1", token[1] - 0x80, "UCS")
        # Not elif:
        if token[0] == "CDESIG":
            if token[1] == "C0":
                try:
                    cur_c0 = c0bytes[token[2]], c0sets[c0bytes[token[2]]]
                except KeyError:
                    yield ("ERROR", "UNSUPC0", token[2])
                    cur_c0 = "nil", c0sets["nil"]
            else:
                assert token[1] == "C1"
                try:
                    cur_c1 = c1bytes[token[2]], c1sets[c1bytes[token[2]]]
                except KeyError:
                    yield ("ERROR", "UNSUPC1", token[2])
                    cur_c1 = "nil", c1sets["nil"]
        elif token[0] == "C0":
            ctr = cur_c0[1][token[1]]
            if ctr is None:
                yield ("ERROR", "UNDEFC0", token[1], cur_c0[0])
            else:
                yield ("CTRL", ctr, token[2] + "C0")
        # NOTE: assumes C1 control escape sequences already recognised as such by tokenfeed.
        elif token[0] == "C1":
            ctr = cur_c1[1][token[1]]
            if ctr is None:
                yield ("ERROR", "UNDEFC1", token[1], cur_c1[0])
            else:
                yield ("CTRL", ctr, token[2] + "C1")
        else:
            yield token














