from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from alpha_mini_rug.speech_to_text import SpeechToText
from time import time
import cv2 as cv
import numpy as np
import wave
import os


audio_processor = SpeechToText() # create an instance of the class
audio_processor.silence_time = 1 # parameter set to indicate when to stop recording
audio_processor.silence_threshold2 = 100 # any sound recorded below this value is considered silence
audio_processor.logging = True # set to true if you want to see all the output

@inlineCallbacks
def STT_continuous(session, response_time: int = 1000):
	info = yield session.call("rom.sensor.hearing.info")
	print(info)
	yield session.call("rom.sensor.hearing.sensitivity", 200)

	yield session.call("rie.dialogue.config.language",lang="en")
	yield session.call("rie.dialogue.say", text="Say something")
	print("listening to audio")
	yield session.subscribe(audio_processor.listen_continues, "rom.sensor.hearing.stream")
	yield session.call("rom.sensor.hearing.stream")
	for _ in range(response_time):
		if not audio_processor.new_words:
			yield sleep(0.5) # VERY IMPORTANT, OTHERWISE THE CONNECTION TO THE SERVER MIGHT CRASH
			print("I am recording")
		else:
			word_array = audio_processor.give_me_words()
			print(word_array)
			return word_array
		audio_processor.loop()
	return None

def TTS(session, text):
	print("saying stuff")
	session.call("rie.dialogue.say", text=text)

def make_outputdir():
	output_dir = "output"
	output_file = os.path.join(output_dir, "output.wav")
	os.makedirs(output_dir, exist_ok=True)
	if not os.path.exists(output_file):
		with open(output_file, "wb") as f:
			f.write(b"")
			# Write an empty byte string to create the file

@inlineCallbacks
def main(session, details):
	yield sleep(2)
	yield session.call("rom.optional.behavior.play", name="BlocklyStand")
	make_outputdir()
	
	word_array = STT_continuous(session)
	yield word_array

	if word_array:
		yield TTS(session, str(word_array))
	else:
		print("No words found")

	yield session.call("rom.optional.behavior.play", name="BlocklyCrouch")
	session.leave()


wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.67a48c4e85ba37f92bb13c87",
)

wamp.on_join(main)

if __name__ == "__main__":
	run([wamp])