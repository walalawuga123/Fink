# Required imports
import math
from google.colab import output
from IPython.display import display, Javascript
import gspread
import pandas as pd
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

# Mount Google Drive and authenticate
drive.mount('/content/drive')
auth.authenticate_user()  # Authenticate manually to avoid errors
# Get authenticated credentials
creds, _ = default()
gc = gspread.authorize(creds)

# Function to create input boxes and submit button using JS
def create_input_boxes():
    display(Javascript('''
    // Create input elements
    function createInput(id, placeholder) {
        var input = document.createElement("input");
        input.id = id;
        input.placeholder = placeholder;
        input.style.margin = "10px";
        input.style.padding = "12px";
        input.style.fontSize = "16px";
        input.style.width = "250px";
        input.style.height = "40px";
        return input;
    }

    var input1 = createInput("xL1000", "Enter xL1000");
    var input2 = createInput("xL3000", "Enter xL3000");
    var input3 = createInput("xR1000", "Enter xR1000");
    var input4 = createInput("xR3000", "Enter xR3000");
    var input5 = createInput("zL1000", "Enter zL1000");
    var input6 = createInput("zL3000", "Enter zL3000");
    var input7 = createInput("zR1000", "Enter zR1000");
    var input8 = createInput("zR3000", "Enter zR3000");

    // Submit button
    var button = document.createElement("button");
    button.innerHTML = "Submit";
    button.style.margin = "10px";
    button.style.padding = "12px 20px";
    button.style.fontSize = "16px";
    button.style.backgroundColor = "#4CAF50";
    button.style.color = "white";
    button.style.border = "none";
    button.style.borderRadius = "8px";
    button.style.cursor = "pointer";

    // Finish correction button
    var finishButton = document.createElement("button");
    finishButton.innerHTML = "Finish Correction";
    finishButton.style.margin = "10px";
    finishButton.style.padding = "12px 20px";
    finishButton.style.fontSize = "16px";
    finishButton.style.backgroundColor = "#FF5733";
    finishButton.style.color = "white";
    finishButton.style.border = "none";
    finishButton.style.borderRadius = "8px";
    finishButton.style.cursor = "pointer";

    // Result output box
    var resultBox = document.createElement("textarea");
    resultBox.id = "resultBox";
    resultBox.style.margin = "10px";
    resultBox.style.padding = "12px";
    resultBox.style.fontSize = "16px";
    resultBox.style.width = "250px";
    resultBox.style.height = "100px";
    resultBox.style.display = "block";  // Ensure it's visible by default
    resultBox.readOnly = true;

    // Create a container for the input fields and arrange them in 4 columns
    var inputContainer = document.createElement("div");
    inputContainer.style.display = "grid";
    inputContainer.style.gridTemplateColumns = "1fr 1fr 1fr 1fr"; // 4 columns
    inputContainer.style.gridGap = "10px";
    inputContainer.style.marginTop = "20px";

    // Append inputs to the container in the desired order (4 columns)
    inputContainer.appendChild(input1); // xL1000
    inputContainer.appendChild(input3); // xR1000
    inputContainer.appendChild(input5); // zL1000
    inputContainer.appendChild(input7); // zR1000
    inputContainer.appendChild(input2); // xL3000
    inputContainer.appendChild(input4); // xR3000
    inputContainer.appendChild(input6); // zL3000
    inputContainer.appendChild(input8); // zR3000

    // Add the container, buttons, and result box to the page
    var container = document.createElement("div");
    container.className = "custom-inputs";
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.alignItems = "center";
    container.style.marginTop = "20px";

    container.appendChild(inputContainer);
    container.appendChild(button);
    container.appendChild(finishButton);
    container.appendChild(resultBox);
    document.body.appendChild(container);

    // Button click actions for Submit and Finish correction
    button.onclick = function() {
        var val1 = document.getElementById("xR1000").value;
        var val2 = document.getElementById("xR3000").value;
        var val3 = document.getElementById("zR1000").value;
        var val4 = document.getElementById("zR3000").value;
        var val5 = document.getElementById("xL1000").value;
        var val6 = document.getElementById("xL3000").value;
        var val7 = document.getElementById("zL1000").value;
        var val8 = document.getElementById("zL3000").value;
        google.colab.kernel.invokeFunction("notebook.update_correction_result", [val1, val2, val3, val4, val5, val6, val7, val8], {});
    }

    finishButton.onclick = function() {
        google.colab.kernel.invokeFunction("notebook.finish_correction", [], {});
    }
    '''))
    
