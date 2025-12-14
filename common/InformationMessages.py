class InformationMessages:
    new_event_info_message = '''The Create New Event section allows you to quickly add events to your Google Calendar with customized details. Here's how to use it:

• Event Information:
    - Summary: (Required) Enter a brief title or name for your event.
    - Description: (Optional) Add more details to describe the event. This can be helpful for further context, such as the agenda or any notes.
    - Color: (Required) Choose a color to visually categorize your event for easy identification on your calendar.
• Date Interval:
    - From: (Required) Set the starting date and time for the event.
    - To: (Required) Set the ending date and time for the event.
    - Timezone: (Required) Select the timezone in which the event will occur (default is UTC).

Once you've filled in the event details, simply click Create to add the event to your calendar. This tool makes it easy to create events quickly and organize your calendar effectively.
'''

    update_events_info_message = '''This section of the Calendar Data Manager enables you to update multiple events in your Google Calendar simultaneously, saving you time and effort. Here's how it works:

• Filter Existing Events: Use fields such as Summary, Description, Color, and a Date Interval to select the events you want to edit. You can refine your search by combining these criteria.
• Apply New Values: Define the updates you want to make, such as changing the summary, description, or event color.
• Edit with Precision: Specify the date range and timezone to ensure that only the desired events within that period are modified.

Once you've set your filters and new values, click the Edit button to apply the changes instantly across all matching events. This tool ensures a seamless way to manage your calendar efficiently.'''


    get_events_info_message = '''This section of the Calendar Data Manager allows you to efficiently retrieve and analyze your Google Calendar events. Here's what you can do:

• Filter by Date Interval: Specify a time range to narrow down the events you want to retrieve. You can set the start and end dates, along with the timezone, for precise filtering.
• Save Results: Export the retrieved events list to a file in `.csv` or `.txt` format for further analysis or sharing. You can choose the file location, name, and whether to overwrite an existing file.
• Preview Results or Visualize Data: Quickly preview the events in a table or generate graphs directly from the exported file. This feature enables you to gain insights and statistics about your calendar activities.

Once you've configured your filters, click Get to retrieve the data or Get and Plot to visualize it right away!
        '''
    
    graph_info_message = '''The Create Graph section of the Calendar Data Manager lets you transform your event data into insightful visualizations for better analysis. Here's what you can do:

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