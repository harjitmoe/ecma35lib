#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# ANSEL (ANSI/NISO Z39.47), vanilla (without an eszett)
graphdata.gsets["ir231"] = (94, 1, (
                         (0x0141,),  (0x00D8,),  (0x0110,), 
             (0x00DE,),  (0x00C6,),  (0x0152,),  (0x02B9,),
             (0x00B7,),  (0x266D,),  (0x00AE,),  (0x00B1,), 
             (0x01A0,),  (0x01AF,),  (0x02BC,),  None, 
             (0x02BB,),  (0x0142,),  (0x00F8,),  (0x0111,), 
             (0x00FE,),  (0x00E6,),  (0x0153,),  (0x02BA,), 
             (0x0131,),  (0x00A3,),  (0x00F0,),  None,      
             (0x01A1,),  (0x01B0,),  None,       None, 
             (0x00B0,),  (0x2113,),  (0x2117,),  (0x00A9,), 
             (0x266F,),  (0x00BF,),  (0x00A1,),  None,
             None,       None,       None,       None, 
             None,       None,       None,       None,  
             None,       None,       None,       None,      
             None,       None,       None,       None, 
             None,       None,       None,       None,      
             None,       None,       None,       None, 
             (-0x0309,), (-0x0300,), (-0x0301,), (-0x0302,), 
             (-0x0303,), (-0x0304,), (-0x0306,), (-0x0307,), 
             (-0x0308,), (-0x030C,), (-0x030A,), (-0xFE20,), 
             (-0xFE21,), (-0x0315,), (-0x030B,), (-0x0310,), 
             (-0x0327,), (-0x0328,), (-0x0323,), (-0x0324,), 
             (-0x0325,), (-0x0333,), (-0x0332,), (-0x0326,), 
             (-0x031C,), (-0x032E,), (-0xFE22,), (-0xFE23,), 
             None,       None,       (-0x0313,) ))

# ANSEL (ANSI/NISO Z39.47), with Library of Congress additions.
# LoC still use the same escape sequence as assigned for the standard one though.
graphdata.gsets["ir231/marc"] = (94, 1, (
                         (0x0141,),  (0x00D8,),  (0x0110,), 
             (0x00DE,),  (0x00C6,),  (0x0152,),  (0x02B9,),
             (0x00B7,),  (0x266D,),  (0x00AE,),  (0x00B1,), 
             (0x01A0,),  (0x01AF,),  (0x02BC,),  None, 
             (0x02BB,),  (0x0142,),  (0x00F8,),  (0x0111,), 
             (0x00FE,),  (0x00E6,),  (0x0153,),  (0x02BA,), 
             (0x0131,),  (0x00A3,),  (0x00F0,),  None,      
             (0x01A1,),  (0x01B0,),  None,       None, 
             (0x00B0,),  (0x2113,),  (0x2117,),  (0x00A9,), 
             (0x266F,),  (0x00BF,),  (0x00A1,),  (0x00DF,), 
             (0x20AC,),  None,       None,       None, 
             None,       None,       None,       None,  
             None,       None,       None,       None,      
             None,       None,       None,       None, 
             None,       None,       None,       None,      
             None,       None,       None,       None, 
             (-0x0309,), (-0x0300,), (-0x0301,), (-0x0302,), 
             (-0x0303,), (-0x0304,), (-0x0306,), (-0x0307,), 
             (-0x0308,), (-0x030C,), (-0x030A,), (-0xFE20,), 
             (-0xFE21,), (-0x0315,), (-0x030B,), (-0x0310,), 
             (-0x0327,), (-0x0328,), (-0x0323,), (-0x0324,), 
             (-0x0325,), (-0x0333,), (-0x0332,), (-0x0326,), 
             (-0x031C,), (-0x032E,), (-0xFE22,), (-0xFE23,), 
             None,       None,       (-0x0313,) ))

# ANSEL (ANSI/NISO Z39.47), with Library of Congress and Genealogical Society of Utah additions.
# The extensions do not collide and mostly co-exist, besides both adding the eszett (a conspicuous
#   omission from the original ANSEL if I ever saw one). GSU's midline letters are not only mapped
#   to their ASCII equivalents on Wikipedia, but also by GSU's now-discontinued PAF (arguably the
#   only source of true wisdom in this respect). No idea what they were originally for. Mapping
#   straight to their ASCII equivalents seems foolish here though, hence the zenkaku mappings.
graphdata.gsets["ir231/full"] = (94, 1, (
                         (0x0141,),  (0x00D8,),  (0x0110,), 
             (0x00DE,),  (0x00C6,),  (0x0152,),  (0x02B9,),
             (0x00B7,),  (0x266D,),  (0x00AE,),  (0x00B1,), 
             (0x01A0,),  (0x01AF,),  (0x02BC,),  None, 
             (0x02BB,),  (0x0142,),  (0x00F8,),  (0x0111,), 
             (0x00FE,),  (0x00E6,),  (0x0153,),  (0x02BA,), 
             (0x0131,),  (0x00A3,),  (0x00F0,),  None,      
             (0x01A1,),  (0x01B0,),  (0x25A1,),  (0x25A0,), 
             (0x00B0,),  (0x2113,),  (0x2117,),  (0x00A9,), 
             (0x266F,),  (0x00BF,),  (0x00A1,),  (0x00DF,), 
             (0x20AC,),  None,       None,       None, 
             None,       (0xFF45,),  (0xFF4F,),  (0x00DF,), 
             None,       None,       None,       None,      
             None,       None,       None,       None, 
             None,       None,       None,       None,      
             None,       None,       None,       None, 
             (-0x0309,), (-0x0300,), (-0x0301,), (-0x0302,), 
             (-0x0303,), (-0x0304,), (-0x0306,), (-0x0307,), 
             (-0x0308,), (-0x030C,), (-0x030A,), (-0xFE20,), 
             (-0xFE21,), (-0x0315,), (-0x030B,), (-0x0310,), 
             (-0x0327,), (-0x0328,), (-0x0323,), (-0x0324,), 
             (-0x0325,), (-0x0333,), (-0x0332,), (-0x0326,), 
             (-0x031C,), (-0x032E,), (-0xFE22,), (-0xFE23,), 
             (-0x0338,), None,       (-0x0313,) ))


