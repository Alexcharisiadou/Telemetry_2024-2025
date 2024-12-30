from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import datetime
from historytab import HistoryTab  # Εισάγουμε την κλάση HistoryTab

# Dummy data classes
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
        self.Mode = "OFF"
        self.APPS = 0
        self.BrakeSensor = 0

class IVTData:
    def __init__(self):
        self.current = 0
        self.voltage = 605
        self.wattage = 0

class InverterData:
    def __init__(self):
        self.motorRPM = 23
        self.motorTemperature = 30
        self.igbtTemperature = 35

class SharedData:
    def __init__(self):
        self.acu = ACUData()
        self.vcu = VCUData()
        self.bms = BMSData()
        self.ivt = IVTData()
        self.inverter = InverterData()

shared_data = SharedData()

# Initialize main window
root = ThemedTk(theme="arc")
root.title("Dashboard")
root.geometry("1200x800")

# Create Notebook for tabs
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

# Configure root grid for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create the Dashboard tab
main_frame = Frame(notebook)
notebook.add(main_frame, text="Dashboard")

# Configure the main_frame grid to expand rows and columns evenly
for i in range(4):
    main_frame.grid_rowconfigure(i, weight=1)
for j in range(2):
    main_frame.grid_columnconfigure(j, weight=1)

# Function to create a scrollable frame
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

# Frames for the main dashboard

# Inverter Frame
inverter_frame = Frame(main_frame, bg="lightyellow", highlightbackground="black", highlightthickness=2)
inverter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
inverter_label = Label(inverter_frame, text="Inverter:", fg="blue", bg="lightyellow", font=("Arial", 20, "bold"))
inverter_label.grid(row=0, column=0, padx=10, pady=5)
inverter_rpm_label = Label(inverter_frame, text=f"Motor RPM: {shared_data.inverter.motorRPM}", bg="lightyellow",
                           font=("Arial", 18))
inverter_rpm_label.grid(row=1, column=0, padx=10, pady=5)
motor_temp_label = Label(inverter_frame, text=f"Motor Temp: {shared_data.inverter.motorTemperature}°C",
                         bg="lightyellow", font=("Arial", 18))
motor_temp_label.grid(row=2, column=0, padx=10, pady=5)
igbt_temp_label = Label(inverter_frame, text=f"IGBT Temp: {shared_data.inverter.igbtTemperature}°C", bg="lightyellow",
                        font=("Arial", 18))
igbt_temp_label.grid(row=3, column=0, padx=10, pady=5)

# ACU Flags Frame with scrollable content
acu_flags_frame = Frame(main_frame, bg="lightblue", highlightbackground="black", highlightthickness=2)
acu_flags_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
scrollable_acu = create_scrollable_frame(acu_flags_frame)
acu_flags_label = Label(scrollable_acu, text="ACU Flags:", fg="blue", bg="lightblue", font=("Arial", 20, "bold"))
acu_flags_label.grid(row=0, column=0, padx=10, pady=5)
acu_air_plus_label = Label(scrollable_acu, text=f"Air+: {shared_data.acu.airPlus}", bg="lightblue", font=("Arial", 18))
acu_air_plus_label.grid(row=1, column=0, padx=10, pady=5)
acu_air_minus_label = Label(scrollable_acu, text=f"Air-: {shared_data.acu.airMinus}", bg="lightblue",
                            font=("Arial", 18))
acu_air_minus_label.grid(row=2, column=0, padx=10, pady=5)
acu_pre_relay_label = Label(scrollable_acu, text=f"Pre Relay: {shared_data.acu.preRelay}", bg="lightblue",
                            font=("Arial", 18))
acu_pre_relay_label.grid(row=3, column=0, padx=10, pady=5)
acu_ts_over_60_label = Label(scrollable_acu, text=f"Over 60V: {shared_data.acu.TSOver60}", bg="lightblue",
                             font=("Arial", 18))
