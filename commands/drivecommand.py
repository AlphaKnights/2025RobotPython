import commands2
import typing
from subsystems.drivesubsystem import DriveSubsystem

class DriveCommand(commands2.Command):
    def __init__(self, swerve_subsystem: DriveSubsystem, x: typing.Callable[[], float], y: typing.Callable[[], float], rot: typing.Callable[[], float], align: typing.Callable[[], bool]) -> None:
        super().__init__()
        self.swerve = swerve_subsystem
        self.y = y
        self.x = x
        self.rot = rot
        self.addRequirements(swerve_subsystem)

    def execute(self) -> None:
        self.swerve.drive(self.x(), self.y(), self.rot(), True, True)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        self.swerve.drive(0, 0, 0, False, True)