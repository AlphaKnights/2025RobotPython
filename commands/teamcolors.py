import commands2
import typing
from subsystems.ledsubsystem import LEDSubsystem
class TeamColorsCommand(commands2.Command):
    def __init__(self, led_sub: LEDSubsystem) -> None:
        super().__init__()
        self.led = led_sub
        self.addRequirements(led_sub)

    def execute(self) -> None:
        self.led.teamLights()

    def isFinished(self) -> bool:
        return False
    
    def end(self, interrupted: bool) -> None:
        pass