# pylint: disable=no-member

import typing
import commands2
import limelight  # type: ignore
import ntcore
from interfaces.limelight_results import LimelightResults
import requests

class LimelightSystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.failed = False
        limelights = limelight.discover_limelights(debug=True)
        self.nt = ntcore.NetworkTableInstance.getDefault()


        if not limelights:
            print('No limelight')
            return
            # raise ValueError("No limelights found")

        self.limelight = limelight.Limelight(limelights[0])

        self.nt.setServer('roborio-6695-frc.local')
        self.nt.startClient4(str(self.limelight.get_name()))
        self.nt.startDSClient()

    def get_results_json(self):
        response = requests.get(f"{self.limelight.base_url}/results", timeout=2)

        if response.ok:
            return response.json()
        
        return None
        
    def get_results(self) -> typing.Optional[LimelightResults]:
        if self.failed or self.limelight is None or self.limelight.get_status() is not None:
            return None
        try:
            results = self.get_results_json()

        except:
            print('Cannot connect to limelight')
            self.failed = True
            return None
        
        if results is None:
            self.failed = True
            return None

        if results["botpose_tagcount"] == 0:
            return None

        return LimelightResults(results)
    
    def periodic(self) -> None: 
        super().periodic()



        results = self.get_results()

        if results is not None:
            print('x: ', results.tx)
            print('y: ', results.ty)