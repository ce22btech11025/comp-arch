from clang import cindex
from clang.cindex import Config
import os

# === Fix for libclang.dll missing on Windows ===
# Try default LLVM path or custom environment variable
possible_paths = [
    r"C:\Program Files\LLVM\bin\libclang.dll",
    r"C:\Program Files (x86)\LLVM\bin\libclang.dll"
]

found_path = None
for path in possible_paths:
    if os.path.exists(path):
        found_path = path
        break

if found_path:
    Config.set_library_file(found_path)
else:
    print("⚠️ libclang.dll not found. Please install LLVM and update the path in parser.py.")
# ==============================================

class CParser:
    """
    Wrapper around libclang to parse and traverse C source code.
    """

    def __init__(self, clang_lib_path: str = None):
        if clang_lib_path:
            cindex.Config.set_library_file(clang_lib_path)
        self.index = cindex.Index.create()

    def parse(self, filename: str):
        """
        Parse a C source file and return the AST root.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Source file not found: {filename}")
        translation_unit = self.index.parse(filename, args=['-std=c11'])
        return translation_unit.cursor

    def dump_ast(self, cursor=None, depth=0):
        """
        Recursively print AST nodes (useful for debugging).
        """
        if cursor is None:
            raise ValueError("Cursor must be provided from parse().cursor")

        indent = '  ' * depth
        print(f"{indent}{cursor.kind} ({cursor.spelling})")

        for child in cursor.get_children():
            self.dump_ast(child, depth + 1)
