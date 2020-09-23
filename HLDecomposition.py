# HL分解
class HLDecomposition:
    def __init__(self, N):
        self.N = N
        self.pos = 0
        self.G = [list() for _ in range(N)]
        self.vid = [-1] * N
        self.head = [0] * N
        self.sub = [1] * N
        self.hvy = [-1] * N
        self.par = [-1] * N
        self.dep = [0] * N
        self.inv = [0] * N
        self.rng = [0] * N  # subtree of v -> [vid[v], rng[v])

    def add_edge(self, u, v):
        self.G[u].append(v)
        self.G[v].append(u)
        return

    def build(self, rs=(0,)):
        for r in rs:
            self._dfs(r)
            self._dfs_hld(r)
        return

    def get_id(self, v):
        return self.vid[v]

    def _dfs(self, rt):
        self.par[rt] = -1
        self.dep[rt] = 0
        st = list();
        st.append([rt, 0])
        while st:
            v, i = st[-1]
            if i < len(self.G[v]):
                u = self.G[v][i]
                st[-1][1] += 1
                if u == self.par[v]:
                    continue
                self.par[u] = v
                self.dep[u] = self.dep[v] + 1
                st.append([u, 0])
            else:
                st.pop()
                res = 0
                for u in self.G[v]:
                    if u == self.par[v]:
                        continue
                    self.sub[v] += self.sub[u]
                    if res < self.sub[u]:
                        res = self.sub[u]
                        self.hvy[v] = u
        return

    def _dfs_hld(self, r):
        q = [r]
        while q:
            v = q[-1]
            if self.vid[v] < 0:
                self.vid[v] = self.pos
                self.pos += 1
                self.inv[self.vid[v]] = v
                self.head[v] = v
                if self.hvy[self.par[v]] == v:
                    self.head[v] = self.head[self.par[v]]
                for u in self.G[v]:
                    if u != self.par[v] and u != self.hvy[v]:
                        q.append(u)
                if self.hvy[v] >= 0:
                    q.append(self.hvy[v])
            else:
                q.pop()
                self.rng[v] = self.pos
        return

    def for_each(self, u, v, func=None, edge=False):
        while True:
            if self.vid[u] > self.vid[v]:
                u, v = v, u
            if self.head[u] != self.head[v]:
                if func:
                    func(self.vid[self.head[v]], self.vid[v])
                else:
                    yield (self.vid[self.head[v]], self.vid[v])
                v = self.par[self.head[v]]
            else:
                if u != v:
                    if func:
                        func(self.vid[u] + edge, self.vid[v])
                    else:
                        yield (self.vid[u] + edge, self.vid[v])
                break

    def subtree_range(self, v):  # Need Repair
        return (self.vid[v], self.rng[v])
