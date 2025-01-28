import commands2
import typing 

from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from math import sqrt

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem

from constants import AlignConstants

class AutoAlign(commands2.Command):
    """Align to the closest AprilTag
    """

    def __init__(self, drive_subsystem: DriveSubsystem, limelight_subsystem: LimelightSystem, gY: float, gX: float) -> None:
        self.drive_subsystem = drive_subsystem
        self.limelight_subsystem = limelight_subsystem

        self.addRequirements(self.drive_subsystem)
        self.addRequirements(self.limelight_subsystem)
    
        self.goalY = gY #offset (negative leaves further from the apriltag)
        self.goalX = gX #offset (positive to the right)

    def execute(self) -> None:
        results = self.limelight_subsystem.get_results()

        if results is None:
            self.drive_subsystem.setX()
            return
        

        tx = results.tx
        ty = results.ty
        ta = results.ta

        print(f'x: {tx}, y: {ty}')


        # Keep some between the tag and robot
        ty = ty + self.goalY
        tx = tx + self.goalY

        if (tx > ty):
            y = ty/tx
            x = 1
        else:
            y = 1
            x = tx/ty

        if abs(tx) < AlignConstants.kAlignDeadzone:
            y = 0

        if abs(ty) < AlignConstants.kAlignDeadzone:
            x = 0

        dist = sqrt(tx**2 + ty**2)

        if dist > AlignConstants.kDistToSlow:
            dist = 1.0
        else:
            dist = dist / AlignConstants.kDistToSlow

        self.drive_subsystem.drive(x * AlignConstants.kMaxNormalizedSpeed * dist, y * AlignConstants.kMaxNormalizedSpeed * dist, 0, False, False)


    def isFinished(self) -> bool:
        results = self.limelight_subsystem.get_results()
        if results is None:
            return False

        tx = results.tx
        ty = results.ty

        ty = ty - 0.25


        # Define margin of error
        margin_of_error = 0.01

        # Check if the tag is within the margin of error
        return abs(tx) < margin_of_error and abs(ty) < margin_of_error

    def end(self, interrupted: bool = False) -> None:
        self.drive_subsystem.setX()

    def interrupted(self) -> None:
        self.end()
