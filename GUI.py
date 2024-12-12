from ast import List
from datetime import datetime
import glob
from io import BytesIO
import tempfile
from Logger import Logger
import threading
from typing import Final, List
import webbrowser
import os

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import requests
from PIL import Image as pilImage, ImageTk, ImageDraw

from ConfigKeys import ConfigKeys
import JSONPreferences as js
import CalendarEventsManager as gc
import Plotter
from DataEditor import DataCSV
import pandas as pandas
import warnings

import tkinter
from tkinter import filedialog
import customtkinter as ctk
from CTkMenuBar import *
from CTkMessagebox import *
from tkcalendar import *
from CTkToolTip import *
from CTkTable import *
from CTkScrollableDropdown import *
from CTkXYFrame import *

from CommonOperations import CommonOperations
import GUIWidgets
import FrameController

# consts
TIMEZONE: Final[List[str]] = ['Africa/Abidjan', 'Africa/Accra', 'Africa/Algiers', 'Africa/Bissau', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/El_Aaiun', 'Africa/Juba', 'Africa/Khartoum', 'Africa/Lagos', 'Africa/Maputo', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Sao_Tome', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Asuncion', 'America/Atikokan', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Cayenne', 'America/Chicago', 'America/Chihuahua', 'America/Costa_Rica', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Fort_Nelson', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Colombo', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kathmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Riyadh', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ulaanbaatar', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faroe', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Sydney', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'GMT', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Wake', 'Pacific/Wallis', 'UTC']

DATE_FORMATTER: Final[str] = '%d-%m-%Y %H:%M'
DAY_FORMATTER: Final[str] = "%m/%d/%y" # use this only for calendar picker

warnings.filterwarnings("ignore", category=UserWarning, message=".*Given image is not CTkImage.*")
#?###########################################################
class NewEventsFrame(ctk.CTkFrame):
    main_class = None
    toplevel_window = None
    _common = CommonOperations()
    
    def __init__(self, parent, main_class):
        ctk.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # load images
        calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        info_image = tkinter.PhotoImage(file='./imgs/information.png')
        icon = tkinter.PhotoImage(file='./imgs/icon.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        (sidebar_button_1, sidebar_button_2, sidebar_button_3, sidebar_button_4, google_calendar_link, logo_button) = GUIWidgets.create_side_bar_frame(self, plus_image, edit_image, list_image, chart_image, google_image, icon)
        sidebar_button_1.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[NewEventsFrame]))
        sidebar_button_2.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[EditEventsFrame]))
        sidebar_button_3.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GetEventsFrame]))
        sidebar_button_4.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GraphFrame]))
        logo_button.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[MainFrame]))
        google_calendar_link.configure(command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
        
        # create main panel
        section_message = '''The Create New Event section allows you to quickly add events to your Google Calendar with customized details. Here's how to use it:

• Event Information:
    - Summary: (Required) Enter a brief title or name for your event.
    - Description: (Optional) Add more details to describe the event. This can be helpful for further context, such as the agenda or any notes.
    - Color: (Required) Choose a color to visually categorize your event for easy identification on your calendar.
• Date Interval:
    - From: (Optional) Set the starting date and time for the event.
    - To: (Optional) Set the ending date and time for the event.
    - Timezone: (Optional) Select the timezone in which the event will occur (default is UTC).

Once you've filled in the event details, simply click Create to add the event to your calendar. This tool makes it easy to create events quickly and organize your calendar effectively.
'''

        # create main panel
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
        title_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(title_frame, text="Create New Event", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=0, sticky="e")
        ctk.CTkButton(title_frame, text="", width=10, image=info_image,  fg_color="transparent", command=lambda: CommonOperations.open_info_section_dialog(self, "Edit Events", section_message)).grid(row=0, column=1, padx=5, pady=0, sticky="w")
        
        # main entry
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Event Information")
        self.main_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_summary = ctk.CTkLabel(self.main_frame, text="Summary:")
        self.label_summary.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_summary = ctk.CTkEntry(self.main_frame, placeholder_text="summary")
        self.entry_summary.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        self.label_description = ctk.CTkLabel(self.main_frame, text="Description:")
        self.label_description.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_description = ctk.CTkTextbox(self.main_frame, width=250, height=100)
        self.entry_description.grid(row=1, column=1, padx=(0, 0), pady=(10, 0), sticky="ew")
        self.label_color = ctk.CTkLabel(self.main_frame, text="Color:")
        self.label_color.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")
        self.multi_selection = ctk.CTkComboBox(self.main_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection, values=list(ConfigKeys.Keys.EVENT_COLOR.value.keys()), button_color="transparent", command=self.combobox_callback)
        self.multi_selection.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get("Light Blue"))
        self.multi_selection.set("Light Blue")
        self.multi_selection.grid(row=2, column=1, padx=0, pady=(10, 10), sticky="w")        

        # date
        (self.entry_date_from, self.entry_date_to, self.timezone_selection, self.entry_date_button, self.entry_date_button2) = GUIWidgets.create_date_interval_scroll_frame(self, calendar_image, TIMEZONE)
        self.entry_date_button.configure(command=lambda: self.date_picker(1))
        self.entry_date_button2.configure(command=lambda: self.date_picker(2))
        
        # create button
        self.create_button = ctk.CTkButton(self, image=plus_image, text="Create", border_width=2, command=self.create_event)
        self.create_button.grid(row=3, column=1, padx=20, pady=20)
        
        # Tooltips
        CTkToolTip(self.entry_summary, delay=0.3, message="(Required) Insert event title")
        CTkToolTip(self.entry_description, delay=0.3, message="(Optional) Insert event description")
        CTkToolTip(self.multi_selection, delay=0.3, message="(Required) Choose event color")
        CTkToolTip(self.entry_date_from, delay=0.3, message="(Optional) Enter date from")
        CTkToolTip(self.entry_date_to, delay=0.3, message="(Optional) Enter date to")
        CTkToolTip(self.timezone_selection, delay=0.3, message="(Optional) Choose time zone")
        CTkToolTip(self.create_button, delay=0.3, message="Create new event")
        
        # create log textbox
        self.log_box = ctk.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=4, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def create_event(self):
        Logger.write_log("Creating event", Logger.LogType.INFO)
        summary = self.entry_summary.get()
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        time_zone = self.timezone_selection.get()
        
        # update preferred TimeZone
        self._common.set_timezone(time_zone)
        
        if len(summary.replace(" ", "")) == 0:
            Logger.write_log(f"Error on creating event: summary is missing", Logger.LogType.WARN)
            self._common.write_log(self.log_box, f"Error on creating event: summary is missing")
            return
        if len(date_from.replace(" ", "")) == 0 or len(date_to.replace(" ", "")) == 0:
            Logger.write_log(f"Error on creating event: date is missing", Logger.LogType.WARN)
            self._common.write_log(self.log_box, f"Error on creating event: date is missing")
            return
        try:
            date_from = datetime.strptime(date_from, DATE_FORMATTER)
            date_to = datetime.strptime(date_to, DATE_FORMATTER)
        except ValueError as error:
            Logger.write_log(f"Error on creating event: date format is not correct", Logger.LogType.ERROR, error)
            self._common.write_log(self.log_box, f"Error on creating event: date format is not correct")
            return
        
        # get color index
        color_index = self._common.get_color_id(ConfigKeys.Keys.EVENT_COLOR.value, self.multi_selection.get())
        
        try: 
            gc.CalendarEventsManager.createEvent(self._common.get_credentials(), summary, self.entry_description.get("0.0", tkinter.END), date_from, date_to, color_index, timeZone=time_zone)
            Logger.write_log(f"Event '{summary}' created succesfully!", Logger.LogType.INFO)
            self._common.write_log(self.log_box, f"Event '{summary}' created succesfully!")
        except FileNotFoundError as file_not_found_error:
            self._common.messagebox_exception(file_not_found_error)
            Logger.write_log(f"File not found error: {str(file_not_found_error)}", Logger.LogType.ERROR, file_not_found_error)
            self._common.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            self._common.messagebox_exception(permission_error)
            Logger.write_log(f"Permission error: {str(permission_error)}", Logger.LogType.ERROR, permission_error)
            self._common.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except HttpError as http_error:
            self._common.messagebox_exception(http_error)
            Logger.write_log(f"HTTP error: {str(http_error)}", Logger.LogType.ERROR, http_error)
            self._common.write_log(self.log_box, f"HTTP error: {str(http_error)}")
        except Exception as error:
            self._common.messagebox_exception(error)
            Logger.write_log(f"Generic error: {str(error)}", Logger.LogType.ERROR, error)
            self._common.write_log(self.log_box, f"Generic error: {str(error)}")   
        
    def combobox_callback(self, color):
        self.multi_selection.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get(color))
        self.multi_selection.set(color)
        Logger.write_log(f"color '{color}' selected", Logger.LogType.INFO)
        self._common.write_log(self.log_box, f"color '{color}' selected")
    
    def date_picker(self, type):
        self.toplevel_window = self._common.date_picker_window(type, self.toplevel_window, self.entry_date_from, self.entry_date_to, self.log_box)
