import copy
import tkinter as tk
from tkinter import IntVar

from repo.system.ParametersAndOutput import *
from repo.system.Enums import *
from repo.system.Setup import *
from datetime import datetime
from repo.system.ParametersAndOutput import SimulationEncoder
import ctypes  # An included library with Python install.

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
        self.parameters.totalLength = self.parameters.encoding['totalLength']
        self.parameters.packetLength = self.parameters.encoding['packetLength']
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
        self.update(self.encText, self.parameters.encoding)
        tk.Button(master=encodingFrame, text='Change encoding').pack(side=tk.BOTTOM)
        channelFrame = tk.Frame(master=mainFrame)
        channelFrame.pack(side=tk.RIGHT)
        tk.Label(master=channelFrame, text='Channel model').pack(side=tk.TOP)
        self.chText = tk.Text(master=channelFrame)
        self.chText.pack(side=tk.TOP)
        self.update(self.chText, self.parameters.noiseModel)
        tk.Button(master=channelFrame, text='Change channel', command=self.changeChannel).pack(side=tk.BOTTOM)
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
        if self.channel['type'] == 'TWO_STATE':
            self.chooseInt("1 to 2", "Input probability of changing state from 1 to 2 in %:",
                           'firstToSecondProbability')
            self.chooseInt("2 to 1", "Input probability of changing state from 2 to 1 in %:",
                           'secondToFirstProbability')
            ctypes.windll.user32.MessageBoxW(0, "Now proceed with setting inner channel 1", "State 1", 0)
            innerChannel = ChannelWizard(self.master).run()
            self.channel.update({'firstChannel': innerChannel})
            ctypes.windll.user32.MessageBoxW(0, "Now proceed with setting inner channel 2", "State 2", 0)
            innerChannel = ChannelWizard(self.master).run()
            self.channel.update({'secondChannel': innerChannel})
        else:
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
        self.chooseInt("BER", "Input BER in %:", 'BER')

    def chooseInt(self, title, label, key):
        dialog = tk.Toplevel(master=self.master)
        dialog.title(title)

        label = tk.Label(master=dialog, text=label)
        label.pack(side=tk.TOP)

        intVar: IntVar = tk.IntVar()
        intVar.set(0)

        textBox = tk.Entry(master=dialog, textvariable=intVar)
        textBox.pack(side=tk.TOP)

        okButt = tk.Button(master=dialog, text="OK", command=lambda: self.closeDialog({key: intVar.get()}, dialog))
        okButt.pack(side=tk.BOTTOM)

        dialog.grab_set()
        dialog.wait_window()

    def closeDialog(self, diction, dialog):
        self.channel.update(diction)
        dialog.destroy()
