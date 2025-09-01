"""
Class called factorial to find the factorial of a number, 
In Two different apporaches "Iter" , "Recurisive".
"""


class Factorial:
    """
    Class to find the factorial of a number using iterative and recursive methods.
    """

    def __init__(self):
        pass

    def factorial_iter(self, num: int) -> int:
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

    def factorial_recur(self, num: int) -> int:
        """
        Find the factorial of the given number using recursion.
        Args:
            num (int): The number to find the factorial of.

        Returns:
            int: The factorial of the number.
        """
        if num in (0, 1):
            return 1
        return num * self.factorial_recur(num - 1)


factorial = Factorial()
print(factorial.factorial_iter(5))
print(factorial.factorial_recur(5))
