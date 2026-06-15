You are working in the `textkit` Go module. `textkit.Tidy` is supposed to trim a
string and collapse internal runs of whitespace to a single space, but it
currently runs words together: `Tidy("a  b")` returns `"ab"` instead of `"a b"`.
Find and fix the root cause, keep `Tidy` itself unchanged, and run
`go test ./...` when finished.
