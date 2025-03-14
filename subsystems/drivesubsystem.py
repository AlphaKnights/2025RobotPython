import math
import typing
import time
from typing import Callable, Sequence

import wpimath.kinematics
import wpilib
from navx import AHRS 

from commands2 import Subsystem
from wpimath.filter import SlewRateLimiter
from wpimath.controller import ProfiledPIDControllerRadians
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, Trajectory, TrajectoryGenerator
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveModuleState,
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
)

from wpilib import SmartDashboard, SendableChooser, Field2d


from constants import AutoConstants, DriveConstants, ModuleConstants
import swerveutils
# from .maxswervemodule import MAXSwerveModule
from .talonswervemodule import TalonSwerveModule as MAXSwerveModule # type: ignore

from pathplannerlib.auto import AutoBuilder # type: ignore
from pathplannerlib.controller import PPHolonomicDriveController  # type: ignore
from pathplannerlib.config import RobotConfig, PIDConstants # type: ignore
from wpilib import DriverStation


class DriveSubsystem(Subsystem):
    """
    The DriveSubsystem class is a subsystem that controls the swerve drive of the robot.
    """
    def __init__(self) -> None:
        super().__init__()

        # Create MAXSwerveModules
        # self.frontLeft = MAXSwerveModule(
            #  DriveConstants.kFrontLeftDrivingCanId,
        #     DriveConstants.kFrontLeftTurningCanId,
        #     DriveConstants.kFrontLeftCANCoderId,
        #     DriveConstants.kFrontLeftChassisAngularOffset,
        # )

        # self.frontRight = MAXSwerveModule(
        #     DriveConstants.kFrontRightDrivingCanId,
        #     DriveConstants.kFrontRightTurningCanId,
        #     DriveConstants.kFrontRightCANCoderId,
        #     DriveConstants.kFrontRightChassisAngularOffset,
        # )

        # self.rearLeft = MAXSwerveModule(
        #     DriveConstants.kRearLeftDrivingCanId,
        #     DriveConstants.kRearLeftTurningCanId,
        #     DriveConstants.kRearLeftCANCoderId,
        #     DriveConstants.kBackLeftChassisAngularOffset,
        # )

        # self.rearRight = MAXSwerveModule(
        #     DriveConstants.kRearRightDrivingCanId,
        #     DriveConstants.kRearRightTurningCanId,
        #     DriveConstants.kRearRightCANCoderId,
        #     DriveConstants.kBackRightChassisAngularOffset,
        # )

        self.field = Field2d()
        SmartDashboard.putData("Field", self.field)
        self.frontLeft = MAXSwerveModule(
            DriveConstants.kFrontLeftDrivingId,
            DriveConstants.kFrontLeftTurningId,
            DriveConstants.kFrontLeftCANCoderId,
            DriveConstants.kFrontLeftChassisAngularOffset,
            # 1,
            # DriveConstants.kFrontLeftPosition,
        )


        self.frontRight = MAXSwerveModule(
            DriveConstants.kFrontRightDrivingId,
            DriveConstants.kFrontRightTurningId,
            DriveConstants.kFrontRightCANCoderId,
            DriveConstants.kFrontRightChassisAngularOffset,
            # 2,
            # DriveConstants.kFrontRightPosition,
        )


        self.rearLeft = MAXSwerveModule(
            DriveConstants.kRearLeftDrivingId,
            DriveConstants.kRearLeftTurningId,
            DriveConstants.kRearLeftCANCoderId,
            DriveConstants.kBackLeftChassisAngularOffset,
            # 3,
            # DriveConstants.kRearLeftPosition,
        )


        self.rearRight = MAXSwerveModule(
            DriveConstants.kRearRightDrivingId,
            DriveConstants.kRearRightTurningId,
            DriveConstants.kRearRightCANCoderId,
            DriveConstants.kBackRightChassisAngularOffset,
            # 4,
            # DriveConstants.kRearRightPosition
        )



        # The gyro sensor
        self.gyro = AHRS(AHRS.NavXComType.kMXP_SPI)
        self.gyro.enableBoardlevelYawReset(False)
        self.gyro.reset()
        while abs(self.gyro.getAngle()) > 5:
            print('wrong angle', self.gyro.getAngle())
            self.gyro.reset()
        # self.gyro = wpilib.ADXRS450_Gyro()
            self.gyro_heading = self.gyro.getAngle()

        # Slew rate filter variables for controlling lateral acceleration
        self.currentRotation = 0.0
        self.currentTranslationDir = 0.0
        self.currentTranslationMag = 0.0

        self.magLimiter = SlewRateLimiter(DriveConstants.kMagnitudeSlewRate)
        self.rotLimiter = SlewRateLimiter(DriveConstants.kRotationalSlewRate)
        self.prevTime = wpilib.Timer.getFPGATimestamp()

        # Odometry class for tracking robot pose
        self.odometry = SwerveDrive4Odometry(
            DriveConstants.kDriveKinematics,
            Rotation2d.fromDegrees(self.gyro.getAngle()),
            (
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.rearLeft.getPosition(),
                self.rearRight.getPosition(),
            ),
        )

        config = RobotConfig.fromGUISettings()

        # Configure the AutoBuilder last
        AutoBuilder.configure(
            self.getPose, # Robot pose supplier
            self.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.getCurrentSpeeds, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            lambda speeds, feedforwards: self.drive(speeds, False, False), # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also outputs individual module feedforwards
            PPHolonomicDriveController( # PPHolonomicController is the built in path following controller for holonomic drive trains
                PIDConstants(5, 0, 0), # Translation PID constants
                PIDConstants(13, 0, 0), # Rotation PID constants
                1,
            ),
            config, # The robot configuration
            self.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self # Reference to this subsystem to set requirements
        )

    def periodic(self) -> None:
        # Update the odometry in the periodic block
        self.odometry.update(
            Rotation2d.fromDegrees(self.gyro.getAngle()),
            (
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.rearLeft.getPosition(),
                self.rearRight.getPosition(),
            ),
        )
        self.field.setRobotPose(self.odometry.getPose())

    def getPose(self) -> Pose2d:
        """Returns the currently-estimated pose of the robot.

        :returns: The pose.
        """
        return self.odometry.getPose()

    def resetOdometry(self, pose: Pose2d) -> None:
        """Resets the odometry to the specified pose.

        :param pose: The pose to which to set the odometry.

        """
        self.odometry.resetPosition(
            Rotation2d.fromDegrees(self.gyro.getAngle()),
            (
                self.frontLeft.getPosition(),
                self.frontRight.getPosition(),
                self.rearLeft.getPosition(),
                self.rearRight.getPosition(),
            ),
            pose,
        )

    def resetPose(self, pose: Pose2d) -> None:
        """Resets the pose of the robot.

        :param pose: The pose to which to set the robot.
        """
        self.resetOdometry(pose)

    def drive(
        self,
        speeds: ChassisSpeeds,
        fieldRelative: bool,
        rateLimit: bool,
    ) -> None:
        """Method to drive the robot using joystick info.

        :param xSpeed:        Speed of the robot in the x direction (forward).
        :param ySpeed:        Speed of the robot in the y direction (sideways).
        :param rot:           Angular rate of the robot.
        :param fieldRelative: Whether the provided x and y speeds are relative to the
                              field.
        :param rateLimit:     Whether to enable rate limiting for smoother control.
        """

        # speeds = ChassisSpeeds(10, 0, 0)

        # print('angle', self.gyro.getAngle())

        swerveModuleStates = DriveConstants.kDriveKinematics.toSwerveModuleStates(speeds)

        # swerveModuleStates = SwerveDrive4Kinematics.desaturateWheelSpeeds(swerveModuleStates, DriveConstants.kMaxSpeedMetersPerSecond)

        if fieldRelative:
            swerveModuleStates = DriveConstants.kDriveKinematics.toSwerveModuleStates(ChassisSpeeds.fromFieldRelativeSpeeds(speeds, Rotation2d.fromDegrees(self.gyro.getAngle())))

        self.frontLeft.setDesiredState(swerveModuleStates[0])
        self.frontRight.setDesiredState(swerveModuleStates[1])
        self.rearLeft.setDesiredState(swerveModuleStates[2])
        self.rearRight.setDesiredState(swerveModuleStates[3])

    def setX(self) -> None:
        # return
        """Sets the wheels into an X formation to prevent movement."""
        self.frontLeft.setDesiredState(SwerveModuleState(0, Rotation2d.fromDegrees(45)))
        self.frontRight.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(-45))
        )
        self.rearLeft.setDesiredState(SwerveModuleState(0, Rotation2d.fromDegrees(-45)))
        self.rearRight.setDesiredState(SwerveModuleState(0, Rotation2d.fromDegrees(45)))

    def setModuleStates(
        self,
        desiredStates: typing.Sequence[SwerveModuleState],
    ) -> None:
        """Sets the swerve ModuleStates.

        :param desiredStates: The desired SwerveModule states. Must be 4 states
        """
        
        desiredStates = (
            desiredStates[0],
            desiredStates[1],
            desiredStates[2],
            desiredStates[3],
        )

        fl, fr, rl, rr = SwerveDrive4Kinematics.desaturateWheelSpeeds(
            desiredStates, DriveConstants.kMaxSpeedMetersPerSecond
        )
        self.frontLeft.setDesiredState(fl)
        self.frontRight.setDesiredState(fr)
        self.rearLeft.setDesiredState(rl)
        self.rearRight.setDesiredState(rr)

        # return self.setStates

    def resetEncoders(self) -> None:
        """Resets the drive encoders to currently read a position of 0."""
        self.frontLeft.resetEncoders()
        self.rearLeft.resetEncoders()
        self.frontRight.resetEncoders()
        self.rearRight.resetEncoders()

    def zeroHeading(self) -> None:
        """Zeroes the heading of the robot."""
        self.gyro.reset()
        # self.gyro_heading = self.gyro.getAngle()

    def getHeading(self) -> float:
        """Returns the heading of the robot.

        :returns: the robot's heading in degrees, from -180 to 180
        """
        return Rotation2d.fromDegrees(self.gyro.getAngle()).degrees()
    
    def getCurrentSpeeds(self) -> ChassisSpeeds:
        """Returns the current speeds of the robot.

        :returns: The current speeds of the robot
        """
        moduleStates = (
            self.frontLeft.getState(),
            self.frontRight.getState(),
            self.rearLeft.getState(),
            self.rearRight.getState(),
        )

        return DriveConstants.kDriveKinematics.toChassisSpeeds(moduleStates)
    
    def getTurnRate(self) -> float:
        """Returns the turn rate of the robot.

        :returns: The turn rate of the robot, in degrees per second
        """
        return self.gyro.getRate() * (-1.0 if DriveConstants.kGyroReversed else 1.0)

    def shouldFlipPath(self) -> bool:
    # Boolean supplier that controls when the path will be mirrored for the red alliance
    # This will flip the path being followed to the red side of the field.
    # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed
