import webbrowser
import os
import traceback
import tempfile
import pandas
from datetime import datetime, timedelta
from babel import numbers
from googleapiclient.errors import HttpError

import JSONSettings as js
import GoogleCalendarEventsManager as gc
import Plotter
from DataEditor import DataCSV

import tkinter
from tkinter import filedialog
import customtkinter
from CTkMenuBar import *
from CTkMessagebox import *
from tkcalendar import *
from tkcalendar import *
from CTkToolTip import *

#* TODO: add scrollable dropdown -> https://github.com/Akascape/CTkScrollableDropdown
#* TODO: when it is realesed -> https://customtkinter.tomschimansky.com/showcase/
#? TODO: get token expire date and other informations 
#* TODO: allow copy text from log box
#* TODO: use more function and set private variables and functions where it is possible
#? TODO: merge all the logbox to one
#* TODO: add new frame "delete events"
#* TODO: add log frame: https://developers.google.com/calendar/api/guides/errors?hl=en
#* TODO: resolve problems: https://developers.google.com/calendar/api/troubleshoot-authentication-authorization?hl=en
#?###########################################################
class NewEventsFrame(customtkinter.CTkFrame):
    main_class = None
    toplevel_window = None
    event_color = {"Lavender": "#7986cb", "Sage": "#33b679", "Grape": "#8e24aa", "Flamingo": "#e67c73", "Banana": "#f6bf26", "Tangerine": "#f4511e", "Peacock": "#039be5", "Graphite": "#616161", "Blueberry": "#3f51b5", "Basil": "#0b8043", "Tomato": "#d50000"}
    timezone = ['Africa/Abidjan', 'Africa/Accra', 'Africa/Algiers', 'Africa/Bissau', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/El_Aaiun', 'Africa/Juba', 'Africa/Khartoum', 'Africa/Lagos', 'Africa/Maputo', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Sao_Tome', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Asuncion', 'America/Atikokan', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Cayenne', 'America/Chicago', 'America/Chihuahua', 'America/Costa_Rica', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Fort_Nelson', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Colombo', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kathmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Riyadh', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ulaanbaatar', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faroe', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Sydney', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'GMT', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Wake', 'Pacific/Wallis', 'UTC']
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
                
        # load images
        calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Other Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, image=plus_image, text="New Events", command=self.go_to_new_events_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, image=edit_image, text="Edit Events", command=self.go_to_edit_events_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, image=list_image, text="Get Events List", command=self.go_to_get_events_by_title_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, image=chart_image, text="Graph", command=self.go_to_graph_frame)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.google_calendar_link = customtkinter.CTkButton(self.sidebar_frame, image=google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/'))
        self.google_calendar_link.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # create main panel
        self.title_label_main = customtkinter.CTkLabel(self, text="Create New Event", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label_main.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")
        
        # main entry
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="ew")
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_summary = customtkinter.CTkLabel(self.main_frame, text="Summary:")
        self.label_summary.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_summary = customtkinter.CTkEntry(self.main_frame, placeholder_text="summary")
        self.entry_summary.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        self.label_description = customtkinter.CTkLabel(self.main_frame, text="Description:")
        self.label_description.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_description = customtkinter.CTkTextbox(self.main_frame, width=250, height=100)
        self.entry_description.grid(row=1, column=1, padx=(0, 0), pady=(10, 0), sticky="ew")
        self.label_color = customtkinter.CTkLabel(self.main_frame, text="Color:")
        self.label_color.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")
        self.multi_selection = customtkinter.CTkComboBox(self.main_frame, state="readonly", values=list(self.event_color.keys()), command=self.combobox_callback)
        self.multi_selection.set("Lavender")
        self.multi_selection.grid(row=2, column=1, padx=0, pady=(10, 10), sticky="w")
        self.color_preview = customtkinter.CTkCanvas(self.main_frame, width=15, height=15)
        self.color_preview.grid(row=2, column=1, sticky="w", padx=(150, 0), pady=(10, 10))
        self.color_preview.configure(bg=self.event_color.get('Lavender'))
        
        # date
        self.date_frame = customtkinter.CTkFrame(self, width=400)
        self.date_frame.grid(row=2, column=1, padx=(50, 50), pady=10, sticky="nsew")
        self.date_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_date_frame = customtkinter.CTkLabel(master=self.date_frame, text="Date Interval")
        self.label_date_frame.grid(row=0, column=0, columnspan=3, padx=0, pady=10, sticky="ew")
        self.label_date_from = customtkinter.CTkLabel(self.date_frame, text="From:")
        self.label_date_from.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_date_from = customtkinter.CTkEntry(self.date_frame, placeholder_text="yyyy-mm-dd hh:mm")
        self.entry_date_from.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        self.entry_date_button = customtkinter.CTkButton(self.date_frame, text="", width=10, image=calendar_image, command=lambda: self.date_picker(1))
        self.entry_date_button.grid(row=1, column=2, padx=0, pady=10, sticky="w")
        self.label_date_to = customtkinter.CTkLabel(self.date_frame, text="To:")
        self.label_date_to.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_date_to = customtkinter.CTkEntry(self.date_frame, placeholder_text="yyyy-mm-dd hh:mm")
        self.entry_date_to.grid(row=2, column=1, padx=0, pady=10, sticky="ew")
        self.entry_date_button2 = customtkinter.CTkButton(self.date_frame, text="", width=10, image=calendar_image, command=lambda: self.date_picker(2))
        self.entry_date_button2.grid(row=2, column=2, padx=0, pady=10, sticky="w")
        self.label_timezone = customtkinter.CTkLabel(self.date_frame, text="Timezone:")
        self.label_timezone.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.timezone_selection = customtkinter.CTkComboBox(self.date_frame, state="readonly", values=list(self.timezone), command=self.combobox_callback)
        self.timezone_selection.set(self.main_class.get_timezone())
        self.timezone_selection.grid(row=3, column=1, padx=0, pady=(10, 10), sticky="nsew")
        
        # create button
        self.create_button = customtkinter.CTkButton(self, image=plus_image, text="Create", border_width=2, command=self.create_event)
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
        self.log_box = customtkinter.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=4, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def create_event(self):
        summary = self.entry_summary.get()
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        time_zone = self.timezone_selection.get()
        
        # update preferred TimeZone
        self.main_class.set_timezone(time_zone)
        
        if len(summary.replace(" ", "")) == 0:
            self.main_class.write_log(self.log_box, f"Error on creating event: summary is missing")
            return
        if len(date_from.replace(" ", "")) == 0 or len(date_to.replace(" ", "")) == 0:
            self.main_class.write_log(self.log_box, f"Error on creating event: date is missing")
            return
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M')
            date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M')
        except ValueError:
            self.main_class.write_log(self.log_box, f"Error on creating event: date format is not correct")
        
        # get color index
        color_index = self.main_class.get_color_id(self.event_color, self.multi_selection.get())
        
        try: 
            gc.GoogleCalendarEventsManager.createEvent(self.main_class.get_credentials(), summary, self.entry_description.get("0.0", tkinter.END), date_from, date_to, color_index, timeZone=time_zone)
            self.main_class.write_log(self.log_box, f"Event '{summary}' created succesfully!")
        except FileNotFoundError as file_not_found_error:
            self.main_class.messagebox_exception(file_not_found_error)
            self.main_class.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            self.main_class.messagebox_exception(permission_error)
            self.main_class.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except HttpError as http_error:
            self.main_class.messagebox_exception(http_error)
            self.main_class.write_log(self.log_box, f"HTTP error: {str(http_error)}")
        except Exception as error:
            self.main_class.messagebox_exception(error)
            self.main_class.write_log(self.log_box, f"Generic error: {str(error)}")   
        
    def combobox_callback(self, color):
        self.color_preview.configure(bg=self.event_color.get(color))
        self.main_class.write_log(self.log_box, f"color '{color}' selected")
    
    def date_picker(self, type):
        self.toplevel_window = self.main_class.date_picker_window(type, self.toplevel_window, self.entry_date_from, self.entry_date_to, self.log_box)
    
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsFrame)
    
    def go_to_graph_frame(self):
        self.main_class.show_frame(GraphFrame)
#?###########################################################

