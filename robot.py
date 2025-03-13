#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib
from cscore import VideoSource
from cscore import CameraServer

from robotcontainer import RobotContainer
from ntcore import NetworkTableInstance
from constants import OIConstants
from vision import CameraSubsystem, Direction


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()
        self.autonomousCommand = None
        self.frontCamera = CameraServer.startAutomaticCapture("front", 0)
        self.rearCamera = CameraServer.startAutomaticCapture("rear", 1)
        self.server = CameraServer.addSwitchedCamera("switch")
        self.frontCamera.setConnectionStrategy(VideoSource.ConnectionStrategy.kConnectionKeepOpen)
        self.rearCamera.setConnectionStrategy(VideoSource.ConnectionStrategy.kConnectionKeepOpen)
        self.server.setSource(self.frontCamera)
        
        self.driverController = wpilib.Joystick(OIConstants.kDriverControllerPort)

    # def autonomousInit(self) -> None:
    #     self.autonomousCommand = self.container.getAutonomousCommand()

    #     if self.autonomousCommand:
    #         self.autonomousCommand.schedule()

    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
    
    def teleopPeridodic(self) -> None:
        print("Setting camera 2")
        self.server.setSource(self.rearCamera)
    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()




if __name__ == "__main__":
    wpilib.run(MyRobot)
