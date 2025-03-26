
# Import required modules
import gspread
import pandas as pd
import gdown

file_id = '1e7ZqoPTFdUS_E163w0M41izWisuC9tJd' # need to be change after switch files
filename = gdown.download(f"https://drive.google.com/uc?id={file_id}", "downloaded_file.xlsx", quiet=False)
head_parameter = pd.read_excel(filename, sheet_name = 'Sheet1')

# Mount Google Drive
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default

drive.mount('/content/drive')

# Authenticate manually to avoid errors
from google.colab import auth
auth.authenticate_user()

# Import required libraries
import gspread
from google.auth import default
from gspread_dataframe import set_with_dataframe
import gdown
import pandas as pd

# Get authenticated credentials
creds, _ = default()
gc = gspread.authorize(creds)

# Download the file from shared link using gdown
file_id = '10a9LPPYnVm5NurO8dxmdZbkVH5ksNLZYPstuM5o6Q-E'  # Correct Google Sheet file ID
filename = gdown.download(f"https://drive.google.com/uc?id={file_id}", "testing.xlsx", quiet=False)

# Load and modify the Excel file
head_parameter = pd.read_excel(filename, sheet_name='Sheet1')
print(head_parameter)



# Open the existing Google Sheet using its file ID
#sh = gc.open_by_key(file_id)  # Open the Google Sheet with the same file_id
#worksheet = sh.get_worksheet(0)  # Select the first sheet
#worksheet.clear()  # Clear the old content
#set_with_dataframe(worksheet, df)  # Overwrite the sheet with new data
