import math

import commands2
import commands2.sequentialcommandgroup
import commands2.waitcommand
import wpimath
import wpilib
from wpilib import SmartDashboard


from commands2 import cmd
from wpimath.controller import HolonomicDriveController
from wpimath.controller import PIDController, ProfiledPIDControllerRadians, HolonomicDriveController
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpimath.kinematics import ChassisSpeeds

from constants import AutoConstants, DriveConstants, OIConstants, ElevatorConstants


from subsystems.elevator import ElevatorSubsystem
from commands.elevatorUpCommand import ElevatorUpCommand
from commands.elevatorDownCommand import ElevatorDownCommand
from commands.elevatorPos import ElevatorPosCommand
from commands.auto_align import AutoAlign
from constants import AutoConstants, DriveConstants, OIConstants
from subsystems.drivesubsystem import DriveSubsystem

from subsystems.limelight_subsystem import LimelightSystem
from commands.auto_rotate import AutoRotate
from commands.drivecommand import DriveCommand
from controls import DriverController
from pathplannerlib.auto import AutoBuilder # type: ignore
from pathplannerlib.auto import NamedCommands # type: ignore
from pathplannerlib.auto import PathPlannerAuto # type: ignore

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The robot's subsystems
        self.robotDrive = DriveSubsystem()
        self.elevator = ElevatorSubsystem()

        self.limelight = LimelightSystem()

        # NamedCommands.registerCommand('Auto Position', AutoAlign(self.robotDrive, self.limelight, 0.2, 0))
        # NamedCommands.registerCommand('Auto Rotate', AutoRotate(self.robotDrive, self.limelight))
        
        self.autoChooser = AutoBuilder.buildAutoChooser()

        SmartDashboard.putData("Auto Chooser", self.autoChooser)

        # button boards
        self.buttonBoard = commands2.button.CommandJoystick(OIConstants.kButtonBoardPort)
         # The driver's controller
        self.driverController = DriverController(self.robotDrive, self.limelight)

        # Configure the button bindings
        self.configureButtonBindings()

        # Configure default commands
        self.driverController.setDefaultCommands()


    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        #manual elevator
        self.buttonBoard.button(OIConstants.kElevatorUpButton).whileTrue(ElevatorUpCommand(self.elevator))
        self.buttonBoard.button(OIConstants.kElevatorDownButton).whileTrue(ElevatorDownCommand(self.elevator))

        #level 0
        self.buttonBoard.button(OIConstants.kElevatorLvl0Button).whileTrue(ElevatorPosCommand(self.elevator, ElevatorConstants.kLvl0Height))

        #level 1
        self.buttonBoard.button(OIConstants.kElevatorLvl1Button).whileTrue(ElevatorPosCommand(self.elevator, ElevatorConstants.kLvl1Height))

        #level 2
        self.buttonBoard.button(OIConstants.kElevatorLvl2Button).whileTrue(ElevatorPosCommand(self.elevator, ElevatorConstants.kLvl2Height))

        #level 3
        self.buttonBoard.button(OIConstants.kElevatorLvl3Button).whileTrue(ElevatorPosCommand(self.elevator, ElevatorConstants.kLvl3Height))

        #level 4
        self.buttonBoard.button(OIConstants.kElevatorLvl4Button).whileTrue(ElevatorPosCommand(self.elevator, ElevatorConstants.kLvl4Height))

        # self.elevator.setDefaultCommand(ElevatorPosCommand(self.elevator))




    def disablePIDSubsystems(self) -> None:
        """Disables all ProfiledPIDSubsystem and PIDSubsystem instances.
        This should be called on robot disable to prevent integral windup."""

    
    def getAutonomousCommand(self) -> commands2.Command:
        # https://github.com/robotpy/robotpy-rev/tree/384ca50b2ede3ab44e09f0c12b8c5db33dff7c9e/examples/maxswerve

        # return AutoAlign(self.robotDrive, self.limelight).andThen(AutoRotate(self.robotDrive, self.limelight))
        # return commands2.SequentialCommandGroup(commands2.InstantCommand(lambda: self.robotDrive.drive(ChassisSpeeds(-8, 0, 0), False, False), self.robotDrive), 
        #                                         commands2.WaitCommand(AutoConstants.kTimedTime),
        #                                         commands2.InstantCommand(lambda: self.robotDrive.drive(ChassisSpeeds(0, 0, 0), False, False), self.robotDrive)
        #                                         )
        return self.autoChooser.getSelected()
