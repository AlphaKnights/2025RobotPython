import commands2
import typing
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem

class DriveCommand(commands2.Command):
    def __init__(self, swerve_subsystem: DriveSubsystem, limelight_susbsystem: LimelightSystem, x: typing.Callable[[], float], y: typing.Callable[[], float], rot: typing.Callable[[], float], align: typing.Callable[[], bool]) -> None:
        super().__init__()
        self.swerve = swerve_subsystem
        self.limelight = limelight_susbsystem
        self.y = y
        self.x = x
        self.rot = rot
        self.align = align
        self.addRequirements(swerve_subsystem)
        self.addRequirements(limelight_susbsystem)

    def execute(self) -> None:
        align = self.align()
        if not align:
            self.swerve.drive(self.x(), self.y(), self.rot(), True, True)
            return
        
        results = self.limelight.get_results()

        if results is None:
            print('No limelight detected')
            self.swerve.setX()
            return
        
        print('Aligning:', results.tag_id)

        tx = results.tx
        ty = results.ty

        print(f'x: {tx}, y: {ty}')


        # Keep some between the tag and robot
        ty = ty - 0.25
        
        y = -0.1 if tx > 0 else 0.1
        x = 0.1 if ty > 0 else -0.1

        if abs(tx) < 0.01:
            y = 0

        if abs(ty) < 0.01:
            x = 0

        if y != 0 or x != 0:
            self.swerve.drive(x, y, 0, False, False)
            return

        ta = results.ta

        print(f'a: {ta}')
        
        a = -0.2 if ta > 0 else 0.2

        if abs(a) > 0.01:
            self.swerve.drive(0, 0, a, False, False)
            return
        
        print('Already aligned')
        

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        self.swerve.drive(0, 0, 0, False, True)