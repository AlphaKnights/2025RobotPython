import phoenix6
import math

from constants import ModuleConstants

from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState

class TalonSwerveModule:
    def __init__(self,
                    drive_motor_id: int,
                    turn_motor_id: int,
                    encoder_id: int,
                    offset: float
                ) -> None:
        self.drive_motor = phoenix6.hardware.TalonFX(drive_motor_id)
        self.turn_motor = phoenix6.hardware.TalonFX(turn_motor_id)
        self.encoder = phoenix6.hardware.CANcoder(encoder_id)

        drive_motor_config = phoenix6.configs.TalonFXConfiguration()

        drive_motor_config.current_limits.supply_current_limit_enable = True
        drive_motor_config.current_limits.supply_current_limit = ModuleConstants.kDrivingMotorCurrentLimit
        
        drive_motor_config.slot0.k_p = ModuleConstants.kDrivingP
        drive_motor_config.slot0.k_i = ModuleConstants.kDrivingI
        drive_motor_config.slot0.k_d = ModuleConstants.kDrivingD

        drive_motor_config.open_loop_ramps.duty_cycle_open_loop_ramp_period = 0
        drive_motor_config.closed_loop_ramps.duty_cycle_closed_loop_ramp_period = 0

        drive_motor_config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE

        drive_motor_config.feedback.sensor_to_mechanism_ratio = ModuleConstants.kDrivingEncoderPositionFactor

        # Replace to_deserialize with string very weird workaround
        self.drive_motor.configurator.apply(drive_motor_config)

        turn_motor_config = phoenix6.configs.TalonFXConfiguration()

        turn_motor_config.current_limits.supply_current_limit_enable = True
        turn_motor_config.current_limits.supply_current_limit = ModuleConstants.kTurningMotorCurrentLimit

        turn_motor_config.slot0.k_p = ModuleConstants.kTurningP
        turn_motor_config.slot0.k_i = ModuleConstants.kTurningI
        turn_motor_config.slot0.k_d = ModuleConstants.kTurningD

        turn_motor_config.open_loop_ramps.duty_cycle_open_loop_ramp_period = 0
        turn_motor_config.closed_loop_ramps.duty_cycle_closed_loop_ramp_period = 0

        turn_motor_config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE

        turn_motor_config.feedback.sensor_to_mechanism_ratio = ModuleConstants.kTurningEncoderPositionFactor

        self.turn_motor.configurator.apply(turn_motor_config)

        self.offset = offset
        self.desired_state = SwerveModuleState(0.0, Rotation2d(self.encoder.get_position().value_as_double))
        self.encoder.set_position(0)
    
    def get_state(self) -> SwerveModuleState:
        return SwerveModuleState(self.encoder.get_velocity().value_as_double, Rotation2d(self.encoder.get_position().value_as_double - self.offset))
    
    def get_position(self) -> Rotation2d:
        return Rotation2d(self.encoder.get_position().value_as_double - self.offset)
    
    def set_desired_state(self, desired_state: SwerveModuleState) -> None:
        corrected_state = SwerveModuleState()
        corrected_state.speed = desired_state.speed
        corrected_state.angle = Rotation2d(desired_state.angle.radians() + self.offset)

        corrected_state.optimize(Rotation2d(self.encoder.get_position().value_as_double))

        self.drive_motor.set(desired_state.speed)
        self.turn_motor.set_position(desired_state.angle.radians() / (2* math.pi))

        self.desired_state = desired_state

    def reset_encoders(self) -> None:
        self.encoder.set_position(0)


                 