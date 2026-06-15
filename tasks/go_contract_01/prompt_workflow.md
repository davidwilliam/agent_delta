You are adding a new function to a small Go string library. Follow this
workflow:

1. Read `textkit.go` to learn the package name, imports, and the style of the
   existing functions (`Reverse`, `WordCount`, `Truncate`).
2. State the contract: `CountWords(s string) int` returns the number of
   whitespace-separated words in `s` with `strings.Fields` semantics, that is,
   runs of whitespace collapse to a single separator, leading and trailing
   whitespace is ignored, an empty or all-whitespace string returns 0, and
   Unicode words are counted correctly (`"café au lait"` is 3 words).
3. Make the smallest change: add the exported `CountWords` to `textkit.go`,
   matching the existing doc-comment and formatting style. The simplest correct
   body is `return len(strings.Fields(s))`. Avoid hand-rolled splitting that
   miscounts whitespace runs, empty input, or multibyte characters.
4. Do not change any existing exported function or its behaviour, and do not
   touch `go.mod` or `go.sum`.
5. Run `go test ./...`. If anything fails, debug once and re-run.
6. Review the diff against the requirements, then summarize the change.
