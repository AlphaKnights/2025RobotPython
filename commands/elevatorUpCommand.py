import commands2
from constants import ElevatorConstants
from subsystems.elevator import ElevatorSubsystem

class ElevatorUpCommand(commands2.Command):
    def __init__(self, elevator_subsystem: ElevatorSubsystem) -> None:
        super().__init__()
        self.elevator = elevator_subsystem
        self.addRequirements(elevator_subsystem)

    def execute(self) -> None:
        self.elevator.move(0.1 * ElevatorConstants.kElevatorMaxSpeed)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        self.elevator.stop()