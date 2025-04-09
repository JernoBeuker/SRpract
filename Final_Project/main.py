# alpha-mini imports
from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
from alpha_mini_rug import perform_movement

import os                           # to go through the file system
from dotenv import load_dotenv      # to load the .env file
from google import genai            # to interact with gemini
import random as rd                 # to select randomly

# our utility functions
from utils import count_syllables, random_gesture_syllable, save_dict, load_dict, starting_prompt1, starting_prompt2
import config as cf                 # our prompts, gestures and other global variables

load_dotenv()

REALM = 'rie.' + os.getenv("REALM")
GEMINI_API_KEY = os.getenv("KEY")

# set up speech-to-text processor
audio_processor = SpeechToText()
audio_processor.silence_time = 1  # time of allowed silence after speech
audio_processor.silence_threshold2 = 200  # lower -> robot picks up dimmer sounds
audio_processor.logging = False

# setup a chat with GEMINI
client = genai.Client(api_key=GEMINI_API_KEY)
wow_chat = client.chats.create(model="gemini-2.0-flash")

@inlineCallbacks
def motion(session, frames: list):
    """Executes the movement with the given frames."""
    yield perform_movement(
        session,
        frames=frames,
        mode="linear",
        sync=True, 
        force=True
    )
    yield sleep(frames[-1]["time"] / 1000)

@inlineCallbacks
def TTS(session, text):
    """Speaks the given text."""
    # calculate how long it will take to speak the text
    duration = count_syllables(text) * cf.TIME_PER_SYLLABLE

    # start speech
    session.call("rie.dialogue.say", text=text)

    time = 0
    # while there is time to do a gesture
    while time < duration - cf.GESTURE_TIME:

        # get a time after which we will do a gesture
        sleep_time = random_gesture_syllable(min=2, max=8)

        # update the "current time" by how long we will wait plus how long
        # the gesture will be
        time += sleep_time + cf.GESTURE_TIME

        # wait to do the gesture
        yield sleep(sleep_time)

        # do a random gesture from the list of beat-gestures
        yield motion(session, rd.choice(cf.GESTURES))

@inlineCallbacks
def setup_session_STT(session):
    """Making sure the session and the audio processor are set up for speech-to-text."""
    yield session.call("rom.sensor.hearing.sensitivity", 1400)
    yield session.call("rie.dialogue.config.language", lang="en")

    yield session.subscribe(
        audio_processor.listen_continues, "rom.sensor.hearing.stream"
    )
    yield session.call("rom.sensor.hearing.stream")

def call_gemini_api(chat, prompt):
    """Calls Google Gemini API with the given prompt and returns the response."""
    response = chat.send_message(prompt)
    if response.text:
        return response.text
    else:
        return "Sorry, I encountered an error."

@inlineCallbacks
def STT_continuous(session, response_time=10):
    """By default, the robot waits 5 seconds for a response,
    returning None if no response is given"""
    audio_processor.do_speech_recognition = True

    # listen for 5 seconds
    for _ in range(response_time):
        if not audio_processor.new_words:
            yield sleep(0.5)
        else:
            # stop listening
            audio_processor.do_speech_recognition = False

            # return most confidently heard speech
            return audio_processor.give_me_words()[-1][0]
        audio_processor.loop()
    return None

@inlineCallbacks
def asking_user_play_game(session):
    """Asks if the user wants to interact or not"""
    # ask if the user wants to play Taboo
    yield TTS(session, cf.STARTING_TEXT)
    word_array = yield STT_continuous(session)

    # if no response was registered
    while not word_array:
        yield TTS(session, "I didn't hear you, can you say that again?")
        word_array = yield STT_continuous(session)

    # the user does not want to interact
    if "no" in word_array:
        yield session.call("rom.optional.behavior.play", name="BlocklyCrouch")
        yield TTS(session, text="Okay, I am sad, but bye")
        session.leave()

@inlineCallbacks
def asking_user_roles(session, player_stats: dict):
    """Asking if the user wants to think of a word or if the robot should think of a word."""
    # asking user if they want to start thinking of a word
    yield TTS(session, cf.WHO_IS_WHAT)
    word_array = yield STT_continuous(session)

    # match user "knowledge probability" to CEFR level
    for prob_range, cefr_level in cf.KNOWLEDGE_TO_LEVEL.items():
        if round(player_stats['stats']['knowledge_state']) in prob_range:

            # if user does not want to start thinking of a word
            if "no" in word_array:
                yield TTS(session, text="Okay, I will think of a word now then")

                # wordlist for user's CEFR level
                with open(f"words/{cefr_level}.txt", 'r') as wordlist_file:
                    cefr_words = [word.strip() for word in wordlist_file]

                # sample 5 random words from the wordlist
                random_words = rd.sample(cefr_words, 5)

                # return appropriate LLM prompt
                return starting_prompt1(random_words)

            # if user wants to start with thinking of a word
            else:
                # return appropriate LLM prompt
                return starting_prompt2(cefr_level)

