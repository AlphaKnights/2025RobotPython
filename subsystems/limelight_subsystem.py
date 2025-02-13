# pylint: disable=no-member

import typing
import commands2
import limelight  # type: ignore
from networktables import NetworkTables
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
        limelight_table = NetworkTables.getTable("limelight")
        botpose = limelight_table.getNumberArray("botpose_wpiblue", [0]*7)
        x = botpose[0]
        y = botpose[1]
        yaw = botpose[5]
        print(x, y, yaw)
        if results["botpose_tagcount"] == 0:
            return None

        return LimelightResults(results)