#?###########################################################
#* TODO: add preview and confirm button before edit
class EditEventsFrame(customtkinter.CTkFrame):
    main_class = None
    date_picker_window = None
    event_color_from = {"Lavender": "#7986cb", "Sage": "#33b679", "Grape": "#8e24aa", "Flamingo": "#e67c73", "Banana": "#f6bf26", "Tangerine": "#f4511e", "Peacock": "#039be5", "Graphite": "#616161", "Blueberry": "#3f51b5", "Basil": "#0b8043", "Tomato": "#d50000", "No Color Filtering": ""}
    event_color_to = {"Lavender": "#7986cb", "Sage": "#33b679", "Grape": "#8e24aa", "Flamingo": "#e67c73", "Banana": "#f6bf26", "Tangerine": "#f4511e", "Peacock": "#039be5", "Graphite": "#616161", "Blueberry": "#3f51b5", "Basil": "#0b8043", "Tomato": "#d50000"}
    timezone = ['Africa/Abidjan', 'Africa/Accra', 'Africa/Algiers', 'Africa/Bissau', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/El_Aaiun', 'Africa/Juba', 'Africa/Khartoum', 'Africa/Lagos', 'Africa/Maputo', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Sao_Tome', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Asuncion', 'America/Atikokan', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Cayenne', 'America/Chicago', 'America/Chihuahua', 'America/Costa_Rica', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Fort_Nelson', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Colombo', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kathmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Riyadh', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ulaanbaatar', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faroe', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Sydney', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'GMT', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Wake', 'Pacific/Wallis', 'UTC']
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # load images
        calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        arrow_image = tkinter.PhotoImage(file='./imgs/arrow-right2.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 4), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Other Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, image=plus_image, text="New Events", command=self.go_to_new_events_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, image=edit_image, text="Edit Events", command=self.go_to_edit_events_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, image=list_image, text="Get Events List", command=self.go_to_get_events_by_title_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, image=chart_image, text="Graph", command=self.go_to_graph_frame)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.google_calendar_link = customtkinter.CTkButton(self.sidebar_frame, image=google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/'))
        self.google_calendar_link.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # create main panel
        self.title_label_main = customtkinter.CTkLabel(self, text="Edit Events", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label_main.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")
                
        # Create a frame with a 1x2 grid
        main_frame = customtkinter.CTkFrame(self)
        main_frame.grid(row=1, column=1, padx=50, pady=10, sticky="ew")
        main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # old main values
        self.old_values_frame = customtkinter.CTkFrame(main_frame)
        self.old_values_frame.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        self.old_values_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_frame_old = customtkinter.CTkLabel(self.old_values_frame, text="OLD Values")
        self.label_frame_old.grid(row=0, column=0, columnspan=3, padx=0, pady=10, sticky="ew")
        self.label_summary_old = customtkinter.CTkLabel(self.old_values_frame, text="Summary:")
        self.label_summary_old.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_summary_old = customtkinter.CTkEntry(self.old_values_frame, placeholder_text="summary")
        self.entry_summary_old.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        self.label_description_old = customtkinter.CTkLabel(self.old_values_frame, text="Description:")
        self.label_description_old.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_description_old = customtkinter.CTkTextbox(self.old_values_frame, width=250, height=100)
        self.entry_description_old.grid(row=2, column=1, padx=(0, 0), pady=(10, 0), sticky="ew")
        self.label_color_old = customtkinter.CTkLabel(self.old_values_frame, text="Color:")
        self.label_color_old.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")
        self.multi_selection_old = customtkinter.CTkComboBox(self.old_values_frame, state="readonly", values=list(self.event_color_from.keys()), command=self.combobox_callback_color1)
        self.multi_selection_old.set("No Color Filtering")
        self.multi_selection_old.grid(row=3, column=1, padx=0, pady=(10, 10), sticky="w")
        self.color_preview_old = customtkinter.CTkCanvas(self.old_values_frame, width=15, height=15)
        self.color_preview_old.grid(row=3, column=1, sticky="w", padx=(150, 0), pady=(10, 10))
        
        # Centered img label
        customtkinter.CTkLabel(main_frame, text="", image=arrow_image).grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        
        # new main values
        self.new_values_frame = customtkinter.CTkFrame(main_frame)
        self.new_values_frame.grid(row=1, column=2, padx=25, pady=10, sticky="ew")
        self.new_values_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_frame_new = customtkinter.CTkLabel(self.new_values_frame, text="NEW Values")
        self.label_frame_new.grid(row=0, column=0, columnspan=3, padx=0, pady=10, sticky="ew")
        self.label_summary_new = customtkinter.CTkLabel(self.new_values_frame, text="Summary:")
        self.label_summary_new.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_summary_new = customtkinter.CTkEntry(self.new_values_frame, placeholder_text="summary")
        self.entry_summary_new.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        self.label_description_new = customtkinter.CTkLabel(self.new_values_frame, text="Description:")
        self.label_description_new.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_description_new = customtkinter.CTkTextbox(self.new_values_frame, width=250, height=100)
        self.entry_description_new.grid(row=2, column=1, padx=(0, 0), pady=(10, 0), sticky="ew")
        self.label_color_new = customtkinter.CTkLabel(self.new_values_frame, text="Color:")
        self.label_color_new.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")
        self.multi_selection_new = customtkinter.CTkComboBox(self.new_values_frame, state="readonly", values=list(self.event_color_to.keys()), command=self.combobox_callback_color2)
        self.multi_selection_new.set("Lavander")
        self.multi_selection_new.grid(row=3, column=1, padx=0, pady=(10, 10), sticky="w")
        self.color_preview_new = customtkinter.CTkCanvas(self.new_values_frame, width=15, height=15)
        self.color_preview_new.grid(row=3, column=1, sticky="w", padx=(150, 0), pady=(10, 10))
        self.color_preview_new.configure(bg=self.event_color_to.get('Lavender'))
        
        # date
        self.date_frame = customtkinter.CTkFrame(self, width=400)
        self.date_frame.grid(row=2, column=1, padx=(50, 50), pady=10, sticky="nsew")
        self.date_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_date_frame = customtkinter.CTkLabel(master=self.date_frame, text="Date Interval")
        self.label_date_frame.grid(row=0, column=0, columnspan=3, padx=0, pady=10, sticky="ew")
        self.label_date_from = customtkinter.CTkLabel(self.date_frame, text="From:")
        self.label_date_from.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_date_from = customtkinter.CTkEntry(self.date_frame, placeholder_text="yyyy-mm-dd hh:mm")
        self.entry_date_from.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        self.entry_date_button = customtkinter.CTkButton(self.date_frame, text="", width=10, image=calendar_image, command=lambda: self.date_picker(1))
        self.entry_date_button.grid(row=1, column=2, padx=0, pady=10, sticky="w")
        self.label_date_to = customtkinter.CTkLabel(self.date_frame, text="To:")
        self.label_date_to.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_date_to = customtkinter.CTkEntry(self.date_frame, placeholder_text="yyyy-mm-dd hh:mm")
        self.entry_date_to.grid(row=2, column=1, padx=0, pady=10, sticky="ew")
        self.entry_date_button2 = customtkinter.CTkButton(self.date_frame, text="", width=10, image=calendar_image, command=lambda: self.date_picker(2))
        self.entry_date_button2.grid(row=2, column=2, padx=0, pady=10, sticky="w")
        self.label_timezone = customtkinter.CTkLabel(self.date_frame, text="Timezone:")
        self.label_timezone.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.timezone_selection = customtkinter.CTkComboBox(self.date_frame, state="readonly", values=list(self.timezone), command=self.combobox_callback)
        self.timezone_selection.set(self.main_class.get_timezone())
        self.timezone_selection.grid(row=3, column=1, padx=0, pady=(10, 10), sticky="nsew")
        
        # edit button
        self.edit_button = customtkinter.CTkButton(self, image=edit_image, text="Edit", border_width=2, command=self.edit_event)
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
        self.log_box = customtkinter.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=4, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def date_picker(self, type):
        self.date_picker_window = self.main_class.date_picker_window(type, self.date_picker_window, self.entry_date_from, self.entry_date_to, self.log_box)
    
    def edit_event(self):
        events = None
        
        # get values OLD
        summary_old = self.entry_summary_old.get()
        description_old = self.entry_description_old.get('0.0', tkinter.END)
        color_index_old = self.main_class.get_color_id(self.event_color_from, self.multi_selection_old.get())  # get color index
        
        # get values NEW
        summary_new = self.entry_summary_new.get()
        description_new = self.entry_description_new.get('0.0', tkinter.END)
        color_index_new = self.main_class.get_color_id(self.event_color_to, self.multi_selection_new.get())  # get color index
        
        # check errors
        if summary_old is None or len(summary_old) == 0:
            self.main_class.write_log(self.log_box, f"ERROR: summary is missing")
            return
        if summary_new is None or len(summary_new) == 0:
            self.main_class.write_log(self.log_box, f"ERROR: summary is missing")
            return
        
        # date
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        try:
            if len(date_from) != 0:
                date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M')
            if len(date_to) != 0:
                date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M')
        except ValueError:
            self.main_class.write_log(self.log_box, f"Error on creating event: date format is not correct")
            
        time_zone = self.timezone_selection.get()
        
        # update preferred TimeZone
        self.main_class.set_timezone(time_zone)
            
        try:
            events = gc.GoogleCalendarEventsManager.editEvent(self.main_class.get_credentials(), summary_old, description_old, color_index_old, summary_new, description_new, color_index_new, date_from, date_to, time_zone)
            
            if events == None or len(events) == 0:
                self.main_class.write_log(self.log_box, f"No events obtained")
            else:
                self.main_class.write_log(self.log_box, f"{len(events)} Event(s) edited succesfully!")
        except FileNotFoundError as file_not_found_error:
            self.main_class.messagebox_exception(file_not_found_error)
            self.main_class.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            self.main_class.messagebox_exception(permission_error)
            self.main_class.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except ValueError as value_error:
            self.main_class.messagebox_exception(value_error)
            self.main_class.write_log(self.log_box, f"Value error: {str(value_error)}")
        except Exception as error:
            self.main_class.messagebox_exception(error)
            self.main_class.write_log(self.log_box, f"Generic error: {str(error)}")
    
    def combobox_callback(self, color):
        self.color_preview.configure(bg=self.event_color.get(color))
        self.main_class.write_log(self.log_box, f"color '{color}' selected")
    
    def combobox_callback_color1(self, color):
        self.color_preview_old.configure(bg=self.event_color_from.get(color))
        self.main_class.write_log(self.log_box, f"color '{color}' selected")
    
    def combobox_callback_color2(self, color):
        self.color_preview_new.configure(bg=self.event_color_to.get(color))
        self.main_class.write_log(self.log_box, f"color '{color}' selected")
    
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsFrame)
    
    def go_to_graph_frame(self):
        self.main_class.show_frame(GraphFrame)
