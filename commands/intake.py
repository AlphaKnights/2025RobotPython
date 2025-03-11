import commands2
import typing
from subsystems.coral_manipulator import CoralManipulator
from constants import LaunchConstants
class IntakeCommand(commands2.Command):
    def __init__(self, coral_manip: CoralManipulator) -> None:
        super().__init__()
        self.coral_manipulator = coral_manip
        self.addRequirements(coral_manip)

    def execute(self) -> None:
        self.coral_manipulator.launch(LaunchConstants.kLaunchSpeed)
        print("intaking")

    def isFinished(self) -> bool:
        return (self.coral_manipulator.rangeFinder.getRangeInches() <= 3.0)
    
    def end(self, interrupted: bool) -> None:
        self.coral_manipulator.stop()