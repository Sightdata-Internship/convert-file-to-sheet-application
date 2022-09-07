import http.client
import pprint
import ssl

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd
from gspread_dataframe import set_with_dataframe, get_as_dataframe

# connect with site, get response and header info
connection = http.client.HTTPSConnection("sightdata.ai")
connection.request("GET", "/")
response = connection.getresponse()
headers = response.getheaders()

# connect with google spreadsheet using api key
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("tasksheets-360312-bbf002405e77.json", scope)
employee = gspread.authorize(creds)
sheet = employee.open('Sightdata Employee').get_worksheet(1)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint("Headers: {}".format(headers))

# check if successfully connected with site
if response.status == 200:
    print('[{}]: '.format(connection), "Up!")
    print("Headers: {}".format(headers))
    
    # Update info to sheet
    sheet.update('A1', response.status)

connection.close()