import commands2
from constants import ElevatorConstants
from subsystems.elevator import ElevatorSubsystem

class ElevatorDownCommand(commands2.Command):
    def __init__(self, climb_subsystem: ElevatorSubsystem) -> None:
        super().__init__()
        self.climb = climb_subsystem
        self.addRequirements(climb_subsystem)

    def execute(self) -> None:
        self.climb.move(0.1 * ElevatorConstants.kElevatorMaxSpeed)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        self.climb.stop()