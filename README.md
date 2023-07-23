# Python-Tools
A repository for python functions that can help make things a little easier

Tools Index:

# Python Function Extractor

![Screenshot 2023-07-22 123734](https://github.com/putkoff/Python-Tools/assets/57512254/e6c3c53a-6f63-4b62-81ee-7b29b409c504.png)

## Overview
This project comprises a Python script that utilizes the Abstract Syntax Tree (AST) to parse a Python file, extract specific functions along with their dependencies, and export these functions and their dependencies into a new Python file. Additionally, the script incorporates a graphical user interface (GUI) using PySimpleGUI.
## Features

- Parse a Python file to extract function definitions and import statements.
- Check function dependencies (i.e., other functions that are called within a target function) and include these in the extraction.
- Handle scenarios where there are multiple functions with the same name (overloading) in the source file.
- Permit the user to select which overloaded function to include in the output file.
- Provide a user-friendly GUI for selecting the source file and the functions to extract.

