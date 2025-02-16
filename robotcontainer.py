import math

import commands2
import wpimath
import wpilib
from wpilib import SmartDashboard

from commands2 import cmd
from wpimath.controller import HolonomicDriveController
from wpimath.controller import PIDController, ProfiledPIDControllerRadians, HolonomicDriveController
from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpimath.units import rotationsToRadians

from phoenix6 import swerve, units

from commands.auto_align import AutoAlign
from constants import AutoConstants, DriveConstants, OIConstants
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem
from commands.auto_rotate import AutoRotate
from commands.drivecommand import DriveCommand

from generated.tuner_constants import TunerConstants # type: ignore
from pathplannerlib.auto import AutoBuilder # type: ignore
from pathplannerlib.auto import NamedCommands # type: ignore



class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The robot's subsystems
        self.robotDrive = TunerConstants.create_drivetrain()
        self.limelight = LimelightSystem()
        
        self.max_speed = TunerConstants.speed_at_12_volts

        self._drive = (
            swerve.requests.FieldCentric()
            .with_deadband(self.max_speed * 0.1)
            .with_rotational_deadband(
                rotationsToRadians(0.75) * 0.1
            )  # Add a 10% deadband
            .with_drive_request_type(
                swerve.SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
            )  # Use open-loop control for drive motors
        )
        # self.autoChooser = AutoBuilder.buildAutoChooser()

        # SmartDashboard.putData("Auto Chooser", self.autoChooser)

        # The driver's controller
        self.driverController = wpilib.XboxController(OIConstants.kDriverControllerPort)

        # Configure the button bindings
        self.configureButtonBindings()

        # Configure default commands
        self.robotDrive.setDefaultCommand(
            # Drivetrain will execute this command periodically
            self.robotDrive.apply_request(
                lambda: (
                    self._drive.with_velocity_x(
                        -self.driverController.getLeftY() * self.max_speed
                    )  # Drive forward with negative Y (forward)
                    .with_velocity_y(
                        -self.driverController.getLeftX() * self.max_speed
                    )  # Drive left with negative X (left)
                    .with_rotational_rate(
                        -self.driverController.getRightX() * rotationsToRadians(0.75)
                    )  # Drive counterclockwise with negative X (left)
                )
            )
        )

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

    def disablePIDSubsystems(self) -> None:
        """Disables all ProfiledPIDSubsystem and PIDSubsystem instances.
        This should be called on robot disable to prevent integral windup."""

    
    def getAutonomousCommand(self) -> commands2.Command:
        # """Use this to pass the autonomous command to the main {@link Robot} class.

        # :returns: the command to run in autonomous
        # """
        # # Create config for trajectory
        # config = TrajectoryConfig(
        #     AutoConstants.kMaxSpeedMetersPerSecond,
        #     AutoConstants.kMaxAccelerationMetersPerSecondSquared,
        # )
        # # Add kinematics to ensure max speed is actually obeyed
        # config.setKinematics(DriveConstants.kDriveKinematics)

        # # An example trajectory to follow. All units in meters.
        # exampleTrajectory = TrajectoryGenerator.generateTrajectory(
        #     # Start at the origin facing the +X direction
        #     Pose2d(0, 0, Rotation2d(0)),
        #     # Pass through these two interior waypoints, making an 's' curve path
        #     [Translation2d(1, 1), Translation2d(2, -1)],
        #     # End 3 meters straight ahead of where we started, facing forward
        #     Pose2d(3, 0, Rotation2d(0)),
        #     config,
        # )

        # exampleTrajectoryTwo = TrajectoryGenerator.generateTrajectory(
        #     # Start at the origin facing the +X direction
        #     Pose2d(0, 0, Rotation2d(0)),
        #     # Pass through these two interior waypoints, making an 's' curve path
        #     # [Translation2d(1, 1), Translation2d(2, -1)],
        #     [],
        #     # End 3 meters straight ahead of where we started, facing forward
        #     Pose2d(3, 0, Rotation2d(0)),
        #     config,
        # )

        # thetaController = ProfiledPIDControllerRadians(
        #     AutoConstants.kPThetaController,
        #     0,
        #     0,
        #     AutoConstants.kThetaControllerConstraints,
        # )
        # thetaController.enableContinuousInput(-math.pi, math.pi)

        # controller = HolonomicDriveController(
        #     PIDController(AutoConstants.kPXController, 0, 0),
        #     PIDController(AutoConstants.kPYController, 0, 0),
        #     thetaController,
        # )

        # swerveControllerCommand = commands2.SwerveControllerCommand(
        #     exampleTrajectory,
        #     self.robotDrive.getPose,
        #     DriveConstants.kDriveKinematics,
        #     controller,
        #     self.robotDrive.setModuleStates,
        #     (self.robotDrive,),
        # )

        # # Reset odometry to the starting pose of the trajectory.
        # self.robotDrive.resetOdometry(exampleTrajectory.initialPose())

        # # Run path following command, then stop at the end.
        # return swerveControllerCommand.andThen(
        #     cmd.run(
        #         lambda: self.robotDrive.drive(0, 0, 0, False, False),
        #         self.robotDrive,
        #     )
        # )

        # https://github.com/robotpy/robotpy-rev/tree/384ca50b2ede3ab44e09f0c12b8c5db33dff7c9e/examples/maxswerve

        return AutoAlign(self.robotDrive, self.limelight).andThen(AutoRotate(self.robotDrive, self.limelight))

        # return self.autoChooser.getSelected()
