import tkinter
from ttkthemes import ThemedTk
from tkinter import *
from tkinter import ttk
import threading
import time

# Dummy data classes
class ACUData:
    def __init__(self):
        self.temperature = 11
        self.vicorTemperature = 0
        self.humidity = 12
        self.imdResistance = 0
        self.imdStatus = 0
        self.airPlus = "Armed"
        self.airMinus = "Disarmed"
        self.preRelay = "Disarmed"
        self.TSOver60 = "No"
        self.AMSError = "OK"
        self.IMDError = "OK"
        self.lastError = "None"
        self.AirsStuck = "None"


class BMSData:
    def __init__(self):
        self.minimumCellVoltage = 0.0
        self.minimumCellVoltageID = 0
        self.maximumCellVoltage = 0.0
        self.maximumCellVoltageID = 0
        self.maximumTemperature = 0
        self.maximumTemperatureID = 0
        self.lastError = "None"
        self.ISOSPI = "OK"
        self.voltages = "OK"
        self.temperatures = "OK"
        self.currentSensor = "OK"


class VCUData:
    def __init__(self):
        self.Mode = "OFF"
        self.APPS = 0
        self.BrakeSensor = 0
        self.lastError = "None"


class IVTData:
    def __init__(self):
        self.current = 0
        self.voltage = 605
        self.wattage = 0
        self.wattageCounter = 0
        self.currentCounter = 0


class InverterData:
    def __init__(self):
        self.motorRPM = 23
        self.motorTemperature = 0
        self.igbtTemperature = 0


class TelemetryData:
    def __init__(self):
        self.isConnected = False
        self.PER = 105
        self.timeOutTimer = 0


class DataLoggerData:
    def __init__(self):
        self.vehicleSpeed = 2
        self.wheelRPM = 4


class SharedData:
    def __init__(self):
        self.telemetry = TelemetryData()
        self.acu = ACUData()
        self.vcu = VCUData()
        self.bms = BMSData()
        self.ivt = IVTData()
        self.inverter = InverterData()
        self.datalogger = DataLoggerData()


SharedData = SharedData()

# Initialize the window
root = ThemedTk(theme="arc")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

# Enable dynamic resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Scrollable frame setup
def create_scrollable_frame(parent):
    canvas = Canvas(parent)
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    return scrollable_frame

# Frame για τον Inverter
inverterFrame = Frame(root, bg="lightyellow", highlightbackground="black", highlightthickness=2)
inverterFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

inverterLabel = Label(inverterFrame, text="Inverter:", fg="blue", bg="lightyellow", font=("Arial", 20, "bold"))
inverterLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

inverterRPMLabel = Label(inverterFrame, text="Motor RPM: 23", bg="lightyellow", font=("Arial", 18))
inverterRPMLabel.grid(row=1, column=0, padx=10, pady=5)

inverterMotorTemperatureLabel = Label(inverterFrame, text="Motor Temperature: 0°C", bg="lightyellow", font=("Arial", 18))
inverterMotorTemperatureLabel.grid(row=2, column=0, padx=10, pady=5)

inverterIGBTTemperatureLabel = Label(inverterFrame, text="IGBT Temperature: 0°C", bg="lightyellow", font=("Arial", 18))
inverterIGBTTemperatureLabel.grid(row=3, column=0, padx=10, pady=5)

# Frame για ACU Flags (με scrollbar)
acuFlagsFrame = Frame(root, bg="lightblue", highlightbackground="black", highlightthickness=2)
acuFlagsFrame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
scrollable_acu = create_scrollable_frame(acuFlagsFrame)

acuFlagsLabel = Label(scrollable_acu, text="ACU Flags:", fg="blue", bg="lightblue", font=("Arial", 20, "bold"))
acuFlagsLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

acuAirPlusLabel = Label(scrollable_acu, text="Air+: Armed", bg="lightblue", font=("Arial", 18))
acuAirPlusLabel.grid(row=1, column=0, padx=10, pady=5)

acuAirMinusLabel = Label(scrollable_acu, text="Air-: Disarmed", bg="lightblue", font=("Arial", 18))
acuAirMinusLabel.grid(row=2, column=0, padx=10, pady=5)

acuPreLabel = Label(scrollable_acu, text="Pre: Disarmed", bg="lightblue", font=("Arial", 18))
acuPreLabel.grid(row=3, column=0, padx=10, pady=5)

acuTSOver60Label = Label(scrollable_acu, text="Over 60V: No", bg="lightblue", font=("Arial", 18))
acuTSOver60Label.grid(row=4, column=0, padx=10, pady=5)

acuAMSErrorLabel = Label(scrollable_acu, text="AMS Error: OK", bg="lightblue", font=("Arial", 18))
acuAMSErrorLabel.grid(row=5, column=0, padx=10, pady=5)

acuIMDErrorLabel = Label(scrollable_acu, text="IMD Error: OK", bg="lightblue", font=("Arial", 18))
acuIMDErrorLabel.grid(row=6, column=0, padx=10, pady=5)

acuAirsStuckLabel = Label(scrollable_acu, text="Airs Stuck: No", bg="lightblue", font=("Arial", 18))
acuAirsStuckLabel.grid(row=7, column=0, padx=10, pady=5)

# Frame για ACU Data
acuDataFrame = Frame(root, bg="lightcyan", highlightbackground="black", highlightthickness=2)
acuDataFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

acuDataLabel = Label(acuDataFrame, text="ACU Data:", fg="blue", bg="lightcyan", font=("Arial", 20, "bold"))
acuDataLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

acuHumidityLabel = Label(acuDataFrame, text="Humidity: 12%", bg="lightcyan", font=("Arial", 18))
acuHumidityLabel.grid(row=1, column=0, padx=10, pady=5)

