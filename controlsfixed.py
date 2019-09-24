#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

fixedcontrols = {tuple(b"n"): "LS2",
                 tuple(b"o"): "LS3",
                 tuple(b"~"): "LS1R",
                 tuple(b"}"): "LS2R",
                 tuple(b"|"): "LS3R",
                 }

def fixedcontrolsfilter(stream):
    for token in stream:
        if token[0] != "ESC":
            yield token
        elif token[1] not in (None, b"#"[0]):
            yield token
        elif (token[3] < 0x30) or (token[3] > 0x7E):
            yield token
        # NOTE: assumes C1 controls already recognised as such by tokenfeed, and as such won't
        # still show up as control escapes. Otherwise, we'd need to test that the ones without the
        # intervening "#" byte aren't in fact C1 controls.
        else:
            seq = ((token[1],) if token[1] is not None else ()) + token[2] + (token[3],)
            if seq in fixedcontrols:
                yield ("CTRL", fixedcontrols[seq], "FIXESC")
            else:
                yield ("ERROR", "UNSUPPESC", seq)













