from commands2 import Subsystem

import wpilib

from rev import SparkMax, SparkMaxConfig, ClosedLoopConfig

from constants import ElevatorConstants

class ElevatorSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.elevatorMotorL = SparkMax(ElevatorConstants.kLeftMotorCanId, SparkMax.MotorType.kBrushless)
        self.elevatorMotorR = SparkMax(ElevatorConstants.kRightMotorCanId, SparkMax.MotorType.kBrushless)

        self.elevatorMotorLEncoder = self.elevatorMotorL.getEncoder()
        self.elevatorMotorLPID = self.elevatorMotorL.getClosedLoopController()

        self.elevatorMotorREncoder = self.elevatorMotorR.getEncoder()
        self.elevatorMotorRPID = self.elevatorMotorR.getClosedLoopController()

        l_config = SparkMaxConfig()
        l_config.inverted(True)
        l_config.IdleMode(int(SparkMax.IdleMode.kCoast))
        l_config.softLimit.forwardSoftLimit(ElevatorConstants.kForwardSoftLimit) \
            .reverseSoftLimit(ElevatorConstants.kReverseSoftLimit)
        l_config.softLimit.forwardSoftLimitEnabled(True) \
            .reverseSoftLimitEnabled(True)
        
        l_config.encoder.positionConversionFactor(ElevatorConstants.kEncoderPositionFactor) \
            .velocityConversionFactor(ElevatorConstants.kEncoderVelocityFactor)
        
        l_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder) \
            .pid(ElevatorConstants.kP, ElevatorConstants.kI, ElevatorConstants.kD) \
            .outputRange(-1, 1) \
            .positionWrappingEnabled(False)         
           

        r_config = SparkMaxConfig()
        r_config.inverted(False)
        r_config.IdleMode(int(SparkMax.IdleMode.kCoast))
        r_config.softLimit.forwardSoftLimit(ElevatorConstants.kForwardSoftLimit) \
            .reverseSoftLimit(ElevatorConstants.kReverseSoftLimit)
        r_config.softLimit.forwardSoftLimitEnabled(True) \
            .reverseSoftLimitEnabled(True)
        
        r_config.encoder.positionConversionFactor(ElevatorConstants.kEncoderPositionFactor) \
            .velocityConversionFactor(ElevatorConstants.kEncoderVelocityFactor)
        
        r_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder) \
            .pid(ElevatorConstants.kP, ElevatorConstants.kI, ElevatorConstants.kD) \
            .outputRange(-1, 1) \
            .positionWrappingEnabled(False)
        # r_config.follow(ElevatorConstants.kLeftMotorCanId, True)
# 
        self.elevatorMotorL.configure(l_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
        self.elevatorMotorR.configure(r_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)

        # self.upperLimit = wpilib.DigitalInput(ElevatorConstants.kUpperLimit)
        # self.lowerLimit = wpilib.DigitalInput(ElevatorConstants.kLowerLimit)
    
    def periodic(self) -> None:
        # if (not self.upperLimit.get() and self.elevatorMotorL.get() > 0):
        #     self.elevatorMotorL.stopMotor()
        #     self.elevatorMotorR.stopMotor()
        #     return
        
        # if (not self.lowerLimit.get() and self.elevatorMotorL.get() < 0):
        #     self.elevatorMotorL.stopMotor()
        #     self.elevatorMotorR.stopMotor()
        #     return

        # if (not self.lowerLimit.get()):
        #     print ("Lower On")
        
        # if (not self.upperLimit.get()):
        #     print ("Upper On")

        if self.elevatorMotorL.getForwardLimitSwitch():
            self.resetEncoders()


        # print("Left Position: " + str(self.elevatorMotorLEncoder.getPosition()))
        # print("Right Position: " + str(self.elevatorMotorREncoder.getPosition()))
        return

    def resetEncoders(self) -> None:
        self.elevatorMotorLEncoder.setPosition(0)
        self.elevatorMotorREncoder.setPosition(0)

    def move(self, speed: float) -> None:
        # if (not self.upperLimit.get() and speed > 0):
        #     self.elevatorMotorL.stopMotor()
        #     self.elevatorMotorR.stopMotor()
        #     return
        
        # if (not self.lowerLimit.get() and speed < 0):
        #     self.elevatorMotorL.stopMotor()
        #     self.elevatorMotorR.stopMotor()
        #     return
    
        self.elevatorMotorL.set(speed)
        self.elevatorMotorR.set(speed)
        

    def setPosition(self, position: float) -> None:
        print(self.elevatorMotorLEncoder.getPosition())
        self.elevatorMotorLPID.setReference(position, SparkMax.ControlType.kPosition)
        self.elevatorMotorRPID.setReference(position, SparkMax.ControlType.kPosition)


    def stop(self) -> None:
        print("Stop")
        self.elevatorMotorL.stopMotor()
        self.elevatorMotorR.stopMotor()