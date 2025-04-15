import tkinter
from ttkthemes import ThemedTk
from tkinter import *
from tkinter import ttk
from datetime import datetime
import serial
import serial.tools.list_ports
import threading
from history_tab import HistoryTab  # Ensure history_tab.py has its demo code wrapped in if __name__ == "__main__"

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

# Initialize the main window
root = ThemedTk(theme="arc")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

# Create a shared data instance
shared_data = SharedData()

# Create the main Notebook with two tabs
main_notebook = ttk.Notebook(root)
main_notebook.pack(expand=True, fill="both")

# Dashboard Tab
dashboard_frame = Frame(main_notebook)
main_notebook.add(dashboard_frame, text="Dashboard")

# ================= SERIAL CONNECTION PANEL ====================
serial_frame = Frame(dashboard_frame, bg="white", highlightbackground="black", highlightthickness=2)
serial_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
Label(serial_frame, text="Serial Port:", font=("Arial", 16), bg="white").pack(side=LEFT, padx=10)

# Dropdown to select port
port_var = StringVar()
available_ports = [port.device for port in serial.tools.list_ports.comports()]
port_dropdown = ttk.Combobox(serial_frame, textvariable=port_var, values=available_ports, state="readonly")
port_dropdown.pack(side=LEFT, padx=10)

# Connection status label
connection_status = Label(serial_frame, text="Not Connected", bg="white", fg="red", font=("Arial", 14, "italic"))
connection_status.pack(side=LEFT, padx=10)

# Connect button logic
serial_connection = None


def read_serial():
    global serial_connection
    while serial_connection and serial_connection.is_open:
        try:
            line = serial_connection.readline().decode().strip()
            if line:
                print("Serial Data:", line)
                # Example parsing logic (adjust format to your actual serial data)
                if line.startswith("RPM:"):
                    rpm = int(line.split(":")[1])
                    shared_data.inverter.motorRPM = rpm
        except Exception as e:
            print("Read error:", e)


def connect_serial():
    global serial_connection
    port = port_var.get()
    if port:
        try:
            serial_connection = serial.Serial(port, 9600, timeout=1)
            connection_status.config(text=f"Connected to {port}", fg="green")
            threading.Thread(target=read_serial, daemon=True).start()
        except serial.SerialException as e:
            connection_status.config(text="Connection Failed", fg="red")
            print(f"Error: {e}")

Button(serial_frame, text="Connect", command=connect_serial).pack(side=LEFT, padx=10)
# ==============================================================

# Adjust grid layout
for i in range(1, 5):
    dashboard_frame.grid_rowconfigure(i, weight=1)
dashboard_frame.grid_columnconfigure(0, weight=1)
dashboard_frame.grid_columnconfigure(1, weight=1)

