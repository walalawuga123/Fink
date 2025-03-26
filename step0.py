import gspread
import pandas as pd
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth

# Mount Google Drive and authenticate
drive.mount('/content/drive')
auth.authenticate_user()  # Authenticate manually to avoid errors
# Get authenticated credentials
creds, _ = default()
gc = gspread.authorize(creds)

file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID here
sh = gc.open_by_key(file_id)  # Open the Google Sheet with the file_id
worksheet = sh.get_worksheet(0)  # Select the first sheet

head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet
new_mouse_id = str(input("Mouse ID: "))
head_parameter[new_mouse_id] = ""

worksheet.clear()
set_with_dataframe(worksheet, head_parameter)
