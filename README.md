# Python-Tools
A repository for python functions that can help make things a little easier
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Python Function Extractor
https://github.com/putkoff/Python-Tools/tree/main

This project consists of a Python script that uses the Abstract Syntax Tree (AST) to parse a Python file, extract specific functions along with their dependencies, and output these functions and their dependencies into a new Python file. The script also provides a graphical user interface (GUI) using PySimpleGUI.

![Screenshot 2023-07-22 123734](https://github.com/putkoff/Python-Tools/assets/57512254/e6c3c53a-6f63-4b62-81ee-7b29b409c504)

Features
Parse a Python file to extract function definitions and import statements

Check function dependencies (i.e., other functions that are called within a target function) and include these in the extraction

Handle cases where there are multiple functions with the same name (overloading) in the source file

Allow the user to select which overloaded function to include in the output file

Provide a simple GUI for selecting the source file and the functions to extract

Installation
This script requires Python 3.6 or later. The required libraries are ast, astunparse, and PySimpleGUI.

To install the required libraries, use the following pip commands:

pip install astunparse
pip install PySimpleGUI
How to Use
Run the script. A GUI window will open.

Use the file browser to select a Python (.py) file. If you attempt to select a non-Python file, a popup will inform you to select a Python file.

Click the "Load Functions" button. This will load all the functions in the selected Python file and display them in the list box.

Select one or multiple functions from the list box that you want to extract. Use Ctrl+click to select multiple functions.

Click the "Grab Functions" button. The selected functions along with their dependencies and necessary import statements will be written to a new file named output.py.

If you attempt to grab functions and there are multiple definitions of the selected function in the source file, a new window will open. This window will display the source code of the overloaded functions and ask you to choose one. Make your choice by selecting the radio button next to the corresponding function and click "OK".

Note
This script currently only supports simple import statements (e.g., import os), not from-import statements (e.g., from os import path). Also, it does not account for import aliasing. If your source code uses from-import statements or import aliasing, the resulting output.py might not run as expected.

Support
If you encounter any problems or have any suggestions, please open an issue on this GitHub repository.
