import tkinter as tk
from tkinter import messagebox, font as tkfont
import configparser
import datetime
import os
from PIL import Image, ImageTk
import webbrowser


# --- GLOBAL CONFIGURATION ---
CONFIG_FILE = 'config.ini'
IMAGE_FILE = 'logo.jpg'

class MeasurementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secchi LéXPLORE - GC 2025")
        self.root.geometry("550x700")  # Augmenté pour l'encart de texte

        # --- FONT DEFINITION ---
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.entry_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=11, weight="bold")

        self.fields = ["Date (YYYY-MM-DD)", "Time (UTC HH:MM)", "Lowering Depth (m)", "Raising Depth (m)", "Operator"]
        self.entries = {}
        self.tk_image = None

        self.create_widgets()
        self.create_info_text()  # Ajout de l'encart de texte
        self.check_config()
        self.autofill_datetime()

    def create_widgets(self):
        """Creates and places all the widgets in the window."""
        try:
            pil_image = Image.open(IMAGE_FILE)
            target_width = 400
            original_width, original_height = pil_image.size
            aspect_ratio = original_height / original_width
            target_height = int(target_width * aspect_ratio)
            resized_image = pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized_image)
            image_label = tk.Label(self.root, image=self.tk_image)
            image_label.pack(pady=10)
        except FileNotFoundError:
            error_label = tk.Label(self.root, text=f"Image '{IMAGE_FILE}' not found.", font=self.label_font, fg="red")
            error_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(self.root, text=f"Could not load image: {e}", font=self.label_font, fg="red")
            error_label.pack(pady=10)

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        for field in self.fields:
            frame = tk.Frame(main_frame)
            frame.pack(pady=5, fill='x')
            label = tk.Label(frame, text=field, width=20, anchor='w', font=self.label_font)
            label.pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(frame, font=self.entry_font)
            entry.pack(side=tk.RIGHT, expand=True, fill='x')
            self.entries[field] = entry

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.save_button = tk.Button(
            button_frame, text="Save Measurement", command=self.save_data,
            font=self.button_font, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.autofill_button = tk.Button(
            button_frame, text="Autofill Date/Time", command=self.autofill_datetime,
            font=self.button_font)
        self.autofill_button.pack(side=tk.LEFT, padx=10)

        self.view_button = tk.Button(
            button_frame,
            text="View Latest Secchis",
            command=self.open_measurements_link,
            font=self.button_font,
            bg="#2196F3",
            fg="white"
        )
        self.view_button.pack(side=tk.LEFT, padx=10)

    def create_info_text(self):
        """Creates and displays the configurable info text from config.ini"""
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        # Texte par défaut si non défini dans le config
        default_info = ("Bienvenue dans l'application Secchi LéXPLORE!\n"
                       "N'oubliez pas de vérifier les valeurs avant enregistrement.\n"
                       "Les profondeurs doivent être saisies en mètres.")

        info_text = config['DEFAULT'].get('InfoText', default_info)

        if info_text:
            # Frame pour l'encart avec une bordure
            info_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE, bg='#f0f0f0')
            info_frame.pack(pady=10, padx=20, fill="both")

            # Label avec le texte
            info_label = tk.Label(
                info_frame,
                text=info_text,
                font=self.label_font,
                justify=tk.LEFT,
                wraplength=500,
                padx=10,
                pady=10,
                bg='#f0f0f0'
            )
            info_label.pack(fill="both", expand=True)

    def check_config(self):
        """Checks if config.ini exists and creates it if not with all required fields."""
        if not os.path.exists(CONFIG_FILE):
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                'SavePath': '.',
                'MeasurementID': '1',
                'MeasurementsURL': 'https://www.google.com',
                'InfoText': ('Bienvenue')
            }
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

    def autofill_datetime(self):
        """Fills the date and time fields with the current UTC values."""
        now_utc = datetime.datetime.utcnow()
        self.entries["Date (YYYY-MM-DD)"].delete(0, tk.END)
        self.entries["Date (YYYY-MM-DD)"].insert(0, now_utc.strftime('%Y-%m-%d'))
        self.entries["Time (UTC HH:MM)"].delete(0, tk.END)
        self.entries["Time (UTC HH:MM)"].insert(0, now_utc.strftime('%H:%M'))

    def open_measurements_link(self):
        """Opens the URL specified in the config file in a new browser tab."""
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        url = config['DEFAULT'].get('MeasurementsURL')

        if url and url.strip():
            try:
                webbrowser.open_new_tab(url)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open the link.\nError: {e}")
        else:
            messagebox.showwarning(
                "Not Configured",
                "The web link is not configured in the config.ini file.\n"
                "Please add a 'MeasurementsURL' key to the [DEFAULT] section."
            )

    def save_data(self):
        """Validates input and saves the data to a text file."""
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        save_path = config['DEFAULT'].get('SavePath', '.')
        measurement_id = config['DEFAULT'].getint('MeasurementID', 1)

        date_str = self.entries["Date (YYYY-MM-DD)"].get()
        time_str = self.entries["Time (UTC HH:MM)"].get()
        op_str = self.entries["Operator"].get()
        depth1_str = self.entries["Lowering Depth (m)"].get()
        depth2_str = self.entries["Raising Depth (m)"].get()

        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Format", "The date is not in the correct format.\nPlease use YYYY-MM-DD.")
            return

        try:
            datetime.datetime.strptime(time_str, '%H:%M')
        except ValueError:
            messagebox.showerror("Invalid Format", "The time is not in the correct format.\nPlease use HH:MM.")
            return

        if not all([date_str, time_str, depth1_str, depth2_str, op_str]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            depth1 = float(depth1_str)
            depth2 = float(depth2_str)
            avg_depth = (depth1 + depth2) / 2
        except ValueError:
            messagebox.showerror("Error", "Depths must be valid numbers.")
            return

        filename_time = time_str.replace(":", "-")
        filename = f"{date_str}_{filename_time}_Secchi_LeXPLORE.txt"
        filepath = os.path.join(save_path, filename)

        header = "measurement_id;date;utc_time;lowering_depth;raising_depth;average_depth;operator\n"
        data_line = f"{measurement_id};{date_str};{time_str};{depth1};{depth2};{avg_depth:.2f};{op_str}\n"

        try:
            with open(filepath, 'w') as f:
                f.write(header)
                f.write(data_line)

            messagebox.showinfo("Success", f"Data saved to:\n{filepath}")

            config['DEFAULT']['MeasurementID'] = str(measurement_id + 1)
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

            self.entries["Lowering Depth (m)"].delete(0, tk.END)
            self.entries["Raising Depth (m)"].delete(0, tk.END)
            self.entries["Operator"].delete(0, tk.END)
            self.autofill_datetime()

        except Exception as e:
            messagebox.showerror("File Error", f"Could not save file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MeasurementApp(root)
    root.mainloop()
