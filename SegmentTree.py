# http://tsutaj.hatenablog.com/entry/2017/03/29/204841
import operator


class SegmentTree:
    def __init__(self, size, fn=operator.add, default=None, initial_values=None):
        """
        :param int size:
        :param callable fn: 区間に適用する関数。引数を 2 つ取る。min, max, operator.xor など
        :param default:初期値
        :param list initial_values:
        """
        default = default or 0

        # size 以上である最小の 2 冪を size とする
        n = 1
        while n < size:
            n *= 2
        self._size = n
        self._fn = fn

        self._tree = [default] * (self._size * 2 - 1)
        if initial_values:
            i = self._size - 1
            for v in initial_values:
                self._tree[i] = v
                i += 1
            i = self._size - 2
            while i >= 0:
                self._tree[i] = self._fn(self._tree[i * 2 + 1], self._tree[i * 2 + 2])
                i -= 1

    def set(self, i, value):
        """
        i 番目に value を設定
        :param int i:
        :param value:
        :return:
        """
        x = self._size - 1 + i
        self._tree[x] = value

        while x > 0:
            x = (x - 1) // 2
            self._tree[x] = self._fn(self._tree[x * 2 + 1], self._tree[x * 2 + 2])

    def update(self, i, value):
        """
        もとの i 番目と value に fn を適用したものを i 番目に設定
        :param int i:
        :param value:
        :return:
        """
        x = self._size - 1 + i
        self.set(i, self._fn(self._tree[x], value))

    def get(self, from_i, to_i=None, k=0, L=None, r=None):
        """
        [from_i, to_i) に fn を適用した結果を返す
        :param int from_i:
        :param int to_i:
        :param int k: self._tree[k] が、[L, r) に fn を適用した結果を持つ
        :param int L:
        :param int r:
        :return:
        """
        if to_i is None:
            return self._tree[self._size - 1 + from_i]

        L = 0 if L is None else L
        r = self._size if r is None else r

        if from_i <= L and r <= to_i:
            return self._tree[k]

        if to_i <= L or r <= from_i:
            return None

        ret_L = self.get(from_i, to_i, k * 2 + 1, L, (L + r) // 2)
        ret_r = self.get(from_i, to_i, k * 2 + 2, (L + r) // 2, r)
        if ret_L is None:
            return ret_r
        if ret_r is None:
            return ret_L
        return self._fn(ret_L, ret_r)

    def __len__(self):
        return self._size



# past No2 N
class StarrySkyTree:
    """ Starry Sky Tree(区間加算・区間最小(大)値取得) """

    def __init__(self, N, func, intv):
        self.intv = intv
        self.func = func
        LV = (N - 1).bit_length()
        self.N0 = 2 ** LV
        self.data = [0] * (2 * self.N0)
        self.lazy = [0] * (2 * self.N0)

    # 伝搬される区間のインデックス(1-indexed)を全て列挙するgenerator
    def gindex(self, l, r):
        L = l + self.N0
        R = r + self.N0
        lm = (L // (L & -L)) >> 1
        rm = (R // (R & -R)) >> 1
        while L < R:
            if R <= rm:
                yield R
            if L <= lm:
                yield L
            L >>= 1
            R >>= 1
        while L:
            yield L
            L >>= 1

    # 遅延評価の伝搬処理
    def propagates(self, *ids):
        # 1-indexedで単調増加のインデックスリスト
        for i in reversed(ids):
            v = self.lazy[i - 1]
            if not v:
                continue
            self.lazy[2 * i - 1] += v
            self.lazy[2 * i] += v
            self.data[2 * i - 1] += v
            self.data[2 * i] += v
            self.lazy[i - 1] = 0

    def update(self, l, r, x):
        """ 区間[l,r)の値にxを加算 """

        # 1. lazyの値は伝搬させない
        # 2. 区間[l,r)のdata, lazyの値を更新
        L = self.N0 + l
        R = self.N0 + r
        while L < R:
            if R & 1:
                R -= 1
                self.lazy[R - 1] += x
                self.data[R - 1] += x
            if L & 1:
                self.lazy[L - 1] += x
                self.data[L - 1] += x
                L += 1
            L >>= 1
            R >>= 1
        # 3. 更新される区間を部分的に含んだ区間のdataの値を更新 (lazyの値を考慮)
        for i in self.gindex(l, r):
            self.data[i - 1] = self.func(self.data[2 * i - 1], self.data[2 * i]) + self.lazy[i - 1]

    def query(self, l, r):
        """ 区間[l,r)の最小(大)値を取得 """

        # 1. トップダウンにlazyの値を伝搬
        self.propagates(*self.gindex(l, r))
        L = self.N0 + l
        R = self.N0 + r

        # 2. 区間[l, r)の最小(大)値を求める
        s = self.intv
        while L < R:
            if R & 1:
                R -= 1
                s = self.func(s, self.data[R - 1])
            if L & 1:
                s = self.func(s, self.data[L - 1])
                L += 1
            L >>= 1
            R >>= 1
        return s


"""遅延評価セグメント木"""
"""
セグメント木上で、各区間を計算する必要があるまで更新しない(値の伝搬を遅延させる)ようにしたデータ構造。
区間の更新処理と区間の取得処理がO(logN)でできる。
"""

# ABC 153 F Coki628 veryfi
# segfuncに使用
from operator import add
class LasySegmentTree:
    def __init__(self, size: int, segfunc, lazy_ide_ele=0):
        self.lazy_ide_ele = lazy_ide_ele
        self.segfunc = segfunc
        self.N0 = 1 << (size - 1).bit_length()
        self.lazy = [self.lazy_ide_ele] * (2 * self.N0)

    def gindex(self, left, right):
        L = left + self.N0
        R = right + self.N0
        lm = (L // (L & -L)) >> 1
        rm = (R // (R & -R)) >> 1
        while L < R:
            if R <= rm:
                yield R
            if L <= lm:
                yield L
            L >>= 1
            R >>= 1
        while L:
            yield L
            L >>= 1

    def propagates(self, *ids):
        for i in reversed(ids):
            idx = i - 1
            v = self.lazy[idx]
            if v == self.lazy_ide_ele:
                continue
            self.lazy[2 * idx + 1] = self.segfunc(self.lazy[2 * idx + 1], v)
            self.lazy[2 * idx + 2] = self.segfunc(self.lazy[2 * idx + 2], v)
            self.lazy[idx] = self.lazy_ide_ele

    def update(self, left: int, right: int, x):
        L = self.N0 + left
        R = self.N0 + right

        while L < R:
            if R & 1:
                R -= 1
                self.lazy[R - 1] = self.segfunc(self.lazy[R - 1], x)
            if L & 1:
                self.lazy[L - 1] = self.segfunc(self.lazy[L - 1], x)
                L += 1
            L >>= 1
            R >>= 1

    def query(self, k: int):
        self.propagates(*self.gindex(k, k + 1))
        return self.lazy[k + self.N0 - 1]

# ABC 146 F   very:AT274
class RangeMinimumQuery:
    def __init__(self, n, inf=2 ** 31 - 1):
        self.n = 1 << (n - 1).bit_length()
        self.INF = inf
        self.segtree = [self.INF] * (2 * self.n)

    # i番目の値(0-indexed)をxに変更
    def update(self, i, x):
        i += self.n
        self.segtree[i] = x
        while i > 0:
            i //= 2
            self.segtree[i] = min(self.segtree[2 * i], self.segtree[2 * i + 1])

    # [l, r)のmin
    def query(self, l, r):
        L, R = l + self.n, r + self.n
        R = min(R, len(self.segtree))
        s = self.INF
        while L < R:
            if L & 1:
                s = min(s, self.segtree[L])
                L += 1

            if R & 1:
                s = min(s, self.segtree[R - 1])
                R -= 1

            L >>= 1
            R >>= 1

        return s


# 不変な数列の任意の区間に対する最小値/最大値を、前処理 O(NlogN)O(NlogN), クエリごと O(1) で求めるデータ構造です。
# 数列の値が変わる場合はSegmentTree
from operator import or_
class SparseTable:
    def __init__(self, N, arr, op):
        self.N = N
        self.depth = N.bit_length()
        self.op = op
        self.arr = tuple(arr)
        self._build()

    def __call__(self, s, t):
        """
        [s, t)区間（0-indexed）での値を返す
        """
        i = (t - s).bit_length() - 1
        L = self.table[i][s]
        R = self.table[i][t - (1 << i)]
        return self.op(L, R)

    def _build(self):
        self.table = []
        self.table.append(self.arr)
        N = self.N
        for i in range(self.depth - 1):
            shift = 1 << i
            N -= shift
            t = tuple(self.op(self.table[-1][j], self.table[-1][j + shift])
                      for j in range(N))
            self.table.append(t)