// Public tests for go_loc_01. Injected into agentdelta_eval/public at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestTidyCollapsesSingleRun(t *testing.T) {
	if got := textkit.Tidy("a  b"); got != "a b" {
		t.Fatalf("Tidy(\"a  b\") = %q, want %q", got, "a b")
	}
}

func TestTidyTrimsAndCollapses(t *testing.T) {
	if got := textkit.Tidy("  hello   world  "); got != "hello world" {
		t.Fatalf("Tidy(\"  hello   world  \") = %q, want %q", got, "hello world")
	}
}
