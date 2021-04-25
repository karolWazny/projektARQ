from .Decoder import *
from .Encoder import *
from .Packet import Packet
class Receiver:
    def __init__(self):
        self.completeData = []
        self.receivedData = []

    def decodeParity(self,packet):
        EvenDecoder.decode(self)
        while True:
            try:
                EvenDecoder.checkForError(self)
                break
            except Exception:
                ParityEncoder.encode(self,packet)
    def decodeCRC(self,packet,key):
        CRCDecoder.decode(self)
        while True:
            try:
                CRCDecoder.checkForError(self)
                break
            except Exception:
                CRCEncoder.encode(self,packet,key)
    def decodeHamming(self,packet):
        HammingDecoder.decode(self)
        while True:
            try:
                HammingDecoder.checkForError(self)
                break
            except Exception:
                HammingEncoder.encode(self,packet)



