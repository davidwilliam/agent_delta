package textkit

import "strings"

// collapseSpaces collapses runs of whitespace to a single space and trims ends.
// Reference solution for go_loc_01: the fix is here in the helper, not in Tidy.
// strings.Fields splits on runs of any whitespace and drops empties, so joining
// the fields with a single space both collapses internal runs and trims the ends.
func collapseSpaces(s string) string {
	return strings.Join(strings.Fields(s), " ")
}

// Tidy trims and collapses internal whitespace to single spaces.
// Unchanged from the fixture: the bug was never in Tidy.
func Tidy(s string) string {
	return collapseSpaces(strings.TrimSpace(s))
}