#?###########################################################

#?###########################################################
class EditEventsFrame(ctk.CTkFrame):
    main_class = None
    _common = CommonOperations()
    toplevel_window: ctk.CTkToplevel = None
    date_picker_window = None
    event_color_from = ConfigKeys.Keys.EVENT_COLOR.value
    event_color_to = ConfigKeys.Keys.EVENT_COLOR.value
    
    def __init__(self, parent, main_class):
        ctk.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        self.event_color_from["No Color Filtering"] = "" # adding a new element inside the dictionary
        
        # load images
        calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        arrow_image = tkinter.PhotoImage(file='./imgs/arrow-right2.png')
        info_image = tkinter.PhotoImage(file='./imgs/information.png')
        icon = tkinter.PhotoImage(file='./imgs/icon.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 4), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        (sidebar_button_1, sidebar_button_2, sidebar_button_3, sidebar_button_4, google_calendar_link, logo_button) = GUIWidgets.create_side_bar_frame(self, plus_image, edit_image, list_image, chart_image, google_image, icon)
        sidebar_button_1.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[NewEventsFrame]))
        sidebar_button_2.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[EditEventsFrame]))
        sidebar_button_3.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GetEventsFrame]))
        sidebar_button_4.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GraphFrame]))
        logo_button.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[MainFrame]))
        google_calendar_link.configure(command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))

        section_message = '''This section of the Calendar Data Manager enables you to update multiple events in your Google Calendar simultaneously, saving you time and effort. Here's how it works:

• Filter Existing Events: Use fields such as Summary, Description, Color, and a Date Interval to select the events you want to edit. You can refine your search by combining these criteria.
• Apply New Values: Define the updates you want to make, such as changing the summary, description, or event color.
• Edit with Precision: Specify the date range and timezone to ensure that only the desired events within that period are modified.

Once you've set your filters and new values, click the Edit button to apply the changes instantly across all matching events. This tool ensures a seamless way to manage your calendar efficiently.'''

        # create main panel
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
        title_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(title_frame, text="Edit Events", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=0, sticky="e")
        ctk.CTkButton(title_frame, text="", width=10, image=info_image,  fg_color="transparent", command=lambda: CommonOperations.open_info_section_dialog(self, "Edit Events", section_message)).grid(row=0, column=1, padx=5, pady=0, sticky="w")

        # Create a frame with a 1x2 grid
        main_frame = ctk.CTkScrollableFrame(self, label_text="Event Information")
        main_frame.grid(row=1, column=1, padx=50, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # old main values
        self.old_values_frame = ctk.CTkFrame(main_frame)
        self.old_values_frame.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        self.old_values_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_frame_old = ctk.CTkLabel(self.old_values_frame, text="OLD Values")
        self.label_frame_old.grid(row=0, column=0, columnspan=3, padx=0, pady=0, sticky="ew")
        self.label_summary_old = ctk.CTkLabel(self.old_values_frame, text="Summary:")
        self.label_summary_old.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_summary_old = ctk.CTkEntry(self.old_values_frame, placeholder_text="summary")
        self.entry_summary_old.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=5, sticky="w")
        self.label_description_old = ctk.CTkLabel(self.old_values_frame, text="Description:")
        self.label_description_old.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_description_old = ctk.CTkTextbox(self.old_values_frame, width=250, height=100)
        self.entry_description_old.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="ew")
        self.label_color_old = ctk.CTkLabel(self.old_values_frame, text="Color:")
        self.label_color_old.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.multi_selection_old = ctk.CTkComboBox(self.old_values_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection_old, values=list(self.event_color_from.keys()), button_color="transparent", command=self.combobox_callback_color1)
        self.multi_selection_old.configure(button_color=self.event_color_from.get("No Color Filtering"))
        self.multi_selection_old.set("No Color Filtering")
        self.multi_selection_old.grid(row=3, column=1, padx=0, pady=5, sticky="w")
        
        # Centered img label
        ctk.CTkLabel(main_frame, text="", image=arrow_image).grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        
        # new main values
        self.new_values_frame = ctk.CTkFrame(main_frame)
        self.new_values_frame.grid(row=1, column=2, padx=25, pady=10, sticky="ew")
        self.new_values_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_frame_new = ctk.CTkLabel(self.new_values_frame, text="NEW Values")
        self.label_frame_new.grid(row=0, column=0, columnspan=3, padx=0, pady=0, sticky="ew")
        self.label_summary_new = ctk.CTkLabel(self.new_values_frame, text="Summary:")
        self.label_summary_new.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_summary_new = ctk.CTkEntry(self.new_values_frame, placeholder_text="summary")
        self.entry_summary_new.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=5, sticky="w")
        self.label_description_new = ctk.CTkLabel(self.new_values_frame, text="Description:")
        self.label_description_new.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_description_new = ctk.CTkTextbox(self.new_values_frame, width=250, height=100)
        self.entry_description_new.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="ew")
        self.label_color_new = ctk.CTkLabel(self.new_values_frame, text="Color:")
        self.label_color_new.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.multi_selection_new = ctk.CTkComboBox(self.new_values_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection_new, values=list(ConfigKeys.Keys.EVENT_COLOR.value.keys()), button_color="transparent", command=self.combobox_callback_color2)
        self.multi_selection_new.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get("Light Blue"))
        self.multi_selection_new.set("Light Blue")
        self.multi_selection_new.grid(row=3, column=1, padx=0, pady=5, sticky="w")
        
        # date
        (self.entry_date_from, self.entry_date_to, self.timezone_selection, self.entry_date_button, self.entry_date_button2) = GUIWidgets.create_date_interval_scroll_frame(self, calendar_image, TIMEZONE)
        self.entry_date_button.configure(command=lambda: self.date_picker(1))
        self.entry_date_button2.configure(command=lambda: self.date_picker(2))
        
        # edit button
        self.edit_button = ctk.CTkButton(self, image=edit_image, text="Edit", border_width=2, command=self.edit_events)
        self.edit_button.grid(row=3, column=1, columnspan=2, padx=20, pady=20)
        
        # Tooltips
        CTkToolTip(self.entry_summary_old, delay=0.3, message="(Required) Insert OLD event title")
        CTkToolTip(self.entry_description_old, delay=0.3, message="(Optional) Insert the OLD event description")
        CTkToolTip(self.multi_selection_old, delay=0.3, message="(Optional) Choose OLD event color")
        CTkToolTip(self.entry_summary_new, delay=0.3, message="(Required) Insert NEW event title")
        CTkToolTip(self.entry_description_new, delay=0.3, message="(Optional/Required) Insert NEW event description;\n If the old description is set, this field will not be ignored.")
        CTkToolTip(self.multi_selection_new, delay=0.3, message="(Required) Choose NEW event color")
        CTkToolTip(self.entry_date_from, delay=0.3, message="(Optional) Enter date from")
        CTkToolTip(self.entry_date_to, delay=0.3, message="(Optional) Enter date to")
        CTkToolTip(self.timezone_selection, delay=0.3, message="(Optional) Choose time zone")
        CTkToolTip(self.edit_button, delay=0.3, message="Edit events")
        
        # create log textbox
        self.log_box = ctk.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=4, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def date_picker(self, type):
        self.date_picker_window = CommonOperations.date_picker_window(type, self.date_picker_window, self.entry_date_from, self.entry_date_to, self.log_box)
    
    def edit_events(self):
        Logger.write_log("Editing events", Logger.LogType.INFO)

        # Get OLD values
        summary_old = self.entry_summary_old.get()
        description_old = self.entry_description_old.get('0.0', tkinter.END)
        color_index_old = CommonOperations.get_color_id(self.event_color_from, self.multi_selection_old.get())  # Get color index for old events
        
        # Get NEW values
        summary_new = self.entry_summary_new.get()
        description_new = self.entry_description_new.get('0.0', tkinter.END)
        color_index_new = CommonOperations.get_color_id(self.event_color_to, self.multi_selection_new.get())  # Get color index for new events
        
        # Validate input data
        if not summary_old:
            Logger.write_log("ERROR: Missing old summary", Logger.LogType.WARN)
            CommonOperations.write_log(self.log_box, "ERROR: Missing old summary")
            return
        if not summary_new:
            Logger.write_log("ERROR: Missing new summary", Logger.LogType.WARN)
            CommonOperations.write_log(self.log_box, "ERROR: Missing new summary")
            return
        
        # Get date range
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        
        try:
            # Parse dates if provided
            if date_from:
                date_from = datetime.strptime(date_from, DATE_FORMATTER)
            if date_to:
                date_to = datetime.strptime(date_to, DATE_FORMATTER)
        except ValueError:
            Logger.write_log("ERROR: Invalid date format", Logger.LogType.ERROR)
            CommonOperations.write_log(self.log_box, "ERROR: Invalid date format")
            return
        
        # Get timezone
        time_zone = self.timezone_selection.get()
        
        # Update preferred timezone
        CommonOperations.set_timezone(time_zone)

        try:
            # Retrieve events to edit
            old_events = gc.CalendarEventsManager.getEvents(
                self._common.get_credentials(),
                title=summary_old,
                description=description_old,
                start_date=date_from,
                end_date=date_to,
                time_zone=time_zone,
                color_id=color_index_old
            )
            
            if not old_events:
                Logger.write_log("No events found", Logger.LogType.INFO)
                CommonOperations.write_log(self.log_box, "No events found")
            else:
                # Simulate event updates without applying them
                new_events = gc.CalendarEventsManager.simulateEventUpdates(
                    self._common.get_credentials(),
                    old_events,
                    summary_new,
                    description_new,
                    color_index_new,
                    date_from,
                    date_to,
                    time_zone
                )
                # Show the list of old and new events for comparison
                self.events_list_viewer_window(old_events, new_events, summary_new, description_new, color_index_new, date_from, date_to, time_zone)
        
        # Handle various exceptions
        except FileNotFoundError as e:
            self._common.messagebox_exception(e)
            Logger.write_log(f"File not found error: {str(e)}", Logger.LogType.ERROR, e)
            CommonOperations.write_log(self.log_box, f"File not found error: {str(e)}")
        except PermissionError as e:
            self._common.messagebox_exception(e)
            Logger.write_log(f"Permission error: {str(e)}", Logger.LogType.ERROR, e)
            CommonOperations.write_log(self.log_box, f"Permission error: {str(e)}")
        except ValueError as e:
            self._common.messagebox_exception(e)
            Logger.write_log(f"Value error: {str(e)}", Logger.LogType.ERROR, e)
            CommonOperations.write_log(self.log_box, f"Value error: {str(e)}")
        except Exception as e:
            self._common.messagebox_exception(e)
            Logger.write_log(f"Generic error: {str(e)}", Logger.LogType.ERROR, e)
            CommonOperations.write_log(self.log_box, f"Generic error: {str(e)}")       
    
    def combobox_callback_color1(self, color):
        self.multi_selection_old.configure(button_color=self.event_color_from.get(color))
        self.multi_selection_old.set(color)
        Logger.write_log(f"Old color '{color}' selected", Logger.LogType.INFO)
        CommonOperations.write_log(self.log_box, f"color '{color}' selected")

    def combobox_callback_color2(self, color):
        self.multi_selection_new.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get(color))
        self.multi_selection_new.set(color)
        Logger.write_log(f"New color '{color}' selected", Logger.LogType.INFO)
        CommonOperations.write_log(self.log_box, f"color '{color}' selected")
        
    def update_events(self, old_events: dict, summary_new: str, description_new: str, color_index_new, date_from: str, date_to: str, time_zone: str):
        # Apply updates to the events
        msg = CTkMessagebox(title="Edit events", message=f"Are you sure you want to confirm the changes?\n{len(old_events)} events will be changed.", icon="question", option_1="No", option_2="Yes")
        if msg.get() == "Yes":
            Logger.write_log(f"Old events edited: {old_events}", Logger.LogType.INFO)

            updated_events = gc.CalendarEventsManager.editEvent(
                self._common.get_credentials(),
                old_events,
                summary_new,
                description_new,
                color_index_new,
                date_from,
                date_to,
                time_zone
            )
            if updated_events is None: return
            
            Logger.write_log(f"{len(updated_events)} event(s) successfully updated!", Logger.LogType.INFO)
            CommonOperations.write_log(self.log_box, f"{len(updated_events)} event(s) successfully updated!")
            self.close_top_frame_window()
    
    def close_top_frame_window(self):
        self.toplevel_window.destroy()    
    
    def events_list_viewer_window(self, old_events: dict, new_events: dict, summary_new: str, description_new: str, color_index_new, date_from, date_to, time_zone):
        Logger.write_log("Events list viewer", Logger.LogType.INFO)
        
        # Create a new window if it doesn't exist
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel()
            self.toplevel_window.after(200, lambda: self.toplevel_window.iconbitmap('./imgs/list.ico')) # i have to delay the icon because it' buggy on windows
            self.toplevel_window.title(f'{len(old_events)} Event(s) Found')

            # Configure grid layout
            self.toplevel_window.grid_rowconfigure(0, weight=1)
            self.toplevel_window.grid_columnconfigure(0, weight=1)
            self.toplevel_window.grid_columnconfigure(1, weight=1)

            # Scrollable frame for events display
            event_frame = ctk.CTkFrame(self.toplevel_window)
            event_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

            # Buttons for updating or canceling the event changes
            button_update = ctk.CTkButton(self.toplevel_window, text="Update Results", command=lambda: self.update_events(old_events, summary_new, description_new, color_index_new, date_from, date_to, time_zone))
            button_update.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")

            button_cancel = ctk.CTkButton(self.toplevel_window, text="Cancel", command=self.close_top_frame_window)
            button_cancel.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="nsew")

            # Extract and display old and new event details with colors
            old_events_info = self.extract_event_info(old_events)
            new_events_info = self.extract_event_info(new_events)

            # Display old events in red and new events in green with reduced spacing
            for i in range(len(old_events_info)):
                old_event_str = f"- INDEX: {old_events_info[i]['index']} | ID: {old_events_info[i]['ID']} | SUMMARY: {old_events_info[i]['summary']} | START: {old_events_info[i]['start']} | END: {old_events_info[i]['end']} | DURATION: {old_events_info[i]['duration']}"
                new_event_str = f"+ INDEX: {new_events_info[i]['index']} | ID: {new_events_info[i]['ID']} | SUMMARY: {new_events_info[i]['summary']} | START: {new_events_info[i]['start']} | END: {new_events_info[i]['end']} | DURATION: {new_events_info[i]['duration']}\n"

                # Old event in red with reduced row height (smaller font)
                old_event_label = ctk.CTkLabel(event_frame, text=old_event_str, text_color="red", anchor="w")
                old_event_label.grid(row=i*2, column=0, sticky="w", padx=0, pady=0)

                # New event in green with reduced row height (smaller font)
                new_event_label = ctk.CTkLabel(event_frame, text=new_event_str, text_color="green", anchor="w")
                new_event_label.grid(row=i*2 + 1, column=0, sticky="w", padx=0, pady=0)

            # Bring the window to the front
            self.toplevel_window.attributes("-topmost", True)
            CommonOperations.centerTopLevel(self.toplevel_window)
        else:
            self.toplevel_window.focus()  # Focus the window if it already exists

    def extract_event_info(self, events: dict):
        # Extract relevant event information for display
        event_info_list = []
        for index, event in enumerate(events, start=1):
            try:
                start_date = event['start']['dateTime']
                end_date = event['end']['dateTime']
            except KeyError:
                start_date = event['start']['date']
                end_date = event['end']['date']

            start_datetime = datetime.fromisoformat(start_date)
            end_datetime = datetime.fromisoformat(end_date)
            duration = end_datetime - start_datetime

            event_info = {
                'index': index,
                'ID': event['id'],
                'summary': event['summary'],
                'start': start_date,
                'end': end_date,
                'duration': duration
            }
            event_info_list.append(event_info)

        return event_info_list
    
    
