# import time

# import commands2
# import wpilib.drive

# from subsystems.drivesubsystem import DriveSubsystem
# from subsystems.limelight_subsystem import LimelightSystem

# class Navigate(commands2.CommandBase):
#     def __init__(self, drivetrain: DriveSubsystem, limelight: LimelightSystem) -> None:
#         super().__init__()
#         self.drivetrain = drivetrain
#         self.limelight = limelight
#         self.addRequirements(drivetrain, limelight)

#     def initialize(self) -> None:
#         self.timer = wpilib.Timer()
#         self.timer.start()

#     def execute(self) -> None:
#         results = self.limelight.get_results()

#         tag = results.tag_id if results else -1




#     def isFinished(self) -> bool: # pylint: disable=invalid-name
#         return False

#     def end(self) -> None:
#         self.drivetrain.arcade_drive(0, 0)