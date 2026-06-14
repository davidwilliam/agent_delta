// Public tests for go_task_001. Injected into agentdelta_eval/public at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestTruncateOverLength(t *testing.T) {
	if got := textkit.Truncate("hello", 10); got != "hello" {
		t.Fatalf("Truncate(\"hello\", 10) = %q, want %q", got, "hello")
	}
}

func TestTruncateExactLength(t *testing.T) {
	if got := textkit.Truncate("hello", 5); got != "hello" {
		t.Fatalf("Truncate(\"hello\", 5) = %q, want %q", got, "hello")
	}
}

func TestTruncateWithinLength(t *testing.T) {
	if got := textkit.Truncate("hello", 2); got != "he" {
		t.Fatalf("Truncate(\"hello\", 2) = %q, want %q", got, "he")
	}
}