#?###########################################################

#?###########################################################
class GetEventsFrame(ctk.CTkFrame):
    main_class = None
    toplevel_window = None
    toplevel_entry_window = None
    date_picker_window = None
    file_viewer_window = None
    events_preview_in_table = None
    data = None
    events = None
    _common = CommonOperations()
    event_color = ConfigKeys.Keys.EVENT_COLOR.value

    def __init__(self, parent, main_class):
        ctk.CTkFrame.__init__(self, parent)
        self.main_class = main_class

        self.event_color["No Color Filtering"] = ""
        
        # load images
        calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        self.folder_image = tkinter.PhotoImage(file='./imgs/folder.png')
        file_image = tkinter.PhotoImage(file='./imgs/file.png')
        table_image = tkinter.PhotoImage(file='./imgs/table.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        info_image = tkinter.PhotoImage(file='./imgs/information.png')
        icon = tkinter.PhotoImage(file='./imgs/icon.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # create sidebar frame with widgets
        (sidebar_button_1, sidebar_button_2, sidebar_button_3, sidebar_button_4, google_calendar_link, logo_button) = GUIWidgets.create_side_bar_frame(self, plus_image, edit_image, list_image, chart_image, google_image, icon)
        sidebar_button_1.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[NewEventsFrame]))
        sidebar_button_2.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[EditEventsFrame]))
        sidebar_button_3.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GetEventsFrame]))
        sidebar_button_4.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GraphFrame]))
        logo_button.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[MainFrame]))
        google_calendar_link.configure(command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
        
        section_message = '''This section of the Calendar Data Manager allows you to efficiently retrieve and analyze your Google Calendar events. Here's what you can do:

• Filter by Date Interval: Specify a time range to narrow down the events you want to retrieve. You can set the start and end dates, along with the timezone, for precise filtering.
• Save Results: Export the retrieved events list to a file in `.csv` or `.txt` format for further analysis or sharing. You can choose the file location, name, and whether to overwrite an existing file.
• Preview Results or Visualize Data: Quickly preview the events in a table or generate graphs directly from the exported file. This feature enables you to gain insights and statistics about your calendar activities.

Once you've configured your filters, click Get to retrieve the data or Get and Plot to visualize it right away!
        '''

        # create main panel
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
        title_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(title_frame, text="Get Events List", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=0, sticky="e")
        ctk.CTkButton(title_frame, text="", width=10, image=info_image,  fg_color="transparent", command=lambda: CommonOperations.open_info_section_dialog(self, "Get Events List", section_message)).grid(row=0, column=1, padx=5, pady=0, sticky="w")

        # create a container frame for the two scrollable frames
        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="nsew") 
        self.container_frame.grid_columnconfigure((0, 1), weight=1)  # 2 Columns for main_frame and date_frame

        # Column 1: main_frame (Event Information)
        self.main_frame = ctk.CTkScrollableFrame(self.container_frame, label_text="Event Information")
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)  # Setup columns for fields
        self.label_id = ctk.CTkLabel(self.main_frame, text="ID:")
        self.label_id.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_id = ctk.CTkEntry(self.main_frame, placeholder_text="id")
        self.entry_id.grid(row=0, column=1, padx=(10, 10), pady=5, sticky="w")
        self.label_summary = ctk.CTkLabel(self.main_frame, text="Summary:")
        self.label_summary.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_summary = ctk.CTkEntry(self.main_frame, placeholder_text="summary")
        self.entry_summary.grid(row=1, column=1, padx=(10, 10), pady=5, sticky="w")
        self.label_description = ctk.CTkLabel(self.main_frame, text="Description:")
        self.label_description.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_description = ctk.CTkTextbox(self.main_frame, width=150, height=100)
        self.entry_description.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="ew")
        self.label_color = ctk.CTkLabel(self.main_frame, text="Color:")
        self.label_color.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.multi_selection = ctk.CTkComboBox(self.main_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection, values=list(self.event_color.keys()), button_color="transparent", command=self.combobox_callback)
        self.multi_selection.configure(button_color=self.event_color.get("No Color Filtering"))
        self.multi_selection.set("No Color Filtering")
        self.multi_selection.grid(row=3, column=1, padx=0, pady=5, sticky="w")
        
        # Column 2: date_frame (Date Interval)
        (self.entry_date_from, self.entry_date_to, self.entry_date_button, self.label_date_to, self.entry_date_button2, self.timezone_selection) = GUIWidgets.create_date_selection_for_events_list_scroll_frame(self.container_frame, TIMEZONE, calendar_image)
        self.entry_date_button.configure(command=lambda: self.date_picker(1))
        self.entry_date_button2.configure(command=lambda: self.date_picker(2))

        # file output
        (self.file_path, self.overwrite_mode, self.button_file_path, self.button_open_file, self.button_open_events_table_preview) = GUIWidgets.create_file_output_scroll_frame_for_events_list_frame(self, self.folder_image, file_image, table_image)
        self.button_file_path.configure(command=lambda: self.get_file_path(self.file_path))
        self.button_open_file.configure(command=self.open_file)
        self.button_open_events_table_preview.configure(command=self.events_table_preview)

        # create a container frame for the buttons
        self.container_frame2 = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame2.grid(row=4, column=1, padx=(50, 50), pady=10, sticky="nsew") 
        self.container_frame2.grid_columnconfigure((0, 1), weight=1)  # 2 Columns for main_frame and date_frame

        # get list button
        self.get_button = ctk.CTkButton(self.container_frame2, image=list_image, text="Get", border_width=2, command=self.get_and_preview)
        self.get_button.grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.get_and_plot_button = ctk.CTkButton(self.container_frame2, image=chart_image, text="Get and plot", border_width=2, command=self.get_and_plot)
        self.get_and_plot_button.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        # Tooltips
        CTkToolTip(self.entry_id, delay=0.3, message="(Optional) Enter event id This is a very specific field;\n if you want to get a specific event and you know the specific event id, you can enter it and ignore the fields below.\n Otherwise you can ignore it and proceed to fill in the other fields.")
        CTkToolTip(self.entry_summary, delay=0.3, message="(Optional) Insert event title")
        CTkToolTip(self.entry_description, delay=0.3, message="(Optional) Insert the event description")
        CTkToolTip(self.multi_selection, delay=0.3, message="(Optional) Choose event color")
        CTkToolTip(self.entry_date_from, delay=0.3, message="(Optional) Enter date from")
        CTkToolTip(self.entry_date_to, delay=0.3, message="(Optional) Enter date to")
        CTkToolTip(self.timezone_selection, delay=0.3, message="(Optional) Choose time zone")
        CTkToolTip(self.file_path, delay=0.3, message="(Optional) Enter the path to the file;\n if you want to save the results to a specific file (.csv, .txt)")
        CTkToolTip(self.overwrite_mode, delay=0.3, message="If it is enabled, it overwrites the contents of the file with the newly obtained events.\n Otherwise, it adds the newly obtained events without deleting anything.")
        CTkToolTip(self.button_open_file, delay=0.3, message="Open file preview")
        CTkToolTip(self.button_open_events_table_preview, delay=0.3, message="Open file preview in table")
        CTkToolTip(self.get_button, delay=0.3, message="Get and save events.")
        CTkToolTip(self.get_and_plot_button, delay=0.3, message="Get and plot events without saving to a file.")
        
        # create log textbox
        self.log_box = ctk.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=5, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")

        self.cleanup_temp_files()

    # returns the number of events obtained
    def get_events(self):
        self.events = None
        
        id = self.entry_id.get()
        if len(id) != 0:
            try: 
                self.events = gc.CalendarEventsManager.getEventByID(self._common.get_credentials(), id)
                #self.events_list_viewer_window()
                Logger.write_log(f"Event obtained succesfully!", Logger.LogType.INFO)
                self._common.write_log(self.log_box, f"Event obtained succesfully!")
                return
            except FileNotFoundError as file_not_found_error:
                self._common.messagebox_exception(file_not_found_error)
                Logger.write_log(f"File not found error: {str(file_not_found_error)}", Logger.LogType.ERROR, file_not_found_error)
                self._common.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
            except PermissionError as permission_error:
                self._common.messagebox_exception(permission_error)
                Logger.write_log(f"Permission error: {str(permission_error)}", Logger.LogType.ERROR, permission_error)
                self._common.write_log(self.log_box, f"Permission error: {str(permission_error)}")
            except ValueError as value_error:
                self._common.messagebox_exception(value_error)
                Logger.write_log(f"Value error: {str(value_error)}", Logger.LogType.ERROR, value_error)
                self._common.write_log(self.log_box, f"Value error: {str(value_error)}")
            except Exception as error:
                self._common.messagebox_exception(error)
                Logger.write_log(f"Generic error: {str(error)}", Logger.LogType.ERROR, error)
                self._common.write_log(self.log_box, f"Generic error: {str(error)}")
        
        summary = self.entry_summary.get()
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        description = self.entry_description.get("0.0", tkinter.END).replace('\n', '')
        time_zone = self.timezone_selection.get()
        
        # update preferred TimeZone
        self._common.set_timezone(time_zone)
         
        try:
            if len(date_from) != 0:
                date_from = datetime.strptime(date_from, DATE_FORMATTER)
            if len(date_to) != 0:
                date_to = datetime.strptime(date_to, DATE_FORMATTER)
        except ValueError as error:
            Logger.write_log(f"Error on creating event: date format is not correct", Logger.LogType.ERROR, error)
            self._common.write_log(self.log_box, f"Error on creating event: date format is not correct")
            return
        
        # get color index
        color_index = self._common.get_color_id(ConfigKeys.Keys.EVENT_COLOR.value, self.multi_selection.get())
        
        try: 
            self.events = gc.CalendarEventsManager.getEvents(creds=self._common.get_credentials(), title=summary, start_date=date_from, end_date=date_to, color_id=color_index, description=description, time_zone=time_zone)
            if self.events == None or len(self.events) == 0:
                Logger.write_log(f"No events obtained", Logger.LogType.INFO)
                self._common.write_log(self.log_box, f"No events obtained")
                return 0
            
            #self.events_list_viewer_window() # i have to truncate the list for performances reason
            Logger.write_log(f"{len(self.events)} Event(s) obtained succesfully!", Logger.LogType.INFO)
            self._common.write_log(self.log_box, f"{len(self.events)} Event(s) obtained succesfully!")
            return len(self.events)
        except FileNotFoundError as file_not_found_error:
            self._common.messagebox_exception(file_not_found_error)
            Logger.write_log(f"File not found error: {str(file_not_found_error)}", Logger.LogType.ERROR, file_not_found_error)
            self._common.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            self._common.messagebox_exception(permission_error)
            Logger.write_log(f"Permission error: {str(permission_error)}", Logger.LogType.ERROR, permission_error)
            self._common.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except ValueError as value_error:
            self._common.messagebox_exception(value_error)
            Logger.write_log(f"Value error: {str(value_error)}", Logger.LogType.ERROR, value_error)
            self._common.write_log(self.log_box, f"Value error: {str(value_error)}")
        # except GoogleCalendarConnectionError as connection_error:
        #     self._common.messagebox_exception(connection_error)
        #     CommonOperations.write_log(self.log_box, f"Connection error: {str(connection_error)}")
        # except GoogleCalendarAPIError as api_error:
        #     self._common.messagebox_exception(api_error)
        #     CommonOperations.write_log(self.log_box, f"Google Calendar API error: {str(api_error)}")
        except Exception as error:
            self._common.messagebox_exception(error)
            Logger.write_log(f"Generic error: {str(error)}", Logger.LogType.ERROR, error)
            self._common.write_log(self.log_box, f"Generic error: {str(error)}")

    def get_and_preview(self):
        events_count = self.get_events()
        
        if (events_count == 0): 
            return;
        
        self.events_list_viewer_window()

    def get_and_plot(self):
        events_count = self.get_events()
        
        if events_count == 0: 
            return
        
        # save results to a temp file
        tmp = tempfile.NamedTemporaryFile(delete=False)  # Prevent automatic deletion
        try:
            self.file_path.delete("0", tkinter.END)
            self.file_path.insert("0", string=tmp.name)
            self.save_results_to_file()

            # open graph frame
            FrameController.show_frame(self._common.get_frames()[GraphFrame])
            
            # edit file field to add temp file
            GraphFrame.set_file_path(self._common.get_frames()[GraphFrame], text=tmp.name)
        except Exception as e:
            raise e
        
    def cleanup_temp_files(self):
        """Delete temp files of the previus sessions"""
        temp_dir = tempfile.gettempdir() 
        app_temp_files = glob.glob(os.path.join(temp_dir, 'tmp*'))  # 'tmp' prefix

        # delete all temp files
        for temp_file in app_temp_files:
            try:
                os.unlink(temp_file)  
            except PermissionError:
                pass  # skip if I'm using the file
            except FileNotFoundError:
                pass          
    
    def events_list_viewer_window(self):  
        Logger.write_log("Events list viewer", Logger.LogType.INFO)

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel()
            self.toplevel_window.after(200, lambda: self.toplevel_window.iconbitmap('./imgs/list.ico')) # i have to delay the icon because it' buggy on windows
            self.toplevel_window.title(f'{len(self.events)} Event(s) obtained')

            # Create a grid inside the toplevel window
            self.toplevel_window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically
            self.toplevel_window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
            self.toplevel_window.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally
            
            event_list_file_viewer = ctk.CTkTextbox(self.toplevel_window)
            event_list_file_viewer.bind("<Key>", lambda e: "break")  # set the textbox readonly
            event_list_file_viewer.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10), sticky="nsew")
            
            button_save = ctk.CTkButton(self.toplevel_window, text="Save results", command=lambda: self.get_filepath_to_save_results())
            button_save.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")
            
            button_cancel = ctk.CTkButton(self.toplevel_window, text="Cancel", command=lambda: self.close_top_frame_window())
            button_cancel.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="nsew")
             
            event_list_file_viewer.delete(1.0, tkinter.END)

            events_info = self.format_events_content()
            
            # print event after event
            for event in events_info:
                event_info_str = f"INDEX: {event['index']} | ID: {event['ID']} | SUMMARY: {event['summary']} | START: {event['start']} | END: {event['end']} | DURATION: {event['duration']}\n"
                event_list_file_viewer.insert(tkinter.END, event_info_str)
    
            self.toplevel_window.attributes("-topmost", True) # focus to this windows
            CommonOperations.centerTopLevel(self.toplevel_window)
        else:
            self.toplevel_window.focus()  # if window exists focus it
        
        return self.toplevel_window
    
    def format_events_content(self):
        # obtain only important informations about the event
        event_dict = {}
        events_info = []
        index = 1
        for event in self.events:
            
            # somethimes the event doesn't have 'dateTime'
            try:
                start_date = event['start']['dateTime']
                end_date = event['end']['dateTime']
            except:
                start_date = event['start']['date']
                end_date = event['end']['date']
            
            start_datetime = datetime.fromisoformat(start_date)
            end_datetime = datetime.fromisoformat(end_date)
            duration = end_datetime - start_datetime
            
            event_dict = {
                'index': index,
                'ID': event['id'],
                'summary': event['summary'],
                'start': start_date,
                'end': end_date,
                'duration': duration
            }
            events_info.append(event_dict)
            index += 1 
        
        return events_info

    def get_filepath_to_save_results(self):
        if self.file_path != None and len(self.file_path.get()) != 0:
            self.save_results_to_file() 
            return
        
        if self.toplevel_entry_window is None or not self.toplevel_entry_window.winfo_exists():
            self.toplevel_entry_window = ctk.CTkToplevel()
            self.toplevel_entry_window.after(200, lambda: self.toplevel_entry_window.iconbitmap('./imgs/folder.ico')) # i have to delay the icon because it' buggy on windows
            self.toplevel_entry_window.title('Select a file to save the results')
            self.toplevel_entry_window.geometry("350x50")
            entry = ctk.CTkEntry(self.toplevel_entry_window, width=250, placeholder_text="file path")
            entry.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="nsew")
            button_add_filepath = ctk.CTkButton(self.toplevel_entry_window, width=10, text="", image=self.folder_image, command=lambda: self.get_file_path(entry))
            button_add_filepath.grid(row=0, column=1, padx=5, pady=(10, 10), sticky="nsew")
            button_ok = ctk.CTkButton(self.toplevel_entry_window, width=10, text="Ok", command=lambda: self.save_results_to_file2(entry))
            button_ok.grid(row=0, column=2, padx=5, pady=(10, 10), sticky="nsew") 
                
            self.toplevel_entry_window.resizable(False, False)
            self.toplevel_entry_window.attributes("-topmost", False) # focus to this windows
            CommonOperations.centerTopLevel(self.toplevel_entry_window)
        else:
            self.toplevel_entry_window.focus()  # if window exists focus it
        
        return self.toplevel_entry_window
    
    def save_results_to_file(self):
        try:
            # close the toplevel windows
            if self.toplevel_window: self.close_top_frame_window()
            if self.toplevel_entry_window: self.close_top_frame_entry_window()
            
            # if file doesn't exist, create it
            if not os.path.isfile(self.file_path.get()):
                file = open(self.file_path.get(), "x")
                file.close()
            
            # get all from file csv
            self.data = {}
            if self.overwrite_mode.get() == "off":
                self.data = DataCSV.loadDataFromFile(self.file_path.get(), '|')
            
            # add into data object
            counter = 0
            for event in self.events:
                
                # somethimes the event doesn't have 'dateTime'  
                try:
                    start_date = event['start']['dateTime']
                    end_date = event['end']['dateTime']
                except:
                    start_date = event['start']['date']
                    end_date = event['end']['date']
                    
                start_datetime = datetime.fromisoformat(start_date)
                end_datetime = datetime.fromisoformat(end_date)
                duration = end_datetime - start_datetime
                
                added = DataCSV.addData(self.data, event['id'], data_list=(event['id'], event['summary'], start_date, end_date, duration))
                if added:
                    counter += 1
                
            # save all into data
            DataCSV.saveDataToFile(self.data, self.file_path.get(), '|', 'utf-8')     
            
            Logger.write_log(f"{counter} event(s) added to file {self.file_path.get()}", Logger.LogType.INFO)
            self._common.write_log(self.log_box, f"{counter} event(s) added to file {self.file_path.get()}")
            
        except FileNotFoundError as file_not_found_error:
            self._common.messagebox_exception(file_not_found_error)
            Logger.write_log(f"File not found error: {str(file_not_found_error)}", Logger.LogType.ERROR, file_not_found_error)
            self._common.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            self._common.messagebox_exception(permission_error)
            Logger.write_log(f"Permission error: {str(permission_error)}", Logger.LogType.ERROR, permission_error)
            self._common.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except ValueError as value_error:
            self._common.messagebox_exception(value_error)
            Logger.write_log(f"Value error: {str(value_error)}", Logger.LogType.ERROR, value_error)
            self._common.write_log(self.log_box, f"Value error: {str(value_error)}")
        except KeyError as key_error:
            self._common.messagebox_exception(key_error)
            Logger.write_log(f"Key error: {str(key_error)}", Logger.LogType.ERROR, key_error)
            self._common.write_log(self.log_box, f"Key error: {str(key_error)}")
        except Exception as error:
            self._common.messagebox_exception(error)
            Logger.write_log(f"Generic error: {str(error)}", Logger.LogType.ERROR, error)
            self._common.write_log(self.log_box, f"Generic error: {str(error)}")
    
    def save_results_to_file2(self, entry):
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", entry.get())
        
        self.save_results_to_file()
    
    def close_top_frame_window(self):
        self.toplevel_window.destroy()
        
    def close_top_frame_entry_window(self):
        self.toplevel_entry_window.destroy()
        
    def combobox_callback(self, color):
        self.multi_selection.configure(button_color=self.event_color.get(color))
        self.multi_selection.set(color)
        Logger.write_log(f"color '{color}' selected", Logger.LogType.INFO)
        CommonOperations.write_log(log_box=self.log_box, message=f"color '{color}' selected")
    
    def get_file_path(self, entry):
        self._common.get_file_path(self.log_box, entry)
    
    def set_logbox_text(self, text):
        self.log_box.delete("0.0", tkinter.END)
        self.log_box.insert("0.0", text)
    
    def open_file(self):
        self.file_viewer_window = self._common.file_viewer_window(self.file_viewer_window, self.file_path.get(), self.log_box)
    
    def events_table_preview(self):
        self.events_preview_in_table = self._common.events_preview_in_table(self.events_preview_in_table, self.file_path.get(), self.log_box)
    
    def date_picker(self, type):
        self.date_picker_window = self._common.date_picker_window(type, self.date_picker_window, self.entry_date_from, self.entry_date_to, self.log_box)
