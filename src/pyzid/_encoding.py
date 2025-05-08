__author__ = 'deadblue'

import math


_encoding_chars = '0123456789abcdefghijkmnpqrtuvwxy'

_decoding_dict = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
    'g': 16,
    'h': 17,
    'i': 18,
    'j': 19,
    'k': 20,
    'm': 21,
    'n': 22,
    'p': 23,
    'q': 24,
    'r': 25,
    't': 26,
    'u': 27,
    'v': 28,
    'w': 29,
    'x': 30,
    'y': 31,
}


def encode(src: bytes) -> str:
    int_val = int.from_bytes(src, byteorder='big', signed=False)
    buf_size = math.ceil(len(src) / 5) * 8
    buf = []
    for i in range(buf_size):
        ch_index = int_val >> (5 * (23 - i)) & 0x1f
        buf.append(_encoding_chars[ch_index])
    return ''.join(buf)

def decode(src: str) -> bytes:
    n = 0
    for ch in src:
        index = _decoding_dict[ch]
        n = (n << 5) | (index & 0x1f)
    return n.to_bytes(15, 'big')
