import re
from typing import Set


class TypePromoter:
    """
    Two-pass type promoter:
      1) analyze_code(code) -> collect index_vars and array_vars
      2) promote_code(code) -> promote integer declarations except for index_vars,
         and promote array/pointer declarations consistently for array_vars.
    """

    INT_TYPES_RE = r"(?:unsigned\s+)?(?:short|int|long\s+long|long)"
    INT_DECL_RE = re.compile(rf"\b({INT_TYPES_RE})\b")

    def __init__(self, promote_to: str = "float"):
        self.promote_to = promote_to
        self.index_vars: Set[str] = set()
        self.array_vars: Set[str] = set()

    def _find_identifiers(self, expr: str):
        """Return identifiers in an expression string."""
        return set(re.findall(r'\b([A-Za-z_]\w*)\b', expr))

    def analyze_code(self, code: str):
        """Scan the full source and populate self.index_vars and self.array_vars."""
        self.index_vars.clear()
        self.array_vars.clear()

        # 1) find for-loop counters: for (int i = 0; ... ) or for (i = 0; ... ) (we prefer the declaration)
        for_loop_decl = re.findall(r'for\s*\(\s*(?:' + self.INT_TYPES_RE + r'\s+)?([A-Za-z_]\w*)\s*=', code)
        self.index_vars.update(for_loop_decl)

        # 2) find variables used inside square brackets, e.g., arr[i], matrix[l + i]
        # For every [ ... ], extract identifiers inside and mark them index_vars
        bracket_contents = re.findall(r'\[([^\]]+)\]', code)
        for content in bracket_contents:
            ids = self._find_identifiers(content)
            self.index_vars.update(ids)

        # 3) find array/pointer declarations like: int arr[...]; or int *arr;
        arr_decl_pattern = re.compile(r'\b(' + self.INT_TYPES_RE + r')\s+([A-Za-z_]\w*)\s*(\[[^\]]*\]|\s*\*+)')
        for m in arr_decl_pattern.finditer(code):
            varname = m.group(2)
            self.array_vars.add(varname)
            # also if the array's size expression contains ids, mark them index_vars
            size_expr = re.search(rf'\b{re.escape(varname)}\s*\[\s*([^\]]*)\]', code)
            if size_expr:
                inner = size_expr.group(1)
                ids = self._find_identifiers(inner)
                self.index_vars.update(ids)

        # 4) variables passed as array parameters: func(float arr[]), detect patterns int arr[] in params
        param_array_pattern = re.compile(r'\b(' + self.INT_TYPES_RE + r')\s+([A-Za-z_]\w*)\s*\[\s*\]')
        for m in param_array_pattern.finditer(code):
            self.array_vars.add(m.group(2))

        # 5) variables used with ++ or -- are often counters — keep them int
        incdec = re.findall(r'(\b[A-Za-z_]\w*)\s*(?:\+\+|--)', code)
        self.index_vars.update(incdec)

        # 6) catch common index variable names heuristically (i, j, k, idx) if they appear anywhere
        # (conservative: only add if they occur in for/[] contexts already)
        common = {"i", "j", "k", "idx", "l", "r", "m", "n"}
        self.index_vars.update({v for v in common if v in code})

    def _split_decl_variables(self, decl_tail: str):
        """
        Given the tail of a declaration after the type (e.g., "a, *b, c[10];"),
        return list of (name, text_fragment) where name is var name and fragment is original snippet.
        Used to decide per-variable promotion.
        """
        # Remove trailing semicolon
        tail = decl_tail.strip()
        if tail.endswith(';'):
            tail = tail[:-1]

        # Split by commas, but keep pointer/array notation
        parts = [p.strip() for p in tail.split(',')]
        result = []
        for p in parts:
            # get variable name
            # patterns: "*ptr", "arr[10]", "x", "x = 5"
            m = re.match(r'(\*?\s*([A-Za-z_]\w*))', p)
            if m:
                name = m.group(2)
            else:
                # fallback: first id in part
                ids = re.findall(r'([A-Za-z_]\w*)', p)
                name = ids[0] if ids else None
            result.append((name, p))
        return result

    def promote_code(self, code: str) -> str:
        """
        Promote types in declarations while preserving index variables.
        Operates on whole-file text.
        """
        # Analyze file to populate index_vars & array_vars
        self.analyze_code(code)

        out_lines = []
        lines = code.splitlines()

        # Patterns to detect top-level declarations (simple heuristics)
        # e.g., "int a, b = 0, *p;" or "long long count = 0;"
        decl_line_re = re.compile(r'^\s*(' + self.INT_TYPES_RE + r')\b(.*);')  # group1=type, group2=rest

        for line in lines:
            stripped = line.strip()

            # keep preprocessor and comments unchanged
            if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                out_lines.append(line)
                continue

            m = decl_line_re.match(line)
            if m:
                base_type = m.group(1)
                tail = m.group(2).strip()

                # split declared variables
                vars_parts = self._split_decl_variables(tail)
                new_parts = []
                for varname, part in vars_parts:
                    if not varname:
                        new_parts.append(part)
                        continue

                    # If variable is a known index var, keep original integer type
                    if varname in self.index_vars:
                        new_parts.append(f"{base_type} {part}")
                        continue

                    # If variable is one of known array names we must promote it to promote_to
                    if varname in self.array_vars:
                        # Replace base type with promote_to for this var
                        new_parts.append(f"{self.promote_to} {part}")
                        continue

                    # Otherwise promote this variable's type
                    new_parts.append(f"{self.promote_to} {part}")

                # Reconstruct line: join the parts by comma; remove duplicated types
                # We need to merge parts with same type to a valid C declaration.
                # Build groups by type string prefix
                grouped = {}
                for p in new_parts:
                    # p looks like "<type> <rest>"
                    m2 = re.match(r'^\s*([A-Za-z_][\w]*)\s+(.*)', p)
                    if m2:
                        t = m2.group(1)
                        rest = m2.group(2)
                    else:
                        # fallback
                        t = base_type
                        rest = p
                    grouped.setdefault(t, []).append(rest.strip())

                # Build final line with combined groups
                final_parts = []
                for t, rests in grouped.items():
                    final_parts.append(f"{t} " + ", ".join(rests))

                final_line = "; ".join(final_parts) + ";"
                out_lines.append(final_line)
                continue

            # Handle function parameter lists: change "int arr[]" or "int *arr" or "int x" in params
            # We'll replace int types in params except for names in index_vars.
            # Simple heuristic: detect "(" ... ")" on single line function defs/declarations
            if '(' in line and ')' in line and re.search(r'\)\s*{|\);', line) or re.search(r'\w+\s+\w+\s*\(.*\)', line):
                # get params substring
                try:
                    head, rest = line.split('(', 1)
                    params, tail = rest.rsplit(')', 1)
                except ValueError:
                    out_lines.append(line)
                    continue

                # split params by comma
                params_list = [p.strip() for p in params.split(',') if p.strip()]
                new_params = []
                for p in params_list:
                    # leave varargs or empty alone
                    if p == "..." or p == "void":
                        new_params.append(p)
                        continue

                    # find var name in param
                    ids = self._find_identifiers(p)
                    pname = None
                    for id_ in ids:
                        if id_ not in {"int", "long", "short", "float", "double", "const", "unsigned"}:
                            pname = id_
                            break

                    if pname and pname in self.index_vars:
                        # keep original param text
                        new_params.append(p)
                    else:
                        # replace int-like type tokens with promote_to
                        p_new = re.sub(self.INT_DECL_RE, self.promote_to, p)
                        new_params.append(p_new)

                new_line = head + "(" + ", ".join(new_params) + ")" + tail
                out_lines.append(new_line)
                continue

            # No special handling — keep line (but still replace int types in other contexts cautiously)
            # Replace standalone int types only where not inside bracket/for header — a conservative pass:
            # If line contains '[' or 'for(' or 'while(' we skip naive replacement to avoid breaking indices
            if '[' in line or 'for(' in line or 'for (' in line or 'while(' in line:
                out_lines.append(line)
                continue

            # Otherwise, replace int types with promote_to (conservative)
            replaced = re.sub(self.INT_DECL_RE, self.promote_to, line)
            out_lines.append(replaced)

        # join results, preserve final newline
        return "\n".join(out_lines) + ("\n" if code.endswith("\n") else "")
