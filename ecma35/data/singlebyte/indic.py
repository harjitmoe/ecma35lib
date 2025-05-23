#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, 2020, 2024, 2025.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ecma35.data import graphdata
from ecma35.data.singlebyte import sbmapparsers as parsers

# TIS-620 (with NBSP) ISO-8859-11 Latin/Thai RHS
graphdata.gsets["ir166"] = (96, 1, tuple((i,) if i else None for i in (
             0x00A0, 0x0E01, 0x0E02, 0x0E03, 0x0E04, 0x0E05, 0x0E06, 0x0E07, 
             0x0E08, 0x0E09, 0x0E0A, 0x0E0B, 0x0E0C, 0x0E0D, 0x0E0E, 0x0E0F, 
             0x0E10, 0x0E11, 0x0E12, 0x0E13, 0x0E14, 0x0E15, 0x0E16, 0x0E17, 
             0x0E18, 0x0E19, 0x0E1A, 0x0E1B, 0x0E1C, 0x0E1D, 0x0E1E, 0x0E1F, 
             0x0E20, 0x0E21, 0x0E22, 0x0E23, 0x0E24, 0x0E25, 0x0E26, 0x0E27, 
             0x0E28, 0x0E29, 0x0E2A, 0x0E2B, 0x0E2C, 0x0E2D, 0x0E2E, 0x0E2F, 
             0x0E30, 0x0E31, 0x0E32, 0x0E33, 0x0E34, 0x0E35, 0x0E36, 0x0E37, 
             0x0E38, 0x0E39, 0x0E3A, None,   None,   None,   None,   0x0E3F, 
             0x0E40, 0x0E41, 0x0E42, 0x0E43, 0x0E44, 0x0E45, 0x0E46, 0x0E47, 
             0x0E48, 0x0E49, 0x0E4A, 0x0E4B, 0x0E4C, 0x0E4D, 0x0E4E, 0x0E4F, 
             0x0E50, 0x0E51, 0x0E52, 0x0E53, 0x0E54, 0x0E55, 0x0E56, 0x0E57, 
             0x0E58, 0x0E59, 0x0E5A, 0x0E5B, None,   None,   None,   None,)))

graphdata.gsets["ir166/1986"] = (94, 1, tuple((i,) if i else None for i in (
                     0x0E01, 0x0E02, 0x0E03, 0x0E04, 0x0E05, 0x0E06, 0x0E07, 
             0x0E08, 0x0E09, 0x0E0A, 0x0E0B, 0x0E0C, 0x0E0D, 0x0E0E, 0x0E0F, 
             0x0E10, 0x0E11, 0x0E12, 0x0E13, 0x0E14, 0x0E15, 0x0E16, 0x0E17, 
             0x0E18, 0x0E19, 0x0E1A, 0x0E1B, 0x0E1C, 0x0E1D, 0x0E1E, 0x0E1F, 
             0x0E20, 0x0E21, 0x0E22, 0x0E23, 0x0E24, 0x0E25, 0x0E26, 0x0E27, 
             0x0E28, 0x0E29, 0x0E2A, 0x0E2B, 0x0E2C, 0x0E2D, 0x0E2E, 0x0E2F, 
             0x0E30, 0x0E31, 0x0E32, 0x0E33, 0x0E34, 0x0E35, 0x0E36, 0x0E37, 
             0x0E38, 0x0E39, 0x0E3A, None,   None,   None,   None,   0x0E3F, 
             0x0E40, 0x0E41, 0x0E42, 0x0E43, 0x0E44, 0x0E45, 0x0E46, 0x0E47, 
             0x0E48, 0x0E49, 0x0E4A, 0x0E4B, 0x0E4C, 0x0E4D, 0x0E4E, 0x0E4F, 
             0x0E50, 0x0E51, 0x0E52, 0x0E53, 0x0E54, 0x0E55, 0x0E56, 0x0E57, 
             0x0E58, 0x0E59, 0x0E5A, 0x0E5B, None,   None,   None,)))

# IBM code page 9066 or 13162; maximal version of IBM code page 874.
graphdata.gsets["ir166/ibm"] = (96, 1, ((3656, 63603), (3585,), (3586,), (3587,), (3588,), (3589,), (3590,), (3591,), (3592,), (3593,), (3594,), (3595,), (3596,), (3597,), (3598,), (3599,), (3600,), (3601,), (3602,), (3603,), (3604,), (3605,), (3606,), (3607,), (3608,), (3609,), (3610,), (3611,), (3612,), (3613,), (3614,), (3615,), (3616,), (3617,), (3618,), (3619,), (3620,), (3621,), (3622,), (3623,), (3624,), (3625,), (3626,), (3627,), (3628,), (3629,), (3630,), (3631,), (3632,), (3633,), (3634,), (3635,), (3636,), (3637,), (3638,), (3639,), (3640,), (3641,), (3642,), (3657, 63603), (3658, 63603), (3659, 63603), (3660, 63603), (3647,), (3648,), (3649,), (3650,), (3651,), (3652,), (3653,), (3654,), (3655,), (3656,), (3657,), (3658,), (3659,), (3660,), (3661,), (3662,), (3663,), (3664,), (3665,), (3666,), (3667,), (3668,), (3669,), (3670,), (3671,), (3672,), (3673,), (3674,), (3675,), (162,), (172,), (166,), (160,)))
graphdata.chcpdocs['9066'] = graphdata.chcpdocs['13162'] = 'ecma-35'
graphdata.defgsets['9066'] = graphdata.defgsets['13162'] = ('ir006', 'ir166/ibm', 'nil', 'nil')

