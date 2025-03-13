# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

"""
The constants module is a convenience place for teams to hold robot-wide
numerical or boolean constants. Don't use this for any other purpose!
"""


import math
from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics
from wpimath.trajectory import TrapezoidProfileRadians


# from rev import CANSparkMax
from rev import SparkMax, SparkBaseConfig


class NeoMotorConstants:
    kFreeSpeedRpm = 5676


class DriveConstants:
    # Driving Parameters - Note that these are not the maximum capable speeds of
    # the robot, rather the allowed maximum speeds
    kMaxSpeedMetersPerSecond = 15
    # kMaxAngularSpeed = math.tau  # radians per second
    kMaxAngularSpeed = 20

    kDirectionSlewRate = 1.2  # radians per second
    kMagnitudeSlewRate = 1.8  # percent per second (1 = 100%)
    kRotationalSlewRate = 2.0  # percent per second (1 = 100%)

    # Chassis configuration
    kTrackWidth = units.inchesToMeters(26.5)
    # Distance between centers of right and left wheels on robot
    kWheelBase = units.inchesToMeters(26.5)

    # Distance between front and back wheels on robot
    kModulePositions = [
        Translation2d(kWheelBase / 2, kTrackWidth / 2),
        Translation2d(kWheelBase / 2, -kTrackWidth / 2),
        Translation2d(-kWheelBase / 2, kTrackWidth / 2),
        Translation2d(-kWheelBase / 2, -kTrackWidth / 2),
    ]
    kDriveKinematics = SwerveDrive4Kinematics(*kModulePositions)

    
    # Offsets of the modules from the robot 
    kFrontLeftChassisAngularOffset = math.radians(-0.764892578125 * (360))
    kFrontRightChassisAngularOffset = math.radians(0.75 * (360))
    kBackLeftChassisAngularOffset = math.radians(0.079833984375 * (360))
    kBackRightChassisAngularOffset = math.radians(0.367919921875 * (360))

    # SPARK MAX CAN IDs
    kFrontLeftDrivingCanId = 6
    kRearLeftDrivingCanId = 21
    kFrontRightDrivingCanId = 11
    kRearRightDrivingCanId = 3

    kFrontLeftTurningCanId = 22
    kRearLeftTurningCanId = 14
    kFrontRightTurningCanId = 13
    kRearRightTurningCanId = 12

    # Kraken IDs
    kFrontLeftDrivingId = 5
    kRearLeftDrivingId = 7
    kFrontRightDrivingId = 4
    kRearRightDrivingId = 1

    kFrontLeftTurningId = 6
    kRearLeftTurningId = 8
    kFrontRightTurningId = 3
    kRearRightTurningId = 2

    kFrontLeftCANCoderId = 3    
    kRearLeftCANCoderId = 4
    kFrontRightCANCoderId = 2
    kRearRightCANCoderId = 1

    kGyroReversed = True

class ModuleConstants:
    # The MAXSwerve module can be configured with one of three pinion gears: 12T, 13T, or 14T.
    # This changes the drive speed of the module (a pinion gear with more teeth will result in a
    # robot that drives faster).
    kDrivingMotorPinionTeeth = 14

    # Invert the turning encoder, since the output shaft rotates in the opposite direction of
    # the steering motor in the MAXSwerve Module.
    kTurningEncoderInverted = True

    # Calculations required for driving motor conversion factors and feed forward
    kDrivingMotorFreeSpeedRps = NeoMotorConstants.kFreeSpeedRpm / 60
    kWheelDiameterMeters = 0.0762
    kWheelCircumferenceMeters = kWheelDiameterMeters * math.pi
    # 45 teeth on the wheel's bevel gear, 22 teeth on the first-stage spur gear, 15 teeth on the bevel pinion
    kDrivingMotorReduction = (45.0 * 22) / (kDrivingMotorPinionTeeth * 15)
    kDriveWheelFreeSpeedRps = (
        kDrivingMotorFreeSpeedRps * kWheelCircumferenceMeters
    ) / kDrivingMotorReduction

    kDrivingEncoderPositionFactor = (
        kWheelDiameterMeters * math.pi
    ) / kDrivingMotorReduction  # meters
    kDrivingEncoderVelocityFactor = (
        (kWheelDiameterMeters * math.pi) / kDrivingMotorReduction
    ) / 60.0  # meters per second

    kTurningEncoderPositionFactor = math.tau  # radian
    kTurningEncoderVelocityFactor = math.tau / 60.0  # radians per second

    kTurningEncoderPositionPIDMinInput = 0  # radian
    kTurningEncoderPositionPIDMaxInput = kTurningEncoderPositionFactor  # radian

    kDrivingP = 0.65
    kDrivingI = 0
    kDrivingD = 0
    kDrivingFF = 1.5
    kDrivingV = 0.3
    kDrivingA = 1.5
    kDrivingMinOutput = -1
    kDrivingMaxOutput = 1

    kTurningP = 40
    kTurningI = 0
    kTurningD = 0
    kTurningFF = 0
    kTurningMinOutput = -1
    kTurningMaxOutput = 1


    kDrivingMotorIdleMode = SparkBaseConfig.IdleMode.kBrake
    kTurningMotorIdleMode = SparkBaseConfig.IdleMode.kBrake

    kDrivingMotorCurrentLimit = 50  # amp
    kTurningMotorCurrentLimit = 20  # amp


class OIConstants:
    kDriverControllerPort = 1
    kDriveDeadband = 0.4

    kButtonBoardPort = 0
    kElevatorUpButton = 9
    kElevatorDownButton = 8
    kElevatorLvl0Button = 1
    kElevatorLvl1Button = 2
    kElevatorLvl2Button = 3
    kElevatorLvl3Button = 4
    kElevatorLvl4Button = 5

class AutoConstants:
    kMaxSpeedMetersPerSecond = 10
    kMaxAccelerationMetersPerSecondSquared = 10
    kMaxAngularSpeedRadiansPerSecond = math.pi
    kMaxAngularSpeedRadiansPerSecondSquared = math.pi

    kPXController = 1
    kPYController = 1
    kPThetaController = 1

    # Constraint for the motion profiled robot angle controller
    kThetaControllerConstraints = TrapezoidProfileRadians.Constraints(
        kMaxAngularSpeedRadiansPerSecond, kMaxAngularSpeedRadiansPerSecondSquared
    )

class ElevatorConstants:
    kLeftMotorCanId = 4
    kRightMotorCanId = 32
    kUpperLimit = 1
    kLowerLimit = 2

    kEncoderPositionFactor = 1
    kEncoderVelocityFactor = 1

    kP = 0.05
    kI = 0
    kD = 0

    kLvl0Height = 0.0
    
    kLvl1Height = 0.0
    
    kLvl2Height = 0.0

    kLvl3Height = 0.0
    
    kLvl4Height = 0.0

    kForwardSoftLimit = 10000
    kReverseSoftLimit = -100

    kElevatorMaxSpeed = 1
    kTimedSpeed = 0.6
    kTimedTime = 4

class LEDConstants:
    kLEDPort = 0
    kLEDBuffer = 64

    kSilverHue = 0
    kSilverSat = 0
    kSilverVal = 10

    kBlueHue = 90
    kBlueSat = 220
    kBlueVal = 30

class AlignConstants:
    kMaxNormalizedSpeed = 5.0
    kMaxTurningSpeed = 1.0
    kDistToSlow = 0.3
    kRotDistToSlow = 0.5
    kAlignDeadzone = 0.01
    kAlignRotDeadzone = 5

