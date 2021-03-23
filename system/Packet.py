class Packet:
    def __init__(self):
        self.bits = []

    def addBit(self, bit):
        self.bits.append(bit)

    def length(self):
        return len(self.bits)

# ################## test ########################################
x = Packet()
#for y in range(111):
    #if x.addBit(1) == -1:
        #print(x.bits)
        #send(x.bitList)
        #x = Packet(8)
        #x.addBit(1)

#print(len(x.bits))
#print(x.bits)
