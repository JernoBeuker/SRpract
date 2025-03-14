import random as rd

level = ""
words = []

STARTING_PROMPT1 = f"You are playing the game of taboo. Pick the easiest word \
    in the following list for you to keep in mind: {words}. I will \
    have to guess this word with yes or no questions. Only think of the word \
    and answer the questions with a yes or no, do not explain the game. Once \
    I guessed the word, say: you guessed it, lets celebrate!"

STARTING_PROMPT2 = f"You are playing the game of taboo. I have a word in mind and \
    you have to guess it by asking me yes or no questions. Keep in mind that my level \
    of proficiency is {level} in English so base your questions on that. Only ask the \
    question, do not explain the game. Once I told you that you guessed the word, say: \
    Lets celebrate!"

STARTING_TEXT = "Do you want to play a game of Taboo? If you ever want to give up and \
                stop the game, just say the word stop."

WHO_IS_WHAT = "Do you want to start with thinking of a word?"

IMPORTANT_WORDS = "Hello, for the following sentence, I need a robot to make hand gestures. \
    I want these gestures to match the important words of the sentence, can you \
    give me the important words of the sentence? Do only a couple a sentence \
    Only answer with the keywords, do not put them in bulletpoints. The sentence is: "

NAME_FROM_STRING = "Can you find the name in the following text, only respond with the name: "

SYLLABLES_TIL_GESTURE = 5
TIME_PER_SYLLABLE = 0.2

GETTING_USER_NAME = "I will be glad to play a game with you. What is your name?"

GESTURE_TIME = 1.6
SYLLABLES_TIL_GESTURE = 5
TIME_PER_SYLLABLE = 0.2

CEFR_LEVELS = ("a1", "a2", "b1", "b2", "c1")

KNOWLEDGE_TO_LEVEL = {
    tuple(range(0, 20)): CEFR_LEVELS[0],
    tuple(range(20, 40)): CEFR_LEVELS[1],
    tuple(range(40, 60)): CEFR_LEVELS[2],
    tuple(range(60, 80)): CEFR_LEVELS[3],
    tuple(range(80, 100)): CEFR_LEVELS[4]
}

STANDARD_PLAYER = {
    "name": "",
    "stats": {
        "games_played": 0,
        "games_won": 0,
        "knowledge_state": 30
    }
}

# --------------------------------------------Gestures------------------------------------------

LH_NATURAL = {"body.arms.left.lower.roll": -0.6,"body.arms.left.upper.pitch": -0.1}
RH_NATURAL = {"body.arms.right.lower.roll": -0.6,"body.arms.right.upper.pitch": -0.1}
HEAD_NATURAL = {"body.head.roll": 0, "body.head.pitch": 0, "body.head.yaw": 0}

