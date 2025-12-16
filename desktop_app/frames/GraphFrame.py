import threading
from tkinter import filedialog
import tkinter

from CTkMessagebox import CTkMessagebox
from common.CommonOperations import CommonOperations
from common.ConfigKeys import ConfigKeys
from common.ExceptionHandler import ExceptionHandler
import desktop_app.GUIWidgets as GUIWidgets
from desktop_app.LogService import LogService
from common.Plotter import Plotter
from desktop_app.frames.BaseFrame import BaseFrame
from desktop_app.Images import Images
import customtkinter as ctk

class GraphFrame(BaseFrame):
    file_viewer_window = None
    events_preview_in_table = None
    _common = CommonOperations()
    _logger = LogService.get_logger(__name__)
    stop_event = threading.Event()

    def __init__(self, parent):
        BaseFrame.__init__(self, parent)
        img = Images()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.setup_sidebar(img)

        # create main panel
        (self.file_path, button_file_path, button_open_file, button_open_events_table_preview) = GUIWidgets.create_file_path_scroll_frame_for_graph_frame(self, img.folder_image, img.file_image, img.table_image, img.info_image)
        button_file_path.configure(command=self.get_file_path)
        button_open_file.configure(command=self.__open_file)
        button_open_events_table_preview.configure(command=self.__events_table_preview)

        # Graph types
        (self.button_select_all, self.button_deselect_all, self.total_hours_per_year, self.total_hours_per_month, self.total_hours_by_summary, self.total_hours_by_summary2, self.total_hours_per_year_by_summary, self.total_hours_per_month_by_summary, self.total_hours_per_month_grouped_by_year) = GUIWidgets.create_graph_types_scroll_frame(self, img.square_check_image, img.square_image)
        self.button_select_all.configure(command=self.__select_all)
        self.button_deselect_all.configure(command=self.__deselect_all)

        self.graph_button = ctk.CTkButton(self, command=self.__generate_graph, image=img.chart_image, border_width=2, text="Generate")
        self.graph_button.grid(row=4, column=1, padx=20, pady=20)

        self.add_tooltips(
            (self.file_path, "(Required) Enter the path to the file you generated from the 'Get Events List' section."),
            (button_open_file, "Open file preview"),
            (button_open_events_table_preview, "Open file preview in table"),
            (self.graph_button, "Generate graphs"),
            (self.button_select_all, "Select all types"),
            (self.button_deselect_all, "Deselect all types")
        )

        # create log textbox
        self.log_box = self.create_log_box(5, 1, 2)

    def get_file_path(self):
        file_path = filedialog.askopenfilename(title="Select file where do you want to save data", filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")))
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", file_path)
        self._logger.info(f"file '{file_path}' selected")
        self._common.write_log(self.log_box, f"file '{file_path}' selected")

    def set_file_path(self, text: str):
        self.file_path.delete("0", tkinter.END)
        self.file_path.insert("0", string=text)

    def __open_file(self):
        self.file_viewer_window = self._common.file_viewer_window(self.file_viewer_window, self.file_path.get(), self.log_box)

    def __events_table_preview(self):
        self.events_preview_in_table = self._common.events_preview_in_table(self.events_preview_in_table, self.file_path.get(), self.log_box)

    def __select_all(self):
        self.total_hours_per_year.select()
        self.total_hours_per_month.select()
        self.total_hours_by_summary.select()
        self.total_hours_by_summary2.select()
        self.total_hours_per_year_by_summary.select()
        self.total_hours_per_month_by_summary.select()
        self.total_hours_per_month_grouped_by_year.select()
        self._logger.info(f"all chart types selected")
        self._common.write_log(self.log_box, f"all chart types selected")

    def __deselect_all(self):
        self.total_hours_per_year.deselect()
        self.total_hours_per_month.deselect()
        self.total_hours_by_summary.deselect()
        self.total_hours_by_summary2.deselect()
        self.total_hours_per_year_by_summary.deselect()
        self.total_hours_per_month_by_summary.deselect()
        self.total_hours_per_month_grouped_by_year.deselect()
        self._logger.info(f"all chart types deselected")
        self._common.write_log(self.log_box, f"all chart types deselected")

    # Timeout function to stop the chart generation
    def __generate_chart_with_timeout(self, chart_function, data, timeout=ConfigKeys.Keys.GRAPH_TIMEOUT.value):
        def target():
            try:
                if not self.stop_event.is_set():  # Check if timeout occurred
                    chart_function(data)
            except Exception as ex:
                self._common.messagebox_exception(ex)
                self._logger.info(f"An error occurred during setting timeout for chart generation")
                self._common.write_log(self.log_box, f"An error occurred during setting timeout for chart generation")

        # Create and start the thread
        chart_thread = threading.Thread(target=target)
        chart_thread.start()

        # Wait for the thread to finish or timeout
        chart_thread.join(timeout)

        # If the thread is still alive after the timeout, set the stop event
        if chart_thread.is_alive():
            self.stop_event.set()
            self._logger.warning(f"Chart generation timed out.")
            self._common.write_log(self.log_box, "Chart generation timed out.")
            CTkMessagebox(title="Chart Generation Error", message="One or more charts were cancelled due to a timeout. Please try again later.", icon="cancel", option_1="OK")

    def __reset_stop_event(self):
        self.stop_event.clear()  # Reset the stop event for future calls

    def __generate_graph(self):
        if self._common.check_file_path_errors(self.log_box, self.file_path.get()):
            return

        try:
            self._logger.info(f"Generating chart")
            self._common.write_log(self.log_box, "Generating chart")
            data = Plotter.load_data_from_csv(self.file_path.get())
            Plotter.all_stats(data)

            self.__reset_stop_event()

            if self.total_hours_per_year.get() == "on":
                self.__generate_chart_with_timeout(Plotter.chart_total_hours_per_year, data)
            if self.total_hours_per_month.get() == "on":
                self.__generate_chart_with_timeout(Plotter.chart_total_hours_per_month, data)
            if self.total_hours_by_summary.get() == "on":
                self.__generate_chart_with_timeout(Plotter.chart_total_hours_by_summary, data)
            if self.total_hours_by_summary2.get() == "on":
                self.__generate_chart_with_timeout(Plotter.chart_total_hours_by_summary_pie, data)
            if self.total_hours_per_year_by_summary.get() == "on":
                self.__generate_chart_with_timeout(Plotter.chart_total_hours_per_year_by_summary, data)
            if self.total_hours_per_month_by_summary.get() == "on":
                self.__generate_chart_with_timeout(Plotter.chart_total_hours_per_month_by_summary, data)
            if self.total_hours_per_month_grouped_by_year.get() == "on":
                self.__generate_chart_with_timeout(Plotter.chart_total_hours_per_month_grouped_by_year, data)

        except Exception as error:
            ExceptionHandler.handle_exception(self._common, self.log_box, error)