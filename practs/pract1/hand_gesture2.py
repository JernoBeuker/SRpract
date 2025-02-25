from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from alpha_mini_rug import perform_movement
from autobahn.twisted.util import sleep
from gestures import NATURAL_POS, GESTURES, CELEBRATE, THINK_DEEPLY
import random as rd


@inlineCallbacks
def motion(session, frames):
    yield perform_movement(session,
        frames=frames,
        mode="last",        # experiment with this variable
        sync=True, 
        force=False
    )
    yield sleep(frames[-1]["time"] / 1000)


@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield sleep(1)
    yield motion(session, NATURAL_POS)
    yield sleep(1)
    # for _ in range(10):
    yield motion(session, THINK_DEEPLY)
    yield sleep(1)
    yield session.call("rom.optional.behavior.play", name="BlocklyCrouch")
    yield sleep(1)
    session.leave()

wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.67bd963ca06ea6579d142ade",
)

wamp.on_join(main)

if __name__ == "__main__":
	run([wamp])