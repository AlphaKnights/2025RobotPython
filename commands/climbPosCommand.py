import commands2
from subsystems.climb import Climb

class ElevatorPosCommand(commands2.Command):
    def __init__(self, climb_subsystem: Climb, position: float) -> None:
        super().__init__()
        self.climb = climb_subsystem
        self.addRequirements(climb_subsystem)
        self.position = position

    def execute(self) -> None:
        self.climb.setPosition(self.position)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        # self.elevator.stop()
        pass