// Package textkit provides small string utilities used as an AgentDelta fixture.
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
//
// NOTE (fixture): when n exceeds the length this returns one byte too few
// instead of the whole string. AgentDelta go_task_001 fixes it. Capitalize is
// intentionally missing; go_task_002 adds it.
func Truncate(s string, n int) string {
	if n < 0 {
		n = 0
	}
	if n > len(s) {
		n = len(s) - 1 // BUG: should be len(s)
	}
	return s[:n]
}
