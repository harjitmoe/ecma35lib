#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Return values: (value, is_error)

def gbv(bytevalue, idx):
    # SLOOOOOOW (the overhead of calling and returning this function will add up FAST).
    # The alternative is nigh unmaintainable though.
    idx -= 1 # ETS 300 706 itself uses one-indexing, so it's less prone to error if we do also.
    return ((bytevalue & (1 << idx)) >> idx)

def read_eighttoseven(byte1):
    """Parse the data from the ETS 300 706 "odd parity" (8/7) check-bit structure."""
    return (byte1 & 0x7F), not (gbv(byte1, 1) ^ gbv(byte1, 2) ^ gbv(byte1, 3) ^ gbv(byte1, 4) ^ 
                                gbv(byte1, 5) ^ gbv(byte1, 6) ^ gbv(byte1, 7) ^ gbv(byte1, 8))

def read_eighttofour(byte1):
    """Parse the data from the ETS 300 706 "8/4" (one-byte Hamming) check-bit structure."""
    nominal = gbv(byte1, 2) | (gbv(byte1, 4) << 1) | (gbv(byte1, 6) << 2) | (gbv(byte1, 8) << 3)
    error1 = not (gbv(byte1, 1) ^ gbv(byte1, 2) ^ gbv(byte1, 6) ^ gbv(byte1, 8))
    error2 = not (gbv(byte1, 2) ^ gbv(byte1, 3) ^ gbv(byte1, 4) ^ gbv(byte1, 8))
    error3 = not (gbv(byte1, 2) ^ gbv(byte1, 4) ^ gbv(byte1, 5) ^ gbv(byte1, 6))
    error4 = not (gbv(byte1, 1) ^ gbv(byte1, 2) ^ gbv(byte1, 3) ^ gbv(byte1, 4) ^ 
                  gbv(byte1, 5) ^ gbv(byte1, 6) ^ gbv(byte1, 7) ^ gbv(byte1, 8))
    if (not error4) and (error1 or error2 or error3):
        return nominal, True
    elif error1 and error2 and error3:
        return (nominal ^ 0x1), False
    elif error2 and error3:
        return (nominal ^ 0x2), False
    elif error1 and error3:
        return (nominal ^ 0x4), False
    elif error1 and error2:
        return (nominal ^ 0x8), False
    else:
        return nominal, True

def read_twentyfourtoeighteen(byte1, byte2, byte3):
    """Parse the data from the ETS 300 706 "24/18" (three-byte Hamming) check-bit structure."""
    nominal = gbv(byte1, 3) | (gbv(byte1, 5) << 1) | (gbv(byte1, 6) << 2) | (gbv(byte1, 7) << 3) |\
              (gbv(byte2, 1) << 4) | (gbv(byte2, 2) << 5) | (gbv(byte2, 3) << 6) | (gbv(byte2, 4) << 7) |\
              (gbv(byte2, 5) << 8) | (gbv(byte2, 6) << 9) | (gbv(byte2, 7) << 10) | (gbv(byte3, 1) << 11) |\
              (gbv(byte3, 2) << 12) | (gbv(byte3, 3) << 13) | (gbv(byte3, 4) << 14) | (gbv(byte3, 5) << 15) |\
              (gbv(byte3, 6) << 16) | (gbv(byte3, 7) << 17)
    error1 = not (gbv(byte1, 1) ^ gbv(byte1, 3) ^ gbv(byte1, 5) ^ gbv(byte1, 7) ^
                  gbv(byte2, 1) ^ gbv(byte2, 3) ^ gbv(byte2, 5) ^ gbv(byte2, 7) ^
                  gbv(byte3, 1) ^ gbv(byte3, 3) ^ gbv(byte3, 5) ^ gbv(byte3, 7))
    error2 = not (gbv(byte1, 2) ^ gbv(byte1, 3) ^ gbv(byte1, 6) ^ gbv(byte1, 7) ^
                  gbv(byte2, 2) ^ gbv(byte2, 3) ^ gbv(byte2, 6) ^ gbv(byte2, 7) ^
                  gbv(byte3, 2) ^ gbv(byte3, 3) ^ gbv(byte3, 6) ^ gbv(byte3, 7))
    error3 = not (gbv(byte1, 4) ^ gbv(byte1, 5) ^ gbv(byte1, 6) ^ gbv(byte1, 7) ^
                  gbv(byte2, 4) ^ gbv(byte2, 5) ^ gbv(byte2, 6) ^ gbv(byte2, 7) ^
                  gbv(byte3, 4) ^ gbv(byte3, 5) ^ gbv(byte3, 6) ^ gbv(byte3, 7))
    error4 = not (gbv(byte1, 8) ^ gbv(byte2, 1) ^ gbv(byte2, 2) ^ gbv(byte2, 3) ^ 
                  gbv(byte2, 4) ^ gbv(byte2, 5) ^ gbv(byte2, 6) ^ gbv(byte2, 7))
    error5 = not (gbv(byte2, 8) ^ gbv(byte3, 1) ^ gbv(byte3, 2) ^ gbv(byte3, 3) ^ 
                  gbv(byte3, 4) ^ gbv(byte3, 5) ^ gbv(byte3, 6) ^ gbv(byte3, 7))
    error6 = not (gbv(byte1, 1) ^ gbv(byte1, 2) ^ gbv(byte1, 3) ^ gbv(byte1, 4) ^ 
                  gbv(byte1, 5) ^ gbv(byte1, 6) ^ gbv(byte1, 7) ^ gbv(byte1, 8) ^ 
                  gbv(byte2, 1) ^ gbv(byte2, 2) ^ gbv(byte2, 3) ^ gbv(byte2, 4) ^ 
                  gbv(byte2, 5) ^ gbv(byte2, 6) ^ gbv(byte2, 7) ^ gbv(byte2, 8) ^ 
                  gbv(byte3, 1) ^ gbv(byte3, 2) ^ gbv(byte3, 3) ^ gbv(byte3, 4) ^ 
                  gbv(byte3, 5) ^ gbv(byte3, 6) ^ gbv(byte3, 7) ^ gbv(byte3, 8))
    if (not error6) and (error1 or error2 or error3 or error4 or error5):
        return nominal, True
    elif error6 and not (error1 or error2 or error3 or error4 or error5):
        return nominal, False
    errorindex = error1 | (error2 << 1) | (error3 << 2) | (error4 << 3) | (error5 << 4)
    if not errorindex:
        return nominal, False
    elif 1 <= errorindex <= 24:
        return nominal ^ (1 << (errorindex - 1)), False
    else:
        return nominal, True






