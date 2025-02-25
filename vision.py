from cscore import CameraServer
def main():
    CameraServer.enableLogging()
    camera1 = CameraServer.startAutomaticCapture(0)
    camera2 = CameraServer.startAutomaticCapture(1)
    CameraServer.waitForever()