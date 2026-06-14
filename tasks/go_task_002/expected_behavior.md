# Expected behavior - go_task_002

Add `Capitalize` to `textkit.go`:

```go
// Capitalize returns s with its first character uppercased.
func Capitalize(s string) string {
	if s == "" {
		return ""
	}
	return strings.ToUpper(s[:1]) + s[1:]
}
```

Key discriminators:
- Only the first character changes; the rest is preserved (`hELLO` -> `HELLO`).
- Empty input returns empty.
- Non-letter first character is unchanged (`123` -> `123`).
