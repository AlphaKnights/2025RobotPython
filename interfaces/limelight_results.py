# pylint: disable=too-few-public-methods

class LimelightResults:
    tag_id: int

    def __init__(self, data: dict) -> None:
        self.tag_id = data["Fiducial"][0]["fID"]
        self.tx = data["Fiducial"][0]['t6t_rs'][0]
        self.ty = data["Fiducial"][0]['t6t_rs'][2] - 0.457
        self.yaw = data["Fiducial"][0]['t6t_rs'][4]

        self.fx = data["Fiducial"][0]['t6r_fs'][0] /100 - 72.39
        self.fy = data["Fiducial"][0]['t6r_fs'][2] / 100 - 72.39
        self.fa = data["Fiducial"][0]['t6r_fs'][4] 

        #8cm from the right edge
        #18 from the front
        #72.39 cm by 72.39 (robot)
        #805.18 cm by 1737.36 cm (field)

        #front offset is 36.195 cm - 8cm = 28.195 cm
        

        # 1.48

        # 7 inches from front 0.178
        # 11.5 0.292