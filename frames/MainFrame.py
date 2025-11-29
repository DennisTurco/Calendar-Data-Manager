from enums.FrameTypes import FrameTypes
import webbrowser
import customtkinter as ctk

from ConfigKeys import ConfigKeys
from CommonOperations import CommonOperations
import frames.FrameController as FrameController
from frames.BaseFrame import BaseFrame
from Images import Images

class MainFrame(BaseFrame):
    _common = CommonOperations()

    def __init__(self, parent):
        BaseFrame.__init__(self, parent)
        img = Images()

        title_font = ctk.CTkFont(family="Georgia", weight='bold', slant='italic', size=45)

        ctk.CTkLabel(self, text="", image=img.icon, fg_color="transparent").pack(padx=20, pady=(50, 20))
        ctk.CTkLabel(self, text="Calendar Data Manager", font=title_font, text_color='#e06c29', fg_color="transparent").pack(padx=20, pady=50)
        #ctk.CTkLabel(self, text="Choose the action", fg_color="transparent", font=("Arial", 32)).pack(20, 20)
        ctk.CTkButton(master=self, image=img.plus_image, text="New Events", command=lambda: FrameController.show_frame(FrameTypes.NewEventsFrame, self._common)).pack(padx=20, pady=10, anchor='center')
        ctk.CTkButton(master=self, image=img.edit_image, text="Edit Events", command=lambda: FrameController.show_frame(FrameTypes.EditEventsFrame, self._common)).pack(padx=20, pady=10, anchor='center')
        ctk.CTkButton(master=self, image=img.list_image, text="Get Events", command=lambda: FrameController.show_frame(FrameTypes.GetEventsFrame, self._common)).pack(padx=20, pady=10, anchor='center')
        ctk.CTkButton(master=self, image=img.chart_image, text="Graph", command=lambda: FrameController.show_frame(FrameTypes.GraphFrame, self._common)).pack(padx=20, pady=10, anchor='center')

        button_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        button_frame.pack(side='bottom', anchor='sw', padx=20, pady=10)

        ctk.CTkLabel(self, text=f"Version {ConfigKeys.Keys.VERSION.value}", fg_color="transparent").place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10) # version

        if ConfigKeys.Keys.HOMEBUTTONS_MESSAGESECTION.value:
            ctk.CTkLabel(button_frame, text="If you'd like to learn more about the project or support it:", fg_color="transparent", font=("Arial", 12, "italic")).pack(side='top', anchor='w', pady=(0, 10)) # description

        if ConfigKeys.Keys.HOMEBUTTONS_GITHUB.value:
            github_btn = ctk.CTkButton(master=button_frame, image=img.github_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open(ConfigKeys.Keys.GITHUB_PAGE_LINK.value))
            github_btn.pack(side='left', padx=5)
            self.add_tooltips((github_btn, "Github page"))

        if ConfigKeys.Keys.HOMEBUTTONS_BUYMEACOFFE.value:
            donate_buymeacoffe_btn = ctk.CTkButton(master=button_frame, image=img.buymeacoffe_donation_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_BUYMEACOFFE_PAGE_LINK.value))
            donate_buymeacoffe_btn.pack(side='left', padx=5)
            self.add_tooltips((donate_buymeacoffe_btn, "Donate with \"buy me a coffe\""))

        if ConfigKeys.Keys.HOMEBUTTONS_PAYPAL.value:
            donate__paypal_btn = ctk.CTkButton(master=button_frame, image=img.paypal_donation_image, fg_color="transparent", border_width=1, text="", width=32, height=32, command=lambda: webbrowser.open(ConfigKeys.Keys.DONATE_PAYPAL_PAGE_LINK.value))
            donate__paypal_btn.pack(side='left', padx=5)
            self.add_tooltips((donate__paypal_btn, "Donate with \"Paypal\""))