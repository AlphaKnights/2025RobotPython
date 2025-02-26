import commands2
from subsystems.elevator import ElevatorSubsystem

class ElevatorPosCommand(commands2.Command):
    def __init__(self, elevator_subsystem: ElevatorSubsystem, position: float) -> None:
        super().__init__()
        self.elevator = elevator_subsystem
        self.addRequirements(elevator_subsystem)
        self.position = position

    def execute(self) -> None:
        self.elevator.setPosition(self.position)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        # self.elevator.stop()
        pass