graphdata.gsets["ir166/minimal"] = (94, 1, ((3585,), (3586,), (3587,), (3588,), (3589,), (3590,), (3591,), (3592,), (3593,), (3594,), (3595,), (3596,), (3597,), (3598,), (3599,), (3600,), (3601,), (3602,), (3603,), (3604,), (3605,), (3606,), (3607,), (3608,), (3609,), (3610,), (3611,), (3612,), (3613,), (3614,), (3615,), (3616,), (3617,), (3618,), (3619,), (3620,), (3621,), (3622,), (3623,), (3624,), (3625,), (3626,), (3627,), (3628,), (3629,), (3630,), (3631,), (3632,), (3633,), (3634,), (3635,), (3636,), (3637,), (3638,), (3639,), (3640,), (3641,), (3642,), None, None, None, None, (3647,), (3648,), (3649,), (3650,), (3651,), (3652,), (3653,), (3654,), (3655,), (3656,), (3657,), (3658,), (3659,), (3660,), (3661,), None, None, (3664,), (3665,), (3666,), (3667,), (3668,), (3669,), (3670,), (3671,), (3672,), (3673,), None, None, None, None, None))
graphdata.chcpdocs['4970'] = 'ecma-35'
graphdata.defgsets['4970'] = ('ir006', 'ir166/minimal', 'nil', 'nil')

graphdata.gsets["ir166/ibm/euro"] = (96, 1, ((3656, 63603), (3585,), (3586,), (3587,), (3588,), (3589,), (3590,), (3591,), (3592,), (3593,), (3594,), (3595,), (3596,), (3597,), (3598,), (3599,), (3600,), (3601,), (3602,), (3603,), (3604,), (3605,), (3606,), (3607,), (3608,), (3609,), (3610,), (3611,), (3612,), (3613,), (3614,), (3615,), (3616,), (3617,), (3618,), (3619,), (3620,), (3621,), (3622,), (3623,), (3624,), (3625,), (3626,), (3627,), (3628,), (3629,), (3630,), (3631,), (3632,), (3633,), (3634,), (3635,), (3636,), (3637,), (3638,), (3639,), (3640,), (3641,), (3642,), (3657, 63603), (3658, 63603), (3659, 63603), (8364,), (3647,), (3648,), (3649,), (3650,), (3651,), (3652,), (3653,), (3654,), (3655,), (3656,), (3657,), (3658,), (3659,), (3660,), (3661,), (3662,), (3663,), (3664,), (3665,), (3666,), (3667,), (3668,), (3669,), (3670,), (3671,), (3672,), (3673,), (3674,), (3675,), (162,), (172,), (166,), (160,)))
graphdata.chcpdocs['1161'] = 'ecma-35'
graphdata.defgsets['1161'] = ('ir006', 'ir166/ibm/euro', 'nil', 'nil')

# Code pages 874 (TIS-620 exts)
# Per alias comments in ICU's convrtrs.txt, IBM's 874 is identical to IBM's 9066.
# Microsoft's 874, on the other hand, matches the layout of IBM's 1162.
_windows_thai = parsers.read_single_byte("WHATWG/index-windows-874.txt")
_windows_thai += (None,) * (128 - len(_windows_thai))
graphdata.rhses["1162"] = _windows_thai
# The two only collide at 0xA0, which IBM uses for an alternate U+0E48 and which Microsoft
#   uses for an NBSP. Favour the more-deployed Microsoft / ISO-8859-11 NBSP for "874".
graphdata.rhses["874"] = tuple(a or b for a, b in zip(
        graphdata.rhses["1162"],
        (None,) * 32 + graphdata.gsets["ir166/ibm/euro"][2]))
graphdata.defgsets["874"] = graphdata.defgsets["1162"] = ("ir006", "ir166/ibm/euro", "nil", "nil")

