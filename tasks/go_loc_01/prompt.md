# go_loc_01: Fix word-run-together output from the whitespace helper

## minimal

You are working in the `textkit` Go module. `textkit.Tidy` is supposed to trim a
string and collapse internal runs of whitespace to a single space, but it
currently runs words together: `Tidy("a  b")` returns `"ab"` instead of `"a b"`.
Find and fix the root cause, keep `Tidy` itself unchanged, and run
`go test ./...` when finished.

## strong

You are working in the `textkit` Go module (package `textkit`, module path
`textkit`). The exported function `Tidy(s string) string` should trim leading
and trailing whitespace and collapse every internal run of whitespace to a
single space, for example `Tidy("  hello   world  ")` should return
`"hello world"`. Right now it returns `"helloworld"`: the words run together.

`Tidy` delegates the whitespace work to an unexported helper, `collapseSpaces`.
Read the package, locate where the spaces are being destroyed, and fix the root
cause. The bug is in the helper, not in `Tidy`. The corrected `collapseSpaces`
should collapse runs of any whitespace (spaces, tabs, newlines) to a single
space and trim the ends; `strings.Fields` plus `strings.Join` gives exactly that
behaviour.

Constraints:
- Fix the helper (`collapseSpaces`), not `Tidy`. Do not paper over the symptom
  by rewriting `Tidy` to re-insert spaces.
- Do not change the signature or doc contract of `Tidy`.
- Do not modify `go.mod` or `go.sum`, and do not weaken or delete the tests.

When finished, run `go test ./...` and summarize what you changed and why the
root cause was in the helper.

## workflow

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
6. Run `go test ./...` to confirm the baseline still passes, then summarize the
   change and explain why fixing `Tidy` instead of the helper would be wrong.
