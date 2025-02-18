# import swervepy
# import swervepy.impl
# from wpimath.geometry import Translation2d, Rotation2d
# from pint import Quantity

# from commands2 import Subsystem
# from constants import DriveConstants, ModuleConstants

# class drivetrain(Subsystem):
#     """
#     The DriveSubsystem class is a subsystem that controls the swerve drive of the robot.
#     """
#     def __init__(self) -> None:
#         super().__init__()

#         drive_params = swervepy.impl.TypicalDriveComponentParameters(
#             wheel_circumference=ModuleConstants.kWheelCircumferenceMeters * swervepy.u.meter,
#             gear_ratio=ModuleConstants.kDrivingEncoderPositionFactor,
#             max_speed=ModuleConstants.kDriveWheelFreeSpeedRps * swervepy.u.radian_per_second,
#             open_loop_ramp_rate=0,
#             closed_loop_ramp_rate=0,
#             continuous_current_limit=ModuleConstants.kDrivingMotorCurrentLimit,
#             peak_current_limit=ModuleConstants.kDrivingMotorCurrentLimit,
#             peak_current_duration=0.1,
#             neutral_mode=swervepy.impl.NeutralMode.BRAKE,
#             kP=ModuleConstants.kDrivingP,
#             kI=ModuleConstants.kDrivingI,
#             kD=ModuleConstants.kDrivingD,
#             kS=0,
#             kV=0,
#             kA=0,
#             invert_motor=False
#         )

#         turning_params = swervepy.impl.TypicalAzimuthComponentParameters(
#             gear_ratio=ModuleConstants.kTurningEncoderPositionFactor,
#             max_angular_velocity=ModuleConstants.kTurningEncoderVelocityFactor * swervepy.u.radian_per_second,
#             ramp_rate=0,
#             continuous_current_limit=ModuleConstants.kTurningMotorCurrentLimit,
#             peak_current_limit=ModuleConstants.kTurningMotorCurrentLimit,
#             peak_current_duration=0.1,
#             neutral_mode=swervepy.impl.NeutralMode.BRAKE,
#             kP=ModuleConstants.kTurningP,
#             kI=ModuleConstants.kTurningI,
#             kD=ModuleConstants.kTurningD,
#             invert_motor=False
#         )

#         fl = swervepy.impl.CoaxialSwerveModule(
#                 drive=swervepy.impl.Falcon500CoaxialDriveComponent(
#                     id_=DriveConstants.kFrontLeftDrivingId,
#                     parameters=drive_params,
#                 ),
#                 azimuth=swervepy.impl.Falcon500CoaxialAzimuthComponent(
#                     id_=DriveConstants.kFrontLeftTurningId,
#                     azimuth_offset=Rotation2d(DriveConstants.kFrontLeftChassisAngularOffset),
#                     parameters=turning_params,
#                     absolute_encoder=swervepy.impl.AbsoluteCANCoder(DriveConstants.kFrontLeftCANCoderId)
#                 ),
#                 placement=DriveConstants.kFrontLeftPosition,
#             )
        
#         fr = swervepy.impl.CoaxialSwerveModule(
#                 drive=swervepy.impl.Falcon500CoaxialDriveComponent(
#                     id_=DriveConstants.kFrontRightDrivingId,
#                     parameters=drive_params,
#                 ),
#                 azimuth=swervepy.impl.Falcon500CoaxialAzimuthComponent(
#                     id_=DriveConstants.kFrontRightTurningId,
#                     azimuth_offset=Rotation2d(DriveConstants.kFrontRightChassisAngularOffset),
#                     parameters=turning_params,
#                     absolute_encoder=swervepy.impl.AbsoluteCANCoder(DriveConstants.kFrontRightCANCoderId)
#                 ),
#                 placement=DriveConstants.kFrontRightPosition,
#             )
        
#         rl = swervepy.impl.CoaxialSwerveModule(
#                 drive=swervepy.impl.Falcon500CoaxialDriveComponent(
#                     id_=DriveConstants.kRearLeftDrivingId,
#                     parameters=drive_params,
#                 ),
#                 azimuth=swervepy.impl.Falcon500CoaxialAzimuthComponent(
#                     id_=DriveConstants.kRearLeftTurningId,
#                     azimuth_offset=Rotation2d(DriveConstants.kBackLeftChassisAngularOffset),
#                     parameters=turning_params,
#                     absolute_encoder=swervepy.impl.AbsoluteCANCoder(DriveConstants.kRearLeftCANCoderId)
#                 ),
#                 placement=DriveConstants.kRearLeftPosition,
#             )
        
#         rr = swervepy.impl.CoaxialSwerveModule(
#                 drive=swervepy.impl.Falcon500CoaxialDriveComponent(
#                     id_=DriveConstants.kRearRightDrivingId,
#                     parameters=drive_params,
#                 ),
#                 azimuth=swervepy.impl.Falcon500CoaxialAzimuthComponent(
#                     id_=DriveConstants.kRearRightTurningId,
#                     azimuth_offset=Rotation2d(DriveConstants.kBackRightChassisAngularOffset),
#                     parameters=turning_params,
#                     absolute_encoder=swervepy.impl.AbsoluteCANCoder(DriveConstants.kRearRightCANCoderId)
#                 ),
#                 placement=DriveConstants.kRearRightPosition,
#             )
        
        

        
    