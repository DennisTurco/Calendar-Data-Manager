from typing import Any
from common.CalendarEventsManager import CalendarEventsManager
from common.entities.EventInfo import EventInfo

class EventsService:
    @staticmethod
    def get_connection_setup(credentials_path, token_path):
        return CalendarEventsManager.connection_setup(
            credentials_path=credentials_path,
            scopes=CalendarEventsManager.SCOPE,
            token_path=token_path
        )

    @staticmethod
    def get_user_info(credentials):
        return CalendarEventsManager.get_user_info(credentials)

    @staticmethod
    def fetch_event_by_id(creds, event_id) -> list[Any]:
        return CalendarEventsManager.get_event_by_id(
            creds=creds,
            event_id=event_id
        )

    @staticmethod
    def fetch_events(creds, event_info: EventInfo) -> list[Any]:
        return CalendarEventsManager.get_events(
            creds=creds,
            title=event_info.summary,
            start_date=event_info.range.date_from,
            end_date=event_info.range.date_to,
            color_id=event_info.color,
            description=event_info.description,
            time_zone=event_info.time_zone
        )

    @staticmethod
    def edit_events(creds, event_info: EventInfo, old_events) -> list | None:
        return CalendarEventsManager.edit_event(
            creds=creds,
            old_events=old_events,
            summary_new=event_info.summary,
            description_new=event_info.description,
            color_id_new=event_info.color,
            time_zone=event_info.time_zone
        )

    @staticmethod
    def simulate_update_events(creds, event_info: EventInfo, old_events) -> list:
        return CalendarEventsManager.simulate_event_updates(
            creds=creds,
            old_events=old_events,
            summary_new=event_info.summary,
            description_new=event_info.description,
            color_id_new=event_info.color,
            time_zone=event_info.time_zone
        )

    @staticmethod
    def create_event(creds, event_info: EventInfo) -> None:
        CalendarEventsManager.create_event(
            creds=creds,
            summary=event_info.summary,
            description=event_info.description,
            start_date=event_info.range.date_from,
            end_date=event_info.range.date_to,
            color_event_id=event_info.color,
        )