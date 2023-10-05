import ast
import importlib.util
import os
from abstract_utilities.read_write_utils import read_from_file
from abstract_utilities.string_clean import eatAll,eatInner,eatOuter
import builtins


def make_list(obj):
    if not isinstance(obj,list):
        obj=[obj]
    return obj
def remove_items_from_list(list_obj,items):
    items=make_list(items)
    for item in items:
        while item in list_obj:
            list_obj.remove(item)
    return list_obj
def split_it(obj,delim):
    if delim in obj:
        list_obj = obj.split(delim)
        while '' in list_obj:
            list_obj=remove_items_from_list(list_obj,[''])
       
        return list_obj
    return make_list(obj)

class FileManager:
    def __init__(self,file_path):
        self.file_path = file_path
        self.directory = os.path.dirname(file_path)
        self.source_code = self.read_file()
        self.clear_source_code = self.clear_bad_lines()
        self.lines = self.source_code.split('\n')
        self.tree = ast.parse(self.source_code)
    def read_file(self):
        with open(self.file_path, "r") as source:
            text = source.read()
        return text
    def get_source_code(self,source_code=None):
        if source_code == None:
            self.source_code =  self.source_code or self.get_test_source_code()
        else:
            self.source_code = source_cope
    def get_test_source_code(self):
        return """import os\nfrom sys import exit\nclass MyClass:def method1(self):pass\ndef standalone_function():pass"""
    def clear_bad_lines(self):
        new_doc = ''
        count=0
        nclosed_symbols = {'(': 0, '{': 0, '[': 0}
        for i,char in enumerate(self.source_code):
            if char in ["[","(","{","}","]",")"]:
                if char in ["[","(","{"]:
                    nclosed_symbols[char]+=1
                elif char in ["}","]",")"]:
                    nclosed_symbols[{"}":"{","]":"[",")":"("}[char]]-=1
                count=0
                for each in ["[","(","{"]:
                    count+=nclosed_symbols[each]
                new_doc+=char
            elif char in ['\n','\t'] and count !=0:
                pass
            elif char == ' ' and new_doc[-1] == ' ':
                pass
            elif char == ' ' and new_doc[-1] in ["[","(","{"]:
                pass
            elif char == ',' and self.source_code[i+1] in ["}","]",")"]:
                pass
            elif char == ' ' and self.source_code[i+1] in ["}","]",")"]:
                pass
            elif char == ' ' and new_doc[-1] == ',':
                pass
            else:
               new_doc+=char
        return new_doc
    
