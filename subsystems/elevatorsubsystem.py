import math
import typing

import wpilib

from commands2 import Subsystem

from rev import CANSparkMax


class ElevatorSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.elevatorMotor = CANSparkMax(0, CANSparkMax.MotorType.kBrushless)
        self.elevatorMotor.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.elevatorMotor.setSoftLimit(CANSparkMax.SoftLimitDirection.kForward, 10)
        self.elevatorMotor.setSoftLimit(CANSparkMax.SoftLimitDirection.kReverse, 10)

    def periodic(self) -> None:
        # Safety Precautions
        # Timer/Encoder Limits -> Limit Switches -> Physical Barrier


        pass