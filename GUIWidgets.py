
from tkinter import PhotoImage
import customtkinter as ctk
from CTkScrollableDropdown import *
from CommonOperations import CommonOperations

def create_side_bar_frame(master, plus_image: PhotoImage, edit_image: PhotoImage, list_image: PhotoImage, chart_image: PhotoImage, google_image: PhotoImage, logo_app: PhotoImage):
    sidebar_frame = ctk.CTkFrame(master, width=140, corner_radius=0)
    sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
    sidebar_frame.grid_rowconfigure(6, weight=1)
    
    resized_logo = logo_app.subsample(2, 2)
    # logo_label = ctk.CTkLabel(sidebar_frame, text="", image=resized_logo, width=32, height=32, fg_color="transparent")
    # logo_label.grid(row=0, column=0, padx=(20, 20), pady=(10, 20))
    logo_button = ctk.CTkButton(sidebar_frame, text="", width=32, height=32, fg_color="transparent", image=resized_logo)
    logo_button.grid(row=0, column=0, padx=(20, 20), pady=(10, 20))
    
    title_label = ctk.CTkLabel(sidebar_frame, text="Other Options", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.grid(row=1, column=0, padx=20, pady=(20, 10))
    sidebar_button_1 = ctk.CTkButton(sidebar_frame, image=plus_image, text="New Events")
    sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
    sidebar_button_2 = ctk.CTkButton(sidebar_frame, image=edit_image, text="Edit Events")
    sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
    sidebar_button_3 = ctk.CTkButton(sidebar_frame, image=list_image, text="Get Events List")
    sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
    sidebar_button_4 = ctk.CTkButton(sidebar_frame, image=chart_image, text="Graph")
    sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)
    google_calendar_link = ctk.CTkButton(sidebar_frame, image=google_image, text="Google Calendar")
    google_calendar_link.grid(row=7, column=0, padx=20, pady=(10, 10))
    return (sidebar_button_1, sidebar_button_2, sidebar_button_3, sidebar_button_4, google_calendar_link, logo_button)

def create_date_interval_scroll_frame(master, calendar_image: PhotoImage, timezone: list[str]):
    date_frame = ctk.CTkScrollableFrame(master, label_text="Date Interval")
    date_frame.grid(row=2, column=1, padx=(50, 50), pady=10, sticky="nsew")
    date_frame.grid_columnconfigure((0, 1, 2), weight=1)
    label_date_from = ctk.CTkLabel(date_frame, text="From:")
    label_date_from.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_date_from = ctk.CTkEntry(date_frame, placeholder_text="dd-mm-yyyy hh:mm")
    entry_date_from.grid(row=0, column=1, padx=0, pady=10, sticky="ew")
    entry_date_button = ctk.CTkButton(date_frame, text="", width=10, image=calendar_image)
    entry_date_button.grid(row=0, column=2, padx=0, pady=10, sticky="w")
    label_date_to = ctk.CTkLabel(date_frame, text="To:")
    label_date_to.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_date_to = ctk.CTkEntry(date_frame, placeholder_text="dd-mm-yyyy hh:mm")
    entry_date_to.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
    entry_date_button2 = ctk.CTkButton(date_frame, text="", width=10, image=calendar_image)
    entry_date_button2.grid(row=1, column=2, padx=0, pady=10, sticky="w")
    label_timezone = ctk.CTkLabel(date_frame, text="Timezone:")
    label_timezone.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    timezone_selection = ctk.CTkComboBox(date_frame, state="readonly")
    CTkScrollableDropdown(timezone_selection, values=list(timezone), justify="left", button_color="transparent")
    timezone_selection.set(CommonOperations.get_timezone())
    timezone_selection.grid(row=2, column=1, padx=0, pady=(10, 10), sticky="nsew")
    return (entry_date_from, entry_date_to, timezone_selection, entry_date_button, entry_date_button2)

