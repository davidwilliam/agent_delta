// Public tests for go_contract_01. Injected into agentdelta_eval/public at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestCountWordsTwoWords(t *testing.T) {
	if got := textkit.CountWords("hello world"); got != 2 {
		t.Fatalf("CountWords(\"hello world\") = %d, want 2", got)
	}
}

func TestCountWordsEmpty(t *testing.T) {
	if got := textkit.CountWords(""); got != 0 {
		t.Fatalf("CountWords(\"\") = %d, want 0", got)
	}
}
