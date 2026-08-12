import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip


# ==========================================
# CHARACTER SETS
# ==========================================

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"

AMBIGUOUS = "0Ol1I"


# ==========================================
# PASSWORD HISTORY
# ==========================================

password_history = []


# ==========================================
# GENERATE SECURE PASSWORD
# ==========================================

def generate_password():

    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Length",
            "Please enter a valid password length."
        )
        return

    # Minimum length
    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    # Selected character types
    selected_types = []

    if uppercase_var.get():
        selected_types.append("uppercase")

    if lowercase_var.get():
        selected_types.append("lowercase")

    if numbers_var.get():
        selected_types.append("numbers")

    if symbols_var.get():
        selected_types.append("symbols")

    # At least two types required
    if len(selected_types) < 2:
        messagebox.showerror(
            "Character Types Required",
            "Please select at least two character types."
        )
        return

    # ==========================================
    # BUILD CHARACTER POOL
    # ==========================================

    character_sets = []

    if uppercase_var.get():
        character_sets.append(UPPERCASE)

    if lowercase_var.get():
        character_sets.append(LOWERCASE)

    if numbers_var.get():
        character_sets.append(NUMBERS)

    if symbols_var.get():
        character_sets.append(SYMBOLS)

    # Remove ambiguous characters
    if ambiguous_var.get():

        character_sets = [
            remove_ambiguous(char_set)
            for char_set in character_sets
        ]

    # Make sure no character set became empty
    character_sets = [
        char_set
        for char_set in character_sets
        if char_set
    ]

    if len(character_sets) < 2:
        messagebox.showerror(
            "Invalid Selection",
            "Your selected character types contain no usable characters."
        )
        return

    # Password must contain at least one
    # character from every selected type
    password_characters = []

    for char_set in character_sets:
        password_characters.append(
            secrets.choice(char_set)
        )

    # Combined pool
    combined_pool = "".join(character_sets)

    # Fill remaining characters
    while len(password_characters) < length:

        password_characters.append(
            secrets.choice(combined_pool)
        )

    # Securely shuffle the password
    password_characters = secure_shuffle(
        password_characters
    )

    password = "".join(password_characters)

    # Display password
    password_var.set(password)

    # Update strength
    update_strength(
        length,
        len(selected_types)
    )

    # Copy automatically
    try:
        pyperclip.copy(password)
        clipboard_label.config(
            text="✓ Password copied to clipboard"
        )
    except Exception:
        clipboard_label.config(
            text="⚠ Could not access clipboard"
        )

    # Add to history
    add_to_history(password)


# ==========================================
# REMOVE AMBIGUOUS CHARACTERS
# ==========================================

def remove_ambiguous(characters):

    return "".join(
        char
        for char in characters
        if char not in AMBIGUOUS
    )


# ==========================================
# SECURE SHUFFLE
# ==========================================

def secure_shuffle(items):

    items = items.copy()

    for i in range(len(items) - 1, 0, -1):

        j = secrets.randbelow(i + 1)

        items[i], items[j] = (
            items[j],
            items[i]
        )

    return items


# ==========================================
# PASSWORD STRENGTH
# ==========================================

def update_strength(length, type_count):

    if length >= 16 and type_count >= 4:

        strength = "Strong"
        progress = 100

    elif length >= 12 and type_count >= 3:

        strength = "Strong"
        progress = 85

    elif length >= 10 and type_count >= 3:

        strength = "Medium"
        progress = 65

    elif length >= 8 and type_count >= 2:

        strength = "Medium"
        progress = 50

    else:

        strength = "Weak"
        progress = 30

    strength_label.config(
        text=f"Strength: {strength}"
    )

    strength_bar["value"] = progress


# ==========================================
# COPY PASSWORD
# ==========================================

def copy_password():

    password = password_var.get()

    if not password:

        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )

        return

    try:

        pyperclip.copy(password)

        clipboard_label.config(
            text="✓ Password copied to clipboard"
        )

    except Exception:

        messagebox.showerror(
            "Clipboard Error",
            "Unable to access clipboard."
        )


# ==========================================
# HISTORY
# ==========================================

def add_to_history(password):

    password_history.insert(
        0,
        password
    )

    # Keep only last 5
    if len(password_history) > 5:
        password_history.pop()

    update_history_display()


