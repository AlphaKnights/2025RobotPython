from commands2 import Subsystem

import wpilib

from rev import SparkMax, SparkMaxConfig, ClosedLoopConfig

from constants import ElevatorConstants

class ElevatorSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.elevatorMotorL = SparkMax(ElevatorConstants.kLeftMotorCanId, SparkMax.MotorType.kBrushless)
        self.elevatorMotorR = SparkMax(ElevatorConstants.kRightMotorCanId, SparkMax.MotorType.kBrushless)

        self.elevatorMotorLEncoder = self.elevatorMotorL.getAbsoluteEncoder()
        self.elevatorMotorLPID = self.elevatorMotorL.getClosedLoopController()

        l_config = SparkMaxConfig()
        l_config.IdleMode(int(SparkMax.IdleMode.kBrake))
        l_config.softLimit.forwardSoftLimit(10) \
            .reverseSoftLimit(10)
        
        l_config.encoder.positionConversionFactor(ElevatorConstants.kEncoderPositionFactor) \
            .velocityConversionFactor(ElevatorConstants.kEncoderVelocityFactor)
        
        l_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder) \
            .pid(ElevatorConstants.kP, ElevatorConstants.kI, ElevatorConstants.kD) \
            .outputRange(-1, 1) \
            

        r_config = SparkMaxConfig()
        r_config.IdleMode(int(SparkMax.IdleMode.kBrake))
        r_config.follow(ElevatorConstants.kLeftMotorCanId)

        self.elevatorMotorL.configure(l_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
        self.elevatorMotorR.configure(r_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)

        self.upperLimit = wpilib.DigitalInput(ElevatorConstants.kUpperLimit)
        self.lowerLimit = wpilib.DigitalInput(ElevatorConstants.kLowerLimit)
    
    def periodic(self) -> None:
        if (not self.upperLimit.get() and self.elevatorMotorL.get() > 0):
            self.elevatorMotorL.stopMotor()
            self.elevatorMotorR.stopMotor()
        
        if (not self.lowerLimit.get() and self.elevatorMotorL.get() < 0):
            self.elevatorMotorL.stopMotor()
            self.elevatorMotorR.stopMotor()

    def move(self, speed: float) -> None:
        if (not self.upperLimit.get() and speed > 0):
            self.elevatorMotorL.stopMotor()
            self.elevatorMotorR.stopMotor()
            return
        
        if (not self.lowerLimit.get() and speed < 0):
            self.elevatorMotorL.stopMotor()
            self.elevatorMotorR.stopMotor()
            return
    
        self.elevatorMotorL.set(speed)
        self.elevatorMotorR.set(-speed)

    def setPosition(self, position: float) -> None:
        self.elevatorMotorLPID.setReference(position, SparkMax.ControlType.kPosition)

    def stop(self) -> None:
        self.elevatorMotorL.stopMotor()
        self.elevatorMotorR.stopMotor()