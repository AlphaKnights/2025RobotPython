import commands2
from constants import winchConstants
from subsystems.winch import WinchSubsystem

class WinchMoveCommand(commands2.Command):
    def __init__(self, winch_subsystem: WinchSubsystem, speed) -> None:
        super().__init__()
        self.winch = winch_subsystem
        self.addRequirements(winch_subsystem)
        self.speed = speed

    def execute(self) -> None:
        self.winch.move(self.speed)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        self.winch.stop()