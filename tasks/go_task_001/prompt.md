You are working in the `textkit` Go module.

There is a bug in `Truncate` in `textkit.go`. When `n` is greater than the length
of the string, it returns one byte too few instead of returning the whole string.
For example, `Truncate("hello", 10)` currently returns `"hell"` instead of
`"hello"`.

Please fix `Truncate` so that:
1. When `n >= len(s)`, it returns the whole string `s`.
2. When `0 <= n <= len(s)`, it returns the first `n` bytes.
3. When `n < 0`, it returns an empty string.
4. It never panics.

Keep the change minimal and consistent with the existing code. When finished, run
`go test ./...` and summarize what you changed.
