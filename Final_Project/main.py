import os
from google import genai
import config as cf
from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
from alpha_mini_rug import perform_movement
from dotenv import load_dotenv
import random as rd
from utils import count_syllables, random_gesture_syllable, save_dict, load_dict

load_dotenv()

REALM = os.getenv("REALM")
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

def setup_session_STT(session):
    """Making sure the session and the audio processor are set up for speech-to-text."""
    yield session.call("rom.sensor.hearing.sensitivity", 1400)
    yield session.call("rie.dialogue.cf.language", lang="en")

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
def STT_continuous(session, response_time=15):
    """By default, the robot waits 5 seconds for a response,
    returning None if no response is given"""
    audio_processor.do_speech_recognition = True
    for _ in range(response_time):
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("\t\t\t\tI am listening")
        else:
            audio_processor.do_speech_recognition = False
            return audio_processor.give_me_words()
        audio_processor.loop()
    return None

def asking_user_play_game(session):
    """Asks if the user wants to interact or not"""
    yield TTS(session, cf.STARTING_TEXT)
    word_array = yield STT_continuous(session)

    # the user does not want to interact
    if "no" in word_array[-1]:
        yield TTS(session, text="Okay, I am sad, but bye")
        session.leave()

def asking_user_roles(session, player_stats: dict):
    """Asking if the user wants to think of a word or if the robot should think of a word."""
    yield TTS(session, cf.WHO_IS_WHAT)
    word_array = yield STT_continuous(session)

    if "no" in word_array[-1]:
        yield TTS(session, text="Okay, I will think of a word now then")

        for key, cefr_level in cf.KNOWLEDGE_TO_LEVEL.items():
            if player_stats['stats']['knowledge_state'] in key:

                with open(f"words/{cefr_level}.txt", 'r') as wordlist_file:
                    cefr_words = [word.strip() for word in wordlist_file]

                random_words = rd.sample(cefr_words, 5)
                cf.words = random_words

                return cf.STARTING_PROMPT1

    else:
        for key, cefr_level in cf.KNOWLEDGE_TO_LEVEL.items():
            if player_stats['stats']['knowledge_state'] in key:
                cf.level = cefr_level
                return cf.STARTING_PROMPT2


@inlineCallbacks
def get_stats_player(session):
    players_dict = load_dict()

    yield TTS(session, cf.GETTING_USER_NAME)
    response = yield STT_continuous(session)
    name = yield call_gemini_api(wow_chat, cf.NAME_FROM_STRING + response)

    if name in players_dict:
        return players_dict[name]
    else:
        player = cf.STANDARD_PLAYER
        player["name"] = name
        return player

def calculate_BKT(player, gamestate, p_T_win=0.1, p_T_loss=0.02):
    p_L = player["stats"]["knowledge_state"] / 100.0  

    # Determine probability transition based on game outcome
    p_T = p_T_win
    if gamestate["winner"] == "bot":
        p_T = p_T_loss  # Lower learning probability on failure

    # Compute updated knowledge state using BKT formula
    new_p_L = p_L + (1 - p_L) * p_T

    # Convert back to 0-100 scale
    player["stats"]["knowledge_state"] = round(new_p_L * 100, 2)
    
    return player

def save_player_progress(player_stats:dict, game_state:dict):
    player_stats["stats"]["games_played"] += 1
    if game_state["winner"] == "user":
        player_stats["stats"]["games_won"] += 1
    
    player_stats = calculate_BKT(player_stats, game_state)
    
    players_dict = load_dict()
    players_dict[player_stats["name"]] = player_stats
    save_dict(players_dict)

def game_setup(session):
    """setting up the wow game before we enter the gameplay loop"""

    # Asks if the user wants to play a game
    yield asking_user_play_game(session)

    player_stats = yield get_stats_player(session)

    # Asks the user if they want to think of a word or if the robot should
    # think of a word, and returns the starting prompt for gemini
    starting_prompt = yield asking_user_roles(session, player_stats)
    llm_response = yield call_gemini_api(wow_chat, starting_prompt)
    yield TTS(session, llm_response)

    return player_stats

def game_loop(session, game_state):
    while game_state['winner'] != None:
        # get the spoken words of the user in an array
        word_array = yield STT_continuous(session)

        if word_array == None:  # could not get words from user
            yield TTS(session, "I didn't hear you, can you say that again?")
        elif word_array[-1] == "stop":  # if user decides to stop interacting
            game_state['winner'] = "bot"
            return game_state
        else:  # respond to the user
            llm_response = yield call_gemini_api(wow_chat, word_array[-1])

            if rd.randint(0,10) < 3:
                yield motion(session, cf.EUREKA)
                yield session.call("rie.dialogue.say", text=llm_response)
            else:
                yield TTS(session, llm_response)

            #Ending the game
            if "celebrate" in llm_response:
                game_state['winner'] = "user"
                yield motion(session, cf.CELEBRATE)
                yield sleep(2)
                return game_state


@inlineCallbacks
def main(session, details):
    yield sleep(2)
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield motion(session, cf.NATURAL_POS)
    yield sleep(1)

    yield setup_session_STT(session)
    player_stats = game_setup(session)

    game_state = {
        'winner': None
    }

    game_state = game_loop(session, game_state)

    # Leave the session appropriately
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
