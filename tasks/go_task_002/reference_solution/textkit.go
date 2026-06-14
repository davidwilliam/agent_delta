// Package textkit provides small string utilities used as an AgentDelta fixture.
// Reference solution for go_task_002 (add Capitalize).
package textkit

import "strings"

// Reverse returns s with its bytes reversed.
func Reverse(s string) string {
	b := []byte(s)
	for i, j := 0, len(b)-1; i < j; i, j = i+1, j-1 {
		b[i], b[j] = b[j], b[i]
	}
	return string(b)
}

// WordCount returns the number of whitespace-separated words in s.
func WordCount(s string) int {
	return len(strings.Fields(s))
}

// Truncate returns the first n bytes of s, or all of s when n exceeds the length.
func Truncate(s string, n int) string {
	if n < 0 {
		n = 0
	}
	if n > len(s) {
		n = len(s) - 1 // BUG: untouched by this task (go_task_001 fixes it)
	}
	return s[:n]
}

// Capitalize returns s with its first character uppercased.
func Capitalize(s string) string {
	if s == "" {
		return ""
	}
	return strings.ToUpper(s[:1]) + s[1:]
}
