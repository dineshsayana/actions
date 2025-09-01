"""
This functions find the factorial of a number, In Two different apporaches "Iter" , "Recurisive".
"""


def factorial_iter(num: int) -> int:
    """
    Find the factorial of the given number
    Args:
        num (int): The number to find the factorial of.

    Returns:
        int: The factorial of the number.
    """
    result = 1
    for i in range(1, num + 1):
        result *= i

    return result


def factorial_recur(num: int) -> int:
    """
    Find the factorial of the given number using recursion.
    Args:
        num (int): The number to find the factorial of.

    Returns:
        int: The factorial of the number.
    """
    if num in (0, 1):
        return 1
    return num * factorial_recur(num - 1)


print(factorial_iter(5))
print(factorial_recur(5))
