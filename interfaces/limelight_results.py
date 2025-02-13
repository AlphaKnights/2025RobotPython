# pylint: disable=too-few-public-methods

class LimelightResults:
    tag_id: int

    def __init__(self, data: dict) -> None:
        self.tag_id = data["Fiducial"][0]["fID"]
        self.tx = data["Fiducial"][0]['t6r_fs'][0]
        self.ty = data["Fiducial"][0]['t6r_fs'][2]
        self.ta = data["Fiducial"][0]['t6r_fs'][4]
        