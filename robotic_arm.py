from serial_func import SerialPort
import time
import datetime

class RoboticArm:
    def __init__(self) -> None:
        self.com_port = None
        self.current_position = None

    def open_coms(self, device_name: str, baud_rate: int):
        self.com_port = SerialPort(device_name, baud_rate)

    def load_current_position(self) -> int:
        self.com_port.write('')
        print(self.com_port.read_and_wait(2))

    def home(self):
        self.com_port.write('home\r')
    
    def move_pos(self, name: str):
        self.com_port.write('move '+name+'\r')
        time.sleep(0.05)

    def create_pos(self, name:str, x, y, z):
        self.com_port.write('defp '+name+'\r')
        time.sleep(0.05)
        self.com_port.write('SETPV '+name+' x '+x+'\r')
        time.sleep(0.05)
        self.com_port.write('SETPV '+name+' y '+y+'\r')
        time.sleep(0.05)
        self.com_port.write('SETPV '+name+' z '+z+'\r')
        time.sleep(0.05)
