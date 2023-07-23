Terminal_input_tools

# Python Terminal Input Tool

## Overview
This Python script provides a simple and effective way to execute terminal commands within your Python environment. It not only automates terminal tasks but also enables the interaction of Python with bash shell commands.

## Features

- Deletes files using a function `delFile(x)`.
- Sets the home directory with `homeIt()`.
- Modifies the global variable using `changeGlob(x, y)`.
- Changes file permissions using `chmodIt(x)`.
- Writes text to a file with `pen(x, y)`.
- Reads text from a file using `reader(x)`.
- Adds a character to a string `k` times with `addThis(x, y, k)`.
- Formats text with tabs using `tabIt(x)`.
- Creates a path by joining two strings with `createPath(x, y)`.
- Converts a filename into an absolute path with `makeFileCurr(x)`.
- Creates a bash sample script using `createBashSamp()`.
- Checks if a specific process has finished using `lastP(x)`.
- Executes bash commands using `bash_it(x)`.
- Creates a password script for sudo tasks with `createPassScript()`.
- Replaces 'sudo' in a command with a method for entering password with `sudoReplace(x)`.
- Executes a list of commands using `runAllStrings(ls)`.
- Installs OpenVPN using a list of commands with `installOpenVpn()`.

## Prerequisites
This script requires Python 3.6 or later. The required libraries are `os`, `func`, `subprocess`, and `stat`.

## Usage

Import the required modules and define the functions you want to use. After defining the functions, call them as needed. For example, to create a password script for sudo tasks:

```python
homeIt()
createPassScript()
```

## Support
For any issues or suggestions, please open an issue on this GitHub repository.
