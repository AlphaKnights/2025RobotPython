import wpilib
import wpimath
from constants import OIConstants
from commands.drivecommand import DriveCommand
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem


class DriverController():
    def __init__(self, driveSub: DriveSubsystem, limeSub: LimelightSystem) -> None:
        self.robotDrive = driveSub
        self.limelight = limeSub

        self.joystickDrive = False
        if wpilib.Joystick(OIConstants.kDriverControllerPort).getName() == "Logitech Extreme 3D":
            self.joystickDrive = True
        # The driver's controller
        self.joystickDrive = True

        if self.joystickDrive:
            self.driverController = wpilib.Joystick(OIConstants.kDriverControllerPort)
        else:
            self.driverController = wpilib.XboxController(OIConstants.kDriverControllerPort)

    def setDefaultCommands(self) -> None:
        # Configure default commands
        if self.joystickDrive:
            self.robotDrive.setDefaultCommand(
                DriveCommand(
                    self.robotDrive,
                    self.limelight,
                    lambda:
                        -wpimath.applyDeadband(
                            self.driverController.getRawAxis(1), OIConstants.kDriveDeadband
                        ) * (-self.driverController.getRawAxis(3) + 1)/2,
                    lambda:
                        -wpimath.applyDeadband(
                            self.driverController.getRawAxis(0), OIConstants.kDriveDeadband
                        ) * (-self.driverController.getRawAxis(3) + 1)/2,
                    lambda:
                        -wpimath.applyDeadband(
                            self.driverController.getRawAxis(2), OIConstants.kDriveDeadband
                        ) * (-self.driverController.getRawAxis(3) + 1)/2,
                    # lambda: 0.4 if self.driverController.getRawButton(11) else 0,
                    # lambda: 0,
                    
                    # lambda: 0,

                    lambda: self.driverController.getRawButton(12),
                    lambda: self.driverController.getRawButton(11)
                    ),
                )
        else:
            self.robotDrive.setDefaultCommand(
                # The left stick controls translation of the robot.
                # Turning is controlled by the X axis of the right stick.
                DriveCommand(
                    self.robotDrive,
                    self.limelight,
                    lambda:
                        -wpimath.applyDeadband(
                            self.driverController.getLeftY(), OIConstants.kDriveDeadband
                        ),
                    lambda:
                        -wpimath.applyDeadband(
                            self.driverController.getLeftX(), OIConstants.kDriveDeadband
                        ),
                    lambda:
                        -wpimath.applyDeadband(
                            self.driverController.getRawAxis(2), OIConstants.kDriveDeadband
                        ),
                    self.driverController.getAButton,
                    self.driverController.getXButton
                    ),
                )