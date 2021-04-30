class Packet:
    def __init__(self):
        self.__content = []
        self.retransmissions = 0

    def add(self, bit):
        self.__content.append(bit)

    def length(self):
        return len(self.__content)

    def content(self):
        return self.__content

    def clear(self):
        return self.__content.clear()

    def retransmissions(self):
        return self.retransmissions

    def distorted(self):
        self.retransmissions += 1

    def __eq__(self, other):
        if isinstance(other, list):
            return other == self.__content
        elif other is None:
            return False
        return other.__dict__ == self.__dict__

    @staticmethod
    def fromList(content):
        output = Packet()
        output.__content = content
        return output
