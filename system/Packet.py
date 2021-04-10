class Packet:
    def __init__(self):
        self.__content = []

    def add(self, bit):
        self.__content.append(bit)

    def length(self):
        return len(self.__content)

    def content(self):
        return self.__content

    @staticmethod
    def fromList(content):
        output = Packet()
        output.__content = content
        return output
