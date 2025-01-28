import commands2
from subsystems.elevatorsubsystem import ElevatorSubsystem

class ElevatorDownCommand(commands2.Command):
    def __init__(self, elevator_subsystem: ElevatorSubsystem) -> None:
        super().__init__()
        self.elevator = elevator_subsystem
        self.addRequirements(elevator_subsystem)

    def execute(self) -> None:
        self.elevator.move(-0.3)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        self.elevator.stop()