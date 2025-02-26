from wpilib import CameraServer
from cscore import UsbCamera, VideoSink
class CameraSubsystem:

    def __init__(self, f_camera: UsbCamera, r_camera: UsbCamera, table: VideoSink):
        super().__init__()
        CameraSubsystem.front_camera = f_camera
        CameraSubsystem.rear_camera = r_camera
        CameraSubsystem.server = table

    
    def select(self, direction):
        if direction == "FRONT":
            CameraSubsystem.server.setSource(CameraSubsystem.front_camera)
        else:
            CameraSubsystem.server.setSource(CameraSubsystem.rear_camera)