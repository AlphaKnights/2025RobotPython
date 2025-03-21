import wpilib
import commands2.button
import wpimath
from constants import OIConstants
from commands.drivecommand import DriveCommand
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.limelight_subsystem import LimelightSystem


class DriverController():
    def __init__(self, driveSub: DriveSubsystem, limeSub: LimelightSystem, buttonBoard: commands2.button.CommandJoystick) -> None:
        self.robotDrive = driveSub
        self.limelight = limeSub
        self.buttonBoard = buttonBoard

        self.joystickDrive = wpilib.Joystick(OIConstants.kDriverControllerPort).getName() == "Logitech Extreme 3D"

        self.controller = wpilib.Joystick(OIConstants.kDriverControllerPort)

        if self.joystickDrive:
            self.joystickDriverController = wpilib.Joystick(OIConstants.kDriverControllerPort)
        else:
            self.xBoxDriverController = wpilib.XboxController(OIConstants.kDriverControllerPort)

    def setDefaultCommands(self) -> None:
        # Configure default commands
        print(self.joystickDrive)
        if self.joystickDrive:
            self.robotDrive.setDefaultCommand(
                DriveCommand(
                    self.robotDrive,
                    self.limelight,
                    lambda:
                        -wpimath.applyDeadband(
                            self.joystickDriverController.getRawAxis(1), OIConstants.kDriveDeadband
                        ) * (-self.joystickDriverController.getRawAxis(3) + 1)/2,
                    lambda:
                        -wpimath.applyDeadband(
                            self.joystickDriverController.getRawAxis(0), OIConstants.kDriveDeadband
                        ) * (-self.joystickDriverController.getRawAxis(3) + 1)/2,
                    lambda:
                        -wpimath.applyDeadband(
                            self.joystickDriverController.getRawAxis(2), OIConstants.kDriveDeadband
                        ) * (-self.joystickDriverController.getRawAxis(3) + 1)/2,
                    # lambda: 0.4 if self.joystickDriverController.getRawButton(11) else 0,
                    # lambda: 0,
                    
                    # lambda: 0,

                    lambda: self.buttonBoard.button(OIConstants.kAlignLeftButton).getAsBoolean(),
                    lambda: self.buttonBoard.button(OIConstants.kAlignRightButton).getAsBoolean(),
                    lambda: self.joystickDriverController.getRawButton(11)
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
                            self.xBoxDriverController.getLeftY(), OIConstants.kDriveDeadband
                        ),
                    lambda:
                        -wpimath.applyDeadband(
                            self.xBoxDriverController.getLeftX(), OIConstants.kDriveDeadband
                        ),
                    lambda:
                        -wpimath.applyDeadband(
                            self.xBoxDriverController.getRawAxis(2), OIConstants.kDriveDeadband
                        ),
                    lambda: self.buttonBoard.button(OIConstants.kAlignLeftButton).getAsBoolean(),
                    lambda: self.buttonBoard.button(OIConstants.kAlignRightButton).getAsBoolean(),
                    self.xBoxDriverController.getXButton
                    ),
                )