#?###########################################################

#?###########################################################
#? TODO: add list of flag to choose what you want to obtain from the event (ex: location, participants, ecc...)
class GetEventsFrame(customtkinter.CTkFrame):
    main_class = None
    toplevel_window = None
    toplevel_entry_window = None
    date_picker_window = None
    file_viewer_window = None
    data = None
    events = None
    event_color = {"Lavender": "#7986cb", "Sage": "#33b679", "Grape": "#8e24aa", "Flamingo": "#e67c73", "Banana": "#f6bf26", "Tangerine": "#f4511e", "Peacock": "#039be5", "Graphite": "#616161", "Blueberry": "#3f51b5", "Basil": "#0b8043", "Tomato": "#d50000", "No Color Filtering": ""}
    timezone = ['Africa/Abidjan', 'Africa/Accra', 'Africa/Algiers', 'Africa/Bissau', 'Africa/Cairo', 'Africa/Casablanca', 'Africa/Ceuta', 'Africa/El_Aaiun', 'Africa/Juba', 'Africa/Khartoum', 'Africa/Lagos', 'Africa/Maputo', 'Africa/Monrovia', 'Africa/Nairobi', 'Africa/Ndjamena', 'Africa/Sao_Tome', 'Africa/Tripoli', 'Africa/Tunis', 'Africa/Windhoek', 'America/Adak', 'America/Anchorage', 'America/Araguaina', 'America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia', 'America/Asuncion', 'America/Atikokan', 'America/Bahia', 'America/Bahia_Banderas', 'America/Barbados', 'America/Belem', 'America/Belize', 'America/Blanc-Sablon', 'America/Boa_Vista', 'America/Bogota', 'America/Boise', 'America/Cambridge_Bay', 'America/Campo_Grande', 'America/Cancun', 'America/Caracas', 'America/Cayenne', 'America/Chicago', 'America/Chihuahua', 'America/Costa_Rica', 'America/Creston', 'America/Cuiaba', 'America/Curacao', 'America/Danmarkshavn', 'America/Dawson', 'America/Dawson_Creek', 'America/Denver', 'America/Detroit', 'America/Edmonton', 'America/Eirunepe', 'America/El_Salvador', 'America/Fort_Nelson', 'America/Fortaleza', 'America/Glace_Bay', 'America/Godthab', 'America/Goose_Bay', 'America/Grand_Turk', 'America/Guatemala', 'America/Guayaquil', 'America/Guyana', 'America/Halifax', 'America/Havana', 'America/Hermosillo', 'America/Indiana/Indianapolis', 'America/Indiana/Knox', 'America/Indiana/Marengo', 'America/Indiana/Petersburg', 'America/Indiana/Tell_City', 'America/Indiana/Vevay', 'America/Indiana/Vincennes', 'America/Indiana/Winamac', 'America/Inuvik', 'America/Iqaluit', 'America/Jamaica', 'America/Juneau', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Kralendijk', 'America/La_Paz', 'America/Lima', 'America/Los_Angeles', 'America/Louisville', 'America/Lower_Princes', 'America/Maceio', 'America/Managua', 'America/Manaus', 'America/Marigot', 'America/Martinique', 'America/Matamoros', 'America/Mazatlan', 'America/Menominee', 'America/Merida', 'America/Metlakatla', 'America/Mexico_City', 'America/Miquelon', 'America/Moncton', 'America/Monterrey', 'America/Montevideo', 'America/Montreal', 'America/Montserrat', 'America/Nassau', 'America/New_York', 'America/Nipigon', 'America/Nome', 'America/Noronha', 'America/North_Dakota/Beulah', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Nuuk', 'America/Ojinaga', 'America/Panama', 'America/Pangnirtung', 'America/Paramaribo', 'America/Phoenix', 'America/Port-au-Prince', 'America/Port_of_Spain', 'America/Porto_Acre', 'America/Porto_Velho', 'America/Puerto_Rico', 'America/Punta_Arenas', 'America/Rainy_River', 'America/Rankin_Inlet', 'America/Recife', 'America/Regina', 'America/Resolute', 'America/Rio_Branco', 'America/Santarem', 'America/Santiago', 'America/Santo_Domingo', 'America/Sao_Paulo', 'America/Scoresbysund', 'America/Sitka', 'America/St_Barthelemy', 'America/St_Johns', 'America/St_Kitts', 'America/St_Lucia', 'America/St_Thomas', 'America/St_Vincent', 'America/Swift_Current', 'America/Tegucigalpa', 'America/Thule', 'America/Thunder_Bay', 'America/Tijuana', 'America/Toronto', 'America/Tortola', 'America/Vancouver', 'America/Whitehorse', 'America/Winnipeg', 'America/Yakutat', 'America/Yellowknife', 'Antarctica/Casey', 'Antarctica/Davis', 'Antarctica/DumontDUrville', 'Antarctica/Macquarie', 'Antarctica/Mawson', 'Antarctica/McMurdo', 'Antarctica/Palmer', 'Antarctica/Rothera', 'Antarctica/Syowa', 'Antarctica/Troll', 'Antarctica/Vostok', 'Arctic/Longyearbyen', 'Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau', 'Asia/Aqtobe', 'Asia/Ashgabat', 'Asia/Atyrau', 'Asia/Baghdad', 'Asia/Bahrain', 'Asia/Baku', 'Asia/Bangkok', 'Asia/Barnaul', 'Asia/Beirut', 'Asia/Bishkek', 'Asia/Brunei', 'Asia/Chita', 'Asia/Choibalsan', 'Asia/Colombo', 'Asia/Damascus', 'Asia/Dhaka', 'Asia/Dili', 'Asia/Dubai', 'Asia/Dushanbe', 'Asia/Famagusta', 'Asia/Gaza', 'Asia/Hebron', 'Asia/Ho_Chi_Minh', 'Asia/Hong_Kong', 'Asia/Hovd', 'Asia/Irkutsk', 'Asia/Istanbul', 'Asia/Jakarta', 'Asia/Jayapura', 'Asia/Jerusalem', 'Asia/Kabul', 'Asia/Kamchatka', 'Asia/Karachi', 'Asia/Kathmandu', 'Asia/Khandyga', 'Asia/Kolkata', 'Asia/Krasnoyarsk', 'Asia/Kuala_Lumpur', 'Asia/Kuching', 'Asia/Kuwait', 'Asia/Macau', 'Asia/Magadan', 'Asia/Makassar', 'Asia/Manila', 'Asia/Muscat', 'Asia/Nicosia', 'Asia/Novokuznetsk', 'Asia/Novosibirsk', 'Asia/Omsk', 'Asia/Oral', 'Asia/Phnom_Penh', 'Asia/Pontianak', 'Asia/Pyongyang', 'Asia/Qatar', 'Asia/Qostanay', 'Asia/Qyzylorda', 'Asia/Riyadh', 'Asia/Sakhalin', 'Asia/Samarkand', 'Asia/Seoul', 'Asia/Shanghai', 'Asia/Singapore', 'Asia/Srednekolymsk', 'Asia/Taipei', 'Asia/Tashkent', 'Asia/Tbilisi', 'Asia/Tehran', 'Asia/Thimphu', 'Asia/Tokyo', 'Asia/Tomsk', 'Asia/Ulaanbaatar', 'Asia/Urumqi', 'Asia/Ust-Nera', 'Asia/Vientiane', 'Asia/Vladivostok', 'Asia/Yakutsk', 'Asia/Yangon', 'Asia/Yekaterinburg', 'Asia/Yerevan', 'Atlantic/Azores', 'Atlantic/Bermuda', 'Atlantic/Canary', 'Atlantic/Cape_Verde', 'Atlantic/Faroe', 'Atlantic/Madeira', 'Atlantic/Reykjavik', 'Atlantic/South_Georgia', 'Atlantic/St_Helena', 'Atlantic/Stanley', 'Australia/Adelaide', 'Australia/Brisbane', 'Australia/Broken_Hill', 'Australia/Currie', 'Australia/Darwin', 'Australia/Eucla', 'Australia/Hobart', 'Australia/Lindeman', 'Australia/Lord_Howe', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Sydney', 'Canada/Atlantic', 'Canada/Central', 'Canada/Eastern', 'Canada/Mountain', 'Canada/Newfoundland', 'Canada/Pacific', 'Europe/Amsterdam', 'Europe/Andorra', 'Europe/Astrakhan', 'Europe/Athens', 'Europe/Belgrade', 'Europe/Berlin', 'Europe/Bratislava', 'Europe/Brussels', 'Europe/Bucharest', 'Europe/Budapest', 'Europe/Busingen', 'Europe/Chisinau', 'Europe/Copenhagen', 'Europe/Dublin', 'Europe/Gibraltar', 'Europe/Guernsey', 'Europe/Helsinki', 'Europe/Isle_of_Man', 'Europe/Istanbul', 'Europe/Jersey', 'Europe/Kaliningrad', 'Europe/Kiev', 'Europe/Kirov', 'Europe/Lisbon', 'Europe/Ljubljana', 'Europe/London', 'Europe/Luxembourg', 'Europe/Madrid', 'Europe/Malta', 'Europe/Mariehamn', 'Europe/Minsk', 'Europe/Monaco', 'Europe/Moscow', 'Europe/Oslo', 'Europe/Paris', 'Europe/Podgorica', 'Europe/Prague', 'Europe/Riga', 'Europe/Rome', 'Europe/Samara', 'Europe/San_Marino', 'Europe/Sarajevo', 'Europe/Saratov', 'Europe/Simferopol', 'Europe/Skopje', 'Europe/Sofia', 'Europe/Stockholm', 'Europe/Tallinn', 'Europe/Tirane', 'Europe/Ulyanovsk', 'Europe/Uzhgorod', 'Europe/Vaduz', 'Europe/Vatican', 'Europe/Vienna', 'Europe/Vilnius', 'Europe/Volgograd', 'Europe/Warsaw', 'Europe/Zagreb', 'Europe/Zaporozhye', 'Europe/Zurich', 'GMT', 'Indian/Antananarivo', 'Indian/Chagos', 'Indian/Christmas', 'Indian/Cocos', 'Indian/Comoro', 'Indian/Kerguelen', 'Indian/Mahe', 'Indian/Maldives', 'Indian/Mauritius', 'Indian/Mayotte', 'Indian/Reunion', 'Pacific/Apia', 'Pacific/Auckland', 'Pacific/Bougainville', 'Pacific/Chatham', 'Pacific/Chuuk', 'Pacific/Easter', 'Pacific/Efate', 'Pacific/Enderbury', 'Pacific/Fakaofo', 'Pacific/Fiji', 'Pacific/Funafuti', 'Pacific/Galapagos', 'Pacific/Gambier', 'Pacific/Guadalcanal', 'Pacific/Guam', 'Pacific/Honolulu', 'Pacific/Kiritimati', 'Pacific/Kosrae', 'Pacific/Kwajalein', 'Pacific/Majuro', 'Pacific/Marquesas', 'Pacific/Midway', 'Pacific/Nauru', 'Pacific/Niue', 'Pacific/Norfolk', 'Pacific/Noumea', 'Pacific/Pago_Pago', 'Pacific/Palau', 'Pacific/Pitcairn', 'Pacific/Pohnpei', 'Pacific/Port_Moresby', 'Pacific/Rarotonga', 'Pacific/Saipan', 'Pacific/Tahiti', 'Pacific/Tarawa', 'Pacific/Tongatapu', 'Pacific/Wake', 'Pacific/Wallis', 'UTC']
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # load images
        calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        self.folder_image = tkinter.PhotoImage(file='./imgs/folder.png')
        file_image = tkinter.PhotoImage(file='./imgs/file.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Other Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, image=plus_image, text="New Events", command=self.go_to_new_events_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, image=edit_image, text="Edit Events", command=self.go_to_edit_events_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, image=list_image, text="Get Events List", command=self.go_to_get_events_by_title_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, image=chart_image, text="Graph", command=self.go_to_graph_frame)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.google_calendar_link = customtkinter.CTkButton(self.sidebar_frame, image=google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/'))
        self.google_calendar_link.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # create main panel
        self.title_label_main = customtkinter.CTkLabel(self, text="Get Events List", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label_main.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")
        
        #? TODO: add like mode check box
        #? TODO: add option to update the previus get list with the new list
        # main entry
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="ew")
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_id = customtkinter.CTkLabel(self.main_frame, text="ID:")
        self.label_id.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_id = customtkinter.CTkEntry(self.main_frame, placeholder_text="id")
        self.entry_id.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        self.label_summary = customtkinter.CTkLabel(self.main_frame, text="Summary:")
        self.label_summary.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_summary = customtkinter.CTkEntry(self.main_frame, placeholder_text="summary")
        self.entry_summary.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        self.label_description = customtkinter.CTkLabel(self.main_frame, text="Description:")
        self.label_description.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_description = customtkinter.CTkTextbox(self.main_frame, width=250, height=100)
        self.entry_description.grid(row=2, column=1, padx=(0, 0), pady=(10, 0), sticky="ew")
        self.label_color = customtkinter.CTkLabel(self.main_frame, text="Color:")
        self.label_color.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")
        self.multi_selection = customtkinter.CTkComboBox(self.main_frame, state="readonly", values=list(self.event_color.keys()), command=self.combobox_callback)
        self.multi_selection.set("No Color Filtering")
        self.multi_selection.grid(row=3, column=1, padx=0, pady=(10, 10), sticky="w")
        self.color_preview = customtkinter.CTkCanvas(self.main_frame, width=15, height=15)
        self.color_preview.grid(row=3, column=1, sticky="w", padx=(150, 0), pady=(10, 10))
        
        # date
        self.date_frame = customtkinter.CTkFrame(self, width=400)
        self.date_frame.grid(row=2, column=1, padx=(50, 50), pady=10, sticky="nsew")
        self.date_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.label_date_frame = customtkinter.CTkLabel(master=self.date_frame, text="Date Interval")
        self.label_date_frame.grid(row=0, column=0, columnspan=3, padx=0, pady=10, sticky="ew")
        self.label_date_from = customtkinter.CTkLabel(self.date_frame, text="From:")
        self.label_date_from.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_date_from = customtkinter.CTkEntry(self.date_frame, placeholder_text="yyyy-mm-dd hh:mm")
        self.entry_date_from.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        self.entry_date_button = customtkinter.CTkButton(self.date_frame, text="", width=10, image=calendar_image, command=lambda: self.date_picker(1))
        self.entry_date_button.grid(row=1, column=2, padx=0, pady=10, sticky="w")
        self.label_date_to = customtkinter.CTkLabel(self.date_frame, text="To:")
        self.label_date_to.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_date_to = customtkinter.CTkEntry(self.date_frame, placeholder_text="yyyy-mm-dd hh:mm")
        self.entry_date_to.grid(row=2, column=1, padx=0, pady=10, sticky="ew")
        self.entry_date_button2 = customtkinter.CTkButton(self.date_frame, text="", width=10, image=calendar_image, command=lambda: self.date_picker(2))
        self.entry_date_button2.grid(row=2, column=2, padx=0, pady=10, sticky="w")
        self.label_timezone = customtkinter.CTkLabel(self.date_frame, text="Timezone:")
        self.label_timezone.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.timezone_selection = customtkinter.CTkComboBox(self.date_frame, state="readonly", values=list(self.timezone), command=self.combobox_callback)
        self.timezone_selection.set(self.main_class.get_timezone())
        self.timezone_selection.grid(row=3, column=1, padx=0, pady=(10, 10), sticky="nsew")

        # file output
        self.file_output_frame = customtkinter.CTkFrame(self, width=400)
        self.file_output_frame.grid(row=3, column=1, padx=(50, 50), pady=10, sticky="nsew")
        self.file_output_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.title_label_file = customtkinter.CTkLabel(master=self.file_output_frame, text="Save results to file")
        self.title_label_file.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="s")
        self.file_path = customtkinter.CTkEntry(master=self.file_output_frame, placeholder_text="file path")
        self.file_path.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        self.button_file_path = customtkinter.CTkButton(self.file_output_frame, text="", width=10, image=self.folder_image, command=lambda: self.get_file_path(self.file_path))
        self.button_file_path.grid(row=1, column=2, padx=0, pady=10, sticky="w")
        self.button_open_file = customtkinter.CTkButton(master=self.file_output_frame, image=file_image, text="open", command=self.open_file)
        self.button_open_file.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="s")

        # get list button
        self.get_button = customtkinter.CTkButton(self, image=list_image, text="Get", border_width=2, command=self.get_events)
        self.get_button.grid(row=4, column=1, padx=20, pady=20)
        
        # Tooltips
        CTkToolTip(self.entry_id, delay=0.3, message="(Optional) Enter event id This is a very specific field;\n if you want to get a specific event and you know the specific event id, you can enter it and ignore the fields below.\n Otherwise you can ignore it and proceed to fill in the other fields.")
        CTkToolTip(self.entry_summary, delay=0.3, message="(Optional) Insert event title")
        CTkToolTip(self.entry_description, delay=0.3, message="(Optional) Insert the event description")
        CTkToolTip(self.multi_selection, delay=0.3, message="(Optional) Choose event color")
        CTkToolTip(self.entry_date_from, delay=0.3, message="(Optional) Enter date from")
        CTkToolTip(self.entry_date_to, delay=0.3, message="(Optional) Enter date to")
        CTkToolTip(self.timezone_selection, delay=0.3, message="(Optional) Choose time zone")
        CTkToolTip(self.file_path, delay=0.3, message="(Optional) Enter the path to the file;\n if you want to save the results to a specific file (.csv, .txt)")
        CTkToolTip(self.button_open_file, delay=0.3, message="Open file preview")
        CTkToolTip(self.get_button, delay=0.3, message="Get events")
        
        # create log textbox
        self.log_box = customtkinter.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=5, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def get_events(self):
        self.events = None
        
        id = self.entry_id.get()
        if len(id) != 0:
            try: 
                self.events = gc.GoogleCalendarEventsManager.getEventByID(self.main_class.get_credentials(), id)
                self.events_list_viewer_window()
                self.main_class.write_log(self.log_box, f"Event obtained succesfully!")
                return
            except FileNotFoundError as file_not_found_error:
                self.main_class.messagebox_exception(file_not_found_error)
                self.main_class.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
            except PermissionError as permission_error:
                self.main_class.messagebox_exception(permission_error)
                self.main_class.write_log(self.log_box, f"Permission error: {str(permission_error)}")
            except ValueError as value_error:
                self.main_class.messagebox_exception(value_error)
                self.main_class.write_log(self.log_box, f"Value error: {str(value_error)}")
            except Exception as error:
                self.main_class.messagebox_exception(error)
                self.main_class.write_log(self.log_box, f"Generic error: {str(error)}")
        
        summary = self.entry_summary.get()
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        description = self.entry_description.get("0.0", tkinter.END).replace('\n', '')
        time_zone = self.timezone_selection.get()
        
        # update preferred TimeZone
        self.main_class.set_timezone(time_zone)
         
        try:
            if len(date_from) != 0:
                date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M')
            if len(date_to) != 0:
                date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M')
        except ValueError:
            self.main_class.write_log(self.log_box, f"Error on creating event: date format is not correct")
        
        # get color index
        color_index = self.main_class.get_color_id(self.event_color, self.multi_selection.get())
        
        try: 
            self.events = gc.GoogleCalendarEventsManager.getEvents(creds=self.main_class.get_credentials(), title=summary, start_date=date_from, end_date=date_to, color_id=color_index, description=description, time_zone=time_zone)
            if self.events == None or len(self.events) == 0:
                self.main_class.write_log(self.log_box, f"No events obtained")
                return
            
            self.events_list_viewer_window() # i have to truncate the list for performances reason
            self.main_class.write_log(self.log_box, f"{len(self.events)} Event(s) obtained succesfully!")
        except FileNotFoundError as file_not_found_error:
            self.main_class.messagebox_exception(file_not_found_error)
            self.main_class.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            self.main_class.messagebox_exception(permission_error)
            self.main_class.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except ValueError as value_error:
            self.main_class.messagebox_exception(value_error)
            self.main_class.write_log(self.log_box, f"Value error: {str(value_error)}")
        # except GoogleCalendarConnectionError as connection_error:
        #     self.main_class.messagebox_exception(connection_error)
        #     self.main_class.write_log(self.log_box, f"Connection error: {str(connection_error)}")
        # except GoogleCalendarAPIError as api_error:
        #     self.main_class.messagebox_exception(api_error)
        #     self.main_class.write_log(self.log_box, f"Google Calendar API error: {str(api_error)}")
        except Exception as error:
            self.main_class.messagebox_exception(error)
            self.main_class.write_log(self.log_box, f"Generic error: {str(error)}")
    
    def events_list_viewer_window(self):  
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = customtkinter.CTkToplevel()
            self.toplevel_window.title(f'{len(self.events)} Event(s) obtained')

            # Create a grid inside the toplevel window
            self.toplevel_window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically
            self.toplevel_window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
            self.toplevel_window.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally
            
            event_list_file_viewer = customtkinter.CTkTextbox(self.toplevel_window)
            event_list_file_viewer.bind("<Key>", lambda e: "break")  # set the textbox readonly
            event_list_file_viewer.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10), sticky="nsew")
            
            button_save = customtkinter.CTkButton(self.toplevel_window, text="Save results", command=lambda: self.get_filepath_to_save_results())
            button_save.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")
            
            button_cancel = customtkinter.CTkButton(self.toplevel_window, text="Cancel", command=lambda: self.close_top_frame_window())
            button_cancel.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="nsew")
             
            event_list_file_viewer.delete(1.0, tkinter.END)

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
            
            # print event after event
            for event in events_info:
                event_info_str = f"INDEX: {event['index']} | ID: {event['ID']} | SUMMARY: {event['summary']} | START: {event['start']} | END: {event['end']} | DURATION: {event['duration']}\n"
                event_list_file_viewer.insert(tkinter.END, event_info_str)
    
            self.toplevel_window.attributes("-topmost", True) # focus to this windows
        else:
            self.toplevel_window.focus()  # if window exists focus it
        
        return self.toplevel_window
    
    def get_filepath_to_save_results(self):
        
        if self.file_path != None and len(self.file_path.get()) != 0:
            self.save_results_to_file() 
            return
        
        if self.toplevel_entry_window is None or not self.toplevel_entry_window.winfo_exists():
            
            self.toplevel_entry_window = customtkinter.CTkToplevel()
            self.toplevel_entry_window.title('Select a file to save the results')
            self.toplevel_entry_window.geometry("350x50")
            entry = customtkinter.CTkEntry(self.toplevel_entry_window, width=250, placeholder_text="file path")
            entry.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="nsew")
            button_add_filepath = customtkinter.CTkButton(self.toplevel_entry_window, width=10, text="", image=self.folder_image, command=lambda: self.get_file_path(entry))
            button_add_filepath.grid(row=0, column=1, padx=5, pady=(10, 10), sticky="nsew")
            button_ok = customtkinter.CTkButton(self.toplevel_entry_window, width=10, text="Ok", command=lambda: self.save_results_to_file2(entry))
            button_ok.grid(row=0, column=2, padx=5, pady=(10, 10), sticky="nsew") 
                
            self.toplevel_entry_window.resizable(False, False)
            self.toplevel_entry_window.attributes("-topmost", False) # focus to this windows
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
            
            self.main_class.write_log(self.log_box, f"{counter} event(s) added to file {self.file_path.get()}")
            
        except FileNotFoundError as file_not_found_error:
            self.main_class.messagebox_exception(file_not_found_error)
            self.main_class.write_log(self.log_box, f"File not found error: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            self.main_class.messagebox_exception(permission_error)
            self.main_class.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except ValueError as value_error:
            self.main_class.messagebox_exception(value_error)
            self.main_class.write_log(self.log_box, f"Value error: {str(value_error)}")
        except KeyError as key_error:
            self.main_class.messagebox_exception(key_error)
            self.main_class.write_log(self.log_box, f"Key error: {str(key_error)}")
        except Exception as error:
            self.main_class.messagebox_exception(error)
            self.main_class.write_log(self.log_box, f"Generic error: {str(error)}")
    
    def save_results_to_file2(self, entry):
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", entry.get())
        
        self.save_results_to_file()
    
    def close_top_frame_window(self):
        self.toplevel_window.destroy()
        
    def close_top_frame_entry_window(self):
        self.toplevel_entry_window.destroy()
        
    def combobox_callback(self, color):
        self.color_preview.configure(bg=self.event_color.get(color))
        self.main_class.write_log(self.log_box, f"color '{color}' selected")
    
    def get_file_path(self, entry):
        self.main_class.get_file_path(self.log_box, entry)
    
    def set_logbox_text(self, text):
        self.log_box.delete("0.0", tkinter.END)
        self.log_box.insert("0.0", text)
    
    def open_file(self):
        self.file_viewer_window = self.main_class.file_viewer_window(self.file_viewer_window, self.file_path.get(), self.log_box)
    
    def date_picker(self, type):
        self.date_picker_window = self.main_class.date_picker_window(type, self.date_picker_window, self.entry_date_from, self.entry_date_to, self.log_box)

    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsFrame)
        
    def go_to_graph_frame(self):
        self.main_class.show_frame(GraphFrame)
