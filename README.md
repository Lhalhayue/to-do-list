# PinkPlan - To-Do List Management System

## Before running
Open `main.py` and replace `[Your Roll Number]` in the window title and About dialog with your actual roll number. Your lecturer requires your name and roll number to be visible in the application title or About dialog for screenshots.

## Install
Open the terminal in this folder and run:

```powershell
python -m pip install -r requirements.txt
```

## Run
```powershell
python main.py
```

## Files
- `main.py`: PyQt6 interface, menu, event handling, validation and display.
- `task_logic.py`: add, update, delete, complete, filter and JSON file operations.
- `tasks.json`: sample task data. The application updates this file as you work.
- `partA/`: Hello World examples for PyQt6, Tkinter and Kivy.

## Optional Kivy example
Install Kivy separately before running its example:

```powershell
python -m pip install kivy
python partA/hello_kivy.py
```

## Assignment checklist
This project includes a main window and menu bar, more than eight widget types, QVBoxLayout/QGridLayout/QHBoxLayout, more than five signal-slot connections, message dialogs, input validation, JSON persistence, pink-and-white styling, and separate GUI and logic files. It also includes search and filtering as stretch features.

Test every feature yourself and take screenshots from your own running application. Complete your test results and write your report based on what you actually observe.
