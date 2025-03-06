#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib
from cscore import UsbCamera, VideoSink, CameraServer

from robotcontainer import RobotContainer
from ntcore import NetworkTableInstance
from constants import OIConstants
from vision import CameraSubsystem


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self) -> None:
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()
        self.autonomousCommand = None
        frontCamera = CameraServer.startAutomaticCapture(1)
        rearCamera = CameraServer.startAutomaticCapture(0)
        cameraSelection = NetworkTableInstance.getDefault().getTable("").getEntry("CameraSelection")
        
        self.driverController = wpilib.Joystick(OIConstants.kDriverControllerPort)
        self.camera = CameraSubsystem(frontCamera, rearCamera, cameraSelection)
        self.direction = 1

    # def autonomousInit(self) -> None:
    #     self.autonomousCommand = self.container.getAutonomousCommand()

    #     if self.autonomousCommand:
    #         self.autonomousCommand.schedule()

    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
    
    def teleopPeridodic(self) -> None:
        if self.driverController.getYChannel() <= 0:
            print("Setting camera 1")
            self.direction = 1
            self.camera.select(self.direction)
            CameraServer.getVideo()
        else:
            print("Setting camera 2")
            self.direction = 0
            self.camera.select(self.direction)
            CameraServer.getVideo()
    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()




if __name__ == "__main__":
    wpilib.run(MyRobot)
