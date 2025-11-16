import CalendarEventsManager as gc
from entities.EventInfo import EventInfo

class EventsService:
    def __init__(self, common):
        self.common = common

    def get_connection_setup(self, credentials_path, token_path):
        return gc.CalendarEventsManager.connectionSetup(
            credentials_path=credentials_path,
            scopes=gc.CalendarEventsManager.SCOPE,
            token_path=token_path
        )

    def get_user_info(self, credentials):
        return gc.CalendarEventsManager.get_user_info(credentials)

    def fetch_event_by_id(self, event_id):
        return gc.CalendarEventsManager.getEventByID(
            creds=self.common.get_credentials_or_exception(),
            ID=event_id
        )

    def fetch_events(self, event_info: EventInfo):
        return gc.CalendarEventsManager.getEvents(
            creds=self.common.get_credentials_or_exception(),
            title=event_info.summary,
            start_date=event_info.start,
            end_date=event_info.end,
            color_id=event_info.color,
            description=event_info.description,
            time_zone=event_info.time_zone
        )

    def edit_events(self, event_info: EventInfo, old_events):
        return gc.CalendarEventsManager.editEvent(
            creds=self.common.get_credentials_or_exception(),
            old_events=old_events,
            summary_new=event_info.summary,
            description_new=event_info.description,
            color_id_new=event_info.color,
            start_date=event_info.start,
            end_date=event_info.end,
            time_zone=event_info.time_zone
        )

    def simulate_update_events(self, event_info: EventInfo, old_events):
        return gc.CalendarEventsManager.simulateEventUpdates(
            creds=self.common.get_credentials_or_exception(),
            old_events=old_events,
            summary_new=event_info.summary,
            description_new=event_info.description,
            color_id_new=event_info.color,
            start_date=event_info.start,
            end_date=event_info.end,
            time_zone=event_info.time_zone
        )

    def create_event(self, event_info: EventInfo):
        gc.CalendarEventsManager.createEvent(
            creds=self.common.get_credentials_or_exception(),
            summary=event_info.summary,
            description=event_info.description,
            start_date=event_info.start,
            end_date=event_info.end,
            color_event_id=event_info.color,
            timeZone=event_info.time_zone
        )