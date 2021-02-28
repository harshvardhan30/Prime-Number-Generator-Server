"""
WSGI config for server1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server1.settings')

application = get_wsgi_application()
# limiter, to avoid accidentally use very large number which will take a long time
MAX_LIMIT = 10 ** 6


def generateSmallPrimeNumbers(n):
    # limiter, to avoid accidentally use very large number which will take a long time
    MAX_LIMIT = 10 ** 6
    if 2 > n:
        return []
    elif 2 == n:
        return [2]
    elif 3 == n:
        return [2, 3]
    elif n > MAX_LIMIT:
        # max limit
        n = MAX_LIMIT

    method = 2
    if method == 1:
        return _generateSmallPrimes_1_brute(n)
    else:
        return _generateSmallPrimes_2_limiter(n)


def _generateSmallPrimes_1_brute(n):
    # init prime list, init with first and second prime (2 and 3)
    primes = [2, 3]

    # from 5 to n, step=2, eg: 5,7,9,11,13,15,etc.

    # include n
    limit = n + 1
    for v in range(5, limit, 2):

        sqrt_limit = int(v ** 0.5) + 1

        # do small-prime divisions
        # starting from second index (3) to current total primes
        # NOTE: skip division by 2 because no even value

        isPrime = True
        for j in range(1, len(primes)):
            prime = primes[j]
            if prime > sqrt_limit:
                break
            if v % prime == 0:
                isPrime = False
                break

        if isPrime:
            primes.append(v)

    return primes


def _generateSmallPrimes_2_limiter(n):
    # init prime list, init with first and second prime (2 and 3)
    primes = [2, 3]

    # init limiter variables
    primeArrayIndexLimit = 1
    maxValueWithLimit = primes[primeArrayIndexLimit] ** 2

    # next number to check
    v = 5

    # loop until reached the final value
    while n >= v:

        # avoid overshoot
        if maxValueWithLimit > n:
            maxValueWithLimit = n + 1  # + 1 to include 'n'

        # get value to check, only for ODD values, eg: 5,7,9,11,13,15,17,etc.
        for v in range(v, maxValueWithLimit, 2):

            isPrime = True

            # divide by existing small primes, skip first prime (because v always ODD !!, primes[0] == 2)
            for i in range(1, primeArrayIndexLimit):
                if v % primes[i] == 0:
                    isPrime = False
                    break

            if isPrime:
                primes.append(v)

        # increase v to avoid double check same v
        v += 2

        # update limiter
        primeArrayIndexLimit += 1
        maxValueWithLimit = primes[primeArrayIndexLimit] ** 2

    return primes


######## TESTING generate prime numbers with small value ##########

if __name__ == '__main__':
    import time

    n = 113  # 1000000

    time_start = time.time()
    primes = generateSmallPrimeNumbers(n)
    time_end = time.time()

    print('generate prime up to ', n, 'total primes: ', len(primes))
    print('elapsed time ', format(time_end - time_start, '.3f'), ' seconds')
    print(primes)

