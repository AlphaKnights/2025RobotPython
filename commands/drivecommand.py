import commands2
import typing
from math import sqrt, cos, sin, radians, degrees
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveModuleState,
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
)

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem

from constants import DriveConstants, AlignConstants

class DriveCommand(commands2.Command):
    def __init__(self, swerve_subsystem: DriveSubsystem, limelight_susbsystem: LimelightSystem, x: typing.Callable[[], float], y: typing.Callable[[], float], rot: typing.Callable[[], float], align: typing.Callable[[], bool], heading: typing.Callable[[], bool]) -> None:
        super().__init__()
        self.swerve = swerve_subsystem
        self.limelight = limelight_susbsystem
        self.y = y
        self.x = x
        self.rot = rot
        self.align = align
        self.heading = heading
        self.addRequirements(swerve_subsystem)
        self.addRequirements(limelight_susbsystem)
        self.goalY = 1
        self.goalX = 0
        self.goalA = 0

    def execute(self) -> None:
        align = self.align()
        heading = self.heading()

        if heading:
            self.swerve.zeroHeading()

        # if align:
        #     # self.swerve.resetEncoders()
        #     self.swerve.gyro.reset()
        #     return

        if not align:
            self.swerve.drive(
                ChassisSpeeds(
                    self.x()* DriveConstants.kMaxSpeedMetersPerSecond, 
                    self.y()* DriveConstants.kMaxSpeedMetersPerSecond, 
                    self.rot() * DriveConstants.kMaxAngularSpeed
                ), True, True)
            return
        
        results = self.limelight.get_results()

        if results is None:
            print('No tag detected')
            self.swerve.setX()
            return
        
        print('Aligning:', results.tag_id)

        if results is None:
            self.swerve.setX()
            return
        

        tx = results.tx
        ty = results.ty
        yaw = radians(results.yaw)

        print(f'x: {tx}, y: {ty}')

        goalXSign = self.goalX/abs(self.goalX)

        # Keep some between the tag and robot
        # First adjustment is for distance from tag, second is for x offset
        ty = ty - (cos(yaw) * self.goalY) - (sin(yaw) * self.goalX)
        tx = tx + (sin(yaw) * self.goalY) - (cos(yaw) * self.goalX)
        ta = yaw + self.goalA

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

        if tx < 0: 
            x *= -1

        a = ta/abs(ta)

        if ax < AlignConstants.kAlignDeadzone:
            print("dead X")
            x = 0

        if ay < AlignConstants.kAlignDeadzone:
            print("dead Y")
            y = 0

        if abs(yaw) < AlignConstants.kAlignRotDeadzone:
            a = 0

        dist = sqrt(tx**2 + ty**2)
        print(dist)

        if dist > AlignConstants.kDistToSlow:
            dist = 1.0
        else:
            dist = dist / AlignConstants.kDistToSlow

        if dist < 0.5:
            dist = 0.5
        
        if abs(degrees(ta)) > AlignConstants.kRotDistToSlow:
            aDist = 1.0
        else:
            aDist = max(0.2, abs(ta)/AlignConstants.kRotDistToSlow)

        print ('distance', dist)
        print ('x speed', x)
        print ('y speed', y)
        print ('angle error', ta)
        if (x == 0 and y == 0 and a == 0):
            print('Already aligned')
            self.swerve.setX()
        else:
            self.swerve.drive(ChassisSpeeds(y * AlignConstants.kMaxNormalizedSpeed * dist, -x * AlignConstants.kMaxNormalizedSpeed * dist, -a * AlignConstants.kMaxTurningSpeed * aDist), False, False)
        

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        # self.swerve.drive(0, 0, 0, False, True)
        self.swerve.drive(ChassisSpeeds(0, 0, 0), False, True)
