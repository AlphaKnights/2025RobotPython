# pylint: disable=too-few-public-methods

class LimelightResults:
    tag_id: int

    def __init__(self, data: dict) -> None:
        self.tag_id = data["Fiducial"][0]["fID"]
        self.tx = data["Fiducial"][0]['t6t_cs'][0] / (1.6 * (6.25/6.5))
        self.ty = data["Fiducial"][0]['t6t_cs'][2] / (1.6 * (6.25/6.5))
        self.yaw = data["Fiducial"][0]['t6t_cs'][4]
        