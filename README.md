# Google app sheet app
DESCRIPTION: 
- This application will run at the same time with on-site computer and let user log in or sign up if they need access to the computer site (Main-2.py). The information that user enters will be updated on the sheet as well as the time record that they use the computer. The Google Appsheet app update the adjustment from the sheet and push a notification for the app's user, let them know who logs in the system at what time and date.
- It converts JSON file of employee information into Google sheet and update the sheet using Python (Main.py). The code interacts with a Google AppSheet app to update information of the employee log-in time.

ADDITION REQUIREMENTS:
- gspread with oauth2client installation is needed to run the code
- link to Google Sheet: https://docs.google.com/spreadsheets/d/1bqg6GDAEL8cshyJOZi_dLq0QtG012E6rnop5yxoLdic/edit?usp=sharing
- link to Google AppSheet App: https://www.appsheet.com/start/980a28a6-f06e-4251-917d-b724facbc4bb
- link to install Google AppSheet App: https://www.appsheet.com/newshortcut/980a28a6-f06e-4251-917d-b724facbc4bb

FUTHER ISSUES NEED INVESTIGATION:
- The system ignores n/a value and does not require user to enter necessary information before continuing to process their request.
- The Google Appsheet app requires payment update to access (pay-per-user).
