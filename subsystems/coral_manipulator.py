import math
import typing
import time

import wpilib

from commands2 import Subsystem
from constants import LEDConstants, UltrasonicConstants

class CoralManipulator(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.led = wpilib.AddressableLED(LEDConstants.kLEDPort)
        self.rangeFinder = wpilib.Ultrasonic(1, 2)

        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(LEDConstants.kLEDBuffer)]

        self.led.setLength(LEDConstants.kLEDBuffer)

        self.led.setData(self.ledData)
        self.led.start()
        

    def periodic(self) -> None:
        if not self.rangeFinder.isRangeValid():
            self.lightAll(*LEDConstants.kBadColor)
            return
        
        self.rangeFinder.ping()
        
        time.sleep(0.1)

        if self.rangeFinder.getRangeInches() > 5:
            self.lightAll(*LEDConstants.kBadColor)
            return
        
        self.lightAll(*LEDConstants.kGoodColor)

    def lightAll(self, hue: int, sat: int, val: int) -> None:
        for i in range(LEDConstants.kLEDBuffer):
            self.ledData[i].setHSV(hue, sat, val)

        self.led.setData(self.ledData)

    def teamLights(self) -> None:
        for i in range(LEDConstants.kLEDBuffer):
            if (i % 2 == 0):
                self.ledData[i].setHSV(LEDConstants.kSilverHue, LEDConstants.kSilverSat, LEDConstants.kSilverVal)
            else:
                self.ledData[i].setHSV(LEDConstants.kBlueHue, LEDConstants.kBlueSat, LEDConstants.kBlueVal)