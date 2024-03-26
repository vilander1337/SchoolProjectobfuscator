import ast
import astor
import random
import string
import keyword
import base64
import os

def random_name(length=10):
    # generate random name
    return ''.join(random.choices(string.ascii_letters, k=length))

def obfuscate_code(code):
    # obfuscate assigns, names, functions and attributes
    tree = ast.parse(code)
    used_names = {}  # dictionary for something 
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not keyword.iskeyword(node.name) and not node.name in dir(__builtins__):
                if node.name not in used_names:
                    used_names[node.name] = random_name()
                node.name = used_names[node.name]
        elif isinstance(node, ast.Name):
            if not keyword.iskeyword(node.id) and not node.id in dir(__builtins__):
                if node.id in used_names:
                    node.id = used_names[node.id]
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                if not keyword.iskeyword(node.attr) and not node.attr in dir(__builtins__):
                    if node.attr in used_names:
                        node.attr = used_names[node.attr]
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if not keyword.iskeyword(target.id) and not target.id in dir(__builtins__):
                        if target.id in used_names:
                            target.id = used_names[target.id]

    # compile 
    obfuscated_tree = ast.fix_missing_locations(tree)
    obfuscated_code = astor.to_source(obfuscated_tree)

    # code this to base 64
    encoded_code = base64.b64encode(obfuscated_code.encode()).decode()

    obfuscated_script = f"import base64;exec(compile(base64.b64decode('''{encoded_code}'''),'','exec'))"

    return obfuscated_script

def obfuscate_file(input_file):
    # open file
    with open(input_file, 'r') as f:
        original_code = f.read()

    obfuscated_script = obfuscate_code(original_code)
    return obfuscated_script

def main():
    src_folder = 'src'
    output_folder = 'output'

    # check and create folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # scan files
    src_files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]

    if not src_files:
        print("No files to obfuscate!")
        return

    print("Available files to obfuscate: ")
    for i, file in enumerate(src_files):
        print(f"{i + 1}. {file}")

    choice = int(input("Enter the file number to obfuscation: "))

    if choice < 1 or choice > len(src_files):
        print("Incorrect file selection.")
        return

    chosen_file = src_files[choice - 1]
    input_file = os.path.join(src_folder, chosen_file)
    output_file = os.path.join(output_folder, f"{chosen_file}.obf.py")

    obfuscated_script = obfuscate_file(input_file)

    #write data to file
    with open(output_file, 'w') as f:
        f.write('# Obfuscated Code\n\n')
        f.write(obfuscated_script)

    print(f"The file was successfully obfuscated and saved to: {output_file}")

if __name__ == "__main__":
    main()
