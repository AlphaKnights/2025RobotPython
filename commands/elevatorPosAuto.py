import commands2
from subsystems.elevator import ElevatorSubsystem

class ElevatorPosAutoCommand(commands2.Command):
    def __init__(self, elevator_subsystem: ElevatorSubsystem, position: float) -> None:
        super().__init__()
        self.elevator = elevator_subsystem
        self.addRequirements(elevator_subsystem)
        self.position = position

    def execute(self) -> None:
        self.elevator.setPosition(self.position)

    def isFinished(self) -> bool:
        return (self.elevator.elevatorMotorLEncoder.getPosition() - self.position <= 1.0) and (self.elevator.elevatorMotorREncoder.getPosition() - self.position <= 1.0)
    
    def end(self, interrupted: bool) -> None:
        # self.elevator.stop()
        pass