def create_file_output_scroll_frame_for_events_list_frame(master, folder_image: PhotoImage, file_image: PhotoImage, table_image: PhotoImage):
    file_output_frame = ctk.CTkScrollableFrame(master, label_text="Save results to file")
    file_output_frame.grid(row=3, column=1, padx=(50, 50), pady=10, sticky="ew")
    file_output_frame.grid_columnconfigure(0, weight=1)
    first_row_frame = ctk.CTkFrame(file_output_frame)  # first row
    first_row_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    first_row_frame.grid_columnconfigure((0, 1, 2), weight=1)
    file_path = ctk.CTkEntry(master=first_row_frame, placeholder_text="file path")
    file_path.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    button_file_path = ctk.CTkButton(first_row_frame, text="", width=10, image=folder_image)
    button_file_path.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    overwrite_mode = ctk.CTkCheckBox(first_row_frame, text="Overwrite file", onvalue="on", offvalue="off") # second row
    overwrite_mode.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    third_row_frame = ctk.CTkFrame(file_output_frame)  # third row
    third_row_frame.grid(row=2, column=0, padx=0, pady=0, sticky="ew")
    third_row_frame.grid_columnconfigure((0, 1), weight=1)
    button_open_file = ctk.CTkButton(master=third_row_frame, image=file_image, text="open")
    button_open_file.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    button_open_events_table_preview = ctk.CTkButton(master=third_row_frame, image=table_image, text="table preview")
    button_open_events_table_preview.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    return (file_path, overwrite_mode, button_file_path, button_open_file, button_open_events_table_preview)

def create_file_path_scroll_frame_for_graph_frame(master, folder_image: PhotoImage, file_image: PhotoImage, table_image: PhotoImage, info_image: PhotoImage):
    section_message = '''The Create Graph section of the Calendar Data Manager lets you transform your event data into insightful visualizations for better analysis. Here's what you can do:

• Select File for Analysis: Choose a previously generated `.csv` or `.txt` file that contains your calendar event data. You can preview the file content before proceeding.
• Choose Graph Types: Select from various visualization options, including:
    - Hours per Year
    - Hours by Summary (Bar Chart or Pie Chart)
    - Hours per Month
    - Hours per Year by Summary
    - Hours per Month by Summary

Use the Select All or Deselect All buttons for quick graph type selection.

• Generate Graphs: Once you've set your preferences, click Generate to create the selected graphs. These visualizations help you uncover patterns and trends in your calendar usage, such as how much time you spend on specific activities or summaries over different periods.

This feature is perfect for analyzing productivity, tracking activity trends, and gaining valuable insights from your calendar data.
        '''

    # create main panel
    title_frame = ctk.CTkFrame(master, fg_color="transparent")
    title_frame.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
    title_frame.grid_columnconfigure((0, 1), weight=1)
    ctk.CTkLabel(title_frame, text="Create Graph", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=0, sticky="e")
    ctk.CTkButton(title_frame, text="", width=10, image=info_image,  fg_color="transparent", command=lambda: CommonOperations.open_info_section_dialog(master, "Create Graph", section_message)).grid(row=0, column=1, padx=5, pady=0, sticky="w")

    file_output_frame = ctk.CTkScrollableFrame(master, label_text="Set File Path")
    file_output_frame.grid(row=1, column=1, padx=(50, 50), pady=10, sticky="ew")
    file_output_frame.grid_columnconfigure(0, weight=1)
    first_row_frame = ctk.CTkFrame(file_output_frame) # first row
    first_row_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
    first_row_frame.grid_columnconfigure((0, 1, 2), weight=1)
    file_path = ctk.CTkEntry(master=first_row_frame, placeholder_text="file path")
    file_path.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    button_file_path = ctk.CTkButton(first_row_frame, text="", width=10, image=folder_image)
    button_file_path.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    second_row_frame = ctk.CTkFrame(file_output_frame) # second row
    second_row_frame.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
    second_row_frame.grid_columnconfigure((0, 1), weight=1)
    button_open_file = ctk.CTkButton(master=second_row_frame, image=file_image, text="open")
    button_open_file.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    button_open_events_table_preview = ctk.CTkButton(master=second_row_frame, image=table_image, text="table preview")
    button_open_events_table_preview.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    return (file_path, button_file_path, button_open_file, button_open_events_table_preview)

