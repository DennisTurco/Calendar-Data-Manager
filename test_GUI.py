import unittest
from unittest.mock import MagicMock, Mock, patch
import tkinter as tk
import tkinter
from datetime import datetime

import tkinter as tk
from tkinter import filedialog

from GUI import App  # module name
from GUI import SetupFrame # module name
from GUI import MainFrame # module name
from GUI import GraphFrame # module name
from GUI import EditEventsFrame # module name
from GUI import GetEventsFrame # module name
from GUI import NewEventsFrame # module name

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = App()
        
    def tearDown(self):
        if hasattr(self.app, "root") and self.app.root is not None:
            self.app.root.destroy()

    def test_init_window(self):
        self.assertEqual(self.app.root.iconbitmap(), './imgs/icon.ico')
        self.assertEqual(self.app.root.title(), "Google Calendar Data Manager")
        self.assertEqual(self.app.root.winfo_width(), 1100)
        self.assertEqual(self.app.root.winfo_height(), 900)

    def test_init_menu(self):
        self.assertIsNotNone(self.app.root.menu)

        # Simulate menu clicks
        self.app.root.menu.invoke(0)  # Click on "New Credentials"
        self.assertEqual(self.app.show_frame(SetupFrame), self.app.frames[SetupFrame])

        self.app.root.menu.invoke(2)  # Click on "About" submenu "Appearance" -> "Dark"
        self.assertEqual(self.app.root.option_add('*TButton*highlightBackground', '#2d2d2d'), None)

    # Add more test cases as needed


