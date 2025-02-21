# import phoenix6

# from commands2 import Subsystem
# import phoenix6.swerve

# from wpimath.geometry import Translation2d
# from wpimath.kinematics import SwerveModuleState, SwerveModulePosition

# class TalonSwerveModule(Subsystem):
#     def __init__(self,
#                     drive_motor_id: int,
#                     turn_motor_id: int,
#                     encoder_id: int,
#                     offset: float,
#                     index: int,
#                     location: Translation2d
#                 ) -> None:
#         super().__init__()

#         constants = phoenix6.swerve.SwerveModuleConstants()

#         constants.steer_motor_id=turn_motor_id
#         constants.drive_motor_id=drive_motor_id
#         constants.encoder_id=encoder_id
#         constants.encoder_offset=offset
#         constants.location_x=location.x
#         constants.location_y=location.y
#         constants.drive_motor_inverted=False
#         constants.steer_motor_inverted=False
#         constants.encoder_inverted=False
#         # constants.steer_motor_initial_configs.NeutralMode=phoenix6.signals.NeutralModeValue.BRAKE
#         # constants.drive_motor_initial_configs.NeutralMode=phoenix6.signals.NeutralModeValue.BRAKE
        

#         self.swerve_module = phoenix6.swerve.SwerveModule(
#             drive_motor_type=phoenix6.hardware.TalonFX,
#             steer_motor_type=phoenix6.hardware.TalonFX,
#             encoder_type=phoenix6.hardware.CANcoder,
#             canbus_name='',
#             drivetrain_id=0,
#             index=index,
#             constants=constants,
#         )

#         self.requests = self.swerve_module.ModuleRequest()

#     def getState(self) -> SwerveModuleState:
#         return self.swerve_module.get_current_state()
    
#     def getPosition(self) -> SwerveModulePosition:
#         return self.swerve_module.get_position(True)
    
#     def setDesiredState(self, state: SwerveModuleState) -> None:
#         self.requests.with_state(new_state=state)

#     def resetEncoders(self) -> None:
#         self.swerve_module.reset_position()