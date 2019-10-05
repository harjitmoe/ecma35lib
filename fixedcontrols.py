#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

import controldata

def _proc_pu(token):
    assert token[0] == "ESC"
    assert token[1] in (None, b"#"[0])
    assert 0x30 <= token[3] < 0x40
    follbytes = (1 if token[1] else 0) + len(token[2]) + 1
    start = 3 # PU1 and PU2 are C1 controls so start after those
    for i in range(follbytes): # i.e. includes 0 but not follbytes itself
        if i == 0:
            noatlevel = 0
        elif i in (1, 2):
            noatlevel = 16
        else:
            noatlevel = 16 ** (i - 1)
        start += noatlevel
    index = 0
    for i in token[2]:
        index |= (i & 0x0F)
        index <<= 4
    index |= (token[3] & 0x0F)
    return "PU{:d}".format(start + index)

def decode_fixed_controls(stream, state):
    for token in stream:
        if token[0] != "ESC":
            yield token
        elif token[1] not in (None, b"#"[0]):
            yield token
        elif 0x30 <= token[3] < 0x40:
            seq = ((token[1],) if token[1] is not None else ()) + token[2] + (token[3],)
            yield ("CTRL", _proc_pu(token), "ISO-IR", seq, "FIXED", "ESC")
        # NOTE: assumes C1 controls already recognised as such by tokenfeed, and as such won't
        # still show up as control escapes. Otherwise, we'd need to test that the ones without the
        # intervening "#" byte aren't in fact C1 controls.
        else:
            assert 0x40 <= token[3] <= 0x7E
            seq = ((token[1],) if token[1] is not None else ()) + token[2] + (token[3],)
            if seq in controldata.fixed_controls:
                yield ("CTRL", controldata.fixed_controls[seq], "ISO-IR", seq, "FIXED", "ESC")
            else:
                yield ("ERROR", "UNSUPPESC", seq)













