import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError("Password length must be greater than 0.")
        
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        character_pool = ""
        if use_letters:
            character_pool += string.ascii_letters
        if use_numbers:
            character_pool += string.digits
        if use_symbols:
            character_pool += string.punctuation

        if not character_pool:
            messagebox.showerror("Error", "No character types selected for password generation.")
            return
        
        password = ''.join(random.choice(character_pool) for _ in range(length))
        result_label.config(text=f"Generated Password: {password}")
        
        # Copy password to clipboard
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Success", "Password copied to clipboard!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    length_entry.delete(0, tk.END)
    letters_var.set(True)
    numbers_var.set(True)
    symbols_var.set(True)
    result_label.config(text="")

# GUI Setup
root = tk.Tk()
root.title("Password Generator")

# Input Fields
tk.Label(root, text="Password Length:").grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Character Type Checkboxes
letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=letters_var).grid(row=1, column=0, padx=10, pady=5)
tk.Checkbutton(root, text="Include Numbers", variable=numbers_var).grid(row=1, column=1, padx=10, pady=5)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).grid(row=2, column=0, padx=10, pady=5)

# Buttons
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=0, padx=10, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=3, column=1, padx=10, pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Start GUI Event Loop
root.mainloop()
