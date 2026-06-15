Fix `parse_row` in `mathkit.csvlite` so it handles double-quoted CSV fields: a comma
inside quotes is not a separator, and surrounding quotes are stripped. Do not import
the `csv` module.
