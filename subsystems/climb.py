from commands2 import Subsystem
from rev import SparkMax, SparkMaxConfig, ClosedLoopConfig

from constants import ClimbConstants

class Climb(Subsystem):
    def __init__(self):
        self.climbMotorL = SparkMax(ClimbConstants.kLeftMotorCanId, SparkMax.MotorType.kBrushless)
        self.climbMotorR = SparkMax(ClimbConstants.kRightMotorCanId, SparkMax.MotorType.kBrushless)

        self.climbMotorLEncoder = self.climbMotorL.getEncoder()
        self.climbMotorLPID = self.climbMotorL.getClosedLoopController()

        self.climbMotorREncoder = self.climbMotorR.getEncoder()
        self.climbMotorRPID = self.climbMotorR.getClosedLoopController()

        l_config = SparkMaxConfig()
        l_config.inverted(True)
        l_config.IdleMode(int(SparkMax.IdleMode.kCoast))
        l_config.softLimit.forwardSoftLimit(ClimbConstants.kForwardSoftLimit) \
            .reverseSoftLimit(ClimbConstants.kReverseSoftLimit)
        l_config.softLimit.forwardSoftLimitEnabled(True) \
            .reverseSoftLimitEnabled(True)
        
        l_config.encoder.positionConversionFactor(ClimbConstants.kEncoderPositionFactor) \
            .velocityConversionFactor(ClimbConstants.kEncoderVelocityFactor)
        
        l_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder) \
            .pid(ClimbConstants.kP, ClimbConstants.kI, ClimbConstants.kD) \
            .outputRange(-1, 1) \
            .positionWrappingEnabled(False)         
           

        r_config = SparkMaxConfig()
        r_config.inverted(False)
        r_config.IdleMode(int(SparkMax.IdleMode.kCoast))
        r_config.softLimit.forwardSoftLimit(ClimbConstants.kForwardSoftLimit) \
            .reverseSoftLimit(ClimbConstants.kReverseSoftLimit)
        r_config.softLimit.forwardSoftLimitEnabled(True) \
            .reverseSoftLimitEnabled(True)
        
        r_config.encoder.positionConversionFactor(ClimbConstants.kEncoderPositionFactor) \
            .velocityConversionFactor(ClimbConstants.kEncoderVelocityFactor)
        
        r_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder) \
            .pid(ClimbConstants.kP, ClimbConstants.kI, ClimbConstants.kD) \
            .outputRange(-1, 1) \
            .positionWrappingEnabled(False)
        # r_config.follow(ClimbConstants.kLeftMotorCanId, True)
# 
        self.climbMotorL.configure(l_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
        self.climbMotorR.configure(r_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
        
    def stop(self):
        self.climbMotorR.stopMotor()
        self.climbMotorL.stopMotor()

    def move(self, speed):
        self.climbMotorL.set(speed)
        self.climbMotorR.set(speed)

    def setPosition(self, position):
        print(self.climbMotorLEncoder.getPosition())
        self.climbMotorLPID.setReference(position, SparkMax.ControlType.kPosition)
        self.climbMotorRPID.setReference(position, SparkMax.ControlType.kPosition)