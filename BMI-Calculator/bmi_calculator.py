import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ==========================================
# DATABASE
# ==========================================

def create_database():
    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            unit_system TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# UNIT CHANGE
# ==========================================

def change_units(event=None):
    unit = unit_var.get()

    if unit == "Metric":

        weight_label.config(text="Weight (kg):")
        height_label.config(text="Height:")

        # Hide Imperial fields
        height_ft_entry.grid_remove()
        height_in_entry.grid_remove()

        # Show Metric field
        height_cm_entry.grid(
            row=3,
            column=1,
            padx=10
        )

        height_unit_label.config(text="cm")

    else:

        weight_label.config(text="Weight (lb):")
        height_label.config(text="Height:")

        # Hide Metric field
        height_cm_entry.grid_remove()

        # Show Imperial fields
        height_ft_entry.grid(
            row=3,
            column=1,
            padx=10
        )

        height_in_entry.grid(
            row=3,
            column=2,
            padx=5
        )

        height_unit_label.config(text="ft")


# ==========================================
# BMI CALCULATION
# ==========================================

def calculate_bmi():

    name = name_entry.get().strip()
    unit = unit_var.get()

    # --------------------------
    # Validate name
    # --------------------------

    if not name:

        messagebox.showerror(
            "Invalid Input",
            "Please enter your name."
        )

        return

    # --------------------------
    # Metric
    # --------------------------

    if unit == "Metric":

        weight_text = weight_entry.get().strip()
        height_text = height_cm_entry.get().strip()

        try:
            weight = float(weight_text)
            height_cm = float(height_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers."
            )

            return

        if weight <= 0:

            messagebox.showerror(
                "Invalid Input",
                "Weight must be greater than 0."
            )

            return

        if height_cm <= 0:

            messagebox.showerror(
                "Invalid Input",
                "Height must be greater than 0."
            )

            return

        # Convert cm to meters
        height_m = height_cm / 100

        # BMI
        bmi = weight / (height_m ** 2)

        display_weight = f"{weight} kg"
        display_height = f"{height_cm} cm"

    # --------------------------
    # US / Imperial
    # --------------------------

    else:

        weight_text = weight_entry.get().strip()
        feet_text = height_ft_entry.get().strip()
        inches_text = height_in_entry.get().strip()

        try:

            weight_lb = float(weight_text)
            feet = float(feet_text)
            inches = float(inches_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers."
            )

            return

        if weight_lb <= 0:

            messagebox.showerror(
                "Invalid Input",
                "Weight must be greater than 0."
            )

            return

        if feet < 0 or inches < 0:

            messagebox.showerror(
                "Invalid Input",
                "Height cannot be negative."
            )

            return

        if feet == 0 and inches == 0:

            messagebox.showerror(
                "Invalid Input",
                "Height must be greater than 0."
            )

            return

        if inches >= 12:

            messagebox.showerror(
                "Invalid Input",
                "Inches must be less than 12."
            )

            return

        # Convert to total inches
        total_inches = feet * 12 + inches

        # BMI formula for pounds/inches
        bmi = (weight_lb / (total_inches ** 2)) * 703

        display_weight = f"{weight_lb} lb"
        display_height = f"{feet} ft {inches} in"

    # ==========================================
    # BMI CATEGORY
    # ==========================================

    if bmi < 18.5:

        category = "Underweight"
        color = "orange"

    elif bmi < 25:

        category = "Normal"
        color = "green"

    elif bmi < 30:

        category = "Overweight"
        color = "orange"

    else:

        category = "Obese"
        color = "red"

    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        foreground=color
    )

    # Save record
    save_record(
        name,
        display_weight,
        display_height,
        bmi,
        category,
        unit
    )


# ==========================================
# SAVE RECORD
# ==========================================

def save_record(
    name,
    weight,
    height,
    bmi,
    category,
    unit
):

    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()

    date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO bmi_records
        (name, weight, height, bmi, category, unit_system, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        weight,
        height,
        bmi,
        category,
        unit,
        date
    ))

    conn.commit()
    conn.close()

    load_history()


# ==========================================
# LOAD HISTORY
# ==========================================

def load_history():

    for row in history_table.get_children():
        history_table.delete(row)

    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, weight, height, bmi,
               category, unit_system, date
        FROM bmi_records
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    for record in records:

        history_table.insert(
            "",
            tk.END,
            values=(
                record[0],
                record[1],
                record[2],
                f"{record[3]:.2f}",
                record[4],
                record[5],
                record[6]
            )
        )


# ==========================================
# SHOW BMI GRAPH
# ==========================================

