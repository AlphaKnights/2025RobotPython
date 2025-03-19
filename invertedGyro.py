from navx import AHRS 


class invertedGyro(AHRS):
    def __init__(self, comType : AHRS.NavXComType) -> None:
        super().__init__(AHRS.NavXComType.kMXP_SPI)
    
    def getAngle(self) -> float:
        return -super().getAngle()
    
        


        

