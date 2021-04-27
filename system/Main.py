from .ParametersAndOutput import SimulationLog, SimulationParameters, SimulationOutput, saveObjectToJson
from .Frontend import UserInteraction
from .Setup import Setup


class Main:
    if __name__ == '__main__':
        simulationLog = SimulationLog()
        simulationLog.params = SimulationParameters()
        simulationLog.output = SimulationOutput()
        user = UserInteraction(simulationLog)
        userParameters = user.chooseParameters()
        setup = Setup(userParameters)
        simulation = setup.run()
        simulationEndLog = simulation.simulate()
        # TODO zrobic podawanie nazwy pliku przez uzytkownika albo jakos inaczej
        filename = 'randomName'
        saveObjectToJson(simulationEndLog, filename)
