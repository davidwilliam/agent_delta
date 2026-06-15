You are localizing and fixing a multi-file bug in a small Go string library.
Follow this workflow:

1. Reproduce the symptom: `Tidy("a  b")` returns `"ab"` (words run together)
   instead of `"a b"`. The expected contract is trim plus collapse internal
   whitespace runs to a single space.
2. Trace the call. `Tidy` calls `strings.TrimSpace` and then delegates to the
   unexported helper `collapseSpaces`. Read both and decide which one violates
   the contract. `Tidy` is a thin wrapper, so inspect `collapseSpaces` closely.
3. Identify the root cause: `collapseSpaces` removes all spaces
   (`strings.ReplaceAll(s, " ", "")`) instead of collapsing runs to one space.
   This is why the symptom appears in `Tidy` even though `Tidy` is correct.
4. Fix `collapseSpaces` so it collapses runs of any whitespace to a single space
   and trims the ends. `strings.Join(strings.Fields(s), " ")` does this in one
   line. Leave `Tidy` exactly as it is.
5. Do not modify `go.mod` or `go.sum`, and do not weaken or delete the tests.
6. Run `go test ./...` to confirm the baseline still passes, then review the diff
   against the requirements and explain why fixing `Tidy` instead of the helper
   would be wrong.
