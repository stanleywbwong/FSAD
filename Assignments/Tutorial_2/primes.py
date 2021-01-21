from math import sqrt, floor    # no need to import everything

def primes(n):
    return [num for num in range(1, n+1) if check_prime(num)]

def check_prime(num):
    # edge case
    if num == 1:
        return False

    # small runtime optimization, only check for factors up to floor of sqrt
    for i in range(2, int(floor(sqrt(num)))+1):
        if num % i == 0:
            return False

    return True

# basic driver code to test
if __name__ == "__main__":
    assert primes(0) == []
    assert primes(1) == []
    assert primes(10) == [2,3,5,7]
    assert primes(11) == [2,3,5,7,11]
    assert primes(100) == [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]