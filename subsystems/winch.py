from rev import SparkMax, SparkMaxConfig, ClosedLoopConfig
from commands2 import Subsystem
from constants import winchConstants
class WinchSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.winchMotor = SparkMax(winchConstants.kMotorCanId, SparkMax.MotorType.kBrushless)

        self.winchMotorEncoder = self.winchMotor.getEncoder()
        self.winchMotorPID = self.winchMotor.getClosedLoopController()

        l_config = SparkMaxConfig()
        l_config.inverted(True)
        l_config.IdleMode(int(SparkMax.IdleMode.kCoast))
        l_config.softLimit.forwardSoftLimit(winchConstants.kForwardSoftLimit) \
            .reverseSoftLimit(winchConstants.kReverseSoftLimit)
        l_config.softLimit.forwardSoftLimitEnabled(True) \
            .reverseSoftLimitEnabled(True)
        
        l_config.encoder.positionConversionFactor(winchConstants.kEncoderPositionFactor) \
            .velocityConversionFactor(winchConstants.kEncoderVelocityFactor)
        
        l_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder) \
            .pid(winchConstants.kP, winchConstants.kI, winchConstants.kD) \
            .outputRange(-1, 1) \
            .positionWrappingEnabled(False)         
# 
        self.winchMotor.configure(l_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)

    def move(self, speed):
        self.winchMotor.set(speed)

    def movePos(self, pos):
        self.winchMotorPID.setReference(pos, SparkMax.ControlType.kPosition)

    def stop(self):
        self.winchMotor.stopMotor()
