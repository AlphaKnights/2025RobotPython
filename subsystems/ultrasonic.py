# pylint: disable=no-member

import typing
import commands2
import wpilib
import limelight  # type: ignore
import time
from interfaces.limelight_results import LimelightResults
from constants import UltrasonicConstants

class UltrasonicSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.rangeFinder = wpilib.Ultrasonic(UltrasonicConstants.kPingChannel, UltrasonicConstants.kEchoChannel)
        self.rangeFinder.setAutomaticMode(False)
        self.rangeFinder.setEnabled(True)
        

    def periodic(self) -> None:
        if self.rangeFinder.isRangeValid():
            self.rangeFinder.ping()
            time.sleep(0.01)
        # We can read the distance in inches
            distanceInches = self.rangeFinder.getRangeInches()
            print(distanceInches)
        # We can also publish the data itself periodically
        # SmartDashboard.putNumber("Distance[mm]", distanceMillimeters)
        # SmartDashboard.putNumber("Distance[in]", distanceInches)
            
