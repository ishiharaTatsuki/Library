# 素因数分解 列挙
# 4未満の場合、値が入るので注意
def prime_factorize(n):
    if 2 <= n < 4:
        return [n]
    res = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            res.append(i)
            n //= i
        i += 1
    if n != 1:
        res.append(n)
    res.sort()
    return res


# 素数:指数:exponent
def dic_prime_fact(n):
    dic = {}  # 素数:指数
    i = 2
    while i * i <= n:
        while n % i == 0:
            n //= i
            if i in dic:
                dic[i] += 1
            else:
                dic[i] = 1
        i += 1
    if n > 1:
        dic[n] = 1
    return dic


# 素数テーブル
# エラトステネスのふるい
def make_primes_table(n):
    if n < 2:
        return [False] * n
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            # 倍数は素数ではないので削除していく
            for j in range(i * 2, n + 1, i):
                is_prime[j] = False
    return is_prime


# 素数判定
def is_prime(x):
    if x < 2:
        return False
    elif x == 2:
        return True
    if x % 2 == 0:
        return False
    for i in range(3, int(x ** 0.5) + 1, 2):
        if x % i == 0:
            return False
    return True
