#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020, 2021.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

abbreviations = {
    "ASCII": "American Standard Code for Information Interchange",
    "LAT1S": "Latin-1 Supplement",
    "HJ": "Hangul Jamo",
    "RAD": "Code-point for a radical",
    "HCJ": "Hangul Element / Compatibility Jamo",
    "STRK": "Code-point for a stroke",
    "CJKA": "Chinese/Japanese/Korean Extension A",  
    "URO": "Unified Repertoire and Ordering",
    "URO+": "Appendage to Unified Repertoire and Ordering", 
    "HJXA": "Hangul Jamo, Extended A",
    "HS": "Hangul Syllable",
    "HJXB": "Hangul Jamo, Extended B",
    "PUA": "Private Use Area",
    "DD": "Dirty Dozen (of unified ideographs in the Compatibility Ideographs block)",
    "CI": "Compatibility Ideograph",
    "VF": "Vertical Form",
    "VCF": "Compatibility Form (Vertical)",
    "CF": "Compatibility Form",
    "SFV": "Small Form Variant",
    "FWF": "Full-Width Form",
    "REPL": "Replacement Character",
    "BMP": "Miscellaneous Basic Multilingual Plane",
    "SMP": "Supplementary Multilingual Plane",
    "CJKB": "Chinese/Japanese/Korean Extension B",
    "CJKB+": "Appendage to Chinese/Japanese/Korean Extension B",
    "CJKC": "Chinese/Japanese/Korean Extension C",
    "CJKD": "Chinese/Japanese/Korean Extension D",
    "CJKE": "Chinese/Japanese/Korean Extension E",  
    "CJKF": "Chinese/Japanese/Korean Extension F",  
    "CIS": "Compatibility Ideographs Supplement",
    "SIP": "Miscellaneous Supplementary Ideographic Plane",
    "CJKG": "Chinese/Japanese/Korean Extension G",
    "TIP": "Miscellaneous Tertiary Ideographic Plane", 
    "SSP": "Supplementary Special-purpose Plane",
    "SPUA": "Supplementary Private-Use Area A",
    "SPUB": "Supplementary Private-Use Area B",
    "ASTR": "Other Astral Plane",
    "BPUP": "Beyond-Unicode Private-Use Planes",
    "BPUG": "Beyond-Unicode Private-Use Groups",
    "BYND": "Beyond Unicode, not Private Use",
}

def initialism(codepoint):
    #####################################
    # BASIC MULTILINGUAL PLANE
    if codepoint < 0x80:
        return "ASCII"
    elif 0x80 <= codepoint < 0x100:
        return "LAT1S"
    elif 0x1100 <= codepoint < 0x1200:
        return "HJ"
    elif 0x2E80 <= codepoint < 0x2FE0:
        return "RAD"
    elif 0x3130 <= codepoint < 0x3190:
        return "HCJ"
    elif 0x31C0 <= codepoint < 0x31F0:
        return "STRK"
    elif 0x3400 <= codepoint < 0x4DC0:
        return "CJKA"
    elif 0x4E00 <= codepoint < 0x9FA6:
        return "URO"
    elif 0x9FA6 <= codepoint < 0xA000:
        return "URO+"
    elif 0xA960 <= codepoint < 0xA980:
        return "HJXA"
    elif 0xAC00 <= codepoint < 0xD7B0:
        return "HS"
    elif 0xD7B0 <= codepoint < 0xD800:
        return "HJXB"
    elif 0xE000 <= codepoint < 0xF900:
        return "PUA"
    elif 0xF900 <= codepoint < 0xFB00: # the BMP's Compatibility Ideographs block
        if codepoint in (0xFA0E, 0xFA0F, 0xFA11, 0xFA13, 0xFA14, 0xFA1F,
                    0xFA21, 0xFA23, 0xFA24, 0xFA27, 0xFA28, 0xFA29):
            return "DD"
        else:
            return "CI"
    elif 0xFE10 <= codepoint < 0xFE20:
        return "VF"
    elif 0xFE30 <= codepoint < 0xFE50:
        if (codepoint <= 0xFE44) or (codepoint in (0xFE47, 0xFE48)):
            return "VCF"
        else:
            return "CF"
    elif 0xFE50 <= codepoint < 0xFE70:
        return "SFV"
    elif (0xFF01 <= codepoint < 0xFF61) or (0xFFE0 <= codepoint < 0xFFE7):
        return "FWF"
    elif codepoint in (0xFFFC, 0xFFFD):
        return "REPL"
    elif codepoint < 0x10000:
        return "BMP"
    #####################################
    # SUPPLEMENTARY MULTILINGUAL PLANE
    elif 0x10000 <= codepoint < 0x20000:
        return "SMP"
    #####################################
    # SUPPLEMENTARY IDEOGRAPHIC PLANE
    elif 0x20000 <= codepoint < 0x2A6D7:
        return "CJKB"
    elif 0x2A6D7 <= codepoint < 0x2A6E0:
        return "CJKB+"
    elif 0x2A700 <= codepoint < 0x2B740:
        return "CJKC"
    elif 0x2B740 <= codepoint < 0x2B820:
        return "CJKD"
    elif 0x2B820 <= codepoint < 0x2CEB0:
        return "CJKE"
    elif 0x2CEB0 <= codepoint < 0x2EBF0:
        return "CJKF"
    elif 0x2F800 <= codepoint < 0x2FA20:
        return "CIS"
    elif 0x20000 <= codepoint < 0x30000:
        return "SIP"
    #####################################
    # TERTIARY IDEOGRAPHIC PLANE
    elif 0x30000 <= codepoint < 0x31350:
        return "CJKG"
    elif 0x30000 <= codepoint < 0x40000:
        return "TIP"
    #####################################
    # SUPPLEMENTARY SPECIAL-PURPOSE PLANE
    elif 0xE0000 <= codepoint < 0xF0000:
        return "SSP"
    #####################################
    # SUPPLEMENTARY PRIVATE USE AREA
    elif 0xF0000 <= codepoint < 0x100000:
        return "SPUA"
    elif codepoint >= 0x100000:
        return "SPUB"
    #####################################
    # ANY OTHER PLANE WITHIN UNICODE
    elif codepoint < 0x100000000:
        return "ASTR"
    #####################################
    # BEYOND-UNICODE PRIVATE USE AREA
    elif 0xE00000 <= codepoint < 0x1000000:
        return "BPUP"
    elif 0x60000000 <= codepoint < 0x100000000:
        return "BPUG"
    #####################################
    # OTHERWISE BEYOND UNICODE
    else:
        return "BYND"

