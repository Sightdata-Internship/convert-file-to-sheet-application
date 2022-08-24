import json
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd


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
    df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
    
    #insert JSON file into sheet as a dataframe
    for i in df['Employees']:
        existing = gd.get_as_dataframe(sheet)
        updated = existing.append(i)
        gd.set_with_dataframe(sheet, updated)
    # headers={'Content-Type': 'application/json'}

def main():
    convertFileToSheet()

if __name__ == "__main__":
    main()