class Diver:
    @staticmethod
    def divSignal(signal, packetSize):
        signalLength = (len(signal))
        counter = 0
        packetList = []
        while (counter + 1) * packetSize < signalLength:
            packetList.append(signal[0 + counter * packetSize:packetSize * (counter + 1)])
            counter += 1
        packetList.append(signal[packetSize * counter:signalLength])
        return packetList