"""Integer arithmetic evaluator (reference solution for task_014).

Recursive-descent parser with standard precedence, parentheses, and unary +/-.
Division truncates toward zero via int(a / b).
"""


def calc(expr):
    s = "".join(expr.split())
    i = 0

    def parse_expr():
        nonlocal i
        val = parse_term()
        while i < len(s) and s[i] in "+-":
            op = s[i]
            i += 1
            rhs = parse_term()
            val = val + rhs if op == "+" else val - rhs
        return val

    def parse_term():
        nonlocal i
        val = parse_factor()
        while i < len(s) and s[i] in "*/":
            op = s[i]
            i += 1
            rhs = parse_factor()
            val = val * rhs if op == "*" else int(val / rhs)
        return val

    def parse_factor():
        nonlocal i
        if s[i] == "+":
            i += 1
            return parse_factor()
        if s[i] == "-":
            i += 1
            return -parse_factor()
        if s[i] == "(":
            i += 1
            val = parse_expr()
            i += 1  # consume ')'
            return val
        start = i
        while i < len(s) and s[i].isdigit():
            i += 1
        return int(s[start:i])

    return parse_expr()
