import os
import requests
from google import genai
from config import STARTING_PROMPT1, STARTING_PROMPT2, STARTING_TEXT, WHO_IS_WHAT
from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
from alpha_mini_rug import perform_movement
from dotenv import load_dotenv
from gestures import NATURAL_POS, GESTURES
import random as rd

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


def motion(session, frames: list):
    """Executes the movement with the given frames."""
    yield perform_movement(session,
        frames=frames,
        mode="linear",
        sync=True, 
        force=False
    )
    yield sleep(frames[-1]["time"] / 1000)

def TTS(session, text):
    """Speaks the given text."""
    yield session.call("rie.dialogue.say", text=text)

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
def STT_continuous(session, response_time=15):
    """By default, the robot waits 5 seconds for a response,
    returning None if no response is given"""
    for _ in range(response_time):
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("\t\t\t\tI am listening")
        else:
            return audio_processor.give_me_words()
        audio_processor.loop()
    return None

def asking_user_play_game(session):
    """Asks if the user wants to interact or not"""
    yield TTS(session, STARTING_TEXT)
    word_array = yield STT_continuous(session)
    print(word_array[-1])

    # the user does not want to interact
    if "no" in word_array[-1]:
        yield TTS(session, text="Okay, I am sad, but bye")
        session.leave()

def asking_user_roles():
    """Asking if the user wants to think of a word or if the robot should think of a word."""
    yield TTS(session, WHO_IS_WHAT)
    word_array = yield STT_continuous(session)
    print(word_array[-1])

    if "no" in word_array[-1]:
        yield TTS(session, text="Okay, I will think of a word now then")
        return STARTING_PROMPT1
    else:
        return STARTING_PROMPT2


@inlineCallbacks
def main(session, details):
    yield sleep(2)
    yield session.call("rom.optional.behavior.play", name="BlocklyCrouch")
    yield setup_session_STT()

    # Asks if the user wants to play a game
    yield asking_user_play_game()

    # Asks the user if they want to think of a word or if the robot should think of a word, and returns the starting prompt for gemini
    starting_prompt = yield asking_user_roles()
    llm_response = yield call_gemini_api(wow_chat, STARTING_PROMPT2)
    yield TTS(session, llm_response)

    while True:
        # get the spoken words of the user in an array
        word_array = yield STT_continuous(session)

        if word_array == None:  # could not get words from user
            yield TTS(session, "I didn't hear you, can you say that again?")
        elif word_array[-1] == "stop":  # if user decides to stop interacting
            break
        else:  # respond to the user
            llm_response = yield call_gemini_api(wow_chat, word_array[-1])
            yield TTS(session, llm_response)

        print(word_array[-1])

    # Leave the session appropriately
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
