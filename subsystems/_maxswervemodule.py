from rev import SparkMax, ClosedLoopConfig, EncoderConfig, SparkBaseConfig
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition

from constants import ModuleConstants

class MAXSwerveModule:
    def __init__(
            self, drivingCANId: int, turningCANId: int, chassisAngularOffset: float
    ) -> None:
        
        self.desiredState = SwerveModuleState(0.0, Rotation2d())
        self.chassisAngularOffset = chassisAngularOffset

        self.driving_motor = SparkMax(drivingCANId, SparkMax.MotorType.kBrushless)
        self.turning_motor = SparkMax(turningCANId, SparkMax.MotorType.kBrushless)

        self.driving_encoder = self.driving_motor.getEncoder()
        self.turning_encoder = self.turning_motor.getAbsoluteEncoder()

        self.driving_PID_controller = self.driving_motor.getClosedLoopController()
        self.turning_PID_controller = self.turning_motor.getClosedLoopController()

        # self.turning_motor.setInverted(ModuleConstants.kTurningEncoderInverted)

        driving_motor_config = SparkBaseConfig() 
        driving_motor_config.setIdleMode(ModuleConstants.kDrivingMotorIdleMode) 
        driving_motor_config.smartCurrentLimit(ModuleConstants.kDrivingMotorCurrentLimit)

        turning_motor_config = SparkBaseConfig() 
        turning_motor_config.setIdleMode(ModuleConstants.kTurningMotorIdleMode)
        turning_motor_config.smartCurrentLimit(ModuleConstants.kTurningMotorCurrentLimit)



        driving_motor_encoder_config = EncoderConfig()
        driving_motor_encoder_config.positionConversionFactor(ModuleConstants.kDrivingEncoderPositionFactor)
        driving_motor_encoder_config.velocityConversionFactor(ModuleConstants.kDrivingEncoderVelocityFactor)

        driving_motor_config.apply(driving_motor_encoder_config)


        turning_motor_encoder_config = EncoderConfig()
        turning_motor_encoder_config.positionConversionFactor(ModuleConstants.kTurningEncoderPositionFactor)
        turning_motor_encoder_config.velocityConversionFactor(ModuleConstants.kTurningEncoderVelocityFactor)
        # turning_motor_encoder_config.inverted(ModuleConstants.kTurningEncoderInverted)

        turning_motor_config.apply(turning_motor_encoder_config)



        driving_motor_PID_config = ClosedLoopConfig()
        driving_motor_PID_config.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder)
        driving_motor_PID_config.P(ModuleConstants.kDrivingP)
        driving_motor_PID_config.I(ModuleConstants.kDrivingI)
        driving_motor_PID_config.D(ModuleConstants.kDrivingD)
        driving_motor_PID_config.velocityFF(ModuleConstants.kDrivingFF)
        driving_motor_PID_config.outputRange(ModuleConstants.kDrivingMinOutput, ModuleConstants.kDrivingMaxOutput)
        
        driving_motor_config.apply(driving_motor_PID_config)



        turning_motor_PID_config = ClosedLoopConfig()
        turning_motor_PID_config.positionWrappingEnabled(True)
        turning_motor_PID_config.positionWrappingMinInput(ModuleConstants.kTurningEncoderPositionPIDMinInput)
        turning_motor_PID_config.positionWrappingMaxInput(ModuleConstants.kTurningEncoderPositionPIDMaxInput)

        turning_motor_PID_config.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder)
        turning_motor_PID_config.P(ModuleConstants.kTurningP)
        turning_motor_PID_config.I(ModuleConstants.kTurningI)
        turning_motor_PID_config.D(ModuleConstants.kTurningD)
        turning_motor_PID_config.velocityFF(ModuleConstants.kTurningFF)
        turning_motor_PID_config.outputRange(ModuleConstants.kTurningMinOutput, ModuleConstants.kTurningMaxOutput)

        turning_motor_config.apply(turning_motor_PID_config)

        self.driving_motor.configure(driving_motor_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
        self.turning_motor.configure(turning_motor_config, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)

        self.desiredState.angle = Rotation2d(self.turning_encoder.getPosition())
        self.driving_encoder.setPosition(0)

    def getState(self) -> SwerveModuleState:
        return SwerveModuleState(
            self.driving_encoder.getVelocity(),
            Rotation2d(self.turning_encoder.getPosition() - self.chassisAngularOffset)
        )
    
    def getPosition(self) -> SwerveModulePosition:
        return SwerveModulePosition(
            self.driving_encoder.getPosition(),
            Rotation2d(self.turning_encoder.getPosition() - self.chassisAngularOffset)
        )
    
    def setDesiredState(self, desiredState: SwerveModuleState) -> None:
        correctedDesiredState = SwerveModuleState()
        correctedDesiredState.speed = desiredState.speed
        correctedDesiredState.angle = desiredState.angle + Rotation2d(self.chassisAngularOffset)

        correctedDesiredState.optimize(Rotation2d(self.turning_encoder.getPosition()))

        self.driving_PID_controller.setReference(correctedDesiredState.speed, SparkMax.ControlType.kVelocity)

        self.turning_PID_controller.setReference(correctedDesiredState.angle.radians(), SparkMax.ControlType.kPosition)

        self.desiredState = correctedDesiredState

    def resetEncoders(self) -> None:
        self.driving_encoder.setPosition(0)