def update_history_display():

    history_list.delete(
        0,
        tk.END
    )

    for password in password_history:

        history_list.insert(
            tk.END,
            password
        )


# ==========================================
# CLEAR PASSWORD
# ==========================================

def clear_password():

    password_var.set("")

    strength_label.config(
        text="Strength: --"
    )

    strength_bar["value"] = 0

    clipboard_label.config(
        text=""
    )


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Secure Password Generator"
)

root.geometry(
    "650x720"
)

root.resizable(
    False,
    False
)


# ==========================================
# TITLE
# ==========================================

title = tk.Label(
    root,
    text="🔐 Secure Password Generator",
    font=("Arial", 24, "bold")
)

title.pack(
    pady=15
)


subtitle = tk.Label(
    root,
    text="Generate strong cryptographically secure passwords",
    font=("Arial", 11)
)

subtitle.pack()


# ==========================================
# LENGTH
# ==========================================

length_frame = tk.Frame(root)

length_frame.pack(
    pady=20
)

tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    padx=10
)

length_var = tk.IntVar(
    value=16
)

length_spinbox = tk.Spinbox(
    length_frame,
    from_=8,
    to=128,
    textvariable=length_var,
    width=8,
    font=("Arial", 12)
)

length_spinbox.grid(
    row=0,
    column=1
)


# ==========================================
# CHARACTER TYPES
# ==========================================

type_frame = tk.LabelFrame(
    root,
    text="Character Types",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

type_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


uppercase_var = tk.BooleanVar(
    value=True
)

lowercase_var = tk.BooleanVar(
    value=True
)

numbers_var = tk.BooleanVar(
    value=True
)

symbols_var = tk.BooleanVar(
    value=True
)


tk.Checkbutton(
    type_frame,
    text="Uppercase (A-Z)",
    variable=uppercase_var,
    font=("Arial", 11)
).pack(
    anchor="w"
)


tk.Checkbutton(
    type_frame,
    text="Lowercase (a-z)",
    variable=lowercase_var,
    font=("Arial", 11)
).pack(
    anchor="w"
)


tk.Checkbutton(
    type_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 11)
).pack(
    anchor="w"
)


tk.Checkbutton(
    type_frame,
    text="Symbols (!@#$...)",
    variable=symbols_var,
    font=("Arial", 11)
).pack(
    anchor="w"
)


# ==========================================
# AMBIGUOUS CHARACTERS
# ==========================================

ambiguous_var = tk.BooleanVar(
    value=False
)

tk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, l, 1, I)",
    variable=ambiguous_var,
    font=("Arial", 11)
).pack(
    pady=10
)


# ==========================================
# GENERATE BUTTON
# ==========================================

generate_button = tk.Button(
    root,
    text="🔑 Generate Password",
    command=generate_password,
    font=("Arial", 12, "bold"),
    width=25,
    height=2
)

generate_button.pack(
    pady=10
)


# ==========================================
# PASSWORD DISPLAY
# ==========================================

password_var = tk.StringVar()

password_entry = tk.Entry(
    root,
    textvariable=password_var,
    font=("Consolas", 15),
    justify="center",
    width=42,
    state="readonly"
)

password_entry.pack(
    pady=10
)


# ==========================================
# COPY BUTTON
# ==========================================

copy_button = tk.Button(
    root,
    text="📋 Copy to Clipboard",
    command=copy_password,
    width=22,
    font=("Arial", 11)
)

copy_button.pack(
    pady=5
)


clipboard_label = tk.Label(
    root,
    text="",
    font=("Arial", 10)
)

clipboard_label.pack()


# ==========================================
# STRENGTH
# ==========================================

strength_label = tk.Label(
    root,
    text="Strength: --",
    font=("Arial", 12, "bold")
)

strength_label.pack(
    pady=5
)


strength_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    mode="determinate"
)

strength_bar.pack(
    pady=5
)


# ==========================================
# HISTORY
# ==========================================

history_label = tk.Label(
    root,
    text="Last 5 Generated Passwords",
    font=("Arial", 13, "bold")
)

history_label.pack(
    pady=10
)


history_list = tk.Listbox(
    root,
    width=55,
    height=5,
    font=("Consolas", 10)
)

history_list.pack(
    pady=5
)


# ==========================================
# START
# ==========================================

root.mainloop()