class TestSetupFrame(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.setup_frame = SetupFrame(self.root, Mock())

    def tearDown(self):
        if self.setup_frame.toplevel_window:
            self.setup_frame.toplevel_window.destroy()
        self.root.destroy()

    def test_setCredentialsPathFrame(self):
        self.assertIsNone(self.setup_frame.toplevel_window)

        # Simulate button press
        with patch.object(self.setup_frame, 'toplevel_window', None):
            self.setup_frame.setCredentialsPathFrame()
        self.assertIsNotNone(self.setup_frame.toplevel_window)
        self.assertTrue(self.setup_frame.toplevel_window.winfo_exists())

    def test_setCredentialsPath(self):
        # Simulate button press
        self.setup_frame.file_path.delete(0, tk.END)
        self.setup_frame.file_path.insert(0, '/path/to/credentials.json')
        with patch('your_module_name.os.remove') as mock_remove, \
             patch('your_module_name.gc.GoogleCalendarEventsManager.connectionSetup') as mock_connection_setup, \
             patch('your_module_name.CTkMessagebox') as mock_messagebox:
            
            mock_connection_setup.return_value = Mock()
            mock_messagebox.return_value.get.return_value = "Ok"

            self.setup_frame.__setCredentialsPath()

            mock_connection_setup.assert_called_once_with('/path/to/credentials.json', ['https://www.googleapis.com/auth/calendar'], '/path/to/token.json')
            mock_remove.assert_not_called()
            mock_messagebox.assert_called_once_with(message="Credentials setted successfully", icon="check", option_1="Ok")
            self.assertTrue(self.setup_frame.main_class.set_credentials.called)

        # Test exception case
        with patch('your_module_name.os.remove') as mock_remove, \
             patch('your_module_name.gc.GoogleCalendarEventsManager.connectionSetup') as mock_connection_setup, \
             patch('your_module_name.CTkMessagebox') as mock_messagebox:

            mock_connection_setup.side_effect = Exception("Test exception")
            mock_messagebox.return_value.get.return_value = "Yes"

            self.setup_frame.__setCredentialsPath()

            mock_connection_setup.assert_called_once()
            mock_remove.assert_not_called()
            mock_messagebox.assert_called_once_with(title="Credentials error", message="Do you wish to retry?", icon="cancel", option_1="No", option_2="Yes")
            self.assertTrue(self.setup_frame.setCredentialsPathFrame.called)

    def test_getFilePath(self):
        with patch.object(filedialog, 'askopenfilename', return_value='/path/to/credentials.json'):
            self.assertEqual(self.setup_frame.__getFilePath(), '/path/to/credentials.json')
            self.assertEqual(self.setup_frame.file_path.get(), '/path/to/credentials.json')

    # Add more test cases as needed
    

class TestMainFrame(unittest.TestCase):

    def setUp(self):
        # Initialize a sample main_class object
        self.sample_main_class = MagicMock()

    @patch('your_module_name.customtkinter.CTkButton')
    def test_init(self, mock_ctk_button):
        # Create an instance of MainFrame
        main_frame = MainFrame(MagicMock(), self.sample_main_class)

        # Check if CTkButton was called with the correct parameters
        mock_ctk_button.assert_any_call(master=main_frame, image=MagicMock(), text="New Events", command=main_frame.go_to_new_events_frame)
        mock_ctk_button.assert_any_call(master=main_frame, image=MagicMock(), text="Edit Events", command=main_frame.go_to_edit_events_frame)
        mock_ctk_button.assert_any_call(master=main_frame, image=MagicMock(), text="Get Events", command=main_frame.go_to_get_events_by_title_frame)
        mock_ctk_button.assert_any_call(master=main_frame, image=MagicMock(), text="Graph", command=main_frame.go_to_graph_frame)

    def test_go_to_new_events_frame(self):
        # Create an instance of MainFrame
        main_frame = MainFrame(MagicMock(), self.sample_main_class)

        # Call the method
        main_frame.go_to_new_events_frame()

        # Check if show_frame was called with the correct argument
        self.sample_main_class.show_frame.assert_called_once_with("NewEventsFrame")

    def test_go_to_edit_events_frame(self):
        # Create an instance of MainFrame
        main_frame = MainFrame(MagicMock(), self.sample_main_class)

        # Call the method
        main_frame.go_to_edit_events_frame()

        # Check if show_frame was called with the correct argument
        self.sample_main_class.show_frame.assert_called_once_with("EditEventsFrame")

    def test_go_to_get_events_by_title_frame(self):
        # Create an instance of MainFrame
        main_frame = MainFrame(MagicMock(), self.sample_main_class)

        # Call the method
        main_frame.go_to_get_events_by_title_frame()

        # Check if show_frame was called with the correct argument
        self.sample_main_class.show_frame.assert_called_once_with("GetEventsFrame")

    def test_go_to_graph_frame(self):
        # Create an instance of MainFrame
        main_frame = MainFrame(MagicMock(), self.sample_main_class)

        # Call the method
        main_frame.go_to_graph_frame()

        # Check if show_frame was called with the correct argument
        self.sample_main_class.show_frame.assert_called_once_with("GraphFrame")

class TestGraphFrame(unittest.TestCase):

    def setUp(self):
        # Initialize a sample main_class object
        self.sample_main_class = MagicMock()

    @patch('your_module_name.customtkinter.CTkButton')
    @patch('your_module_name.customtkinter.CTkLabel')
    @patch('your_module_name.customtkinter.CTkTextbox')
    @patch('your_module_name.customtkinter.CTkEntry')
    @patch('your_module_name.filedialog.askopenfilename')
    def test_init(self, mock_askopenfilename, mock_ctk_entry, mock_ctk_textbox, mock_ctk_label, mock_ctk_button):
        # Configure mocks
        mock_askopenfilename.return_value = '/path/to/sample/file.txt'

        # Create an instance of GraphFrame
        graph_frame = GraphFrame(MagicMock(), self.sample_main_class)

        # Check if CTkButton was called with the correct parameters
        mock_ctk_button.assert_any_call(command=graph_frame.go_to_new_events_frame, image=MagicMock(), text="New Events")
        mock_ctk_button.assert_any_call(command=graph_frame.go_to_edit_events_frame, image=MagicMock(), text="Edit Events")
        mock_ctk_button.assert_any_call(command=graph_frame.go_to_get_events_by_title_frame, image=MagicMock(), text="Get Events List")
        mock_ctk_button.assert_any_call(command=graph_frame.go_to_graph_frame, image=MagicMock(), text="Graph")

        # Check if CTkLabel was called with the correct parameters
        mock_ctk_label.assert_any_call(text="Other Options", font=MagicMock())
        mock_ctk_label.assert_any_call(text="Create Graph", font=MagicMock())

        # Check if CTkTextbox was called with the correct parameters
        mock_ctk_textbox.assert_called_once_with(graph_frame, width=250, height=100)
        mock_ctk_textbox.return_value.bind.assert_called_once_with("<Key>", mock_ctk_textbox.return_value)

        # Check if CTkEntry was called with the correct parameters
        mock_ctk_entry.assert_called_once_with(master=mock_ctk_entry.return_value, placeholder_text="file path")

        # Check if CTkButton for file path was called with the correct parameters
        mock_ctk_button.assert_called_with(graph_frame.file_output_frame, text="", width=10, image=MagicMock(), command=graph_frame.get_file_path)

    @patch('your_module_name.Plotter.Plotter.loadData')
    @patch('your_module_name.Plotter.Plotter.graph')
    def test_generate_graph(self, mock_graph, mock_load_data):
        # Create an instance of GraphFrame
        graph_frame = GraphFrame(MagicMock(), self.sample_main_class)

        # Configure mocks
        mock_load_data.return_value = [(1, 2), (2, 4), (3, 6)]

        # Set file path
        graph_frame.file_path.insert(0, '/path/to/sample/file.txt')

        # Call the method
        graph_frame.generate_graph()

        # Check if the write_log method was called
        self.sample_main_class.write_log.assert_called_once()

        # Check if the Plotter.Plotter.loadData and Plotter.Plotter.graph methods were called
        mock_load_data.assert_called_once_with('/path/to/sample/file.txt')
        mock_graph.assert_called_once_with([(1, 2), (2, 4), (3, 6)])

    @patch('your_module_name.CTkMessagebox')
    @patch('your_module_name.filedialog.askopenfilename')
    def test_open_file(self, mock_askopenfilename, mock_ctk_messagebox):
        # Configure mocks
        mock_askopenfilename.return_value = '/path/to/sample/file.txt'

        # Create an instance of GraphFrame
        graph_frame = GraphFrame(MagicMock(), self.sample_main_class)

        # Call the method
        graph_frame.open_file()

        # Check if file_viewer_window was called with the correct parameters
        self.sample_main_class.file_viewer_window.assert_called_once_with(None, '/path/to/sample/file.txt', graph_frame.log_box)

    @patch('your_module_name.filedialog.askopenfilename')
    def test_get_file_path(self, mock_askopenfilename):
        # Configure mocks
        mock_askopenfilename.return_value = '/path/to/sample/file.txt'

        # Create an instance of GraphFrame
        graph_frame = GraphFrame(MagicMock(), self.sample_main_class)

        # Call the method
        graph_frame.get_file_path()

        # Check if the file_path entry was updated with the correct value
        self.assertEqual(graph_frame.file_path.get(), '/path/to/sample/file.txt')

        # Check if the write_log method was called
        self.sample_main_class.write_log.assert_called_once()

    def test_combobox_callback(self):
        # Create an instance of GraphFrame
        graph_frame = GraphFrame(MagicMock(), self.sample_main_class)

        # Mock event_color
        mock_event_color = MagicMock()

        # Call the method
        graph_frame.combobox_callback(mock_event_color)

        # Check if the color_preview configure method was called with the correct parameters
        graph_frame.color_preview.configure.assert_called_once_with(bg=mock_event_color)

        # Check if the write_log method was called
        self.sample_main_class.write_log.assert_called_once()
        
class TestGetEventsFrame(unittest.TestCase):

    def setUp(self):
        # Mocking tkinter.Tk() to avoid opening a GUI window during testing
        patcher = patch('tkinter.Tk')
        self.mock_tk = patcher.start()
        self.addCleanup(patcher.stop)

    def test_get_events(self):
        # Replace 'YourMainClass' with the actual class used in main_class parameter
        main_class_instance = App()  # Create an instance of YourMainClass
        get_events_frame = GetEventsFrame(tkinter.Tk(), main_class_instance)

        # Mocking the entry values
        get_events_frame.entry_id.insert(0, "your_test_id")
        get_events_frame.entry_summary.insert(0, "your_test_summary")
        get_events_frame.entry_date_from.insert(0, "2024-01-26 08:00")
        get_events_frame.entry_date_to.insert(0, "2024-01-27 08:00")
        get_events_frame.entry_description.insert(tkinter.END, "your_test_description")

        # Mocking Google Calendar API call
        with patch('your_module.gc.GoogleCalendarEventsManager.getEvents') as mock_get_events:
            mock_get_events.return_value = [{'id': 'event_id_1', 'summary': 'Event 1'}]  # Replace with your expected data

            # Call the get_events method
            get_events_frame.get_events()

            # Assert that the events were obtained successfully
            self.assertIsNotNone(get_events_frame.events)
            self.assertEqual(len(get_events_frame.events), 1)

    # Add more test cases for different scenarios as needed
    

class TestEditEventsFrame(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.main_class = Mock()
        self.edit_events_frame = EditEventsFrame(self.root, self.main_class)

    def tearDown(self):
        self.root.destroy()

    @patch('your_module.GoogleCalendarEventsManager.editEvent')
    @patch('your_module.GoogleCalendarEventsManager.get_credentials')
    def test_edit_event(self, mock_get_credentials, mock_edit_event):
        # Mocking return values
        mock_get_credentials.return_value = 'dummy_credentials'
        mock_edit_event.return_value = ['event1', 'event2']  # Replace with expected return values

        # Set up initial values in the frame
        self.edit_events_frame.entry_summary_old.insert(0, 'Old Summary')
        self.edit_events_frame.entry_description_old.insert('1.0', 'Old Description')
        self.edit_events_frame.multi_selection_old.set('Lavender')

        self.edit_events_frame.entry_summary_new.insert(0, 'New Summary')
        self.edit_events_frame.entry_description_new.insert('1.0', 'New Description')
        self.edit_events_frame.multi_selection_new.set('Sage')

        self.edit_events_frame.entry_date_from.insert(0, '2022-01-01 12:00')
        self.edit_events_frame.entry_date_to.insert(0, '2022-01-02 12:00')
        self.edit_events_frame.timezone_selection.set('America/New_York')

        # Call the method to be tested
        self.edit_events_frame.edit_event()

        # Assertions based on expected behavior
        mock_get_credentials.assert_called_once()
        mock_edit_event.assert_called_once_with(
            'dummy_credentials',
            'Old Summary',
            'Old Description',
            0,  # Replace with the expected color index for 'Lavender'
            'New Summary',
            'New Description',
            1,  # Replace with the expected color index for 'Sage'
            datetime(2022, 1, 1, 12, 0),
            datetime(2022, 1, 2, 12, 0),
            'America/New_York'
        )

        # Add more assertions based on the expected behavior of your application
        
class TestNewEventsFrame(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.main_class = MockMainClass()  # You might need to create a mock for your main class
        self.frame = NewEventsFrame(self.root, self.main_class)

    def tearDown(self):
        self.root.destroy()

    def test_widgets_existence(self):
        self.assertIsInstance(self.frame.sidebar_frame, tkinter.Frame)
        self.assertIsInstance(self.frame.title_label, tkinter.Label)
        # Add more assertions for other widgets

    def test_create_event(self):
        # Mock user input
        self.frame.entry_summary.insert(0, "Test Event")
        self.frame.entry_date_from.insert(0, "2024-01-27 10:00")
        self.frame.entry_date_to.insert(0, "2024-01-27 12:00")
        self.frame.timezone_selection.set("UTC")

        # Mock the Google Calendar Events Manager
        with patch('your_module.GoogleCalendarEventsManager.createEvent') as mock_create_event:
            mock_create_event.return_value = None
            self.frame.create_event()

        # Assertions
        mock_create_event.assert_called_once()
        args, kwargs = mock_create_event.call_args
        self.assertEqual(args[0], self.main_class.get_credentials())  # Assuming get_credentials returns something valid
        self.assertEqual(args[1], "Test Event")
        # Add more assertions for other arguments

    def test_combobox_callback(self):
        # Mock user selection
        self.frame.multi_selection.set("Sage")
        self.frame.combobox_callback(self.frame.multi_selection.get())

        # Assertion
        self.assertEqual(self.frame.color_preview['bg'], self.frame.event_color["Sage"])

    def test_date_picker(self):
        with patch.object(self.frame.main_class, 'date_picker_window') as mock_date_picker_window:
            self.frame.date_picker(1)

        # Assertion
        mock_date_picker_window.assert_called_once()

    def test_go_to_new_events_frame(self):
        with patch.object(self.frame.main_class, 'show_frame') as mock_show_frame:
            self.frame.go_to_new_events_frame()

        # Assertion
        mock_show_frame.assert_called_once_with(NewEventsFrame)

# MockMainClass is used to simulate the behavior of the main class.
class MockMainClass:
    def get_credentials(self):
        # Replace with your actual implementation
        pass

    def get_timezone(self):
        # Replace with your actual implementation
        pass

    def set_timezone(self, timezone):
        # Replace with your actual implementation
        pass

    def get_color_id(self, event_color, color):
        # Replace with your actual implementation
        pass

    def write_log(self, log_box, message):
        # Replace with your actual implementation
        pass

    def messagebox_exception(self, exception):
        # Replace with your actual implementation
        pass

    def date_picker_window(self, type, toplevel_window, entry_date_from, entry_date_to, log_box):
        # Replace with your actual implementation
        pass

if __name__ == '__main__':
    unittest.main()
