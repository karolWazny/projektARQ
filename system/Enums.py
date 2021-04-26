from enum import Enum, unique, auto


# https://docs.python.org/3/library/enum.html

@unique
class Encoding(Enum):
    PARITY = auto()
    ODDITY = auto()
    HAMMING = auto()
    CRC = auto()

    def __eq__(self, other):
        if isinstance(other, Encoding):
            return self.__dict__ == other.__dict__
        if isinstance(other, str):
            return self.__dict__['_name_'] == other
        else:
            return False


@unique
class Noise(Enum):
    BINARY_SYMMETRIC = auto()
    BINARY_ERASURE = auto()
    Z_CHANNEL = auto()
    TWO_STATE = auto()

    def __eq__(self, other):
        if isinstance(other, Noise):
            return self.__dict__ == other.__dict__
        if isinstance(other, str):
            return self.__dict__['_name_'] == other
        else:
            return False
