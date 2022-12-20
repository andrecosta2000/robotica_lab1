from robotic_arm import RoboticArm
from load_image import PATH
import numpy as np
import time

print('Starting')
print('###########################')
print('###### Loading Image ######')
print('###########################')
drawing = PATH()
pos_vec_array=drawing.load_paths_png('images/test_draw_1.png')

print('############################')
print('#### Initializing Robot ####')
print('############################')
robot = RoboticArm()
robot.open_coms('/dev/tty.usbserial-AB6YJ9ZL', 9600)
robot.load_current_position()
robot.set_origin()
""" x=int(input('enter x'))
y=int(input('enter y'))
print(robot.get_z(x,y))
robot.create_pos('v45', 4500, 1200, 1500) """

print('###########################')
print('##### Preparing Image #####')
print('###########################')
scale=2
max_points=5
n_paths=2

"""pos_vec_array = np.zeros([n_paths,max_points,3])
pos_vec_array[0][0]=[4000, 1000, 0]
pos_vec_array[0][1]=[4500, 1500, 0]
pos_vec_array[0][2]=[4000, 1000, 0]
pos_vec_array[0][3]=[4500, 1500, 0]
pos_vec_array[0][4]=[4000, 1000, 0]"""
for path in pos_vec_array:
    for point in path:
        point[0]=point[0]*scale+robot.origin[0]
        point[1]=point[1]*scale+robot.origin[1]
        point[2]=robot.get_z(point[0], [1])
        
print('###########################')
print('######### Drawing #########')
print('###########################')
robot.create_pos_vector('vdz', pos_vec_array[0])
robot.move_pos_vec('vdz', pos_vec_array[0])
#robot.create_pos('v44', 4000, 1000, 1300)
#robot.move_pos('v45')
#robot.set_origin()
