import json
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd
from gspread_dataframe import set_with_dataframe

# function: convertFileToSheet
## reads and convert JSON file to google sheet
def convertFileToSheet():
    
    #connect Python with Google Sheet using API keys
    scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("tasksheets-360312-bbf002405e77.json", scope)
    employee = gspread.authorize(creds)
    sheet = employee.open('Sight Data Employee').sheet1
    
    #read JSON file into dataframe 
    file = open('Sample-employee-JSON-data.json')
    data = json.load(file)
    
    #add all employee info into an existing dataframe
    existing = pd.DataFrame()
    for i in data['Employees']:
        df = pd.DataFrame.from_dict(pd.json_normalize(i), orient='columns')
        existing = existing.append(df)
    
    #add dataframe to Google Sheet    
    set_with_dataframe(sheet, existing)    
    
def main():
    convertFileToSheet()

if __name__ == "__main__":
    main()