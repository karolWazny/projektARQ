from enum import Enum, unique, auto


# https://docs.python.org/3/library/enum.html
@unique
class Encoding(Enum):
    PARITY = auto()
    ODDITY = auto()
    HAMMING = auto()
    CRC = auto()

@unique
class Noise(Enum):
    BINARY_SYMMETRIC = auto()
    BINARY_ERASURE = auto()
    Z_CHANNEL = auto()