#?###########################################################

#?###########################################################
class GraphFrame(ctk.CTkFrame):
    main_class = None
    file_viewer_window = None
    events_preview_in_table = None
    _common = CommonOperations()
    stop_event = threading.Event() 
    
    def __init__(self, parent, main_class):
        ctk.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # load images
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        folder_image = tkinter.PhotoImage(file='./imgs/folder.png')
        file_image = tkinter.PhotoImage(file='./imgs/file.png')
        table_image = tkinter.PhotoImage(file='./imgs/table.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        square_image = tkinter.PhotoImage(file='./imgs/square.png')
        square_check_image = tkinter.PhotoImage(file='./imgs/square-check.png')
        info_image = tkinter.PhotoImage(file='./imgs/information.png')
        icon = tkinter.PhotoImage(file='./imgs/icon.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # create sidebar frame with widgets
        (sidebar_button_1, sidebar_button_2, sidebar_button_3, sidebar_button_4, google_calendar_link, logo_button) = GUIWidgets.create_side_bar_frame(self, plus_image, edit_image, list_image, chart_image, google_image, icon)
        sidebar_button_1.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[NewEventsFrame]))
        sidebar_button_2.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[EditEventsFrame]))
        sidebar_button_3.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GetEventsFrame]))
        sidebar_button_4.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[GraphFrame]))
        logo_button.configure(command=lambda: FrameController.show_frame(self._common.get_frames()[MainFrame]))
        google_calendar_link.configure(command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
        
        # create main panel
        (self.file_path, self.button_file_path, self.button_open_file, self.button_open_events_table_preview) = GUIWidgets.create_file_path_scroll_frame_for_graph_frame(self, folder_image, file_image, table_image, info_image)
        self.button_file_path.configure(command=self.get_file_path)
        self.button_open_file.configure(command=self.open_file)
        self.button_open_events_table_preview.configure(command=self.events_table_preview)
        
        # Graph types
        (self.button_select_all, self.button_deselect_all, self.total_hours_per_year, self.total_hours_per_month, self.total_hours_by_summary, self.total_hours_by_summary2, self.total_hours_per_year_by_summary, self.total_hours_per_month_by_summary) = GUIWidgets.create_graph_types_scroll_frame(self, square_check_image, square_image)
        self.button_select_all.configure(command=self.select_all)
        self.button_deselect_all.configure(command=self.deselect_all)

        # Generate Graph Button
        self.graph_button = ctk.CTkButton(self, command=self.generate_graph, image=chart_image, border_width=2, text="Generate")
        self.graph_button.grid(row=4, column=1, padx=20, pady=20)
        
        # Tooltips
        CTkToolTip(self.file_path, delay=0.3, message="(Required) Enter the path to the file you generated from the 'Get Events List' section.")
        CTkToolTip(self.button_open_file, delay=0.3, message="Open file preview")
        CTkToolTip(self.button_open_events_table_preview, delay=0.3, message="Open file preview in table")
        CTkToolTip(self.graph_button, delay=0.3, message="Generate graphs")
        CTkToolTip(self.button_select_all, delay=0.3, message="Select all types")
        CTkToolTip(self.button_deselect_all, delay=0.3, message="Deselect all types")
        
        # create log textbox
        self.log_box = ctk.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=5, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def get_file_path(self):
        file_path = filedialog.askopenfilename(title="Select file where do you want to save data", filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")))
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", file_path)
        Logger.write_log(f"file '{file_path}' selected", Logger.LogType.INFO)
        self._common.write_log(self.log_box, f"file '{file_path}' selected")
    
    def set_file_path(self, text: str):
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", string=text)

    def set_logbox_text(self, text):
        self.log_box.delete("0.0", tkinter.END)
        self.log_box.insert("0.0", text)
    
    def open_file(self):
        self.file_viewer_window = self._common.file_viewer_window(self.file_viewer_window, self.file_path.get(), self.log_box)

    def events_table_preview(self):
        self.events_preview_in_table = self._common.events_preview_in_table(self.events_preview_in_table, self.file_path.get(), self.log_box)

    def select_all(self):
        self.total_hours_per_year.select()
        self.total_hours_per_month.select()
        self.total_hours_by_summary.select()
        self.total_hours_by_summary2.select()
        self.total_hours_per_year_by_summary.select()
        self.total_hours_per_month_by_summary.select()
        Logger.write_log(f"all chart types selected", Logger.LogType.INFO)
        self._common.write_log(self.log_box, f"all chart types selected")
        
    def deselect_all(self):
        self.total_hours_per_year.deselect()
        self.total_hours_per_month.deselect()
        self.total_hours_by_summary.deselect()
        self.total_hours_by_summary2.deselect()
        self.total_hours_per_year_by_summary.deselect()
        self.total_hours_per_month_by_summary.deselect()
        Logger.write_log(f"all chart types deselected", Logger.LogType.INFO)
        self._common.write_log(self.log_box, f"all chart types deselected")
        
    # Timeout function to stop the chart generation
    def generate_chart_with_timeout(self, chart_function, data, timeout=ConfigKeys.Keys.GRAPH_TIMEOUT.value):
        def target():
            try:
                if not self.stop_event.is_set():  # Check if timeout occurred
                    chart_function(data)
            except Exception as ex:
                self._common.messagebox_exception(ex)
                Logger.write_log(f"An error occurred during setting timeout for chart generation", Logger.LogType.INFO)
                self._common.write_log(self.log_box, f"An error occurred during setting timeout for chart generation")

        # Create and start the thread
        chart_thread = threading.Thread(target=target)
        chart_thread.start()

        # Wait for the thread to finish or timeout
        chart_thread.join(timeout)

        # If the thread is still alive after the timeout, set the stop event
        if chart_thread.is_alive():
            self.stop_event.set()
            Logger.write_log(f"Chart generation timed out.", Logger.LogType.WARN)
            self._common.write_log(self.log_box, "Chart generation timed out.")
            CTkMessagebox(title="Chart Generation Error", message="One or more charts were cancelled due to a timeout. Please try again later.", icon="cancel", option_1="OK")

    def reset_stop_event(self):
        self.stop_event.clear()  # Reset the stop event for future calls

    def generate_graph(self):
        if self._common.check_file_path_errors(self.log_box, self.file_path.get()):
            return

        try:
            Logger.write_log(f"Generating chart", Logger.LogType.INFO)
            self._common.write_log(self.log_box, "Generating chart")
            data = Plotter.Plotter.loadData(self.file_path.get())
            Plotter.Plotter.allStats(data)

            # Reset the stop event before generating new charts
            self.reset_stop_event()

            if self.total_hours_per_year.get() == "on":
                self.generate_chart_with_timeout(Plotter.Plotter.chart_TotalHoursPerYear, data)
            if self.total_hours_per_month.get() == "on":
                self.generate_chart_with_timeout(Plotter.Plotter.chart_TotalHoursPerMonth, data)
            if self.total_hours_by_summary.get() == "on":
                self.generate_chart_with_timeout(Plotter.Plotter.chart_TotalHoursBySummary, data)
            if self.total_hours_by_summary2.get() == "on":
                self.generate_chart_with_timeout(Plotter.Plotter.chart_TotalHoursBySummaryPie, data)
            if self.total_hours_per_year_by_summary.get() == "on":
                self.generate_chart_with_timeout(Plotter.Plotter.chart_TotalHoursPerYearBySummary, data)
            if self.total_hours_per_month_by_summary.get() == "on":
                self.generate_chart_with_timeout(Plotter.Plotter.chart_TotalHoursPerMonthBySummary, data)

        except FileNotFoundError as error:
            Logger.write_log(f"Error, the file '{self.file_path.get()}' doesn't exist", Logger.LogType.ERROR, error)
            self._common.write_log(self.log_box, f"Error, the file '{self.file_path.get()}' doesn't exist")
        except pandas.errors.EmptyDataError as error:
            Logger.write_log(f"Error, the file '{self.file_path.get()}' is empty", Logger.LogType.ERROR, error)
            self._common.write_log(self.log_box, f"Error, the file '{self.file_path.get()}' is empty")
        except PermissionError as permission_error:
            Logger.write_log(f"Permission error: {str(permission_error)}", Logger.LogType.ERROR, permission_error)
            self._common.messagebox_exception(permission_error)
            self._common.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except ValueError as value_error:
            Logger.write_log(f"Value error: {str(value_error)}", Logger.LogType.ERROR, value_error)
            self._common.messagebox_exception(value_error)
            self._common.write_log(self.log_box, f"Value error: {str(value_error)}")
        except Exception as error:
            Logger.write_log(f"Generic error: {str(error)}", Logger.LogType.ERROR, error)
            self._common.messagebox_exception(error)
            self._common.write_log(self.log_box, f"Generic error: {str(error)}")

#?###########################################################

#?###########################################################
class MainFrame(ctk.CTkFrame):
    _common = CommonOperations()
    
    def __init__(self, parent, main_class):
        ctk.CTkFrame.__init__(self, parent)
        
        # load images
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        buymeacoffe_donation_image = tkinter.PhotoImage(file='./imgs/donation.png')
        paypal_donation_image = tkinter.PhotoImage(file='./imgs/paypal.png')
        github_image = tkinter.PhotoImage(file='./imgs/github.png')
        icon_image = tkinter.PhotoImage(file='./imgs/icon.png')
    
        # custom font
        title_font = ctk.CTkFont(family="Georgia", weight='bold', slant='italic', size=45)
        
        # main
        ctk.CTkLabel(self, text="", image=icon_image, fg_color="transparent").pack(padx=20, pady=(50, 20))
        ctk.CTkLabel(self, text="Calendar Data Manager", font=title_font, text_color='#e06c29', fg_color="transparent").pack(padx=20, pady=50)
        #ctk.CTkLabel(self, text="Choose the action", fg_color="transparent", font=("Arial", 32)).pack(padx=20, pady=20)
        ctk.CTkButton(master=self, image=plus_image, text="New Events", command=lambda: FrameController.show_frame(self._common.get_frames()[NewEventsFrame])).pack(padx=20, pady=10, anchor='center')
        ctk.CTkButton(master=self, image=edit_image, text="Edit Events", command=lambda: FrameController.show_frame(self._common.get_frames()[EditEventsFrame])).pack(padx=20, pady=10, anchor='center')
        ctk.CTkButton(master=self, image=list_image, text="Get Events", command=lambda: FrameController.show_frame(self._common.get_frames()[GetEventsFrame])).pack(padx=20, pady=10, anchor='center')
        ctk.CTkButton(master=self, image=chart_image, text="Graph", command=lambda: FrameController.show_frame(self._common.get_frames()[GraphFrame])).pack(padx=20, pady=10, anchor='center')
        
        button_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        button_frame.pack(side='bottom', anchor='sw', padx=20, pady=10)
        
        ctk.CTkLabel(self, text=f"Version {ConfigKeys.Keys.VERSION.value}", fg_color="transparent").place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10) # version
        
        if (ConfigKeys.Keys.HOMEBUTTONS_MESSAGESECTION.value):
            ctk.CTkLabel(button_frame, text="If you'd like to learn more about the project or support it:", fg_color="transparent", font=("Arial", 12, "italic")).pack(side='top', anchor='w', pady=(0, 10)) # description

        if (ConfigKeys.Keys.HOMEBUTTONS_GITHUB.value):
            github_btn = ctk.CTkButton(master=button_frame, image=github_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open(ConfigKeys.Keys.GITHUB_PAGE_LINK.value))
            github_btn.pack(side='left', padx=5)
            CTkToolTip(github_btn, delay=0.3, message="Github page")

        if (ConfigKeys.Keys.HOMEBUTTONS_BUYMEACOFFE.value):
            donate_buymeacoffe_btn = ctk.CTkButton(master=button_frame, image=buymeacoffe_donation_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_BUYMEACOFFE_PAGE_LINK.value))
            donate_buymeacoffe_btn.pack(side='left', padx=5)
            CTkToolTip(donate_buymeacoffe_btn, delay=0.3, message="Donate with \"buy me a coffe\"")
        
        if (ConfigKeys.Keys.HOMEBUTTONS_PAYPAL.value):
            donate__paypal_btn = ctk.CTkButton(master=button_frame, image=paypal_donation_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_PAYPAL_PAGE_LINK.value))
            donate__paypal_btn.pack(side='left', padx=5)
            CTkToolTip(donate__paypal_btn, delay=0.3, message="Donate with \"Paypal\"")
        
