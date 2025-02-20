import phoenix6
from commands2 import Command, Subsystem

import typing

class TalonSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.talon = phoenix6.hardware.TalonFX(1)
    
    def set(self, v: float) -> None:
        self.talon.set(v)

class RunMotor(Command):
    def __init__(self, talon: TalonSubsystem, v: typing.Callable[[], float]) -> None:
        super().__init__()
        self.talon = talon
        self.v = v

        self.addRequirements(talon)
    
    def execute(self) -> None:
        self.talon.set(self.v())
    
    def end(self, interrupted: bool) -> None:
        self.talon.set(0)