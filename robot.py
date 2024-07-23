
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring 

import wpilib
import wpilib.drive

import wpimath
import wpimath.filter
import wpimath.controller

from src import drivetrain


class MyRobot(wpilib.TimedRobot):
    def __init__(self) -> None:
        super().__init__()

        self.controller: wpilib.XboxController
        self.swerve: drivetrain.Drivetrain

        self.xspeed_limiter: wpimath.filter.SlewRateLimiter
        self.yspeed_limiter: wpimath.filter.SlewRateLimiter
        self.rot_limiter: wpimath.filter.SlewRateLimiter

    def robotInit(self) -> None:
        """Robot initialization function"""
        self.controller = wpilib.XboxController(0)
        self.swerve = drivetrain.Drivetrain()

        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from
        # 0 to 1.
        self.xspeed_limiter = wpimath.filter.SlewRateLimiter(3)
        self.yspeed_limiter = wpimath.filter.SlewRateLimiter(3)
        self.rot_limiter = wpimath.filter.SlewRateLimiter(3)

    def autonomousPeriodic(self) -> None:
        self.drive_with_joystick(False)
        self.swerve.update_odometry()

    def teleopPeriodic(self) -> None:
        self.drive_with_joystick(True)

    def drive_with_joystick(self, field_relative: bool) -> None:
        # Get the x speed. We are inverting this because Xbox controllers return
        # negative values when we push forward.
        x_speed = (
            -self.xspeed_limiter.calculate(
                wpimath.applyDeadband(self.controller.getLeftY(), 0.02)
            )
            * drivetrain.KMAXSPEED
        )

        # Get the y speed or sideways/strafe speed. We are inverting this because
        # we want a positive value when we pull to the left. Xbox controllers
        # return positive values when you pull to the right by default.
        y_speed = (
            -self.yspeed_limiter.calculate(
                wpimath.applyDeadband(self.controller.getLeftX(), 0.02)
            )
            * drivetrain.KMAXSPEED
        )

        # Get the rate of angular rotation. We are inverting this because we want a
        # positive value when we pull to the left (remember, CCW is positive in
        # mathematics). Xbox controllers return positive values when you pull to
        # the right by default.
        rot = (
            -self.rot_limiter.calculate(
                wpimath.applyDeadband(self.controller.getRightX(), 0.02)
            )
            * drivetrain.KMAXSPEED
        )

        self.swerve.drive(
            x_speed,
            y_speed,
            rot,
            field_relative,
            self.getPeriod())
