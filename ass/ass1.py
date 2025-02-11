from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
import os
import requests
from dotenv import load_dotenv

# Set up speech-to-text processor
audio_processor = SpeechToText()
audio_processor.silence_time = 1
audio_processor.silence_threshold2 = 100
audio_processor.logging = True

load_dotenv()
GEMINI_API_KEY = os.getenv("KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"

def call_gemini_api(prompt):
    """Calls Google Gemini API with the given prompt and returns the response."""
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"prompt": {"text": prompt}, "temperature": 0.7}
    
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("output", "")
    else:
        return "Sorry, I encountered an error."

@inlineCallbacks
def STT_continuous(session, response_time=1000):
    yield session.call("rom.sensor.hearing.sensitivity", 200)
    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.say", text="Say something")
    
    yield session.subscribe(audio_processor.listen_continues, "rom.sensor.hearing.stream")
    yield session.call("rom.sensor.hearing.stream")
    
    for _ in range(response_time):
        if not audio_processor.new_words:
            yield sleep(0.5)
        else:
            return audio_processor.give_me_words()
        audio_processor.loop()
    return None

def TTS(session, text):
    session.call("rie.dialogue.say", text=text)

def make_outputdir():
    os.makedirs("output", exist_ok=True)

def format_prompt(word_array):
    """Formats a structured prompt for the Taboo game."""
    return (f"You are the host of a Taboo game. The player must guess a word based on clues. "
            f"Do NOT use the forbidden words. Provide a hint in a conversational style.\n"
            f"Word to guess: {word_array[0]}\n"
            f"Forbidden words: {', '.join(word_array[1:])}")

@inlineCallbacks
def main(session, details):
    yield sleep(2)
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    make_outputdir()
    
    word_array = yield STT_continuous(session)
    if word_array:
        formatted_prompt = format_prompt(word_array)
        llm_response = call_gemini_api(formatted_prompt)
        yield TTS(session, llm_response)
    else:
        yield TTS(session, "I didn't hear anything. Try again.")
    
    session.leave()

wamp = Component(
    transports=[{"url": "ws://wamp.robotsindeklas.nl", "serializers": ["msgpack"], "max_retries": 0}],
    realm="rie.67a48c4e85ba37f92bb13c87",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])