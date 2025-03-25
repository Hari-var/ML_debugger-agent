import ast
import sys

def pares_py_file(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
    tree= ast.parse(file_content)

    function_list = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    class_list = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    import_list = [value.name for node in ast.walk(tree) if isinstance(node, ast.Import) for value in node.names]
    from_import_list = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) if  node.module]

    return {
        "function_list": function_list,
        "class_list": class_list,
        "import_list": import_list,
        "from_import_list": from_import_list,
        "source_code":file_content
    }

if __name__ == "__main__":
    tree= (pares_py_file(r"C:\practice\file_structure_retriver.py"))
    print(tree['function_list'])
    print(tree['class_list'])
    print(tree['import_list'])
    print(tree['from_import_list'])
    print(tree['source_code'])