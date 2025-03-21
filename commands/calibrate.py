import commands2
from constants import ElevatorConstants
from subsystems.elevator import ElevatorSubsystem
from wpilib import DigitalInput

class calibrateCommand(commands2.Command):
    def __init__(self, elevator_subsystem: ElevatorSubsystem) -> None:
        super().__init__()
        self.elevator = elevator_subsystem
        self.addRequirements(elevator_subsystem)

    def execute(self) -> None:
        if not self.elevator.elevatorMotorL.getForwardLimitSwitch():
            self.elevator.move(-0.1 * ElevatorConstants.kElevatorMaxSpeed)

    def isFinished(self) -> bool:
        if self.elevator.elevatorMotorL.getForwardLimitSwitch():
            self.elevator.stop()
            self.elevator.resetEncoders()
            return True
        return False
    
    def end(self, interrupted: bool) -> None:
        self.elevator.stop()