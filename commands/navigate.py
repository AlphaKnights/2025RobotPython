# import math
# import commands2
# import wpilib.drive

# from commands2 import cmd
# from wpimath.controller import HolonomicDriveController
# from wpimath.controller import PIDController, ProfiledPIDControllerRadians, HolonomicDriveController
# from wpimath.geometry import Pose2d, Rotation2d, Translation2d
# from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator

# from constants import AutoConstants, DriveConstants, OIConstants

# from subsystems.drivesubsystem import DriveSubsystem
# # from subsystems.limelight_subsystem import LimelightSystem

# class Navigate(commands2.Command):
#     def __init__(self, drivetrain: DriveSubsystem) -> None:
#         super().__init__()
#         self.drivetrain = drivetrain
#         # self.limelight = limelight
#         self.addRequirements(drivetrain)

#     def initialize(self) -> None:
#         self.timer = wpilib.Timer()
#         self.timer.start()

#     def execute(self) -> None:
#         # results = self.limelight.get_results()

#         # tag = results.tag_id if results else -1

#         config = TrajectoryConfig(
#             AutoConstants.kMaxSpeedMetersPerSecond,
#             AutoConstants.kMaxAccelerationMetersPerSecondSquared,
#         )
#         # Add kinematics to ensure max speed is actually obeyed
#         config.setKinematics(DriveConstants.kDriveKinematics)

#         # An example trajectory to follow. All units in meters.
#         exampleTrajectory = TrajectoryGenerator.generateTrajectory(
#             # Start at the origin facing the +X direction
#             Pose2d(0, 0, Rotation2d(0)),
#             # Pass through these two interior waypoints, making an 's' curve path
#             [Translation2d(1, 1), Translation2d(2, -1)],
#             # End 3 meters straight ahead of where we started, facing forward
#             Pose2d(3, 0, Rotation2d(0)),
#             config,
#         )

#         exampleTrajectoryTwo = TrajectoryGenerator.generateTrajectory(
#             # Start at the origin facing the +X direction
#             Pose2d(0, 0, Rotation2d(0)),
#             # Pass through these two interior waypoints, making an 's' curve path
#             # [Translation2d(1, 1), Translation2d(2, -1)],
#             [],
#             # End 3 meters straight ahead of where we started, facing forward
#             Pose2d(3, 0, Rotation2d(0)),
#             config,
#         )

#         thetaController = ProfiledPIDControllerRadians(
#             AutoConstants.kPThetaController,
#             0,
#             0,
#             AutoConstants.kThetaControllerConstraints,
#         )
#         thetaController.enableContinuousInput(-math.pi, math.pi)

#         controller = HolonomicDriveController(
#             PIDController(AutoConstants.kPXController, 0, 0),
#             PIDController(AutoConstants.kPYController, 0, 0),
#             thetaController,
#         )

#         swerveControllerCommand = commands2.SwerveControllerCommand(
#             exampleTrajectory,
#             self.drivetrain.getPose,
#             DriveConstants.kDriveKinematics,
#             controller,
#             self.drivetrain.setModuleStates,
#             (self.drivetrain,),
#         )

#         # Reset odometry to the starting pose of the trajectory.
#         self.drivetrain.resetOdometry(exampleTrajectory.initialPose())

        

#         # swerveControllerCommand.execute()


#     def isFinished(self) -> bool: # pylint: disable=invalid-name
#         return False

#     def end(self, interrupted: bool) -> None:
#         self.drivetrain.drive(0, 0, 0, False, False)