file_mgr = FileManager(file_path = "/home/joben_joe/Documents/modules/abstract_py/src/abstract_py/test_scripts/limit_test.py")
class InitialAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_to_class_map = {}
        self.current_class = None
        self.import_analysis=self.analyze_imports()
    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            self.function_to_class_map[node.name] = self.current_class
        self.generic_visit(node)

    def analyze_imports(code: str):
        """
        Analyze imports in the provided Python code using AST.
        
        Args:
            code: The Python code to analyze.
            
        Returns:
            A list of dictionaries containing import information.
        """
        # Function to get module location
        def get_module_location(module_name):
            spec = importlib.util.find_spec(module_name)
            return spec.origin if spec else None

        # Extract imports from the AST
        imports = []
        for node in ast.walk(file_mgr.tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append({
                        'type': 'import',
                        'line': 'import ' + n.name,
                        'source': [n.name.split('.')[0]],
                        'alias': [n.asname] if n.asname else [],
                        'location': get_module_location(n.name.split('.')[0])
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                for n in node.names:
                    imports.append({
                        'type': 'from',
                        'line': f'from {module} import {n.name}',
                        'source': [module.split('.')[0]],
                        'object': [n.name],
                        'alias': [n.asname] if n.asname else [],
                        'location': get_module_location(module.split('.')[0])
                    })
        return imports
class FunctionAnalyser:
    def __init__(self):
        self.source_code= file_mgr.source_code
        self.tree = file_mgr.tree
        self.lines= file_mgr.lines
        self.class_methods= self.get_classes()
        self.class_names = self.get_class_names()
        self.function_methods = self.get_funcs()
        self.function_names = self.get_func_names()
        self.imports = self.get_imports()
        self.import_names = self.get_import_names()
        self.import_lines = self.get_import_lines()
        self.import_ls,self.all_imps = self.extract_import_info()
    def get_funcs(self):
        return [func for func in ast.walk(self.tree) if isinstance(func, ast.FunctionDef)]
    def get_func_names(self):
        return [func.name for func in self.get_funcs()]
    def get_classes(self):
        return [cls for cls in ast.walk(self.tree) if isinstance(cls, ast.ClassDef)]
    def get_class_names(self):
        return [cls.name for cls in self.get_classes()]
    def get_imports(self):
        return [imp for imp in ast.walk(self.tree) if isinstance(imp, (ast.Import, ast.ImportFrom))]
    def get_import_names(self):
        return [imp.names[0].name for imp in ast.walk(self.tree) if isinstance(imp, (ast.Import, ast.ImportFrom))]
    def get_import_lines(self):
        lines = self.source_code.split('\n')
        return [line for line in lines if line.startswith(('import ', 'from '))]
    def extract_import_info(self):
        template_js = {"from":"source","import":{"import":"source","from":"object"},"as":"alias"}
        import_ls=[]
        all_imps=[]
        for line in file_mgr.lines:
            line_lst=line.split(' ')
            if line_lst[0] in ["from","import"]:
                
                import_js = {}
                import_js["type"]=line_lst[0]
                import_js["line"]=line
                for word in line_lst:
                    word=eatAll(word,['(',')'])
                    if word in template_js:
                        current_action = template_js[word]
                        if isinstance(current_action,dict):
                            current_action = current_action[import_js["type"]]
                        import_js[current_action]={}
                    else:

                        import_js[current_action]=split_it(word,',')
                import_js["location"]=[]
                for import_item in import_js["source"]:
                    import_items=split_it(import_item,'.')
                    try:
                        import_js["location"]=imp.find_module(import_items[0])[1]
                    except:
                        import_js["location"]=None
                import_ls.append(import_js)
        
        for each in import_ls:
            if "alias" in each:
                all_imps=all_imps+each["alias"]
            elif "object" in each:
                all_imps=all_imps+each["object"]
            else:
                all_imps=all_imps+each["source"]
        return import_ls,all_imps
    def get_instance(self,func_name):
            instance=None
            if func_name in self.class_names:
                instance = ast.ClassDef
              
            if func_name in self.function_names:
                instance = ast.FunctionDef
        
            if func_name in self.import_names:
                instance = (ast.Import, ast.ImportFrom)

            return instance
    def get_func_deps(self, func_name):
        func_def_node = self.get_func_node(func_name)
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
    def get_instance(self,func_name):
        instance=None
        if func_name in self.class_names:
            instance = ast.ClassDef
          
        if func_name in self.function_names:
            instance = ast.FunctionDef
    
        if func_name in self.import_names:
            instance = (ast.Import, ast.ImportFrom)

        return instance
    def get_func_node(self,func_name):
        try:
            if self.get_type(func_name) == "import":
                return None if self.get_instance(func_name) == None else next((node for node in ast.walk(self.tree) if isinstance(node, self.get_instance(func_name)) and node.names[0].names == func_name), None)

            return None if self.get_instance(func_name) == None else next((node for node in ast.walk(self.tree) if isinstance(node, self.get_instance(func_name)) and node.name == func_name), None)
        except:
            return None
    def get_func_code(self, func_name):
        func_node = self.get_func_node(func_name)
        if func_node is None:
            return ""
        start_line = func_node.lineno
        if hasattr(func_node, "end_lineno"):  # Check if the AST node has the end_lineno attribute (Python 3.8+)
            end_line = func_node.end_lineno
        else:  # If not, you might revert to your original logic or another approach.
            end_line = start_line + len(func_node.body)
        func_code = "\n".join(self.lines[start_line-1:end_line])
        return func_code

    def get_type(self,func_name):
        instance=None
        if func_name in self.class_names:
            return "class"
        if func_name in self.function_names:
            return "function"
        if func_name in self.imports:
            return "import"


class ScriptAnalyzer(ast.NodeVisitor):
    def __init__(self, function_to_class_map):
        self.functions = set()
        self.classes = set()
        self.imports = set()
        self.variables = set()
        self.others = set()
        self.function_to_class_map = function_to_class_map
        
    def analyze(self, tree):
        # Preprocess the tree to set parent attribute
        set_parents(tree)

        # Visit nodes for analysis
        self.visit(tree)

    def visit_ClassDef(self, node):
        self.classes.add(node.name)
        self.current_class = node.name
        self.generic_visit(node)  # continue to the inner nodes
        self.current_class = None


    def visit_FunctionDef(self, node):
        if node.name in self.function_to_class_map:
            self.classes.add(self.function_to_class_map[node.name])
        else:
            self.functions.add(node.name)
        self.generic_visit(node)

    def visit_Import(self, node):
        for n in node.names:
            self.imports.add(n.name)
        self.generic_visit(node)
    def add_known_imports(self,imports_js):
        known_import_methods = imports_js
        self.functions -= known_import_methods
    def visit_ImportFrom(self, node):
        module = node.module
        for n in node.names:
            self.imports.add(f"{module}.{n.name}")
        self.generic_visit(node)
    def visit_Name(self, node):
        self.variables.add(node.id)
        self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.functions.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):  # for method calls
            # Add the method's full name, e.g., "requests.get" or "response.json"
            if isinstance(node.func.value, ast.Name):
                self.functions.add(f"{node.func.value.id}.{node.func.attr}")
            else:
                self.functions.add(node.func.attr)
        self.generic_visit(node)




initial_analyzer = InitialAnalyzer()
def map_functions_to_classes(script):
    tree = ast.parse(script)
    
    initial_analyzer.visit(tree)
    return initial_analyzer.function_to_class_map
function_to_class_map=map_functions_to_classes(file_mgr.source_code)
analyzer = ScriptAnalyzer(function_to_class_map)
def analyze_script(script):
    tree = ast.parse(script)
    analyzer.visit(tree)
    return analyzer.classes, analyzer.functions, analyzer.imports
def set_parents(node, parent=None):
    for child in ast.iter_child_nodes(node):
        child.parent = parent
        set_parents(child, child)
def integrated_analysis(code):
    # Get all the imports from the code
    imports = initial_analyzer.import_analysis
    # Create a mapping for easier reference
    import_mapping = {}
    for entry in imports:
        if 'alias' in entry and entry['alias']:
            import_mapping[entry['alias'][0]] = entry
        else:
            for obj in entry.get('object', []):
                import_mapping[obj] = entry
            for src in entry['source']:
                import_mapping[src] = entry
    # Analyze the code using the previous function
    classes, functions, imports_used = analyze_script(code)

    # Refine the functions set to provide more detailed information
    refined_functions = set()
    for func in functions:
        if func in import_mapping:
            module_name = import_mapping[func]['source'][0]
            refined_functions.add(f"{module_name}.{func}")
        else:
            refined_functions.add(func)

    return classes, refined_functions, imports_used
def build_the_import(import_names):
    all_imports_ls,all_imports = FunctionAnalyser().extract_import_info()
    imports_needed=[]
    for obj in import_names:
        spl_imp = obj.split('.')
        if len(spl_imp)>1 and isinstance(spl_imp,list):
            obj=spl_imp[-1]
        for import_js in all_imports_ls:
            import_phrase = import_js["type"]+' '+(',').join(import_js["source"])
            if "alias" in import_js:
                 if obj in import_js["alias"]:
                    if "object" in import_js:
                        import_phrase=import_phrase+' '+(',').join(import_js["object"])
                    import_phrase=import_phrase+' as '+obj
                    if import_phrase not in imports_needed:
                        imports_needed.append(import_phrase)
            elif "object" in import_js:
                if obj in import_js["object"]:
                    import_phrase=import_phrase+' import '+obj
                    if import_phrase not in imports_needed:
                        imports_needed.append(import_phrase)
            else:
                if obj in import_js["source"]:
                    if import_phrase not in imports_needed:
                        imports_needed.append(import_phrase)
    return imports_needed


function_name = "fetch_price_from_coingecko"
# Given lists/sets and the function name
function_definition = FunctionAnalyser().get_func_code(function_name)
analyzer.classes_geko, analyzer.functions_geko, analyzer.imports_geko =integrated_analysis(function_definition)
analyzer.classes, analyzer.functions, analyzer.imports =integrated_analysis(file_mgr.source_code)
function_attributions = analyzer.functions  # and so on
# 1. Extract imports
required_imports = []
for imp in analyzer.imports:
    # This logic assumes that you've got some mapping which provides the actual import lines
    required_imports+=build_the_import([imp]) # Using the function you've provided

input(required_imports)
# 2. Extract function definitions
# Assuming you have a mechanism similar to FunctionAnalyser().get_func_code
function_definitions = [FunctionAnalyser().get_func_code(func) for func in analyzer.functions_geko]

# 3. Extract class definitions
# Assuming you have a mechanism to extract full class definitions
class_definitions = [FunctionAnalyser().get_func_code(cls) for cls in analyzer.classes_geko]
#input(required_imports)
# 4. Combine to generate standalone script
standalone_script = '\n\n'.join(required_imports+ class_definitions + function_definitions + [function_definition])

#standalone_code = create_standalone_script(function_name, initial_analyzer.import_analysis, function_attributions)
print("standalone output:\n",standalone_script)

