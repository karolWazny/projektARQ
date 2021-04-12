import json
from json import JSONEncoder


class SimulationParameters:
    def __init__(self):
        self.totalLength = None  # int
        self.packetLength = None  # int
        self.noiseModel = None  # słownik, gdzie pierwsza para identyfikuje model, pozostałe to parametry
        self.encoding = None  # słownik, gdzie pierwsza para identyfikuje model, pozostałe to parametry

    @staticmethod
    def fromDictionary(dictionary):
        output = SimulationParameters()
        output.packetLength = dictionary['packetLength']
        output.totalLength = dictionary['totalLength']
        output.encoding = dictionary['encoding']
        output.noiseModel = dictionary['noiseModel']
        return output

    def __eq__(self, other):
        if not isinstance(other, SimulationParameters):
            return NotImplemented

        return self.totalLength == other.totalLength and \
               self.packetLength == other.packetLength and \
               self.encoding == other.encoding and \
               self.noiseModel == other.noiseModel


class SimulationOutput:
    def __init__(self):
        self.transmissionsTotal = None
        self.retransmissions = None
        self.errorsTotal = None
        self.errorsUndetected = None

    @staticmethod
    def fromDictionary(dictionary):
        output = SimulationOutput()
        output.transmissionsTotal = dictionary['transmissionsTotal']
        output.retransmissions = dictionary['retransmissions']
        output.errorsTotal = dictionary['errorsTotal']
        output.errorsUndetected = dictionary['errorsUndetected']
        return output

    def __eq__(self, other):
        if not isinstance(other, SimulationOutput):
            return NotImplemented

        return self.transmissionsTotal == other.transmissionsTotal and \
               self.retransmissions == other.retransmissions and \
               self.errorsTotal == other.errorsTotal and \
               self.errorsUndetected == other.errorsUndetected


class SimulationLog:
    def __init__(self):
        self.params = None
        self.output = None

    @staticmethod
    def fromDictionary(dictionary):
        output = SimulationLog()
        output.params = SimulationParameters.fromDictionary(dictionary['params'])
        output.output = SimulationOutput.fromDictionary(dictionary['output'])
        return output

    def __eq__(self, other):
        if not isinstance(other, SimulationLog):
            return NotImplemented

        return self.params == other.params and \
               self.output == other.output


def saveObjectToJson(objectToSave, fileName):
    fileName = jsonFileNameFrom(fileName)
    with open(fileName, 'w') as fileObject:
        json.dump(objectToSave, fileObject, indent=4, cls=SimulationEncoder)


def readParametersFromJson(fileName):
    dictionary = readFromJson(fileName)
    output = SimulationParameters.fromDictionary(dictionary)
    return output


def readLogFromJson(fileName):
    dictionary = readFromJson(fileName)
    output = SimulationLog.fromDictionary(dictionary)
    return output

def readFromJson(fileName):
    fileName = jsonFileNameFrom(fileName)
    with open(fileName, 'r') as fileObject:
        dictionary = json.load(fileObject)
    return dictionary


def jsonFileNameFrom(name):
    if name.endswith('.json'):
        return name
    return name + '.json'


class SimulationEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == '__main__':
    params = SimulationParameters()
    params.packetLength = 6
    filename = 'params'
    saveObjectToJson(params, filename)
    parameters = readParametersFromJson(filename)
    print(parameters.packetLength)