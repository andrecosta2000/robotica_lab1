from serial_func import SerialPort
import time
#import datetime
import re
import numpy as np

class RoboticArm:
    def __init__(self) -> None:
        self.com_port = None
        self.current_position = np.zeros(3)
        self.origin = np.zeros(3)
        self.normal_vector = np.zeros(3)
        self.d = 0

    def open_coms(self, device_name: str, baud_rate: int):
        self.com_port = SerialPort(device_name, baud_rate)

    def load_current_position(self) -> None:
        self.com_port.write('defp t1\r')
        time.sleep(0.05)
        self.com_port.write('here t1\r')
        time.sleep(0.05)
        answer = self.com_port.read_and_wait(0.5)
        answer = answer.split('\t')
        print(answer)
        for word in answer:
            if word.__contains__('X:'):
                print('X is: ', word)
                self.current_position[0] = re.findall('\d+', word)
            if word.__contains__('Y:'):
                print('Y is: ', word)
                self.current_position[1] = re.findall('\d+', word)
            if word.__contains__('Z:'):
                print('Z is: ', word)
                self.current_position[2] = re.findall('\d+', word)
        #print(self.com_port.read_and_wait(2))

    def set_origin(self) -> None:
        """Defines drawing plane from 3 points"""

        """ input('Move to Origin and press [Enter]')
        self.load_current_position()
        self.origin = self.current_position
        input('Move to 2nd referrence point and press [Enter]')
        self.load_current_position()
        point2=np.zeros(3)
        point2=self.current_position
        input('Move to 3rd referrence point and press [Enter]')
        self.load_current_position()
        point3=self.current_position """
        self.origin[0]=1000
        self.origin[1]=300
        self.origin[2]=-200

        point2=np.zeros(3)
        point2[0]=2000
        point2[1]=300
        point2[2]=-200

        point3=np.zeros(3)
        point3[0]=2000
        point3[1]=1000
        point3[2]=-300

        ab=point2-self.origin
        ac=point3-self.origin
        self.normal_vector=np.cross(ab,ac)
        self.d = -(self.normal_vector[0]*point3[0]+self.normal_vector[1]*point3[1] \
            + self.normal_vector[2]*point3[2])

    def home(self):
        self.com_port.write('home\r')
    
    def move_pos(self, name: str):
        self.com_port.write('move '+name+'\r')
        time.sleep(0.05)

    def create_pos(self, name:str, x, y, z) -> None:
        self.com_port.write('defp '+name+'\r')
        time.sleep(0.05)
        self.com_port.write('here '+name+'\r')
        time.sleep(0.05)
        self.com_port.write('SETPVc '+name+' x '+x+'\r')
        time.sleep(0.05)
        self.com_port.write('SETPVc '+name+' y '+y+'\r')
        time.sleep(0.05)
        self.com_port.write('SETPVc '+name+' z '+z+'\r')
        time.sleep(0.05)

    def get_z(self, x, y) -> int:
        """Determines z for xy on drawing plane"""
        return -(self.normal_vector[0]*x+self.normal_vector[1]*y+self.d)/ \
            self.normal_vector[2]