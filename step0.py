import gspread
import pandas as pd
import gdown
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth
drive.mount('/content/drive')
auth.authenticate_user() # Authenticate manually to avoid errors

# Load and modify the Excel file

file_id = '1e7ZqoPTFdUS_E163w0M41izWisuC9tJd' # need to be change after switch files
filename = gdown.download(f"https://drive.google.com/uc?id={file_id}", "downloaded_file.xlsx", quiet=False)
head_parameter = pd.read_excel(filename, sheet_name='Sheet1')
l = len(head_parameter.columns)
print(l)
print(head_parameter[:,l])

# Open the existing Google Sheet using its file ID
#sh = gc.open_by_key(file_id)  # Open the Google Sheet with the same file_id
#worksheet = sh.get_worksheet(0)  # Select the first sheet
#worksheet.clear()  # Clear the old content
#set_with_dataframe(worksheet, df)  # Overwrite the sheet with new data
