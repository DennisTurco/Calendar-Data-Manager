import GoogleCalendarEventsManager as gc
import webbrowser
import JSONSettings as js
import io, subprocess, sys

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

#?###########################################################
class NewEventFrame(customtkinter.CTkFrame):
    
    main_class = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class


class MainFrame(customtkinter.CTkFrame):
    
    main_class = None
    
    def __init__(self, parent, main_class):
        customtkinter.CTkFrame.__init__(self, parent)
        self.main_class = main_class
        
        # text title
        label = customtkinter.CTkLabel(self, text="Choose the action", fg_color="transparent", font=("Arial", 32))
        label.pack(padx=20, pady=20)
        
        # buttons action
        button = customtkinter.CTkButton(master=self, text="New Events", command=self.show_frame("NewEventFrame"))
        button.pack(padx=20, pady=10)
        button1 = customtkinter.CTkButton(master=self, text="Edit Events", command=None)
        button1.pack(padx=20, pady=10)
        button2 = customtkinter.CTkButton(master=self, text="Get Events", command=None)
        button2.pack(padx=20, pady=10)
        
    def show_frame(self, frame: str):
        self.main_class.show_frame(frame)
        
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
        self.root.geometry(f"{1100}x{580}")
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
        for F in (SetupFrame, MainFrame, NewEventFrame):

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
        js.SJONSettings.WriteToJSON(self.credentials_path, self.token_path)
#*###########################################################

if __name__ == "__main__":
    app = App()
