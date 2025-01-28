from rev import SparkMax, SparkAbsoluteEncoder, SparkClosedLoopController
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition
from constants import ModuleConstants

class MAXSwerveModule:
    def __init__(self, drivingCANId: int, turningCANId: int, chassisAngularOffset: float) -> None:
        """Constructs a MAXSwerveModule using REVLib 2025 configuration system"""
        self.chassisAngularOffset = chassisAngularOffset
        self.desiredState = SwerveModuleState(0.0, Rotation2d())

        # Initialize motors with new class names :cite[4]
        self.drivingSpark = SparkMax(drivingCANId, SparkMax.MotorType.kBrushless)
        self.turningSpark = SparkMax(turningCANId, SparkMax.MotorType.kBrushless)

        # Create configuration objects :cite[1]
        driving_config = SparkMaxConfig()
        turning_config = SparkMaxConfig()

        # Configure driving motor
        driving_config.idleMode(ModuleConstants.kDrivingMotorIdleMode)
        driving_config.smartCurrentLimit(ModuleConstants.kDrivingMotorCurrentLimit)
        driving_config.closedLoop.pid(
            ModuleConstants.kDrivingP,
            ModuleConstants.kDrivingI,
            ModuleConstants.kDrivingD
        ).ff(ModuleConstants.kDrivingFF)
        driving_config.outputRange(
            ModuleConstants.kDrivingMinOutput,
            ModuleConstants.kDrivingMaxOutput
        )

        # Configure turning motor
        turning_config.idleMode(ModuleConstants.kTurningMotorIdleMode)
        turning_config.smartCurrentLimit(ModuleConstants.kTurningMotorCurrentLimit)
        turning_config.closedLoop.pid(
            ModuleConstants.kTurningP,
            ModuleConstants.kTurningI,
            ModuleConstants.kTurningD
        ).ff(ModuleConstants.kTurningFF)
        turning_config.outputRange(
            ModuleConstants.kTurningMinOutput,
            ModuleConstants.kTurningMaxOutput
        )
        turning_config.closedLoop.positionWrapping(
            minInput=ModuleConstants.kTurningEncoderPositionPIDMinInput,
            maxInput=ModuleConstants.kTurningEncoderPositionPIDMaxInput
        )

        # Apply configurations :cite[1]
        self.drivingSpark.configure(driving_config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters)
        self.turningSpark.configure(turning_config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters)

        # Get encoders
        self.drivingEncoder = self.drivingSpark.getEncoder()
        self.turningEncoder = self.turningSpark.getAbsoluteEncoder()

        # Configure encoder conversions :cite[4]
        self.drivingEncoder.setPositionConversionFactor(ModuleConstants.kDrivingEncoderPositionFactor)
        self.drivingEncoder.setVelocityConversionFactor(ModuleConstants.kDrivingEncoderVelocityFactor)
        
        self.turningEncoder.setPositionConversionFactor(ModuleConstants.kTurningEncoderPositionFactor)
        self.turningEncoder.setVelocityConversionFactor(ModuleConstants.kTurningEncoderVelocityFactor)
        self.turningEncoder.setInverted(ModuleConstants.kTurningEncoderInverted)

        # Get closed-loop controllers :cite[4]
        self.drivingPID = self.drivingSpark.getClosedLoopController()
        self.turningPID = self.turningSpark.getClosedLoopController()

        # Initialize positions
        self.desiredState.angle = Rotation2d(self.turningEncoder.getPosition())
        self.drivingEncoder.setPosition(0)

    def getState(self) -> SwerveModuleState:
        return SwerveModuleState(
            self.drivingEncoder.getVelocity(),
            Rotation2d(self.turningEncoder.getPosition() - self.chassisAngularOffset)
        )

    def getPosition(self) -> SwerveModulePosition:
        return SwerveModulePosition(
            self.drivingEncoder.getPosition(),
            Rotation2d(self.turningEncoder.getPosition() - self.chassisAngularOffset)
        )

    def setDesiredState(self, desiredState: SwerveModuleState) -> None:
        correctedState = SwerveModuleState(
            desiredState.speed,
            desiredState.angle + Rotation2d(self.chassisAngularOffset)
        )
        
        optimizedState = SwerveModuleState.optimize(
            correctedState,
            Rotation2d(self.turningEncoder.getPosition())
        )

        # Set references using new control types :cite[4]
        self.drivingPID.setReference(optimizedState.speed, ControlType.kVelocity)
        self.turningPID.setReference(optimizedState.angle.radians(), ControlType.kPosition)

        self.desiredState = desiredState

    def resetEncoders(self) -> None:
        self.drivingEncoder.setPosition(0)