import tkinter as tk
import tkinter.filedialog
from tkinter import IntVar

from Tools.scripts.dutree import display
from ipyfilechooser import FileChooser

from .ParametersAndOutput import *
from .Enums import *
from .Setup import *
from datetime import datetime
from .ParametersAndOutput import SimulationEncoder
import ctypes


def packetLengthWithNParityBits(parityBits):
    return 2 ** parityBits - parityBits - 1


def centerDialog(window):
    window.resizable(False, False)  # This code helps to disable windows from resizing

    window_height = 70
    window_width = 300

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


class Main:
    def __init__(self):
        self.window = self.prepareWindow()
        self.parameters = self.obtainParameters()
        self.output = None

    def prepareWindow(self):
        window = tk.Tk(className="arq simulator")  # todo wymusic zaczynanie z wielkiej litery
        runButt = tk.Button(window, text="Run simulation", command=self.runSimulation)
        runButt.pack()
        paramButt = tk.Button(window, text="Change Parameters", command=self.changeParameters)
        paramButt.pack()
        manyButt = tk.Button(window, text="Run in a series", command=self.runSeries)
        manyButt.pack()
        fileButt = tk.Button(window, text="Choose output file", command=self.chooseFile)
        fileButt.pack()
        window.geometry("250x120")
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

    def chooseFile(self):
        filename = tkinter.filedialog.askopenfilename()
        self.output = readObjectFromJson(MultipleRunLog, filename)

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

    def runSeries(self):
        log = SimulationLog()
        log.params = self.parameters
        log.output = []
        tmpLog = SimulationLog()
        tmpLog.params = self.parameters
        setup = Setup(tmpLog)
        simulation = setup.getSimulation()
        filename = self.generateCurrentTimeString()
        for index in range(0, 10000):
            simulation.simulate()
            log.output.append(tmpLog.output)
            simulation.reset()
        saveObjectToJson(log, filename)

    @staticmethod
    def generateCurrentTimeString():
        now = datetime.now()
        return now.strftime("%Y-%m-%d-%H%M%S")


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
        tk.Button(master=encodingFrame, text='Change encoding', command=self.changeEncoding).pack(side=tk.BOTTOM)
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

    def changeEncoding(self):
        self.parameters.encoding = EncodingWizard(self.window).run()
        self.parameters.totalLength = self.parameters.encoding['totalLength']
        self.parameters.packetLength = self.parameters.encoding['packetLength']
        self.update(self.encText, self.parameters.encoding)

    def update(self, textField, textSource):
        textField.configure(state=tk.NORMAL)
        textField.delete(1.0, tk.END)
        textField.insert(tk.INSERT, json.dumps(textSource, indent=2, cls=SimulationEncoder))
        textField.configure(state=tk.DISABLED)


class Wizard:
    def __init__(self, master):
        self.diction = dict()
        self.master = master

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

        centerDialog(dialog)

        dialog.grab_set()
        dialog.wait_window()

    def closeDialog(self, diction, dialog):
        self.diction.update(diction)
        dialog.destroy()

    def chooseType(self, options):
        dialog = tk.Toplevel(master=self.master)
        dialog.title("Channel type")
        strVar = tk.StringVar()
        strVar.set(options[0])
        optionMenu = tk.OptionMenu(dialog, strVar, *options)
        optionMenu.pack(side=tk.TOP)

        okButt = tk.Button(master=dialog, text="OK", command=lambda: self.closeDialog({'type': strVar.get()}, dialog))
        okButt.pack(side=tk.BOTTOM)

        centerDialog(dialog)
        dialog.grab_set()
        dialog.wait_window()


class ChannelWizard(Wizard):
    def __init__(self, master):
        super().__init__(master)

    def run(self):
        self.chooseType(["BINARY_SYMMETRIC", "BINARY_ERASURE", "Z_CHANNEL", "TWO_STATE"])
        if self.diction['type'] == 'TWO_STATE':
            self.chooseInt("1 to 2", "Input probability of changing state from 1 to 2 in %:",
                           'firstToSecondProbability')
            self.chooseInt("2 to 1", "Input probability of changing state from 2 to 1 in %:",
                           'secondToFirstProbability')
            ctypes.windll.user32.MessageBoxW(0, "Now proceed with setting inner channel 1", "State 1", 0)
            innerChannel = ChannelWizard(self.master).run()
            self.diction.update({'firstChannel': innerChannel})
            ctypes.windll.user32.MessageBoxW(0, "Now proceed with setting inner channel 2", "State 2", 0)
            innerChannel = ChannelWizard(self.master).run()
            self.diction.update({'secondChannel': innerChannel})
        else:
            self.chooseBer()
        return self.diction

    def chooseBer(self):
        self.chooseInt("BER", "Input BER in %:", 'BER')


class EncodingWizard(Wizard):
    def __init__(self, master):
        super().__init__(master)

    def run(self):
        self.chooseTotalLength()
        self.chooseType(['PARITY', 'HAMMING', 'CRC'])
        if self.diction['type'] == 'PARITY':
            self.choosePacketLength()
        elif self.diction['type'] == 'HAMMING':
            self.chooseParityBits()
            self.diction.update({'packetLength': packetLengthWithNParityBits(self.diction['parityBits'])})
        elif self.diction['type'] == 'CRC':
            self.choosePacketLength()
            self.chooseEncodingKey()
        return self.diction

    def chooseTotalLength(self):
        self.chooseInt("Total length", "Input total number of bits to be sent:", 'totalLength')

    def choosePacketLength(self):
        self.chooseInt("Packet length", "Input the number of bits in one packet before encoding:", 'packetLength')

    def chooseParityBits(self):
        self.chooseInt("Parity bits", "Input the number of redundancy bits in one packet:", 'parityBits')

    def chooseEncodingKey(self):
        dialog = tk.Toplevel(master=self.master)
        dialog.title('Key')

        label = tk.Label(master=dialog,
                         text='Polynomial (oldest to youngest separated with ",":')
        label.pack(side=tk.TOP)

        strVar = tk.StringVar()

        textBox = tk.Entry(master=dialog, textvariable=strVar)
        textBox.pack(side=tk.TOP)

        okButt = tk.Button(master=dialog, text="OK",
                           command=lambda: self.parseArrayAndClose('key', dialog, strVar.get()))
        okButt.pack(side=tk.BOTTOM)

        centerDialog(dialog)
        dialog.grab_set()
        dialog.wait_window()

    def parseArrayAndClose(self, key, dialog, stringToParse):
        arr = stringToParse.split(',')
        out = []
        for element in arr:
            out.append(int(element))
        self.closeDialog({key: out}, dialog)