# Python callback to compute corrections and update Google Sheets
def CorrectionCalculation(xR1000, xR3000, zR1000, zR3000, xL1000, xL3000, zL1000, zL3000):
    try:
        # Convert all values to float
        xR1000 = float(xR1000)
        xR3000 = float(xR3000)
        zR1000 = float(zR1000)
        zR3000 = float(zR3000)
        xL1000 = float(xL1000)
        xL3000 = float(xL3000)
        zL1000 = float(zL1000)
        zL3000 = float(zL3000)

        # Theta Calculations
        Theta_L = round(-math.atan((xL3000 - xL1000) / 2000) * 180 /  math.pi, 4)
        Theta_R = round(math.atan((xR3000 - xR1000) / 2000) * 180 / math.pi, 4)
        YawCorrection = round((Theta_R - Theta_L) / 2, 3)

        # Offsets and Ratios
        Zoffset1000 = zL1000 - zR1000
        Zoffset3000 = zL3000 - zR3000
        Xoffset1000 = xR1000 - xL1000
        Xoffset3000 = xR3000 - xL3000
        Ratio1000 = Zoffset1000 / Xoffset1000
        Ratio3000 = Zoffset3000 / Xoffset3000

        # Angle Calculations
        Angle1000 = round(math.atan(Ratio1000) * 360 / (2 * math.pi), 2)
        Angle3000 = round(math.atan(Ratio3000) * 360 / (2 * math.pi), 2)
        RollCorrection = round((Angle1000 + Angle3000) / 2, 2)

        # Compose result
        result = (
            f"Yaw correction: {YawCorrection}°\\n\\n"
            f"Roll correction: {RollCorrection}°\\n\\n"
        )

        # Return results
        return YawCorrection, RollCorrection, result

    except ValueError:
        result = "⚠️ Please enter valid numerical values."
        return None, None, result

# Display result in the result box
def output_result(result):
    display(Javascript(f'''
    var resultBox = document.getElementById("resultBox");
    resultBox.style.display = "block";
    resultBox.value = `{result}`;
    '''))

# Callback function to update corrections and update the sheet
def update_correction_result(xR1000, xR3000, zR1000, zR3000, xL1000, xL3000, zL1000, zL3000):
    # Capture the YawCorrection, RollCorrection, and result from the calculation
    YawCorrection, RollCorrection, result = CorrectionCalculation(xR1000, xR3000, zR1000, zR3000, xL1000, xL3000, zL1000, zL3000)

    # If no valid result, show error and return
    if not YawCorrection or not RollCorrection:
        output_result(result)
        return

    # Display the result in the result box
    output_result(result)

# Callback function to finish correction and update the Google Sheet
def finish_correction():
    # Fetch the head_parameter DataFrame from Google Sheets
    file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID
    sh = gc.open_by_key(file_id)  # Open the Google Sheet with the file_id
    worksheet = sh.get_worksheet(0)  # Select the first sheet

    head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet
    
    # Collect final input for all columns via JavaScript prompt (ensure user interaction)
    final_xR1000 = prompt("Enter final xR1000");
    final_xR3000 = prompt("Enter final xR3000");
    final_zR1000 = prompt("Enter final zR1000");
    final_zR3000 = prompt("Enter final zR3000");
    final_xL1000 = prompt("Enter final xL1000");
    final_xL3000 = prompt("Enter final xL3000");
    final_zL1000 = prompt("Enter final zL1000");
    final_zL3000 = prompt("Enter final zL3000");

    # Update the sheet with the final values
    head_parameter.iloc[17, -1] = final_xR1000
    head_parameter.iloc[21, -1] = final_xR3000
    head_parameter.iloc[33, -1] = final_zR1000
    head_parameter.iloc[37, -1] = final_zR3000
    head_parameter.iloc[9, -1] = final_xL1000
    head_parameter.iloc[13, -1] = final_xL3000
    head_parameter.iloc[25, -1] = final_zL1000
    head_parameter.iloc[29, -1] = final_zL3000

    # Write the updated DataFrame back to the sheet
    worksheet.clear()
    set_with_dataframe(worksheet, head_parameter)

# Register the callbacks for updating corrections and finishing the process
output.register_callback('notebook.update_correction_result', update_correction_result)
output.register_callback('notebook.finish_correction', finish_correction)

# Initialize the input boxes and the callback
create_input_boxes()
