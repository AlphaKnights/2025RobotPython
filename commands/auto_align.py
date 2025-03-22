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

    def execute(self) -> None:
        results = self.limelight_subsystem.get_results()

        if results is None:
            # self.drive_subsystem.setX()
            return
        
        self.timer.reset()

        tx = results.tx
        ty = results.ty
        yaw = radians(results.yaw)

        print("tx: ", tx, "ty: ", ty, "angle", yaw)

        ty = ty - (cos(yaw) * self.goalY) - (sin(yaw) * self.goalX)
        tx = -tx - (sin(yaw) * self.goalY) - (cos(yaw) * self.goalX)

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
            rotSign = int(yaw/abs(yaw))

        deadzone = 0.05 if self.goalX < 0 else AlignConstants.kAlignDeadzone
        
        if ax < deadzone:
            print("dead X")
            x = 0

        if ay < deadzone:
            print("dead Y")
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

        self.drive_subsystem.drive(
            speeds = ChassisSpeeds(
                vx = y * AlignConstants.kMaxNormalizedSpeed * sqrt(dist), 
                vy = -x * AlignConstants.kMaxNormalizedSpeed * sqrt(dist), 
                omega = -rotSign * AlignConstants.kMaxTurningSpeed * sqrt(aDist)
            ), 
            fieldRelative=False, 
            rateLimit=False
            )

    def isFinished(self) -> bool:
        results = self.limelight_subsystem.get_results()
        if results is None:
            time = self.timer.get()
            print('time: ', time)
            # If more than a 5 seconds passes then there is no tag
            if time > 5:
                return True
            
            # If more than a second but less than 1 second passes, then spin in place until a tag is found
            if time > 1:
                self.drive_subsystem.drive(
                    speeds=ChassisSpeeds(
                        vx=0,
                        vy=0,
                        omega=5), 
                    fieldRelative=False, 
                    rateLimit=False
                )
                return False
            
            self.drive_subsystem.setX()
        return self.x == 0 and self.y == 0 and self.a == 0

    def initialize(self) -> None:
        self.timer.start()
        self.timer.reset()
        return super().initialize()

    def end(self, interrupted: bool = False) -> None:
        self.drive_subsystem.setX()
