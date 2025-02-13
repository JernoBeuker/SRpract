from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
import os
import requests
from google import genai

# Set up speech-to-text processor

audio_processor = SpeechToText()
audio_processor.silence_time = 1
audio_processor.silence_threshold2 = 200
audio_processor.logging = False

GEMINI_API_KEY = "AIzaSyAKNvPSqM18woLY83IWlYUnf9oDF2R8X_c"
STARTING_PROMPT1 = "You are playing the game of taboo. Think of a word. I will \
    have to guess this word with yes or no questions. Only think of the word \
    and answer the questions with a yes or no, do not explain the game"

STARTING_PROMPT2 = "You are playing the game of taboo. I have a word in mind and \
    you have to guess it by asking me yes or no questions. Only ask the question, \
    do not explain the game"
STARTING_TEXT = "Do you want to play a game of Taboo? If you ever want to stop the \
    game, just say the word stop."

WHO_IS_WHAT = "Do you want to start with thinking of a word?"
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
def STT_continuous(session, response_time=15, start=False):
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
            return audio_processor.give_me_words()
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
    print(word_array[-1])
    if 'no' in word_array[-1]:
        yield TTS(session, text='Okay, I am sad, but bye')
        session.leave()
        
    yield TTS(session, WHO_IS_WHAT)
    word_array = yield STT_continuous(session, start=True)
    print(word_array)
    print(word_array[-1])
    if 'no' in word_array[-1]:
        TTS(session, text='Okay, I will think of a word now then')
        llm_response = yield call_gemini_api(STARTING_PROMPT1)
    else:
        llm_response = yield call_gemini_api(STARTING_PROMPT2)
    yield TTS(session, llm_response)

    while True:
        word_array = yield STT_continuous(session)
        print(word_array)
        print(word_array[-1])
        if word_array[-1] == 'stop':
            break
        elif word_array[-1] != None:
            llm_response = yield call_gemini_api(word_array[-1])
            yield TTS(session, llm_response)
        else:
            yield TTS(session, "I didn't hear anything. Try the game again.")
    
    session.leave()

wamp = Component(
    transports=[{"url": "ws://wamp.robotsindeklas.nl", "serializers": ["msgpack"], "max_retries": 0}],
    realm="rie.67adc33985ba37f92bb17021",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])