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
        input.style.width = "300px";
        input.style.height = "40px";
        return input;
    }

    var input1 = createInput("input1", "Enter Initial angle");
    var input2 = createInput("input2", "Enter RCS-lambda distance")
    var input3 = createInput("input3", "Enter DV offset");
    
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

    // Result output box
    var resultBox = document.createElement("textarea");
    resultBox.id = "resultBox";
    resultBox.style.margin = "10px";
    resultBox.style.padding = "12px";
    resultBox.style.fontSize = "16px";
    resultBox.style.width = "300px";
    resultBox.style.height = "100px";
    resultBox.style.display = "block";  // Ensure it's visible by default
    resultBox.readOnly = true;

    // Plot result box (for embedding the plot)
    var plotBox = document.createElement("div");
    plotBox.id = "plotBox";
    plotBox.style.margin = "10px";
    plotBox.style.height = "400px";  // Set a height for the plot display

    // Button click action
    button.onclick = function() {
        var val1 = document.getElementById("input1").value;
        var val2 = document.getElementById("input2").value;
        var val3 = document.getElementById("input3").value;
        google.colab.kernel.invokeFunction("notebook.update_angle_result", [val1, val2, val3], {});
    }

    // Add everything to the container
    var container = document.createElement("div");
    container.className = "custom-inputs";
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.alignItems = "center";
    container.style.marginTop = "20px";

    container.appendChild(input1);
    container.appendChild(input2);
    container.appendChild(input3);
    container.appendChild(button);
    container.appendChild(resultBox);
    container.appendChild(plotBox);
    document.body.appendChild(container);
    '''))
    
# Python callback to compute angle correction and update Google Sheets
def AngleCorrection(initial_angle, RCSL, DVoffset):
    try:
        # Convert all values to float
        initial_angle = float(initial_angle)
        RCSL = float(RCSL)
        DVoffset = float(DVoffset)

        # Calculate pitch correction
        PitchCorrection = round(math.atan(-DVoffset / RCSL) * 180 / math.pi, 2)

        # Final angle
        AdvisedAngle = round(PitchCorrection + initial_angle, 2)

        # Compose result
        result = (
            f"Pitch correction: {PitchCorrection}°\\n\\n"
            f"Initial angle: {initial_angle}°\\n\\n"
            f"Advised angle: {AdvisedAngle}°"
        )

        # Return the AdvisedAngle for later use
        return AdvisedAngle, result

    except ValueError:
        result = "⚠️ Please enter valid numerical values."
        return None, result

# Display result in the result box
def output_result(result):
    display(Javascript(f'''
    var resultBox = document.getElementById("resultBox");
    resultBox.style.display = "block";
    resultBox.value = `{result}`;
    '''))

# Callback function to update angle and update the sheet
def update_angle_result(val1, val2, val3):
    # Capture the advised angle from the AngleCorrection function
    advised_angle, result = AngleCorrection(val1, val2, val3)

    # If no valid result, show error and return
    if not advised_angle:
        output_result(result)
        return

    # Fetch the head_parameter DataFrame from Google Sheets
    file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID
    sh = gc.open_by_key(file_id)  # Open the Google Sheet with the file_id
    worksheet = sh.get_worksheet(0)  # Select the first sheet

    head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet
    new_mouse_id = head_parameter.columns[-1]  # Assuming last column is new mouse ID

    # Update the sheet with the advised angle at the 8th column (index 8)
    head_parameter.iloc[7, -1] = val2 # RCS-Lambda distance
    head_parameter.iloc[8, -1] = advised_angle
    
    
    # Write the updated DataFrame back to the sheet
    worksheet.clear()
    set_with_dataframe(worksheet, head_parameter)
    
    # Display the result in the result box
    output_result(result)

    # Plot the histogram with the advised angle
    plot_histogram(advised_angle)

# Function to plot histogram with the advised angle
def plot_histogram(mousedata):
    # Fetch data for histogram
    file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID
    sh = gc.open_by_key(file_id)
    worksheet = sh.get_worksheet(0)
    head_parameter = pd.DataFrame(worksheet.get_all_records())

    pitch_raw = head_parameter.iloc[8, 6:-1].values
    pitch_metadata = [x for x in pitch_raw if x != '']
    pitch_mean = np.mean(pitch_metadata)
    pitch_std = np.std(pitch_metadata)

    binwidth = pitch_std / 2  # binsize
    bins = np.arange(min(pitch_metadata), max(pitch_metadata) + binwidth, binwidth)

    fig, ax = plt.subplots(figsize=(5, 5))
    y, x, _ = ax.hist(pitch_metadata, color='black', bins=bins, rwidth=0.8)  # obtain x and y of the histogram
    Ylim = 1.1 * max(y)  # calculate max height of the histogram

    ax.axvline(pitch_mean, lw=2, color='black', ls='-')  # mean
    for n in [1, -1]:
        ax.axvline(pitch_mean + n * pitch_std, lw=1, color='black', ls='--')  # 1 std
        ax.axvline(pitch_mean + 2 * n * pitch_std, lw=1, color='black', ls='dotted')  # 2 std
    
    ax.set_xlabel('Pitch angle (˚)')
    ax.set_ylabel('Number of mice')
    ax.set_xlim(pitch_mean - 4 * pitch_std, pitch_mean + 4 * pitch_std)
    ax.set_ylim(0, Ylim)

    # Check if mousedata is inside the valid range and plot accordingly
    if pitch_mean - 2 * pitch_std <= mousedata <= pitch_mean + 2 * pitch_std:
        ax.scatter(mousedata, max(y), color='red', marker='*', s=100)
    else:
        ax.scatter(mousedata, Ylim*0.9, facecolors='none', edgecolor='blue', marker='o', s=100)
        ax.scatter(mousedata, Ylim*0.9, color='blue', marker='.', s=50)
        ax.set_title("PARAMETER OUT OF BOUNDS!", fontweight="bold")

    # Convert plot to image and display in result box
    img_buf = BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    display(Javascript(f'''
    var plotBox = document.getElementById("plotBox");
    plotBox.innerHTML = '<img src="data:image/png;base64,' + "{img_base64}" + '" />';
    '''))

# Register and run the callback to update angle and sheet
output.register_callback('notebook.update_angle_result', update_angle_result)

# Initialize the input boxes and the callback
create_input_boxes()
