import os
import ast
import PySimpleGUI as psg
def get_imp_defs(file):
    func_ls,class_ls = [],[]
    with open(file, "r") as source:
        text = source.read()
    lines = text.split('\n')
    for line in lines:
        if line[:len('def ')] == 'def ':
            func_ls.append(line.split('def ')[1].split('(')[0])
        if line[:len('class ')] == 'class ':
            class_ls.append(line.split('class ')[1].split('(')[0])
    return func_ls,class_ls
def get_funcs(file):
    with open(file, "r") as source:
        tree = ast.parse(source.read())
    return [func for func in ast.walk(tree) if isinstance(func, ast.FunctionDef)]

def get_imports(file):
    with open(file, "r") as source:
        tree = ast.parse(source.read())
    return [imp.names[0].name for imp in ast.walk(tree) if isinstance(imp, (ast.Import, ast.ImportFrom))]

def get_classes(file):
    with open(file, "r") as source:
        tree = ast.parse(source.read())
    return [cls.name for cls in ast.walk(tree) if isinstance(cls, ast.ClassDef)]

import os
import ast
import PySimpleGUI as psg
import ast
class DependencyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.functions = set()
        self.classes = {}
        self.method_calls = {}

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(f'{node.module}.{alias.name}')

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.functions.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.functions.add(node.func.attr)
        self.generic_visit(node)  # continue to visit children nodes

    def visit_Name(self, node):
        self.functions.add(node.id)
        self.generic_visit(node)  # continue to visit children nodes

    def visit_Attribute(self, node):
        self.functions.add(node.attr)
        self.generic_visit(node)  # continue to visit children nodes

    # Add visit_FunctionDef to visit function definitions inside a function
    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        for child in ast.iter_child_nodes(node):
            self.visit(child)

    # Add visit_ClassDef to visit class definitions inside a function
    def visit_ClassDef(self, node):
        self.classes[node.name] = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        for child in ast.iter_child_nodes(node):
            self.visit(child)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                self.method_calls[node.func.attr] = node.func.value.id
        else:
            self.generic_visit(node)
class FunctionAnalyser:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as source:
            self.source_code = source.read()
            self.tree = ast.parse(self.source_code)

    def get_funcs(self):
        return [func for func in ast.walk(self.tree) if isinstance(func, ast.FunctionDef)]

    def get_imports(self):
        return [imp.names[0].name for imp in ast.walk(self.tree) if isinstance(imp, (ast.Import, ast.ImportFrom))]

    def get_classes(self):
        return [cls.name for cls in ast.walk(self.tree) if isinstance(cls, ast.ClassDef)]

    def get_func_deps(self, func_name):
        func_def_node = next((node for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef) and node.name == func_name), None)
        if func_def_node is None:
            print(f"Function '{func_name}' not found in script.")
            return None

        visitor = DependencyVisitor()
        for node in func_def_node.body:
            visitor.visit(node)

        return visitor.imports, visitor.functions, visitor.classes

    def get_import_lines(self):
        lines = self.source_code.split('\n')
        return [line for line in lines if line.startswith(('import ', 'from '))]

    def get_func_code(self, func_name):
        func_node = next((node for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef) and node.name == func_name), None)
        if func_node is None:
            return ""

        start_line = func_node.lineno
        end_line = start_line + len(func_node.body)
        lines = self.source_code.split('\n')
        func_code = "\n".join(lines[start_line-1:end_line])

        return func_code

def get_func_deps(script, func_name):
    # Parse script into an Abstract Syntax Tree (AST)
    tree = ast.parse(script)

    # Find the function definition node for the given function name
    func_def_node = next((node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == func_name), None)
    if func_def_node is None:
        print(f"Function '{func_name}' not found in script.")
        return None

    # Visit each node in the function body and collect dependencies
    visitor = DependencyVisitor()
    input(visitor)
    for node in func_def_node.body:
        visitor.visit(node)

    return visitor.imports, visitor.functions, visitor.classes

def get_deps_of_func(func, file):
    with open(file, "r") as source:
        tree = ast.parse(source.read())
    func_node = next((node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == func), None)
    if func_node is None:
        return set(), set(), set()

    visitor = DependencyVisitor()
    all_funcs = get_funcs(file)
    all_funcs = [func.name for func in all_funcs]
    all_classes = get_classes(file)
    all_imports = get_imports(file)

    for child in ast.iter_child_nodes(func_node):
        visitor.visit(child)

    # remove any function from visitor.functions that is not in all_funcs, all_classes or all_imports
    visitor.functions = {f for f in visitor.functions if f in all_funcs or f in all_classes or f in all_imports}

    # if a method call is associated with a class, remove the method call from visitor.functions and add the class to visitor.classes
    for method, cls in visitor.method_calls.items():
        if method in visitor.functions:
            visitor.functions.remove(method)
        if cls in all_classes:
            visitor.classes.add(cls)

    return visitor.imports, visitor.functions, visitor.classes


