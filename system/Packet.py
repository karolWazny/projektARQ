class Packet:
    def __init__(self, length):
        self.bitList = []
        self.length = length

    def addBit(self, bit):
        if len(self.bitList) >= self.length:
            return -1
        else:
            self.bitList.append(bit)


# ################## test ########################################
x = Packet(8)
for y in range(111):
    if x.addBit(1) == -1:
        print(x.bitList)
        # send(x.bitList)
        x = Packet(8)
        x.addBit(1)

print(len(x.bitList))
print(x.bitList)
