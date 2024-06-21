import ast


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.classes[self.current_class] = {'docstring': ast.get_docstring(node), 'methods': []}
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'parameters': [arg.arg for arg in node.args.args]
        }
        if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
            self.classes[self.current_class]['methods'].append(func_info)
        else:
            if 'functions' not in self.classes:
                self.classes['functions'] = []
            self.classes['functions'].append(func_info)
        self.generic_visit(node)


def add_parents(node):
    for child in ast.iter_child_nodes(node):
        child.parent = node
        add_parents(child)


def analyze_code(file_path):
    with open(file_path, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read(), filename=file_path)
        add_parents(tree)

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    return analyzer.classes


def create_markdown(file_path, classes):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Documentation\n\n")

        for cls_name, cls_info in classes.items():
            if cls_name != 'functions':
                f.write(f"## Class: `{cls_name}`\n")
                if cls_info['docstring']:
                    f.write(f"**Docstring:**\n```\n{cls_info['docstring']}\n```\n")
                if cls_info['methods']:
                    f.write("\n### Methods\n")
                    for method in cls_info['methods']:
                        params = ", ".join(method['parameters'])
                        f.write(f"- `{method['name']}({params})`\n")
                        if method['docstring']:
                            f.write(f"  **Docstring:**\n  ```\n  {method['docstring']}\n  ```\n")

        if 'functions' in classes:
            f.write("\n## Functions\n")
            for func in classes['functions']:
                params = ", ".join(func['parameters'])
                f.write(f"- `{func['name']}({params})`\n")
                if func['docstring']:
                    f.write(f"  **Docstring:**\n  ```\n  {func['docstring']}\n  ```\n")


def create_md(python_file, output_file="README2.md"):
    classes = analyze_code(python_file)
    create_markdown(output_file, classes)
    print(f"Documentation has been written to {output_file}")


create_md(r'C:\Users\cemem\PycharmProjects\CemirUtils\cemirutils\utils.py')
