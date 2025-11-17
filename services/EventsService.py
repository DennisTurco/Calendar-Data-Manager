from CalendarEventsManager import CalendarEventsManager
from entities.EventInfo import EventInfo

class EventsService:
    def __init__(self, common):
        self.common = common

    def get_connection_setup(self, credentials_path, token_path):
        return CalendarEventsManager.connection_setup(
            credentials_path=credentials_path,
            scopes=CalendarEventsManager.SCOPE,
            token_path=token_path
        )

    def get_user_info(self, credentials):
        return CalendarEventsManager.get_user_info(credentials)

    def fetch_event_by_id(self, event_id):
        return CalendarEventsManager.get_event_by_id(
            creds=self.common.get_credentials_or_exception(),
            event_id=event_id
        )

    def fetch_events(self, event_info: EventInfo):
        return CalendarEventsManager.get_events(
            creds=self.common.get_credentials_or_exception(),
            title=event_info.summary,
            start_date=event_info.range.date_from,
            end_date=event_info.range.date_to,
            color_id=event_info.color,
            description=event_info.description,
            time_zone=event_info.time_zone
        )

    def edit_events(self, event_info: EventInfo, old_events):
        return CalendarEventsManager.edit_event(
            creds=self.common.get_credentials_or_exception(),
            old_events=old_events,
            summary_new=event_info.summary,
            description_new=event_info.description,
            color_id_new=event_info.color,
            time_zone=event_info.time_zone
        )

    def simulate_update_events(self, event_info: EventInfo, old_events):
        return CalendarEventsManager.simulate_event_updates(
            creds=self.common.get_credentials_or_exception(),
            old_events=old_events,
            summary_new=event_info.summary,
            description_new=event_info.description,
            color_id_new=event_info.color,
            time_zone=event_info.time_zone
        )

    def create_event(self, event_info: EventInfo):
        CalendarEventsManager.create_event(
            creds=self.common.get_credentials_or_exception(),
            summary=event_info.summary,
            description=event_info.description,
            start_date=event_info.range.date_from,
            end_date=event_info.range.date_to,
            color_event_id=event_info.color,
        )