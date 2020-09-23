# nCk % mod web:drken

# nCk = n! / n!(n-k)! のテーブル作成
def COMinit(n, MOD):
    fact = [1, 1]
    fact_inv = [1, 1]
    inv = [0, 1]
    for i in range(2, n + 1):
        fact.append((fact[-1] * i) % MOD)
        inv.append((-inv[MOD % i] * (MOD // i)) % MOD)
        fact_inv.append((fact_inv[-1] * inv[i]) % MOD)
    return fact, fact_inv

# 二項係数計算
def Combination(n, k, MOD=10**9+7):
    fac, finv = COMinit(n, MOD)
    if n<k: return 0
    if n<0 or k<0: return 0
    ret = fac[n] * (finv[k] * finv[n-k] % MOD) % MOD
    return ret

# テーブルなし
def combination(n, r, mod=10**9+7):
    n1, r = n+1, min(r, n-r)
    numer = denom = 1
    for i in range(1, r+1):
        numer = numer * (n1-i) % mod
        denom = denom * i % mod
    return numer * pow(denom, mod-2, mod) % mod


############ABC171F used:Ribura##########################
# init() == COMinit(n, MOD):と同じ (fac, finv)を作成
# n_max: 要素の数 len(A[])? ABC151E
class Combination:
    def __init__(self, n_max, mod=10 ** 9 + 7):
        # O(n_max + log(mod))
        self.mod = mod
        f = 1
        self.fac = fac = [f]
        for i in range(1, n_max + 1):
            f = f * i % mod
            fac.append(f)
        f = pow(f, mod - 2, mod)
        self.facinv = facinv = [f]
        for i in range(n_max, 0, -1):
            f = f * i % mod
            facinv.append(f)
        facinv.reverse()

    # "n 要素" は区別できる n 要素
    # "k グループ" はちょうど k グループ

    def __call__(self, n, r):  # self.C と同じ
        return self.fac[n] * self.facinv[r] % self.mod * self.facinv[n - r] % self.mod

    def nCr(self, n, r):
        if not 0 <= r <= n:
            return 0
        return self.fac[n] * self.facinv[r] % self.mod * self.facinv[n - r] % self.mod

    def nPr(self, n, r):
        if not 0 <= r <= n:
            return 0
        return self.fac[n] * self.facinv[n - r] % self.mod

    def nHr(self, n, r):
        if (n == 0 and r > 0) or r < 0:
            return 0
        return self.fac[n + r - 1] * self.facinv[r] % self.mod * self.facinv[n - 1] % self.mod

    def rising_factorial(self, n, r):  # 上昇階乗冪 n * (n+1) * ... * (n+r-1)
        return self.fac[n + r - 1] * self.facinv[n - 1] % self.mod

    def stirling_first(self, n, k):  # 第 1 種スターリング数  lru_cache を使うと O(nk)  # n 要素を k 個の巡回列に分割する場合の数
        if n == k:
            return 1
        if k == 0:
            return 0
        return (self.stirling_first(n - 1, k - 1) + (n - 1) * self.stirling_first(n - 1, k)) % self.mod

    def stirling_second(self, n, k):  # 第 2 種スターリング数 O(k + log(n))  # n 要素を区別のない k グループに分割する場合の数
        if n == k:
            return 1  # n==k==0 のときのため
        return self.facinv[k] * sum(
            (-1) ** (k - m) * self.C(k, m) * pow(m, n, self.mod) for m in range(1, k + 1)) % self.mod

    def balls_and_boxes_3(self, n, k):  # n 要素を区別のある k グループに分割する場合の数  O(k + log(n))
        return sum((-1) ** (k - m) * self.C(k, m) * pow(m, n, self.mod) for m in range(1, k + 1)) % self.mod

    def bernoulli(self, n):  # ベルヌーイ数  lru_cache を使うと O(n**2 * log(mod))
        if n == 0:
            return 1
        if n % 2 and n >= 3:
            return 0  # 高速化
        return (- pow(n + 1, self.mod - 2, self.mod) * sum(
            self.C(n + 1, k) * self.bernoulli(k) % self.mod for k in range(n))) % self.mod

    def faulhaber(self, k, n):  # べき乗和 0^k + 1^k + ... + (n-1)^k
        # bernoulli に lru_cache を使うと O(k**2 * log(mod))  bernoulli が計算済みなら O(k * log(mod))
        return pow(k + 1, self.mod - 2, self.mod) * sum(
            self.C(k + 1, j) * self.bernoulli(j) % self.mod * pow(n, k - j + 1, self.mod) % self.mod for j in
            range(k + 1)) % self.mod

    def lah(self, n, k):  # n 要素を k 個の空でない順序付き集合に分割する場合の数  O(1)
        return self.C(n - 1, k - 1) * self.fac[n] % self.mod * self.facinv[k] % self.mod

    def bell(self, n, k):  # n 要素を k グループ以下に分割する場合の数  O(k**2 + k*log(mod))
        return sum(self.stirling_second(n, j) for j in range(1, k + 1)) % self.mod


##################################
X, Y = 3,3
total = int((X+Y)/3)
n = X - total
ret = Combination(total, n)
print(ret)



