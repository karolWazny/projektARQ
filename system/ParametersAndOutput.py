import json


class SimulationParameters:
    def __init__(self):
        self.totalLength = None  # int
        self.packetLength = None  # int
        self.noiseModel = None  # słownik, gdzie pierwsza para identyfikuje model, pozostałe to parametry
        self.encoding = None  # słownik, gdzie pierwsza para identyfikuje model, pozostałe to parametry


class SimulationOutput:
    def __init__(self):
        self.transmissionsTotal = None
        self.retransmissions = None
        self.errorsTotal = None
        self.errorsUndetected = None


def saveParametersToFile(parameters, fileName):
    with open(fileName, 'w') as fileObject:
        json.dump(parameters.__dict__, fileObject)


def readParametersFromFile(fileName):
    with open(fileName, 'r') as fileObject:
        dictionary = json.load(fileObject)
        parameters = SimulationParameters()
        parameters.packetLength = dictionary['packetLength']
        parameters.totalLength = dictionary['totalLength']
        parameters.encoding = dictionary['encoding']
        parameters.noiseModel = dictionary['noiseModel']
    return parameters


if __name__ == '__main__':
    params = SimulationParameters()
    params.packetLength = 5
    filename = 'params.json'
    saveParametersToFile(params, filename)
    parameters = readParametersFromFile(filename)
    print(parameters.packetLength)
