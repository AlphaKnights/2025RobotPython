import wpilib
from wpilib.cameraserver import CameraServer
from constants import CameraConstants
from constants import OIConstants
from ntcore import NetworkTableInstance

class cameraServer:
    def __init__(self) -> None:
        super().__init__()
        self.driverController = wpilib.XboxController(OIConstants.kDriverControllerPort)
        self.cameraSelection = NetworkTableInstance.getDefault().getTable("").getEntry("CameraSelection")
        wpilib.CameraServer.launch("vision.py:main")
    def run(self) -> None:
        if self.driverController.getLeftY() < 0:
            self.cameraSelection.setString("USB Camera 1")
        else:
            self.cameraSelection.setString("USB Camera 0")