#?###########################################################

#?###########################################################
class GraphFrame(customtkinter.CTkFrame):
    main_class = None
    date_picker_window = None
    file_viewer_window = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # load images
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        folder_image = tkinter.PhotoImage(file='./imgs/folder.png')
        file_image = tkinter.PhotoImage(file='./imgs/file.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Other Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, image=plus_image, text="New Events", command=self.go_to_new_events_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, image=edit_image, text="Edit Events", command=self.go_to_edit_events_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, image=list_image, text="Get Events List", command=self.go_to_get_events_by_title_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, image=chart_image, text="Graph", command=self.go_to_graph_frame)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.google_calendar_link = customtkinter.CTkButton(self.sidebar_frame, image=google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/'))
        self.google_calendar_link.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # create main panel
        self.title_label_main = customtkinter.CTkLabel(self, text="Create Graph", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label_main.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")
        
        # file output
        self.file_output_frame = customtkinter.CTkFrame(self, width=400)
        self.file_output_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="nsew")
        self.file_output_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.file_output_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.file_label = customtkinter.CTkLabel(self.file_output_frame, text="Set file path")
        self.file_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 10), sticky="nsew")
        self.file_path = customtkinter.CTkEntry(master=self.file_output_frame, placeholder_text="file path")
        self.file_path.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
        self.button_file_path = customtkinter.CTkButton(self.file_output_frame, text="", width=10, image=folder_image, command=self.get_file_path)
        self.button_file_path.grid(row=1, column=2, padx=0, pady=10, sticky="w")
        self.button_open_file = customtkinter.CTkButton(master=self.file_output_frame, image=file_image, text="open", command=self.open_file)
        self.button_open_file.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="n")

        # Generate Graph Button
        self.graph_button = customtkinter.CTkButton(self, command=self.generate_graph, image=chart_image, border_width=2, text="Generate")
        self.graph_button.grid(row=4, column=1, padx=20, pady=20)
        
        # Tooltips
        CTkToolTip(self.file_path, delay=0.3, message="(Required) Enter the path to the file you generated from the 'Get Events List' section.")
        CTkToolTip(self.button_open_file, delay=0.3, message="Open file preview")
        CTkToolTip(self.graph_button, delay=0.3, message="Generate graphs")
        
        # create log textbox
        self.log_box = customtkinter.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=5, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def combobox_callback(self, color):
        self.color_preview.configure(bg=self.event_color.get(color))
        self.main_class.write_log(self.log_box, f"color '{color}' selected")
    
    def get_file_path(self):
        file_path = filedialog.askopenfilename(title="Select file where do you want to save data", filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")))
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", file_path)
        self.main_class.write_log(self.log_box, f"file '{file_path}' selected")
    
    def set_logbox_text(self, text):
        self.log_box.delete("0.0", tkinter.END)
        self.log_box.insert("0.0", text)
    
    def open_file(self):
        self.file_viewer_window = self.main_class.file_viewer_window(self.file_viewer_window, self.file_path.get(), self.log_box)
    
    def date_picker(self, type):
        self.date_picker_window = self.main_class.date_picker_window(type, self.date_picker_window, self.entry_date_from, self.entry_date_to, self.log_box)
    
    def generate_graph(self):
        if self.main_class.check_file_path_errors(self.log_box, self.file_path.get()): return  
        
        try:
            self.main_class.write_log(self.log_box, "Generating chart")
            data = Plotter.Plotter.loadData(self.file_path.get())
            Plotter.Plotter.graph(data)
        except FileNotFoundError:
            self.main_class.write_log(self.log_box, f"Error, the file '{self.file_path.get()}' doesn't exist")
            return
        except pandas.errors.EmptyDataError:
            self.main_class.write_log(self.log_box, f"Error, the file '{self.file_path.get()}' is empty")
            return
        except PermissionError as permission_error:
            self.main_class.messagebox_exception(permission_error)
            self.main_class.write_log(self.log_box, f"Permission error: {str(permission_error)}")
        except ValueError as value_error:
            self.main_class.messagebox_exception(value_error)
            self.main_class.write_log(self.log_box, f"Value error: {str(value_error)}")
        # except Plotter.PlotterError as plotter_error:
        #     # Replace 'PlotterError' with the actual custom exception class from your Plotter module
        #     self.main_class.messagebox_exception(plotter_error)
        #     self.main_class.write_log(self.log_box, f"Plotter error: {str(plotter_error)}")
        except Exception as error:
            self.main_class.messagebox_exception(error)
            self.main_class.write_log(self.log_box, f"Generic error: {str(error)}")
    
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsFrame)
        
    def go_to_graph_frame(self):
        self.main_class.show_frame(GraphFrame)
