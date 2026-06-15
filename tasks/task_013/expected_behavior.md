# Expected behavior - task_013

A DP over `dp[i][j]` = does `text[:i]` match `pattern[:j]` (see reference). `*`
allows either consuming a text char (`dp[i-1][j]`) or matching empty
(`dp[i][j-1]`); `?` or a literal advances both. Seed `dp[0][j]` so leading runs of
`*` match the empty text.

Discriminators: `*` matching empty, multiple/consecutive `*`, full-string
matching (no partial), and `?` requiring exactly one character.
