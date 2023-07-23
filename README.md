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

## Installation

This script necessitates Python 3.6 or higher. The required libraries are `ast`, `astunparse`, and `PySimpleGUI`.

To install the requisite libraries, employ the following pip commands:

```bash
pip install astunparse
pip install PySimpleGUI
```

## Usage

1. Execute the script. A GUI window will appear.
2. Use the file browser to select a Python (.py) file. If you try to select a non-Python file, a popup will notify you to select a Python file.
3. Click the "Load Functions" button. This action will load all the functions in the selected Python file and display them in the list box.
4. Choose one or multiple functions from the list box that you wish to extract. Utilize Ctrl+click to select multiple functions.
5. Press the "Grab Functions" button. The chosen functions along with their dependencies and necessary import statements will be written to a new file named `output.py`.
6. If you attempt to grab functions and there are multiple definitions of the selected function in the source file, a new window will launch. This window will show the source code of the overloaded functions and prompt you to make a choice. Make your selection by clicking the radio button next to the corresponding function and press "OK".

## Note
This script currently only supports simple import statements (e.g., `import os`), not from-import statements (e.g., `from os import path`). Additionally, it does not account for import aliasing. If your source code employs from-import statements or import aliasing, the resulting `output.py` might not function as expected.

## Support
If you encounter any issues or have any suggestions, please open an issue on this GitHub repository.
