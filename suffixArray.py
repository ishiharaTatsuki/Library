# SuffixArray O(N**2)
class SuffixArray(object):
    """
    construct:
        suffix array: O(N(logN)^2)
        lcp array: O(N)
        sparse table: O(NlogN)
    query:
        lcp: O(1)
    """

    def __init__(self, s):
        """
        s: str
        """
        self.__s = s
        self.__n = len(s)
        self.__suffix_array()
        self.__lcp_array()
        self.__sparse_table()

    # suffix array
    def __suffix_array(self):
        s = self.__s;
        n = self.__n
        # initialize
        sa = list(range(n))
        rank = [ord(s[i]) for i in range(n)]
        tmp = [0] * n
        k = 1
        cmp_key = lambda i: (rank[i], rank[i + k] if i + k < n else -1)
        # iterate
        while (k <= n):
            sa.sort(key=cmp_key)
            tmp[sa[0]] = 0
            for i in range(1, n):
                tmp[sa[i]] = tmp[sa[i - 1]] + (cmp_key(sa[i - 1]) < cmp_key(sa[i]))
            rank = tmp[:]
            k <<= 1
        self.__sa = sa
        self.__rank = rank

    # LCP array
    def __lcp_array(self):
        s = self.__s;
        n = self.__n
        sa = self.__sa;
        rank = self.__rank
        lcp = [0] * n
        h = 0
        for i in range(n):
            j = sa[rank[i] - 1]
            if h > 0: h -= 1
            if rank[i] == 0: continue
            while j + h < n and i + h < n and s[j + h] == s[i + h]: h += 1
            lcp[rank[i]] = h
        self.__lcp = lcp

    # sparse table
    def __sparse_table(self):
        n = self.__n
        logn = max(0, (n - 1).bit_length())
        table = [[0] * n for _ in range(logn)]
        table[0] = self.__lcp[:]
        # construct
        from itertools import product
        for i, k in product(range(1, logn), range(n)):
            if k + (1 << (i - 1)) >= n:
                table[i][k] = table[i - 1][k]
            else:
                table[i][k] = min(table[i - 1][k], table[i - 1][k + (1 << (i - 1))])
        self.__table = table

    def lcp(self, a, b):
        """
        a,b: int 0<=a,b<n
        return LCP length between s[a:] and s[b:]
        """
        if a == b: return self.__n - a
        l, r = self.__rank[a], self.__rank[b]
        l, r = min(l, r) + 1, max(l, r) + 1
        i = max(0, (r - l - 1).bit_length() - 1)
        table = self.__table
        return min(table[i][l], table[i][r - (1 << i)])

# Z algorithm
def Z(s):
    n = len(s)
    z = [0]*n
    z[0] = n
    L, R = 0, 0
    for i in range(1, n):
        if i >= R: # 過去の結果が全く使えない
            L = R = i
            while R < n and s[R-L]==s[R]:
                R += 1
            z[i] = R-L
        elif z[i-L] < R-i: # 過去の結果が全て使える
            z[i] = z[i-L]
        else: # 過去の結果が一部使える
            L = i
            while R < n and s[R-L] == s[R]:
                R += 1
            z[i] = R-L
    return z

if __name__ == '__main__':
    s = "strangeorange"
    n = len(s)
    sa = SuffixArray(s)
    print("sa:",sa.lcp(2, 8))  # 5
    print("z:", Z("abaaabaabb"))
