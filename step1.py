import math
from google.colab import output
from IPython.display import display, Javascript

# Create input boxes using JavaScript for better compatibility in Colab
def create_input_boxes():
    display(Javascript('''
    var input1 = document.createElement("input");
    input1.id = "input1";
    input1.placeholder = "Enter RCS-lambda distance";
    input1.style.margin = "5px";
    
    var input2 = document.createElement("input");
    input2.id = "input2";
    input2.placeholder = "Enter DV offset";
    input2.style.margin = "5px";
    
    var button = document.createElement("button");
    button.innerHTML = "Submit";
    button.style.margin = "5px";
    
    button.onclick = function() {
        var val1 = document.getElementById("input1").value;
        var val2 = document.getElementById("input2").value;
        google.colab.kernel.invokeFunction("notebook.calculate_angle", [val1, val2], {});
    }
    
    document.body.appendChild(input1);
    document.body.appendChild(input2);
    document.body.appendChild(button);
    '''))
    
# Function to calculate and display angle correction
def AngleCorrection(RCSL, DVoffset):
    try:
        # Convert input to float for calculation
        RCSL = float(RCSL)
        DVoffset = float(DVoffset)
        
        # Calculate pitch correction
        PitchCorrection = round(math.atan(-DVoffset / RCSL) * 180 / 3.14159, 2)
        
        # Print result
        print(f'Advise angle correction: {PitchCorrection}°')
    except ValueError:
        print("⚠️ Please enter valid numerical values.")

# Register the function and create input boxes
output.register_callback('notebook.calculate_angle', AngleCorrection)
create_input_boxes()
