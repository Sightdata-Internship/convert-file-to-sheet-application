from datetime import datetime, date

import PySimpleGUI as sg
import json
import pandas as pd
import pygsheets as pgs

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd
from gspread_dataframe import set_with_dataframe, get_as_dataframe

## Function: runUserLogInGUI
# Task: runs the initial login GUI when computer starts running
# Parameters: none
def runUserLogInGUI():
    # GUI layout design
    title = "User log in"
    layout = [
        [sg.Text("Enter userID")],
        [sg.InputText()],
        [sg.Button("Log in")],
        [sg.Button("Sign up")]
    ]

    window = sg.Window(title, layout)

    while True:
        event, values = window.read()
        if event == "Log in" or event == "Sign up" or event ==sg.WIN_CLOSED:
            break
        
    window.close()
    userId = values[0]
    return userId

## Function: runOldUserLogInGUI
# Task: show Welcome GUI if user ID is recognised
# Parameters: none
def runOldUserLogInGUI():
    # GUI layout design
    title = "User log in"
    layout = [
        [sg.Text("Welcome to site!")]
    ]
    
    window = sg.Window(title, layout, margins = (50, 50))

    while True:
        event, values = window.read()
        if event ==sg.WIN_CLOSED:
            break
        
    window.close()

## Function: runNewUserSignUpGUI
# Task: show sign up form for new user to fill in
# Parameters: None
def runNewUserSignUpGUI():
    # GUI layout design
    title = "New User Sign up"
    layout =  [
        [sg.Text("Fill in the information below")],
        [sg.Text("User ID:", size = (15,1)), sg.InputText()],
        [sg.Text("Job title:", size = (15,1)), sg.InputText()],
        [sg.Text("First name:", size = (15,1)), sg.InputText()],
        [sg.Text("Last Name:", size = (15,1)), sg.InputText()],
        [sg.Text("Employee Code", size = (15,1)), sg.InputText()],
        [sg.Text("Region", size = (15,1)), sg.InputText()],
        [sg.Text("Phone number", size = (15,1)), sg.InputText()],
        [sg.Text("Email address", size = (15,1)), sg.InputText()],
        [sg.Button("Sign Up")]
    ]
    window = sg.Window(title, layout)

    while True:
        event, values = window.read()
        if event == "Sign Up" or event ==sg.WIN_CLOSED:
            break
        
    # get user information input and assign to those value and return them as a list 
    userId = values[0]
    jobTitle = values[1]
    firstName = values[2]
    lastName = values[3]
    employeeCode = values[4]
    region = values[5] 
    phoneNumber = values[6]
    emailAddress = values[7] 
    
    window.close()
    return [userId, jobTitle, firstName, lastName, employeeCode, region, phoneNumber, emailAddress]

## Function: checkValidUserId
# Task: check if user ID is valid
# Parameters: userId, data
def checkValidUserId(userId, data):
    isValid = True
    i = 0
    
    ## check if userId match with data from json file
    while i <= 2: 
        if userId == data["Employees"][i]["userId"]:
            isValid = True
            break
        else:
            isValid = False    
        i += 1
    
    ## check if userId match with data from the sheet    
    #connect Python with Google Sheet using API keys
    scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("tasksheets-360312-bbf002405e77.json", scope)
    employee = gspread.authorize(creds)
    sheet = employee.open('Sightdata Employee').get_worksheet(3)
    
    values_list = sheet.col_values(1)
    j = 0
    
    while j < len(values_list):
        # print(values_list[j])
        if userId == values_list[j]:
            isValid = True
            break
        else:
            isValid = False
        j += 1
    return isValid

## Function: addValueToSheet2
# Task: get user log in time and sync with Googlesheet 
# Parameters: userId
def addValueToSheet2(userId):
    # connect Python with Google Sheet using API keys
    scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("tasksheets-360312-bbf002405e77.json", scope)
    employee = gspread.authorize(creds)
    sheet = employee.open('Sightdata Employee').get_worksheet(2)
    
    ## get date/time value when user log in
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    today = date.today()
    current_date = today.strftime("%m/%d/%y")
    
    userCheckInList =[userId, current_time, current_date, current_time, current_date]

    df = pd.DataFrame (userCheckInList).transpose()
    df.columns = ['userId', 'arriveTime', 'arriveDate', 'leaveTime', 'leaveDate']
    
    existing = pd.DataFrame(sheet.get_all_records())
    
    new_df= pd.DataFrame()
    new_df = new_df.append(df)
    new_df = new_df.append(existing)
    
    set_with_dataframe(sheet, new_df)

## Function: addValueToSheet1
# Task: sync user sign up information with Googlesheet
# Parameters: userId, jobTitle, firstName, lastName, employeeCode, region, phoneNumber, emailAddress
def addValueToSheet1(userId, jobTitle, firstName, lastName, employeeCode, region, phoneNumber, emailAddress):
    #connect Python with Google Sheet using API keys
    scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("tasksheets-360312-bbf002405e77.json", scope)
    employee = gspread.authorize(creds)
    sheet = employee.open('Sightdata Employee').get_worksheet(3)
    
    userInfoList =[userId, jobTitle, firstName, lastName, employeeCode, region, phoneNumber, emailAddress]
    
    df = pd.DataFrame (userInfoList).transpose()
    df.columns = ['userId', 'jobTitle', 'firstName', 'lastName', 'employeeCode', 'region', 'phoneNumber', 'emailAddress']
    print (df)
    
    existing = pd.DataFrame(sheet.get_all_records())
    
    new_df= pd.DataFrame()
    new_df = new_df.append(df)
    new_df = new_df.append(existing)
    
    set_with_dataframe(sheet, new_df)
    
def main():
    #read JSON file into dataframe 
    file = open('Sample-employee-JSON-data.json')
    data = json.load(file)
    
    userId = ""
    userId = runUserLogInGUI()
    
    newUserInfo = []
    if checkValidUserId(userId, data):
        runOldUserLogInGUI()
        addValueToSheet2(userId)
    else:
        newUserInfo = runNewUserSignUpGUI()
        userId = newUserInfo[0]
        jobTitle = newUserInfo[1]
        firstName = newUserInfo[2]
        lastName = newUserInfo[3]
        employeeCode = newUserInfo[4]
        region = newUserInfo[5] 
        phoneNumber = newUserInfo[6]
        emailAddress = newUserInfo[7] 
        addValueToSheet1(userId, jobTitle, firstName, lastName, employeeCode, region, phoneNumber, emailAddress)
        addValueToSheet2(userId)
        runOldUserLogInGUI()
    

if __name__ == "__main__":
    main()