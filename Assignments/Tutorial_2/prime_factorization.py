from math import sqrt, floor
from primes import check_prime

def prime_factorization(n):
    factorization = []

    # edge case
    if n == 1:
        return [1]

    # slightly suboptimal because of repeated check for factors in check_prime(n)
    # and the same check in the contained for loop
    while not check_prime(n):
        for i in range(2, int(floor(sqrt(n)))+1):
            if n % i == 0:
                n /= i
                factorization.append(i)
                break

    factorization.append(n) # add final factor to list

    return factorization

if __name__ == "__main__":
    assert prime_factorization(1) == [1]
    assert prime_factorization(2) == [2]
    assert prime_factorization(10) == [2,5]
    assert prime_factorization(91) == [7,13]
    assert prime_factorization(120) == [2,2,2,3,5]
    assert prime_factorization(1024) == [2,2,2,2,2,2,2,2,2,2]