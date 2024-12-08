from django.shortcuts import render

# Create your views here.


# gmail aceess data start 

# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import schedule
from time import gmtime, strftime
import time
from datetime import datetime, timezone
import datetime
import pytz
from dateutil import tz, parser
import json
import requests


# gm = time.strftime("%a, %d %b %Y %X",
#                   time.gmtime())


# # API_ENDPOINT = "http://127.0.0.1:8000/account/gmail-data/"
# API_ENDPOINT = "https://itb-usa.a2hosted.com/account/gmail-data/"

# # Define the SCOPES. If modifying it, delete the token.pickle file.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# def getEmails():
#     # Variable creds will store the user access token.
#     # If no valid token found, we will create one.
#     creds = None

#     # The file token.pickle contains the user access token.
#     # Check if it exists
#     if os.path.exists('/home/itbusaah/idriver_education_djangoproject/emailserviceapp/token.pickle'):

#         # Read the token from the file and store it in the variable creds
#         with open('/home/itbusaah/idriver_education_djangoproject/emailserviceapp/token.pickle', 'rb') as token:
#             creds = pickle.load(token)

#     # If credentials are not available or are invalid, ask the user to log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 '/home/itbusaah/idriver_education_djangoproject/emailserviceapp/credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)

#         # Save the access token in token.pickle file for the next run
#         with open('/home/itbusaah/idriver_education_djangoproject/emailserviceapp/token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     # Connect to the Gmail API
#     service = build('gmail', 'v1', credentials=creds)

#     # request a list of all the messages
#     result = service.users().messages().list(userId='me').execute()

#     # We can also pass maxResults to get any number of emails. Like this:
#     # result = service.users().messages().list(maxResults=200, userId='me').execute()
#     messages = result.get('messages')
#     # messages is a list of dictionaries where each dictionary contains a message id.

#     # iterate through all the messages
#     for msg in messages:
#         # Get the message from its id
#         txt = service.users().messages().get(
#             userId='me', id=msg['id']).execute()

#         # Use try-except to avoid any Errors
#         try:
#             # Get value of 'payload' from dictionary 'txt'
#             payload = txt['payload']
#             headers = payload['headers']
#             # Look for Subject and Sender Email in the headers
#             for d in headers:
#                 if d['name'] == 'Subject':
#                     subject = d['value']
#                 if d['name'] == 'From':
#                     sender = d['value']
#                 if d['name'] == 'Date':
#                     date = d['value']

#             # The Body of the message is in Encrypted format. So, we have to decode it.
#             # Get the data and decode it with base 64 decoder.
#             parts = payload.get('parts')[0]
#             data = parts['body']['data']
#             data = data.replace("-", "+").replace("_", "/")
#             decoded_data = base64.b64decode(data)

#             soup = BeautifulSoup(decoded_data, 'html.parser')

#             strValue = ""
#             for ml in soup:
#                 strValue += " ".join(ml.text.split())

#             x = parser.parse(date)
#             date1 = x.strftime("%a, %d %b %Y %X")
#             timestamp = datetime.datetime.strptime(
#                 date1, "%a, %d %b %Y %X").timestamp()
#             currenttimestamp = datetime.datetime.strptime(
#                 gm, "%a, %d %b %Y %X").timestamp()

#             gmailtimedate = datetime.datetime.fromtimestamp(
#                 timestamp).strftime('%d-%m-%Y')
#             currenttimedate = datetime.datetime.fromtimestamp(
#                 currenttimestamp).strftime('%d-%m-%Y')
#             if gmailtimedate == currenttimedate:

#                 data = {
#                     'subject': subject,
#                     'sender': sender,
#                     'date': date,
#                     'body': strValue,
#                     'currenttimedate': currenttimedate,
#                 }
#                 r = requests.post(url=API_ENDPOINT, data=data)
#                 print("376", r.text)
#         except:
#             pass


# schedule.every(10).seconds.do(getEmails)


# try:
#     while True:
#         schedule.run_pending()
# except KeyboardInterrupt:
#     print('Stopped')




      
# gmail aceess data end