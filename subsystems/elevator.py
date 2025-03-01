from commands2 import Subsystem

import wpilib
import phoenix6
import math

import phoenix6.swerve
import phoenix6.controls
from phoenix6.swerve.swerve_module_constants import SteerFeedbackType
from phoenix6.signals.spn_enums import FeedbackSensorSourceValue, InvertedValue
from phoenix6.controls import VelocityVoltage, PositionVoltage

from constants import ModuleConstants

from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition
from rev import SparkMax, SparkMaxConfig, ClosedLoopConfig

from constants import ElevatorConstants

class ElevatorSubsystem(Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.elevatorMotorL = phoenix6.hardware.TalonFX(ElevatorConstants.kLeftMotorCanId)
        self.elevatorMotorR = phoenix6.hardware.TalonFX(ElevatorConstants.kLeftMotorCanId)

        l_config = phoenix6.configs.TalonFXConfiguration()
        l_config.feedback.feedback_sensor_source = FeedbackSensorSourceValue.REMOTE_CANCODER

  

        l_config.motor_output.duty_cycle_neutral_deadband = 0

        l_config.slot0.k_p = ElevatorConstants.kP
        l_config.slot0.k_i = ElevatorConstants.kI
        l_config.slot0.k_d = ElevatorConstants.kD

        l_config.open_loop_ramps.duty_cycle_open_loop_ramp_period = 0
        l_config.closed_loop_ramps.duty_cycle_closed_loop_ramp_period = 0

        l_config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.COAST

        l_config.feedback.sensor_to_mechanism_ratio = 1
        l_config.closed_loop_general.continuous_wrap = False

        l_config.motor_output.inverted = InvertedValue(True)
        
##################
        l_config.softLimit.forwardSoftLimit(30) \
            .reverseSoftLimit(-10)
        l_config.softLimit.forwardSoftLimitEnabled(True) \
            .reverseSoftLimitEnabled(True)
        
        l_config.encoder.positionConversionFactor(ElevatorConstants.kEncoderPositionFactor) \
            .velocityConversionFactor(ElevatorConstants.kEncoderVelocityFactor)
        
        l_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder) \
            .pid(ElevatorConstants.kP, ElevatorConstants.kI, ElevatorConstants.kD) \
            .outputRange(-1, 1) \
            .positionWrappingEnabled(False)         
        ##########   
        
        
        r_config = phoenix6.configs.TalonFXConfiguration()
        r_config.feedback.feedback_remote_sensor_id = encoder_id
        r_config.feedback.feedback_sensor_source = FeedbackSensorSourceValue.REMOTE_CANCODER

        r_config.current_limits.supply_current_limit_enable = True
        r_config.current_limits.supply_current_limit = ElevatorConstants.kForwardSoftLimit
        
        r_config.motor_output.duty_cycle_neutral_deadband = 0

        r_config.slot0.k_p = ElevatorConstants.kP
        r_config.slot0.k_i = ElevatorConstants.kI
        r_config.slot0.k_d = ElevatorConstants.kD

        r_config.open_loop_ramps.duty_cycle_open_loop_ramp_period = 0
        r_config.closed_loop_ramps.duty_cycle_closed_loop_ramp_period = 0

        r_config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.COAST

        r_config.feedback.sensor_to_mechanism_ratio = 1
        r_config.closed_loop_general.continuous_wrap = False

        r_config.motor_output.inverted = InvertedValue(False)

        


        r_config.IdleMode(int(SparkMax.IdleMode.kCoast))
        r_config.softLimit.forwardSoftLimit(ElevatorConstants.kForwardSoftLimit) \
            .reverseSoftLimit(ElevatorConstants.kReverseSoftLimit)
        r_config.softLimit.forwardSoftLimitEnabled(True) \
            .reverseSoftLimitEnabled(True)
                
        r_config.closedLoop.setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder) \
            .pid(ElevatorConstants.kP, ElevatorConstants.kI, ElevatorConstants.kD) \
            .outputRange(-1, 1) \
            .positionWrappingEnabled(False)
        # r_config.follow(ElevatorConstants.kLeftMotorCanId, True)


        self.elevatorMotorL.configurator.apply(l_config)
        self.elevatorMotorR.configurator.apply(r_config)
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

        print("Left Position: " + str(self.elevatorMotorL.get_position()))
        print("Right Position: " + str(self.elevatorMotorR.get_position()))
        

    def move(self, speed: float) -> None:
        # if (not self.upperLimit.get() and speed > 0):
        #     self.elevatorMotorL.stopMotor()
        #     self.elevatorMotorR.stopMotor()
        #     return
        
        # if (not self.lowerLimit.get() and speed < 0):
        #     self.elevatorMotorL.stopMotor()
        #     self.elevatorMotorR.stopMotor()
        #     return
    
        self.elevatorMotorL.set_control(phoenix6.controls.PositionVoltage(speed))
        self.elevatorMotorL.set_control(phoenix6.controls.PositionVoltage(-speed))

    def setPosition(self, position: float) -> None:
        self.elevatorMotorL.set_position(position)
        self.elevatorMotorR.set_position(position)


    def stop(self) -> None:
        print("Stop")
        self.elevatorMotorL.stopMotor()
        self.elevatorMotorR.stopMotor()