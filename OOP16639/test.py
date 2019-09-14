from contracts import contract

def factorize(n):
    """
        Factorize positive integer and return its factors.
        :type n: int,>=0
        :rtype: tuple[N],N>0
    """
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        ans.append(n)
    return ans


if __name__ == "__main__":
    x = 77
    # a, b = factorize(x)
    m = factorize(x)
    print(m)
