from models.greenhouse_data import GreenHouseData


class Scanner:
    log = []

    def isNormalData(self, data:dict) -> bool:
        pass

    def getLog(self) -> []:
        return self.log


class ScannerResult:

    msg = ""
    type = ""

    def __init__(self, msg: str, typ: str):
        self.msg = msg
        self.type = typ



class InvernaderoDataScanner(Scanner):

    #estos valores tienen que concordar con invernadero
    data_dict = {
        "temp": [15, 20, -10, 45],
        "hum": [65, 70, 0, 100],
        "water_ph": [5.5, 6.5, 0, 14],
        "soil_ph": [4.6, 6.5, 0, 14],
        "water_salinity": [0.0, 1.0, 0, 5],
        "water_o2": [4, 8, 2, 8],
    }

    def __init__(self):
        pass

    def isNormalData(self, data:dict) -> bool:
        res = True

        margen = 3
        freq_envio_seg = 60

        last_value = GreenHouseData().last(data["user"]["_id"])

        res = self.isNormalDataValues(data)

        if last_value is not None and last_value["ip"] != data["ip"]:
            res = False
            self.log.append(ScannerResult("Ha cambiado la IP: {0} desde el último envío".format(data["ip"]), "CRITICAL"))


        segundos = (data["created"] - last_value["created"]).total_seconds() if last_value is not None else 0
        min = freq_envio_seg-margen
        max = freq_envio_seg+margen
        if last_value is not None and not (min <= segundos <= max):
            res = False
            self.log.append(ScannerResult("El tiempo transcurrido desde el último envío es de {} segundos".format(segundos), "WARNING"))


        return res


    def isNormalDataValues(self, data:dict) -> bool:
        res = True

        for i in self.data_dict:

            value = data[i]

            normal_min = self.data_dict[i][0]
            normal_max = self.data_dict[i][1]
            min = self.data_dict[i][2]
            max = self.data_dict[i][3]

            if normal_min <= value <= normal_max:
                pass #normal
            elif value < min or value > max:
                res = False
                self.log.append(ScannerResult("valor de {0} erroneo: {1}".format(i, value), "CRITICAL"))
            else:
                self.log.append(ScannerResult("valor de {0} anómalo: {1}".format(i, value), "WARNING"))
                res = False

        return res