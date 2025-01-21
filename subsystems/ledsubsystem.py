import math
import typing

import wpilib

from commands2 import Subsystem
from constants import LEDConstants

class DriveSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.led = wpilib.AddressableLED(LEDConstants.kLEDPort)

        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(LEDConstants.kLEDBuffer)]

        self.led.setLength(LEDConstants.kLEDBuffer)

        self.led.setData(self.ledData)
        self.led.start()

    def periodic(self) -> None:
        self.led.setData(self.ledData)

    def lightAll(self, hue: int, sat: int, val: int) -> None:
        for i in range(LEDConstants.kLEDBuffer):
            self.ledData[i].setHSV(hue, sat, val)