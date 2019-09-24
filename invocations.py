#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

def invocationfilter(stream, *, def_grset=1):
    glset = 0
    grset = def_grset
    workingsets = ("G0", "G1", "G2", "G3")
    single_set = -1
    for token in stream:
        if single_set >= 0:
            if token[0] in ("GL", "GR"):
                yield ("SINGLEAREA", token[0]) # Inject for announcement verification.
                yield (workingsets[single_set], token[1])
                single_set = -1
                continue
            else:
                yield ("ERROR", "SINGLETRUNCATE", workingsets[single_set])
                single_set = -1
                # (Fall through to next part.)
            #
        # Keep the shift tokens in the stream for metadata, announcement verification, etc…
        # Since no GL or GR opcodes will remain, this won't break anything.
        # NOT elif (so byte after truncated single shift sequence isn't swallowed):
        if token[0] == "CTRL" and token[1] in ("SI", "LS0"):
            glset = 0
            yield token
        elif token[0] == "CTRL" and token[1] in ("SO", "LS1"):
            glset = 1
            yield token
        elif token[0] == "CTRL" and token[1] == "LS1R":
            grset = 1
            yield token
        elif token[0] == "CTRL" and token[1] == "LS2":
            glset = 2
            yield token
        elif token[0] == "CTRL" and token[1] == "LS2R":
            grset = 2
            yield token
        elif token[0] == "CTRL" and token[1] == "SS2":
            single_set = 2
            yield token
        elif token[0] == "CTRL" and token[1] == "LS3":
            glset = 3
            yield token
        elif token[0] == "CTRL" and token[1] == "LS3R":
            grset = 3
            yield token
        elif token[0] == "CTRL" and token[1] == "SS3":
            single_set = 3
            yield token
        elif token[0] == "GL":
            yield (workingsets[glset], token[1])
        elif token[0] == "GR":
            yield (workingsets[grset], token[1])
        else:
            yield token












