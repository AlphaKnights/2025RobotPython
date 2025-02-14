#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib

from robotcontainer import RobotContainer
from ntcore import NetworkTableInstance
from constants import OIConstants


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()
        self.autonomousCommand = None

        self.driverController = wpilib.XboxController(OIConstants.kDriverControllerPort)
        self.cameraSelection = NetworkTableInstance.getDefault().getTable("").getEntry("CameraSelection")
        wpilib.CameraServer.launch("vision.py:main")

    # def autonomousInit(self) -> None:
    #     self.autonomousCommand = self.container.getAutonomousCommand()

    #     if self.autonomousCommand:
    #         self.autonomousCommand.schedule()

    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
    
    def teleopPeridodic(self) -> None:
        if self.driverController.getLeftY() < 0:
            print("Setting camera 2")
            self.cameraSelection.setString("USB Camera 1")
        else:
            print("Setting camera 1")
            self.cameraSelection.setString("USB Camera 0")
    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()




if __name__ == "__main__":
    wpilib.run(MyRobot)
