You are working in the `textkit` Go module.

Please add a `Capitalize` function to `textkit.go`.

`Capitalize(s string) string` should:
1. Uppercase the first character of `s`.
2. Leave the rest of the string unchanged.
3. Return an empty string when `s` is empty.

For example, `Capitalize("hello")` returns `"Hello"` and `Capitalize("hELLO")`
returns `"HELLO"`.

Keep the change minimal and consistent with the existing code. When finished, run
`go test ./...` and summarize what you changed.