def show_graph():

    name = name_entry.get().strip()

    if not name:

        messagebox.showwarning(
            "Name Required",
            "Enter a user's name first."
        )

        return

    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, bmi
        FROM bmi_records
        WHERE name = ?
        ORDER BY id
    """, (name,))

    records = cursor.fetchall()

    conn.close()

    if not records:

        messagebox.showinfo(
            "No Data",
            "No BMI records found for this user."
        )

        return

    dates = [
        record[0]
        for record in records
    ]

    bmi_values = [
        record[1]
        for record in records
    ]

    plt.figure(figsize=(9, 5))

    plt.plot(
        dates,
        bmi_values,
        marker="o"
    )

    plt.axhline(
        18.5,
        linestyle="--",
        label="18.5"
    )

    plt.axhline(
        25,
        linestyle="--",
        label="25"
    )

    plt.axhline(
        30,
        linestyle="--",
        label="30"
    )

    plt.title(
        f"BMI History - {name}"
    )

    plt.xlabel("Date")

    plt.ylabel("BMI")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


# ==========================================
# CLEAR FIELDS
# ==========================================

def clear_fields():

    name_entry.delete(0, tk.END)

    weight_entry.delete(0, tk.END)

    height_cm_entry.delete(0, tk.END)

    height_ft_entry.delete(0, tk.END)

    height_in_entry.delete(0, tk.END)

    result_label.config(
        text="BMI: --\nCategory: --",
        foreground="black"
    )


# ==========================================
# CREATE DATABASE
# ==========================================

create_database()


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("BMI Calculator")

root.geometry("950x700")

root.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=15)


subtitle_label = tk.Label(
    root,
    text="Calculate and track your Body Mass Index",
    font=("Arial", 11)
)

subtitle_label.pack()


# ==========================================
# INPUT FRAME
# ==========================================

input_frame = tk.Frame(root)

input_frame.pack(pady=20)


# ==========================================
# NAME
# ==========================================

tk.Label(
    input_frame,
    text="Name:",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8
)

name_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

name_entry.grid(
    row=0,
    column=1,
    padx=10
)


# ==========================================
# UNIT SYSTEM
# ==========================================

tk.Label(
    input_frame,
    text="Unit System:",
    font=("Arial", 12)
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)

unit_var = tk.StringVar()

unit_var.set("Metric")

unit_dropdown = ttk.Combobox(
    input_frame,
    textvariable=unit_var,
    values=[
        "Metric",
        "US / Imperial"
    ],
    state="readonly",
    width=22,
    font=("Arial", 11)
)

unit_dropdown.grid(
    row=1,
    column=1,
    padx=10
)

unit_dropdown.bind(
    "<<ComboboxSelected>>",
    change_units
)


# ==========================================
# WEIGHT
# ==========================================

weight_label = tk.Label(
    input_frame,
    text="Weight (kg):",
    font=("Arial", 12)
)

weight_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=8
)

weight_entry = tk.Entry(
    input_frame,
    width=15,
    font=("Arial", 12)
)

weight_entry.grid(
    row=2,
    column=1,
    padx=10
)


# ==========================================
# HEIGHT LABEL
# ==========================================

height_label = tk.Label(
    input_frame,
    text="Height:",
    font=("Arial", 12)
)

height_label.grid(
    row=3,
    column=0,
    padx=10,
    pady=8
)


# ==========================================
# METRIC HEIGHT
# ==========================================

height_cm_entry = tk.Entry(
    input_frame,
    width=15,
    font=("Arial", 12)
)

height_cm_entry.grid(
    row=3,
    column=1,
    padx=10
)

height_unit_label = tk.Label(
    input_frame,
    text="cm",
    font=("Arial", 11)
)

height_unit_label.grid(
    row=3,
    column=2,
    padx=5
)


# ==========================================
# IMPERIAL HEIGHT
# ==========================================

height_ft_entry = tk.Entry(
    input_frame,
    width=8,
    font=("Arial", 12)
)

height_in_entry = tk.Entry(
    input_frame,
    width=8,
    font=("Arial", 12)
)


# ==========================================
# BUTTONS
# ==========================================

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


calculate_button = tk.Button(
    button_frame,
    text="Calculate BMI",
    command=calculate_bmi,
    width=15,
    font=("Arial", 11, "bold")
)

calculate_button.grid(
    row=0,
    column=0,
    padx=5
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=10,
    font=("Arial", 11)
)

clear_button.grid(
    row=0,
    column=1,
    padx=5
)


graph_button = tk.Button(
    button_frame,
    text="View BMI Trend",
    command=show_graph,
    width=15,
    font=("Arial", 11)
)

graph_button.grid(
    row=0,
    column=2,
    padx=5
)


# ==========================================
# RESULT
# ==========================================

result_label = tk.Label(
    root,
    text="BMI: --\nCategory: --",
    font=("Arial", 18, "bold")
)

result_label.pack(pady=15)


# ==========================================
# HISTORY
# ==========================================

history_label = tk.Label(
    root,
    text="BMI History",
    font=("Arial", 16, "bold")
)

history_label.pack(pady=5)


columns = (
    "Name",
    "Weight",
    "Height",
    "BMI",
    "Category",
    "Unit",
    "Date"
)

history_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=10
)


for column in columns:

    history_table.heading(
        column,
        text=column
    )

    history_table.column(
        column,
        width=120
    )


history_table.pack(
    padx=20,
    pady=10
)


# ==========================================
# LOAD OLD RECORDS
# ==========================================

load_history()


# ==========================================
# START APPLICATION
# ==========================================

root.mainloop()