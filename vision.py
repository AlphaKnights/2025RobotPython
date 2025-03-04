from wpilib import CameraServer
from cscore import UsbCamera, VideoSink
from ntcore import NetworkTableInstance
class CameraSubsystem:

    def __init__(self, f_camera: UsbCamera, r_camera: UsbCamera):
        super().__init__()
        CameraSubsystem.front_camera = f_camera
        CameraSubsystem.rear_camera = r_camera
        CameraSubsystem.server = NetworkTableInstance.getDefault().getTable("").getEntry("CameraSelection")

    
    def select(self, direction):
        if direction == "FRONT":
            CameraSubsystem.server.setString(CameraSubsystem.front_camera.getName())
        else:
            CameraSubsystem.server.setString(CameraSubsystem.rear_camera.getName())