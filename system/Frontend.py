import copy
import tkinter as tk
from tkinter import IntVar

from repo.system.ParametersAndOutput import *
from repo.system.Enums import *
from repo.system.Setup import *
from datetime import datetime
from repo.system.ParametersAndOutput import SimulationEncoder


def listMessageBox(arr, parent):
    window = tk.Toplevel(master=parent)
    listbox = tk.Listbox(window)
    listbox.pack(fill=tk.BOTH, expand=1)  # adds listbox to window
    [listbox.insert(tk.END, row) for row in arr]  # one line for loop
    window.grab_set()


arr = ['a', 'b', 'c', '1', '2', '3']


# klasa przekazana w ręce Karola
class UserInteraction:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog

    def chooseParameters(self):
        while self.simulationLog.params.packetLength is not None or self.simulationLog.params.totalLength is not None \
                or self.simulationLog.params.encoding is not None or self.simulationLog.params.noiseModel is not None:
            try:
                self.simulationLog.params.totalLength = input("Podaj dlugosc ciagu do transmisji: ")
                if not type(self.simulationLog.params.totalLength) is int:
                    raise TypeError("Only integers are allowed")
                if self.simulationLog.params.totalLength < 0:
                    raise ValueError("Sorry, no numbers below zero")
                self.simulationLog.params.packetLength = input("Podaj dlugosc wysylanego pakietu")
                if not type(self.simulationLog.params.packetLength) is int:
                    raise TypeError("Only integers are allowed")
                if self.simulationLog.params.packetLength < 0:
                    raise ValueError("Sorry, no numbers below zero")
                self.simulationLog.params.noiseModel = input("Podaj rodzaj znieksztalcania")
                if not self.simulationLog.params.__eq__(self.simulationLog.params.noiseModel):
                    raise NameError("Only noiseModels from dictionary are allowed")
                self.simulationLog.params.encoding = input("Podaj rodzaj kodowania")
                if not self.simulationLog.params.__eq__(self.simulationLog.params.encoding):
                    raise NameError("Only codingModels from dictionary are allowed")
            except (TypeError, ValueError, NameError):
                pass
        return self.simulationLog


class Main:
    def __init__(self):
        self.window = self.prepareWindow()
        self.parameters = self.obtainParameters()

    def prepareWindow(self):
        window = tk.Tk(className="arq simulator")  # todo wymusic zaczynanie z wielkiej litery
        runButt = tk.Button(window, text="Run simulation", command=self.runSimulation)
        runButt.pack()
        paramButt = tk.Button(window, text="Change Parameters", command=self.changeParameters)
        paramButt.pack()
        window.geometry("250x100")
        return window

    def run(self):
        self.window.mainloop()

    def obtainParameters(self):
        try:
            params = readParametersFromJson('params.json')
        except FileNotFoundError:
            params = self.makeDefaultParameters()
            saveObjectToJson(params, 'params.json')
        return params

    def makeDefaultParameters(self):
        params = SimulationParameters()
        params.packetLength = 8
        params.totalLength = 1024
        params.noiseModel = {'type': Noise.BINARY_SYMMETRIC,
                             'BER': 10}
        params.encoding = {'type': Encoding.PARITY,
                           'packetLength': 8,
                           'totalLength': 1024}
        return params

    def runSimulation(self):
        now = datetime.now()
        log = SimulationLog()
        log.params = self.parameters
        setup = Setup(log)
        simulation = setup.getSimulation()
        simulation.simulate()
        filename = now.strftime("%Y-%m-%d-%H%M%S")
        saveObjectToJson(log, filename)

    def changeParameters(self):
        paramWindow = ParametersChanger(self.parameters)
        paramWindow.run()
        saveObjectToJson(self.parameters, 'params.json')


class ParametersChanger:
    def __init__(self, parameters):
        self.parameters = parameters
        self.encText = None
        self.chText = None
        self.window = self.prepareWindow()

    def run(self):
        self.window.grab_set()
        self.window.wait_window()

    def prepareWindow(self):
        window = tk.Toplevel()
        mainFrame = tk.Frame(window)
        mainFrame.pack()
        encodingFrame = tk.Frame(mainFrame)
        encodingFrame.pack(side=tk.LEFT)
        tk.Label(master=encodingFrame, text='Encoding model').pack(side=tk.TOP)
        self.encText = tk.Text(master=encodingFrame)
        self.encText.pack(side=tk.TOP)
        self.encText.insert(tk.INSERT, json.dumps(self.parameters.encoding, indent=2, cls=SimulationEncoder))
        self.encText.configure(state=tk.DISABLED)
        tk.Button(master=encodingFrame, text='Change encoding', command=self.changeChannel).pack(side=tk.BOTTOM)
        channelFrame = tk.Frame(master=mainFrame)
        channelFrame.pack(side=tk.RIGHT)
        tk.Label(master=channelFrame, text='Channel model').pack(side=tk.TOP)
        self.chText = tk.Text(master=channelFrame)
        self.chText.pack(side=tk.TOP)
        self.chText.insert(tk.INSERT, json.dumps(self.parameters.noiseModel, indent=2, cls=SimulationEncoder))
        self.chText.configure(state=tk.DISABLED)
        tk.Button(master=channelFrame, text='Change channel').pack(side=tk.BOTTOM)
        return window

    def changeChannel(self):
        self.parameters.noiseModel = ChannelWizard(self.window).run()
        self.update(self.chText, self.parameters.noiseModel)

    def update(self, textField, textSource):
        textField.configure(state=tk.NORMAL)
        textField.delete(1.0, tk.END)
        textField.insert(tk.INSERT, json.dumps(textSource, indent=2, cls=SimulationEncoder))
        textField.configure(state=tk.DISABLED)


class ChannelWizard:
    def __init__(self, master):
        self.master = master
        self.channel = dict()

    def run(self):
        self.chooseType()
        if not self.channel['type'] == 'TWO_STATE':
            self.chooseBer()
            return self.channel

    def chooseType(self):
        dialog = tk.Toplevel(master=self.master)
        dialog.title("Channel type")
        options = ["BINARY_SYMMETRIC", "BINARY_ERASURE", "Z_CHANNEL", "TWO_STATE"]
        strVar = tk.StringVar()
        strVar.set(options[0])
        optionMenu = tk.OptionMenu(dialog, strVar, *options)
        optionMenu.pack(side=tk.TOP)

        okButt = tk.Button(master=dialog, text="OK", command=lambda: self.closeDialog({'type': strVar.get()}, dialog))
        okButt.pack(side=tk.BOTTOM)
        dialog.grab_set()
        dialog.wait_window()

    def chooseBer(self):
        dialog = tk.Toplevel(master=self.master)
        dialog.title("BER")

        label = tk.Label(master=dialog, text="Input BER in %:")
        label.pack(side=tk.TOP)

        intVar: IntVar = tk.IntVar()
        intVar.set(0)

        textBox = tk.Entry(master=dialog, textvariable=intVar)
        textBox.pack(side=tk.TOP)

        okButt = tk.Button(master=dialog, text="OK", command=lambda: self.closeDialog({'BER': intVar.get()}, dialog))
        okButt.pack(side=tk.BOTTOM)

        dialog.grab_set()
        dialog.wait_window()

    def closeDialog(self, diction, dialog):
        self.channel.update(diction)
        dialog.destroy()
