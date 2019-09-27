#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019.

utf16docs = (("DOCS", True, (0x40,)),
             ("DOCS", True, (0x43,)),
             ("DOCS", True, (0x45,)),
             ("DOCS", True, (0x4A,)),
             ("DOCS", True, (0x4B,)),
             ("DOCS", True, (0x4C,)))

def decode_utf16(stream, *, pedantic_surrogates=True):
    is_utf16 = False
    utf16_lead = None
    reconsume = None
    while 1:
        token = next(stream) if reconsume is None else reconsume
        reconsume = None
        if (token[0] == "DOCS"):
            if utf16_lead:
                if pedantic_surrogates:
                    yield ("ERROR", "UTF16ISOLATE", utf16_lead)
                else:
                    yield ("UCS", utf16_lead, "UTF-16", "UCS-2")
                utf16_lead = None
            is_utf16 = (token in utf16docs)
            yield token
        elif is_utf16 or (token[0] == "CESU"):
            if not utf16_lead:
                # Lead word
                if token[0] not in ("WORD", "CESU"):
                    yield token # Escape code passing through
                elif (token[1] < 0xD800) or (token[1] >= 0xDC00):
                    if (0xDC00 <= token[1] < 0xE000) and pedantic_surrogates:
                        yield ("ERROR", "UTF16ISOLATE", token[1]) # isolated trailing surrogate
                    elif token[0] == "CESU":
                        # Can only get here with pass_cesu ON and pedantic_surrogates OFF.
                        yield ("UCS", token[1], "UTF-8", "WTF-8") # "Wobbly UTF-8"
                    else:
                        yield ("UCS", token[1], "UTF-16", "UCS-2") # non-surrogate BMP code
                else:
                    utf16_lead = token[1]
            else:
                # Trail word
                if ((token[0] not in ("WORD", "CESU")) or (token[1] < 0xDC00)
                                                       or (token[1] >= 0xE000)):
                    # i.e. isn't a continuation word
                    if pedantic_surrogates:
                        yield ("ERROR", "UTF16ISOLATE", utf16_lead)
                    elif token[0] == "CESU":
                        # Can only get here with pass_cesu ON and pedantic_surrogates OFF.
                        yield ("UCS", utf16_lead, "UTF-8", "WTF-8") # "Wobbly UTF-8"
                    else:
                        yield ("UCS", utf16_lead, "UTF-16", "UCS-2")
                    utf16_lead = None
                    reconsume = token
                    continue
                else:
                    ucs = (((utf16_lead & 1023) << 10) | (token[1] & 1023)) + 0x10000
                    if token[0] == "CESU":
                        yield ("UCS", ucs, "UTF-8", "CESU-8")
                    else:
                        yield ("UCS", ucs, "UTF-16", "UTF-16")
                    utf16_lead = None
                #
            #
        else: # i.e. isn't a DOCS, nor a UTF-16 part of the stream
            yield token
        #
    #
#








