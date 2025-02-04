from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

@inlineCallbacks
def main(session, details):
	yield session.call("rom.optional.behavior.play", name="BlocklyStand")
	# yield session.call("rie.dialogue.say", text="Hallo wereld!")
	# yield sleep(2)
	yield session.call("rie.dialogue.say_animated", text="Hello I speak!")
	sleep(2)
	yield session.call("rom.optional.behavior.play", name="BlocklyWaveRightArm")
	session.leave() # Close the connection with the robot

wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.67a2098385ba37f92bb12edd",
)

wamp.on_join(main)

if __name__ == "__main__":
	run([wamp])