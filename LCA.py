import sys
sys.setrecursionlimit(500000)
class LCA:
    def __init__(self, E, root, cost_flag=True):
        self.root = root
        self.E = E  # V<V>
        self.n = len(E)  # 頂点数
        self.logn = 1  # n < 1<<logn  ぴったりはだめ
        self.cost_flag = cost_flag
        while self.n >= (1 << self.logn):
            self.logn += 1

        # parent[n][v] = ノード v から 1<<n 個親をたどったノード
        self.parent = [[-1] * self.n for _ in range(self.logn)]
        # ノード間の最大重み
        self.max_cost = [[0] * self.n for _ in range(self.logn)]

        self.depth = [0] * self.n
        self.dfs(root, -1, 0)
        for k in range(self.logn - 1):
            for v in range(self.n):
                p_ = self.parent[k][v]
                if p_ >= 0:
                    self.parent[k + 1][v] = self.parent[k][p_]
                    self.max_cost[k + 1][v] = max(self.max_cost[k][v], self.max_cost[k][p_]);

    def dfs(self, v, p, dep):
        # ノード番号、親のノード番号、深さ
        self.parent[0][v] = p
        self.depth[v] = dep
        for e in self.E[v]:
            if self.cost_flag:
                to, cost = e
            else:
                to, cost = e, 0

            if to != p:
                self.max_cost[0][to] = cost
                self.dfs(to, v, dep + 1)

    def get_lca(self, u, v):
        if self.depth[u] > self.depth[v]:
            u, v = v, u  # self.depth[u] <= self.depth[v]
        dep_diff = self.depth[v] - self.depth[u]
        for k in range(self.logn):
            if dep_diff >> k & 1:
                v = self.parent[k][v]
        if u == v:
            return u
        for k in range(self.logn - 1, -1, -1):
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        return self.parent[0][u]

    def get_max_cost(self, u, v):
        if self.depth[u] > self.depth[v]:
            u, v = v, u  # self.depth[u] <= self.depth[v]
        dep_diff = self.depth[v] - self.depth[u]
        ret = 0
        for k in range(self.logn):
            if dep_diff >> k & 1:
                ret = max(ret, self.max_cost[k][v])
                v = self.parent[k][v]
        if u == v:
            return ret
        for k in range(self.logn - 1, -1, -1):
            if self.parent[k][u] != self.parent[k][v]:
                ret = max(ret, self.max_cost[k][u], self.max_cost[k][v])
                u = self.parent[k][u]
                v = self.parent[k][v]
        ret = max(ret, self.max_cost[0][u], self.max_cost[0][v])
        return ret

    def distance(self, u, v):
        """
        u, v 間の距離
        depth[u] + depth[v] - depth[lca] * 2
        :param u:
        :param v:
        :rtype: int
        """
        lca = self.get_lca(u, v)
        return self.depth[u] + self.depth[v] - self.depth[lca] * 2
