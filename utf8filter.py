#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

utf8docs = (("DOCS", False, (0x47,)),
            ("DOCS", True, (0x47,)),
            ("DOCS", True, (0x48,)),
            ("DOCS", True, (0x49,)))

def utf8filter(stream):
    is_utf8 = False
    utf8_brot = []
    utf8_seeking = 0
    reconsume = None
    firstchar = True
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if (token[0] == "DOCS"):
            if utf8_brot:
                yield ("ERROR", "UTF8TRUNC", tuple(utf8_brot))
                del utf8_brot[:]
            is_utf8 = (token in utf8docs)
            firstchar = True
            yield token
        elif is_utf8:
            if not utf8_brot:
                # Lead byte
                if token[0] != "WORD":
                    yield token # Escape code passing through
                    firstchar = False
                elif token[1] < 0x80:
                    yield ("UCS", token[1]) # 1-byte code
                    firstchar = False
                elif (token[1] & 0b11000000) == 0x80:
                    # i.e. is a continuation byte
                    yield ("ERROR", "UTF8ISOLCONT", (token[1],))
                    firstchar = False
                else:
                    for bc in range(8):
                        if not token[1] & (0x80 >> bc):
                            break
                    assert bc > 1
                    utf8_seeking = bc
                    utf8_brot.append(token[1])
            else:
                # Continuation byte
                if (token[0] != "WORD") or (token[1] < 0x80) or ((token[1] & 0b11000000) != 0x80):
                    # i.e. isn't a continuation byte
                    yield ("ERROR", "UTF8TRUNC", tuple(utf8_brot))
                    del utf8_brot[:]
                    reconsume = token
                    firstchar = False
                    continue
                else:
                    utf8_brot.append(token[1])
                    assert len(utf8_brot) <= utf8_seeking
                    if len(utf8_brot) == utf8_seeking:
                        ucs = utf8_brot.pop(0) & ((0x80 >> utf8_seeking) - 1)
                        while utf8_brot:
                            ucs <<= 6
                            ucs |= utf8_brot.pop(0) & 0b00111111
                        if ucs == 0xFEFF and firstchar:
                            yield ("BOM", None)
                        else:
                            yield ("UCS", ucs)
                        firstchar = False
                        # utf8_brot is now empty, and utf8_seeking will be set by next lead byte
                    #
                #
            #
        else: # i.e. isn't a DOCS, nor a UTF-8 part of the stream
            yield token
        #
    #
#








