You are working in the `textkit` Go module (package `textkit`, module path
`textkit`). Add an exported function to `textkit.go`:

```go
func CountWords(s string) int
```

It must return the number of whitespace-separated words in `s`, using
`strings.Fields` semantics. The simplest correct implementation is
`return len(strings.Fields(s))`.

Requirements:
1. A `CountWords` function exists in package `textkit`.
2. `CountWords` returns the number of whitespace-separated words using
   `strings.Fields` semantics.
3. Runs of whitespace between words collapse to a single separator.
4. Leading and trailing whitespace is ignored.
5. An empty string and an all-whitespace string both return 0.
6. Unicode words are counted correctly (`CountWords("café au lait")` is 3).
7. The existing exported functions (`Reverse`, `WordCount`, `Truncate`) are
   unchanged.
8. Do not modify `go.mod` or `go.sum`.
9. Do not weaken or delete the tests.
10. Keep the patch minimal and consistent with the existing code style.

When finished, run `go test ./...` and summarize what you changed.
