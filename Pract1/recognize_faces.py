from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.call("rie.vision.face.find")
    yield session.call("rie.dialogue.say", text="Hoi!")
    yield session.call("rie.vision.face.track")
    yield session.call("rie.dialogue.say", text="Ik zie je niet meer!")
    yield session.call("rom.optional.behavior.play", name="BlocklyCrouch")
    session.leave() # Sluit de verbinding met de robot
    # Create wamp connection

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