FRAMES_RH_GESTURE = [
            {"time": 400, "data": RH_NATURAL},
            {"time": 1000, "data": {"body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0,7)}},
            {"time": 1600, "data": RH_NATURAL}
            ]

FRAMES_LH_GESTURE = [
        	{"time": 400, "data": LH_NATURAL},
            {"time": 1000, "data": {"body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL}
            ]

FRAMES_LH_RH_GESTURE = [
        	{"time": 400, "data": LH_NATURAL | RH_NATURAL},
            {"time": 1000, "data": {"body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL | RH_NATURAL}
            ]

FRAMES_HEAD_L_GESTURE = [
            {"time": 400, "data": HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(-0.3, -0.1),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0}},
            {"time": 1600, "data": HEAD_NATURAL}
            ]

FRAMES_HEAD_R_GESTURE = [
            {"time": 400, "data": HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0}},
            {"time": 1600, "data": HEAD_NATURAL}
            ]

FRAMES_LEFT_HEAD_GESTURE = [
            {"time": 400, "data": LH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(-0.3, -0.1),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL | HEAD_NATURAL}
            ]

FRAMES_RIGHT_HEAD_GESTURE = [
            {"time": 400, "data": RH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": RH_NATURAL | HEAD_NATURAL}
            ]

FRAMES_LEFT_HEAD_GESTURE2 = [
            {"time": 400, "data": LH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.left.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.left.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": LH_NATURAL | HEAD_NATURAL}
            ]

FRAMES_RIGHT_HEAD_GESTURE2 = [
            {"time": 400, "data": RH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(-0.3, -0.1),
                                    "body.head.yaw": 0,
                                    "body.head.pitch": 0,
                                    "body.arms.right.lower.roll": rd.uniform(-1.6, -1.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-0.9, -0.7)}},
            {"time": 1600, "data": RH_NATURAL | HEAD_NATURAL}
            ]

# Iconic gestures
CELEBRATE = [
        	{"time": 0, "data": LH_NATURAL | RH_NATURAL | {"body.torso.yaw": 0}},
            {"time": 1000, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(-0.5, -0.3)}},
            {"time": 1600, "data": {"body.arms.left.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.left.upper.pitch": rd.uniform(-2.1, -1.9), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9),
                                    "body.torso.yaw": rd.uniform(-0.9, -0.7)}},
            {"time": 2200, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(-0.5, -0.3)}},
            {"time": 2800, "data": {"body.arms.left.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.left.upper.pitch": rd.uniform(-2.1, -1.9), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9),
                                    "body.torso.yaw": 0}},
            {"time": 3400, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(0.3, 0.5),}},
            {"time": 4000, "data": {"body.arms.left.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.left.upper.pitch": rd.uniform(-2.1, -1.9), 
                                    "body.arms.right.lower.roll": rd.uniform(-1.1, -0.9),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9),
                                    "body.torso.yaw": 0.8}},
            {"time": 4600, "data": {"body.arms.left.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.left.upper.pitch": rd.uniform(-3.6, -3.4), 
                                    "body.arms.right.lower.roll": rd.uniform(-0.3, -0.1),
                                    "body.arms.right.upper.pitch": rd.uniform(-3.6, -3.4),
                                    "body.torso.yaw": rd.uniform(0.3, 0.5),}},
            {"time": 5600, "data": LH_NATURAL | RH_NATURAL | {"body.torso.yaw": 0}}
            ]

EUREKA = [
            {"time": 0, "data": RH_NATURAL | HEAD_NATURAL},
            {"time": 1000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": -1.4,
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 1400, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": rd.uniform(-1,8, -1.6),
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 2000, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": -1.4,
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 2600, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": rd.uniform(-1,8, -1.6),
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 3200, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": -1.4,
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 3800, "data": {"body.head.roll": rd.uniform(0.1, 0.3),
                                    "body.head.yaw": rd.uniform(-0,6, -0.4),
                                    "body.head.pitch": rd.uniform(0.3, 0.5),
                                    "body.arms.right.lower.roll": rd.uniform(-1,8, -1.6),
                                    "body.arms.right.upper.pitch": rd.uniform(-1,4, -1.2)}},
            {"time": 4400, "data": {"body.head.roll": 0.0,
                                    "body.head.yaw": 0.0,
                                    "body.head.pitch": rd.uniform(-0,4, -0.2),
                                    "body.arms.right.lower.roll": rd.uniform(-0,6, -0.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9)}},
            {"time": 5000, "data": {"body.head.roll": 0.0,
                                    "body.head.yaw": 0.0,
                                    "body.head.pitch": rd.uniform(-0,4, -0.2),
                                    "body.arms.right.lower.roll": rd.uniform(-0,6, -0.4),
                                    "body.arms.right.upper.pitch": rd.uniform(-2.1, -1.9)}},
            {"time": 5600, "data": RH_NATURAL | HEAD_NATURAL}
            ]

GESTURES = [
    FRAMES_RH_GESTURE, 
    FRAMES_LH_GESTURE, 
    FRAMES_LH_RH_GESTURE, 
    FRAMES_HEAD_L_GESTURE,
    FRAMES_HEAD_R_GESTURE,
    FRAMES_LEFT_HEAD_GESTURE, 
    FRAMES_RIGHT_HEAD_GESTURE, 
    FRAMES_LEFT_HEAD_GESTURE2, 
    FRAMES_RIGHT_HEAD_GESTURE2
]

NATURAL_POS = [{"time": 400, "data": LH_NATURAL | RH_NATURAL | HEAD_NATURAL}]