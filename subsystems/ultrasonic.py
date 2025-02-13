# pylint: disable=no-member

import typing
import commands2
import wpilib
import limelight  # type: ignore
import time
from interfaces.limelight_results import LimelightResults

class UltrasonicSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.rangeFinder = wpilib.Ultrasonic(1, 2)
        self.rangeFinder.setAutomaticMode(True)

    def periodic(self) -> None:
        time.sleep(0.5)
        # We can read the distance in millimeters
        distanceMillimeters = self.rangeFinder.getRangeMM()
        # ... or in inches
        distanceInches = self.rangeFinder.getRangeInches()

        # We can also publish the data itself periodically
        # SmartDashboard.putNumber("Distance[mm]", distanceMillimeters)
        # SmartDashboard.putNumber("Distance[in]", distanceInches)

        print(distanceInches)
