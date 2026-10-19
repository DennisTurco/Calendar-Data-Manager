from typing import Any

from common.ConfigKeys import ConfigKeys
from common.entities.EventInfo import EventInfo
from common.services.EventsService import EventsService


class EventQueries:
    """UI-agnostic event helpers shared by the desktop and web apps.

    Kept free of tkinter/customtkinter imports so the web app can run where no GUI toolkit
    is installed (e.g. serverless hosts). CommonOperations delegates here for the desktop app.
    """

    @staticmethod
    def get_color_id(color_selected, colors=None) -> int:
        colors = colors if colors is not None else ConfigKeys.Keys.EVENT_COLOR.value
        color_index = 0

        for idx, color in enumerate(colors.keys()):
            if color == color_selected:
                color_index = idx + 1
                break

        # check if the color is valid (it is not set 'No Color Filtering')
        if color_index == 12:  # 'No Color Filtering' has index == 12
            color_index = -1

        return color_index

    @staticmethod
    def get_events(creds, event_info: EventInfo) -> list[Any]:
        if event_info.id is not None and len(event_info.id) != 0:
            return EventsService.fetch_event_by_id(creds, event_info.id)

        return EventsService.fetch_events(creds, event_info)
