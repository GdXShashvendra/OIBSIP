# 🔐 Secure Random Password Generator

A Python GUI application that generates strong and cryptographically secure passwords based on user-defined requirements.

## 🚀 Features

- Password length control from 8 to 128 characters
- Uppercase letters
- Lowercase letters
- Numbers
- Symbols
- At least two character types required
- Guaranteed inclusion of every selected character type
- Cryptographically secure password generation using Python `secrets`
- Password strength indicator
- Automatic clipboard copying
- Manual copy-to-clipboard button
- Option to exclude ambiguous characters
- Last 5 generated passwords displayed during the current session
- Input validation
- No password history is stored on disk

## 🛠️ Technologies

- Python
- Tkinter
- secrets
- string
- pyperclip

## 📁 Project Structure

```text
Random-Password-Generator/
│
├── password_generator.py
├── requirements.txt
└── README.md