import time
import math

from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import AvrPcmSetBaseColorPayload, AvrPcmSetServoAbsPayload, AvrAutonomousEnablePayload
from loguru import logger

class Sandbox(MQTTModule):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Class initialized")
        logger.debug("Sandbox Initialized Yay!")
        self.enabled = False
        self.topic_map = {"avr/autonomous/enable": self.on_autonomous_message}
        self.autonomous_code()
        logger.debug("Sandbox Finished Initializing Yay!")

    def on_autonomous_message(self, payload: AvrAutonomousEnablePayload) -> None:
        self.enabled = payload["enable"]
        logger.debug("Autonomous Message Recieved Yay!")

    def autonomous_code(self) -> None:
        while True:
            if self.enabled:
                box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 0, 255, 0]})
                logger.debug("Setting Color To White")
            time.sleep(1)

if __name__ == "__main__":
    box = Sandbox()
    box.run_non_blocking()
    logger.debug("Sandbox Started Yay!")
    box.send_message("avr/pcm/set_base_color", {"wrgb": [100, 255, 0, 0]})
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
    