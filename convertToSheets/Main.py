import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd

# function: convertFileToSheet
## reads and convert JSON file to google sheet
def convertFileToSheet():
    
    scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("tasksheets-360312-bbf002405e77.json", scope)

    employee = gspread.authorize(creds)

    sheet = employee.open('Sight Data Employee').sheet1
    
    file = open('Sample-employee-JSON-data.json')
    data = json.load(file)
    df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
    #wks = sheet[0]
    # .from_dict(pd.json_normalize(data), orient='columns')

    #update the first sheet with df, starting at cell B2. 
    sheet.set_dataframe(df,(1,1))
    
    # for i in data['Employees']:
    #     print(i)
        #sheet.insert_row(i, headers={'Content-Type': 'application/json'})
        #sheet.insert_row(row,1)

def main():
    convertFileToSheet()

if __name__ == "__main__":
    main()