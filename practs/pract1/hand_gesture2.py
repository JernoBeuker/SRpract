from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from alpha_mini_rug import perform_movement
from autobahn.twisted.util import sleep
from gestures import NATURAL_POS, GESTURES
import random as rd


def motion(session, frames):
    yield perform_movement(session,
        frames=frames,
        mode="linear",
        sync=True, 
        force=False
    )
    yield sleep(frames[-1]["time"] / 1000)


@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyCrouch")
    yield motion(session, NATURAL_POS)
    for _ in range(10):
        yield motion(session, rd.choice(GESTURES))
        yield sleep(1)
    session.leave()

wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.67b30ccdaa9b77655979f1b5",
)

wamp.on_join(main)

if __name__ == "__main__":
	run([wamp])