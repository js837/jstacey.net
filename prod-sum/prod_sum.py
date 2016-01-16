""""
X and Y are two different integers, greater than 1, with sum less than 100. S and P are two mathematicians; S knows the sum X+Y, P knows the product X*Y, and both know the information in these two sentences. The following conversation occurs:

(s1) P says "I do not know X and Y."
(s2) S says "I knew you don't know X and Y."
(s3) P says "Now I know X and Y."
(s4) S says "Now I know X and Y too!"
What are X and Y?
"""


def sums(n):
    """
    Get all possible x, y with x<=y that add to n.

    Example:
    >>> sums(8)
    [(2, 6), (3, 5), (4, 4),]
    """
    ret = set()
    for x in range(2, n // 2 + 1):
        if n < 100:
            ret.add((x, n - x))
    return ret


def products(n):
    """
    Get all possible x, y with x<=y that multiply to n.

    Example:
    >>> products(12)
    [(2, 6), (3, 4) ]
    """
    ret = set()
    x = 2
    while x ** 2 <= n:
        if n % x == 0 and x + n // x < 100:
            ret.add((x, n // x))
        x += 1
    return ret


def s1(x, y):
    p = x * y
    return len(products(p)) > 1


def s2(x, y):
    s = x + y
    for i, j in sums(s):
        p = i * j
        if len(products(p)) <= 1:
            return False
    return True


def s3(x, y):
    p = x * y
    count = 0
    for a, b in products(p):
        if s2(a, b):
            count += 1

    if count == 1:
        return True
    else:
        return False


def s4(x, y):
    s = x + y
    count = 0
    for a, b in sums(s):
        if s3(a, b):
            count += 1

    if count == 1:
        return True
    else:
        return False


def main():
    # Generate the test set
    main_set = set()
    N_MAX = 98
    for y in range(2, N_MAX + 1):
        for x in range(2, y + 1):
            if x + y < 100:
                main_set.add((x, y))

    # Find values which satisfy S1, S2, s3 and s4
    for x, y in main_set:
        if s1(x, y) and s2(x, y) and s3(x, y) and s4(x, y):
            print(x, y)

if __name__ == '__main__':
    main()
