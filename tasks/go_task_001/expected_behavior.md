# Expected behavior - go_task_001

Fix the over-length branch in `Truncate`:

```go
func Truncate(s string, n int) string {
	if n < 0 {
		return ""
	}
	if n > len(s) {
		return s
	}
	return s[:n]
}
```

Key discriminators:
- `n > len(s)` returns the whole string (base returns one byte short).
- `n == len(s)` returns the whole string.
- `n < 0` returns empty.
- No panic for any input.
