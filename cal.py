import customtkinter as ctk
from sympy import sympify, solve, diff, integrate, symbols, SympifyError
from sympy.plotting import plot as sympy_plot
from pint import UnitRegistry
import re

# Initialize unit registry for conversions
ureg = UnitRegistry()

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("AI-Powered Advanced Calculator")
app.geometry("500x700")

# Entry widget for display
display = ctk.CTkEntry(app, font=("Helvetica", 24), justify="right")
display.grid(row=0, column=0, columnspan=4, pady=20, padx=10, sticky="ew")

# Natural language input
nl_input = ctk.CTkEntry(
    app,
    placeholder_text="Ask me (e.g., 'What is 5% of 200?' or 'Solve x^2 - 4 = 0')",
    font=("Helvetica", 14)
)
nl_input.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

# History display
history_label = ctk.CTkLabel(app, text="History:", font=("Helvetica", 14))
history_label.grid(row=2, column=0, columnspan=4, pady=5, padx=10, sticky="w")
history_text = ctk.CTkTextbox(app, width=400, height=100, font=("Helvetica", 12))
history_text.grid(row=3, column=0, columnspan=4, pady=5, padx=10, sticky="ew")

# Button layout
buttons = [
    ("7", 4, 0), ("8", 4, 1), ("9", 4, 2), ("/", 4, 3),
    ("4", 5, 0), ("5", 5, 1), ("6", 5, 2), ("*", 5, 3),
    ("1", 6, 0), ("2", 6, 1), ("3", 6, 2), ("-", 6, 3),
    ("0", 7, 0), (".", 7, 1), ("=", 7, 2), ("+", 7, 3),
    ("Solve", 8, 0), ("Clear", 8, 1), ("%", 8, 2), ("^", 8, 3),
    ("Diff", 9, 0), ("Integrate", 9, 1), ("Convert", 9, 2), ("Plot", 9, 3),
]

# Create buttons
for (text, row, col) in buttons:
    btn = ctk.CTkButton(
        app,
        text=text,
        font=("Helvetica", 16),
        width=50,
        height=50,
        command=lambda t=text: on_button_click(t)
    )
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

# Button click logic
def on_button_click(value):
    if value == "=":
        try:
            result = eval(display.get())
            update_history(f"{display.get()} = {result}")
            display.delete(0, ctk.END)
            display.insert(0, str(result))
        except:
            display.delete(0, ctk.END)
            display.insert(0, "Error")
    elif value == "Clear":
        display.delete(0, ctk.END)
    elif value == "Solve":
        solve_equation()
    elif value == "%":
        display.insert(ctk.END, "/100")
    elif value == "Diff":
        differentiate()
    elif value == "Integrate":
        integrate_func()
    elif value == "Convert":
        convert_units()
    elif value == "Plot":
        plot_function()
    else:
        display.insert(ctk.END, value)

# Solve equations (e.g., "x^2 - 4 = 0")
def solve_equation():
    try:
        equation = display.get()
        x = symbols('x')
        solutions = solve(sympify(equation), x)
        update_history(f"Solved: {equation} = {solutions}")
        display.delete(0, ctk.END)
        display.insert(0, f"Solutions: {solutions}")
    except SympifyError:
        display.delete(0, ctk.END)
        display.insert(0, "Invalid equation")

# Differentiate a function
def differentiate():
    try:
        func = display.get()
        x = symbols('x')
        derivative = diff(sympify(func), x)
        update_history(f"Derivative of {func}: {derivative}")
        display.delete(0, ctk.END)
        display.insert(0, f"Derivative: {derivative}")
    except SympifyError:
        display.delete(0, ctk.END)
        display.insert(0, "Invalid function")

# Integrate a function
def integrate_func():
    try:
        func = display.get()
        x = symbols('x')
        integral = integrate(sympify(func), x)
        update_history(f"Integral of {func}: {integral}")
        display.delete(0, ctk.END)
        display.insert(0, f"Integral: {integral}")
    except SympifyError:
        display.delete(0, ctk.END)
        display.insert(0, "Invalid function")

# Convert units (e.g., "10 meters to feet")
def convert_units():
    try:
        query = display.get()
        match = re.match(r"(\d+)\s*([a-zA-Z]+)\s*to\s*([a-zA-Z]+)", query)
        if match:
            amount, from_unit, to_unit = match.groups()
            quantity = float(amount) * ureg(f"{from_unit}")
            result = quantity.to(f"{to_unit}")
            update_history(f"Converted {amount} {from_unit} to {result}")
            display.delete(0, ctk.END)
            display.insert(0, f"{result}")
        else:
            display.delete(0, ctk.END)
            display.insert(0, "Invalid format. Use: '10 meters to feet'")
    except:
        display.delete(0, ctk.END)
        display.insert(0, "Conversion error")

# Plot a function
def plot_function():
    try:
        func = display.get()
        x = symbols('x')
        sympy_plot(sympify(func), (x, -10, 10), title=f"Plot of {func}")
        update_history(f"Plotted: {func}")
    except SympifyError:
        display.delete(0, ctk.END)
        display.insert(0, "Invalid function")

# Update history
def update_history(entry):
    history_text.insert(ctk.END, entry + "\n")
    history_text.see(ctk.END)

# Natural language processing (simple keyword parser)
def parse_natural_language():
    query = nl_input.get().lower()
    if "what is" in query and "%" in query:
        parts = query.split()
        num = float(parts[2])
        percent = float(parts[4])
        result = (percent / 100) * num
        update_history(f"Calculated: {percent}% of {num} = {result}")
        display.delete(0, ctk.END)
        display.insert(0, f"{result}")
    elif "solve" in query:
        equation = query.replace("solve", "").strip()
        display.delete(0, ctk.END)
        display.insert(0, equation)
        solve_equation()
    else:
        display.delete(0, ctk.END)
        display.insert(0, "Unsupported query")

# Bind natural language input to Enter key
nl_input.bind("<Return>", lambda event: parse_natural_language())

# Configure grid weights for resizing
for i in range(4):
    app.grid_columnconfigure(i, weight=1)
for i in range(10):
    app.grid_rowconfigure(i, weight=1)

# Run the app
app.mainloop()

