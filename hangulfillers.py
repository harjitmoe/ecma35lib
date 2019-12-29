#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
# By HarJIT in 2019, marginally.

import unicodedata as ucd

initials = {'\u3131': '\u1100', '\u3132': '\u1101', '\u3134': '\u1102', '\u3137': '\u1103', '\u3138': '\u1104', '\u3139': '\u1105', '\u3141': '\u1106', '\u3142': '\u1107', '\u3143': '\u1108', '\u3145': '\u1109', '\u3146': '\u110a', '\u3147': '\u110b', '\u3148': '\u110c', '\u3149': '\u110d', '\u314a': '\u110e', '\u314b': '\u110f', '\u314c': '\u1110', '\u314d': '\u1111', '\u314e': '\u1112', '\u3165': '\u1114', '\u3166': '\u1115', '\u3167': '\u115b', '\u316a': '\ua966', '\u316e': '\u111c', '\u316f': '\ua971', '\u3171': '\u111d', '\u3172': '\u111e', '\u3173': '\u1120', '\u3174': '\u1122', '\u3175': '\u1123', '\u3176': '\u1127', '\u3177': '\u1129', '\u3178': '\u112b', '\u3179': '\u112c', '\u317a': '\u112d', '\u317b': '\u112e', '\u317c': '\u112f', '\u317d': '\u1132', '\u317e': '\u1136', '\u317f': '\u1140', '\u3180': '\u1147', '\u3181': '\u114c', '\u3184': '\u1157', '\u3185': '\u1158', '\u3186': '\u1159', '\u3164': '\u115f'}

vowels = {'\u314f': '\u1161', '\u3150': '\u1162', '\u3151': '\u1163', '\u3152': '\u1164', '\u3153': '\u1165', '\u3154': '\u1166', '\u3155': '\u1167', '\u3156': '\u1168', '\u3157': '\u1169', '\u3158': '\u116a', '\u3159': '\u116b', '\u315a': '\u116c', '\u315b': '\u116d', '\u315c': '\u116e', '\u315d': '\u116f', '\u315e': '\u1170', '\u315f': '\u1171', '\u3160': '\u1172', '\u3161': '\u1173', '\u3162': '\u1174', '\u3163': '\u1175', '\u3187': '\u1184', '\u3188': '\u1185', '\u3189': '\u1188', '\u318a': '\u1191', '\u318b': '\u1192', '\u318c': '\u1194', '\u318d': '\u119e', '\u318e': '\u11a1', '\u3164': '\u1160'}

finals = {'\u3132': '\u11a9', '\u3133': '\u11aa', '\u3135': '\u11ac', '\u3136': '\u11ad', '\u313c': '\u11b2', '\u313d': '\u11b3', '\u313e': '\u11b4', '\u313f': '\u11b5', '\u3140': '\u11b6', '\u314b': '\u11bf', '\u3137': '\u11ae', '\u313a': '\u11b0', '\u313b': '\u11b1', '\u3144': '\u11b9', '\u3148': '\u11bd', '\u314a': '\u11be', '\u314c': '\u11c0', '\u314d': '\u11c1', '\u314e': '\u11c2', '\u3141': '\u11b7', '\u3142': '\u11b8', '\u3146': '\u11bb', '\u3131': '\u11a8', '\u3145': '\u11ba', '\u3147': '\u11bc', '\u3134': '\u11ab', '\u3139': '\u11af', '\u3165': '\u11ff', '\u3166': '\u11c6', '\u3167': '\u11c7', '\u3168': '\u11c8', '\u3169': '\u11cc', '\u316a': '\u11ce', '\u316b': '\u11d3', '\u316c': '\u11d7', '\u316d': '\u11d9', '\u316e': '\u11dc', '\u316f': '\u11dd', '\u3170': '\u11df', '\u3171': '\u11e2', '\u3173': '\ud7e3', '\u3175': '\ud7e7', '\u3176': '\ud7e8', '\u3178': '\u11e6', '\u317a': '\u11e7', '\u317c': '\u11e8', '\u317d': '\u11ea', '\u317e': '\ud7ef', '\u317f': '\u11eb', '\u3180': '\u11ee', '\u3181': '\u11f0', '\u3182': '\u11f1', '\u3183': '\u11f2', '\u3184': '\u11f4', '\u3186': '\u11f9', '\u3164': ''}

repertoire = set(finals.keys()) | set(vowels.keys()) | set(initials.keys())

def proc_hangul_fillers(stream, state):
    first = second = third = fourth = None
    for token in stream:
        if first is not None:
            assert fourth is None # Shouldn't remain non-None across iterations.
            if token[0] != "CHAR" or chr(token[1]) not in repertoire:
                yield("ERROR", "TRUNCHANGUL", None)
                yield first
                if second is not None:
                    yield second
                if third is not None:
                    yield third
                first = second = third = None
                state.feedback.append(token) # Don't swallow upcoming token
            elif third is not None:
                fourth = token
                try:
                    if first[1] != 0x3164:
                        raise KeyError
                    # KeyError may also be raised by the following statement:
                    unic = (initials[chr(second[1])] + vowels[chr(third[1])] +
                            finals[chr(fourth[1])])
                except KeyError:
                    yield("ERROR", "BADHANGUL", None)
                    yield first
                    first, second, third, fourth = second, third, fourth, None
                else:
                    cunic = ucd.normalize("NFC", unic)
                    sources = (first, second, third, fourth)
                    yield ("COMPCHAR", tuple(ord(i) for i in cunic), sources)
                    first = second = third = fourth = None
            elif second is not None:
                third = token
            else:
                second = token
        elif token[0] == "CHAR" and token[1] == 0x3164:
            first = token
        else:
            yield token