#?###########################################################

#?###########################################################
class MainFrame(customtkinter.CTkFrame):
    
    main_class = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # load images
        plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        list_image = tkinter.PhotoImage(file='./imgs/list.png')
        edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        chart_image = tkinter.PhotoImage(file='./imgs/chart.png')
        donation_image = tkinter.PhotoImage(file='./imgs/donation.png')
        github_image = tkinter.PhotoImage(file='./imgs/github.png')
        icon = tkinter.PhotoImage(file='./imgs/icon.png')
    
        # custom font
        #! TODO: set custom font
        title_font = customtkinter.CTkFont(family="Georgia", weight='bold', slant='italic', size=45)
        
        # main
        customtkinter.CTkLabel(self, text="", image=icon, fg_color="transparent").pack(padx=20, pady=(50, 20))
        customtkinter.CTkLabel(self, text="Google Calendar Data Manager", font=title_font, text_color='#e06c29', fg_color="transparent").pack(padx=20, pady=50)
        #customtkinter.CTkLabel(self, text="Choose the action", fg_color="transparent", font=("Arial", 32)).pack(padx=20, pady=20)
        customtkinter.CTkButton(master=self, image=plus_image, text="New Events", command=self.go_to_new_events_frame).pack(padx=20, pady=10, anchor='center')
        customtkinter.CTkButton(master=self, image=edit_image, text="Edit Events", command=self.go_to_edit_events_frame).pack(padx=20, pady=10, anchor='center')
        customtkinter.CTkButton(master=self, image=list_image, text="Get Events", command=self.go_to_get_events_by_title_frame).pack(padx=20, pady=10, anchor='center')
        customtkinter.CTkButton(master=self, image=chart_image, text="Graph", command=self.go_to_graph_frame).pack(padx=20, pady=10, anchor='center')
        
        customtkinter.CTkButton(master=self, image=github_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open('https://github.com/DennisTurco/Google-Calendar-Data-Manager')).pack(padx=20, pady=10, anchor='sw')
        customtkinter.CTkButton(master=self, image=donation_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open('https://www.buymeacoffee.com/denno')).pack(padx=20, pady=10, anchor='sw')
        
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsFrame)
        
    def go_to_graph_frame(self):
        self.main_class.show_frame(GraphFrame)