acu_ts_over_60_label.grid(row=4, column=0, padx=10, pady=5)
acu_ams_error_label = Label(scrollable_acu, text=f"AMS Error: {shared_data.acu.AMSError}", bg="lightblue",
                            font=("Arial", 18))
acu_ams_error_label.grid(row=5, column=0, padx=10, pady=5)

# ACU Data Frame
acu_data_frame = Frame(main_frame, bg="lightcyan", highlightbackground="black", highlightthickness=2)
acu_data_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
acu_data_label = Label(acu_data_frame, text="ACU Data:", fg="blue", bg="lightcyan", font=("Arial", 20, "bold"))
acu_data_label.grid(row=0, column=0, padx=10, pady=5)
acu_humidity_label = Label(acu_data_frame, text=f"Humidity: {shared_data.acu.humidity}%", bg="lightcyan",
                           font=("Arial", 18))
acu_humidity_label.grid(row=1, column=0, padx=10, pady=5)
acu_temperature_label = Label(acu_data_frame, text=f"Temperature: {shared_data.acu.temperature}°C", bg="lightcyan",
                              font=("Arial", 18))
acu_temperature_label.grid(row=2, column=0, padx=10, pady=5)
acu_imd_resistance_label = Label(acu_data_frame, text=f"IMD Resistance: {shared_data.acu.imdResistance} Ω",
                                 bg="lightcyan", font=("Arial", 18))
acu_imd_resistance_label.grid(row=3, column=0, padx=10, pady=5)
acu_vicor_temp_label = Label(acu_data_frame, text=f"Vicor Temp: {shared_data.acu.vicorTemperature}°C", bg="lightcyan",
                             font=("Arial", 18))
acu_vicor_temp_label.grid(row=4, column=0, padx=10, pady=5)

# BMS Flags Frame
bms_frame = Frame(main_frame, bg="lightgreen", highlightbackground="black", highlightthickness=2)
bms_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
bms_label = Label(bms_frame, text="BMS Flags:", fg="blue", bg="lightgreen", font=("Arial", 20, "bold"))
bms_label.grid(row=0, column=0, padx=10, pady=5)
bms_min_voltage_label = Label(bms_frame, text=f"Min Voltage: {shared_data.bms.minimumCellVoltage} V", bg="lightgreen",
                              font=("Arial", 18))
bms_min_voltage_label.grid(row=1, column=0, padx=10, pady=5)
bms_max_voltage_label = Label(bms_frame, text=f"Max Voltage: {shared_data.bms.maximumCellVoltage} V", bg="lightgreen",
                              font=("Arial", 18))
bms_max_voltage_label.grid(row=2, column=0, padx=10, pady=5)
bms_max_temp_label = Label(bms_frame, text=f"Max Temp: {shared_data.bms.maximumTemperature}°C", bg="lightgreen",
                           font=("Arial", 18))
bms_max_temp_label.grid(row=3, column=0, padx=10, pady=5)

# IVT Data Frame
ivt_frame = Frame(main_frame, bg="lightgray", highlightbackground="black", highlightthickness=2)
ivt_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
ivt_label = Label(ivt_frame, text="IVT Data:", fg="blue", bg="lightgray", font=("Arial", 20, "bold"))
ivt_label.grid(row=0, column=0, padx=10, pady=5)
ivt_voltage_label = Label(ivt_frame, text=f"Voltage: {shared_data.ivt.voltage} V", bg="lightgray", font=("Arial", 18))
ivt_voltage_label.grid(row=1, column=0, padx=10, pady=5)
ivt_current_label = Label(ivt_frame, text=f"Current: {shared_data.ivt.current} A", bg="lightgray", font=("Arial", 18))
ivt_current_label.grid(row=2, column=0, padx=10, pady=5)
ivt_wattage_label = Label(ivt_frame, text=f"Wattage: {shared_data.ivt.wattage} W", bg="lightgray", font=("Arial", 18))
ivt_wattage_label.grid(row=3, column=0, padx=10, pady=5)

