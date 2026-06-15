"""Minimal CSV row parser (reference solution for mk_minimal_01).

A small char-by-char state machine: top-level commas separate fields, commas
inside double quotes are literal, surrounding quotes are stripped, and a doubled
double-quote inside a quoted field is a single literal quote.
"""


def parse_row(line):
    """Split a single CSV line into its fields, honoring double-quoted fields."""
    fields = []
    field = []
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(ch)
        elif ch == '"':
            in_quotes = True
        elif ch == ",":
            fields.append("".join(field))
            field = []
        else:
            field.append(ch)
        i += 1
    fields.append("".join(field))
    return fields