acuTemperatureLabel = Label(acuDataFrame, text="Temperature: 11°C", bg="lightcyan", font=("Arial", 18))
acuTemperatureLabel.grid(row=2, column=0, padx=10, pady=5)

acuIMDResistanceLabel = Label(acuDataFrame, text="IMD Resistance: 0 Ω", bg="lightcyan", font=("Arial", 18))
acuIMDResistanceLabel.grid(row=3, column=0, padx=10, pady=5)

acuVicorTempLabel = Label(acuDataFrame, text="Vicor Temperature: 0°C", bg="lightcyan", font=("Arial", 18))
acuVicorTempLabel.grid(row=4, column=0, padx=10, pady=5)

# Frame για BMS Flags
bmsFrame = Frame(root, bg="lightgreen", highlightbackground="black", highlightthickness=2)
bmsFrame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
scrollable_bms = create_scrollable_frame(bmsFrame)

bmsLabel = Label(scrollable_bms, text="BMS Flags:", fg="blue", bg="lightgreen", font=("Arial", 20, "bold"))
bmsLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

bmsMinVoltageLabel = Label(scrollable_bms, text="Min Voltage: 0.0 V", bg="lightgreen", font=("Arial", 18))
bmsMinVoltageLabel.grid(row=1, column=0, padx=10, pady=5)

bmsMaxVoltageLabel = Label(scrollable_bms, text="Max Voltage: 0.0 V", bg="lightgreen", font=("Arial", 18))
bmsMaxVoltageLabel.grid(row=2, column=0, padx=10, pady=5)

bmsMaxTemperatureLabel = Label(scrollable_bms, text="Max Temp: 0°C", bg="lightgreen", font=("Arial", 18))
bmsMaxTemperatureLabel.grid(row=3, column=0, padx=10, pady=5)

# Frame για IVT Data
ivtFrame = Frame(root, bg="lightgray", highlightbackground="black", highlightthickness=2)
ivtFrame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

ivtLabel = Label(ivtFrame, text="IVT Data:", fg="blue", bg="lightgray", font=("Arial", 20, "bold"))
ivtLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

ivtVoltageLabel = Label(ivtFrame, text="Voltage: 605 V", bg="lightgray", font=("Arial", 18))
ivtVoltageLabel.grid(row=1, column=0, padx=10, pady=5)

ivtCurrentLabel = Label(ivtFrame, text="Current: 0 A", bg="lightgray", font=("Arial", 18))
ivtCurrentLabel.grid(row=2, column=0, padx=10, pady=5)

ivtWattageLabel = Label(ivtFrame, text="Wattage: 0 W", bg="lightgray", font=("Arial", 18))
ivtWattageLabel.grid(row=3, column=0, padx=10, pady=5)

# Frame για VCU Data
vcuFrame = Frame(root, bg="lightcoral", highlightbackground="black", highlightthickness=2)
vcuFrame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

vcuLabel = Label(vcuFrame, text="VCU Data:", fg="blue", bg="lightcoral", font=("Arial", 20, "bold"))
vcuLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

vcuModeLabel = Label(vcuFrame, text="Mode: OFF", bg="lightcoral", font=("Arial", 18))
vcuModeLabel.grid(row=1, column=0, padx=10, pady=5)

vcuAPPSLabel = Label(vcuFrame, text="APPS: 0%", bg="lightcoral", font=("Arial", 18))
vcuAPPSLabel.grid(row=2, column=0, padx=10, pady=5)

vcuBrakeSensorLabel = Label(vcuFrame, text="Brake: 0%", bg="lightcoral", font=("Arial", 18))
vcuBrakeSensorLabel.grid(row=3, column=0, padx=10, pady=5)

# Frame για DataLogger
dataLoggerFrame = Frame(root, bg="lightpink", highlightbackground="black", highlightthickness=2)
dataLoggerFrame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

dataLoggerLabel = Label(dataLoggerFrame, text="Data Logger:", fg="blue", bg="lightpink", font=("Arial", 20, "bold"))
dataLoggerLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

vehicleSpeedLabel = Label(dataLoggerFrame, text="Vehicle Speed: 0 km/h", bg="lightpink", font=("Arial", 18))
vehicleSpeedLabel.grid(row=1, column=0, padx=10, pady=5)

wheelRPMLabel = Label(dataLoggerFrame, text="Wheel RPM: 0", bg="lightpink", font=("Arial", 18))
wheelRPMLabel.grid(row=2, column=0, padx=10, pady=5)

# Dummy data update simulation
def update_values():
    inverterRPMLabel.config(text=f"Motor RPM: {SharedData.inverter.motorRPM}")
    acuAirPlusLabel.config(text=f"Air+: {SharedData.acu.airPlus}")
    acuAirMinusLabel.config(text=f"Air-: {SharedData.acu.airMinus}")
    acuHumidityLabel.config(text=f"Humidity: {SharedData.acu.humidity}%")
    acuTemperatureLabel.config(text=f"Temperature: {SharedData.acu.temperature}°C")
    acuIMDResistanceLabel.config(text=f"IMD Resistance: {SharedData.acu.imdResistance} Ω")
    acuVicorTempLabel.config(text=f"Vicor Temperature: {SharedData.acu.vicorTemperature}°C")
    bmsMinVoltageLabel.config(text=f"Min Voltage: {SharedData.bms.minimumCellVoltage} V")
    ivtVoltageLabel.config(text=f"Voltage: {SharedData.ivt.voltage} V")
    root.after(1000, update_values)

root.after(1000, update_values)
root.mainloop()
