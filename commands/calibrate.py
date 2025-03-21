import commands2
from constants import ElevatorConstants
from subsystems.elevator import ElevatorSubsystem
from wpilib import DigitalInput

class calibrateCommand(commands2.Command):
    def __init__(self, elevator_subsystem: ElevatorSubsystem, bottom_limit : DigitalInput) -> None:
        super().__init__()
        self.elevator = elevator_subsystem
        self.addRequirements(elevator_subsystem)
        self.bottom_limit = bottom_limit

    def execute(self) -> None:
        if not self.bottom_limit.get():
            self.elevator.move(-0.1 * ElevatorConstants.kElevatorMaxSpeed)

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        self.elevator.stop()