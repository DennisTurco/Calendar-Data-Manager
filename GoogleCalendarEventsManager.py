import os.path

from typing import List, Set, Tuple, Dict
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarEventsManager:
    
    data: Dict[str, List[str]] = None
    
    def saveDataToFile(data: Dict[str, List[str]], filepath: str, delimeter: str = "|", encodingType: str = None):
        if filepath == None or len(filepath) == 0: Exception("File path can't be null")
        
        file = open(filepath, "w", encoding=encodingType)
        counter = 0
        for ID in data.keys():
            elem = data[ID]
            elem = [str(element) for element in elem]
            line = delimeter.join(elem)
            if (counter + 1) < len(data):
                line = line + "\n"
            file.write(line)
            counter += 1
        file.close()
    
    def loadDataFromFile(filepath: str, delimeter: str = "|") -> Dict[str, List[str]]:
        if filepath == None or len(filepath) == 0: Exception("File path can't be null")
        
        file = open(filepath, "r")
        data = dict()
        lines = file.readlines()
        for line in lines:
            elem = line.replace("\n", "").split(delimeter)
            ID = elem[0]
            data[ID] = elem
        file.close()
        return data
    
    def connectionSetup(token_path: str, credentials_path: str, scopes: str) -> Credentials:
        if token_path == None or len(token_path) == 0: Exception("Token path can't be empty")
        if credentials_path == None or len(credentials_path) == 0: Exception("Credentials path can't be empty")
        if scopes == None or len(scopes) == 0: Exception("Scopes link can't be empty")
        
        credentials = None
        
        if os.path.exists(token_path):
            credentials = Credentials.from_authorized_user_file(token_path)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                credentials = flow.run_local_server(port=0)
                
            with open(token_path, "w") as token:
                token.write(credentials.to_json())
    
    def addData(data: Dict[str, List[str]], ID: str, data_list: List[str]) -> bool:
        if ID not in data:
            data[ID] = data_list
            return True
        else:
            return False

    def createEvent(service, title_event: str, start_date, end_date, color_event_id: int = 1, timeZone: str = ''):
        # set the event
        event = {
            'summary': title_event,
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
    
    def getTitleByID(service, event, ID: str) -> str:
        if ID == None: Exception("ID can't be null")
        pass
    
    def getTitleByDate(service, event, start_date: str, end_date: str) -> str:
        if start_date == None or end_date == None: Exception("Date can't be empty")
        pass
    
    def getIDByTitle(service, event, title: str) -> List:
        if title == None: Exception("Title can't be empty")
        pass
    
    def getIDByDate(service, event, start_date: str, end_date: str) -> List:
        if start_date == None or end_date == None: Exception("Date can't be empty")
        pass
    
    def getDescriptionByID(service, event, ID: str) -> str:
        if ID == None: Exception("ID can't be null")
        pass
    
    def getAllDescriptionsByTitle(service, event, like_mode: bool = False) -> Dict[str, List[str]]:
        pass
    
    def editEventTitleByID(service, event, ID: str):
        if ID == None: Exception("ID can't be null")
        pass
    
    def editEventDateByID(service, event, ID: str):
        if ID == None: Exception("ID can't be null")
        pass
    
    def editDescriptionEventByID(service, event):
        pass
    
    def editDescriptionEventByIDTitle(service, event, like_mode: bool = False):
        pass