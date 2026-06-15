// Hidden tests for go_contract_01. Injected into agentdelta_eval/hidden at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestCountWordsCollapsesWhitespaceRuns(t *testing.T) {
	if got := textkit.CountWords("a   b\tc"); got != 3 {
		t.Fatalf("CountWords(\"a   b\\tc\") = %d, want 3", got)
	}
}

func TestCountWordsTrimsLeadingTrailing(t *testing.T) {
	if got := textkit.CountWords("  hi  "); got != 1 {
		t.Fatalf("CountWords(\"  hi  \") = %d, want 1", got)
	}
}

func TestCountWordsSingleWord(t *testing.T) {
	if got := textkit.CountWords("word"); got != 1 {
		t.Fatalf("CountWords(\"word\") = %d, want 1", got)
	}
}

func TestCountWordsAllWhitespace(t *testing.T) {
	if got := textkit.CountWords("   \t  \n "); got != 0 {
		t.Fatalf("CountWords(all whitespace) = %d, want 0", got)
	}
}

func TestCountWordsUnicode(t *testing.T) {
	if got := textkit.CountWords("café au lait"); got != 3 {
		t.Fatalf("CountWords(\"café au lait\") = %d, want 3", got)
	}
}
