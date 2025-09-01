"""
The functions in this module checks if a number is prime or not.
"""

import math


def is_prime(num):
    """
    Check if a number is prime.

    Args:
        num (int): The number to check.
    Returns:
        bool: True if the number is prime else False.
    """
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


print(is_prime(11))
