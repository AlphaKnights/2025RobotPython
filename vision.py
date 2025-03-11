from wpilib import CameraServer
from cscore import UsbCamera, VideoSink
from ntcore import NetworkTableEntry, NetworkTableInstance
class CameraSubsystem:

    def __init__(self, f_camera: UsbCamera, r_camera: UsbCamera, table: NetworkTableEntry):
        super().__init__()
        self.front_camera = f_camera
        self.rear_camera = r_camera
        self.server = table
        

    def select(self, direction):
        if direction == 1:
            self.server.setString(self.front_camera.getName())
        else:
            self.server.setString(self.rear_camera.getName())