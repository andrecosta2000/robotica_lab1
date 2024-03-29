from robotic_arm import RoboticArm
from load_image import PATH
import numpy as np
import time

print('Starting')
print('###########################')
print('###### Loading Image ######')
print('###########################')
drawing = PATH()
drawing.load_paths_png('images/test_draw_1.png')

print('############################')
print('#### Initializing Robot ####')
print('############################')
robot = RoboticArm()
robot.open_coms('/dev/tty.usbserial-AB6YJ9ZL', 9600)
robot.load_current_position()
robot.set_origin()

print('###########################')
print('##### Preparing Image #####')
print('###########################')
scale=0.25
max_points=0
for path in drawing.points:
    if len(path) > max_points:
        max_points = len(path)
#print(max_points)
pos_vec_array = np.zeros([len(drawing.points),max_points+1,3])
for i in range(len(drawing.points)):
    for j in range(len(drawing.points[i])):
        pos_vec_array[i][j][0]=drawing.points[i][j][0]*scale+robot.origin[0]
        pos_vec_array[i][j][1]=drawing.points[i][j][1]*scale+robot.origin[1]
        pos_vec_array[i][j][2]=robot.get_z(pos_vec_array[i][j][0], pos_vec_array[i][j][1])
print(pos_vec_array)


robot.create_pos('t1', int(robot.origin[0]),int(robot.origin[1]),int(robot.origin[2]+300))
robot.move_pos('t1')
print('###########################')
print('######### Drawing #########')
print('###########################')
robot.com_port.write('speed 1\r')
time.sleep(0.5)
for i,vec in enumerate(pos_vec_array):
    print('Loading Points...')
    robot.create_pos_vector(str('vdz'+str(i)), vec)
    print('Drawing...')
    robot.move_pos_vec(str('vdz'+str(i)), vec)
    print('Done')

