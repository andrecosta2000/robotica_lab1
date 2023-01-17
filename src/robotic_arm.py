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
        """Loads arm current position to RoboticArm.current_position object 
        (numpy array of 3 elements [x,y,z])"""
        self.com_port.write('delp t1\r')
        #time.sleep(1)
        #self.com_port.read_and_wait(1)
        self.com_port.write('yes\r')
        #time.sleep(1)
        self.com_port.write('defp t1\r')
        #time.sleep(1)
        self.com_port.write('here t1\r')
        #time.sleep(1)
        answer = self.com_port.read_and_wait(2)
        #print(answer)
        self.com_port.write('listpv t1\r')
        """ print('Getting Answer 1')
        print('Getting Answer') """
        answer = 'test'
        while 'X' not in answer: #waits for coordinates to show on serial bus
            #print('trying-------')
            answer = self.com_port.read_and_wait(0)
            #print('----------')
            #print(answer)
            #print('----------')
        
        """ answer='Position R22\r \
                1: 893  2:-10506    3:-1117 4:-22676    5: 9\r \
                X: 4632 Y:-71       Z: 7290 P:-264      R:-200' """
        answer=re.sub(r'Position R\d+', '',answer)
        x_start=answer.index('X')+2
        y_start=answer.index('Y')+2
        z_start=answer.index('Z')+2
        p_start=answer.index('P')+2
        x_end=y_start-3
        y_end=z_start-3
        z_end=p_start-3
        x = int(re.findall('[-+]?\d+', answer[x_start : x_end])[0])
        y = int(re.findall('[-+]?\d+', answer[y_start : y_end])[0])
        z = int(re.findall('[-+]?\d+', answer[z_start : z_end])[0])
        print(x)
        
        self.current_position[0] = x
        self.current_position[1] = y
        self.current_position[2] = z

    def set_origin(self) -> None:
        """Defines drawing plane from 3 points"""
        print('Calibrate Drawing Plane:')
        input('Move to Origin and press [Enter]')
        self.load_current_position()
        self.origin[0] = self.current_position[0]
        self.origin[1] = self.current_position[1]
        self.origin[2] = self.current_position[2]
        input('Move to 2nd referrence point and press [Enter]')
        self.load_current_position()
        point2=np.zeros(3)
        point2[0]=self.current_position[0]
        point2[1]=self.current_position[1]
        point2[2]=self.current_position[2]
        input('Move to 3rd referrence point and press [Enter]')
        self.load_current_position()
        point3=np.zeros(3)
        point3[0]=self.current_position[0]
        point3[1]=self.current_position[1]
        point3[2]=self.current_position[2]
        self.load_current_position()
        self.com_port.write('delp t1\r')
        #time.sleep(1)
        self.com_port.write('yes\r')
        #time.sleep(1)
        self.create_pos('t1',int(self.current_position[0]), int(self.current_position[1]), int(self.current_position[2]+300))
        self.move_pos('t1')
        print('######################')
        print('######################')
        print(self.origin)
        print(point2)
        print(point3)
        print('######################')
        print('######################')
        """ self.origin[0]=3698
        self.origin[1]=-2197
        self.origin[2]=-635
        point2=np.zeros(3)
        point2[0]=4938
        point2[1]=-2230
        point2[2]=-660
        point3=np.zeros(3)
        point3[0]=3984
        point3[1]=500
        point3[2]=-595 """

        ab=point2-self.origin
        ac=point3-self.origin
        self.normal_vector=np.cross(ab,ac)
        self.d = -(self.normal_vector[0]*point3[0]+self.normal_vector[1]*point3[1] \
            + self.normal_vector[2]*point3[2])

    def home(self):
        """Homes the robot"""
        self.com_port.write('home\r')
    
    def move_pos(self, name: str):
        """Moves robot to predefined position <name>"""
        self.com_port.write('move '+name+'\r')
        time.sleep(1)

    def move_pos_vec(self, name: str, pos_vec: np.array(np.array)):
        """Makes robot run through position vector <name> of size of <pos_vec>"""
        self.com_port.write('moves '+name+' '+str(1)+' '+str(pos_vec.shape[0])+'\r')
        time.sleep(15)

    def create_pos(self, name:str, x, y, z) -> None:
        """Creates position <name> with coordinates (x,y,z)"""
        self.com_port.write('defp '+name+'\r')
        #time.sleep(1)
        self.com_port.write('here '+name+'\r')
        #time.sleep(1)
        self.com_port.write('SETPVc '+name+' x '+str(x)+'\r')
        #time.sleep(1)
        self.com_port.write('SETPVc '+name+' y '+str(y)+'\r')
        #time.sleep(1)
        self.com_port.write('SETPVc '+name+' z '+str(z)+'\r')
        #time.sleep(1)
    
    def create_pos_vector(self, name:str, pos_vec: np.array(np.array)) -> None:
        """Creates position vector <name> with all points from <pos_vec>"""
        self.com_port.write('dimp '+name+'['+str(pos_vec.shape[0])+']'+'\r')
        #time.sleep(1)
        i=1
        self.com_port.write('here '+name+'['+str(i)+']'+'\r')
        #time.sleep(1)
        self.com_port.write('SETPVc '+name+'['+str(i)+']'+' x '+str(int(pos_vec[0][0]))+'\r')
        #time.sleep(1)
        self.com_port.write('SETPVc '+name+'['+str(i)+']'+' y '+str(int(pos_vec[0][1]))+'\r')
        #time.sleep(1)
        self.com_port.write('SETPVc '+name+'['+str(i)+']'+' z '+str(int(pos_vec[0][2]+300))+'\r')
        #time.sleep(1)
        self.com_port.read_and_wait(1)
        for i in range(2, pos_vec.shape[0]+1):
            print('Loading point ', i,' of ', pos_vec.shape[0])
            #print('here '+name+'['+str(i)+']'+'\r')
            #self.create_pos(name+'['+str(i)+']', pos_vec[i-1][0],pos_vec[i-1][1],pos_vec[i-1][2])
            if pos_vec[i-1][2] == 0:
                self.com_port.write('here '+name+'['+str(i)+']'+'\r')
                #time.sleep(1)
                self.com_port.write('SETPVc '+name+'['+str(i)+']'+' x '+str(int(pos_vec[i-2][0]))+'\r')
                #time.sleep(1)
                self.com_port.write('SETPVc '+name+'['+str(i)+']'+' y '+str(int(pos_vec[i-2][1]))+'\r')
                #time.sleep(1)
                self.com_port.write('SETPVc '+name+'['+str(i)+']'+' z '+str(int(pos_vec[i-2][2]+300))+'\r')
                #time.sleep(1)
                self.com_port.read_and_wait(1)
            else:
                self.com_port.write('here '+name+'['+str(i)+']'+'\r')
                #time.sleep(1)
                self.com_port.write('SETPVc '+name+'['+str(i)+']'+' x '+str(int(pos_vec[i-1][0]))+'\r')
                #time.sleep(1)
                self.com_port.write('SETPVc '+name+'['+str(i)+']'+' y '+str(int(pos_vec[i-1][1]))+'\r')
                #time.sleep(1)
                self.com_port.write('SETPVc '+name+'['+str(i)+']'+' z '+str(int(pos_vec[i-1][2]))+'\r')
                #time.sleep(1)
                self.com_port.read_and_wait(1)
            
        #self.com_port.write('dimp '+name+'['+pos_vec.shape[0]+']'+'\r')
        
        time.sleep(1)

    def get_z(self, x, y) -> int:
        """Determines z for given (x,y) on drawing plane"""
        return int(-(self.normal_vector[0]*x+self.normal_vector[1]*y+self.d)/ \
            self.normal_vector[2])