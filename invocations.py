#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

def decode_invocations(stream, *, def_grset=1):
    glset = 0
    grset = def_grset
    workingsets = ("G0", "G1", "G2", "G3")
    sizes = [1, None, None, None]
    is_96 = [0, 0, 1, 1]
    single_set = -1
    single_token = None
    single_need = 0
    single_area = None
    for token in stream:
        if single_set >= 0:
            expected = (single_area,) if single_area else ("GL", "GR")
            if token[0] in expected:
                if not single_area: # Don't inject in the middle of the code sequence.
                    # For announcement verification.
                    yield ("SINGLEOVER", token[0], single_token[1], single_token[2], single_token[3])
                    single_area = token[0]
                yield (workingsets[single_set], token[1], "S" + token[0])
                single_need -= 1
                if not single_need:
                    single_set = -1
                continue
            else:
                yield ("ERROR", "SINGLETRUNCATE", single_token)
                single_set = -1
                # (Fall through to next part.)
            #
        # Keep the locking shift tokens in the stream for metadata, announcements, etc…
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
            single_area = None
            single_set = 2
            single_token = token
            single_need = sizes[single_set]
            if not single_need:
                yield ("ERROR", "INDETERMSINGLE", token)
                single_set = -1
        elif token[0] == "CTRL" and token[1] == "LS3":
            glset = 3
            yield token
        elif token[0] == "CTRL" and token[1] == "LS3R":
            grset = 3
            yield token
        elif token[0] == "CTRL" and token[1] == "SS3":
            single_area = None
            single_set = 3
            single_token = token
            single_need = sizes[single_set]
            if not single_need:
                yield ("ERROR", "INDETERMSINGLE", token)
                single_set = -1
        elif token[0] == "SETSIZE":
            sizes[token[1]] = token[2]
        elif token[0] == "DESIG":
            yield token
            is_96[token[1]] = (token[2] not in ("94", "94n"))
        elif token[0] == "GL":
            if (not is_96[glset]) and (token[1] == 0):
                yield ("CTRL", "SP", "ECMA-35", token[1], "GL", workingsets[glset])
            elif (not is_96[glset]) and (token[1] == 95):
                yield ("CTRL", "DEL", "ECMA-35", token[1], "GL", workingsets[glset])
            else:
                yield (workingsets[glset], token[1], "GL")
        elif token[0] == "GR":
            yield (workingsets[grset], token[1], "GR")
        elif token[0] == "UCS" and token[1] == 0x20:
            yield ("CTRL", "SP", "UCS", token[1], token[2], token[3])
        elif token[0] == "UCS" and token[1] == 0x7F:
            yield ("CTRL", "DEL", "UCS", token[1], token[2], token[3])
        else:
            yield token












