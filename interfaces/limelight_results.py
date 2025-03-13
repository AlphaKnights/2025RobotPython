# pylint: disable=too-few-public-methods

class LimelightResults:
    tag_id: int

    def __init__(self, data: dict) -> None:
        self.tag_id = data["Fiducial"][0]["fID"]
        self.rx = data["Fiducial"][0]['t6r_fs'][0]
        self.ry = data["Fiducial"][0]['t6r_fs'][2]
        self.ra = data["Fiducial"][0]['t6r_fs'][4]

        self.fx = data["Fiducial"][0]['t6r_fs'][0]
        self.fy = data["Fiducial"][0]['t6r_fs'][2]
        self.fa = data["Fiducial"][0]['t6r_fs'][4]
        