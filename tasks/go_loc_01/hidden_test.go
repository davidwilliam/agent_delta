// Hidden tests for go_loc_01. Injected into agentdelta_eval/hidden at score time.
package eval

import (
	"testing"

	"textkit"
)

func TestTidyTabsAndNewlines(t *testing.T) {
	if got := textkit.Tidy("a\tb\nc"); got != "a b c" {
		t.Fatalf("Tidy(\"a\\tb\\nc\") = %q, want %q", got, "a b c")
	}
}

func TestTidyTrimsLeadingTrailing(t *testing.T) {
	if got := textkit.Tidy("   go   "); got != "go" {
		t.Fatalf("Tidy(\"   go   \") = %q, want %q", got, "go")
	}
}

func TestTidySingleWordUnchanged(t *testing.T) {
	if got := textkit.Tidy("word"); got != "word" {
		t.Fatalf("Tidy(\"word\") = %q, want %q", got, "word")
	}
}

func TestTidyEmpty(t *testing.T) {
	if got := textkit.Tidy(""); got != "" {
		t.Fatalf("Tidy(\"\") = %q, want empty", got)
	}
}

func TestTidyMultipleInternalRuns(t *testing.T) {
	if got := textkit.Tidy("one   two     three  four"); got != "one two three four" {
		t.Fatalf("Tidy multiple runs = %q, want %q", got, "one two three four")
	}
}
