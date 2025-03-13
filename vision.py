from cscore import UsbCamera, VideoSink

import enum
class Direction(enum.Enum):
    FRONT = 1
    REAR = 2

class CameraSubsystem:

    def __init__(self, f_camera: UsbCamera, r_camera: UsbCamera, table: VideoSink, table2: VideoSink):
        super().__init__()
        self.front_camera = f_camera
        self.rear_camera = r_camera
        self.server = table
        self.server2 = table2
        

    def select(self):
        self.server.setSource(self.front_camera)
        
        self.server2.setSource(self.rear_camera)