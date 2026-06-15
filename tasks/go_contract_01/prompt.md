# go_contract_01: Add a CountWords function to textkit

## minimal

You are working in the `textkit` Go module. Add an exported function
`CountWords(s string) int` to `textkit.go` that returns the number of
whitespace-separated words in `s`. Keep all existing exported functions and
their behaviour unchanged. When finished, run `go test ./...`.

## strong

You are working in the `textkit` Go module (package `textkit`, module path
`textkit`). Add an exported function to `textkit.go`:

```go
func CountWords(s string) int
```

It must:
1. Return the number of whitespace-separated words in `s`.
2. Collapse runs of whitespace (multiple spaces, tabs, newlines between words
   count as a single separator).
3. Ignore leading and trailing whitespace.
4. Return 0 for an empty string and for an all-whitespace string.
5. Count Unicode words correctly (for example, `CountWords("café au lait")`
   returns 3).

This is exactly `strings.Fields` word-counting semantics, so the simplest
correct implementation is `return len(strings.Fields(s))`.

Constraints:
- Do not change any existing exported function (`Reverse`, `WordCount`,
  `Truncate`) or its behaviour.
- Do not modify `go.mod` or `go.sum`.
- Keep the change small and consistent with the existing code style.

When finished, run `go test ./...` and summarize what you changed.

## workflow

You are adding a new function to a small Go string library. Follow this
workflow:

1. Read `textkit.go` to learn the package name, imports, and the style of the
   existing functions (`Reverse`, `WordCount`, `Truncate`).
2. Add an exported function `CountWords(s string) int` to `textkit.go` that
   returns the number of whitespace-separated words in `s`. Match the existing
   doc-comment and formatting style.
3. The required semantics are those of `strings.Fields`:
   - runs of whitespace collapse to a single separator,
   - leading and trailing whitespace is ignored,
   - an empty or all-whitespace string returns 0,
   - Unicode words are counted correctly (`"café au lait"` is 3 words).
   The simplest correct body is `return len(strings.Fields(s))`. Avoid
   hand-rolled splitting that miscounts whitespace runs, empty input, or
   multibyte characters.
4. Do not change any existing exported function or its behaviour, and do not
   touch `go.mod` or `go.sum`.
5. Run `go test ./...` to confirm the baseline still passes, then summarize the
   change.

## Required API (the tests import these exact names)

- Package `textkit` exposing `func CountWords(s string) int` (returns the number of whitespace-separated words in `s`).