def get_func_code(func, file):
    with open(file, 'r') as f:
        lines = f.readlines()

    code = ''
    recording = False
    indentation = ''

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('def ' + func) or stripped.startswith('class ' + func):
            recording = True
            indentation = line[:len(line) - len(stripped)]
        elif line.startswith(indentation + 'def ') or line.startswith(indentation + 'class '):
            if recording:  # Stop recording if another function/class is encountered
                recording = False
        if recording:
            code += line

    return code
def get_import_lines(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    # Filter lines starting with 'import' or 'from'
    import_lines = [line for line in lines if line.startswith(('import ', 'from '))]

    return import_lines

layout = [
    [psg.FileBrowse(file_types=(("Python Files", "*.py"),), key='-FILEBROWSE-')],
    [psg.Button("Load Functions")],
    [psg.Listbox(values=[], size=(40, 10), key='-LIST-', enable_events=True, select_mode='multiple')],
    [psg.Multiline(size=(60, 20), key='-MULTI-', disabled=True)],
    [psg.Text('Save Location'), psg.InputText(os.getcwd(), key='-SAVEFOLDER-', disabled=True), psg.FolderBrowse('Browse', key='-FOLDERBROWSE-')],
    [psg.Text('Output Filename'), psg.InputText("output", key='-OUTPUTFILE-')],
    [psg.Button('Make Functions'), psg.Button('Grab Dependencies'), psg.Button('Exit')],
]

window = psg.Window('Python Function Browser', layout)
hard_defs,hard_class = [],[]
while True:
    event, values = window.read()
    
    if event in (psg.WINDOW_CLOSED, 'Exit'):
        break
    if event == 'Load Functions':
        file = values['-FILEBROWSE-']
        hard_defs,hard_class = get_imp_defs(file)
        if file.endswith('.py'):
            analyser = FunctionAnalyser(file)
            window['-LIST-'].update([func.name for func in analyser.get_funcs()])
        else:
             psg.popup("Please select a Python file.")
    if event == '-FOLDERBROWSE-':
        hard_defs,hard_class = get_imp_defs(file)
        folder = values['-FOLDERBROWSE-']  # open the folder dialog
        if folder:
            window['-SAVEFOLDER-'].update(folder)
            output_filename = values['-OUTPUTFILE-']
            if output_filename == 'output':
                i = 1
                while os.path.isfile(os.path.join(folder, f'{output_filename}_{i}.py')):
                    i += 1
                output_filename = f'{output_filename}_{i}'
            window['-OUTPUTFILE-'].update(output_filename)

    if event == 'Load Functions':
        file = values['-FILEBROWSE-']  # get the selected file path
        if file.endswith('.py'):
            funcs = get_funcs(file)
            window['-LIST-'].update([func.name for func in funcs])
        else:
            psg.popup("Please select a Python file.")

    if event == '-LIST-':
        selected_functions = values['-LIST-']
        all_imports = set()
        all_functions = set()
        all_classes = set()
        for func in selected_functions:
            imports, functions, classes = get_deps_of_func(func, file)
            all_imports.update(imports)
            functions = set(f for f in functions if f in selected_functions)
            all_functions.update(functions)
            all_classes.update(classes)
        all_deps = list(all_imports) + list(all_functions) + list(all_classes)
        # Add selected functions to all_deps if they are not already in there
        for func in selected_functions:
            if func not in all_deps:
                all_deps.append(func)

        func_code = get_func_code(func, file)
        for hard_def in hard_defs:
            if hard_def+'(' in func_code and hard_def not in all_deps:
                all_deps.append(hard_def)
        for hard_clas in hard_class:
            if hard_clas+'(' in func_code and hard_clas not in all_deps:
                all_deps.append(hard_clas)
        window['-MULTI-'].update("\n".join(sorted(all_deps)))
    if event == 'Make Functions':
        folder = values['-SAVEFOLDER-']
        output_filename = values['-OUTPUTFILE-']
        output_file = os.path.join(folder, f'{output_filename}.py')

        # get names from -MULTI-
        names = window['-MULTI-'].get().split("\n")

        # get import lines from the original file
        import_lines = get_import_lines(file)

        with open(output_file, 'w') as f:
            # Write the import lines to the output file
            f.writelines(import_lines)
            f.write("\n")

            for name in names:
                # get function code associated with the name
                func_code = get_func_code(name, file)
                if func_code:
                    # write the function code to the output file
                    f.write(func_code)
                    f.write("\n\n")

        psg.popup(f"Functions saved to {output_file}.")
window.close()
