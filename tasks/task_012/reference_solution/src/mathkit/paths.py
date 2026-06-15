"""Path utilities (reference solution for task_012)."""


def simplify_path(path):
    """Canonicalize an absolute Unix-style path."""
    stack = []
    for segment in path.split("/"):
        if segment == "" or segment == ".":
            continue
        if segment == "..":
            if stack:
                stack.pop()
        else:
            stack.append(segment)
    return "/" + "/".join(stack)
