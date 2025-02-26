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

TIME_PER_SYLLABLE = 0.2

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
important_words_chat = client.chats.create(model="gemini-2.0-flash")

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
    starting_gesture_times = []
    important_words = call_gemini_api(important_words_chat, IMPORTANT_WORDS + text).split()
    print(important_words)
    print(text)
    
    idx = 0
    end_time_gesture = 0
    for word in important_words:
        word = word[:len(word)-1]
        idx = text.find(word, idx)
        print(idx, word)
        
        print(count_syllables(text[:idx]))
        start_gesture_word = (count_syllables(text[:idx]) * TIME_PER_SYLLABLE) - 1
        
        if start_gesture_word > 0 and start_gesture_word > end_time_gesture:
            starting_gesture_times.append(start_gesture_word)
            end_time_gesture = start_gesture_word + 1.6
        
    session.call("rie.dialogue.say", text=text)
    
    print("perform gestures")
    print(starting_gesture_times)
    
    time = 0
    for item in starting_gesture_times:
        yield sleep(item-time)
        time = item + 1.6
        yield motion(session, rd.choice(GESTURES))
        
    time_text = count_syllables(text) * TIME_PER_SYLLABLE
    yield sleep(time_text - (starting_gesture_times[-1] + 1.6))

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
    yield TTS(session, STARTING_TEXT)
    word_array = yield STT_continuous(session)
    print(word_array[-1])

    # the user does not want to interact
    if "no" in word_array[-1]:
        yield TTS(session, text="Okay, I am sad, but bye")
        session.leave()

def asking_user_roles(session):
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
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sleep(1)
    
    prompt = "The history of human civilization is filled with remarkable achievements, from the development of agriculture to the exploration of space. Over thousands of years, humans have transformed their environment, built towering cities, and developed complex societies. Our ability to innovate and adapt has been a defining trait, allowing us to overcome countless challenges and shape the world in ways previously unimaginable. \
One of the most significant advancements in human history was the development of agriculture. Before its advent, humans lived as hunter-gatherers, constantly moving in search of food. The discovery of farming allowed people to settle in one place, leading to the growth of permanent settlements and eventually, cities. Agriculture provided a reliable food source, enabling population growth and the division of labor. This, in turn, gave rise to specialized professions, trade, and governance. \
As civilizations grew, so did their need for communication. The invention of writing systems, such as cuneiform in Mesopotamia and hieroglyphics in Egypt, marked a major turning point. Writing allowed for the recording of laws, religious texts, and commercial transactions, preserving knowledge for future generations. The written word became a powerful tool, shaping politics, culture, and education. \
Technological advancements continued to shape societies throughout history. The Industrial Revolution of the 18th and 19th centuries brought about unprecedented changes. Mechanized production replaced manual labor, leading to the mass production of goods. This revolution not only improved living standards but also spurred urbanization, as people moved to cities in search of work. Factories and railroads became symbols of progress, connecting people and goods like never before. \
In the 20th and 21st centuries, the rapid development of digital technology has had an equally profound impact. The invention of computers and the internet revolutionized how people communicate, work, and access information. Social media platforms, artificial intelligence, and automation continue to shape the modern world, creating new opportunities and challenges. \
Beyond technological advancements, humanity has always sought to understand the mysteries of the universe. From the early astronomical observations of ancient civilizations to modern space exploration, our curiosity has driven us to expand our knowledge. The landing on the moon in 1969 was a milestone in space exploration, demonstrating what humans can achieve with determination and ingenuity. Today, efforts to explore Mars and beyond continue to push the boundaries of science and engineering. \
Despite these achievements, humanity faces significant challenges. Climate change, resource depletion, and global conflicts threaten progress. Addressing these issues requires cooperation, innovation, and sustainable practices. As history has shown, humans have the capacity to adapt and find solutions. The future will depend on our ability to work together, embracing scientific advancements while ensuring the well-being of future generations. \
In conclusion, human civilization is a testament to resilience, creativity, and ambition. From ancient farming practices to space travel, our journey has been marked by progress and discovery. As we look forward, our ability to solve problems and push the boundaries of knowledge will continue to define our path. The challenges ahead are daunting, but history teaches us that with determination, humanity can overcome them and continue to thrive."
    
    yield TTS(session, prompt[:200])
    
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
