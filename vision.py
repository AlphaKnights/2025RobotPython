from cscore import UsbCamera, MjpegServer

import enum
class Direction(enum.Enum):
    FRONT = 1
    REAR = 2

class CameraSubsystem:

    def __init__(self, f_camera: UsbCamera, r_camera: UsbCamera, table: MjpegServer):
        super().__init__()
        self.front_camera = f_camera
        self.rear_camera = r_camera
        self.server = table
        

    def select(self, direction):
        if direction == Direction.FRONT:
            self.server.setSource(self.front_camera)
        else:
            self.server.setSource(self.rear_camera)