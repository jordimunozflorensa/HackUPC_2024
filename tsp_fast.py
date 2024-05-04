
dp = [[10000000000000] * 20 for _ in range(1 << 20)]

dp[1][0] = 1
for msk in range(2, 1 << n):

    for v in range(n):
        if not msk & (1 << v):
            continue
        for u in g[v]:
            if msk & (1 << u):
                dp[msk][v] += dp[msk - (1 << v)][u]

print(dp[(1 << n) - 1][n - 1])