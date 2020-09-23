# url: https://note.nkmk.me/python-union-find/ より

# n個の要素を0~N-1で管理
class UnionFind:
    # 各要素の親要素の番号を格納するリスト
    # 要素が根（ルート）の場合は-(そのグループの要素数)を格納する
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    # 要素xが属するグループの根を返す
    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    # 要素xが属するグループと要素yが属するグループとを併合する
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    # 要素xが属するグループのサイズ（要素数）を返す
    def size(self, x):
        return -self.parents[self.find(x)]

    # 要素x, yが同じグループに属するかどうかを返す
    def is_same(self, x, y):
        return self.find(x) == self.find(y)

    # 要素xが属するグループに属する要素をリストで返す
    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    # すべての根の要素をリストで返す
    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    # グループの数を返す
    def group_count(self):
        return len(self.roots())

    # {ルート要素: [そのグループに含まれる要素のリスト], ...}の辞書を返す
    def all_group_members(self):
        return {r: self.members(r) for r in self.roots()}

    # ルート要素: [そのグループに含まれる要素のリスト]を文字列で返す (print()での表示用)
    def __str__(self):
        return '\n'.join('{}: {}'.format(r, self.members(r)) for r in self.roots())

# 最小全域木 使用時 very: past No1 L
def kruskal(edges,size):
    """
    :param edges: 入力をそのまま使用 [(a,b,w)....]
    :param size: 頂点数
    :return:
    """
    uf = UnionFind(size)
    edges = sorted(edges, key=lambda e: e[2])
    ret = 0
    for u, v, weight in edges:
        if not uf.is_same(u, v):
            uf.union(u, v)
            ret += weight
    return ret

if __name__ == '__main__':
    uf = UnionFind(6)
    print(uf.parents)    # [-1, -1, -1, -1, -1, -1]

    uf.union(0, 2)
    uf.union(1, 0)
    print(uf.parents)    # [-2, -1, 0, -1, -1, -1]
    print(uf)   # 0: [0, 2], 1: [1], 3: [3], 4: [4], 5: [5]
