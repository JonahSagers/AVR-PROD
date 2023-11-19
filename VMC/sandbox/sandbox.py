import time
import math

from threading import Thread
from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import AvrPcmSetBaseColorPayload, AvrPcmSetServoAbsPayload, AvrAutonomousEnablePayload
from loguru import logger

class Sandbox(MQTTModule):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Sandbox Initialized Yay!")
        self.enabled = False
        #code hangs here
        self.topic_map = {"avr/autonomous/enable": self.on_autonomous_message}
        logger.debug("Sandbox Finished Initializing Yay!")

    def on_autonomous_message(self, payload: AvrAutonomousEnablePayload) -> None:
        logger.debug("Autonomous Message Recieved Yay!")
        self.enabled = payload["enabled"]
        logger.debug("Autonomous Message Processed Yay!")

    def loop(self) -> None:
        autonTriggered = False
        box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 255, 0, 0]})
        while True:
            if self.enabled:
                if autonTriggered == False:
                    box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 0, 0, 255]})
                    logger.debug("Autonomous Enabled")
                    autonTriggered = True
                    box.send_message("avr/fcm/actions", {"action": "takeoff", "payload": {"alt": 4}})
                    logger.debug("Blasting Off")
                    time.sleep(5)
                    box.send_message("avr/fcm/actions", {"action": "goto_location_ned", "payload": {"n": 5.6896, "e": -1.778, "d": -4, "heading": 0}})
                    time.sleep(5)
                    box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 0, 255, 0]})
                    time.sleep(5)
                    box.send_message("avr/fcm/actions", {"action": "goto_location_ned", "payload": {"n": 1.289558, "e": -1.143, "d": -4, "heading": 0}})
                    time.sleep(7)
                    box.send_message("avr/fcm/actions", {"action": "land", "payload": {}})
                    logger.debug("Landing")
            else:
                if autonTriggered == True:
                    autonTriggered = False
                    box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 255, 0, 0]})
            time.sleep(0.5)

if __name__ == "__main__":
    box = Sandbox()

    # Create a new thread for running the loop function independently of the main program
    loop_thread = Thread(target=box.loop)
    loop_thread.setDaemon(
        True
    )  # Setting the thread as a Daemon so it will end when the main program ends
    loop_thread.start()  # Starting the new thread

    box.run()