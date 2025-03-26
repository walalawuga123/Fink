import gspread
import pandas as pd
import gdown
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth

drive.mount('/content/drive')
auth.authenticate_user() # Authenticate manually to avoid errors

# Get authenticated credentials
creds, _ = default()
gc = gspread.authorize(creds)

file_id = '1e7ZqoPTFdUS_E163w0M41izWisuC9tJd' # need to be change after switch files
filename = gdown.download(f"https://drive.google.com/uc?id={file_id}", "downloaded_file.xlsx", quiet=False)
head_parameter = pd.read_excel(filename, sheet_name='Sheet1')
new_mouse_id = str(input("Mouse ID: "))
head_parameter[new_mouse_id] = ""

# Try opening the Google Sheet
sh = gc.open_by_key(file_id)
worksheet = sh.get_worksheet(0)
worksheet.clear()
set_with_dataframe(worksheet, df)
