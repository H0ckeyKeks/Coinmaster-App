import tkinter as tk
from tkinter import ttk  # Themed Tkinter Widgets, which is for buttons, labels, dropdowns etc.
import requests


def convert_currency():
    base_currency = selected_country.get() # Get selected country's currency
    target_currency = target_currency_var.get()
    try:
        amount = float(amount_entry.get())
    # Handling possible errors
    except ValueError:
        conversion_result_label.config(text="Invalid amount. Please enter a number.")
        return

    # Call Frankfurter API for exchange rates
    response = requests.get("https://frankfurter.dev/latest", params={"base": base_currency, "symbols": target_currency})

    if response.status_code == 200:
        rates = response.json().get("rates", {})
        converted_amount = amount * rates.get(target_currency, 0)
        conversion_result_label.config(text=f"{amount} {base_currency} = {converted_amount: .2f} {target_currency}")
    # error handling
    else:
        conversion_result_label.config(text="Error fetching conversion rates")


def calculate_breakdown():
    try:
        amount = float(amount_breakdown_entry.get())
    # Handling possible errors
    except ValueError:
        breakdown_result_label.config(text="Invalid amount. Please enter a number")
        return

    # Retrieve the selected country
    selected_country_name = selected_country.get()


    # Definition of denominations for all Countries
    currency_denominations = {
        "USA": [100, 50, 20, 10, 5, 2, 1, 0.25, 0.10, 0.05, 0.01],
        "Germany": [500, 200, 100, 50, 20, 10, 5, 1, 2, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01],
        "UK": [50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01],
        "Canada": [100, 50, 20, 10, 5, 2, 1, 0.50, 0.25, 0.10, 0.05],
        "Sweden": [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1],
        "Switzerland": [1000, 200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05],
        "Japan": [10000, 5000, 2000, 1000, 500, 100, 50, 10, 5, 1]
    }

    # Get appropriate denominations for selected country
    denominations = currency_denominations.get(selected_country_name)
    if not denominations:
        breakdown_result_label.config(text="Unsupported country.")
        return

    # Calculate the breakdown
    breakdown = {}
    for d in denominations:
        count, amount = divmod(amount, d)
        if count:
            breakdown[d] = int(count)

    # Turning the result into text
    if breakdown:
        result_text = "\n".join([f"{count} x {d}" for d, count in breakdown.items()])
    else:
        result_text = "No denominations found for the given amount."

    # Display the breakdown
    breakdown_result_label.config(text=result_text)


# Create a drop down menu for user input
def on_country_select(event):
    label_action.config(text=f"You selected: {selected_country.get()}. What would you like to do?")
    # Show the action options
    action_frame.pack()

def on_action_select(action):
    selected_action.set(action)
    if action == "Convert Currency":
        conversion_frame.pack() # Show conversion inputs
        breakdown_frame.forget() # Hide denomination breakdown inputs
    elif action == "Calculate Coins and Bills":
        breakdown_frame.pack() # Show breakdown inputs
        conversion_frame.forget() # Hide conversion inputs

# Create main window
root = tk.Tk()  # Creates the main application window
root.title("Coinmaster App")

# Dropdown Menu for selecting a country
# Create variable to hold the selected value
selected_country = tk.StringVar()  # Special variable to manage & store data in tkinter applications; is a bridge between a widget and the variable it is tied to

# Create dropdown options
countries = ["USA", "Germany", "UK", "Canada", "Sweden", "Switzerland", "Japan"]

# Create the dropdown menu
dropdown = ttk.Combobox(root, textvariable=selected_country, values=(countries))
dropdown.set("Select a country") # Default value
dropdown.bind("<<ComboboxSelected>>", on_country_select) # Bind an event to capture selection
dropdown.pack(pady=10)


# Label for actions
label_action = tk.Label(root, text="Select a country to proceed.")
label_action.pack()


# Frame for action selection input
action_frame = tk.Frame(root)
selected_action = tk.StringVar()
tk.Button(action_frame, text="Convert Currency", command=lambda: on_action_select("Convert Currency")).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="Calculate Coins and Bills", command=lambda: on_action_select("Calculate Coins and Bills")).pack(side=tk.RIGHT, padx=5)


# Frame for currency conversion input
conversion_frame = tk.Frame(root)
tk.Label(conversion_frame, text="Enter amount:").pack(side=tk.LEFT)
amount_entry = tk.Entry(conversion_frame)
amount_entry.pack(side=tk.LEFT)
target_currency_var = tk.StringVar()
ttk.Combobox(conversion_frame, textvariable=target_currency_var, values=countries).pack(side=tk.LEFT)
conversion_result_label = tk.Label(conversion_frame, text="")
conversion_result_label.pack()
# Button to trigger conversion
tk.Button(conversion_frame, text="Convert", command=convert_currency).pack()


# Frame for denomination breakdown input
breakdown_frame = tk.Frame(root)
tk.Label(breakdown_frame, text="Enter amount to calculate denominations:").pack(side=tk.LEFT)
amount_breakdown_entry = tk.Entry(breakdown_frame)
amount_breakdown_entry.pack(side=tk.LEFT)
breakdown_result_label = tk.Label(breakdown_frame, text="")
breakdown_result_label.pack()
# Button to trigger calculation
tk.Button(breakdown_frame, text="Calculate", command=calculate_breakdown).pack()


# Start GUI event loop
root.mainloop()





