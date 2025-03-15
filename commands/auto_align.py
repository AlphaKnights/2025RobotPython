import commands2
import typing 

from wpilib import Timer

from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpimath.kinematics import ChassisSpeeds
from math import sqrt, radians, degrees, cos, sin

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

        self.x = 1
        self.y = 1
        self.a = 1

        self.timer = Timer()
        self.timer.start()

    def execute(self) -> None:
        results = self.limelight_subsystem.get_results()

        if results is None:
            self.drive_subsystem.setX()
            return
        
        self.timer.reset()

        tx = results.tx
        ty = results.ty
        yaw = radians(results.yaw)

        ty = ty - (cos(yaw) * self.goalY) - (sin(yaw) * self.goalX)
        tx = tx = -tx - (sin(yaw) * self.goalY) - (cos(yaw) * self.goalX)

        # Normalize the values
        ax = abs(tx)
        ay = abs(ty)

        if (ax > ay):
            y = ay/ax
            x = 1
        else:
            y = 1
            x = ax/ay

        if ty < 0:
            y *= -1

        if tx > 0: 
            x *= -1
        if abs(yaw) < AlignConstants.kAlignRotDeadzone:
            rotSign = 0
        else:
            rotSign = yaw/abs(yaw)

        if ax < AlignConstants.kAlignDeadzone:
            x = 0

        if ay < AlignConstants.kAlignDeadzone:
            y = 0

        dist = sqrt(tx**2 + ty**2)

        if dist > AlignConstants.kDistToSlow:
            dist = 1.0
        else:
            dist = dist / AlignConstants.kDistToSlow

        if dist < 0.5:
            dist = 0.5
        
        if abs(yaw) > AlignConstants.kRotDistToSlow:
            aDist = 1.0
        else:
            aDist = max(0.2, abs(yaw)/AlignConstants.kRotDistToSlow)
        
        self.x = x
        self.y = y
        self.a = rotSign

        self.drive_subsystem.drive(ChassisSpeeds(y * AlignConstants.kMaxNormalizedSpeed * dist, -x * AlignConstants.kMaxNormalizedSpeed * dist, -rotSign * AlignConstants.kMaxTurningSpeed * aDist), False, False)

    def isFinished(self) -> bool:
        results = self.limelight_subsystem.get_results()
        if results is None:
            self.drive_subsystem.drive(ChassisSpeeds(0,0,.4), False, False)
            return self.timer.get() > 5
        
        return self.x == 0 and self.y == 0 and self.a == 0
            
        




    def end(self, interrupted: bool = False) -> None:
        self.drive_subsystem.setX()

    def interrupted(self) -> None:
        self.end()