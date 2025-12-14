import os
import tkinter as tk

class Images:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.normpath(
            os.path.join(self.base_dir, "..", "common", "assets", "images")
        )

        def img(name: str) -> tk.PhotoImage:
            path = os.path.join(assets_dir, name)
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image not found: {path}")
            return tk.PhotoImage(file=path)
        
        def icon_path(name: str) -> str:
            return os.path.join(assets_dir, name)

        self.calendar_image = img("calendar.png")
        self.google_image = img("google.png")
        self.plus_image = img("plus.png")
        self.list_image = img("list.png")
        self.edit_image = img("edit.png")
        self.chart_image = img("chart.png")
        self.info_image = img("information.png")
        self.icon = img("icon.png")
        self.arrow_image = img("arrow-right2.png")
        self.folder_image = img("folder.png")
        self.file_image = img("file.png")
        self.table_image = img("table.png")
        self.square_image = img("square.png")
        self.square_check_image = img("square-check.png")
        self.buymeacoffe_donation_image = img("donation.png")
        self.paypal_donation_image = img("paypal.png")
        self.github_image = img("github.png")
        self.user_image = img("user.png")
        self.bug_ico = icon_path("bug.ico")
        self.calendar_ico = icon_path("calendar.ico")
        self.folder_ico = icon_path("folder.ico")
        self.icon_ico = icon_path("icon.ico")
        self.information_ico = icon_path("information.ico")
        self.list_ico = icon_path("list.ico")
