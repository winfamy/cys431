import time
import math
import sympy
from random import randint
from prime_list import primes
from wrapt_timeout_decorator import *

def current_milli_time():
    return round(time.time() * 1000)

@timeout(2 * 60)
def isPrime_bruteforce(n, verbose=False):
    start = current_milli_time()
    i = 0
    cur_prime = primes[0]
    while (cur_prime < math.sqrt(n)):
        if (n % cur_prime == 0):
            end = current_milli_time()
            print(f"It took {(end - start) / 1000} seconds")
            print(f"Factor found: {cur_prime}\n")
            return True
        
        i += 1
        if i >= len(primes) - 1:
            cur_prime = sympy.nextprime(cur_prime)
        else:
            cur_prime = primes[i]
    return False

@timeout(2 * 60)
def factor_pollardsRho(x, n, verbose=False):
    start = current_milli_time()
    f = lambda f2: ((pow(f2, 2) + 1) % n)
    d = 1
    x2 = y2 = x
    while d == 1:
        x2 = f(x2)
        y2 = f(f(y2))
        d = sympy.gcd(abs(x2 - y2), n)
        if (verbose):
            print(f"({x2}, {y2}), gcd(|{x2}-{y2}|, {n}): {d}")
        # print(f"d gcd(|{x}-{y}|, {n}): {d}")

        if d > 1 and d < n:
            end = current_milli_time()
            if (verbose):
                print(f"d gcd(|{x2}-{y2}|, {n}): {d}")
            print(f"Found a factor: {d}")
            print(f"a = {x2}, b = {y2}")
            print(f"It took {(end - start) / 1000} seconds")
            return d
        
        if d == n:
            return -1

@timeout(2 * 60)
def factor_dixons(n, t, verbose=False):
    start = current_milli_time()
    eqns = []
    factor_base = primes[:t]
    k = 1
    while len(eqns) < t + 10:
        factors = {}
        x = randint(math.ceil(math.sqrt(n)), n)
        k += 1
        x2_mod_n = pow(x, 2, n)
        for factor in factor_base:
            while x2_mod_n % factor == 0:
                factors[factor] = factors.get(factor, 0) + 1
                x2_mod_n /= factor
        
        if x2_mod_n == 1:
            if (verbose):
                built_str = ""
                for factor in factors:
                    built_str += f"{factor}**{factors[factor]}*"
                print(f"[+] Equation Found: {x}^2 mod {n} ({pow(x, 2, n)}) = ({built_str[:-1]}) factored by {factors}")
            eqns.append([x, factors])

    good_eqns = []
    for eqn in eqns:
        factors = eqn[1]
        x = eqn[0]
        if len(list(filter(lambda f: factors[f] % 2 != 0, factors))) == 0:
            if (verbose):
                built_str = ""
                for factor in factors:
                    built_str += f"{factor}**{factors[factor]}*"
                print(f"[+] Good Equation Found: ({x})^2 mod {n} = {pow(x, 2, n)} = ({built_str[:-1]})^2 factored by {factors}")
            good_eqns.append([x, 1, factors])

        for eqn2 in eqns:
            y = int(eqn2[0])
            if x != y:
                bad = False
                factors_cp = factors.copy()
                factors_2 = eqn2[1]
                for factor in factors_2:
                    factors_cp[factor] = factors.get(factor, 0) + factors_2[factor]

                if len(list(filter(lambda f: factors_cp[f] % 2 != 0, factors_cp))) == 0:
                    if (verbose):
                        built_str = ""
                        for factor in factors_cp:
                            built_str += f"{factor}**{factors_cp[factor] // 2}*"
                        print(f"[+] Good Equation Found: ({x}*{y})^2 = ({x*y})^2 = ({built_str[:-1]})^2 factored by {factors_cp}")
                    good_eqns.append([x, y, factors_cp])
    
    for eqn in good_eqns:
        x = eqn[0] * eqn[1]
        y = 1
        factors = eqn[2]
        for factor in factors:
            y *= pow(factor, factors[factor] // 2)
        
        y = int(y)
        # print(abs(x-y), n, math.gcd(abs(x-y), n))
        gcd = math.gcd(abs(x-y), n)
        if (verbose):
            # print(f"GCD(| {x} - {y} |, {n}) = GCD({abs(x-y)}, {n}) = " + str(gcd))
            pass
        if gcd != 1 and gcd != n and gcd != None and gcd != 0:
            end = current_milli_time()
            print(f"GCD(|{x} - {y}|, {n}) = GCD({abs(x - y)}, {n}) = " + str(gcd))
            print(f"It took {(end - start) / 1000} seconds")
            return gcd
    print("Factor not found, try larger factor base")
    return -1 

            
if __name__ == "__main__":
    while True:
        print("PEX1 - Factoring - C1C Grady Phillips")
        verbose = input("Verbose mode (y/n): ")[0] in ['y', 'Y']
        num = input("Enter number: ")
        num = int(num)
        print('\nBrute Force')
        try:
            isPrime_bruteforce(num, verbose=verbose)
        except Exception as e:
            print(f"{e}")

        print('Pollard\'s-Rho')
        for i in range(0, 3):
            try:
                x = randint(2, num - 1)
                f = factor_pollardsRho(x, num, verbose=verbose)
                if f != -1:
                    print(f"Factor found: {f}\n")
                    break
            except Exception as e:
                print(f"{e}")
        
        print("Dixon's")
        for i in range(0, 3):
            try:
                factor_base = input("Enter number for factor base: ")
                factor_base = int(factor_base)
                f = factor_dixons(num, factor_base, verbose=verbose)
                if f != -1:
                    print(f"Factor found: {f}\n")
                    break
            except Exception as e:
                print(f"{e}")
