# pylint: disable=too-few-public-methods

class LimelightResults:
    tag_id: int

    def __init__(self, data: dict) -> None:
        self.tag_id = data["Fiducial"][0]["fID"]
        self.tx = data["Fiducial"][0]['t6t_rs'][0]
        self.ty = data["Fiducial"][0]['t6t_rs'][2]
        self.yaw = data["Fiducial"][0]['t6t_rs'][4]

        self.fx = data["Fiducial"][0]['t6r_fs'][0]
        self.fy = data["Fiducial"][0]['t6r_fs'][2]
        self.fyaw = data["Fiducial"][0]['t6r_fs'][4]







        