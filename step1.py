# Enter the DV offset and RCS-lambda distacne

from ipywidgets import widgets, VBox
from IPython.display import display

# Create two text input boxes
input_RCSL = widgets.Text(description="RCS-lambda distance: ")
input_DVoffset = widgets.Text(description="DV offset: ")

# Display the boxes side by side or vertically
display(VBox([input_box1, input_box2]))

# Function to capture and print the inputs when the button is clicked
def get_inputs(b):
  RCSL = input_RCSL.value
  DVoffset = input_DVoffset.value
  
# Create and display a submit button
button = widgets.Button(description="Submit")
button.on_click(get_inputs)
display(button)
