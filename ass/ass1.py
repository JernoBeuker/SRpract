from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
import os
import requests
from dotenv import load_dotenv
from google import genai

# Set up speech-to-text processor

audio_processor = SpeechToText()
audio_processor.silence_time = 0.5
audio_processor.silence_threshold2 = 200
audio_processor.logging = False

load_dotenv()
GEMINI_API_KEY = os.getenv("KEY")
STARTING_PROMPT = "You are playing the game of taboo. I have a word in mind and you have to guess it by asking me yes or no questions. Only ask the question, do not explain the game"
STARTING_TEXT = "Do you want to play a game of Taboo? If you ever want to stop the game, just say the word stop."
client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(model='gemini-2.0-flash')

def call_gemini_api(prompt):
    """Calls Google Gemini API with the given prompt and returns the response."""
    
    response = chat.send_message(prompt)
    if response.text:
        return response.text
    else:
        return "Sorry, I encountered an error."

@inlineCallbacks
def STT_continuous(session, response_time=10, start=False):
    print("\t\t\t\t\t\t\t\tStarting to listen")
    if start:
        yield session.call("rom.sensor.hearing.sensitivity", 1400)
        yield session.call("rie.dialogue.config.language", lang="en")
        
        yield session.subscribe(audio_processor.listen_continues, "rom.sensor.hearing.stream")
        yield session.call("rom.sensor.hearing.stream")

    print(start)
    for _ in range(response_time):
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("\t\t\t\tI am listening")
        else:
            return audio_processor.give_me_words()[-1]
        audio_processor.loop()
    return None

def TTS(session, text):
    yield session.call("rie.dialogue.say", text=text)

def make_outputdir():
    os.makedirs("output", exist_ok=True)

@inlineCallbacks
def main(session, details):
    yield sleep(2)
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    make_outputdir()
    

    yield TTS(session, STARTING_TEXT)
    word_array = yield STT_continuous(session, start=True)
    print(word_array)

    if 'no' in word_array:
        TTS(session, text='Okay, I am sad, but bye')
        session.leave()

    llm_response = yield call_gemini_api(STARTING_PROMPT)
    yield TTS(session, llm_response)

    while True:
        word_array = yield STT_continuous(session)
        print(word_array)
        if word_array == 'stop':
            break
        elif word_array:
            llm_response = yield call_gemini_api(word_array)
            yield TTS(session, llm_response)
        else:
            yield TTS(session, "I didn't hear anything. Try the game again.")
    
    session.leave()

wamp = Component(
    transports=[{"url": "ws://wamp.robotsindeklas.nl", "serializers": ["msgpack"], "max_retries": 0}],
    realm="rie.67ab212b85ba37f92bb16124",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])