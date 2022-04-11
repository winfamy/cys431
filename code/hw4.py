import math
import sympy
import random

def miller_rabin(n, t):
    p2 = 1
    while p2 < n:
        r = (n - 1) / p2
        if (r % 2 == 1):
            break
        
        r = 0
        p2 *= 2
    
    s = int(math.log2(p2))
    r = int(r)
    if (r == 0): 
        return -1
    for i in range(0, t):
        a = random.randint(2, n - 2)
        y = pow(a, r, n)
        if (y != 1 and y != n - 1):
            j = 1
            while j <= s - 1 and y != n - 1:
                y = pow(y, 2, n)
                if y == 1: 
                    return 0
                j += 1
            if (y != n - 1): 
                return 0
    return 1

for num in [17, 36, 43]: 
    result = miller_rabin(num, 1)
    print(f"{num} is " + ("" if result else "not ") + "prime")
