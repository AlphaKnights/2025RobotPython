import math
import typing

import wpilib

from commands2 import Subsystem
from constants import LEDConstants

class LEDSubsystem(Subsystem):
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

    def teamLights(self) -> None:
        for i in range(LEDConstants.kLEDBuffer):
            if (i % 2 == 0):
                self.ledData[i].setHSV(LEDConstants.kSilverHue, LEDConstants.kSilverSat, LEDConstants.kSilverVal)
            else:
                self.ledData[i].setHSV(LEDConstants.kBlueHue, LEDConstants.kBlueSat, LEDConstants.kBlueVal)