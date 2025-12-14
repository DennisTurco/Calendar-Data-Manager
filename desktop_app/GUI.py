from io import BytesIO
from desktop_app.enums.FrameTypes import FrameTypes
import webbrowser
import requests
from PIL import Image as pilImage, ImageTk, ImageDraw
import tkinter
import customtkinter as ctk
from CTkMenuBar import *

from common.ConfigKeys import ConfigKeys
from common.services.EventsService import EventsService
from common.LogService import LogService
from common.CommonOperations import CommonOperations
import desktop_app.frames.FrameController as FrameController
from desktop_app.Images import Images
from common.JsonPreferences import JsonPreferences

class App:
    _common = CommonOperations()
    _logger = LogService.get_logger(__name__)

    def __init__(self):
        self.root = ctk.CTk()
        self._menu = None
        self.dropdown5 = None
        self._button_5 = None

        ConfigKeys.load_values_from_json()
        self._logger.info("Application started")
        self.__read_data_from_last_session()
        self.__init_window()
        self.__init_menu()
        FrameController.page_controller(self, self.root, self._common)
        self.root.mainloop()

    def __read_data_from_last_session(self):
        list_res = JsonPreferences.read_from_json()

        if not isinstance(list_res, dict) or len(list_res) <= 0:
            return

        self.credentials_path = list_res["CredentialsPath"]
        self.token_path = list_res["TokenPath"]
        try:
            self.credentials = EventsService.get_connection_setup(self.credentials_path, self.token_path)
        except Exception as e:
            print(f"Error: {e}")

    def __init_window(self):
        self.root.iconbitmap(Images().icon_ico)

        self.root.title("Calendar Data Manager")
        CommonOperations.center_window(self.root, ConfigKeys.Keys.APP_WIDTH.value, ConfigKeys.Keys.APP_HEIGHT.value)
        self.root.minsize(1100, 900)

        list_res = JsonPreferences.read_from_json()

        if not isinstance(list_res, dict) or len(list_res) <= 0:
            return

        try:
            appearance = list_res["Appearance"]
            CommonOperations.change_appearance(appearance)
        except (TypeError, ValueError, KeyError): pass
        try:
            text_scaling = list_res["TextScaling"]
            CommonOperations.change_scaling_event(text_scaling)
        except (TypeError, ValueError, KeyError): pass
        try:
            color_theme = list_res["ColorTheme"]
            CommonOperations.change_color_theme(color_theme)
        except (TypeError, ValueError, KeyError): pass

    def __init_menu(self):
        self._menu = CTkMenuBar(self.root)
        button_1 = self._menu.add_cascade("File")
        button_3 = self._menu.add_cascade("Settings")
        button_4 = self._menu.add_cascade("About")
        button_6 = self._menu.add_cascade("Help")

        if self._common.get_credentials_or_none() is not None:
            self.update_username_menu_item()

        dropdown1 = CustomDropdownMenu(widget=button_1)

        if ConfigKeys.Keys.MENUITEM_EXIT.value:
            dropdown1.add_option(option="Exit", command=lambda: exit())

        dropdown1.add_separator()

        dropdown3 = CustomDropdownMenu(widget=button_3)

        if ConfigKeys.Keys.MENUITEM_APPEARANCE.value:
            sub_menu2 = dropdown3.add_submenu("Appearance")
            sub_menu2.add_option(option="Dark", command=lambda: self.__change_app_appearance("dark"))
            sub_menu2.add_option(option="Light", command=lambda: self.__change_app_appearance("light"))

        if ConfigKeys.Keys.MENUITEM_SCALING.value:
            sub_menu3 = dropdown3.add_submenu("Scaling")
            sub_menu3.add_option(option="120%", command=lambda: CommonOperations.change_scaling_event("120"))
            sub_menu3.add_option(option="110%", command=lambda: CommonOperations.change_scaling_event("110"))
            sub_menu3.add_option(option="100%", command=lambda: CommonOperations.change_scaling_event("100"))
            sub_menu3.add_option(option="90%", command=lambda: CommonOperations.change_scaling_event("90"))
            sub_menu3.add_option(option="80%", command=lambda: CommonOperations.change_scaling_event("80"))
            sub_menu3.add_option(option="70%", command=lambda: CommonOperations.change_scaling_event("70"))

        if ConfigKeys.Keys.MENUITEM_THEME.value:
            sub_menu4 = dropdown3.add_submenu("Theme")
            sub_menu4.add_option(option="Blue", command=lambda: CommonOperations.set_color_theme("blue"))
            sub_menu4.add_option(option="Dark Blue", command=lambda: CommonOperations.set_color_theme("dark-blue"))
            sub_menu4.add_option(option="Green", command=lambda: CommonOperations.set_color_theme("green"))

        dropdown4 = CustomDropdownMenu(widget=button_4)
        if ConfigKeys.Keys.SHARD_WEBSITE.value:
            dropdown4.add_option(option="Website", command=lambda: webbrowser.open(ConfigKeys.Keys.SHARD_WEBSITE.value))
        if ConfigKeys.Keys.MENUITEM_SHARE.value:
            dropdown4.add_option(option="Share", command=lambda: webbrowser.open(ConfigKeys.Keys.GITHUB_PAGE_LINK.value))
        if ConfigKeys.Keys.MENUITEM_DONATE.value:
            sub_menu4 = dropdown4.add_submenu("Support this project")
            sub_menu4.add_option(option="Donate with \"Buy me a coffe\"", command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_BUYMEACOFFE_PAGE_LINK.value))
            sub_menu4.add_option(option="Donate with \"Paypal\"", command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_PAYPAL_PAGE_LINK.value))

        dropdown6 = CustomDropdownMenu(widget=button_6)
        if ConfigKeys.Keys.MENUITEM_SUPPORT.value:
            subject: str = "Calendar Data Manager - Support"
            dropdown6.add_option(option="Support", command=lambda: webbrowser.open(f"mailto:{ConfigKeys.Keys.SHARD_EMAIL.value}?subject={subject}"))
        if ConfigKeys.Keys.MENUITEM_BUGREPORT.value:
            dropdown6.add_option(option="Report a bug", command=lambda: webbrowser.open(ConfigKeys.Keys.GITHUB_ISSUES_LINK.value))

    def update_username_menu_item(self):
        # Configure column 4 to expand (to align right).
        self._menu.columnconfigure(4, weight=1)

        credentials = self._common.get_credentials_or_none()
        if credentials is not None:
            (_, email, picture_url) = EventsService.get_user_info(credentials)
            user_image = self.__load_profile_icon_with_fallback(picture_url)

            if self._button_5 is not None:
                self._button_5.configure(text=str(email), image=user_image)
                self._button_5.grid(row=0, column=4, padx=10, pady=10, sticky="e")
            else:
                self._button_5 = ctk.CTkButton(self._menu, text=str(email), fg_color="transparent", image=user_image, command=self.__show_user_menu)
                self._button_5.grid(row=0, column=4, padx=10, pady=10, sticky="e")
                self.dropdown5 = CustomDropdownMenu(widget=self._button_5)
                self.dropdown5.add_option(option="Google Calendar", command=lambda: webbrowser.open(ConfigKeys.Keys.GOOGLE_CALENDAR_LINK.value))
                self.dropdown5.add_option(option="Log out", command=lambda: self.__log_out())

            self.__change_app_appearance_profile()

        else:
            self.__forget_username_menu_item()

    def __load_profile_icon_with_fallback(self, picture_url) -> ImageTk.PhotoImage | tkinter.PhotoImage:
        default_user_image = Images().user_image
        res = self.__get_user_image_from_url(picture_url)
        return res if (picture_url and res is not None) else default_user_image

    @staticmethod
    def __get_user_image_from_url(url) -> ImageTk.PhotoImage | None:
        try:
            response = requests.get(url)
            response.raise_for_status()  # check if the request is correct
            img_data = response.content

            # load the image
            image = pilImage.open(BytesIO(img_data))
            image = image.resize((32, 32), pilImage.LANCZOS)

            # create a mask for the image
            mask = pilImage.new('L', (32, 32), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 32, 32), fill=255)

            # apply the mask
            image = image.convert("RGBA")
            image.putalpha(mask)

            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def __show_user_menu(self):
        self.dropdown5.show()

    def __forget_username_menu_item(self):
        if self._button_5 is not None:
            self._button_5.grid_forget()

    def __log_out(self):
        self._logger.info(f"Logging out")
        self.__forget_username_menu_item()
        FrameController.show_frame(FrameTypes.LoginFrame)

    def __change_app_appearance(self, mode: str):
        self._common.change_appearance(mode)
        self.__change_app_appearance_profile(mode)

    def __change_app_appearance_profile(self, appearance: str = ''):
        self._logger.info(f"Changing appearance to {appearance}")

        if appearance is None or appearance == '':
            appearance = CommonOperations.get_appearance()

        if appearance.lower() == 'light':
            self._button_5.configure(text_color="black")
        elif appearance.lower() == 'dark':
            self._button_5.configure(text_color="white")
        else:
            self._button_5.configure(text_color="#76797e")
