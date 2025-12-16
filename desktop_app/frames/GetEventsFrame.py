from datetime import datetime, timedelta
import glob
import tempfile
from desktop_app.enums.FrameTypes import FrameTypes
from typing import Any
import os
from common.DataEditor import DataCSV
import tkinter
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
from desktop_app.LogService import LogService
from common.CommonOperations import CommonOperations
import desktop_app.GUIWidgets as GUIWidgets
import desktop_app.frames.FrameController as FrameController

class GetEventsFrame(BaseFrame):
    toplevel_window = None
    toplevel_entry_window = None
    date_picker_window = None
    file_viewer_window = None
    events_preview_in_table = None
    data = None
    events: list[Any] = []
    _logger = LogService.get_logger(__name__)
    _common = CommonOperations()
    event_color = ConfigKeys.Keys.EVENT_COLOR.value

    def __init__(self, parent):
        BaseFrame.__init__(self, parent)
        self.img = Images()
        self.event_color["No Color Filtering"] = ""

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.setup_sidebar(self.img)

        section_message = InformationMessages.get_events_info_message

        # create main panel
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
        title_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(title_frame, text="Get Events List", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=0, sticky="e")
        ctk.CTkButton(title_frame, text="", width=10, image=self.img.info_image,  fg_color="transparent", command=lambda: CommonOperations.open_info_section_dialog(self, "Get Events List", section_message)).grid(row=0, column=1, padx=5, pady=0, sticky="w")

        # create a container frame for the two scrollable frames
        container_frame = ctk.CTkFrame(self, fg_color="transparent")
        container_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="nsew")
        container_frame.grid_columnconfigure((0, 1), weight=1)  # 2 Columns for main_frame and date_frame

        # Column 1: main_frame (Event Information)
        main_frame = ctk.CTkScrollableFrame(container_frame, label_text="Event Information")
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)  # Setup columns for fields
        self.label_id = ctk.CTkLabel(main_frame, text="ID:")
        self.label_id.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_id = ctk.CTkEntry(main_frame, placeholder_text="id")
        self.entry_id.grid(row=0, column=1, padx=(10, 10), pady=5, sticky="w")
        label_summary = ctk.CTkLabel(main_frame, text="Summary:")
        label_summary.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_summary = ctk.CTkEntry(main_frame, placeholder_text="summary")
        self.entry_summary.grid(row=1, column=1, padx=(10, 10), pady=5, sticky="w")
        label_description = ctk.CTkLabel(main_frame, text="Description:")
        label_description.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_description = ctk.CTkTextbox(main_frame, width=150, height=100)
        self.entry_description.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="ew")
        label_color = ctk.CTkLabel(main_frame, text="Color:")
        label_color.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.multi_selection = ctk.CTkComboBox(main_frame, state="readonly")
        CTkScrollableDropdown(self.multi_selection, values=list(self.event_color.keys()), button_color="transparent", command=self.__combobox_callback)
        self.multi_selection.configure(button_color=self.event_color.get("No Color Filtering"))
        self.multi_selection.set("No Color Filtering")
        self.multi_selection.grid(row=3, column=1, padx=0, pady=5, sticky="w")

        # Column 2: date_frame (Date Interval)
        (self.entry_date_from, self.entry_date_to, entry_date_button, self.label_date_to, entry_date_button2, self.timezone_selection) = GUIWidgets.create_date_selection_for_events_list_scroll_frame(container_frame, TIMEZONE, self.img.calendar_image)
        entry_date_button.configure(command=lambda: self.__date_picker(1))
        entry_date_button2.configure(command=lambda: self.__date_picker(2))

        # file output
        (self.file_path, self.overwrite_mode, button_file_path, button_open_file, button_open_events_table_preview) = GUIWidgets.create_file_output_scroll_frame_for_events_list_frame(self, self.img.folder_image, self.img.file_image, self.img.table_image)
        button_file_path.configure(command=lambda: self.__get_file_path(self.file_path))
        button_open_file.configure(command=self.__open_file)
        button_open_events_table_preview.configure(command=self.__events_table_preview)

        # create a container frame for the buttons
        container_frame2 = ctk.CTkFrame(self, fg_color="transparent")
        container_frame2.grid(row=4, column=1, padx=(50, 50), pady=10, sticky="nsew")
        container_frame2.grid_columnconfigure((0, 1), weight=1)  # 2 Columns for main_frame and date_frame

        # get list button
        get_button = ctk.CTkButton(container_frame2, image=self.img.list_image, text="Get", border_width=2, command=self.__get_and_preview)
        get_button.grid(row=0, column=0, padx=5, pady=10, sticky="e")
        get_and_plot_button = ctk.CTkButton(container_frame2, image=self.img.chart_image, text="Get and plot", border_width=2, command=self.__get_and_plot)
        get_and_plot_button.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.add_tooltips(
            (self.entry_id, "(Optional) Enter event id This is a very specific field;\n if you want to get a specific event and you know the specific event id, you can enter it and ignore the fields below.\n Otherwise you can ignore it and proceed to fill in the other fields."),
            (self.entry_summary, "(Optional) Insert event title"),
            (self.entry_description, "(Optional) Insert the event description"),
            (self.multi_selection, "(Optional) Choose event color"),
            (self.entry_date_from, "(Optional) Enter date from"),
            (self.entry_date_to, "(Optional) Enter date to"),
            (self.timezone_selection, "(Optional) Choose time zone"),
            (self.file_path, "(Optional) Enter the path to the file;\n if you want to save the results to a specific file (.csv, .txt)"),
            (self.overwrite_mode, "If it is enabled, it overwrites the contents of the file with the newly obtained events.\n Otherwise, it adds the newly obtained events without deleting anything."),
            (button_open_file, "Open file preview"),
            (button_open_events_table_preview, "Open file preview in table"),
            (get_button, "Get and save events."),
            (get_and_plot_button, "Get and plot events without saving to a file.")
        )

        # create log textbox
        self.log_box = self.create_log_box(5, 1, 2)

        self.cleanup_temp_files()

    # returns the number of events obtained
    def __get_events_count(self) -> int:

        entry_id = self.entry_id.get() if len(self.entry_id.get()) != 0 else None
        summary = self.entry_summary.get()
        date_from = self.entry_date_from.get()
        date_to = self.entry_date_to.get()
        description = self.entry_description.get("0.0", tkinter.END).replace('\n', '')
        time_zone = self.timezone_selection.get()

        CommonOperations.set_timezone(time_zone)

        time_range = TimeRange().build_from_string(date_from, date_to)
        color_index = CommonOperations.get_color_id(self.multi_selection.get())
        event_info = EventInfo(summary, description, time_range, color_index, time_zone, entry_id)

        try:
            self.events = CommonOperations.get_events(self._common.get_credentials_or_exception(), event_info)
    
            if len(self.events) > 1:
                self._logger.info(f"{len(self.events)} Event(s) obtained successfully!")
                self._common.write_log(self.log_box, f"{len(self.events)} Event(s) obtained successfully!")
            elif len(self.events) == 0:
                self._logger.info(f"No events obtained")
                self._common.write_log(self.log_box, f"No events obtained")
            elif len(self.events) == 1:
                self._logger.info(f"Event obtained successfully!")
                self._common.write_log(self.log_box, f"Event obtained successfully!")
        except ValueError as _:
            self._logger.error(f"Error on creating event: date format is not correct")
            self._common.write_log(self.log_box, f"Error on creating event: date format is not correct")
            return -1
        except Exception as error:
            ExceptionHandler.handle_exception(self._common, self.log_box, error)
            return -1
        
        return len(self.events)


    def __get_and_preview(self):
        if self.__get_events_count() <= 0:
            return

        self.events_list_viewer_window()

    def __get_and_plot(self):
        if self.__get_events_count() <= 0:
            return

        try:
            # save results to a temp file
            tmp = tempfile.NamedTemporaryFile(delete=False)  # Prevent automatic deletion

            self.file_path.delete("0", tkinter.END)
            self.file_path.insert("0", string=tmp.name)
            self.__save_results_to_file()

            FrameController.show_frame(FrameTypes.GraphFrame, self._common)
            # GraphFrame.set_file_path(FrameTypes.GraphFrame, text=tmp.name)
        except Exception as e:
            raise e

    @staticmethod
    def cleanup_temp_files():
        """Delete temp files of the previous sessions"""
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
        self._logger.info("Events list viewer")

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel()
            self.toplevel_window.after(200, lambda: self.toplevel_window.iconbitmap(self.img.list_ico)) # type: ignore # I have to delay the icon because it's buggy on windows
            self.toplevel_window.title(f'{len(self.events)} Event(s) obtained')

            # Create a grid inside the toplevel window
            self.toplevel_window.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand vertically
            self.toplevel_window.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
            self.toplevel_window.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally

            event_list_file_viewer = ctk.CTkTextbox(self.toplevel_window)
            event_list_file_viewer.bind("<Key>", lambda e: "break")  # set the textbox readonly
            event_list_file_viewer.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10), sticky="nsew")

            button_save = ctk.CTkButton(self.toplevel_window, text="Save results", command=lambda: self.__get_filepath_to_save_results())
            button_save.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="nsew")

            button_cancel = ctk.CTkButton(self.toplevel_window, text="Cancel", command=lambda: self.close_top_frame_window())
            button_cancel.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="nsew")

            event_list_file_viewer.delete(1.0, tkinter.END)

            events_info = self.__format_events_content()

            # print event after event
            for event in events_info:
                event_info_str = f"INDEX: {event['index']} | ID: {event['ID']} | SUMMARY: {event['summary']} | START: {event['start']} | END: {event['end']} | DURATION: {event['duration']}\n"
                event_list_file_viewer.insert(tkinter.END, event_info_str)

            self.toplevel_window.attributes("-topmost", True) # focus to this windows
            CommonOperations.center_top_level(self.toplevel_window)
        else:
            self.toplevel_window.focus()  # if window exists focus it

        return self.toplevel_window

    def __format_events_content(self):
        # obtain only important information about the event
        events_info = []
        index = 1
        for event in self.events:

            (start_date, end_date) = self.__set_event_date_with_fallback(event)
            duration = self.__get_duration_from_date_interval(start_date, end_date)

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

    def __get_filepath_to_save_results(self):
        if self.file_path and self.file_path.get():
            self.__save_results_to_file()
            return None

        if self.toplevel_entry_window is None or not self.toplevel_entry_window.winfo_exists():
            self.toplevel_entry_window = ctk.CTkToplevel()
            self.toplevel_entry_window.after(200, lambda: self.toplevel_entry_window.iconbitmap(self.img.folder_ico)) # type: ignore # I have to delay the icon because it's buggy on windows
            self.toplevel_entry_window.title('Select a file to save the results')
            self.toplevel_entry_window.geometry("350x50")
            entry = ctk.CTkEntry(self.toplevel_entry_window, width=250, placeholder_text="file path")
            entry.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="nsew")
            button_add_filepath = ctk.CTkButton(self.toplevel_entry_window, width=10, text="", image=self.img.folder_image, command=lambda: self.__get_file_path(entry))
            button_add_filepath.grid(row=0, column=1, padx=5, pady=(10, 10), sticky="nsew")
            button_ok = ctk.CTkButton(self.toplevel_entry_window, width=10, text="Ok", command=lambda: self.__save_results_to_file2(entry))
            button_ok.grid(row=0, column=2, padx=5, pady=(10, 10), sticky="nsew")

            self.toplevel_entry_window.resizable(False, False)
            self.toplevel_entry_window.attributes("-topmost", False) # focus to this windows
            CommonOperations.center_top_level(self.toplevel_entry_window)
        else:
            self.toplevel_entry_window.focus()  # if window exists focus it

        return self.toplevel_entry_window

    # sometimes the event doesn't have 'dateTime'
    @staticmethod
    def __set_event_date_with_fallback(event) -> tuple[Any, Any]:
        try:
            start_date = event["start"].get("dateTime")
            end_date = event["end"].get("dateTime")
        except (TypeError, KeyError):
            return None, None  # structure is invalid

            # If dateTime is missing, fall back to date
        if start_date is None:
            start_date = event["start"].get("date")
        if end_date is None:
            end_date = event["end"].get("date")

        return start_date, end_date

    @staticmethod
    def __get_duration_from_date_interval(start_date, end_date) -> timedelta:
        start_datetime = datetime.fromisoformat(start_date)
        end_datetime = datetime.fromisoformat(end_date)
        return end_datetime - start_datetime

    def __save_results_to_file(self):
        try:
            # close the toplevel windows
            if self.toplevel_window: self.close_top_frame_window()
            if self.toplevel_entry_window: self.close_top_frame_entry_window()

            # if file doesn't exist, create it
            if not os.path.isfile(self.file_path.get()):
                file = open(self.file_path.get(), "x")
                file.close()

            # get all from file csv
            data = {}
            if self.overwrite_mode.get() == "off":
                data = DataCSV.load_data_from_file(self.file_path.get(), '|')

            # add into data object
            counter = 0
            for event in self.events:

                (start_date, end_date) = self.__set_event_date_with_fallback(event)
                duration = self.__get_duration_from_date_interval(start_date, end_date)
                data_list = [str(event['id']), str(event['summary']), str(start_date), str(end_date), str(duration)]
                added = DataCSV.add_data(data, event['id'], data_list=data_list)
                if added:
                    counter += 1

            DataCSV.save_data_to_file(data, self.file_path.get(), '|', 'utf-8')

            self._logger.info(f"{counter} event(s) added to file {self.file_path.get()}")
            self._common.write_log(self.log_box, f"{counter} event(s) added to file {self.file_path.get()}")

        except Exception as error:
            ExceptionHandler.handle_exception(self._common, self.log_box, error)

    def __save_results_to_file2(self, entry):
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", entry.get())

        self.__save_results_to_file()

    def close_top_frame_window(self):
        self.toplevel_window.destroy()

    def close_top_frame_entry_window(self):
        self.toplevel_entry_window.destroy()

    def __combobox_callback(self, color):
        self.multi_selection.configure(button_color=self.event_color.get(color))
        self.multi_selection.set(color)
        self._logger.info(f"color '{color}' selected")
        CommonOperations.write_log(log_box=self.log_box, message=f"color '{color}' selected")

    def __get_file_path(self, entry):
        self._common.get_file_path(self.log_box, entry)

    def __open_file(self):
        self.file_viewer_window = self._common.file_viewer_window(self.file_viewer_window, self.file_path.get(), self.log_box)

    def __events_table_preview(self):
        self.events_preview_in_table = self._common.events_preview_in_table(self.events_preview_in_table, self.file_path.get(), self.log_box)

    def __date_picker(self, picker_type):
        self.date_picker_window = self._common.date_picker_window(picker_type, self.date_picker_window, self.entry_date_from, self.entry_date_to, self.log_box)