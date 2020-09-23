# AOJ: DSL_2_C: Range Search (kD Tree)
# 最近傍探索を効率的にできるデータ構造です
# scipy.KDTree(data, leafsize=10) data: (x, y)

class OneD_Tree:
    def __init__(self, P):
        N = len(P)
        self.P = sorted(P)
        # 配列[ノード]でそのノードの内容を返す。
        self.location = [None] * N  # 整列した配列Pにおける位置
        self.left = [None] * N  # そのノードの左子
        self.right = [None] * N  # そのノードの右子
        self.np = 0  # ノード番号の初期化
        self.make_1DTree(0, N)  # 1dtreeを作る

    def make_1DTree(self, l, r):
        if not (l < r):
            return None

        mid = (l + r) // 2
        t = self.np  # 二分木におけるノード番号を割り当てる
        self.np += 1  # ノード番号の更新

        self.location[t] = mid
        self.left[t] = self.make_1DTree(l, mid)
        self.right[t] = self.make_1DTree(mid + 1, r)

        return t  # 現在のノードを返す

    def find(self, sx, tx):
        """
        sx ... 範囲の最初
        tx ... 範囲の終わり 閉区間に注意
        """
        ret = []  # 範囲に含まれる点を格納しておく

        def dfs(v, sx, tx):
            x = self.P[self.location[v]]
            if sx <= x <= tx:
                ret.append(x)
            # 続いて右と左の子が領域に含まれているかも探索する。
            if self.left[v] is not None and sx <= x:
                dfs(self.left[v], sx, tx)
            if self.right[v] is not None and x <= tx:
                dfs(self.right[v], sx, tx)

        dfs(0, sx, tx)
        return ret


from operator import itemgetter


class TwoD_Tree:

    def __init__(self, P):
        # Pの形式として[(pointID, x, y),...,()]となっていることを想定する
        N = len(P)
        self.P = P.copy()
        # 配列[ノード]でそのノードの内容を返す。
        self.location = [None] * N  # 整列した配列Pにおける位置
        self.left = [None] * N  # そのノードの左子
        self.right = [None] * N  # そのノードの右子
        self.np = 0  # ノード番号の初期化
        self.make_2DTree(0, N, 0)  # 2dtreeを作る

    def make_2DTree(self, l, r, depth):
        if not (l < r):
            return None

        mid = (l + r) // 2
        t = self.np
        self.np += 1

        # ここからx,y軸の分岐
        if depth % 2 == 0:
            # はじめの要素がx軸だと仮定して
            self.P[l:r] = sorted(self.P[l:r], key=itemgetter(1))
        else:
            # depthが奇数のときはy軸
            self.P[l:r] = sorted(self.P[l:r], key=itemgetter(2))

        self.location[t] = mid
        self.left[t] = self.make_2DTree(l, mid, depth + 1)
        self.right[t] = self.make_2DTree(mid + 1, r, depth + 1)
        # 現在のノードを返す
        return t

    def find(self, sx, tx, sy, ty):
        """
        :param sx: xの範囲の最初
        :param tx: xの範囲の終わり 閉区間に注意
        :param sy: yの範囲の最初
        :param ty: yの範囲の終わり 閉区間に注意
        :return: 範囲内の要素
        """
        ret = []

        def dfs(v, sx, tx, sy, ty, depth):
            id, x, y = self.P[self.location[v]]
            if (sx <= x <= tx) and (sy <= y <= ty):
                ret.append((id, x, y))
            # 続いて右と左の子が領域に含まれているかも探索する。
            # ここでdepthが偶数奇数で場合分けをする
            if depth % 2 == 0:
                if self.left[v] is not None and sx <= x:
                    dfs(self.left[v], sx, tx, sy, ty, depth + 1)
                if self.right[v] is not None and x <= tx:
                    dfs(self.right[v], sx, tx, sy, ty, depth + 1)
            else:
                if self.left[v] is not None and sy <= y:
                    dfs(self.left[v], sx, tx, sy, ty, depth + 1)
                if self.right[v] is not None and y <= ty:
                    dfs(self.right[v], sx, tx, sy, ty, depth + 1)

        dfs(0, sx, tx, sy, ty, 0)
        return ret


if __name__ == '__main__':
    # 1次元の点の集合
    from random import shuffle

    # test
    P = [0, 2, 4, 5, 9, 12, 13, 15, 18, 20]
    shuffle(P)
    print("集合：", P)

    kdtree = OneD_Tree(P)
    print("tree", kdtree.find(0, 20))
    print(kdtree.find(6, 15))

    # AOJ DSL_2 load data
    print("AOJ DSL_2 load data")
    N = 6
    P2 = [[2, 1], [2, 2], [4, 2], [6, 2], [3, 3], [5, 4]]
    Points = []
    for id, [x, y] in enumerate(P2):
        Points.append((id, x, y))
    kdtree = TwoD_Tree(Points)
    # query
    Q = [[2, 4, 0, 4], [4, 10, 2, 5]]
    for sx, tx, sy, ty in Q:
        # ID_ls = list(map(itemgetter(0), kdtree.find(sx, tx, sy, ty)))
        ID_ls = [x[0] for x in kdtree.find(sx, tx, sy, ty)]  # itemgetterよりも内包表記のほうが早い
        if len(ID_ls) == 0:
            print()
        else:
            print(*sorted(ID_ls), sep='\n')
            print()
