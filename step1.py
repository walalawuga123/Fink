# Required imports
import math
from google.colab import output
from IPython.display import display, Javascript

# Create input boxes using JavaScript with improved styles
def create_input_boxes():
    display(Javascript('''
    // Create first input box
    var input1 = document.createElement("input");
    input1.id = "input1";
    input1.placeholder = "Enter RCS-lambda distance";
    input1.style.margin = "10px";
    input1.style.padding = "12px";
    input1.style.fontSize = "16px";
    input1.style.width = "300px";
    input1.style.height = "40px";
    
    // Create second input box
    var input2 = document.createElement("input");
    input2.id = "input2";
    input2.placeholder = "Enter DV offset";
    input2.style.margin = "10px";
    input2.style.padding = "12px";
    input2.style.fontSize = "16px";
    input2.style.width = "300px";
    input2.style.height = "40px";

    // Create submit button
    var button = document.createElement("button");
    button.innerHTML = "Submit";
    button.style.margin = "10px";
    button.style.padding = "12px 20px";
    button.style.fontSize = "16px";
    button.style.backgroundColor = "#4CAF50";  // Green color
    button.style.color = "white";
    button.style.border = "none";
    button.style.borderRadius = "8px";
    button.style.cursor = "pointer";

    // On button click, send input values to Python
    button.onclick = function() {
        var val1 = document.getElementById("input1").value;
        var val2 = document.getElementById("input2").value;
        google.colab.kernel.invokeFunction("notebook.calculate_angle", [val1, val2], {});
    }
    
    // Clear previous elements if they exist
    var elements = document.getElementsByClassName("custom-inputs");
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }
    
    // Create a container for better layout
    var container = document.createElement("div");
    container.className = "custom-inputs";
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.alignItems = "center";
    container.style.marginTop = "20px";
    
    // Add elements to container
    container.appendChild(input1);
    container.appendChild(input2);
    container.appendChild(button);
    
    // Add the container to the body
    document.body.appendChild(container);
    '''))
    
# Function to calculate and display angle correction
def AngleCorrection(RCSL, DVoffset):
    try:
        # Convert input to float for calculation
        RCSL = float(RCSL)
        DVoffset = float(DVoffset)
        
        # Calculate pitch correction
        PitchCorrection = round(math.atan(-DVoffset / RCSL) * 180 / 3.14159, 2)
        
        # Print result with emoji for better visibility
        print(f'✅ Advise angle correction: {PitchCorrection}°')
    except ValueError:
        print("⚠️ Please enter valid numerical values.")

# Register the function and create input boxes
output.register_callback('notebook.calculate_angle', AngleCorrection)
create_input_boxes()