# Macintosh code page (doesn't have a Mozilla file)
graphdata.rhses["10021"] = ((171,), (187,), (8230,), (3656, 63605), (3657, 63605), (3658, 63605), (3659, 63605), (3660, 63605), (3656, 63603), (3657, 63603), (3658, 63603), (3659, 63603), (3660, 63603), (8220,), (8221,), (3661, 63604), (144,), (8226,), (3633, 63604), (3655, 63604), (3636, 63604), (3637, 63604), (3638, 63604), (3639, 63604), (3656, 63604), (3657, 63604), (3658, 63604), (3659, 63604), (3660, 63604), (8216,), (8217,), (159,), (160,), (3585,), (3586,), (3587,), (3588,), (3589,), (3590,), (3591,), (3592,), (3593,), (3594,), (3595,), (3596,), (3597,), (3598,), (3599,), (3600,), (3601,), (3602,), (3603,), (3604,), (3605,), (3606,), (3607,), (3608,), (3609,), (3610,), (3611,), (3612,), (3613,), (3614,), (3615,), (3616,), (3617,), (3618,), (3619,), (3620,), (3621,), (3622,), (3623,), (3624,), (3625,), (3626,), (3627,), (3628,), (3629,), (3630,), (3631,), (3632,), (3633,), (3634,), (3635,), (3636,), (3637,), (3638,), (3639,), (3640,), (3641,), (3642,), (8288,), (8203,), (8211,), (8212,), (3647,), (3648,), (3649,), (3650,), (3651,), (3652,), (3653,), (3654,), (3655,), (3656,), (3657,), (3658,), (3659,), (3660,), (3661,), (8482,), (3663,), (3664,), (3665,), (3666,), (3667,), (3668,), (3669,), (3670,), (3671,), (3672,), (3673,), (174,), (169,), None, None, None, None)

# RHS of IBM code page 1133 for Lao
graphdata.gsets["ibmlao"] = (96, 1, (None, (3713,), (3714,), (3716,), (3719,), (3720,), (3754,), (3722,), (3725,), (3732,), (3733,), (3734,), (3735,), (3737,), (3738,), (3739,), (3740,), (3741,), (3742,), (3743,), (3745,), (3746,), (3747,), (3749,), (3751,), (3755,), (3757,), (3758,), None, None, None, (3759,), (3760,), (3762,), (3763,), (3764,), (3765,), (3766,), (3767,), (3768,), (3769,), (3772,), (3761,), (3771,), (3773,), None, None, None, (3776,), (3777,), (3778,), (3779,), (3780,), (3784,), (3785,), (3786,), (3787,), (3788,), (3789,), (3782,), None, (3804,), (3805,), (8365,), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, (3792,), (3793,), (3794,), (3795,), (3796,), (3797,), (3798,), (3799,), (3800,), (3801,), None, None, (162,), (172,), (166,), (160,)))
graphdata.chcpdocs['1133'] = 'ecma-35'
graphdata.defgsets['1133'] = ('ir006', 'ibmlao', 'nil', 'nil')
graphdata.gsets["ibmlao/94"] = (94, 1, graphdata.gsets["ibmlao"][2][1:-1])

# 8-bit Devanagari
graphdata.gsets["iscii/devanagari"] = (94, 1, ((2305,), (2306,), (2307,), (2309,), (2310,), (2311,), (2312,), (2313,), (2314,), (2315,), (2318,), (2319,), (2320,), (2317,), (2322,), (2323,), (2324,), (2321,), (2325,), (2326,), (2327,), (2328,), (2329,), (2330,), (2331,), (2332,), (2333,), (2334,), (2335,), (2336,), (2337,), (2338,), (2339,), (2340,), (2341,), (2342,), (2343,), (2344,), (2345,), (2346,), (2347,), (2348,), (2349,), (2350,), (2351,), (2399,), (2352,), (2353,), (2354,), (2355,), (2356,), (2357,), (2358,), (2359,), (2360,), (2361,), None, (2366,), (2367,), (2368,), (2369,), (2370,), (2371,), (2374,), (2375,), (2376,), (2373,), (2378,), (2379,), (2380,), (2377,), (2381,), (2364,), (2404,), None, None, None, None, None, None, (2406,), (2407,), (2408,), (2409,), (2410,), (2411,), (2412,), (2413,), (2414,), (2415,), None, None, None, None))
graphdata.rhses["806"] = ((0x2502,), (0x2524,), (0x2563,), (0x2551,), (0x2557,), (0x255D,), (0x2510,), (0x2514,), (0x2534,), (0x252C,), (0x251C,), (0x2500,), (0x253C,), (0x255A,), (0x2554,), (0x2569,), (0x2566,), (0x2560,), (0x2550,), (0x256C,), (0x2518,), (0x250C,), None, None, None, None, None, None, None, None, None, None, None) + graphdata.gsets["iscii/devanagari"][2] + (None,)
graphdata.chcpdocs["4902"] = 'ecma-35'
graphdata.defgsets["806"] = graphdata.defgsets["4902"] = ("ir006", "iscii/devanagari", "nil", "nil")


