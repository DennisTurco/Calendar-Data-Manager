import customtkinter as ctk
from GUI import LoginFrame, MainFrame, NewEventsFrame, EditEventsFrame, GetEventsFrame, GraphFrame
from Logger import Logger
from CommonOperations import CommonOperations

def show_frame(frame):
    Logger.write_log(f"Raising frame: {frame}", Logger.LogType.INFO)
    frame.tkraise()

def page_controller(master, root, common: CommonOperations):
    # Create a container
    container = ctk.CTkFrame(root) 
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)        

    # Store frame instances in master (APP class)
    master.frames = {}  # Ensure you are storing the frames in master

    # Iterate through the tuple of frame classes
    for F in (LoginFrame, MainFrame, NewEventsFrame, EditEventsFrame, GetEventsFrame, GraphFrame):
        frame = F(container, master)
        master.frames[F] = frame  # Use the class itself as the key
        frame.grid(row=0, column=0, sticky="nsew")

    common.set_frames(master.frames)

    # Show the correct frame based on credentials
    if common.get_credentials() is None or common.get_credentials_path() is None:
        show_frame(master.frames[LoginFrame])  # Access by class
    else:
        show_frame(master.frames[MainFrame])  # Access by class