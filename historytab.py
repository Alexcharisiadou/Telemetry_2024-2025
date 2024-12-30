from tkinter import Tk, Frame, Label, Listbox, Scrollbar, Entry, Button, END, ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class HistoryTab:
    def __init__(self, notebook, shared_data):
        # Δημιουργία πλαισίου για την καρτέλα ιστορικού
        self.frame = Frame(notebook, bg="lightgray")
        notebook.add(self.frame, text="Data History")
        self.shared_data = shared_data
        self.data_log = []  # Για αποθήκευση του ιστορικού δεδομένων

        # Ετικέτα και πεδίο αναζήτησης
        search_label = Label(self.frame, text="Search by Parameter:", font=("Arial", 12), bg="lightgray")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.search_entry = Entry(self.frame, font=("Arial", 12), width=30)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        search_button = Button(self.frame, text="Search", command=self.search_data)
        search_button.grid(row=0, column=2, padx=10, pady=10)

        # Πλαίσια για κάθε κατηγορία δεδομένων
        self.motor_rpm_frame = Frame(self.frame, bg="lightyellow", highlightbackground="black", highlightthickness=1)
        self.motor_rpm_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        motor_rpm_label = Label(self.motor_rpm_frame, text="Motor RPM", font=("Arial", 14, "bold"), bg="lightyellow")
        motor_rpm_label.pack(anchor="w", padx=10, pady=5)

        self.humidity_frame = Frame(self.frame, bg="lightcyan", highlightbackground="black", highlightthickness=1)
        self.humidity_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        humidity_label = Label(self.humidity_frame, text="Humidity", font=("Arial", 14, "bold"), bg="lightcyan")
        humidity_label.pack(anchor="w", padx=10, pady=5)

        # Λίστα για εμφάνιση ιστορικού δεδομένων
        self.history_list = Listbox(self.motor_rpm_frame, font=("Arial", 12), width=40, height=10)
        self.history_list.pack(padx=10, pady=5, fill="both", expand=True)

        self.humidity_list = Listbox(self.humidity_frame, font=("Arial", 12), width=40, height=10)
        self.humidity_list.pack(padx=10, pady=5, fill="both", expand=True)

        # Προσθήκη διαγράμματος
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.ax.set_title("Parameter Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Αρχική ενημέρωση του διαγράμματος
        self.canvas.draw()

        # Προσαρμογή του πλαισίου για δυναμική αλλαγή μεγέθους
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def add_entry(self, parameter, value):
        """Προσθήκη νέας εγγραφής στο ιστορικό δεδομένων."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{current_time} - {parameter}: {value}"
        self.data_log.append((parameter, current_time, value))

        # Εμφάνιση της εγγραφής στο σωστό πλαίσιο
        if parameter == "Motor RPM":
            self.history_list.insert(END, entry)
            if self.history_list.size() > 50:
                self.history_list.delete(0)  # Κρατάμε μόνο τα τελευταία 50 στοιχεία

        elif parameter == "Humidity":
            self.humidity_list.insert(END, entry)
            if self.humidity_list.size() > 50:
                self.humidity_list.delete(0)  # Κρατάμε μόνο τα τελευταία 50 στοιχεία

        # Ενημέρωση διαγράμματος
        self.update_plot(parameter)

    def update_plot(self, parameter):
        """Ενημερώνει το διάγραμμα με τα τελευταία δεδομένα για το συγκεκριμένο parameter."""
        times = []
        values = []

        # Φιλτράρουμε τα δεδομένα για το επιλεγμένο parameter
        for param, timestamp, value in self.data_log:
            if param == parameter:
                times.append(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S"))
                values.append(float(value))  # Μετατρέπουμε την τιμή σε float για το διάγραμμα

        # Αν υπάρχουν δεδομένα για τον συγκεκριμένο parameter, σχεδιάζουμε το διάγραμμα
        if times and values:
            self.ax.clear()
            self.ax.plot(times, values, marker='o', linestyle='-', color='b')
            self.ax.set_title(f"{parameter} Over Time")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel(parameter)
            self.ax.tick_params(axis='x', rotation=45)  # Περιστροφή του άξονα Χ για καλύτερη ανάγνωση
            self.canvas.draw()

    def search_data(self):
        """Αναζήτηση δεδομένων βάσει του παραμέτρου."""
        search_term = self.search_entry.get().strip().lower()
        self.history_list.delete(0, END)  # Καθαρισμός της λίστας του Motor RPM
        self.humidity_list.delete(0, END)  # Καθαρισμός της λίστας του Humidity

        # Φιλτράρισμα δεδομένων
        for entry in self.data_log:
            parameter, timestamp, value = entry
            display_text = f"{timestamp} - {parameter}: {value}"
            if search_term in parameter.lower():
                if parameter == "Motor RPM":
                    self.history_list.insert(END, display_text)
                elif parameter == "Humidity":
                    self.humidity_list.insert(END, display_text)

        # Ενημέρωση διαγράμματος με τα φιλτραρισμένα δεδομένα
        if search_term:
            self.update_plot(search_term)

# Παράδειγμα χρήσης με Notebook και μετρήσεις
root = Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

shared_data = {}  # Placeholder για δεδομένα
history_tab = HistoryTab(notebook, shared_data)

# Προσθήκη παραδειγμάτων μετρήσεων
history_tab.add_entry("Motor RPM", "1500")
history_tab.add_entry("Humidity", "45")
history_tab.add_entry("Motor RPM", "1600")
history_tab.add_entry("Motor RPM", "1550")
history_tab.add_entry("Humidity", "50")

root.mainloop()
