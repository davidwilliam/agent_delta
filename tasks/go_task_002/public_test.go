// Public tests for go_task_002. Injected into agentdelta_eval/public at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestCapitalizeBasic(t *testing.T) {
	if got := textkit.Capitalize("hello"); got != "Hello" {
		t.Fatalf("Capitalize(\"hello\") = %q, want %q", got, "Hello")
	}
}

func TestCapitalizeEmpty(t *testing.T) {
	if got := textkit.Capitalize(""); got != "" {
		t.Fatalf("Capitalize(\"\") = %q, want empty", got)
	}
}

func TestCapitalizeSingle(t *testing.T) {
	if got := textkit.Capitalize("a"); got != "A" {
		t.Fatalf("Capitalize(\"a\") = %q, want %q", got, "A")
	}
}
