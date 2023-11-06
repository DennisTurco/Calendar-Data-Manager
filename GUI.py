import customtkinter
from CTkMenuBar import *
from CTkMessagebox import *

import GoogleCalendarEventsManager as gc

class App():
    
    root = None
    credentials_path = None
    token_path = None
    credentials = None
        
    def __init__(self):
        root = customtkinter.CTk()
        self.root = root
            
        self.init_windows()
        self.init_menu()
        
        root.mainloop()
    
    def init_windows(self):
        # configure window
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
        dropdown1.add_option(option="Open", command=lambda: print("Open"))
        dropdown1.add_option(option="Save")
        dropdown1.add_option(option="Exit", command=lambda: self.exit_app())

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

    def setCredentialsPath(self):
        # get response from dialog
        dialog = customtkinter.CTkInputDialog(title="New Credentials", text="Insert credentials path")
        self.credentials_path = dialog.get_input()
        substring = self.credentials_path.rsplit("\\", 1)[0] + "\\" + "token.json"
        
        # get credentials
        self.credentials = gc.GoogleCalendarEventsManager.connectionSetup(self.credentials_path, gc.GoogleCalendarEventsManager.SCOPE, substring)
        
        # response message box
        if self.credentials is not None:
            CTkMessagebox(message="Credentials setted succeffully", icon="check", option_1="Ok")
        else:
            msg = CTkMessagebox(title="Credentials error", message="Do you wish to retry?", icon="cancel", option_1="Yes", option_2="No")
            response = msg.get()
            if response=="Yes":
                self.setCredentialsPath()

    def open_file(self):
        # Add code to open a file here
        pass

    def exit_app(self):
        self.root.quit()



if __name__ == "__main__":
    app = App()
