from datetime import datetime

from security.InvernaderoDataScanner import InvernaderoDataScanner, Scanner

from models.log_msg import LogMsg


def scan(scanner:Scanner, validated:dict, ip:str, dt:datetime, user:dict):

    if not scanner.isNormalData(validated):
        setAnomalies(scanner.getLog(), ip, dt, user)


def setAnomalies(log:[], ip:str, dt:datetime, user:dict) -> None:

    for error in log:
        setAnomaly(error.msg, error.type, ip, dt, user)

def setAnomaly(msg:str, typ:str, ip:str, dt:datetime, user:dict) -> None:

    u = {
            "_id": user['_id'],
            "name": user['name'],
        } if user is not None else None

    LogMsg().insert({
        "msg": msg,
        "type": typ,
        "ip": ip,
        "date": dt,
        'user': u
    })