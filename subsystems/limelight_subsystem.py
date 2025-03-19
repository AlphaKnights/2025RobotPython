# pylint: disable=no-member

import typing
import commands2
import limelight  # type: ignore
from interfaces.limelight_results import LimelightResults

class LimelightSystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()

        limelights = limelight.discover_limelights(debug=True)
        
        if not limelights:
            raise ValueError("No limelights found")

        self.limelight = limelight.Limelight(limelights[0])

    def get_results(self) -> typing.Optional[LimelightResults]:
        results = self.limelight.get_results()

        if results["botpose_tagcount"] == 0:
            return None

        return LimelightResults(results)