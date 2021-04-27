from repo.system.ParametersAndOutput import SimulationLog, SimulationParameters, SimulationOutput, saveObjectToJson
from repo.system.Frontend import UserInteraction
from repo.system.Setup import Setup
from repo.system.Frontend import *

if __name__ == '__main__':
    main = Main()
    main.run()

    #simulationLog = SimulationLog()
    #simulationLog.params = SimulationParameters()
    #simulationLog.output = SimulationOutput()
    #user = UserInteraction(simulationLog)
    #userParameters = user.chooseParameters()
    #setup = Setup(userParameters)
    #simulation = setup.getSimulation()
    #simulationEndLog = simulation.simulate()
    # TODO zrobic podawanie nazwy pliku przez uzytkownika albo jakos inaczej
    #filename = 'randomName'
    #saveObjectToJson(simulationEndLog, filename)
