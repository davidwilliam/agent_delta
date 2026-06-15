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

Requirements:
1. `Tidy` trims leading and trailing whitespace and collapses internal runs of
   whitespace to a single space.
2. `Tidy("a  b")` is `"a b"` and `Tidy("  hello   world  ")` is `"hello world"`.
3. Runs of any whitespace (spaces, tabs, newlines) collapse to a single space.
4. A single word is unchanged and an empty string returns `""`.
5. The fix is in the `collapseSpaces` helper, not in `Tidy`; do not paper over the
   symptom by rewriting `Tidy` to re-insert spaces.
6. Do not change the signature or doc contract of `Tidy`.
7. Do not change any existing exported function (`Reverse`, `WordCount`,
   `Truncate`) or its behaviour.
8. Do not modify `go.mod` or `go.sum`.
9. Do not weaken or delete the tests.
10. Keep the patch minimal.

When finished, run `go test ./...` and summarize what you changed and why the
root cause was in the helper.
