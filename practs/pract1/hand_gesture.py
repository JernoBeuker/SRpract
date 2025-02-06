from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from alpha_mini_rug import perform_movement

@inlineCallbacks
def main(session, details):
    yield perform_movement(session,
        frames=[{"time": 400, "data": {"body.arms.right.lower.roll": -1,"body.arms.right.upper.pitch": 0}},
            {"time": 1200, "data": {"body.arms.right.lower.roll": -1,"body.arms.right.upper.pitch": -2}},
            {"time": 2000, "data": {"body.arms.right.lower.roll": 0,"body.arms.right.upper.pitch": -2}}],
        mode="linear",
        sync=True, 
        force=False
    )

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