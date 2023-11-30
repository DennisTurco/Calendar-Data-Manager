import GoogleCalendarEventsManager as gc
import webbrowser
import JSONSettings as js
import io, subprocess, sys

import tkinter
from datetime import datetime

try:
    import customtkinter
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter
try:
    from CTkMenuBar import *
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "CTkMenuBar"])
    from CTkMenuBar import *
try:
    from CTkMessagebox import *
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "CTkMessagebox"])
    from CTkMessagebox import *
try:
    from tkcalendar import *
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "tkcalendar"])
    from tkcalendar import *    


#?###########################################################
#TODO: todo
class NewEventsFrame(customtkinter.CTkFrame):
    
    main_class = None
    toplevel_window = None
    event_color = {"Tomato": "#d50000", "Flamingo": "#e67c73", "Tangerine": "#f4511e", "Banana": "#f6bf26", "Sage": "#33b679", "Basil": "#0b8043", "Peacock": "#039be5", "Blueberry": "#3f51b5", "Lavender": "#7986cb", "Wine": "#8e24aa", "Graphite": "#616161"}
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
                
        # load images
        self.calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        self.google_image = tkinter.PhotoImage(file='./imgs/google.png')
        self.plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        self.list_image = tkinter.PhotoImage(file='./imgs/list.png')
        self.edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Other Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, image=self.plus_image, text="New Events", command=self.go_to_new_events_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, image=self.edit_image, text="Edit Events", command=self.go_to_edit_events_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, image=self.list_image, text="Get Events List", command=self.go_to_get_events_by_title_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.google_calendar_link = customtkinter.CTkButton(self.sidebar_frame, image=self.google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/'))
        self.google_calendar_link.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # create main panel
        self.title_label_main = customtkinter.CTkLabel(self, text="Create New Event", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label_main.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")
        
        # main entry
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=1, column=1, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.entry_summary = customtkinter.CTkEntry(self.main_frame, placeholder_text="summary")
        self.entry_summary.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.entry_description = customtkinter.CTkTextbox(self.main_frame, width=250, height=100)
        self.entry_description.grid(row=1, column=1, padx=(0, 0), pady=(10, 0), sticky="nsew")
        self.multi_selection = customtkinter.CTkComboBox(self.main_frame, values=list(self.event_color.keys()))
        self.multi_selection.set("Lavender")
        self.multi_selection.grid(row=2, column=2, padx=10, pady=(10, 10))
        self.color_preview = customtkinter.CTkCanvas(self.main_frame, width=15, height=15)
        self.color_preview.grid(row=2, column=3)
        self.color_preview.configure(bg=self.event_color.get('Lavender'))
        
        # date frame
        self.date_frame = customtkinter.CTkFrame(self, width=400)
        self.date_frame.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.label_date_frame = customtkinter.CTkLabel(master=self.date_frame, text="Date Interval")
        self.label_date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="")
        self.label_date_from = customtkinter.CTkLabel(self.date_frame, text="From:", anchor="w")
        self.label_date_from.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.entry_date_from = customtkinter.CTkEntry(self.date_frame, placeholder_text="dd/mm/yyyy")
        self.entry_date_from.grid(row=1, column=1, padx=(0, 0), pady=(10, 10), sticky="nsew")
        self.entry_date_button = customtkinter.CTkButton(self.date_frame, text="", width=10, image=self.calendar_image, command=lambda: self.date_picker(1))
        self.entry_date_button.grid(row=1, column=2, padx=(0, 0), pady=(10, 10))
        self.label_date_to = customtkinter.CTkLabel(self.date_frame, text="To:", anchor="w")
        self.label_date_to.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.entry_date_to = customtkinter.CTkEntry(self.date_frame, placeholder_text="dd/mm/yyyy")
        self.entry_date_to.grid(row=2, column=1, padx=(0, 0), pady=(10, 10), sticky="nsew")
        self.entry_date_button2 = customtkinter.CTkButton(self.date_frame, text="", width=10, image=self.calendar_image, command=lambda: self.date_picker(2))
        self.entry_date_button2.grid(row=2, column=2, padx=(0, 0), pady=(0, 0))
        
        # create button
        self.create_button = customtkinter.CTkButton(self, command=None, image=self.plus_image, text="Create")
        self.create_button.grid(row=3, column=1, padx=20, pady=20)
        
        # create log textbox
        self.log_box = customtkinter.CTkTextbox(self, width=250, height=100)
        self.log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
        self.log_box.grid(row=4, column=1, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")
    
    def date_picker(self, type):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = customtkinter.CTkToplevel() # create window if its None or destroyed
            self.calendar = Calendar(self.toplevel_window)
            self.calendar.grid(row=0, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew")
            
            if type == 1:
                self.toplevel_window.title("Date From")
                self.confirm_button = customtkinter.CTkButton(self.toplevel_window, text="Confirm", command=lambda: self.get_date(1))
            elif type == 2:
                self.toplevel_window.title("Date To")
                self.confirm_button = customtkinter.CTkButton(self.toplevel_window, text="Confirm", command=lambda: self.get_date(2))
            else:
                Exception("type option doesn't exists")
            
            self.confirm_button.grid(row=1, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew") 
            
            self.toplevel_window.attributes("-topmost", True) # focus to this windows
            self.toplevel_window.resizable(False, False)
        else:
            self.toplevel_window.focus()  # if window exists focus it
    
    def get_date(self, type):
        date = self.calendar.get_date() # get the date from the calendar
        #TODO:
        #date = datetime.strptime(date, "%m-%d-%y") # convert the date string to datetime
        #date = datetime.strftime(date, "%d-%m-%Y") # edit the date format
        if type == 1:
            self.write_log("Date Selected From: " + date)
            self.entry_date_from.delete("0", tkinter.END)
            self.entry_date_from.insert("0", date)
        elif type == 2:
            self.write_log("Date Selected To: " + date)
            self.entry_date_to.delete("0", tkinter.END)
            self.entry_date_to.insert("0", date)
        else:
            Exception("type option doesn't exists")
        
        self.toplevel_window.destroy() 
    
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsByTitleFrame)
    
    def write_log(self, message):
        self.log_box.insert(tkinter.END, "\n" + str(datetime.now()) + ": " + message)

#?###########################################################

#?###########################################################
class EditEventsFrame(customtkinter.CTkFrame):
    
    main_class = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
                
        # load images
        self.calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        self.google_image = tkinter.PhotoImage(file='./imgs/google.png')
        self.plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        self.list_image = tkinter.PhotoImage(file='./imgs/list.png')
        self.edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Other Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, image=self.plus_image, text="New Events", command=self.go_to_new_events_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, image=self.edit_image, text="Edit Events", command=self.go_to_edit_events_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, image=self.list_image, text="Get Events List", command=self.go_to_get_events_by_title_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.google_calendar_link = customtkinter.CTkButton(self.sidebar_frame, image=self.google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/'))
        self.google_calendar_link.grid(row=6, column=0, padx=20, pady=(10, 10))
    
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsByTitleFrame) 
#?###########################################################

#?###########################################################
class GetEventsByTitleFrame(customtkinter.CTkFrame):
    
    main_class = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
                
        # load images
        self.calendar_image = tkinter.PhotoImage(file='./imgs/calendar.png')
        self.google_image = tkinter.PhotoImage(file='./imgs/google.png')
        self.plus_image = tkinter.PhotoImage(file='./imgs/plus.png')
        self.list_image = tkinter.PhotoImage(file='./imgs/list.png')
        self.edit_image = tkinter.PhotoImage(file='./imgs/edit.png')
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Other Options", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, image=self.plus_image, text="New Events", command=self.go_to_new_events_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, image=self.edit_image, text="Edit Events", command=self.go_to_edit_events_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, image=self.list_image, text="Get Events List", command=self.go_to_get_events_by_title_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.google_calendar_link = customtkinter.CTkButton(self.sidebar_frame, image=self.google_image, text="Google Calendar", command=lambda: webbrowser.open('https://calendar.google.com/'))
        self.google_calendar_link.grid(row=6, column=0, padx=20, pady=(10, 10))
    
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsByTitleFrame)
#?###########################################################

#?###########################################################
class MainFrame(customtkinter.CTkFrame):
    
    main_class = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # text title
        label = customtkinter.CTkLabel(self, text="Choose the action", fg_color="transparent", font=("Arial", 32))
        label.pack(padx=20, pady=20)
        
        # buttons action
        button = customtkinter.CTkButton(master=self, text="New Events", command=self.go_to_new_events_frame)
        button.pack(padx=20, pady=10)
        button1 = customtkinter.CTkButton(master=self, text="Edit Events", command=self.go_to_edit_events_frame)
        button1.pack(padx=20, pady=10)
        button2 = customtkinter.CTkButton(master=self, text="Get Events", command=self.go_to_get_events_by_title_frame)
        button2.pack(padx=20, pady=10)
    
    def go_to_new_events_frame(self):
        self.main_class.show_frame(NewEventsFrame)
    
    def go_to_edit_events_frame(self):
        self.main_class.show_frame(EditEventsFrame)
    
    def go_to_get_events_by_title_frame(self):
        self.main_class.show_frame(GetEventsByTitleFrame)
        
#?###########################################################

#?###########################################################   
class SetupFrame(customtkinter.CTkFrame):
    width = 900
    height = 600
    main_class = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # text title
        label = customtkinter.CTkLabel(self, text="Set Credentials", fg_color="transparent", font=("Arial", 32))
        label.pack(padx=20, pady=20)
        
        # buttons action
        button = customtkinter.CTkButton(master=self, text="Google Calendar", width=140, height=50, command=lambda: webbrowser.open('https://calendar.google.com/'))
        button.pack(padx=20, pady=10)
        button1 = customtkinter.CTkButton(master=self, text="Tutorial Setup", width=140, height=50, command=lambda: webbrowser.open('https://developers.google.com/workspace/guides/get-started'))
        button1.pack(padx=20, pady=10)
        button2 = customtkinter.CTkButton(master=self, text="First Setup", width=140, height=50, command=lambda: self.setCredentialsPath())
        button2.pack(padx=20, pady=10)
    
    def setCredentialsPath(self):
        # get response from dialog
        dialog = customtkinter.CTkInputDialog(title="New Credentials", text="Insert credentials path")
        credentials_path = dialog.get_input()
        token_path = credentials_path.rsplit("\\", 1)[0] + "\\" + "token.json"

        # get credentials
        credentials = gc.GoogleCalendarEventsManager.connectionSetup(credentials_path, gc.GoogleCalendarEventsManager.SCOPE, token_path)
        
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
                self.setCredentialsPath()

    
#?###########################################################

#*###########################################################
class App(): 
    root = None
    credentials_path = None
    token_path = None
    credentials = None
        
    def __init__(self):
        root = customtkinter.CTk()
        self.root = root
        
        
        self.init_window()
        self.init_menu()
        self.page_controller()
        
        self.root.mainloop()
        
        return 
        #TODO: solo per test, questo sotto va abilitato
        
        # read data from json to get path from last session
        listRes = js.SJONSettings.ReadFromJSON()
        if listRes != None:
            self.credentials_path = listRes["CredentialsPath"]
            self.token_path = listRes["TokenPath"]
            self.credentials = gc.GoogleCalendarEventsManager.connectionSetup(self.credentials_path, gc.GoogleCalendarEventsManager.SCOPE, self.token_path)
            
        self.init_window()
        self.init_menu()
        self.page_controller()
        
        self.root.mainloop()
        
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def init_window(self):
        # configure window
        self.root.iconbitmap('./imgs/icon.ico')
        self.root.title("Google Calendar Events Manager")
        self.root.geometry(f"{1100}x{900}")
        self.root.minsize(300, 300)
        
    def init_menu(self):
        menu = CTkMenuBar(self.root)
        button_1 = menu.add_cascade("File")
        button_2 = menu.add_cascade("Edit")
        button_3 = menu.add_cascade("Settings")
        button_4 = menu.add_cascade("About")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="New Credentials", command=lambda: self.setCredentialsPath())
        dropdown1.add_option(option="Open")
        dropdown1.add_option(option="Save")
        dropdown1.add_option(option="Exit", command=lambda: exit())

        dropdown1.add_separator()

        dropdown2 = CustomDropdownMenu(widget=button_2)
        dropdown2.add_option(option="Cut")
        dropdown2.add_option(option="Copy")
        dropdown2.add_option(option="Paste")

        dropdown3 = CustomDropdownMenu(widget=button_3)
        dropdown3.add_option(option="Update")
        
        sub_menu2 = dropdown3.add_submenu("Appearance")
        sub_menu2.add_option(option="System", command=lambda: customtkinter.set_appearance_mode("System"))
        sub_menu2.add_option(option="Dark", command=lambda: customtkinter.set_appearance_mode("dark"))
        sub_menu2.add_option(option="Light", command=lambda: customtkinter.set_appearance_mode("light"))

        dropdown4 = CustomDropdownMenu(widget=button_4)
        dropdown4.add_option(option="Share")
        
    def page_controller(self):
        # creating a container
        container = customtkinter.CTkFrame(self.root) 
        container.pack(side = "top", fill = "both", expand = True) 

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)        

        # initializing frames to an empty array
        self.frames = {} 

        # iterating through a tuple consisting of the different page layouts
        for F in (SetupFrame, MainFrame, NewEventsFrame, EditEventsFrame, GetEventsByTitleFrame):

            frame = F(container, self)

            # initializing frame of that object from pages for loop
            self.frames[F] = frame 

            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.show_frame(NewEventsFrame)
        
        return
        #TODO: solo per test, questo sotto va abilitato
        if self.credentials is None or self.credentials_path is None:
            self.show_frame(SetupFrame)
        else:
            self.show_frame(MainFrame)

    def set_credentials(self, credentials, credentials_path, token_path):
        self.credentials = credentials
        self.credentials_path = credentials_path
        self.token_path = token_path
        js.SJONSettings.WriteToJSON(self.credentials_path, self.token_path)
#*###########################################################

if __name__ == "__main__":
    app = App()
