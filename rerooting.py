# 全方位木DP: ei1333
# verified AOJ trafc tree or GRL_5A
import sys
sys.setrecursionlimit(10 ** 7)
INF = 1 << 60
def resolve():
    def dfs1(topo, par):
        for idx in reversed(topo):
            for to in G[idx]:
                if to == par[idx]:
                    continue
                dist[idx] = max(dist[idx], dist[to] + 1)

    def dfs2(idx, d_par, par):
        stack = [(idx,d_par, par)]
        while stack:
            idx, d_par, par = stack.pop()
            d_child = [(0, -1)] # 計算結果、遷移先ノード
            for to in G[idx]:
                if to == par:
                    # 親から伝搬させる Dpar
                    d_child.append((d_par + 1, to))
                else:
                    d_child.append((dist[to] + 1, to))
            d_child.sort(reverse=True)
            ans[idx] = d_child[0][0]
            for to in G[idx]:
                if to == par:
                    continue
                nx_d_par = d_child[d_child[0][1] == to][0]
                stack.append((to, nx_d_par, idx))


    N = int(input())
    if N == 1:
        return print(0)

    G = [[] for _ in range(N)]
    for i in range(N - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        G[a].append(b)
        G[b].append(a)

    topo = []
    P = [-1] * N
    node = [0]
    while node:
        v = node.pop()
        topo.append(v)
        for to in G[v]:
            if to == P[v]:
                continue
            P[to] = v
            node.append(to)

    dist = [0]*N
    ans = [0] * N
    dfs1(topo,P)
    dfs2(0, 0, -1)
    for i in range(N):
        print((N - 1) * 2 - ans[i])

# 再帰版 verify NJPC2017 E
def resolve():
    INF = 1 << 60
    def dfs1(idx, par):
        for (to, cost, bl) in G[idx]:
            if to == par:
                continue
            dfs1(to, idx)
            dist[idx] = max(dist[idx], dist[to] + cost)
            weight[idx] += weight[to] + bl

    def dfs2(idx, d_par, d_w, par):
        d_child = []
        latte = 0
        d_child.append((0, -1))  # cost, par
        for (to, cost, bl) in G[idx]:
            if to == par:
                d_child.append((d_par + cost, to))
                latte += d_w + bl
            else:
                d_child.append((dist[to] + cost, to))
                latte += weight[to] + bl
        d_child.sort(reverse=True)

        ret = INF
        if d_child[0][0] <= D:
            ret = min(ret, latte)
        for (to, cost, bl) in G[idx]:
            if to == par:
                continue
            x = dfs2(to, d_child[d_child[0][1] == to][0], latte - weight[to] - bl, idx)
            ret = min(ret, x)
        return ret

    N, D = map(int, input().split())
    G = [[] for _ in range(N)]
    for _ in range(N - 1):
        a, b, c = map(int, input().split())
        a -= 1
        b -= 1
        G[a].append((b, c, 1))  # 良い方向
        G[b].append((a, c, 0))  # 悪い方向

    dist = [0] * N
    weight = [0] * N

    dfs1(0, -1)
    get = dfs2(0, 0, 0, -1)

    if get == INF:
        print(-1)
    else:
        print(get)

# verified AOJ trafc tree or GRL_5A
def resolve():
    N = int(input())
    G = [[] for _ in range(N)]
    for i in range(N - 1):
        a, b = map(lambda x: int(x) - 1, input().split())
        G[a].append(b)
        G[b].append(a)

    topo = []
    parent = [-1] * N
    node = [0]
    while node:
        s = node.pop()
        topo.append(s)
        for t in G[s]:
            if t == parent[s]:
                continue
            parent[t] = s
            node.append(t)

    memo = [0] * N  # ノードiより下の情報をマージしたもの
    res = [0] * N  # 求めたいやつ、ノードiの上に出ていく情報
    for s in reversed(topo):
        for t in G[s]:
            if t == parent[s]:
                continue
            memo[s] = max(memo[s], res[t])
        res[s] = memo[s] + 1

    TD = [0] * N  # 上からノードiへ向かう辺の情報
    for s in topo:
        acc = TD[s]
        for t in G[s]:
            if t == parent[s]:
                continue
            TD[t] = max(TD[t], acc)
            acc = max(acc, res[t])
        acc = 0
        for t in reversed(G[s]):
            if t == parent[s]:
                continue
            TD[t] = max(TD[t], acc) + 1
            acc = max(acc, res[t])
            res[t] = max(memo[t], TD[t]) + 1

    for i in range(N):
        print((N - 1) * 2 - res[i] + 1)
