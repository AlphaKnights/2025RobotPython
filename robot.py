#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from typing import Optional
import commands2
import wpilib
from wpilib.shuffleboard import Shuffleboard
from wpilib import SmartDashboard
import time
#from wpilib.filter import MedianFilter
from robotcontainer import RobotContainer


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        # self.container = RobotContainer()
        self.autonomousCommand: Optional[commands2.Command] = None
                # Creates a ping-response Ultrasonic object on DIO 1 and 2.
        self.rangeFinder = wpilib.Ultrasonic(1, 2)
        self.rangeFinder.setEnabled(True)
        self.rangeFinder.setAutomaticMode(True)

        # Add the ultrasonic to the "Sensors" tab of the dashboard
        # Data will update automatically
        Shuffleboard.getTab("Sensors").add(self.rangeFinder)

    def teleopPeriodic(self) -> None:
        # We can read the distance in millimeters
        #self.rangeFinder.ping()
        time.sleep(0.1)
        distanceMillimeters = self.rangeFinder.getRangeMM()
        # ... or in inches

        distanceInches = self.rangeFinder.getRangeInches()
        distance = self.rangeFinder.getRange()
        print(distanceInches)

        # We can also publish the data itself periodically
        SmartDashboard.putNumber("Distance[mm]", distanceMillimeters)
        SmartDashboard.putNumber("Distance[in]", distanceInches)

    def autonomousInit(self) -> None:
        # self.autonomousCommand = self.container.getAutonomousCommand()

        # if self.autonomousCommand:
        #     self.autonomousCommand.schedule()
        pass

    def teleopInit(self) -> None:
        # if self.autonomousCommand:
        #     self.autonomousCommand.cancel()
        # By default, the Ultrasonic class polls all ultrasonic sensors every in a round-robin to prevent
        # them from interfering from one another.
        # However, manual polling is also possible -- notes that this disables automatic mode!
        self.rangeFinder.ping()

    def testInit(self) -> None:
        # commands2.CommandScheduler.getInstance().cancelAll()
        pass

    def testPeriodic(self) -> None:
        #if self.rangeFinder.isRangeValid():
            # Data is valid, publish it
            SmartDashboard.putNumber("Distance[mm]", self.rangeFinder.getRangeMM())
            SmartDashboard.putNumber("Distance[in]", self.rangeFinder.getRangeInches())

            # Ping for next measurement
            self.rangeFinder.ping()

    def testExit(self) -> None:
        # Enable automatic mode
        self.rangeFinder.setAutomaticMode(True)

if __name__ == "__main__":
    wpilib.run(MyRobot)
