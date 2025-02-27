import random as rd
import string

TIME_PER_SYLLABLE = 0.2

def random_gesture_syllable(min: int=3, max: int=10) -> None:
    rand_syllable = rd.randint(min, max)
    return rand_syllable * TIME_PER_SYLLABLE
