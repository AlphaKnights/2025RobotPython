#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from typing import Optional
import commands2
import wpilib
from wpilib import SmartDashboard, DriverStation, RobotController
from commands.auto_align import AutoAlign
from robotcontainer import RobotContainer
from commands.drivecommand import DriveCommand

class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()
        self.autonomousCommand: Optional[commands2.Command] = None

    def robotPeriodic(self) -> None:
        SmartDashboard.putNumber("Match Time", DriverStation.getMatchTime())
        SmartDashboard.putNumber("CAN Utilization %", RobotController.getCANStatus().percentBusUtilization * 100.0)
        SmartDashboard.putBoolean("Tag Detected", DriveCommand.isTagDetected)
        SmartDashboard.putBoolean("Aligned to Tag", DriveCommand.isAlligned)
    def autonomousInit(self) -> None:
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()

    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MyRobot)
