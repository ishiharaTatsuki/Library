"""
参考：https://www.hamayanhamayan.com/entry/2018/03/18/085108
　　　http://vartkw.hatenablog.com/entry/2016/12/02/002703
　　　https://ikatakos.com/pot/programming_algorithm/graph_theory/maximum_flow
・二部最大マッチング
・最大流アルゴリズム(Dinic法)
very:ABC 091 C
"""

from collections import deque


class BipartiteMatching:

    def __init__(self, n, m):
        self.n = n
        self.m = m
        # ペアとして有りうる相手を格納する
        self.E = [[] * (n + m + 2) for i in range(n + m + 2)]
        # 決まったペアを格納する
        self.match = [0] * (n + m + 2)
        # 距離(付け替え候補を決める時の深さみたいなものが入ってる)
        self.dist = [0] * (n + m + 2)

    def bfs(self):
        que = deque()
        for i in range(1, self.n + 1):
            # マッチングの決まっていないノードをキューに詰める
            if not self.match[i]:
                self.dist[i] = 0
                que.append(i)
            else:
                self.dist[i] = float('inf')
        self.dist[0] = float('inf')
        while len(que) != 0:
            u = que.popleft()
            if u != 0:
                for v in self.E[u]:
                    if self.dist[self.match[v]] == float('inf'):
                        self.dist[self.match[v]] = self.dist[u] + 1
                        # 付け替えの候補になりうるノードがここで追加されていく
                        que.append(self.match[v])
        # フローを流せるエッジが存在しなければ、dist[0]がINFのまま(Falseを返して終了)
        return self.dist[0] != float('inf')

    def dfs(self, u):
        if u != 0:
            for v in self.E[u]:
                if self.dist[self.match[v]] == self.dist[u] + 1:
                    if self.dfs(self.match[v]):
                        # ペア確定(あとで変わることもある)
                        self.match[v] = u
                        self.match[u] = v
                        return True
            # 今回決められなかったノード
            self.dist[u] = float('inf')
            return False
        return True

    def add(self, a, b):
        b += self.n
        self.E[a + 1].append(b + 1)
        self.E[b + 1].append(a + 1)

    def whois(self, x):
        return self.match[x + 1] - 1

    def solve(self):
        for i in range(self.n + self.m + 1):
            self.match[i] = 0
        res = 0
        while self.bfs():
            for i in range(1, self.n + 1):
                # 前から順に繋げる所は繋いでいって、
                # もっといいのがあれば後から付け替える
                if not self.match[i] and self.dfs(i):
                    res += 1
        return res