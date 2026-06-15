package textkit

import "strings"

// collapseSpaces should collapse runs of whitespace to a single space and trim ends.
// BUG (fixture): it removes ALL spaces instead of collapsing them. AgentDelta
// go_loc_01 fixes it. The symptom shows up in Tidy (words run together); the root
// cause is here in collapseSpaces, not in Tidy.
func collapseSpaces(s string) string {
	return strings.ReplaceAll(s, " ", "")
}

// Tidy trims and collapses internal whitespace to single spaces.
func Tidy(s string) string {
	return collapseSpaces(strings.TrimSpace(s))
}
