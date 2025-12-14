from datetime import datetime, timedelta
from typing import Optional
import tkinter
import customtkinter as ctk
from CTkMessagebox import *
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

class EditEventsFrame(BaseFrame):
    _common = CommonOperations()
    _logger = LogService.get_logger(__name__)
    toplevel_window: Optional[ctk.CTkToplevel] = None
    date_picker_window: Optional[ctk.CTkToplevel] = None
    event_color_from: dict[str, str] = ConfigKeys.Keys.EVENT_COLOR.value
    event_color_to: dict[str, str] = ConfigKeys.Keys.EVENT_COLOR.value

    def __init__(self, parent):
        BaseFrame.__init__(self, parent)
        self.img = Images()

        self.event_color_from["No Color Filtering"] = "" # adding a new element inside the dictionary

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 4), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.setup_sidebar(self.img)

        section_message = InformationMessages.update_events_info_message

        # create main panel
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
        title_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(title_frame, text="Edit Events", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=0, sticky="e")
        ctk.CTkButton(title_frame, text="", width=10, image=self.img.info_image,  fg_color="transparent", command=lambda: CommonOperations.open_info_section_dialog(self, "Edit Events", section_message)).grid(row=0, column=1, padx=5, pady=0, sticky="w")

        # Create a frame with a 1x2 grid
        main_frame = ctk.CTkScrollableFrame(self, label_text="Event Information")
        main_frame.grid(row=1, column=1, padx=50, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # old main values
        old_values_frame = ctk.CTkFrame(main_frame)
        old_values_frame.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        old_values_frame.grid_columnconfigure((0, 1, 2), weight=1)
        label_frame_old = ctk.CTkLabel(old_values_frame, text="OLD Values")
        label_frame_old.grid(row=0, column=0, columnspan=3, padx=0, pady=0, sticky="ew")
        label_summary_old = ctk.CTkLabel(old_values_frame, text="Summary:")
        label_summary_old.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_summary_old = ctk.CTkEntry(old_values_frame, placeholder_text="summary")
        self.entry_summary_old.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=5, sticky="w")
        label_description_old = ctk.CTkLabel(old_values_frame, text="Description:")
        label_description_old.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_description_old = ctk.CTkTextbox(old_values_frame, width=250, height=100)
        self.entry_description_old.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="ew")
        label_color_old = ctk.CTkLabel(old_values_frame, text="Color:")
        label_color_old.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.multi_selection_old = ctk.CTkComboBox(old_values_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection_old, values=list(self.event_color_from.keys()), button_color="transparent", command=self.__combobox_callback_color1)
        self.multi_selection_old.configure(button_color=self.event_color_from.get("No Color Filtering"))
        self.multi_selection_old.set("No Color Filtering")
        self.multi_selection_old.grid(row=3, column=1, padx=0, pady=5, sticky="w")

        # Centered img label
        ctk.CTkLabel(main_frame, text="", image=self.img.arrow_image).grid(row=1, column=1, padx=0, pady=10, sticky="ew")

        # new main values
        new_values_frame = ctk.CTkFrame(main_frame)
        new_values_frame.grid(row=1, column=2, padx=25, pady=10, sticky="ew")
        new_values_frame.grid_columnconfigure((0, 1, 2), weight=1)
        label_frame_new = ctk.CTkLabel(new_values_frame, text="NEW Values")
        label_frame_new.grid(row=0, column=0, columnspan=3, padx=0, pady=0, sticky="ew")
        label_summary_new = ctk.CTkLabel(new_values_frame, text="Summary:")
        label_summary_new.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_summary_new = ctk.CTkEntry(new_values_frame, placeholder_text="summary")
        self.entry_summary_new.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=5, sticky="w")
        label_description_new = ctk.CTkLabel(new_values_frame, text="Description:")
        label_description_new.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_description_new = ctk.CTkTextbox(new_values_frame, width=250, height=100)
        self.entry_description_new.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="ew")
        label_color_new = ctk.CTkLabel(new_values_frame, text="Color:")
        label_color_new.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.multi_selection_new = ctk.CTkComboBox(new_values_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection_new, values=list(ConfigKeys.Keys.EVENT_COLOR.value.keys()), button_color="transparent", command=self.__combobox_callback_color2)
        self.multi_selection_new.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get("Light Blue"))
        self.multi_selection_new.set("Light Blue")
        self.multi_selection_new.grid(row=3, column=1, padx=0, pady=5, sticky="w")

        # date
        (self.entry_date_from, self.entry_date_to, self.timezone_selection, entry_date_button, entry_date_button2) = GUIWidgets.create_date_interval_scroll_frame(self, self.img.calendar_image, TIMEZONE)
        entry_date_button.configure(command=lambda: self.__date_picker(1))
        entry_date_button2.configure(command=lambda: self.__date_picker(2))

        # edit button
        edit_button = ctk.CTkButton(self, image=self.img.edit_image, text="Edit", border_width=2, command=self.__edit_events)
        edit_button.grid(row=3, column=1, columnspan=2, padx=20, pady=20)

        self.add_tooltips(
            (self.entry_summary_old, "(Required) Insert OLD event title"),
            (self.entry_description_old, "(Optional) Insert the OLD event description"),
            (self.multi_selection_old, "(Optional) Choose OLD event color"),
            (self.entry_summary_new, "(Required) Insert NEW event title"),
            (self.entry_description_new, "(Optional/Required) Insert NEW event description;\n If the old description is set, this field will not be ignored."),
            (self.multi_selection_new, "(Required) Choose NEW event color"),
            (self.entry_date_from, "(Optional) Enter date from"),
            (self.entry_date_to, "(Optional) Enter date to"),
            (self.timezone_selection, "(Optional) Choose time zone"),
            (edit_button, "Edit events")
        )

        # create log textbox
        self.log_box = self.create_log_box(4, 1, 2)

    def __date_picker(self, picker_type):
        self.date_picker_window = CommonOperations.date_picker_window(picker_type, self.date_picker_window, self.entry_date_from, self.entry_date_to, self.log_box)

    def __edit_events(self):
        self._logger.info("Editing events")

        # Get OLD values
        summary_old = self.entry_summary_old.get()
        description_old = self.entry_description_old.get('0.0', tkinter.END)
        color_index_old = CommonOperations.get_color_id(self.multi_selection_old.get(), self.event_color_from)  # Get color index for old events

        # Get NEW values
        summary_new = self.entry_summary_new.get()
        description_new = self.entry_description_new.get('0.0', tkinter.END)
        color_index_new = CommonOperations.get_color_id(self.multi_selection_new.get(), self.event_color_to)  # Get color index for new events

        # Validate input data
        if not summary_old:
            self._logger.warning("ERROR: Missing old summary")
            CommonOperations.write_log(self.log_box, "ERROR: Missing old summary")
            return
        if not summary_new:
            self._logger.warning("ERROR: Missing new summary")
            CommonOperations.write_log(self.log_box, "ERROR: Missing new summary")
            return

        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()

        try:
            time_range = TimeRange().build_from_string(date_from, date_to)

            time_zone = self.timezone_selection.get()
            CommonOperations.set_timezone(time_zone)

            # Retrieve events to edit
            event_info = EventInfo(summary_old, description_old, time_range, color_index_old, time_zone)
            old_events = EventsService.fetch_events(self._common.get_credentials_or_exception(), event_info)

            if not old_events:
                self._logger.info("No events found")
                CommonOperations.write_log(self.log_box, "No events found")

            event_info = EventInfo(summary_new, description_new, time_range, color_index_old, time_zone)
            new_events = EventsService.simulate_update_events(self._common.get_credentials_or_exception(), event_info, old_events)
            self.events_list_viewer_window(old_events, new_events, summary_new, description_new, color_index_new, date_from, date_to, time_zone)
        except ValueError:
            self._logger.error("ERROR: Invalid date format")
            CommonOperations.write_log(self.log_box, "ERROR: Invalid date format")
        except Exception as error:
            ExceptionHandler.handle_exception(self._common, self.log_box, error)

    def __combobox_callback_color1(self, color):
        self.multi_selection_old.configure(button_color=self.event_color_from.get(color))
        self.multi_selection_old.set(color)
        self._logger.info(f"Old color '{color}' selected")
        CommonOperations.write_log(self.log_box, f"color '{color}' selected")

    def __combobox_callback_color2(self, color):
        self.multi_selection_new.configure(button_color=ConfigKeys.Keys.EVENT_COLOR.value.get(color))
        self.multi_selection_new.set(color)
        self._logger.info(f"New color '{color}' selected")
        CommonOperations.write_log(self.log_box, f"color '{color}' selected")

    def __update_events(self, old_events: dict, summary_new: str, description_new: str, color_index_new, date_from: str, date_to: str, time_zone: str):
        msg = CTkMessagebox(title="Edit events", message=f"Are you sure you want to confirm the changes?\n{len(old_events)} events will be changed.", icon="question", option_1="No", option_2="Yes")
        if msg.get() == "Yes":
            self._logger.info(f"Old events edited: {old_events}")

            time_range = TimeRange().build_from_string(date_from, date_to)

            event_info = EventInfo(summary_new, description_new, time_range, color_index_new, time_zone)
            updated_events = EventsService.edit_events(self._common.get_credentials_or_exception(), event_info, old_events)
            if updated_events is None: return

            self._logger.info(f"{len(updated_events)} event(s) successfully updated!")
            CommonOperations.write_log(self.log_box, f"{len(updated_events)} event(s) successfully updated!")
            self.close_top_frame_window()

    def close_top_frame_window(self):
        self.toplevel_window.destroy()

    def events_list_viewer_window(self, old_events: dict, new_events: dict, summary_new: str, description_new: str, color_index_new, date_from, date_to, time_zone):
        self._logger.info("Events list viewer")

        # Create a new window if it doesn't exist
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel()
            self.toplevel_window.after(200, lambda: self.toplevel_window.iconbitmap(self.img.list_ico)) # type: ignore # I have to delay the icon because it's buggy on windows
            self.toplevel_window.title(f'{len(old_events)} Event(s) Found')

            # Configure grid layout
            self.toplevel_window.grid_rowconfigure(0, weight=1)
            self.toplevel_window.grid_columnconfigure(0, weight=1)
            self.toplevel_window.grid_columnconfigure(1, weight=1)

            # Scrollable frame for events display
            event_frame = ctk.CTkFrame(self.toplevel_window)
            event_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

            # Buttons for updating or canceling the event changes
            button_update = ctk.CTkButton(self.toplevel_window, text="Update Results", command=lambda: self.__update_events(old_events, summary_new, description_new, color_index_new, date_from, date_to, time_zone))
            button_update.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")

            button_cancel = ctk.CTkButton(self.toplevel_window, text="Cancel", command=self.close_top_frame_window)
            button_cancel.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="nsew")

            # Extract and display old and new event details with colors
            old_events_info = self.__extract_event_info(old_events)
            new_events_info = self.__extract_event_info(new_events)

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
            CommonOperations.center_top_level(self.toplevel_window)
        else:
            self.toplevel_window.focus()  # Focus the window if it already exists

    def __extract_event_info(self, events: dict):
        # Extract relevant event information for display
        event_info_list = []
        for index, event in enumerate(events, start=1):
            try:
                start_date = event['start']['dateTime']
                end_date = event['end']['dateTime']
            except KeyError:
                start_date = event['start']['date']
                end_date = event['end']['date']

            duration = self.__get_duration_from_date_interval(start_date, end_date)

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

    @staticmethod
    def __get_duration_from_date_interval(start_date: str, end_date: str) -> timedelta:
        start_datetime = datetime.fromisoformat(start_date)
        end_datetime = datetime.fromisoformat(end_date)
        return end_datetime - start_datetime