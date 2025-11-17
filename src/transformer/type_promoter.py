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
    # UPDATED: Added optional (static|const) to decl_line_re pattern prefix
    DECL_PREFIX_RE = r"^\s*(?:static\s+|const\s+)?\s*"
    
    def __init__(self, promote_to: str = "float"):
        self.promote_to = promote_to
        self.index_vars: Set[str] = set()
        self.array_vars: Set[str] = set()
        
        # Redefine decl_line_re here to use the new prefix
        self.decl_line_re = re.compile(self.DECL_PREFIX_RE + r'(' + self.INT_TYPES_RE + r')\b(.*);')


    def _find_identifiers(self, expr: str):
        """Return identifiers in an expression string."""
        return set(re.findall(r'\b([A-Za-z_]\w*)\b', expr))

    def analyze_code(self, code: str):
        """Scan the full source and populate self.index_vars and self.array_vars."""
        self.index_vars.clear()
        self.array_vars.clear()

        # 1) find for-loop counters: for (int i = 0; ... ) or for (i = 0; ... )
        for_loop_decl = re.findall(r'for\s*\(\s*(?:' + self.INT_TYPES_RE + r'\s+)?([A-Za-z_]\w*)\s*=', code)
        self.index_vars.update(for_loop_decl)

        # 2) find variables used inside square brackets, e.g., arr[i], matrix[l + i]
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
        common = {"i", "j", "k", "idx", "l", "r", "m", "n"}
        self.index_vars.update({v for v in common if v in code})

    def _split_decl_variables(self, decl_tail: str):
        """
        Given the tail of a declaration after the type (e.g., "a, *b, c[10];"),
        return list of (name, text_fragment) where name is var name and fragment is original snippet.
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
        
        for original_line in lines:
            # IMPORTANT: line will be used for modification, original_line for fallback
            line = original_line
            stripped = original_line.strip()

            # keep preprocessor and comments unchanged
            if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                out_lines.append(original_line)
                continue

            # 1. Handle malloc/calloc/realloc size/cast
            if 'malloc' in original_line or 'calloc' in original_line or 'realloc' in original_line:
                # Replace (int *) to (float *)
                line = re.sub(r'(\s*\(\s*)(' + self.INT_TYPES_RE + r')(\s*\*?\s*\)\s*(?:malloc|calloc|realloc))', 
                              r'\1' + self.promote_to + r'\3', original_line)
                # Replace sizeof(int) to sizeof(float)
                line = re.sub(r'(sizeof\s*\(\s*)(' + self.INT_TYPES_RE + r')(\s*\))', 
                              r'\1' + self.promote_to + r'\3', line)
            
            # 2. Handle top-level declarations (including 'static int arr[N];')
            m = self.decl_line_re.match(line)
            if m:
                prefix = line[:m.start(1)].strip() # Capture 'static' or leading spaces
                base_type = m.group(1)
                tail = m.group(2)
                
                # CRITICAL FIX: Add a check for NoneType to prevent crash
                if tail is None:
                    out_lines.append(original_line)
                    continue

                tail = tail.strip()

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

                    # If variable is one of known array names OR a promoted variable, use promote_to
                    if varname in self.array_vars:
                        new_parts.append(f"{self.promote_to} {part}")
                        continue

                    # Otherwise promote this variable's type
                    new_parts.append(f"{self.promote_to} {part}")
                
                # Reconstruct line: merge parts with same type
                grouped = {}
                for p in new_parts:
                    m2 = re.match(r'^\s*([A-Za-z_][\w]*)\s+(.*)', p)
                    if m2:
                        t = m2.group(1)
                        rest = m2.group(2)
                    else:
                        t = base_type
                        rest = p
                    grouped.setdefault(t, []).append(rest.strip())

                # Build final line with combined groups
                final_parts = []
                for t, rests in grouped.items():
                    # Prefix only applied to the first type group
                    current_prefix = prefix if not final_parts else ""
                    # Ensure prefix is only added if not empty
                    final_part = f"{current_prefix} {t} " + ", ".join(rests)
                    final_parts.append(final_part.strip())

                final_line = "; ".join(final_parts) + ";"
                out_lines.append(final_line)
                continue

            # 3. Handle function parameter lists
            if '(' in line and ')' in line and re.search(r'\)\s*{|\);', line) or re.search(r'\w+\s+\w+\s*\(.*\)', line):
                try:
                    head, rest = line.split('(', 1)
                    params, tail = rest.rsplit(')', 1)
                except ValueError:
                    out_lines.append(line)
                    continue

                # split params by comma
                params_list = [p.strip() for p in params.split(',') if p.strip()]
                new_params = []
                for p_orig in params_list:
                    p = p_orig # use p for modification
                    if p == "..." or p == "void":
                        new_params.append(p)
                        continue

                    ids = self._find_identifiers(p)
                    pname = None
                    for id_ in ids:
                        if id_ not in {"int", "long", "short", "float", "double", "const", "unsigned", self.promote_to}:
                            pname = id_
                            break

                    if pname and pname in self.index_vars:
                        new_params.append(p)
                    else:
                        p_new = re.sub(self.INT_DECL_RE, self.promote_to, p)
                        new_params.append(p_new)

                new_line = head + "(" + ", ".join(new_params) + ")" + tail
                out_lines.append(new_line)
                continue

            # 4. Handle declarations within FOR loops to protect index variables (e.g. `for (int i=0;...`)
            if re.match(r'^\s*for\s*\(', line):
                m_for = re.match(r'^\s*for\s*\(\s*(.*)\s*\)', line)
                if m_for:
                    header = m_for.group(1)
                    # Find the declaration part: 'int i = 0;'
                    decl_match = re.search(r'(' + self.INT_TYPES_RE + r')\s+([A-Za-z_]\w*)\s*=', header)
                    if decl_match:
                        varname = decl_match.group(2)
                        if varname not in self.index_vars:
                            # Only promote if it is NOT a known index
                            line = re.sub(self.INT_DECL_RE, self.promote_to, line)
                            
            # 5. Final Fallback: Append the line (potentially modified by malloc/for loop logic)
            out_lines.append(line)

        # join results, preserve final newline
        return "\n".join(out_lines) + ("\n" if code.endswith("\n") else "")