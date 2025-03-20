from tkinter import Tk, Frame, Label, Listbox, Scrollbar, Entry, Button, END, ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class HistoryTab:
    def __init__(self, notebook, shared_data):
        # Create a frame for the history tab and add it to the notebook
        self.frame = Frame(notebook, bg="lightgray")
        notebook.add(self.frame, text="Data History")
        self.shared_data = shared_data
        self.data_log = []  # List to store history entries

        # Create a search label, entry, and button
        search_label = Label(self.frame, text="Search by Parameter:", font=("Arial", 12), bg="lightgray")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.search_entry = Entry(self.frame, font=("Arial", 12), width=30)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        search_button = Button(self.frame, text="Search", command=self.search_data)
        search_button.grid(row=0, column=2, padx=10, pady=10)

        # Create frames for each category (e.g., Motor RPM and Humidity)
        self.motor_rpm_frame = Frame(self.frame, bg="lightyellow", highlightbackground="black", highlightthickness=1)
        self.motor_rpm_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        motor_rpm_label = Label(self.motor_rpm_frame, text="Motor RPM", font=("Arial", 14, "bold"), bg="lightyellow")
        motor_rpm_label.pack(anchor="w", padx=10, pady=5)

        self.humidity_frame = Frame(self.frame, bg="lightcyan", highlightbackground="black", highlightthickness=1)
        self.humidity_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        humidity_label = Label(self.humidity_frame, text="Humidity", font=("Arial", 14, "bold"), bg="lightcyan")
        humidity_label.pack(anchor="w", padx=10, pady=5)

        # Listboxes for displaying history entries for each category
        self.history_list = Listbox(self.motor_rpm_frame, font=("Arial", 12), width=40, height=10)
        self.history_list.pack(padx=10, pady=5, fill="both", expand=True)

        self.humidity_list = Listbox(self.humidity_frame, font=("Arial", 12), width=40, height=10)
        self.humidity_list.pack(padx=10, pady=5, fill="both", expand=True)

        # Create a matplotlib figure and canvas to show the diagram
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.ax.set_title("Parameter Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.canvas.draw()

        # Make the frame expandable
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def add_entry(self, parameter, value):
        """Add a new entry to the history log."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{current_time} - {parameter}: {value}"
        self.data_log.append((parameter, current_time, value))

        # Display the entry in the appropriate listbox based on the parameter name
        if parameter.lower() == "motor rpm":
            self.history_list.insert(END, entry)
            if self.history_list.size() > 50:
                self.history_list.delete(0)
        elif parameter.lower() == "humidity":
            self.humidity_list.insert(END, entry)
            if self.humidity_list.size() > 50:
                self.humidity_list.delete(0)

        # Optionally update the diagram for this parameter
        self.update_plot(parameter.lower())

    def update_plot(self, search_term):
        """Update the diagram with all entries whose parameter contains the search term."""
        times = []
        values = []
        # Check each log entry for the search term (case-insensitive)
        for param, timestamp, value in self.data_log:
            if search_term in param.lower():
                time_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
                times.append(time_str)
                try:
                    values.append(float(value))
                except ValueError:
                    # Skip non-numeric values
                    pass

        if times and values:
            self.ax.clear()
            self.ax.plot(times, values, marker='o', linestyle='-', color='b')
            self.ax.set_title(f"{search_term.capitalize()} Over Time")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel(search_term.capitalize())
            self.ax.tick_params(axis='x', rotation=45)
            self.canvas.draw()

    def search_data(self):
        """Filter the displayed data and update the diagram based on the search term."""
        search_term = self.search_entry.get().strip().lower()
        # Clear both listboxes
        self.history_list.delete(0, END)
        self.humidity_list.delete(0, END)

        # Filter the data log for entries matching the search term
        for param, timestamp, value in self.data_log:
            display_text = f"{timestamp} - {param}: {value}"
            if search_term in param.lower():
                # Insert in the corresponding listbox based on parameter name
                if param.lower() == "motor rpm":
                    self.history_list.insert(END, display_text)
                elif param.lower() == "humidity":
                    self.humidity_list.insert(END, display_text)
                else:
                    # If the parameter is different, default to the Motor RPM list
                    self.history_list.insert(END, display_text)
        if search_term:
            self.update_plot(search_term)

if __name__ == "__main__":
    # Test/demo code to run this module independently.
    from tkinter import Tk
    root = Tk()
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    shared_data = {}
    history_tab = HistoryTab(notebook, shared_data)
    history_tab.add_entry("Motor RPM", "1500")
    history_tab.add_entry("Humidity", "45")
    history_tab.add_entry("Motor RPM", "1600")
    history_tab.add_entry("Motor RPM", "1550")
    history_tab.add_entry("Humidity", "50")
    root.mainloop()
