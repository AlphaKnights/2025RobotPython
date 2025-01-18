import commands2

from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator

from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystems import LimelightSystem

class AutoAlign(commands2.CommandBase):
    def __init__(self, drive_subsystem: DriveSubsystem, limelight_subsystem: LimelightSystem) -> None:
        self.drive_subsystem = drive_subsystem
        self.limelight_subsystem = limelight_subsystem

        self.addRequirements(self.drive_subsystem)
        self.addRequirements(self.limelight_subsystem)

    def execute(self) -> None:
        results = self.limelight_subsystem.get_results()

        if results is None:
            return
        
        final_pos = Translation2d(results.tx, results.ty)
        final_rot = Rotation2d.fromDegrees(results.ta)

        self.drive_subsystem.navigate(final_pos, final_rot)


    def isFinished(self) -> bool:
        return False

    def end(self) -> None:
        self.drive_subsystem.setX()

    def interrupted(self) -> None:
        self.end()
