
import math
import commands2
import typing
from math import sqrt, cos, sin, radians, degrees
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveModuleState,
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
)
from wpilib import SmartDashboard
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem

from constants import DriveConstants, AlignConstants

class DriveCommand(commands2.Command):
    isAlligned = False
    isTagDetected = False
    
    def __init__(self, swerve_subsystem: DriveSubsystem, limelight_susbsystem: LimelightSystem, x: typing.Callable[[], float], y: typing.Callable[[], float], rot: typing.Callable[[], float], alignL: typing.Callable[[], bool], alignR: typing.Callable[[], bool], heading: typing.Callable[[], bool]) -> None:

        super().__init__()
        self.swerve = swerve_subsystem
        self.limelight = limelight_susbsystem
        self.y = y
        self.x = x
        self.rot = rot
        self.alignL = alignL
        self.alignR = alignR
        self.heading = heading
        self.addRequirements(swerve_subsystem)
        self.addRequirements(limelight_susbsystem)
        self.goalY = AlignConstants.kLeftAlignYOffset
        self.goalX = 0.0
        self.goalA = 0.0


    def execute(self) -> None:
        align = (self.alignL()) or (self.alignR())

        heading = self.heading()
        
        results = self.limelight.get_results()

        DriveCommand.isTagDetected = results is not None
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
                
        if self.alignL():
            self.goalX = AlignConstants.kLeftAlignXOffset
        if self.alignR():
            self.goalX = AlignConstants.kRightAlignXOffset
        
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

        # Keep some between the tag and robot
        # First adjustment is for distance from tag, second is for x offset
        ty = ty - (cos(yaw) * self.goalY) - (sin(yaw) * self.goalX)
        tx = -tx - (sin(yaw) * self.goalY) - (cos(yaw) * self.goalX)

        # ty = ty - cos((math.pi / 2) + (yaw * (math.pi / 180))  - math.atan2(self.goalY, self.goalX))
        # tx = tx - sin((math.pi / 2) + (yaw * (math.pi / 180)) -  math.atan2(self.goalY, self.goalX))

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
        print(dist)

        if dist > AlignConstants.kDistToSlow:
            dist = 1.0
        else:
            dist = sqrt(max(0.0, dist / AlignConstants.kDistToSlow))

        
        if abs(yaw) > AlignConstants.kRotDistToSlow:
            aDist = 1.0
        else:
            aDist = sqrt(max(0.0, abs(yaw)/AlignConstants.kRotDistToSlow))

        print ('distance', dist)
        print ('x speed', tx)
        print ('y speed', ty)
        print ('angle error', math.degrees(yaw))
        if (x == 0 and y == 0 and rotSign == 0):
            print('Already aligned')
            self.swerve.setX()
            DriveCommand.isAlligned = True
            
        else:
            self.swerve.drive(ChassisSpeeds(y * AlignConstants.kMaxNormalizedSpeed * sqrt(dist), -x * AlignConstants.kMaxNormalizedSpeed * sqrt(dist), -rotSign * AlignConstants.kMaxTurningSpeed * sqrt(aDist)), False, False)
            DriveCommand.isAlligned = False
#     def isFinished(self) -> bool:
#         return False
    

    def end(self, interrupted: bool) -> None:
        # self.swerve.drive(0, 0, 0, False, True)
        self.swerve.drive(ChassisSpeeds(0, 0, 0), False, True)
