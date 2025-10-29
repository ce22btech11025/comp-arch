from clang.cindex import CursorKind
from typing import List, Dict
import os

class CodeAnalyzer:
    """
    Analyzes the AST of a C program to identify arithmetic operations,
    variable declarations, and loops.
    """

    def __init__(self, root_cursor):
        self.root = root_cursor
        self.variables = []       # List of {name, type}
        self.operations = []      # List of {op, location, type}
        self.loops = []           # List of loop metadata

    def analyze(self):
        self._walk(self.root)
        return {
            "variables": self.variables,
            "operations": self.operations,
            "loops": self.loops
        }

    def _walk(self, node):
        # Variable declarations
        if node.kind == CursorKind.VAR_DECL:
            vartype = node.type.spelling
            self.variables.append({
                "name": node.spelling,
                "type": vartype,
                "location": self._get_loc(node)
            })

        # Loops
        elif node.kind in (CursorKind.FOR_STMT, CursorKind.WHILE_STMT):
            self.loops.append({
                "kind": node.kind.name,
                "location": self._get_loc(node)
            })

        # Arithmetic operations
        elif node.kind in (
            CursorKind.BINARY_OPERATOR,
            CursorKind.UNARY_OPERATOR
        ):
            op = self._extract_operator(node)
            if op:
                self.operations.append({
                    "operator": op,
                    "location": self._get_loc(node)
                })

        # Recursively visit children
        for child in node.get_children():
            self._walk(child)

    def _extract_operator(self, node):
        """
        Extracts operator symbol from source range text if possible.
        """
        try:
            tokens = list(node.get_tokens())
            for tok in tokens:
                if tok.spelling in ['+', '-', '*', '/', '%']:
                    return tok.spelling
        except Exception:
            pass
        return None

    def _get_loc(self, node):
        """
        Returns (file, line) for easier debugging.
        """
        loc = node.location
        return f"{os.path.basename(loc.file.name)}:{loc.line}" if loc.file else "unknown"
