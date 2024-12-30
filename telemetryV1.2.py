import serial
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import datetime
import serial.tools.list_ports

# Data Classes for Telemetry
class ACUData:
    def __init__(self):
        self.temperature = 11
        self.vicorTemperature = 0
        self.humidity = 12
        self.imdResistance = 0
        self.airPlus = "Armed"
        self.airMinus = "Disarmed"
        self.preRelay = "Disarmed"
        self.TSOver60 = "No"
        self.AMSError = "OK"
        self.IMDError = "OK"
        self.AirsStuck = "No"

class BMSData:
    def __init__(self):
        self.minimumCellVoltage = 0.0
        self.maximumCellVoltage = 0.0
        self.maximumTemperature = 0

class VCUData:
    def __init__(self):
        self.mode = "OFF"
        self.apps = 0.0
        self.brakeSensor = 0.0

class IVTData:
    def __init__(self):
        self.current = 0.0
        self.voltage = 605.0
        self.wattage = 0.0

class InverterData:
    def __init__(self):
        self.motorRPM = 23
        self.motorTemperature = 30
        self.igbtTemperature = 35

class SharedData:
    def __init__(self):
        self.acu = ACUData()
        self.bms = BMSData()
        self.vcu = VCUData()
        self.ivt = IVTData()
        self.inverter = InverterData()

shared_data = SharedData()

# Serial Connection Setup
def setup_serial(port="COM3", baudrate=9600):
    available_ports = [p.device for p in serial.tools.list_ports.comports()]
    print(f"Available ports: {available_ports}")
    if port not in available_ports:
        print(f"Port {port} is not available. Please choose from {available_ports}")
        return None
    try:
        return serial.Serial(port=port, baudrate=baudrate, timeout=1)
    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
        return None

serial_port = setup_serial()

# Tkinter GUI Setup
root = ThemedTk(theme="arc")
root.title("Telemetry Dashboard")
root.geometry("1200x800")

# Notebook for Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

# History Tab
class HistoryTab:
    def __init__(self, notebook):
        self.frame = Frame(notebook)
        notebook.add(self.frame, text="History")
        self.tree = ttk.Treeview(self.frame, columns=("timestamp", "parameter", "value"), show="headings")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("parameter", text="Parameter")
        self.tree.heading("value", text="Value")
        self.tree.pack(expand=True, fill=BOTH)

    def add_entry(self, parameter, value):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tree.insert("", "end", values=(current_time, parameter, value))

history_tab = HistoryTab(notebook)

# Dashboard Tab
dashboad_frame = Frame(notebook)
notebook.add(dashboad_frame, text="Dashboard")

# Layout Configuration for Dashboard
for i in range(4):
    dashboad_frame.grid_rowconfigure(i, weight=1)
for j in range(2):
    dashboad_frame.grid_columnconfigure(j, weight=1)

# ACU Frame
acu_frame = Frame(dashboad_frame, bg="lightblue", highlightbackground="black", highlightthickness=2)
acu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
acu_label = Label(acu_frame, text="ACU Data", bg="lightblue", font=("Arial", 16, "bold"))
acu_label.pack()
acu_temperature_label = Label(acu_frame, text=f"Temperature: {shared_data.acu.temperature}°C", bg="lightblue")
acu_temperature_label.pack()
acu_humidity_label = Label(acu_frame, text=f"Humidity: {shared_data.acu.humidity}%", bg="lightblue")
acu_humidity_label.pack()

# BMS Frame
bms_frame = Frame(dashboad_frame, bg="lightgreen", highlightbackground="black", highlightthickness=2)
bms_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
bms_label = Label(bms_frame, text="BMS Data", bg="lightgreen", font=("Arial", 16, "bold"))
bms_label.pack()
bms_min_voltage_label = Label(bms_frame, text=f"Min Voltage: {shared_data.bms.minimumCellVoltage}V", bg="lightgreen")
bms_min_voltage_label.pack()
bms_max_voltage_label = Label(bms_frame, text=f"Max Voltage: {shared_data.bms.maximumCellVoltage}V", bg="lightgreen")
bms_max_voltage_label.pack()
bms_max_temp_label = Label(bms_frame, text=f"Max Temp: {shared_data.bms.maximumTemperature}°C", bg="lightgreen")
bms_max_temp_label.pack()

# VCU Frame
vcu_frame = Frame(dashboad_frame, bg="lightyellow", highlightbackground="black", highlightthickness=2)
vcu_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
vcu_label = Label(vcu_frame, text="VCU Data", bg="lightyellow", font=("Arial", 16, "bold"))
vcu_label.pack()
vcu_mode_label = Label(vcu_frame, text=f"Mode: {shared_data.vcu.mode}", bg="lightyellow")
vcu_mode_label.pack()
vcu_apps_label = Label(vcu_frame, text=f"APPS: {shared_data.vcu.apps}%", bg="lightyellow")
vcu_apps_label.pack()
vcu_brake_label = Label(vcu_frame, text=f"Brake Sensor: {shared_data.vcu.brakeSensor}%", bg="lightyellow")
vcu_brake_label.pack()

