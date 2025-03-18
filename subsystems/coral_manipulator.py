import math
import typing
import time

import wpilib
import phoenix6

from commands2 import Subsystem
from constants import LEDConstants, UltrasonicConstants, LaunchConstants

class CoralManipulator(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.led = wpilib.AddressableLED(LEDConstants.kLEDPort)
        self.rangeFinder = wpilib.Ultrasonic(UltrasonicConstants.kPingChannel, UltrasonicConstants.kEchoChannel)
        self.rangeFinder.setEnabled(True)
        self.rangeFinder.setAutomaticMode(False)
        self.launch_motor = phoenix6.hardware.TalonFX(LaunchConstants.kLaunchMotor)
        drive_motor_config = phoenix6.configs.TalonFXConfiguration()
        drive_motor_config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE
        self.launch_motor.configurator.apply(drive_motor_config)

        # self.launch_motor 


        self.ledData = [wpilib.AddressableLED.LEDData() for _ in range(LEDConstants.kLEDBuffer)]

        self.led.setLength(LEDConstants.kLEDBuffer)

        self.led.setData(self.ledData)
        self.led.start()
        

    def periodic(self) -> None:
        if not self.rangeFinder.isRangeValid():
            self.lightAll(*LEDConstants.kBadColor)
            print("invalid")
            # return
        
        self.rangeFinder.ping()
        print("ping")
        time.sleep(0.1)
        print(self.rangeFinder.getRangeInches())

        if (self.rangeFinder.isRangeValid()):
        
            if self.rangeFinder.getRangeInches() > 3:
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

    def launch(self, speed: float) -> None:
        self.launch_motor.set(speed)
        # print("fire")

    def stop(self) -> None:
        self.launch_motor.stopMotor()

    