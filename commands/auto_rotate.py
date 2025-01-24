import commands2
import typing 

from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem

class AutoRotate(commands2.Command):
    """Rotate to the closest AprilTag
    """

    def __init__(self, drive_subsystem: DriveSubsystem, limelight_subsystem: LimelightSystem) -> None:
        self.drive_subsystem = drive_subsystem
        self.limelight_subsystem = limelight_subsystem

        self.addRequirements(self.drive_subsystem)
        self.addRequirements(self.limelight_subsystem)

    def execute(self) -> None:
        results = self.limelight_subsystem.get_results()

        if results is None:
            self.drive_subsystem.setX()
            return

        ta = results.ta

        print(f'a: {ta}')
        
        a = -0.2 if ta > 0 else 0.2

        if abs(a) < 0.01:
            a = 0

        self.drive_subsystem.drive(0, 0, a, False, False)


    def isFinished(self) -> bool:
        results = self.limelight_subsystem.get_results()
        if results is None:
            return False

        ta = results.ta

        # Define margin of error
        margin_of_error = 1

        # Check if the tag is within the margin of error
        return abs(ta) < margin_of_error

    def end(self, interrupted: bool = False) -> None:
        self.drive_subsystem.setX()

    def interrupted(self) -> None:
        self.end()