def create_graph_types_scroll_frame(master, square_check_image: PhotoImage, square_image: PhotoImage):
    graph_types_frame = ctk.CTkScrollableFrame(master, label_text="Set Graph Types")
    graph_types_frame.grid(row=2, column=1, padx=(50, 50), pady=10, sticky="ew")
    graph_types_frame.grid_columnconfigure((0, 1), weight=1)
    graph_types_frame.grid_rowconfigure((0, 1), weight=1)
    button_select_all = ctk.CTkButton(graph_types_frame, text="select all", image=square_check_image)
    button_select_all.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    button_deselect_all = ctk.CTkButton(graph_types_frame, text="deselect all", image=square_image)
    button_deselect_all.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    total_hours_per_year = ctk.CTkCheckBox(graph_types_frame, text="Hours per Year", onvalue="on", offvalue="off")
    total_hours_per_year.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    total_hours_per_year.select()
    total_hours_per_month = ctk.CTkCheckBox(graph_types_frame, text="Hours per Month", onvalue="on", offvalue="off")
    total_hours_per_month.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    total_hours_per_month.select()
    total_hours_by_summary = ctk.CTkCheckBox(graph_types_frame, text="Hours by Summary Bar chart", onvalue="on", offvalue="off")
    total_hours_by_summary.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    total_hours_by_summary.select()
    total_hours_by_summary2 = ctk.CTkCheckBox(graph_types_frame, text="Hours by Summary Pie chart", onvalue="on", offvalue="off")
    total_hours_by_summary2.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    total_hours_by_summary2.select()
    total_hours_per_year_by_summary = ctk.CTkCheckBox(graph_types_frame, text="Hours per Year By Summary", onvalue="on", offvalue="off")
    total_hours_per_year_by_summary.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
    total_hours_per_month_by_summary = ctk.CTkCheckBox(graph_types_frame, text="Hours per Month By Summary", onvalue="on", offvalue="off")
    total_hours_per_month_by_summary.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    return(button_select_all, button_deselect_all, total_hours_per_year, total_hours_per_month, total_hours_by_summary, total_hours_by_summary2, total_hours_per_year_by_summary, total_hours_per_month_by_summary)

def create_date_selection_for_events_list_scroll_frame(master, timezone: list[str], calendar_image: PhotoImage):
    date_frame = ctk.CTkScrollableFrame(master, label_text="Date Interval")
    date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    date_frame.grid_columnconfigure(1, weight=1)
    label_date_from = ctk.CTkLabel(date_frame, text="From:")
    label_date_from.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_date_from = ctk.CTkEntry(date_frame, placeholder_text="dd-mm-yyyy hh:mm")
    entry_date_from.grid(row=0, column=1, padx=0, pady=10, sticky="ew")
    entry_date_button = ctk.CTkButton(date_frame, text="", width=10, image=calendar_image)
    entry_date_button.grid(row=0, column=2, padx=0, pady=10, sticky="w")
    label_date_to = ctk.CTkLabel(date_frame, text="To:")
    label_date_to.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_date_to = ctk.CTkEntry(date_frame, placeholder_text="dd-mm-yyyy hh:mm")
    entry_date_to.grid(row=1, column=1, padx=0, pady=10, sticky="ew")
    entry_date_button2 = ctk.CTkButton(date_frame, text="", width=10, image=calendar_image)
    entry_date_button2.grid(row=1, column=2, padx=0, pady=10, sticky="w")
    label_timezone = ctk.CTkLabel(date_frame, text="Timezone:")
    label_timezone.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    timezone_selection = ctk.CTkComboBox(date_frame, state="readonly")
    CTkScrollableDropdown(timezone_selection, values=list(timezone), justify="left", button_color="transparent")
    timezone_selection.set(CommonOperations.get_timezone())
    timezone_selection.grid(row=2, column=1, padx=0, pady=(10, 10), sticky="nsew")
    return (entry_date_from, entry_date_to, entry_date_button, label_date_to, entry_date_button2, timezone_selection)