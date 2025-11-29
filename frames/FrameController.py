import customtkinter as ctk
from enums.FrameTypes import FrameTypes
from frames.LoginFrame import LoginFrame
from frames.MainFrame import MainFrame
from frames.EditEventsFrame import EditEventsFrame
from frames.GetEventsFrame import GetEventsFrame
from frames.GraphFrame import GraphFrame
from frames.NewEventsFrame import NewEventsFrame
from LogService import LogService
from CommonOperations import CommonOperations

def show_frame(frame_type: FrameTypes, common: CommonOperations):
    logger = LogService.get_logger(__name__)
    frame = __get_frame_by_type(frame_type, common)
    logger.info(f"Raising frame: {frame}")
    frame.tkraise()

def page_controller(master, root, common: CommonOperations):
    # Create a container
    container = ctk.CTkFrame(root)
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    __init_frames(master, container, common)

    __show_start_frame_based_on_credentials(common)

def __init_frames(master, container, common: CommonOperations):
    master.frames = {}

    for F in (LoginFrame, MainFrame, NewEventsFrame, EditEventsFrame, GetEventsFrame, GraphFrame):
        frame = F(container, master) if F is LoginFrame else F(container)
        master.frames[F] = frame  # Use the class itself as the key
        frame.grid(row=0, column=0, sticky="nsew")

    common.set_frames(master.frames)

def __show_start_frame_based_on_credentials(common: CommonOperations):
    if common.get_credentials_or_none() is None or len(common.get_credentials_path()) == 0:
        show_frame(FrameTypes.LoginFrame, common)
    else:
        show_frame(FrameTypes.MainFrame, common)

def __get_frame_by_type(frame_type: FrameTypes, common: CommonOperations):
    match frame_type:
        case FrameTypes.EditEventsFrame:
            return common.get_frames()[EditEventsFrame]
        case FrameTypes.GetEventsFrame:
            return common.get_frames()[GetEventsFrame]
        case FrameTypes.GraphFrame:
            return common.get_frames()[GraphFrame]
        case FrameTypes.LoginFrame:
            return common.get_frames()[LoginFrame]
        case FrameTypes.MainFrame:
            return common.get_frames()[MainFrame]
        case FrameTypes.NewEventsFrame:
            return common.get_frames()[NewEventsFrame]
