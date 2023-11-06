import os.path
import datetime as dt

from bs4 import BeautifulSoup
from typing import List, Set, Tuple, Dict

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

TOKEN_PATH = "./settings/token.json"
CREDENTIALS_PATH = "./settings/credentials.json"
DATA_PATH = "./data/data.csv"
DATA_HEADER = ["ID", "StudentName", "StudentSurname", "StudentEmail", "StudentPhone", "SudentSchool", "LessonDate", "LessonMode", "LessonDuration", "LessonSubject"]

def saveDataToFile(data: Dict[str, List[str]], filepath: str):
    file = open(filepath, "w", encoding='utf-8')
    counter = 0
    for ID in data.keys():
        elem = data[ID]
        elem = [str(element) for element in elem]
        line = "|".join(elem)
        if (counter + 1) < len(data):
            line = line + "\n"
        file.write(line)
        counter += 1
    file.close()
        
def loadDataFromFile(filepath: str) -> Dict[str, List[str]]:
    file = open(filepath, "r")
    data = dict()
    lines = file.readlines()
    for line in lines:
        elem = line.replace("\n", "").split("|")
        ID = elem[0]
        data[ID] = elem
    file.close()
    return data

def addData(data: Dict[str, List[str]], ID: str, StudentName: str, StudentSurname: str, StudentEmail: str, StudentPhone: str, StudentSchool: str, LessonDate: str, LessonMode: str, LessonDuration: str, LessonSubject: str):
    if ID not in data:
        data[ID] = [ID, StudentName, StudentSurname, StudentEmail, StudentPhone, StudentSchool, LessonDate, LessonMode, LessonDuration, LessonSubject]
        print(f"Lesson for \"{StudentName} {StudentSurname}\" has been saved in \"{DATA_PATH}\" file")
    else:
        pass
        #print(f"ID {ID} is already in the dictionary. Skipping duplicate data.")

def editBodyEvent(service, event):
    event["summary"] = "Lezioni Private Prenotabili (Luca Lallo)"
    event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            
    #                 description = '''
    # Prenotato da
    # Millene Rizzetto
    # millene.rizzetto@gmail.com

    # Modalità lezione ("distanza" o "in presenza")?
    # distanza

    # Materia (se piu' materie metti "Varie")
    # informatica

    # La tua scuola (Elementari/Medie/Superiori/Università/altro)?
    # università
    # '''   
                 
    description2 = '''
    \nMateria
    Varie

    La tua scuola (Elementari/Medie/Superiori/Università/altro)?
    Superiori
    '''             
    description = event.get('description')
    event['description'] += str(description2)
    print(event['description'])
    
    event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        
def createEvent(service):
    # set values for the event
    title_event = "Lezioni Private Prenotabili (Luca Ballestrieri)"
    color_event_id = 5  
    start_date = dt.datetime(2023, 7, 5,  18, 30, 0)
    end_date   = dt.datetime(2023, 7, 5,  19, 30, 0)

    # set the event
    event = {
        'summary': title_event,
        'start': {
            'dateTime': start_date.isoformat(),
            'timeZone': 'Europe/Rome',
        },
        'end': {
            'dateTime': end_date.isoformat(),
            'timeZone': 'Europe/Rome',
        },
        'colorId': color_event_id,
    }

    # create the event
    service.events().insert(calendarId='primary', body=event).execute()

def getAllLessons(creds: Credentials, filepath: str):
    # load data from file
    data = loadDataFromFile(filepath)
    
    try:
        service = build("calendar", "v3", credentials=creds)
        
        now = dt.datetime.now().isoformat() + "Z" 
        
        # loop until i find all the events (500 occurrences by step) 
        start_date_search = None 
        end_date_search = None
        while True:
            # set the events list
            if start_date_search == None:
                event_result = service.events().list(calendarId="primary", maxResults=500, timeMax=now, singleEvents=True, orderBy="startTime").execute()
            else:
                event_result = service.events().list(calendarId="primary", maxResults=500, timeMin=start_date_search, timeMax=now, singleEvents=True, orderBy="startTime").execute()
            events = event_result.get("items", [])
            
            # i quit if i found all the events -> it happens when the date of the last element inside the list is the same for two times
            if events[len(events)-1]['end'].get('dateTime') == end_date_search:
                break
                
            end_date_search = events[len(events)-1]['end'].get('dateTime')

            # for every step
            for event in events:
                if "Lezioni Private Prenotabili" in event["summary"]:
                    # --------------- get name and surname
                    student_full_name = None
                    student_name = None
                    student_surname = None
                    
                    input_string = event["summary"]
                    student_full_name = input_string[input_string.find("(") + 1:input_string.find(")")]
                    student_full_name = student_full_name.title() # to capitalize all the words inside
                    parts = student_full_name.split()
                    
                    if len(parts) >= 2:
                        student_name = parts[0]
                        student_surname = ' '.join(parts[1:])
                    else:
                        student_name = parts[0]
                    
                    # --------------- get and calculate the lesson duration
                    start_time = None
                    end_time = None
                    duration = None
                    
                    start_time = event['start'].get('dateTime')
                    end_time = event['end'].get('dateTime')
                    start_datetime = dt.datetime.fromisoformat(start_time)
                    end_datetime = dt.datetime.fromisoformat(end_time)
                    duration = end_datetime - start_datetime
                    
                    # --------------- get information from the description
                    description = str(event.get('description')) 
                    
                    # replace <br> with "\n"
                    description = description.replace("<br>", "\n")
                    #remove html tags from text
                    soup = BeautifulSoup(description, 'html.parser')
                    description = soup.get_text()
                    
                    # Split the text into lines
                    lines = description.splitlines()

                    email = None
                    phone = None
                    subject = None
                    mode = None
                    school = None
                    for line in lines:
                        if (len(line) == 0): pass
                        elif (email is None) and ('@' in line):
                            email = line
                            email = email.replace(" ", "")
                        elif (phone is None) and ('1' in line or '2' in line or '3' in line or '4' in line or '5' in line):
                            phone = line
                            phone = phone.replace(" ", "")
                        elif (subject is None) and ("Materia" not in line) and ('infor' in line.lower() or 'progr' in line.lower() or 'ita' in line.lower() or 'ingle' in line.lower() or 'mate' in line.lower() or 'fisica' in line.lower() or 'storia' in line.lower()):
                            subject = line.lower()
                            subject = subject.replace(" ", "")
                        elif (mode is None) and ("lezione" not in line.lower()) and ('presen' in line.lower() or 'dista' in line.lower()):
                            mode = line.lower()
                            mode = mode.replace(" ", "")
                        elif (school is None) and ("la tua scuola" not in line.lower()) and ('elem' in line.lower() or 'medi' in line.lower() or 'super' in line.lower() or 'uni' in line.lower() in line.lower()):
                            school = line.lower()
                            school = school.replace(" ", "")

                        # check errors on booking
                        if (email or phone or subject or mode or school is None):
                            pass
                        
                    addData(data, event['id'], student_name, student_surname, email, phone, school, start_time, mode, duration, subject)
                    
                    # save the start date for the next 500 occurrences
                    start_date_search = start_time
                
            saveDataToFile(data, DATA_PATH)      
        
    except HttpError as error:
        print("An error has occurred: ", error.reason())

def connectionSetup():
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    
    getAllLessons(creds, DATA_PATH)
    
    
if __name__ == "__main__":
    connectionSetup()