import os
import requests
from google import genai
from config import STARTING_PROMPT1, STARTING_PROMPT2, STARTING_TEXT, WHO_IS_WHAT, IMPORTANT_WORDS, SYLLABLES_TIL_GESTURE
from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
from alpha_mini_rug import perform_movement
from dotenv import load_dotenv
from gestures import NATURAL_POS, GESTURES, THINK_DEEPLY, CELEBRATE
import random as rd
from count_syllables import  count_syllables

load_dotenv()

GEMINI_API_KEY = os.getenv("KEY")

# setup a chat with GEMINI
client = genai.Client(api_key=GEMINI_API_KEY)
wow_chat = client.chats.create(model="gemini-2.0-flash")
important_words_chat = client.chats.create(model="gemini-2.0-flash")

@inlineCallbacks
def TTS(text):
    """Speaks the given text."""
    print(IMPORTANT_WORDS + text)
    important_words = call_gemini_api(important_words_chat, IMPORTANT_WORDS + text)
    if 'error' in important_words:
        print("error")
        return
    
    words = important_words.split()
    print(words)
    
    for word in words:
        idx = word.find(text)
    

def call_gemini_api(chat, prompt):
    """Calls Google Gemini API with the given prompt and returns the response."""
    response = chat.send_message(prompt)
    if response.text:
        return response.text
    else:
        return "Sorry, I encountered an error."

@inlineCallbacks
def main():
    prompt = ("In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since. Whenever you feel like criticizing any one, he told me, just remember that all the people in this world haven't had the advantages that you've had. ")
    
    TTS(prompt)
    
    
    # yield setup_session_STT()

    # # Asks if the user wants to play a game
    # yield asking_user_play_game()

    # # Asks the user if they want to think of a word or if the robot should think of a word, and returns the starting prompt for gemini
    # starting_prompt = yield asking_user_roles()
    # llm_response = yield call_gemini_api(wow_chat, starting_prompt)
    # yield TTS(session, llm_response)

    # while True:
    #     # get the spoken words of the user in an array
    #     word_array = yield STT_continuous(session)

    #     if word_array == None:  # could not get words from user
    #         yield TTS(session, "I didn't hear you, can you say that again?")
    #     elif word_array[-1] == "stop":  # if user decides to stop interacting
    #         break
    #     else:  # respond to the user
    #         llm_response = yield call_gemini_api(wow_chat, word_array[-1])
    #         yield TTS(session, llm_response)

    #     print(word_array[-1])

    # Leave the session appropriately

if __name__ == "__main__":
    main()
