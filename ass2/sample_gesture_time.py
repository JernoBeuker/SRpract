import random as rd

TIME_PER_SYLLABLE = 0.2

def random_gesture_syllable(min: int=3, max: int=10) -> float:
    # select a random syllable from [min, max], where min is the first syllable
    # after the last gesture that we can select
    rand_syllable = rd.randint(min, max)

    # convert n'th syllable to time in seconds
    return rand_syllable * TIME_PER_SYLLABLE
