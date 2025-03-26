# Required imports
import math
from google.colab import output
from IPython.display import display, Javascript

# Create styled input interface with JS
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

    var input1 = createInput("input1", "Enter RCS-lambda distance");
    var input2 = createInput("input2", "Enter DV offset");
    var input3 = createInput("input3", "Enter Initial angle");

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
    resultBox.style.display = "none";
    resultBox.readOnly = true;

    // Finish button
    var finishButton = document.createElement("button");
    finishButton.innerHTML = "Finish";
    finishButton.style.margin = "10px";
    finishButton.style.padding = "12px 20px";
    finishButton.style.fontSize = "16px";
    finishButton.style.backgroundColor = "#f44336";
    finishButton.style.color = "white";
    finishButton.style.border = "none";
    finishButton.style.borderRadius = "8px";
    finishButton.style.cursor = "pointer";
    finishButton.style.display = "none";

    // Button click action
    button.onclick = function() {
        var val1 = document.getElementById("input1").value;
        var val2 = document.getElementById("input2").value;
        var val3 = document.getElementById("input3").value;
        google.colab.kernel.invokeFunction("notebook.calculate_angle", [val1, val2, val3], {});
    }

    // Finish click action
    finishButton.onclick = function() {
        input1.style.display = "none";
        input2.style.display = "none";
        input3.style.display = "none";
        resultBox.style.display = "none";
        button.style.display = "none";
        finishButton.style.display = "none";
    }

    // Remove any old UI
    var old = document.getElementsByClassName("custom-inputs");
    while (old.length > 0) {
        old[0].parentNode.removeChild(old[0]);
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
    container.appendChild(finishButton);
    document.body.appendChild(container);
    '''))
    
# Python callback to compute angle and return final result
def AngleCorrection(RCSL, DVoffset, initial_angle):
    try:
        # Convert all values to float
        RCSL = float(RCSL)
        DVoffset = float(DVoffset)
        initial_angle = float(initial_angle)

        # Calculate pitch correction
        PitchCorrection = round(math.atan(-DVoffset / RCSL) * 180 / math.pi, 2)

        # Final angle
        AdvisedAngle = round(PitchCorrection + initial_angle, 2)

        # Compose result
        result = (
            f"✅ Pitch correction: {PitchCorrection}°\\n"
            f"➕ Initial angle: {initial_angle}°\\n"
            f"🎯 Advised angle: {AdvisedAngle}°"
        )

    except ValueError:
        result = "⚠️ Please enter valid numerical values."

    # Display the result
    output_result(result)

# Display result in textarea
def output_result(result):
    display(Javascript(f'''
    var resultBox = document.getElementById("resultBox");
    resultBox.style.display = "block";
    resultBox.value = `{result}`;

    var finishButton = document.querySelector("button:nth-of-type(2)");
    finishButton.style.display = "block";
    '''))
    
# Register and run
output.register_callback('notebook.calculate_angle', AngleCorrection)
create_input_boxes()
