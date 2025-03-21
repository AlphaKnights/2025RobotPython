import commands2
from subsystems.winch import WinchSubsystem

class WinchPosCommand(commands2.Command):
    def __init__(self, winch_subsystem: WinchSubsystem, position: float) -> None:
        super().__init__()
        self.winch = winch_subsystem
        self.addRequirements(winch_subsystem)
        self.position = position

    def execute(self) -> None:
        self.winch.movePos(self.position)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        # self.elevator.stop()
        pass