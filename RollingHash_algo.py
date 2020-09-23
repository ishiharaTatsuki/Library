MOD = 10 ** 9 + 7


# 平衡二部探索
def bisect(l, r, f, discrete=True, left=True):
    """
        l,r: l<r int if discrete else float
        f: function defined on [l,...,r] to {False,True}
        if discrete: f defined on Z; else: R
        if left: f satisfies that there uniquely exists d such that iff i<=d then f(i)
        else: iff i>=d then f(i) is True
        return d such as those above
    """
    assert r > l
    if discrete:
        assert isinstance(l, int) and isinstance(r, int)
    eps = 1 if discrete else 10 ** -12
    if (not left) ^ f(r):
        return r if left else r + 1
    elif left ^ f(l):
        return l - 1 if left else l
    while r - l > eps:
        h = (l + r) // 2 if discrete else (l + r) / 2
        if (not left) ^ f(h):
            l = h
        else:
            r = h
    return h if not discrete else l if left else r


class RollingHash(object):
    """
        construct: O(N)
        query:
            hash: O(1)
            lcp: O(logN)
            search: O(N)
    """
    __base1 = 1007;
    __mod1 = 10 ** 9
    __base2 = 1009;
    __mod2 = 10 ** 7

    def __init__(self, s):
        n = len(s)
        self.__s = s
        self.__n = n
        b1 = self.__base1;
        m1 = self.__mod1
        b2 = self.__base2;
        m2 = self.__mod2
        H1, H2 = [0] * (n + 1), [0] * (n + 1)
        P1, P2 = [1] * (n + 1), [1] * (n + 1)
        for i in range(n):
            H1[i + 1] = (H1[i] * b1 + ord(s[i])) % m1
            H2[i + 1] = (H2[i] * b2 + ord(s[i])) % m2
            P1[i + 1] = P1[i] * b1 % m1
            P2[i + 1] = P2[i] * b2 % m2
        self.__H1 = H1
        self.__H2 = H2
        self.__P1 = P1
        self.__P2 = P2

    @property
    def str(self):
        return self.__s

    @property
    def len(self):
        return self.__n

    def hash(self, l, r=None):
        """
            l,r: int (0<=l<=r<=n)
            return (hash1,hash2) of S[l:r]
        """
        m1 = self.__mod1
        m2 = self.__mod2
        if r is None: r = self.__n
        assert 0 <= l <= r <= self.__n
        hash1 = (self.__H1[r] - self.__P1[r - l] * self.__H1[l] % m1) % m1
        hash2 = (self.__H2[r] - self.__P2[r - l] * self.__H2[l] % m2) % m2
        return hash1, hash2

    @classmethod
    def lcp(cls, rh1, rh2, l1, l2, r1=None, r2=None):
        """
            rh1,rh2: RollingHash object
            l1,l2,r1,r2: int 0<=l1<=r1<=r1.len, 0<=l2<=r2<=rh2.len
            return lcp length between rh1[l1:r1] and rh2[l2:r2]
        """
        if r1 is None: r1 = rh1.__n
        if r2 is None: r2 = rh2.__n
        assert 0 <= l1 <= r1 <= rh1.__n and 0 <= l2 <= r2 <= rh2.__n
        L = 0
        R = min(r1 - l1, r2 - l2)
        if rh1.hash(l1, l1 + R) == rh2.hash(l2, l2 + R): return R
        while R - L > 1:
            H = (L + R) // 2
            if rh1.hash(l1, l1 + H) == rh2.hash(l2, l2 + H): L = H
        else:
            R = H
        return L

    @classmethod
    def search(cls, pattern, text):
        """
        pattern,text: RollingHash object
        return list of index i's satisfying text[i:] starts with pattern
        """
        n = text.__n;
        m = pattern.__n
        res = []
        for i in range(n - m + 1):
            if text.hash(i, i + m) == pattern.hash(0, m):
                res.append(i)
        return res

# ABC 150 F: reborn18
class KMP:
    def __init__(self, P):
        self.P = P
        self.N = len(P)
        self.T = [0] * (self.N + 1)
        self._compile()

    def _compile(self):
        j = 0
        self.T[0] = -1
        for i in range(1, self.N):
            self.T[i] = j
            j += 1 if self.P[i] == self.P[j] else -j
        self.T[self.N] = j

    def search(self, S):
        NS = len(S)
        i = m = 0
        A = []
        while m + i < NS:
            if self.P[i] == S[m + i]:
                i += 1
                if i != self.N:
                    continue
                A.append(m)
            m += i - self.T[i]
            i = max(0, self.T[i])
        return A

def Z_algo(S):
    n = len(S)
    LCP = [0]*n
    i = 1
    j = 0
    c = 0#最も末尾側までLCPを求めたインデックス
    for i in range(1, n):
        #i番目からのLCPが以前計算したcからのLCPに含まれている場合
        if i+LCP[i-c] < c+LCP[c]:
            LCP[i] = LCP[i-c]
        else:
            j = max(0, c+LCP[c]-i)
            while i+j < n and S[j] == S[i+j]: j+=1
            LCP[i] = j
            c = i
    LCP[0] = n
    return LCP



if __name__ == '__main__':
    # d=0ではtrue,d=nではfalseなので、そこでbisectする
    n = 13
    S = "strangeorange"
    rh = RollingHash(S)
    def judge(d):
        J = {rh.hash(i, i+d): -1 for i in range(n-d+1)}
        for i in range(n-d+1):
            h = rh.hash(i, i+d)
            if J[h] != -1:
                if i-J[h] >= d: return True
            else:
                J[h] = i
        return False
    print(bisect(0, n, judge))
