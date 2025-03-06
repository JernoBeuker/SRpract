import string
import random as rd

from config import TIME_PER_SYLLABLE

def count_syllables(text: str) -> int:
    """This function gets a string and outputs the number of syllables in the given text."""
    count = 0
    vowels = "aeiouy"
    vowel_pairs = ["ea", "io", "ou", "oa", "ie", "ue", "ay", "ey", "iy", "uy", "oy"]

    # remove all punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # for all words
    for word in text.split():
        # if a word starts with a vowel
        if word[0] in vowels:
            count += 1

        # start from the second letter in the word, so we can always check
        # the previous letter
        for idx in range(1, len(word)):
            # increase number of syllables for each set of vowels 
            # (e.g. 'a' or 'oa')
            if word[idx - 1 : idx + 1] in vowel_pairs:
                count += 1
                break

            if word[idx] in vowels and word[idx - 1] not in vowels:
                count += 1

        # cases where vowels don't count towards a syllable
        if len(word) > 2 and (word[-1] == "e" or word[-2:] == "ed"):
            count -= 1

        # a word cannot be 0 syllables
        if count == 0:
            count += 1
    return count

def random_gesture_syllable(min: int=3, max: int=10) -> float:
    """Selects a random number of syllables to wait for the next beat gesture 
    and calculates how much time it takes to say those beat gestures.
    It takes two arguments: min and max, which are inclusive boundries and default to 3 and 10 respectively."""
    # select a random syllable from [min, max], where min is the first syllable
    # after the last gesture that we can select
    rand_syllable = rd.randint(min, max)

    # convert n'th syllable to time in seconds
    return rand_syllable * TIME_PER_SYLLABLE