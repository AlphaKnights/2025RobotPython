import commands2
import typing 

from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem

class AutoAlign(commands2.Command):
    """Align to the closest AprilTag
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
        

        tx = results.tx
        ty = results.ty

        print(f'x: {tx}, y: {ty}')


        # Keep some between the tag and robot
        ty = ty - 0.35
        
        y = -0.1 if tx > 0 else 0.1
        x = 0.1 if ty > 0 else -0.1

        if abs(tx) < 0.01:
            y = 0

        if abs(ty) < 0.01:
            x = 0


        self.drive_subsystem.drive(x, y, 0, False, False)


    def isFinished(self) -> bool:
        results = self.limelight_subsystem.get_results()
        if results is None:
            return False

        tx = results.tx
        ty = results.ty

        ty = ty - 0.35


        # Define margin of error
        margin_of_error = 0.01

        # Check if the tag is within the margin of error
        return abs(tx) < margin_of_error and abs(ty) < margin_of_error

    def end(self, interrupted: bool = False) -> None:
        self.drive_subsystem.setX()

    def interrupted(self) -> None:
        self.end()
