import customtkinter as ctk
from desktop_app.CTkScrollableDropdown import *

from common.ConfigKeys import ConfigKeys
from common.ExceptionHandler import ExceptionHandler
from common.settings import TIMEZONE
from common.InformationMessages import InformationMessages
from common.entities.TimeRange import TimeRange
from desktop_app.frames.BaseFrame import BaseFrame
from desktop_app.Images import Images
from common.services.EventsService import EventsService
from common.entities.EventInfo import EventInfo
from common.LogService import LogService
from common.CommonOperations import CommonOperations
import desktop_app.GUIWidgets as GUIWidgets

class NewEventsFrame(BaseFrame):
    toplevel_window = None
    _common = CommonOperations()
    _logger = LogService.get_logger(__name__)

    def __init__(self, parent):
        BaseFrame.__init__(self, parent)
        img = Images()
        self.event_service = EventsService(self._common)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.setup_sidebar(img)

        # create main panel
        section_message = InformationMessages.new_event_info_message

        # create main panel
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
        title_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(title_frame, text="Create New Event", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=0, sticky="e")
        ctk.CTkButton(title_frame, text="", width=10, image=img.info_image,  fg_color="transparent", command=lambda: CommonOperations.open_info_section_dialog(self, "Edit Events", section_message)).grid(row=0, column=1, padx=5, pady=0, sticky="w")

        # main entry
        ctk.CTkFrame(self)
        main_frame = ctk.CTkScrollableFrame(self, label_text="Event Information")
        main_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="nsew")
        main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        label_summary = ctk.CTkLabel(main_frame, text="Summary:")
        label_summary.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_summary = ctk.CTkEntry(main_frame, placeholder_text="summary")
        self.entry_summary.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="w")
        label_description = ctk.CTkLabel(main_frame, text="Description:")
        label_description.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")
        self.entry_description = ctk.CTkTextbox(main_frame, width=250, height=100)
        self.entry_description.grid(row=1, column=1, padx=(0, 0), pady=(10, 0), sticky="ew")
        label_color = ctk.CTkLabel(main_frame, text="Color:")
        label_color.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")
        self.multi_selection = ctk.CTkComboBox(main_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection, values=list(ConfigKeys.Keys.EVENT_COLOR.value.keys()), button_color="transparent", command=self.__combobox_callback)
        self.multi_selection.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get("Light Blue"))
        self.multi_selection.set("Light Blue")
        self.multi_selection.grid(row=2, column=1, padx=0, pady=(10, 10), sticky="w")

        # date
        (self.entry_date_from, self.entry_date_to, self.timezone_selection, entry_date_button, entry_date_button2) = GUIWidgets.create_date_interval_scroll_frame(self, img.calendar_image, TIMEZONE)
        entry_date_button.configure(command=lambda: self.__date_picker(1))
        entry_date_button2.configure(command=lambda: self.__date_picker(2))

        # create button
        self.create_button = ctk.CTkButton(self, image=img.plus_image, text="Create", border_width=2, command=self.__create_event)
        self.create_button.grid(row=3, column=1, padx=20, pady=20)

        self.add_tooltips(
            (self.entry_summary, "(Required) Insert event title"),
            (self.entry_description, "(Optional) Insert event description"),
            (self.multi_selection, "(Required) Choose event color"),
            (self.entry_date_from, "(Optional) Enter date from"),
            (self.entry_date_to, "(Optional) Enter date to"),
            (self.timezone_selection, "(Optional) Choose time zone"),
            (self.create_button, "Create new event")
        )

        # create log textbox
        self.log_box = self.create_log_box(4, 1, 2)

    def __create_event(self):
        self._logger.info("Creating event")
        summary = self.entry_summary.get()
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        time_zone = self.timezone_selection.get()

        # update preferred TimeZone
        self._common.set_timezone(time_zone)

        if len(summary.replace(" ", "")) == 0:
            self._logger.warning(f"Error on creating event: summary is missing")
            self._common.write_log(self.log_box, f"Error on creating event: summary is missing")
            return
        if len(date_from.replace(" ", "")) == 0 or len(date_to.replace(" ", "")) == 0:
            self._logger.warning(f"Error on creating event: date is missing")
            self._common.write_log(self.log_box, f"Error on creating event: date is missing")
            return
        try:
            time_range = TimeRange().build_from_string(date_from, date_to)
            color_index = self._common.get_color_id(ConfigKeys.Keys.EVENT_COLOR.value, self.multi_selection.get())
            event_info = EventInfo(summary, str(self.entry_description), time_range, color_index, time_zone)
            self.event_service.create_event(event_info)
            self._logger.info(f"Event '{summary}' created successfully!")
            self._common.write_log(self.log_box, f"Event '{summary}' created successfully!")
        except ValueError as _:
            self._logger.error(f"Error on creating event: date format is not correct")
            self._common.write_log(self.log_box, f"Error on creating event: date format is not correct")
        except Exception as error:
            ExceptionHandler.handle_exception(self._common, self.log_box, error)

    def __combobox_callback(self, color):
        self.multi_selection.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get(color))
        self.multi_selection.set(color)
        self._logger.info(f"color '{color}' selected")
        self._common.write_log(self.log_box, f"color '{color}' selected")

    def __date_picker(self, picker_type):
        self.toplevel_window = self._common.date_picker_window(picker_type, self.toplevel_window, self.entry_date_from, self.entry_date_to, self.log_box)