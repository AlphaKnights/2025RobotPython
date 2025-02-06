from rev import SparkClosedLoopController, SparkMax, AbsoluteEncoder, RelativeEncoder, SparkMaxConfig, ClosedLoopConfig

from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition

from constants import ModuleConstants

class MAXSwerveModule:
    def __init__(
            self, drivingCANId: int, turningCANId: int, chassisAngularOffset: float
        ) -> None:

        self.drive_motor = SparkMax(drivingCANId, SparkMax.MotorType.kBrushless)
        self.turn_motor = SparkMax(turningCANId, SparkMax.MotorType.kBrushless)

        self.drive_encoder = self.drive_motor.getEncoder()
        self.turn_encoder = self.turn_motor.getAbsoluteEncoder()

        self.drive_PID_controller = self.drive_motor.getClosedLoopController()
        self.turn_PID_controller = self.turn_motor.getClosedLoopController()

        drivingConfig = SparkMaxConfig()

        drivingConfig.IdleMode(int(ModuleConstants.kDrivingMotorIdleMode)) 
        drivingConfig.smartCurrentLimit(ModuleConstants.kDrivingMotorCurrentLimit)

        drivingConfig.encoder.positionConversionFactor(ModuleConstants.kDrivingEncoderPositionFactor)
        drivingConfig.encoder.velocityConversionFactor(ModuleConstants.kDrivingEncoderVelocityFactor)

        drivingConfig.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder)
        drivingConfig.closedLoop.pid(ModuleConstants.kDrivingP, ModuleConstants.kDrivingI, ModuleConstants.kDrivingD)
        drivingConfig.closedLoop.velocityFF(ModuleConstants.kDrivingFF)
        drivingConfig.closedLoop.outputRange(ModuleConstants.kDrivingMinOutput, ModuleConstants.kDrivingMaxOutput)


        turningConfig = SparkMaxConfig()

        turningConfig.IdleMode(int(ModuleConstants.kTurningMotorIdleMode))
        turningConfig.smartCurrentLimit(ModuleConstants.kTurningMotorCurrentLimit)

        turningConfig.absoluteEncoder.inverted(True)
        turningConfig.absoluteEncoder.positionConversionFactor(ModuleConstants.kTurningEncoderPositionFactor)
        turningConfig.absoluteEncoder.velocityConversionFactor(ModuleConstants.kTurningEncoderVelocityFactor)

        turningConfig.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder)
        turningConfig.closedLoop.pid(ModuleConstants.kTurningP, ModuleConstants.kTurningI, ModuleConstants.kTurningD)
        turningConfig.closedLoop.outputRange(-1, 1)
        turningConfig.closedLoop.positionWrappingEnabled(True)
        turningConfig.closedLoop.positionWrappingInputRange(0, ModuleConstants.kTurningEncoderPositionPIDMaxInput)

        self.drive_motor.configure(drivingConfig, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)
        self.turn_motor.configure(turningConfig, SparkMax.ResetMode.kResetSafeParameters, SparkMax.PersistMode.kPersistParameters)

        self.chassisAngularOffset = chassisAngularOffset
        self.desiredState = SwerveModuleState(0.0, Rotation2d(self.turn_encoder.getPosition()))
        self.drive_encoder.setPosition(0)

    def getState(self) -> SwerveModuleState:
        return SwerveModuleState(self.drive_encoder.getVelocity(), Rotation2d(self.turn_encoder.getPosition() - self.chassisAngularOffset))
    
    def getPosition(self) -> SwerveModulePosition:
        return SwerveModulePosition(self.drive_encoder.getPosition(), Rotation2d(self.turn_encoder.getPosition() - self.chassisAngularOffset))
    
    def setDesiredState(self, desiredState: SwerveModuleState) -> None:
        correctedState = SwerveModuleState()
        correctedState.speed = desiredState.speed
        correctedState.angle = Rotation2d(desiredState.angle.radians() + self.chassisAngularOffset)
        
        correctedState.optimize(Rotation2d(self.turn_encoder.getPosition()))

        self.drive_PID_controller.setReference(correctedState.speed, SparkMax.ControlType.kVelocity)
        self.turn_PID_controller.setReference(correctedState.angle.radians(), SparkMax.ControlType.kPosition)

        self.desiredState = desiredState

    def resetEncoders(self) -> None:
        self.drive_encoder.setPosition(0)

    
