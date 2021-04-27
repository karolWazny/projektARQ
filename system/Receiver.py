from repo.system.Decoder import *
from repo.system.Encoder import *
from repo.system.Packet import Packet
class Receiver:
    def __init__(self):
        self.completeData = []
        self.receivedData = []

    def decodeParity(self,packet):
        EvenDecoder.decode(self)
        while True:
            try:
                EvenDecoder.checkForError(self)
                return Packet
            except Exception:
                ParityEncoder.encode(self,packet)
    def decodeCRC(self,packet,key):
        CRCDecoder.decode(self)
        while True:
            try:
                CRCDecoder.checkForError(self)
                return packet
            except Exception:
                packet = None
                return None
    def decodeHamming(self,packet):
        HammingDecoder.decode(self)
        while True:
            try:
                HammingDecoder.checkForError(self)
                return packet
            except Exception:
                packet = None
                return None



