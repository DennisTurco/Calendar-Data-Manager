from markdown import markdown
import os
from datetime import datetime, timedelta
from typing import Final
from googleapiclient.discovery import build
import pyperclip

from ConfigKeys import ConfigKeys
import JSONPreferences as js

import traceback
import tempfile

import tkinter
from tkinter import filedialog
import customtkinter as ctk
from CTkScrollableDropdown import *
from CTkXYFrame import *
from CTkMenuBar import *
from CTkMessagebox import *
from tkcalendar import *
from CTkToolTip import *
from CTkTable import *
import CustomSpinbox
from google.oauth2.credentials import Credentials

import webbrowser

DATE_FORMATTER: Final[str] = '%d-%m-%Y %H:%M'
DAY_FORMATTER: Final[str] = "%m/%d/%y" # use this only for calendar picker


# singleton class
class CommonOperations():
    _instance = None

    token_path: str
    credentials: Credentials
    credentials_path: str
    _frames = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(CommonOperations, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # initialize variables only one time
        if not hasattr(self, 'credentials'):  # avoid to re-initialize variables
            self.credentials = None
            self.credentials_path = None
            self.token_path = None
    
    def set_credentials(self, credentials, credentials_path, token_path):
        self.credentials = credentials
        self.credentials_path = credentials_path
        self.token_path = token_path
        js.JSONPreferences.WriteCredentialsToJSON(self.credentials_path, self.token_path)

    def get_credentials(self) -> Credentials:
        return self.credentials
    
    def get_credentials_path(self) -> str:
        return self.credentials_path

    def messagebox_exception(self, error):
        error_message = str(error) + '\n\n' + traceback.format_exc()
        
        # Save the full error details to a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt") as temp_file:
            temp_file.write(error_message)
            
        # Provide a link or an option to view the complete error details externally
        msg = CTkMessagebox(title="Exception Error", message=error, icon="cancel", option_1="Ok", option_2="View Details")

        if msg.get() == "Ok": msg.destroy()
        if msg.get() == "View Details": self.messagebox_exception_error_window(error_message)
           
    def messagebox_exception_error_window(self, error):
        if hasattr(self, "toplevel_window") and self.toplevel_window.winfo_exists():
            self.toplevel_window.focus()  # If window exists, focus it
            return

        self.toplevel_window = ctk.CTkToplevel()
        self.toplevel_window.after(200, lambda: self.toplevel_window.iconbitmap('./imgs/bug.ico')) # i have to delay the icon because it' buggy on windows
        self.toplevel_window.title(f'Exception traceback')

        # Create a grid inside the toplevel window
        self.toplevel_window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically
        self.toplevel_window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
        self.toplevel_window.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally

        # Textbox for displaying the error text
        file_viewer = ctk.CTkTextbox(self.toplevel_window)
        file_viewer.grid(row=0, column=0, columnspan=3, padx=0, pady=(0, 10), sticky="nsew")

        # Button to close the window
        button_close = ctk.CTkButton(self.toplevel_window, text="Close", command=self.toplevel_window.destroy)
        button_close.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")
        
        # Button to copy the error text
        button_copy = ctk.CTkButton(self.toplevel_window, text="Copy Error", command=lambda: self.copy_to_clipboard(file_viewer.get("1.0", tkinter.END).strip()))
        button_copy.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="nsew")

        # Button to report the exception
        button_report = ctk.CTkButton(self.toplevel_window, text="Report Exception", command=lambda: webbrowser.open(ConfigKeys.Keys.get('GITHUB_ISSUES_LINK')))
        button_report.grid(row=1, column=2, padx=5, pady=(0, 10), sticky="nsew")

        # Insert text into the box
        file_viewer.delete(0.0, tkinter.END)
        file_viewer.insert(tkinter.END, str(error))

        self.toplevel_window.attributes("-topmost", False)  # Focus on this window
    
    @staticmethod
    def copy_to_clipboard(error_text: str):
        pyperclip.copy(error_text)  

    @staticmethod
    def change_scaling_event(new_scaling: str):
        if new_scaling == None: return
        new_scaling_float = int(new_scaling) / 100
        ctk.set_widget_scaling(new_scaling_float)
        js.JSONPreferences.WriteTextScalingToJSON(new_scaling)
    
    @staticmethod
    def write_log(log_box, message):
        log_box.insert("0.0", "\n" + str(datetime.now()) + ": " + message)

    @staticmethod
    def check_file_path_errors(log_box, filepath):
        if filepath is None or len(filepath) == 0:
            CommonOperations.write_log(log_box, f"ERROR: file path is missing")
            return True
        
        if not os.path.exists(filepath):
            CommonOperations.write_log(log_box, f"ERROR: file '{filepath}' doesn't found")
            return True
    
    @staticmethod
    def get_file_path(logbox, entry):
        file_path = filedialog.askopenfilename(title="Select file where do you want to save data", filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")))
        entry.delete("0", tkinter.END)
        entry.insert("0", file_path)
        CommonOperations.write_log(logbox, f"file '{file_path}' selected")
        return file_path
    
    @staticmethod
    def get_date(type, toplevel_window, entry_date_from, entry_date_to, log_box, calendar, hours, minutes):
        date = calendar.get_date() # get the date from the calendar
        
        try:
            if hours > 23 or hours < 0 or minutes > 59 or minutes < 0:
                return
        except ValueError:
            return
        
        # Format the datetime object as a string in DATE_FORMATTER
        date = datetime.strptime(date, DAY_FORMATTER)
        full_date = datetime(date.year, date.month, date.day, hours, minutes)
        full_date_str = full_date.strftime(DATE_FORMATTER)
        
        if type == 1:
            CommonOperations.write_log(log_box, "Date Selected From: " + full_date_str)
            entry_date_from.delete("0", tkinter.END)
            entry_date_from.insert("0", full_date_str)
        elif type == 2:
            CommonOperations.write_log(log_box, "Date Selected To: " + full_date_str)
            entry_date_to.delete("0", tkinter.END)
            entry_date_to.insert("0", full_date_str)
        else:
            raise Exception("type option doesn't exists")
        
        toplevel_window.destroy()
    
    @staticmethod
    def date_picker_window(type, toplevel_window, entry_date_from, entry_date_to, log_box):
        if toplevel_window is None or not toplevel_window.winfo_exists():
            toplevel_window = ctk.CTkToplevel() # create window if its None or destroyed
            toplevel_window.after(200, lambda: toplevel_window.iconbitmap('./imgs/calendar.ico')) # i have to delay the icon because it' buggy on windows
            
            calendar = Calendar(toplevel_window)
            calendar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            hours_label = ctk.CTkLabel(toplevel_window, text="hours:")
            hours_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

            minutes_label = ctk.CTkLabel(toplevel_window, text="minutes: ")
            minutes_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            
            spinbox_hours = CustomSpinbox.CustomSpinbox(toplevel_window, width=105, step_size=1, min_value=0, max_value=23)
            spinbox_hours.grid(row=1, column=0, padx=(70, 0), pady=10, sticky="w")
            
            spinbox_minutes = CustomSpinbox.CustomSpinbox(toplevel_window, width=105, step_size=1, min_value=0, max_value=59)
            spinbox_minutes.grid(row=2, column=0, padx=(70, 0), pady=10, sticky="w")
            
            # get current hour
            now = datetime.now()
            current_hour = now.strftime("%H")

            # calculate hour after one hour
            after_one_hour = now + timedelta(hours=1)
            hour_after_one_hour = after_one_hour.strftime("%H")

            if type == 1:
                toplevel_window.title("Date From")
                confirm_button = ctk.CTkButton(toplevel_window, text="Confirm", command=lambda: CommonOperations.get_date(1, toplevel_window, entry_date_from, entry_date_to, log_box, calendar, spinbox_hours.get(), spinbox_minutes.get()))
                # set default hour
                spinbox_hours.set(int(current_hour))
            elif type == 2:
                toplevel_window.title("Date To")
                confirm_button = ctk.CTkButton(toplevel_window, text="Confirm", command=lambda: CommonOperations.get_date(2, toplevel_window, entry_date_from, entry_date_to, log_box, calendar, spinbox_hours.get(), spinbox_minutes.get()))
                # set default hour
                spinbox_hours.set(int(hour_after_one_hour))
            else:
                raise Exception("type option doesn't exists")
            
            confirm_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            
            toplevel_window.attributes("-topmost", True) # focus to this windows
            toplevel_window.resizable(False, False)
        else:
            toplevel_window.focus()  # if window exists focus it
        
        return toplevel_window
    
    @staticmethod
    def get_color_id(colors, color_selected):
        color_index = 0
        
        for idx, color in enumerate(colors.keys()):
            if color == color_selected:
                color_index = idx+1
                break
            
        # check if the color is valid (it is not setted 'No Color Filtering')
        if color_index == 12: # 'No Color Filtering' has index == 12
            color_index = -1
            
        return color_index
    
    @staticmethod
    def get_timezone():
        # read data from json to get path from last session
        timezone = 'UTC' # set default timezone
        listRes = js.JSONPreferences.ReadFromJSON()
        if listRes != None and len(listRes) > 0:
            try: timezone = listRes["TimeZone"]
            except: pass
        return timezone
    
    @staticmethod
    def file_viewer_window(toplevel_window, filepath, log_box):
        
        if CommonOperations.check_file_path_errors(log_box, filepath): return
        
        if toplevel_window is None or not toplevel_window.winfo_exists():
            toplevel_window = ctk.CTkToplevel() # create window if its None or destroyed
            toplevel_window.title(filepath)
            toplevel_window.after(200, lambda: toplevel_window.iconbitmap('./imgs/list.ico')) # i have to delay the icon because it' buggy on windows
            file_viewer = ctk.CTkTextbox(toplevel_window)
            file_viewer.bind("<Key>", lambda e: "break")  # set the textbox readonly
            file_viewer.pack(fill=tkinter.BOTH, expand=True)
            
            #insert text into box
            with open(filepath, 'r', encoding='utf-8') as file:
                file_content = file.read()
                file_viewer.delete(1.0, tkinter.END)
                file_viewer.insert(tkinter.END, file_content)

            toplevel_window.attributes("-topmost", True) # focus to this windows
            CommonOperations.write_log(log_box, f"file '{filepath}' opened")
        else:
            toplevel_window.focus()  # if window exists focus it
        
        return toplevel_window
    
    @staticmethod
    def events_preview_in_table(toplevel_window, filepath, log_box):
        if CommonOperations.check_file_path_errors(log_box, filepath):
            return

        if toplevel_window is None or not toplevel_window.winfo_exists():
            events = []

            with open(filepath, 'r', encoding='utf-8') as file:
                counter = 1
                for line in file:
                    event_details = line.strip().split('|')
                    if len(event_details) > 0:
                        event_details.insert(0, str(counter))
                        events.append(event_details)
                        counter += 1
            
            if len(events) == 0:
                CommonOperations.write_log(log_box, f"file '{filepath}' is empty")
                return
            elif len(events) > 200:
                CommonOperations.write_log(log_box, f"unable to display table preview: the file '{filepath}' is too large.")
                return
            
            toplevel_window = ctk.CTkToplevel()  # create window if it's None or destroyed
            toplevel_window.title(filepath)
            toplevel_window.after(200, lambda: toplevel_window.iconbitmap('./imgs/list.ico'))  # delay the icon

            frame = CTkXYFrame(toplevel_window)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            table = CTkTable(frame, row=len(events), column=len(events[0]), values=events)
            table.pack()

            toplevel_window.attributes("-topmost", True)  # focus to this window
            CommonOperations.write_log(log_box, f"file '{filepath}' opened")
            
        else:
            toplevel_window.focus()  # if window exists, focus it

        return toplevel_window
    
    @staticmethod
    def set_timezone(timezone):
        js.JSONPreferences.WriteTimeZoneToJSON(timezone)
    
    @staticmethod
    def set_color_theme(color_theme: str):
        CommonOperations.change_color_theme(color_theme)
        CTkMessagebox(title="Information", message="The theme color will be updated when the application is restarted")
    
    @staticmethod
    def change_color_theme(color_theme: str):
        if color_theme == None: return
        ctk.set_default_color_theme(color_theme) 
        js.JSONPreferences.WriteColorThemeToJSON(color_theme)

    @staticmethod
    def change_appearance(new_appearance: str):
        if new_appearance == None: return
        ctk.set_appearance_mode(new_appearance)
        js.JSONPreferences.WriteAppearanceToJSON(new_appearance)

    @staticmethod
    def open_info_section_dialog(root, title: str, section_message):
        # Create a dialog window with a CTkTextbox
        dialog = ctk.CTkToplevel(root)
        dialog.title(title)
        dialog.after(200, lambda: dialog.iconbitmap('./imgs/information.ico'))

        CommonOperations.centerWindow(dialog, 420, 400)

        # Make the dialog always stay on top
        dialog.attributes("-topmost", True)

        dialog.resizable(False, False)

        # Add a CTkTextbox for displaying the text
        text_box = ctk.CTkTextbox(dialog, wrap="word")
        text_box.insert("1.0", section_message)  # Insert the preprocessed plain text
        text_box.configure(state="disabled")  # Make the textbox read-only
        text_box.pack(pady=5, padx=10, fill="both", expand=True)

        # Add a close button
        close_button = ctk.CTkButton(dialog, text="Ok", command=dialog.destroy)
        close_button.pack(pady=10)
        
    def get_appearance(self) -> str:
        appearance = ctk.get_appearance_mode()

        if appearance is None or appearance == "":
            listRes = js.JSONPreferences.ReadFromJSON()
            appearance = ""
            if listRes != None and len(listRes) > 0:
                try: 
                    appearance = listRes["Appearence"]
                    CommonOperations.change_appearance(appearance)
                except: pass
        
        return appearance
    
    @staticmethod
    def centerWindow(root, app_width, app_height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x = (screen_width / 2) - (app_width / 2) 
        y = (screen_height / 2) - (app_height / 2) 
        
        root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    
    def set_frames(self, frames):
        self._frames = frames

    def get_frames(self):
        return self._frames