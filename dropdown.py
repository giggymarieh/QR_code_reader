import tkinter as tk
from tkinter import ttk

def selection(event):
 selected_entry= combo_var.get()

 combo_var = tk.StringVar()# Create a variable to hold the selected value

# Create a ComboBox widget
 combo = ttk.Combobox(textvariable=combo_var)
 combo["values"] = ("Day 1", "Day 2", "Day 3")
 combo.bind("<<ComboboxSelected>>",selection)

 combo.pack(padx=20, pady=20)# Place the ComboBox on the window

# Create a variable to hold the selected sub-value
 sub_combo_var = tk.StringVar()

# Create a list of sub-options
 sub_options = {
    "Option 1": ["Sub-option 1-1", "Sub-option 1-2", "Sub-option 1-3"],
    "Option 2": ["Sub-option 2-1", "Sub-option 2-2", "Sub-option 2-3"],
    "Option 3": ["Sub-option 3-1", "Sub-option 3-2", "Sub-option 3-3"]
}

# Create the OptionMenu widget for sub-options
sub_combo = ttk.OptionMenu( sub_combo_var, None, ())
sub_combo.pack(padx=20)

# Function to update sub-options based on the selected main option
def update_sub_options(*args):
    selected_option = combo_var.get()
    sub_options_list = sub_options.get(selected_option, [])
    sub_combo["menu"].delete(0, "end")
    for sub_option in sub_options_list:
        sub_combo["menu"].add_command(label=sub_option, command=lambda value=sub_option: sub_combo_var.set(value))

# Link the main ComboBox selection to updating the sub-options
combo_var.trace("w", update_sub_options)

