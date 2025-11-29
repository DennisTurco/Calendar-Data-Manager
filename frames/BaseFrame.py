from enums.FrameTypes import FrameTypes
import webbrowser
import customtkinter as ctk
from CTkToolTip import *

from ConfigKeys import ConfigKeys
from LogService import LogService
from CommonOperations import CommonOperations
import GUIWidgets
import frames.FrameController as FrameController
from Images import Images

class BaseFrame(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        self._common = CommonOperations()
        self._logger = LogService.get_logger(__name__)

    def setup_sidebar(self, img: Images):
        return setup_sidebar(self, self._common, img)

    def create_log_box(self, row: int, column: int = 1, columnspan: int = 2, width: int = 250, height: int = 100):
        return create_log_box(self, row, column, columnspan, width, height)

    def wire_date_picker_buttons(self, entry_date_button, entry_date_button2):
        wire_date_picker_buttons(self, entry_date_button, entry_date_button2)

    @staticmethod
    def add_tooltips(self, *widget_message_pairs, delay: float = 0.3):
        add_tooltips(*widget_message_pairs, delay=delay)


def setup_sidebar(frame, common: CommonOperations, img: Images):
    (sidebar_button_1, sidebar_button_2, sidebar_button_3, sidebar_button_4, google_calendar_link, logo_button) = GUIWidgets.create_side_bar_frame(frame, img.plus_image, img.edit_image, img.list_image, img.chart_image, img.google_image, img.icon)
    sidebar_button_1.configure(command=lambda: FrameController.show_frame(FrameTypes.NewEventsFrame, common))
    sidebar_button_2.configure(command=lambda: FrameController.show_frame(FrameTypes.EditEventsFrame, common))
    sidebar_button_3.configure(command=lambda: FrameController.show_frame(FrameTypes.GetEventsFrame, common))
    sidebar_button_4.configure(command=lambda: FrameController.show_frame(FrameTypes.GraphFrame, common))
    logo_button.configure(command=lambda: FrameController.show_frame(FrameTypes.MainFrame, common))
    google_calendar_link.configure(command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
    return sidebar_button_1, sidebar_button_2, sidebar_button_3, sidebar_button_4, google_calendar_link, logo_button

#TODO: fix here
def wire_date_picker_buttons(frame, entry_date_button, entry_date_button2):
    entry_date_button.configure(command=lambda: frame.__date_picker(1))
    entry_date_button2.configure(command=lambda: frame.__date_picker(2))


def add_tooltips(*widget_message_pairs, delay: float = 0.3):
    for pair in widget_message_pairs:
        try:
            widget, message = pair
            CTkToolTip(widget, delay=delay, message=message)
        except Exception:
            # keep behavior resilient in case of unexpected input
            pass

def create_log_box(parent, row: int, column: int, columnspan: int = 2, width: int = 250, height: int = 100):
    log_box = ctk.CTkTextbox(parent, width=width, height=height)
    log_box.bind("<Key>", lambda e: "break")  # set the textbox readonly
    log_box.grid(row=row, column=column, columnspan=columnspan, padx=(0, 0), pady=(20, 0), sticky="nsew")
    return log_box