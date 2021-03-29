import unittest
from ..system.ParametersAndOutput import *


class FilesHandlingTest(unittest.TestCase):

    def test_parametersToFromFile(self):
        params = SimulationParameters()
        params.totalLength = 100
        params.packetLength = 5
        saveObjectToJson(params, 'params')
        read_params = readParametersFromJson('params')
        self.assertEqual(params, read_params)

    def test_logToFromFile(self):
        params = SimulationParameters()
        params.totalLength = 100
        params.packetLength = 5
        output = SimulationOutput()
        output.transmissionsTotal = 23
        output.retransmissions = 3
        output.errorsTotal = 4
        output.errorsUndetected = 1
        log = SimulationLog()
        log.params = params
        log.output = output
        saveObjectToJson(log, 'log')
        read_log = readLogFromJson('log.json')
        self.assertEqual(log, read_log)
if __name__ == '__main__':
    unittest.main()
