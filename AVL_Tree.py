# viary : ABC170_E AVLの代わり C++:Set() 代わり
from heapq import heappush, heappop
from collections import Counter
class HeapSet:
    def __init__(self):
        self.minQue = []
        self.maxQue = []
        self.counter = Counter()

    def insert(self, x):
        heappush(self.minQue, x)
        heappush(self.maxQue, -x)
        self.counter[x] += 1

    def erase(self, x):
        self.counter[x] -= 1

    def max(self):
        while self.maxQue and self.counter[-self.maxQue[0]] == 0:
            heappop(self.maxQue)
        return -self.maxQue[0] if self.maxQue else None

    def min(self):
        while self.minQue and self.counter[self.minQue[0]] == 0:
            heappop(self.minQue)
        return self.minQue[0] if self.minQue else None


"""
kiri8128  viry ABC 170 E, ABC 140 E
10 ** 5ならだいたい2 ** 17ぐらい用意
最新:ABC 140 E で user:customfolk(kiri8128ブログで最新)のBalancingTreeに変更 2020/09/04
ABC 170 E ではレートとインデックスをbitで管理している
"""

class BalancingTree:
    class node:
        def __init__(self, v, p):
            self.value = v
            self.pivot = p
            self.left = None
            self.right = None

    def __init__(self, n):
        self.N = n
        self.root = self.node(1 << n, 1 << n)

    def debug(self):
        def debug_info(nd_):
            return (nd_.value - 1, nd_.pivot - 1, nd_.left.value - 1 if nd_.left else -1,
                    nd_.right.value - 1 if nd_.right else -1)

        def debug_node(nd):
            re = []
            if nd.left:
                re += debug_node(nd.left)
            if nd.value: re.append(debug_info(nd))
            if nd.right:
                re += debug_node(nd.right)
            return re

        print("Debug - root =", self.root.value - 1, debug_node(self.root)[:50])

    def append(self, v):  # v を追加（その時点で v はない前提）
        v += 1
        nd = self.root
        while True:
            if v == nd.value:
                # v がすでに存在する場合に何か処理が必要ならここに書く
                return 0
            else:
                mi, ma = min(v, nd.value), max(v, nd.value)
                if mi < nd.pivot:
                    nd.value = ma
                    if nd.left:
                        nd = nd.left
                        v = mi
                    else:
                        p = nd.pivot
                        nd.left = self.node(mi, p - (p & -p) // 2)
                        break
                else:
                    nd.value = mi
                    if nd.right:
                        nd = nd.right
                        v = ma
                    else:
                        p = nd.pivot
                        nd.right = self.node(ma, p + (p & -p) // 2)
                        break

    def leftmost(self, nd):
        if nd.left: return self.leftmost(nd.left)
        return nd

    def rightmost(self, nd):
        if nd.right: return self.rightmost(nd.right)
        return nd

    # vより真に小さいやつの中での最大値の値（なければ-1）[10,5,8,20]   v=20 -> return 10
    def find_l(self, v):
        v += 1
        nd = self.root
        prev = 0
        if nd.value < v: prev = nd.value
        while True:
            if v <= nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    return prev - 1
            else:
                prev = nd.value
                if nd.right:
                    nd = nd.right
                else:
                    return prev - 1

    # vより真に大きいやつの中での最小値（なければNone）[10,5,8,20]   v=10 -> return 20
    def find_r(self, v):
        v += 1
        nd = self.root
        prev = 0
        if nd.value > v: prev = nd.value
        while True:
            if v < nd.value:
                prev = nd.value
                if nd.left:
                    nd = nd.left
                else:
                    if prev == 2 ** self.N:
                        return None
                    else:
                        return prev - 1
            else:
                if nd.right:
                    nd = nd.right
                else:
                    if prev == 2 ** self.N:
                        return None
                    else:
                        return prev - 1

    # @property 好みにより付ける  use: BT.find_max  ()をつけない
    def find_max(self):
        return self.find_l((1 << self.N) - 1)

    # @property  好みになる
    def find_min(self):
        return self.find_r(-1)

    def delete(self, v, nd=None, prev=None):  # 値がvのノードがあれば削除（なければ何もしない）
        v += 1
        if not nd: nd = self.root
        if not prev: prev = nd
        while v != nd.value:
            prev = nd
            if v <= nd.value:
                if nd.left:
                    nd = nd.left
                else:
                    return
            else:
                if nd.right:
                    nd = nd.right
                else:
                    return
        if (not nd.left) and (not nd.right):
            if nd.value < prev.value:
                prev.left = None
            else:
                prev.right = None
        elif not nd.left:
            if nd.value < prev.value:
                prev.left = nd.right
            else:
                prev.right = nd.right
        elif not nd.right:
            if nd.value < prev.value:
                prev.left = nd.left
            else:
                prev.right = nd.left
        else:
            nd.value = self.leftmost(nd.right).value
            self.delete(nd.value - 1, nd.right, nd)

    def __contains__(self, v: int) -> bool:
        return self.find_r(v - 1) == v

