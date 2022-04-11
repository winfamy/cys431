from sympy import isprime

print("N: ", end='')
n = int(input())
a = 5

for i in range(1, n):
	if (pow(a, i - 1, i) == 1):
		if (isprime(i)):
			print(f"{i} Fermat Pseudoprime")
		else:
			print(f"{i} *** Fermat Pseudoprime but not Prime ***")
	else:
		print(i)
