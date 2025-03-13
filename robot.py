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
        frontCamera = CameraServer.startAutomaticCapture("front", 0)
        rearCamera = CameraServer.startAutomaticCapture("rear", 1)
        server1 = CameraServer.addServer("server1", 0)
        server2 = CameraServer.addServer("server2", 1)
        frontCamera.setConnectionStrategy(VideoSource.ConnectionStrategy.kConnectionKeepOpen)
        rearCamera.setConnectionStrategy(VideoSource.ConnectionStrategy.kConnectionKeepOpen)
        
        self.driverController = wpilib.Joystick(OIConstants.kDriverControllerPort)
        self.camera = CameraSubsystem(frontCamera, rearCamera, server1, server2)
        self.direction = Direction.FRONT
        self.camera.select()

    # def autonomousInit(self) -> None:
    #     self.autonomousCommand = self.container.getAutonomousCommand()

    #     if self.autonomousCommand:
    #         self.autonomousCommand.schedule()

    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
    
    def teleopPeridodic(self) -> None:
        print("Setting camera 2")
        self.direction = Direction.REAR
        self.camera.select()
    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()




if __name__ == "__main__":
    wpilib.run(MyRobot)
