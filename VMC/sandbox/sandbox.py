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
            #this will probably spam the logs, remove once you test it
            if self.enabled:
                if autonTriggered == False:
                    box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 0, 0, 255]})
                    logger.debug("Autonomous Enabled")
                    autonTriggered = True
                    box.send_message("avr/fcm/actions", {"action": "takeoff", "payload": {"alt": 1}})
                    logger.debug("Blasting Off")
                    time.sleep(5)
                    box.send_message("avr/fcm/actions", {"action": "goto_location_ned", "payload": {"n": 0.5, "e": 0, "d": -1, "heading": 0}})
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
#     box = Sandbox()
#     box.run_non_blocking()
#     logger.debug("Sandbox Started Yay!")
#     box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 255, 0, 0]})
    # placeholder = 0
    # intensity = 0.1
    # while True:
    #     placeholder += 0.08
    #     saturationW = (50 + (math.sin(placeholder) * 50)) * intensity
    #     saturationR = (50 + (math.sin(placeholder + 1.57) * 50)) * intensity
    #     saturationG = (50 + (math.sin(placeholder + 3.14) * 50)) * intensity
    #     saturationB = (50 + (math.sin(placeholder + 4.71) * 50)) * intensity
    #     box.send_message("avr/pcm/set_base_color", {"wrgb": [int(saturationW), int(saturationR), int(saturationG), int(saturationB)]})
    #     #box.send_message("avr/pcm/set_servo_abs", {"servo": 3, "absolute": int(700 + saturationR * 7.5 * (1/intensity))})
    #     logger.debug(saturationR)
    #     time.sleep(0.0166)
    