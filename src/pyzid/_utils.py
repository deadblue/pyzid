__author__ = 'deadblue'

def i2b(num: int, len: int) -> bytes:
    return num.to_bytes(len, 'big')

def b2i(b: bytes) -> int:
    return int.from_bytes(
        b, 'big', 
        signed=False
    )
