def art_points(G):
    N = len(G)
    visited = [False] * N
    prenum = [-1] * N
    lowest = [-1] * N
    parent = [-1] * N
    bridges = []
    timer = 1

    def dfs(cur, prev, timer):
        prenum[cur] = lowest[cur] = timer
        timer += 1
        visited[cur] = True
        for to in G[cur]:
            if not visited[to]:
                parent[to] = cur
                timer = dfs(to, cur, timer)
                lowest[cur] = min(lowest[cur], lowest[to])
                if lowest[to] == prenum[to]:
                    bridges.append((min(cur, to), max(cur, to)))
            elif to != prev:
                lowest[cur] = min(lowest[cur], prenum[to])
        return timer

    for i in range(N):
        if not visited[i]:
            timer = dfs(i, -1, timer)

    aps = set()
    np = 0
    for i in range(1, N):
        p = parent[i]
        if p == 0:
            np += 1
        elif prenum[p] <= lowest[i]:
            aps.add(p)
    if np > 1:
        aps.add(0)
    return aps, bridges