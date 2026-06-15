"""Wildcard matching (reference solution for task_013)."""


def is_match(text, pattern):
    """Full-string wildcard match where ? is any char and * is any sequence."""
    m, n = len(text), len(pattern)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if pattern[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[j - 1] == "*":
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[j - 1] == "?" or pattern[j - 1] == text[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]
