from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import datetime as dt

import GoogleCalendarEventsManager as gc

import customtkinter

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_PATH = "./settings/token.json"
CREDENTIALS_PATH = "./settings/credentials.json"
DATA_PATH = "./data/test.csv"

if __name__ == "__main__":
    
    
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme('dark-blue')
    
    root = customtkinter.CTk()
    root.geometry("500x360")
    
    try:
        credentials = gc.GoogleCalendarEventsManager.connectionSetup(TOKEN_PATH, CREDENTIALS_PATH, SCOPES)
    except:
        gc.GoogleCalendarEventsManager.refreshToken()
        
    
    if credentials is None:
        print("credentials none")
    
    res = gc.GoogleCalendarEventsManager.getAllDescriptionsByTitle(credentials, "Lezioni Private")
    print(len(res))
    
    
    
    
    
    