#?###########################################################

#?###########################################################   
class SetupFrame(customtkinter.CTkFrame):
    width = 900
    height = 600
    main_class = None
    toplevel_window = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # load images
        google_image = tkinter.PhotoImage(file='./imgs/google.png')
        question_image = tkinter.PhotoImage(file='./imgs/question.png')
        arrow_image = tkinter.PhotoImage(file='./imgs/arrow-right.png')
        
        # main content
        customtkinter.CTkLabel(self, text="Set Credentials", fg_color="transparent", font=("Arial", 32)).pack(padx=20, pady=20)
        customtkinter.CTkButton(master=self, image=google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/')).pack(padx=20, pady=10, anchor='center')
        customtkinter.CTkButton(master=self, image=question_image, text="Tutorial Setup", command=lambda: webbrowser.open('https://github.com/DennisTurco/Google-Calendar-Data-Manager/blob/master/docs/GoogleCloudAPISetup.md')).pack(padx=20, pady=10, anchor='center')
        customtkinter.CTkButton(master=self, image=arrow_image, text="First Setup", command=lambda: self.setCredentialsPathFrame()).pack(padx=20, pady=10, anchor='center')
    
    def setCredentialsPathFrame(self):
        folder_image = tkinter.PhotoImage(file='./imgs/folder.png')
        
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = customtkinter.CTkToplevel()
            self.toplevel_window.title('New Credentials')

            # Create a grid inside the toplevel window
            self.toplevel_window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically
            self.toplevel_window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
            self.toplevel_window.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally

            text = customtkinter.CTkLabel(self.toplevel_window, text="Insert credentials path")
            text.grid(row=0, column=0, columnspan=3, padx=20, pady=20)  # Increase columnspan to make space for button_file_path
            self.file_path = customtkinter.CTkEntry(self.toplevel_window, placeholder_text="credentials file path")
            self.file_path.grid(row=1, column=0, columnspan=2, padx=(15, 60), pady=10, sticky="nsew")
            button_file_path = customtkinter.CTkButton(self.toplevel_window, text="", width=10, image=folder_image, command=self.__getFilePath)
            button_file_path.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="e")
            button_save = customtkinter.CTkButton(self.toplevel_window, text="OK", command=self.__setCredentialsPath)
            button_save.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")
            button_cancel = customtkinter.CTkButton(self.toplevel_window, text="Cancel", command=self.toplevel_window.destroy)
            button_cancel.grid(row=2, column=1, padx=15, pady=10, sticky="nsew")
    
            self.toplevel_window.attributes("-topmost", True)
            self.toplevel_window.resizable(False, False)
        else:
            self.toplevel_window.focus()  # if window exists focus it
        
        return self.toplevel_window
    
    def __setCredentialsPath(self):
        # get response from dialog
        credentials_path = self.file_path.get()
        if len(credentials_path) == 0: return
        token_path = credentials_path.rsplit("/", 1)[0] + "/" + "token.json"
        
        self.toplevel_window.destroy()
        
        try:
            # get credentials
            credentials = gc.GoogleCalendarEventsManager.connectionSetup(credentials_path, gc.GoogleCalendarEventsManager.SCOPE, token_path)
        except Exception as error:
            self.main_class.messagebox_exception(error)
            try: os.remove(token_path) # delete token.json 
            except: pass
        
        # response message box
        if credentials is not None:
            CTkMessagebox(message="Credentials setted succeffully", icon="check", option_1="Ok")
            
            # set credentials values to main class
            self.main_class.set_credentials(credentials, credentials_path, token_path)
            
            self.main_class.show_frame(MainFrame)
        else:
            msg = CTkMessagebox(title="Credentials error", message="Do you wish to retry?", icon="cancel", option_1="No", option_2="Yes")
            response = msg.get()
            if response=="Yes":
                self.setCredentialsPathFrame()
    
    def __getFilePath(self):
        file_path = filedialog.askopenfilename(title="Select credentials file", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", file_path)
#?###########################################################

#*###########################################################
class App(): 
    root = None
    credentials_path = None
    token_path = None
    credentials = None
    
    app_width = 1100
    app_height = 900
    
    def __init__(self):
        root = customtkinter.CTk()
        self.root = root
        
        # read data from json to get path from last session
        listRes = js.JSONSettings.ReadFromJSON()
        if listRes != None:
            self.credentials_path = listRes["CredentialsPath"]
            self.token_path = listRes["TokenPath"]
            try: self.credentials = gc.GoogleCalendarEventsManager.connectionSetup(self.credentials_path, gc.GoogleCalendarEventsManager.SCOPE, self.token_path)
            except: pass
            
        self.init_window()
        self.init_menu()
        self.page_controller()
        
        self.root.mainloop()
    
    def change_scaling_event(self, new_scaling: str):
        if new_scaling == None: return
        new_scaling_float = int(new_scaling) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        js.JSONSettings.WriteTextScalingToJSON(new_scaling)
        
    def change_appearance(self, new_appearance: str):
        if new_appearance == None: return
        customtkinter.set_appearance_mode(new_appearance)
        js.JSONSettings.WriteAppearanceToJSON(new_appearance)
    
    def change_color_theme(self, color_theme: str):
        if color_theme == None: return
        customtkinter.set_default_color_theme(color_theme) 
        js.JSONSettings.WriteColorThemeToJSON(color_theme)
    
    def set_color_theme(self, color_theme: str):
        self.change_color_theme(color_theme)
        CTkMessagebox(title="Information", message="The theme color will be updated when the application is restarted")
    
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

        self.toplevel_window = customtkinter.CTkToplevel()
        self.toplevel_window.title(f'Exception traceback')

        # Create a grid inside the toplevel window
        self.toplevel_window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically
        self.toplevel_window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
        self.toplevel_window.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally

        file_viewer = customtkinter.CTkTextbox(self.toplevel_window)
        file_viewer.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10), sticky="nsew")

        button_close = customtkinter.CTkButton(self.toplevel_window, text="Close", command=self.toplevel_window.destroy)
        button_close.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")

        button_report = customtkinter.CTkButton(self.toplevel_window, text="Report Exception", command=lambda: webbrowser.open('https://github.com/DennisTurco/Google-Calendar-Data-Manager/issues'))
        button_report.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="nsew")

        # Insert text into the box
        file_viewer.delete(0.0, tkinter.END)
        file_viewer.insert(tkinter.END, str(error))

        self.toplevel_window.attributes("-topmost", False)  # Focus on this window
    
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def init_window(self):
        # configure window
        self.root.iconbitmap('./imgs/icon.ico')
        self.root.title("Google Calendar Data Manager")
        self.centerWindow()
        self.root.minsize(1100, 900)

        listRes = js.JSONSettings.ReadFromJSON()
        if listRes != None:
            try: 
                appearance = listRes["Appearence"]
                self.change_appearance(appearance)
            except: pass
            try: 
                text_scaling = listRes["TextScaling"]
                self.change_scaling_event(text_scaling)
            except: pass
            try: 
                color_theme = listRes["ColorTheme"]
                self.change_color_theme(color_theme)
            except: pass 
    
    def init_menu(self):
        menu = CTkMenuBar(self.root)
        button_1 = menu.add_cascade("File")
        button_3 = menu.add_cascade("Settings")
        button_4 = menu.add_cascade("About")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="New Credentials", command=lambda: self.show_frame(SetupFrame))
        dropdown1.add_option(option="Exit", command=lambda: exit())

        dropdown1.add_separator()

        dropdown3 = CustomDropdownMenu(widget=button_3)
        sub_menu2 = dropdown3.add_submenu("Appearance")
        sub_menu2.add_option(option="System", command=lambda: self.change_appearance("System"))
        sub_menu2.add_option(option="Dark", command=lambda: self.change_appearance("dark"))
        sub_menu2.add_option(option="Light", command=lambda: self.change_appearance("light"))
        
        sub_menu3 = dropdown3.add_submenu("Scaling")
        sub_menu3.add_option(option="120%", command=lambda: self.change_scaling_event("120"))
        sub_menu3.add_option(option="110%", command=lambda: self.change_scaling_event("110"))
        sub_menu3.add_option(option="100%", command=lambda: self.change_scaling_event("100"))
        sub_menu3.add_option(option="90%", command=lambda: self.change_scaling_event("90"))
        sub_menu3.add_option(option="80%", command=lambda: self.change_scaling_event("80"))
        sub_menu3.add_option(option="70%", command=lambda: self.change_scaling_event("70"))
        
        sub_menu4 = dropdown3.add_submenu("Theme")
        sub_menu4.add_option(option="Blue", command=lambda: self.set_color_theme("blue"))
        sub_menu4.add_option(option="Dark Blue", command=lambda: self.set_color_theme("dark-blue"))
        sub_menu4.add_option(option="Green", command=lambda: self.set_color_theme("green"))

        dropdown4 = CustomDropdownMenu(widget=button_4)
        dropdown4.add_option(option="Share", command=lambda: webbrowser.open('https://github.com/DennisTurco/Google-Calendar-Data-Manager'))
        dropdown4.add_option(option="Report a bug", command=lambda: webbrowser.open('https://github.com/DennisTurco/Google-Calendar-Data-Manager/issues'))
        dropdown4.add_option(option="Donate for this project", command=lambda: webbrowser.open('https://www.buymeacoffee.com/denno'))
        
    def centerWindow(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width / 2) - (self.app_width / 2) 
        y = (screen_height / 2) - (self.app_height / 2) 
        
        self.root.geometry(f'{self.app_width}x{self.app_height}+{int(x)}+{int(y)}')
    
    def page_controller(self):
        # creating a container
        container = customtkinter.CTkFrame(self.root) 
        container.pack(side = "top", fill = "both", expand = True) 

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)        

        # initializing frames to an empty array
        self.frames = {} 

        # iterating through a tuple consisting of the different page layouts
        for F in (SetupFrame, MainFrame, NewEventsFrame, EditEventsFrame, GetEventsFrame, GraphFrame):

            frame = F(container, self)

            # initializing frame of that object from pages for loop
            self.frames[F] = frame 

            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        if self.credentials is None or self.credentials_path is None:
            self.show_frame(SetupFrame)
        else:
            self.show_frame(MainFrame)
    
    def set_credentials(self, credentials, credentials_path, token_path):
        self.credentials = credentials
        self.credentials_path = credentials_path
        self.token_path = token_path
        js.JSONSettings.WriteCredentialsToJSON(self.credentials_path, self.token_path)
        
    def set_timezone(self, timezone):
        js.JSONSettings.WriteTimeZoneToJSON(timezone)
    
    def get_timezone(self):
        # read data from json to get path from last session
        timezone = 'UTC' # set default timezone
        listRes = js.JSONSettings.ReadFromJSON()
        if listRes != None:
            try: timezone = listRes["TimeZone"]
            except: pass
        return timezone
    
    def get_color_id(self, colors, color_selected):
        color_index = 0
        
        for idx, color in enumerate(colors.keys()):
            if color == color_selected:
                color_index = idx+1
                break
            
        # check if the color is valid (it is not setted 'No Color Filtering')
        if color_index == 12: # 'No Color Filtering' has index == 12
            color_index = -1
            
        return color_index
    
    #* TODO: add button up and down hours, minutes by one https://customtkinter.tomschimansky.com/tutorial/spinbox
    def date_picker_window(self, type, toplevel_window, entry_date_from, entry_date_to, log_box):
        if toplevel_window is None or not toplevel_window.winfo_exists():
            toplevel_window = customtkinter.CTkToplevel() # create window if its None or destroyed
            calendar = Calendar(toplevel_window)
            calendar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 
            hours = customtkinter.CTkLabel(toplevel_window, text="hours:")
            hours.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            hours = customtkinter.CTkEntry(toplevel_window, placeholder_text="hh")
            hours.grid(row=1, column=0, padx=(70, 0), pady=10, sticky="w")
            minutes = customtkinter.CTkLabel(toplevel_window, text="minutes: ")
            minutes.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            minutes = customtkinter.CTkEntry(toplevel_window, placeholder_text="mm")
            minutes.grid(row=2, column=0, padx=(70, 0), pady=10, sticky="w")
            
            # get current hour
            now = datetime.now()
            current_hour = now.strftime("%H")

            # calculate hour after one hour
            after_one_hour = now + timedelta(hours=1)
            hour_after_one_hour = after_one_hour.strftime("%H")
                
            if type == 1:
                toplevel_window.title("Date From")
                confirm_button = customtkinter.CTkButton(toplevel_window, text="Confirm", command=lambda: self.get_date(1, toplevel_window, entry_date_from, entry_date_to, log_box, calendar, hours, minutes))
                # set default hour
                hours.delete("0", tkinter.END)
                hours.insert("0", current_hour)
            elif type == 2:
                toplevel_window.title("Date To")
                confirm_button = customtkinter.CTkButton(toplevel_window, text="Confirm", command=lambda: self.get_date(2, toplevel_window, entry_date_from, entry_date_to, log_box, calendar, hours, minutes))
                # set default hour
                hours.delete("0", tkinter.END)
                hours.insert("0", hour_after_one_hour)
            else:
                raise Exception("type option doesn't exists")
            
            confirm_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew") 
            
            toplevel_window.attributes("-topmost", True) # focus to this windows
            toplevel_window.resizable(False, False)
        else:
            toplevel_window.focus()  # if window exists focus it
        
        return toplevel_window
    
    def get_date(self, type, toplevel_window, entry_date_from, entry_date_to, log_box, calendar, hours, minutes):
        date = calendar.get_date() # get the date from the calendar
        
        try:
            if len(hours.get()) == 0: hour = 0
            else: hour = int(hours.get())
            if len(minutes.get()) == 0: minute = 0
            else: minute =  int(minutes.get())
    
            if hour > 23 or hour < 0 or minute > 59 or minute < 0: return
        except ValueError:
            return
        
        # Format the datetime object as a string in "%Y-%m-%d %H:%M" format
        date = datetime.strptime(date, "%m/%d/%y")  
        full_date = datetime(date.year, date.month, date.day, hour, minute)
        full_date_str = full_date.strftime("%Y-%m-%d %H:%M")  
        
        if type == 1:
            self.write_log(log_box, "Date Selected From: " + full_date_str)
            entry_date_from.delete("0", tkinter.END)
            entry_date_from.insert("0", full_date_str)
        elif type == 2:
            self.write_log(log_box, "Date Selected To: " + full_date_str)
            entry_date_to.delete("0", tkinter.END)
            entry_date_to.insert("0", full_date_str)
        else:
            raise Exception("type option doesn't exists")
        
        toplevel_window.destroy() 
    
    def get_file_path(self, logbox, entry):
        file_path = filedialog.askopenfilename(title="Select file where do you want to save data", filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")))
        entry.delete("0", tkinter.END)
        entry.insert("0", file_path)
        self.write_log(logbox, f"file '{file_path}' selected")
        return file_path
    
    def file_viewer_window(self, toplevel_window, filepath, log_box):
        
        if self.check_file_path_errors(log_box, filepath): return
        
        if toplevel_window is None or not toplevel_window.winfo_exists():
            toplevel_window = customtkinter.CTkToplevel() # create window if its None or destroyed
            toplevel_window.title(filepath)
            file_viewer = customtkinter.CTkTextbox(toplevel_window)
            file_viewer.bind("<Key>", lambda e: "break")  # set the textbox readonly
            file_viewer.pack(fill=tkinter.BOTH, expand=True)   
            
            #insert text into box
            with open(filepath, 'r', encoding='utf-8') as file:
                file_content = file.read()
                file_viewer.delete(1.0, tkinter.END)
                file_viewer.insert(tkinter.END, file_content)
        
            toplevel_window.attributes("-topmost", True) # focus to this windows
            self.write_log(log_box, f"file '{filepath}' opened")
        else:
            toplevel_window.focus()  # if window exists focus it
        
        return toplevel_window
    
    def check_file_path_errors(self, log_box, filepath):
        if filepath is None or len(filepath) == 0:
            self.write_log(log_box, f"ERROR: file path is missing")
            return True
        
        if not os.path.exists(filepath): 
            self.write_log(log_box, f"ERROR: file '{filepath}' doesn't found")
            return True
    
    def write_log(self, log_box, message):
        log_box.insert("0.0", "\n" + str(datetime.now()) + ": " + message)

    def get_credentials(self):
        return self.credentials 

#*###########################################################

if __name__ == "__main__":
    app = App()