#?###########################################################

#?###########################################################   
class LoginFrame(ctk.CTkFrame):
    width = 900
    height = 600
    main_class = None
    toplevel_window = None
    _common = CommonOperations()
    
    def __init__(self, parent, main_class):
        ctk.CTkFrame.__init__(self, parent)
        self.main_class = main_class

        # load images
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        arrow_image = tkinter.PhotoImage(file='./imgs/arrow-right.png')

        ctk.CTkLabel(self, text="Login", fg_color="transparent", font=("Arial", 32)).pack(padx=20, pady=20)

        google_calendar = ctk.CTkButton(master=self, image=google_image, text="Google Calendar", height=50, width=250, command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
        google_login = ctk.CTkButton(master=self, image=arrow_image, text="Login with Google", height=50, width=250, command=lambda: self.setCredentialsPathFrame())

        google_calendar.pack(padx=20, pady=10, anchor='center')
        google_login.pack(padx=20, pady=10, anchor='center')

        # Tooltips
        CTkToolTip(google_calendar, delay=0.3, message="View and manage your Google Calendar")
        CTkToolTip(google_login, delay=0.3, message="Login using your Google account")
        
            
    def setCredentialsPathFrame(self):
        self.__setCredentialsPath()
    
    def __setCredentialsPath(self):
        # get response from dialog
        credentials_path = './settings/client.json'
        if len(credentials_path) == 0: return
        token_path = credentials_path.rsplit("/", 1)[0] + "/" + "token.json"
                
        try:
            # get credentials
            credentials = gc.CalendarEventsManager.connectionSetup(credentials_path, gc.CalendarEventsManager.SCOPE, token_path)
        except Exception as error:
            self._common.messagebox_exception(error)
            credentials = None
            try: os.remove(token_path) # delete token.json 
            except: pass
        
        # response message box
        if credentials is not None:
            (user, _, _) = gc.CalendarEventsManager.get_user_info(credentials)
            
            # set credentials values to main class
            self._common.set_credentials(credentials, credentials_path, token_path)
            
            self.updateUsernameMenuItem()
            
            FrameController.show_frame(self._common.get_frames()[MainFrame])
        else:
            msg = CTkMessagebox(title="Credentials error", message="Do you wish to retry?", icon="cancel", option_1="No", option_2="Yes")
            response = msg.get()
            if response=="Yes":
                self.setCredentialsPathFrame()
    
    def updateUsernameMenuItem(self):
        self.main_class.updateUsernameMenuItem()
#?###########################################################

#*###########################################################
class App(): 
    root: ctk.CTk
    _menu: CTkMenuBar
    _button_5: ctk.CTkButton
    _common = CommonOperations()
    frames = {}
    
    app_width: int 
    app_height: int 
    
    def __init__(self):
        root = ctk.CTk()
        self.root = root
        self._menu = None
        self._button_5 = None

        ConfigKeys.load_values_from_json()
        Logger.load_values_from_json()

        self.app_width = ConfigKeys.Keys.APP_WIDTH.value
        self.app_height = ConfigKeys.Keys.APP_HEIGHT.value
        
        Logger.write_log("Application started", Logger.LogType.INFO)

        # read data from json to get path from last session
        listRes = js.JSONPreferences.ReadFromJSON()
        if listRes != None and len(listRes) > 0:
            self.credentials_path = listRes["CredentialsPath"]
            self.token_path = listRes["TokenPath"]
            try: 
                self.credentials = gc.CalendarEventsManager.connectionSetup(self.credentials_path, gc.CalendarEventsManager.SCOPE, self.token_path)
            except Exception as e:
                print(f"Error: {e}")
         
        self.init_window()
        self.init_menu()
        FrameController.page_controller(self, self.root, self._common)
        
        self.root.mainloop()
    
    def init_window(self):
        # configure window
        self.root.iconbitmap('./imgs/icon.ico')
        self.root.title("Calendar Data Manager")
        CommonOperations.centerWindow(self.root, self.app_width, self.app_height)
        self.root.minsize(1100, 900)

        listRes = js.JSONPreferences.ReadFromJSON()
        if listRes != None and len(listRes) > 0:
            try: 
                appearance = listRes["Appearence"]
                CommonOperations.change_appearance(appearance)
            except: pass
            try: 
                text_scaling = listRes["TextScaling"]
                CommonOperations.change_scaling_event(text_scaling)
            except: pass
            try: 
                color_theme = listRes["ColorTheme"]
                CommonOperations.change_color_theme(color_theme)
            except: pass 
    
    def init_menu(self):
        self._menu = CTkMenuBar(self.root) 
        button_1 = self._menu.add_cascade("File")
        button_3 = self._menu.add_cascade("Settings")
        button_4 = self._menu.add_cascade("About")
        button_6 = self._menu.add_cascade("Help")
                        
        if self._common.get_credentials() is not None:
            self.updateUsernameMenuItem()

        dropdown1 = CustomDropdownMenu(widget=button_1)
        
        if (ConfigKeys.Keys.MENUITEM_EXIT.value):
            dropdown1.add_option(option="Exit", command=lambda: exit())

        dropdown1.add_separator()

        dropdown3 = CustomDropdownMenu(widget=button_3)

        if (ConfigKeys.Keys.MENUITEM_APPEARANCE.value):
            sub_menu2 = dropdown3.add_submenu("Appearance")
            sub_menu2.add_option(option="Dark", command=lambda: self.change_app_appearance("dark"))
            sub_menu2.add_option(option="Light", command=lambda: self.change_app_appearance("light"))
        
        if (ConfigKeys.Keys.MENUITEM_SCALING.value):
            sub_menu3 = dropdown3.add_submenu("Scaling")
            sub_menu3.add_option(option="120%", command=lambda: CommonOperations.change_scaling_event("120"))
            sub_menu3.add_option(option="110%", command=lambda: CommonOperations.change_scaling_event("110"))
            sub_menu3.add_option(option="100%", command=lambda: CommonOperations.change_scaling_event("100"))
            sub_menu3.add_option(option="90%", command=lambda: CommonOperations.change_scaling_event("90"))
            sub_menu3.add_option(option="80%", command=lambda: CommonOperations.change_scaling_event("80"))
            sub_menu3.add_option(option="70%", command=lambda: CommonOperations.change_scaling_event("70"))
        
        if (ConfigKeys.Keys.MENUITEM_THEME.value):
            sub_menu4 = dropdown3.add_submenu("Theme")
            sub_menu4.add_option(option="Blue", command=lambda: CommonOperations.set_color_theme("blue"))
            sub_menu4.add_option(option="Dark Blue", command=lambda: CommonOperations.set_color_theme("dark-blue"))
            sub_menu4.add_option(option="Green", command=lambda: CommonOperations.set_color_theme("green"))

        dropdown4 = CustomDropdownMenu(widget=button_4)
        if (ConfigKeys.Keys.SHARD_WEBSITE.value):
            dropdown4.add_option(option="Website", command=lambda: webbrowser.open(ConfigKeys.Keys.SHARD_WEBSITE.value))
        if (ConfigKeys.Keys.MENUITEM_SHARE.value):
            dropdown4.add_option(option="Share", command=lambda: webbrowser.open(ConfigKeys.Keys.GITHUB_PAGE_LINK.value))
        if (ConfigKeys.Keys.MENUITEM_DONATE.value):
            sub_menu4 = dropdown4.add_submenu("Support this project")
            sub_menu4.add_option(option="Donate with \"Buy me a coffe\"", command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_BUYMEACOFFE_PAGE_LINK.value))
            sub_menu4.add_option(option="Donate with \"Paypal\"", command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_PAYPAL_PAGE_LINK.value))

        dropdown6 = CustomDropdownMenu(widget=button_6)
        if (ConfigKeys.Keys.MENUITEM_SUPPORT.value):
            subject: str = "Calendar Data Manager - Support"
            dropdown6.add_option(option="Support", command=lambda: webbrowser.open(f"mailto:{ConfigKeys.Keys.SHARD_EMAIL.value}?subject={subject}"))
        if (ConfigKeys.Keys.MENUITEM_BUGREPORT.value):
            dropdown6.add_option(option="Report a bug", command=lambda: webbrowser.open(ConfigKeys.Keys.GITHUB_ISSUES_LINK.value))

    def updateUsernameMenuItem(self):
        (_, email, picture_url) = gc.CalendarEventsManager.get_user_info(self._common.get_credentials())
        
        # Configure column 4 to expand (to align right).
        self._menu.columnconfigure(4, weight=1)
        
        default_user_image = tkinter.PhotoImage(file='./imgs/user.png')
        
        if self._common.get_credentials() is not None:
            # Try to load the profile image from URL
            res = self.get_user_image_from_url(picture_url)
            if picture_url and res is not None:
                user_image = res
            else:
                # Fallback to default image
                user_image = default_user_image

            if self._button_5 is not None:
                self._button_5.configure(text=str(email), image=user_image)
                self._button_5.grid(row=0, column=4, padx=10, pady=10, sticky="e")
            else:
                self._button_5 = ctk.CTkButton(self._menu, text=str(email), fg_color="transparent", image=user_image, command=self.show_user_menu)
                self._button_5.grid(row=0, column=4, padx=10, pady=10, sticky="e")
                self.dropdown5 = CustomDropdownMenu(widget=self._button_5)
                self.dropdown5.add_option(option="Google Calendar", command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
                self.dropdown5.add_option(option="Log out", command=lambda: self.log_out())
        
            self.change_app_appearance_profile()
        
        else:
            self.forgetUsernameMenuItem()
            
    def get_user_image_from_url(self, url):
        try:
            # get the image
            response = requests.get(url)
            response.raise_for_status()  # check if the request is correct
            img_data = response.content
            
            # load the image
            image = pilImage.open(BytesIO(img_data))
            image = image.resize((32, 32), pilImage.LANCZOS)

            # create a mask for the image
            mask = pilImage.new('L', (32, 32), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 32, 32), fill=255)
            
            # apply the mask
            image = image.convert("RGBA")
            image.putalpha(mask) 

            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def show_user_menu(self):
        self.dropdown5.show()
    
    def forgetUsernameMenuItem(self):
        if self._button_5 is not None:
            self._button_5.grid_forget()
            
    def log_out(self):
        Logger.write_log(f"Logging out", Logger.LogType.INFO)
        self.forgetUsernameMenuItem()
        FrameController.show_frame(self._common.get_frames()[LoginFrame])
    
    def change_app_appearance(self, mode: str):
        self._common.change_appearance(mode)
        self.change_app_appearance_profile(mode)

    def change_app_appearance_profile(self, appearance: str = ''):
        Logger.write_log(f"Changing appearance to {appearance}", Logger.LogType.INFO)

        # edit color text button following the style apperance
        if appearance is None or appearance == '':
            appearance = self._common.get_appearance()

        if appearance.lower() == 'light':
            self._button_5.configure(text_color="black")
        elif appearance.lower() == 'dark':
            self._button_5.configure(text_color="white")
        else:
            self._button_5.configure(text_color="#76797e")

#*###########################################################

if __name__ == "__main__":
    app = App()