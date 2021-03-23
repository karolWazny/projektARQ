class Packet:
    def __init__(self, length):
        self.bits = []
        self.length = length

    def addBit(self, bit):
        if len(self.bits) >= self.length:
            return -1
        else:
            self.bits.append(bit)


# ################## test ########################################
x = Packet(8)
for y in range(111):
    if x.addBit(1) == -1:
        print(x.bits)
        #send(x.bitList)
        x = Packet(8)
        x.addBit(1)

print(len(x.bits))
print(x.bits)
