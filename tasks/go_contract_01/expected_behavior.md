# Expected behavior - go_contract_01

Add `CountWords` to `textkit.go`:

```go
// CountWords returns the number of whitespace-separated words in s.
func CountWords(s string) int {
	return len(strings.Fields(s))
}
```

Key discriminators (the known LLM failure mode is
miscounts_whitespace_runs_or_unicode_or_empty):
- Runs of whitespace collapse to one separator (`"a   b\tc"` is 3 words).
- Leading and trailing whitespace is ignored (`"  hi  "` is 1 word).
- A single word is 1, an empty string is 0, an all-whitespace string is 0.
- Unicode words are counted correctly (`"café au lait"` is 3 words).

At base, `textkit.CountWords` does not exist, so the injected eval package fails
to compile (`undefined: textkit.CountWords`), which the runner reads as a
failing or error run. After the reference adds the function, the baseline,
public, and hidden tests all pass.

Existing exported functions (`Reverse`, `WordCount`, `Truncate`) and their
behaviour are unchanged; only `CountWords` is added.
