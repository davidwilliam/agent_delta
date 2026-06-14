// Hidden tests for go_task_002. Injected into agentdelta_eval/hidden at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestCapitalizePreservesRest(t *testing.T) {
	if got := textkit.Capitalize("hELLO"); got != "HELLO" {
		t.Fatalf("Capitalize(\"hELLO\") = %q, want %q", got, "HELLO")
	}
}

func TestCapitalizeAlreadyUpper(t *testing.T) {
	if got := textkit.Capitalize("Hello"); got != "Hello" {
		t.Fatalf("Capitalize(\"Hello\") = %q, want %q", got, "Hello")
	}
}

func TestCapitalizeDigit(t *testing.T) {
	if got := textkit.Capitalize("123"); got != "123" {
		t.Fatalf("Capitalize(\"123\") = %q, want %q", got, "123")
	}
}

func TestCapitalizeWord(t *testing.T) {
	if got := textkit.Capitalize("go is fun"); got != "Go is fun" {
		t.Fatalf("Capitalize(\"go is fun\") = %q, want %q", got, "Go is fun")
	}
}
