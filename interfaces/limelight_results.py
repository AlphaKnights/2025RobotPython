# pylint: disable=too-few-public-methods

class LimelightResults:
    tag_id: int

    def __init__(self, data: dict) -> None:
        self.tag_id = data["Fiducial"][0]["fID"]
        self.tx = data["tx"]
        self.ty = data["ty"]
        self.ta = data["ta"]
        