# --- Dashboard Content ---
# Inverter frame
inverterFrame = Frame(dashboard_frame, bg="lightyellow", highlightbackground="black", highlightthickness=2)
inverterFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
Label(inverterFrame, text="Inverter:", fg="blue", bg="lightyellow", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
inverterRPMLabel = Label(inverterFrame, text="Motor RPM: 23", bg="lightyellow", font=("Arial", 18))
inverterRPMLabel.grid(row=1, column=0, padx=10, pady=5)
Label(inverterFrame, text="Motor Temperature: 0°C", bg="lightyellow", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=5)
Label(inverterFrame, text="IGBT Temperature: 0°C", bg="lightyellow", font=("Arial", 18)).grid(row=3, column=0, padx=10, pady=5)

# Function to create a scrollable frame (used for flags)
def create_scrollable_frame(parent):
    canvas = Canvas(parent)
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    return scrollable_frame

# ACU Flags frame with scrollbar
acuFlagsFrame = Frame(dashboard_frame, bg="lightblue", highlightbackground="black", highlightthickness=2)
acuFlagsFrame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
scrollable_acu = create_scrollable_frame(acuFlagsFrame)
Label(scrollable_acu, text="ACU Flags:", fg="blue", bg="lightblue", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(scrollable_acu, text="Air+: Armed", bg="lightblue", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=5)
Label(scrollable_acu, text="Air-: Disarmed", bg="lightblue", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=5)
Label(scrollable_acu, text="Pre: Disarmed", bg="lightblue", font=("Arial", 18)).grid(row=3, column=0, padx=10, pady=5)
Label(scrollable_acu, text="Over 60V: No", bg="lightblue", font=("Arial", 18)).grid(row=4, column=0, padx=10, pady=5)
Label(scrollable_acu, text="AMS Error: OK", bg="lightblue", font=("Arial", 18)).grid(row=5, column=0, padx=10, pady=5)
Label(scrollable_acu, text="IMD Error: OK", bg="lightblue", font=("Arial", 18)).grid(row=6, column=0, padx=10, pady=5)
Label(scrollable_acu, text="Airs Stuck: No", bg="lightblue", font=("Arial", 18)).grid(row=7, column=0, padx=10, pady=5)

# ACU Data frame
acuDataFrame = Frame(dashboard_frame, bg="lightcyan", highlightbackground="black", highlightthickness=2)
acuDataFrame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
Label(acuDataFrame, text="ACU Data:", fg="blue", bg="lightcyan", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(acuDataFrame, text="Humidity: 12%", bg="lightcyan", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=5)
Label(acuDataFrame, text="Temperature: 11°C", bg="lightcyan", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=5)
Label(acuDataFrame, text="IMD Resistance: 0 Ω", bg="lightcyan", font=("Arial", 18)).grid(row=3, column=0, padx=10, pady=5)
Label(acuDataFrame, text="Vicor Temperature: 0°C", bg="lightcyan", font=("Arial", 18)).grid(row=4, column=0, padx=10, pady=5)

# BMS Flags frame
bmsFrame = Frame(dashboard_frame, bg="lightgreen", highlightbackground="black", highlightthickness=2)
bmsFrame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
scrollable_bms = create_scrollable_frame(bmsFrame)
Label(scrollable_bms, text="BMS Flags:", fg="blue", bg="lightgreen", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(scrollable_bms, text="Min Voltage: 0.0 V", bg="lightgreen", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=5)
Label(scrollable_bms, text="Max Voltage: 0.0 V", bg="lightgreen", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=5)
Label(scrollable_bms, text="Max Temp: 0°C", bg="lightgreen", font=("Arial", 18)).grid(row=3, column=0, padx=10, pady=5)

# IVT Data frame
ivtFrame = Frame(dashboard_frame, bg="lightgray", highlightbackground="black", highlightthickness=2)
ivtFrame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
Label(ivtFrame, text="IVT Data:", fg="blue", bg="lightgray", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(ivtFrame, text="Voltage: 605 V", bg="lightgray", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=5)
Label(ivtFrame, text="Current: 0 A", bg="lightgray", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=5)
Label(ivtFrame, text="Wattage: 0 W", bg="lightgray", font=("Arial", 18)).grid(row=3, column=0, padx=10, pady=5)

# VCU Data frame
vcuFrame = Frame(dashboard_frame, bg="lightcoral", highlightbackground="black", highlightthickness=2)
vcuFrame.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")
Label(vcuFrame, text="VCU Data:", fg="blue", bg="lightcoral", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(vcuFrame, text="Mode: OFF", bg="lightcoral", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=5)
Label(vcuFrame, text="APPS: 0%", bg="lightcoral", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=5)
Label(vcuFrame, text="Brake: 0%", bg="lightcoral", font=("Arial", 18)).grid(row=3, column=0, padx=10, pady=5)

# Data Logger frame
dataLoggerFrame = Frame(dashboard_frame, bg="lightpink", highlightbackground="black", highlightthickness=2)
dataLoggerFrame.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
Label(dataLoggerFrame, text="Data Logger:", fg="blue", bg="lightpink", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(dataLoggerFrame, text="Vehicle Speed: 0 km/h", bg="lightpink", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=5)
Label(dataLoggerFrame, text="Wheel RPM: 0", bg="lightpink", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=5)

# History Tab (added as a separate tab)
history_tab = HistoryTab(main_notebook, shared_data)

# Dummy data update simulation
def update_values():
    inverterRPMLabel.config(text=f"Motor RPM: {shared_data.inverter.motorRPM}")
    # Update additional dashboard labels as needed...
    root.after(1000, update_values)

root.after(1000, update_values)
root.mainloop()

