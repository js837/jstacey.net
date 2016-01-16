""""
X and Y are two different integers, greater than 1, with sum less than 100. S and P are two mathematicians; S knows the sum X+Y, P knows the product X*Y, and both know the information in these two sentences. The following conversation occurs:

(s1) P says "I do not know X and Y."
(s2) S says "I knew you don't know X and Y."
(s3) P says "Now I know X and Y."
(s4) S says "Now I know X and Y too!"
What are X and Y?
"""

sum_cache = {}
prod_cache = {}


def isqrt(n):
    """
    Integer square root
    """

    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def sums(n):
    """
    Get all possible x, y with x<=y that add to n.

    eg. >>> get_sums(5) = [(2, 3),]
    eg. >>> get_sums(8) = [(2, 6), (3, 5), (4, 4),]
    """
    ret = set()
    for x in range(2, n//2 + 1):
        if n < 100:
            ret.add((x, n-x))
    return ret


def prods(n):
    """
    Get all possible x, y with x<=y that multiply to n.

    eg. >>> get_products(12) = [(2, 6), (3, 4) ]
    """
    limit = isqrt(n)
    ret = set()
    for x in range(2, limit + 1):
        if n % x == 0 and x + n//x < 100:
            ret.add((x, n//x))
    return ret


def s1(x,y):
    """ Return true iff x, y would allow s1 to be true"""
    p = x * y
    return len(prods(p)) > 1
    
    
def s2(x, y):
    s = x + y
    for i, j in sums(s):
        p = i * j
        if len(prods(p)) <= 1:
            return False
    return True


def s3(x, y):       
    p = x * y
    count = 0
    for a, b in prods(p):
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
        
# Generate the main test set
main_set = set()
N_MAX = 98
for y in range(2, N_MAX+1):
    for x in range(2, y+1):
        if x + y < 100:
            main_set.add((x, y))

# Possible values that P has after all the statements have been spoken
p_set = set()
for x, y in main_set:
    if s1(x, y) and s2(x, y) and s3(x, y) and s4(x, y):
        print(x, y)
