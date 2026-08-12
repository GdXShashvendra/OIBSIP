# 🧮 BMI Calculator

A Python GUI application that calculates Body Mass Index (BMI), classifies the result into health categories, stores historical records, and visualizes BMI trends.

## 🚀 Features

- Calculate BMI using weight and height
- BMI classification
- Underweight detection
- Normal weight detection
- Overweight detection
- Obesity detection
- Input validation
- Colour-coded results
- Multi-user support
- SQLite database
- Historical BMI records
- BMI trend visualization
- Clear input functionality

## 🛠️ Technologies Used

- Python
- Tkinter
- SQLite3
- Matplotlib

## 📊 BMI Formula

BMI is calculated using:

BMI = Weight / Height²

Where:

- Weight is measured in kilograms
- Height is measured in meters

## 📋 BMI Categories

| BMI | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| 30 or above | Obese |

## 📁 Project Structure

```text
BMI-Calculator/
│
├── bmi_calculator.py
├── requirements.txt
├── README.md
└── bmi_history.db