# IVT Frame
ivt_frame = Frame(dashboad_frame, bg="lightcoral", highlightbackground="black", highlightthickness=2)
ivt_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
ivt_label = Label(ivt_frame, text="IVT Data", bg="lightcoral", font=("Arial", 16, "bold"))
ivt_label.pack()
ivt_current_label = Label(ivt_frame, text=f"Current: {shared_data.ivt.current}A", bg="lightcoral")
ivt_current_label.pack()
ivt_voltage_label = Label(ivt_frame, text=f"Voltage: {shared_data.ivt.voltage}V", bg="lightcoral")
ivt_voltage_label.pack()
ivt_wattage_label = Label(ivt_frame, text=f"Wattage: {shared_data.ivt.wattage}W", bg="lightcoral")
ivt_wattage_label.pack()

# Inverter Frame
inverter_frame = Frame(dashboad_frame, bg="lightgray", highlightbackground="black", highlightthickness=2)
inverter_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
inverter_label = Label(inverter_frame, text="Inverter Data", bg="lightgray", font=("Arial", 16, "bold"))
inverter_label.pack()
inverter_rpm_label = Label(inverter_frame, text=f"Motor RPM: {shared_data.inverter.motorRPM}", bg="lightgray")
inverter_rpm_label.pack()
inverter_motor_temp_label = Label(inverter_frame, text=f"Motor Temp: {shared_data.inverter.motorTemperature}°C", bg="lightgray")
inverter_motor_temp_label.pack()
inverter_igbt_temp_label = Label(inverter_frame, text=f"IGBT Temp: {shared_data.inverter.igbtTemperature}°C", bg="lightgray")
inverter_igbt_temp_label.pack()

# Serial Data Processing
def process_serial_data(data):
    print(f"Received data: {data}")  # Debug raw data
    try:
        key_value_pairs = data.split(",")
        for pair in key_value_pairs:
            if ":" in pair:
                key, value = pair.split(":")
                key = key.strip().upper()
                value = value.strip()
                if key == "TEMP":
                    shared_data.acu.temperature = float(value)
                    history_tab.add_entry("Temperature", f"{value}°C")
                elif key == "HUMIDITY":
                    shared_data.acu.humidity = float(value)
                    history_tab.add_entry("Humidity", f"{value}%")
                elif key == "VOLTAGE":
                    shared_data.ivt.voltage = float(value)
                    history_tab.add_entry("Voltage", f"{value}V")
                elif key == "CURRENT":
                    shared_data.ivt.current = float(value)
                    history_tab.add_entry("Current", f"{value}A")
                elif key == "APPS":
                    shared_data.vcu.apps = float(value)
                    history_tab.add_entry("APPS", f"{value}%")
    except ValueError as e:
        print(f"Error processing data: {data}, Error: {e}")

# Serial Data Reader
def read_serial_data():
    if running:
        try:
            if serial_port and serial_port.in_waiting > 0:
                line = serial_port.readline().decode("utf-8").strip()
                process_serial_data(line)
        except Exception as e:
            print(f"Serial read error: {e}")
        finally:
            root.after(100, read_serial_data)

# Simulate Serial Data for Testing (Optional)
def simulate_serial_data():
    if running:
        simulated_data = "TEMP:25,HUMIDITY:50,VOLTAGE:605,CURRENT:10,APPS:30"
        process_serial_data(simulated_data)
        root.after(1000, simulate_serial_data)

# Update GUI
def update_gui():
    if running:
        acu_temperature_label.config(text=f"Temperature: {shared_data.acu.temperature}°C")
        acu_humidity_label.config(text=f"Humidity: {shared_data.acu.humidity}%")
        bms_min_voltage_label.config(text=f"Min Voltage: {shared_data.bms.minimumCellVoltage}V")
        bms_max_voltage_label.config(text=f"Max Voltage: {shared_data.bms.maximumCellVoltage}V")
        bms_max_temp_label.config(text=f"Max Temp: {shared_data.bms.maximumTemperature}°C")
        vcu_mode_label.config(text=f"Mode: {shared_data.vcu.mode}")
        vcu_apps_label.config(text=f"APPS: {shared_data.vcu.apps}%")
        vcu_brake_label.config(text=f"Brake Sensor: {shared_data.vcu.brakeSensor}%")
        ivt_current_label.config(text=f"Current: {shared_data.ivt.current}A")
        ivt_voltage_label.config(text=f"Voltage: {shared_data.ivt.voltage}V")
        ivt_wattage_label.config(text=f"Wattage: {shared_data.ivt.wattage}W")
        inverter_rpm_label.config(text=f"Motor RPM: {shared_data.inverter.motorRPM}")
        inverter_motor_temp_label.config(text=f"Motor Temp: {shared_data.inverter.motorTemperature}°C")
        inverter_igbt_temp_label.config(text=f"IGBT Temp: {shared_data.inverter.igbtTemperature}°C")
        root.after(1000, update_gui)

# Handle Window Close Event
def on_closing():
    global running
    running = False  # Stop all updates
    if serial_port and serial_port.is_open:
        serial_port.close()
        print("Serial port closed.")
    root.quit()
    root.destroy()

# Bind the close event to the main window
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start periodic updates
running = True
if serial_port:
    read_serial_data()
else:
    simulate_serial_data()
update_gui()

# Run the application
root.mainloop()
