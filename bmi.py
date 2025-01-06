import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive values.")

        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        bmi_label.config(text=f"BMI: {bmi:.2f}")
        category_label.config(text=f"Category: {category}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except ZeroDivisionError:
        messagebox.showerror("Error", "Height cannot be zero.")

def clear_entries():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    bmi_label.config(text="")
    category_label.config(text="")

# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")

# Input Fields
tk.Label(root, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=10)
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Height (m):").grid(row=1, column=0, padx=10, pady=10)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1, padx=10, pady=10)

# Buttons
calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, column=0, padx=10, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_entries)
clear_button.grid(row=2, column=1, padx=10, pady=10)

# Result Labels
bmi_label = tk.Label(root, text="", font=("Helvetica", 12))
bmi_label.grid(row=3, column=0, columnspan=2, pady=10)

category_label = tk.Label(root, text="", font=("Helvetica", 12))
category_label.grid(row=4, column=0, columnspan=2, pady=10)

# Start GUI Event Loop
root.mainloop()
