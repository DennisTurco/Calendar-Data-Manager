import datetime
import requests
import os.path
from typing import Dict

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from Logger import Logger

class CalendarEventsManager:
    
    SCOPE = [
        'https://www.googleapis.com/auth/calendar',
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    
    @staticmethod
    def get_user_info(credentials: Credentials):
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()

        name = user_info.get('name')
        email = user_info.get('email')
        picture_url = user_info.get('picture')

        Logger.write_log(f"User '{name}' logged with email '{email}'", Logger.LogType.INFO)

        return name, email, picture_url
    
    @staticmethod
    def connectionSetup(credentials_path: str, scopes: str, token_path: str) -> Credentials:
        if token_path == None or len(token_path) == 0: raise ValueError("Token path can't be empty")
        if credentials_path == None or len(credentials_path) == 0: raise ValueError("Credentials path can't be empty")
        if scopes == None or len(scopes) == 0: raise ValueError("Scopes link can't be empty")
        
        credentials = None
        
        if os.path.exists(token_path):
            credentials = Credentials.from_authorized_user_file(token_path)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())  # Refresh the token
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                    credentials = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Errore: {e}")
                    return None
                
            with open(token_path, "w") as token:
                token.write(credentials.to_json())
        
        return credentials
    
    # TODO: Test me
    @staticmethod
    def refreshToken():
        client_secret = "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"
        client_id = "629129916032-161pnnbejkg238auc0rethmlg1njc6om.apps.googleusercontent.com"
        refresh_token = "1//09PbgtBFQPy8dCgYIARAAGAkSNwF-L9IreGgrAtTftppccc4ClFOpbEBq3G6rAJ11uUbvX8roppBgsrvHXBx88QEn5pJh2A5Nols"
        token_url = 'https://oauth2.googleapis.com/token'
        
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            new_access_token = token_data['access_token']
            new_refresh_token = token_data.get('refresh_token', refresh_token)

            # Use the new access token for Google Calendar API requests.
            print(new_access_token)
            print(new_refresh_token)
        else:
            print("Error refreshing access token:", response.text)
 
    @staticmethod
    def createEvent(creds: Credentials, summary: str, description: str, start_date: datetime, end_date: datetime, color_event_id: int = 1, timeZone: str = 'UTC'):
        if creds == None: raise ValueError("Credentials can't be null")
        
        service = build("calendar", "v3", credentials=creds)
        
        # set the event
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_date.isoformat(),
                'timeZone': timeZone,
            },
            'end': {
                'dateTime': end_date.isoformat(),
                'timeZone': timeZone,
            },
            'colorId': color_event_id,
        }

        # create the event
        service.events().insert(calendarId='primary', body=event).execute()
    
    @staticmethod
    def getTitleByID(creds: Credentials, ID: str) -> str:
        if creds == None: raise ValueError("Credentials can't be null")
        if ID == None: raise ValueError("ID can't be null")
        
        try:
            # Call the Google Calendar API to get the event by ID
            service = build("calendar", "v3", credentials=creds)
            event = service.events().get(calendarId='primary', eventId=ID).execute()
            
            title = event['summary'] # Extract and return the event title
            return title
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")

    
    @staticmethod
    def getTitleByDate(creds: Credentials, start_date: str, end_date: str) -> str:
        if creds == None: raise ValueError("Credentials can't be null")
        if start_date == None or end_date == None: raise ValueError("Date can't be empty")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_date,
                timeMax=end_date,
                maxResults=1,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            if events:
                event = events[0]
                title = event.get('summary', '')
                return title
            else:
                return None
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    @staticmethod
    def getIDByTitle(creds: Credentials, title: str) -> str:
        if creds == None: raise ValueError("Credentials can't be null")
        if title == None: raise ValueError("Title can't be empty")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            events_result = service.events().list(
                calendarId='primary',
                q=title,
                maxResults=1,
                singleEvents=True,
            ).execute()
            
            events = events_result.get('items', [])
            
            if events:
                event = events[0]
                ID = event['id']
                return ID
            else:
                return None  
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    @staticmethod
    def getIDByDate(creds: Credentials, start_date: str, end_date: str):
        if creds == None: raise ValueError("Credentials can't be null")
        if start_date == None or end_date == None: raise ValueError("Date can't be empty")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_date,
                timeMax=end_date,
                maxResults=1,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            if events:
                event = events[0]
                ID = event['id']
                return ID
            else:
                return None
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    @staticmethod
    def getDescriptionByID(creds: Credentials, ID: str) -> str:
        if creds == None: raise ValueError("Credentials can't be null")
        if ID == None: raise ValueError("ID can't be null")
        
        try:
            # Call the Google Calendar API to get the event by ID
            service = build("calendar", "v3", credentials=creds)
            event = service.events().get(calendarId='primary', eventId=ID).execute()
            
            description = event.get('description') # Extract and return the event description
            return description
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")        
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    # TODO: test 
    # TODO: add like mode
    @staticmethod
    def getAllDescriptionsByTitle(creds: Credentials, title: str, like_mode: bool = False):
        if creds == None: raise ValueError("Credentials can't be null")
        if title == None: raise ValueError("Title can't be null")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            events = []
            
            now = datetime.datetime.now().isoformat() + "Z"
            start_date_search = None 
            end_date_search = None
            while (True):
                # set the events list
                events_result = service.events().list(
                    calendarId="primary", 
                    maxResults=500, 
                    timeMin=start_date_search, 
                    timeMax=now, 
                    singleEvents=True, 
                    orderBy="startTime").execute()
                
                events = events + events_result.get('items', [])
                
                # i quit if i found all the events -> it happens when the date of the last element inside the list is the same for two times
                if events[len(events)-1]['end'].get('dateTime') == end_date_search:
                    break

                end_date_search = events[len(events)-1]['end'].get('dateTime')
                
                start_date_search = end_date_search
            
            if events:
                return events
            else:
                return None  
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    @staticmethod
    def getEventByID(creds: Credentials, ID: str):
        if creds == None: raise ValueError("Credentials can't be null")
        if ID == None: raise ValueError("ID can't be null")
        
        try:
            # Call the Google Calendar API to get the event by ID
            service = build("calendar", "v3", credentials=creds)
            event = service.events().get(calendarId='primary', eventId=ID).execute()
            
            if event is not None:
                return [event]  # Wrap the event in a list
            else:
                return None
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    # TODO: add like mode for title and description
    @staticmethod
    def getEvents(creds: Credentials, title: str = None, like_mode: bool = False, description: str = None, start_date: str = None, end_date: str = None, time_zone: str = 'UTC', color_id: int = -1):
        if creds is None: raise ValueError("Credentials can't be null")

        try:
            service = build("calendar", "v3", credentials=creds)
            events = []

            start_date_time = None
            end_date_time = None
            end_date_time_search = None

            if start_date:
                # Check if start_date is already a datetime object
                if isinstance(start_date, datetime.datetime):
                    start_date_time = start_date.isoformat() + 'Z'

            if end_date:
                # Check if end_date is already a datetime object
                if isinstance(end_date, datetime.datetime):
                    end_date_time = end_date.isoformat() + 'Z'
            elif end_date is None or len(end_date) == 0:
                # Parsing and formatting end_date
                end_date_time = datetime.datetime.now().isoformat() + "Z"

            end_date_time_search = end_date_time

            while True:
                events_result = service.events().list(
                    calendarId="primary",
                    maxResults=2500,
                    timeMin=start_date_time,
                    timeMax=end_date_time,
                    singleEvents=True,
                    orderBy="startTime",
                    timeZone=time_zone,
                    fields="items"
                ).execute()

                if title != None and len(title) > 0:
                    events += [event for event in events_result.get('items', []) if title.lower() in event.get('summary', '').lower()]
                else:
                    events += [event for event in events_result.get('items', [])]

                if len(events) == 0:
                    return None

                # Exit if all events are found (when the date of the last element inside the list is the same for two times)
                if events[-1]['end'].get('dateTime') == end_date_time_search:
                    break

                end_date_time_search = events[-1]['end'].get('dateTime')

                start_date_time = end_date_time_search

            # Filter events by color_id
            if color_id != -1 and color_id != 0:
                events = [event for event in events if event.get('colorId') == str(color_id)]

            # Filter events by description
            if description and len(description) > 2:  # as default it contains '\n' string
                events = [event for event in events if description.lower() in event.get('description', '').lower()]
            
            if events:
                return events
            else:
                return None      
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")

    # TODO: test me 
    @staticmethod
    def editEventTitleByID(creds: Credentials, ID: str, title: str):
        if creds == None: raise ValueError("Credentials can't be null")
        if ID == None: raise ValueError("ID can't be null")
        if title == None: raise ValueError("Title can't be empty")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            event = service.events().get(calendarId='primary', eventId=ID).execute()
            event['summary'] = title 
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    @staticmethod
    def editEventsTitleByTitle(creds: Credentials, old_title: str, new_title: str, start_date: datetime = None, end_date: datetime = None):
        if creds == None: raise ValueError("Credentials can't be null")
        if old_title == None: raise ValueError("Old Title can't be empty")
        if new_title == None: raise ValueError("New Title can't be empty")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            events = service.events().list(
                calendarId='primary',
                q=old_title,
                timeMin=start_date,
                timeMax=end_date,
                maxResults=2500,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            updated_events = []
            if 'items' in events:
                for event in events['items']:
                    event['summary'] = new_title
                    updated_event = service.events().update(
                        calendarId='primary',
                        eventId=event['id'],
                        body=event
                    ).execute()
                    updated_events.append(updated_event)

            return updated_events

        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    # TODO: test me
    @staticmethod
    def editEventDateByID(creds: Credentials, ID: str, start_date: datetime, end_date: datetime, timeZone: str = 'UTC'):
        if creds == None: raise ValueError("Credentials can't be null")
        if ID == None: raise ValueError("ID can't be null")
        if start_date == None or end_date == None: raise ValueError("Date can't be empty")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            event = service.events().get(calendarId='primary', eventId=ID).execute()
            
            # Update the start and end times along with the time zone
            event['start'] = {'dateTime': start_date, 'timeZone': timeZone}
            event['end'] = {'dateTime': end_date, 'timeZone': timeZone}

            # Update the event in the calendar
            service.events().update(
                calendarId='primary',
                eventId=ID,
                body=event
            ).execute()
        
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    # TODO: test me 
    @staticmethod
    def editDescriptionEventByID(creds: Credentials, ID: str, description: str):
        if creds == None: raise ValueError("Credentials can't be null")
        if ID == None: raise ValueError("ID can't be null")
        if description == None: raise ValueError("Description can't be null")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            event = service.events().get(calendarId='primary', eventId=ID).execute()
            
            # Update the descritpion
            event['description'] = description

            # Update the event in the calendar
            service.events().update(
                calendarId='primary',
                eventId=ID,
                body=event
            ).execute()
        
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    # TODO: test me 
    # TODO: add like mode
    @staticmethod
    def editDescriptionEventsByTitle(creds: Credentials, title: str, description: str, like_mode: bool = False):
        if creds == None: raise ValueError("Credentials can't be null")
        if title == None: raise ValueError("Title can't be null")
        if description == None: raise ValueError("Description can't be null")
        
        try:
            service = build("calendar", "v3", credentials=creds)
            events = service.events().get(calendarId='primary', summary=title).execute()
            
            for event in events:
                # Update the description
                event['description'] = description

                # Update the event in the calendar
                service.events().update(
                    calendarId='primary',
                    eventId=event['id'],
                    body=event
                ).execute()
        
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")

    @staticmethod
    def editEvent(creds: Credentials, old_events: Dict, summary_new: str, description_new: str, color_id_new, start_date: str = None, end_date: str = None, time_zone: str = 'UTC'):
        if creds == None: raise ValueError("Credentials can't be null")
        
        try:
            service = build("calendar", "v3", credentials=creds)

            if old_events == None or len(old_events) == 0: 
                return
            
            # update events
            updated_events = []
            for event in old_events:
                event['summary'] = summary_new
                event['colorId'] = color_id_new
                if description_new != None and len(description_new) > 2:   # as default it contains '\n' string
                    event['description'] = description_new
                
                event['start']['timeZone'] = time_zone
                
                updated_event = service.events().update(
                    calendarId='primary',
                    eventId=event['id'],
                    body=event
                ).execute()
                updated_events.append(updated_event)

            return updated_events

        except HttpError as http_error:
            print(http_error)
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            print(generic_exception)
            raise Exception(f"An error occurred: {str(generic_exception)}")  
    
    @staticmethod
    def simulateEventUpdates(creds: Credentials, old_events: Dict, summary_new: str, description_new: str, color_id_new, start_date: str = None, end_date: str = None, time_zone: str = 'UTC'):
        if creds is None:
            raise ValueError("Credentials can't be null")

        try:
            if old_events is None or len(old_events) == 0:
                return []
            
            # Simulate updates
            simulated_events = []
            for event in old_events:
                simulated_event = event.copy()  # copy the origina event to avoid edit
                simulated_event['summary'] = summary_new
                simulated_event['colorId'] = color_id_new
                if description_new is not None and len(description_new) > 2:
                    simulated_event['description'] = description_new
                
                simulated_event['start']['timeZone'] = time_zone
                
                simulated_events.append(simulated_event)
            
            return simulated_events

        except Exception as generic_exception:
            print(generic_exception)
            raise Exception(f"An error occurred: {str(generic_exception)}")
    
    @staticmethod
    def deleteEventByID(creds: Credentials, ID: str):
        if creds == None: raise ValueError("Credentials can't be null")
        if ID == None: raise ValueError("ID can't be null")

        service = build('calendar', 'v3', credentials=creds)

        try:
            service.events().delete(calendarId='primary', eventId=ID).execute()
        except HttpError as http_error:
            raise HttpError(f"HTTP error occurred: {str(http_error)}")
        except Exception as generic_exception:
            raise Exception(f"An error occurred: {str(generic_exception)}")