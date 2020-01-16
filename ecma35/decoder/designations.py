#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019/2020.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

def decode_designations(stream, state):
    workingsets = ("G0", "G1", "G2", "G3")
    reconsume = None
    irrset = None
    inesc = False
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if token[0] == "ESC" and token[1] in tuple(b"()*+-./$"):
            inesc = False
            if token[1] in tuple(b"()*+"):
                settype = "94"
                wsetbyte = token[1]
                idbytes = token[2] + (token[3],)
            elif token[1] in tuple(b"-./"):
                settype = "96"
                wsetbyte = token[1]
                idbytes = token[2] + (token[3],)
            elif (token[1] == b"$"[0]) and ((not token[2]) or (token[2][0] in tuple(b"()*+"))):
                settype = "94n"
                wsetbyte = token[2][0] if token[2] else None
                idbytes = token[2][1:] + (token[3],)
            else:
                assert (token[1] == b"$"[0]) and (token[2][0] in tuple(b"-./"))
                settype = "96n"
                wsetbyte = token[2][0]
                idbytes = token[2][1:] + (token[3],)
            if (not wsetbyte) or (wsetbyte in tuple(b"(")):
                wset = 0
            elif wsetbyte in tuple(b")-"):
                wset = 1
            elif wsetbyte in tuple(b"*."):
                wset = 2
            else:
                assert wsetbyte in tuple(b"+/")
                wset = 3
            myirr = irrset[2] + (irrset[3],) if irrset is not None else ()
            irrset = None
            yield ("DESIG", wset, settype, idbytes, not wsetbyte, myirr)
        elif token[0] == "ESC" and token[1] == 0x21:
            inesc = False
            c0seq = token[2] + (token[3],)
            myirr = irrset[2] + (irrset[3],) if irrset is not None else ()
            irrset = None
            yield ("CDESIG", "C0", c0seq, myirr)
        elif token[0] == "ESC" and token[1] == 0x22:
            inesc = False
            c1seq = token[2] + (token[3],)
            myirr = irrset[2] + (irrset[3],) if irrset is not None else ()
            irrset = None
            yield ("CDESIG", "C1", c1seq, myirr)
        elif irrset is not None:
            if (token[0] == "C0" and token[1] == 0x1B) or (token[0] in workingsets and
                                                           token[2] == "GL" and inesc):
                # Because the ESC tokens arrive by feedback from a filter downstream from here,
                # we do have to pass the C0 and GL tokens needed to give us the designation ESC
                # token.
                inesc = True
                yield token
            else:
                inesc = False
                yield ("ERROR", "IRRISOLATE", irrset[2] + (irrset[3],))
                irrset = None
                reconsume = token
                continue
        elif token[0] == "ESC" and token[1] == 0x26:
            inesc = False
            irrset = token
        else:
            inesc = False
            yield token












