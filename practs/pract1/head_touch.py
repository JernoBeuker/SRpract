from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

def front(session):
	session.call("rie.dialogue.say", text="Touching front!")
	
def middle(session):
	session.call("rie.dialogue.say", text="Touching middle!")

def rear(session):
	session.call("rie.dialogue.say", text="Touching rear!")


@inlineCallbacks
def main(session, details):
	def touched(frame):
		if ("body.head.front" in frame["data"] and frame["data"]["body.head.front"]):
			print("touch front")
			front(session)
		elif ("body.head.middle" in frame["data"] and frame["data"]["body.head.middle"]):
			print("touch middle")
			middle(session)
		elif ("body.head.rear" in frame["data"] and frame["data"]["body.head.rear"]):
			print("touch rear")
			rear(session)
	sleep(60)
	yield session.subscribe(touched, "rom.sensor.touch.stream")
	yield session.call("rom.sensor.touch.stream")

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