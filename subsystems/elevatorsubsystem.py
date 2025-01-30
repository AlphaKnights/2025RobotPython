import math
import typing

import wpilib

from commands2 import Subsystem

from rev import CANSparkMax


from constants import ElevatorConstants

class ElevatorSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.elevatorMotorL = CANSparkMax(ElevatorConstants.kLeftMotorCanId, CANSparkMax.MotorType.kBrushless)
        self.elevatorMotorR = CANSparkMax(ElevatorConstants.kRightMotorCanId, CANSparkMax.MotorType.kBrushless)

        self.elevatorMotorL.restoreFactoryDefaults()
        self.elevatorMotorR.restoreFactoryDefaults()

        self.elevatorMotorL.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.elevatorMotorL.setSoftLimit(CANSparkMax.SoftLimitDirection.kForward, 10)
        self.elevatorMotorL.setSoftLimit(CANSparkMax.SoftLimitDirection.kReverse, 10)

        self.elevatorMotorR.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.elevatorMotorR.setSoftLimit(CANSparkMax.SoftLimitDirection.kForward, 10)
        self.elevatorMotorR.setSoftLimit(CANSparkMax.SoftLimitDirection.kReverse, 10)
        
        self.elevatorMotorL.burnFlash()
        self.elevatorMotorR.burnFlash()

        self.upperLimit = wpilib.DigitalInput(ElevatorConstants.kUpperLimit)
        self.lowerLimit = wpilib.DigitalInput(ElevatorConstants.kLowerLimit)

    def periodic(self) -> None:
        # Timer/Encoder Limits -> Limit Switches -> Physical Barrier
        if (not self.upperLimit.get() and self.elevatorMotorL.get() > 0):
            self.elevatorMotorL.stopMotor()
        
        if (not self.lowerLimit.get() and self.elevatorMotorL.get() < 0):
            self.elevatorMotorL.stopMotor()
    
    def move(self, speed: float) -> None:
        self.elevatorMotorL.set(speed)
        
        if (not self.upperLimit.get() and self.elevatorMotorL.get() > 0):
            self.elevatorMotorL.stopMotor()
        
        if (not self.lowerLimit.get() and self.elevatorMotorL.get() < 0):
            self.elevatorMotorL.stopMotor()

    def stop(self) -> None:
        self.elevatorMotorL.stopMotor()
        self.elevatorMotorR.stopMotor()