# VCU Data Frame
vcu_frame = Frame(main_frame, bg="lightcoral", highlightbackground="black", highlightthickness=2)
vcu_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
vcu_label = Label(vcu_frame, text="VCU Data:", fg="blue", bg="lightcoral", font=("Arial", 20, "bold"))
vcu_label.grid(row=0, column=0, padx=10, pady=5)
vcu_mode_label = Label(vcu_frame, text=f"Mode: {shared_data.vcu.Mode}", bg="lightcoral", font=("Arial", 18))
vcu_mode_label.grid(row=1, column=0, padx=10, pady=5)
vcu_apps_label = Label(vcu_frame, text=f"APPS: {shared_data.vcu.APPS}%", bg="lightcoral", font=("Arial", 18))
vcu_apps_label.grid(row=2, column=0, padx=10, pady=5)
vcu_brake_label = Label(vcu_frame, text=f"Brake Sensor: {shared_data.vcu.BrakeSensor}%", bg="lightcoral",
                        font=("Arial", 18))
vcu_brake_label.grid(row=3, column=0, padx=10, pady=5)

# Data Logger Frame
data_logger_frame = Frame(main_frame, bg="lightpink", highlightbackground="black", highlightthickness=2)
data_logger_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
data_logger_label = Label(data_logger_frame, text="Data Logger:", fg="blue", bg="lightpink", font=("Arial", 20, "bold"))
data_logger_label.grid(row=0, column=0, padx=10, pady=5)

# Δημιουργία της καρτέλας Data History χρησιμοποιώντας την κλάση HistoryTab
history_tab = HistoryTab(notebook, shared_data)

# Function to update data periodically and log to history
def update_values():
    # Update labels with data
    inverter_rpm_label.config(text=f"Motor RPM: {shared_data.inverter.motorRPM}")
    motor_temp_label.config(text=f"Motor Temp: {shared_data.inverter.motorTemperature}°C")
    igbt_temp_label.config(text=f"IGBT Temp: {shared_data.inverter.igbtTemperature}°C")
    acu_air_plus_label.config(text=f"Air+: {shared_data.acu.airPlus}")
    acu_humidity_label.config(text=f"Humidity: {shared_data.acu.humidity}%")
    acu_temperature_label.config(text=f"Temperature: {shared_data.acu.temperature}°C")
    acu_imd_resistance_label.config(text=f"IMD Resistance: {shared_data.acu.imdResistance} Ω")
    acu_vicor_temp_label.config(text=f"Vicor Temp: {shared_data.acu.vicorTemperature}°C")
    bms_min_voltage_label.config(text=f"Min Voltage: {shared_data.bms.minimumCellVoltage} V")
    bms_max_voltage_label.config(text=f"Max Voltage: {shared_data.bms.maximumCellVoltage} V")
    bms_max_temp_label.config(text=f"Max Temp: {shared_data.bms.maximumTemperature}°C")
    ivt_voltage_label.config(text=f"Voltage: {shared_data.ivt.voltage} V")
    ivt_current_label.config(text=f"Current: {shared_data.ivt.current} A")
    ivt_wattage_label.config(text=f"Wattage: {shared_data.ivt.wattage} W")
    vcu_mode_label.config(text=f"Mode: {shared_data.vcu.Mode}")
    vcu_apps_label.config(text=f"APPS: {shared_data.vcu.APPS}%")
    vcu_brake_label.config(text=f"Brake Sensor: {shared_data.vcu.BrakeSensor}%")

    # Log all data to history on the second page
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_tab.add_entry("Motor RPM", shared_data.inverter.motorRPM)
    history_tab.add_entry("Humidity", shared_data.acu.humidity)
    # Add other parameters similarly if needed

    # Schedule the function to run again after 1 second
    root.after(1000, update_values)

# Start updating values periodically
root.after(1000, update_values)

# Start main loop
root.mainloop()
