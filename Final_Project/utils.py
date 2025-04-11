from string import punctuation      # all punctuation symbols
import random as rd
import json

from config import TIME_PER_SYLLABLE, FILENAME

def save_dict(tasks: dict, filename=FILENAME) -> None:
    """saving the player dictionary"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def load_dict(filename: str=FILENAME) -> dict:
    """loading the player dictionary"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_syllables(text: str) -> int:
    """This function gets a string and outputs the number of syllables in the given text."""
    count = 0
    vowels = "aeiouy"
    vowel_pairs = ["ea", "io", "ou", "oa", "ie", "ue", "ay", "ey", "iy", "uy", "oy"]

    # remove all punctuation
    text = text.translate(str.maketrans('', '', punctuation))

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

            # increase number of syllables for single vowels
            if word[idx] in vowels and word[idx - 1] not in vowels:
                count += 1

        # cases where vowels don't count towards a syllable
        if len(word) > 2 and (word[-1] == "e" or word[-2:] == "ed"):
            count -= 1

        # a word cannot be 0 syllables (e.g. a sudo-word like "hmmm")
        if count == 0:
            count = 1

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

def filter_nouns(input_file: str, output_file: str) -> None:
    """filters the nouns of a given vocabulary file (input_file) and puts them
    in a new file. The output file (output_file) must exist (empty) beforehand"""

    # all nouns
    with open("words/allNouns.txt", 'r') as file:
        nouns = [word.strip() for word in file]

    # all words for a CEFR level
    with open(input_file, 'r') as level:
        words = [line.strip() for line in level]

    # all nouns in the given CEFR level wordlist
    cefr_nouns = [word for word in words if word in nouns]

    # writing the nouns of the CEFR level to the output file
    with open(output_file, 'a') as end_file:
        for noun in cefr_nouns:
            end_file.write(noun)
            end_file.write('\n')

def starting_prompt1(words: list) -> str:
    """LLM prompt when the user has to guess the robot's word"""

    return f"You are playing the game of taboo. Pick the simpelest noun in the following \
    list: {words} to keep in mind, dont say which one. I will \
    have to guess this word with yes or no questions. Do not explain the game. \
    Once I guessed the word, say: you guessed it, lets celebrate! \
    If I give up, say: okay we will stop. After you say what the word was."

def starting_prompt2(level: str) -> str:
    """LLM prompt when robot has to guess user's word"""

    return f"You are playing the game of taboo. I have a word in mind and \
    you have to guess it by asking me yes or no questions. Keep in mind that my level \
    of proficiency is {level} in English so base your questions on that. Only ask the \
    question, do not explain the game. Once I told you that you guessed the word, say: \
    Lets celebrate! If I want to give up or stop, say: okay we will stop."
