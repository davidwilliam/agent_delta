package textkit

import "testing"

// Baseline tests. These cover only behavior that is correct at the fixture base
// and must keep passing (the regression surface). The Truncate over-length bug
// and the missing Capitalize are exercised by the injected task tests, not here.

func TestReverse(t *testing.T) {
	if got := Reverse("abc"); got != "cba" {
		t.Fatalf("Reverse: got %q, want %q", got, "cba")
	}
}

func TestWordCount(t *testing.T) {
	if got := WordCount("a b  c"); got != 3 {
		t.Fatalf("WordCount: got %d, want 3", got)
	}
}

func TestTruncateWithinLength(t *testing.T) {
	if got := Truncate("hello", 3); got != "hel" {
		t.Fatalf("Truncate: got %q, want %q", got, "hel")
	}
}
