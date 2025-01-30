import math

import commands2
import wpimath
import wpilib

from commands2 import cmd
from wpimath.controller import PIDController, ProfiledPIDControllerRadians
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator

from constants import AutoConstants, DriveConstants, OIConstants
from subsystems.drivesubsystem import DriveSubsystem
from commands.drivecommand import DriveCommand

from subsystems.elevatorsubsystem import ElevatorSubsystem
from commands.elevatorUpCommand import ElevatorUpCommand
from commands.elevatorDownCommand import ElevatorDownCommand

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The robot's subsystems
        #self.robotDrive = DriveSubsystem()
        self.elevator = ElevatorSubsystem()

        # The driver's controller
        self.driverController = commands2.button.CommandXboxController(OIConstants.kDriverControllerPort)

        # button boards
        self.buttonBoard = commands2.button.CommandJoystick(OIConstants.kButtonBoardPort)

        # Configure the button bindings
        self.configureButtonBindings()

        # Configure default commands
        # self.robotDrive.setDefaultCommand(
        #     # The left stick controls translation of the robot.
        #     # Turning is controlled by the X axis of the right stick.
        #     DriveCommand(
        #         self.robotDrive,
        #         lambda:   
        #             -wpimath.applyDeadband(
        #                 self.driverController.getLeftY(), OIConstants.kDriveDeadband
        #             ),
        #         lambda:
        #             -wpimath.applyDeadband(
        #                 self.driverController.getLeftX(), OIConstants.kDriveDeadband
        #             ),
        #         lambda:
        #             -wpimath.applyDeadband(
        #                 self.driverController.getRightX(), OIConstants.kDriveDeadband
        #             ),
        #         ),
        #     )

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        self.buttonBoard.button(OIConstants.kElevatorUpButton).whileTrue(ElevatorUpCommand(self.elevator))
        self.driverController.button(OIConstants.kElevatorDownButton).whileTrue(ElevatorDownCommand(self.elevator))



    def disablePIDSubsystems(self) -> None:
        """Disables all ProfiledPIDSubsystem and PIDSubsystem instances.
        This should be called on robot disable to prevent integral windup."""

    
    # def getAutonomousCommand(self) -> commands2.Command:
    #     """Use this to pass the autonomous command to the main {@link Robot} class.

    #     :returns: the command to run in autonomous
    #     """   
    #     # Create config for trajectory
    #     config = TrajectoryConfig(
    #         AutoConstants.kMaxSpeedMetersPerSecond,
    #         AutoConstants.kMaxAccelerationMetersPerSecondSquared,
    #     )
    #     # Add kinematics to ensure max speed is actually obeyed
    #     config.setKinematics(DriveConstants.kDriveKinematics)

    #     # An example trajectory to follow. All units in meters.
    #     exampleTrajectory = TrajectoryGenerator.generateTrajectory(
    #         # Start at the origin facing the +X direction
    #         Pose2d(0, 0, Rotation2d(0)),
    #         # Pass through these two interior waypoints, making an 's' curve path
    #         [Translation2d(1, 1), Translation2d(2, -1)],
    #         # End 3 meters straight ahead of where we started, facing forward
    #         Pose2d(3, 0, Rotation2d(0)),
    #         config,
    #     )

    #     thetaController = ProfiledPIDControllerRadians(
    #         AutoConstants.kPThetaController,
    #         0,
    #         0,
    #         AutoConstants.kThetaControllerConstraints,
    #     )
    #     thetaController.enableContinuousInput(-math.pi, math.pi)

    #     swerveControllerCommand = commands2.SwerveControllerCommand(
    #         exampleTrajectory,
    #         self.robotDrive.getPose,  # Functional interface to feed supplier
    #         DriveConstants.kDriveKinematics,
    #         # Position controllers
    #         PIDController(AutoConstants.kPXController, 0, 0),
    #         PIDController(AutoConstants.kPYController, 0, 0),
    #         thetaController,
    #         self.robotDrive.setModuleStates,
    #         (self.robotDrive,),
    #     )

    #     # Reset odometry to the starting pose of the trajectory.
    #     self.robotDrive.resetOdometry(exampleTrajectory.initialPose())

    #     # Run path following command, then stop at the end.
    #     return swerveControllerCommand.andThen(
    #         cmd.run(
    #             lambda: self.robotDrive.drive(0, 0, 0, False, False),
    #             self.robotDrive,
    #         )
    #     )
