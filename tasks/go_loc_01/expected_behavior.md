# Expected behavior - go_loc_01

The bug is multi-file: the symptom is wrong `Tidy` output and the root cause is
in the unexported helper `collapseSpaces` (both live in `normalize.go`).

At base, `collapseSpaces` strips every space instead of collapsing runs:

```go
func collapseSpaces(s string) string {
	return strings.ReplaceAll(s, " ", "")
}
```

so `Tidy("a  b")` returns `"ab"` and `Tidy("  hello   world  ")` returns
`"helloworld"`. The injected public tests fail at base for exactly this reason.

The correct fix is in the helper, not in `Tidy`:

```go
func collapseSpaces(s string) string {
	return strings.Join(strings.Fields(s), " ")
}
```

`Tidy` is left unchanged:

```go
func Tidy(s string) string {
	return collapseSpaces(strings.TrimSpace(s))
}
```

Key discriminators (the known LLM failure mode is
`patches_tidy_symptom_instead_of_collapse_helper`):
- The fix belongs in `collapseSpaces`. Rewriting `Tidy` to re-insert spaces
  while leaving the broken helper in place patches the symptom, not the root
  cause, and is out of scope.
- Runs of any whitespace (spaces, tabs, newlines) collapse to a single space
  (`"a\tb\nc"` becomes `"a b c"`).
- Leading and trailing whitespace is trimmed (`"   go   "` becomes `"go"`).
- A single word is unchanged (`"word"` stays `"word"`).
- An empty string returns `""`.
- Multiple internal runs each collapse (`"one   two     three  four"` becomes
  `"one two three four"`).

After the reference fixes `collapseSpaces`, the baseline, public, and hidden
tests all pass. All existing exported functions and `Tidy` are unchanged.
