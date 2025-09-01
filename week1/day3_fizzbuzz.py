"""
This program implements the FizzBuzz game.
Write a program that prints numbers from 1 to 100, but:
        •	If the number is divisible by 3, print "Fizz" instead of the number.
        •	If the number is divisible by 5, print "Buzz".
        •	If the number is divisible by both 3 and 5, print "FizzBuzz".
        •	Otherwise, just print the number.
"""


def fizzbuzz(n: int) -> list:
    """
    prints fizzbuzz from 1 to n
    Args:
        n (int): The number to print fizzbuzz up to.
    Returns:
    """
    fizz_list = []
    for i in range(1, n):
        if i % 3 == 0 and i % 5 == 0:
            fizz_list.append("FizzBuzz")
        elif i % 3 == 0:
            fizz_list.append("Fizz")
        elif i % 5 == 0:
            fizz_list.append("Buzz")
        else:
            fizz_list.append(i)
    return fizz_list


# print(fizzbuzz(101))


class FizzBuzz:
    """
    Class to implement FizzBuzz game.
    """

    def __init__(self, num: int):
        self.num = num
        self.rules = {3: "Fizz", 5: "Buzz"}
        self.result = []

    def add_rule(self, divisor: int, word: str) -> None:
        """
        Add a new rule to the fizzbuzz game.
        Args:
            divisor (int): The divisor to check.
            word (str): The word to print if the number is divisible by the divisor.
        """
        self.rules[divisor] = word

    def generate(self) -> list:
        """
        Generate the fizzbuzz list.
        Returns:
            list: The fizzbuzz list.
        """
        for i in range(1, self.num + 1):
            output = ""
            for divisor, word in self.rules.items():
                if i % divisor == 0:
                    output += word
            self.result.append(output or i)
        return self.result


fizzbuzz_game = FizzBuzz(15)
fizzbuzz_game.add_rule(7, "Bazz")
print(fizzbuzz_game.generate())
