// Hidden tests for go_task_001. Injected into agentdelta_eval/hidden at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestTruncateWayOver(t *testing.T) {
	if got := textkit.Truncate("hi", 100); got != "hi" {
		t.Fatalf("Truncate(\"hi\", 100) = %q, want %q", got, "hi")
	}
}

func TestTruncateSingleOver(t *testing.T) {
	if got := textkit.Truncate("x", 5); got != "x" {
		t.Fatalf("Truncate(\"x\", 5) = %q, want %q", got, "x")
	}
}

func TestTruncateNegative(t *testing.T) {
	if got := textkit.Truncate("hello", -3); got != "" {
		t.Fatalf("Truncate(\"hello\", -3) = %q, want empty", got)
	}
}

func TestTruncateZero(t *testing.T) {
	if got := textkit.Truncate("hello", 0); got != "" {
		t.Fatalf("Truncate(\"hello\", 0) = %q, want empty", got)
	}
}
