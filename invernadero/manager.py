from sensor import Sensor
from actuator import Actuator
from plc_sender import PLCSENDER


def env_conf():
    devices = []
    print("Setting up sensors")
    devices.append(Sensor("invernadero"))
    print("Setting up actuators")
    devices.append(Actuator("valve"))
    print("Setting up PLC_SENDER")
    devices.append(PLCSENDER())
    return devices


if __name__ == "__main__":
    while True:
        devices = env_conf()
        for device in devices:
            device.start()

        for device in devices:
            device.join()
    print("Bye")