@inlineCallbacks
def get_stats_player(session):
    players_dict = load_dict()

    # asking user for their name
    yield TTS(session, cf.GETTING_USER_NAME)
    response = yield STT_continuous(session)

    # if no response was registered
    while not response:
        yield TTS(session, "I didn't hear you, can you say that again?")
        response = yield STT_continuous(session)

    # extract user name from response
    response = cf.NAME_FROM_STRING + response
    name = yield call_gemini_api(wow_chat, response.strip())

    # if the user is already registered
    if name in players_dict:
        return players_dict[name]

    # new user
    else:
        player = cf.STANDARD_PLAYER
        player["name"] = name
        return player

def calculate_BKT(player: dict, gamestate: dict, 
                  p_T_win: float=0.1, p_T_loss: float=-0.05) -> dict:

    # prior knowledge state of the user
    p_L = player["stats"]["knowledge_state"] / 100.0  

    # Determine probability transition based on game outcome
    p_T = p_T_loss if gamestate["winner"] == "bot" else p_T_win

    # Compute updated knowledge state using BKT formula
    new_p_L = p_L + (1 - p_L) * p_T
    
    # set hard limits on the range [0, 1]
    if new_p_L < 0:
        new_p_L = 0
    elif new_p_L > 1:
        new_p_L = 1

    # Convert back to 0-100 scale
    player["stats"]["knowledge_state"] = round(new_p_L * 100, 2)
    return player

def save_player_progress(player_stats: dict, game_state: dict) -> None:
    # increase games played
    player_stats["stats"]["games_played"] += 1

    # add a won game for the user
    if game_state["winner"] == "user":
        player_stats["stats"]["games_won"] += 1

    # update user knowledge state with bayesian knowledge tracing
    player_stats = calculate_BKT(player_stats, game_state)
    
    # update the users stats in the players-dictionary
    players_dict = load_dict()
    players_dict[player_stats["name"]] = player_stats
    save_dict(players_dict)

def game_setup(session):
    """setting up the wow game before we enter the gameplay loop"""

    # Asks if the user wants to play a game
    yield asking_user_play_game(session)

    # get the user's information
    player_stats = yield get_stats_player(session)

    # Asks the user what role they would like to play and prompt gemini accordingly
    starting_prompt = yield asking_user_roles(session, player_stats)
    llm_response = yield call_gemini_api(wow_chat, starting_prompt)
    yield TTS(session, llm_response)

    return player_stats

@inlineCallbacks
def game_loop(session, game_state):
    while True:
        # get the spoken words of the user in an array
        word_array = yield STT_continuous(session)

        # if no response was registered
        if not word_array:
            yield TTS(session, "I didn't hear you, can you say that again?")
        else:
            # response to the user
            llm_response = yield call_gemini_api(wow_chat, word_array)

            # robot saying the response with a 30% chance of performing 
            # iconic "eureka" gesture
            if rd.randint(0, 10) < 3:
                yield motion(session, cf.EUREKA)
                yield session.call("rie.dialogue.say", text=llm_response)
            else:
                yield TTS(session, llm_response)

            # the word has been guessed
            if "celebrate" in llm_response:
                game_state['winner'] = "user"
                yield motion(session, cf.CELEBRATE)
                yield sleep(2)
                break

            # user gives up
            elif "stop" in llm_response:
                game_state['winner'] = "bot"
                yield sleep(2)
                break

    return game_state


@inlineCallbacks
def main(session, details):
    # Initialize the session
    yield sleep(2)
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sleep(2)
    yield motion(session, cf.NATURAL_POS)
    yield sleep(1)
    
    # Determine what variant of the game to play and setup player
    yield setup_session_STT(session)
    player_stats = yield game_setup(session)
    
    # Perform the main game loop
    game_state = {'winner': None}
    game_state = yield game_loop(session, game_state)

    # Leave the session
    save_player_progress(player_stats, game_state)
    yield sleep(1)
    yield session.call("rom.optional.behavior.play", name="BlocklyCrouch")
    session.leave()

wamp = Component(
    transports=[
        {
            "url": "ws://wamp.robotsindeklas.nl",
            "serializers": ["msgpack"],
            "max_retries": 0,
        }
    ],
    realm=REALM,
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
