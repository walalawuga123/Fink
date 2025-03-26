# Required imports
import math
from google.colab import output
from IPython.display import display, Javascript, HTML

# Create input boxes and result box with improved styles
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

    // Create result box
    var resultBox = document.createElement("textarea");
    resultBox.id = "resultBox";
    resultBox.style.margin = "10px";
    resultBox.style.padding = "12px";
    resultBox.style.fontSize = "16px";
    resultBox.style.width = "300px";
    resultBox.style.height = "100px";
    resultBox.style.display = "none";  // Hide initially
    resultBox.readOnly = true;
    
    // Create finish button
    var finishButton = document.createElement("button");
    finishButton.innerHTML = "Finish";
    finishButton.style.margin = "10px";
    finishButton.style.padding = "12px 20px";
    finishButton.style.fontSize = "16px";
    finishButton.style.backgroundColor = "#f44336";  // Red color
    finishButton.style.color = "white";
    finishButton.style.border = "none";
    finishButton.style.borderRadius = "8px";
    finishButton.style.cursor = "pointer";
    finishButton.style.display = "none";  // Hide initially
    
    // On button click, send input values to Python
    button.onclick = function() {
        var val1 = document.getElementById("input1").value;
        var val2 = document.getElementById("input2").value;
        google.colab.kernel.invokeFunction("notebook.calculate_angle", [val1, val2], {});
    }
    
    // On finish button click, hide all elements
    finishButton.onclick = function() {
        document.getElementById("input1").style.display = "none";
        document.getElementById("input2").style.display = "none";
        document.getElementById("resultBox").style.display = "none";
        button.style.display = "none";
        finishButton.style.display = "none";
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
    container.appendChild(resultBox);
    container.appendChild(finishButton);
    
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
        
        # Update result box with the calculated value
        output_result(f'✅ Advise angle correction: {PitchCorrection}°')
    except ValueError:
        output_result("⚠️ Please enter valid numerical values.")
        
# Function to update the result box and show it
def output_result(result):
    display(Javascript(f'''
    var resultBox = document.getElementById("resultBox");
    resultBox.style.display = "block";
    resultBox.value = "{result}";
    
    var finishButton = document.querySelector("button:nth-of-type(2)");
    finishButton.style.display = "block";
    '''))
    
# Hide unnecessary Colab logs
def suppress_logs():
    display(Javascript('''
    var outputArea = document.querySelectorAll('.output');
    for (var i = 0; i < outputArea.length; i++) {
        if (outputArea[i].innerText.includes("Cloning into")) {
            outputArea[i].style.display = "none";
        }
    }
    '''))
    
# Register the function and create input boxes
output.register_callback('notebook.calculate_angle', AngleCorrection)
create_input_boxes()
suppress_logs()
