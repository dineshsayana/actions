"""
This program counts the occurance of each word in a given text.
"""


def word_count(text: str) -> dict:
    """
    Count the occurance of each word in the given text.
    Args:
        text (str): The text to count the words in.
    Returns:
        dict: A dictionary with words as keys and their occurance as values.
    """

    words = text.split()
    word_freq = {}
    for word in words:
        word = word.lower().strip(".,!?;\"'()[]{}")
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    return word_freq


SAMPLE_TEXT = "Hello, world! Hello everyone. Welcome to the world of Python. Python is great," \
" and the world is beautiful."
print(word_count(SAMPLE_TEXT))
