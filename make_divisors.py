import numpy as np
# 各Nの約数の個数を作る 0~N 1:1, 2:2, 3:2, 4:2 ABC 172 D maspy
# o(NlogN)
def make_divisors_count(n):
    div = np.zeros(n + 1, np.int64)
    for i in range(1, n + 1):
        for m in range(i, n + 1, i): # iの倍数
            div[m] += 1
    return div


# 約数列挙
# 重複なし
def make_divisors(n):
    divisors = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)

    divisors.sort()
    return divisors

# 約数列挙
# 重複あり set()で削除
def make_divisors(n):
    divisors = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            # divisors.append((i, n // i)) # [(1,max), (2, max-1)]
            divisors += [i, n // i] # [1,2,3,5]
    divisors.sort()
    return divisors


# 最大公約数
def make_gcd(x, y):
    if x < y:
        x, y = y, x

    while y > 0:
        r = x % y
        x, y = y, r
    return x


# 最小公倍数 ABC152 F
from math import gcd
from functools import reduce
def lcm_base(x, y):
    return (x * y) // gcd(x, y)

# 配列の最小公倍数
def lcm_list(arr):
    return reduce(lcm_base, arr, 1)