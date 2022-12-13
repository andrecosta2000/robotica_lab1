from robotic_arm import RoboticArm
#from load_image import PATH
import numpy as np
import time

print('Starting')
    
""" drawing = PATH()
drawing.load_paths_png("images/test_draw_1.png")
positions,n_paths =drawing.generate_arm_positions() """

robot = RoboticArm()
print('init')
robot.open_coms('/dev/tty.usbserial-AB6YJ9ZL', 9600)
""" robot.home()
print('-----------------------------')
print('-----------------------------')
print('HOMING')
time.sleep(120000)
print('Done!')
print('-----------------------------')
print('-----------------------------')
print('-> Creating Position')
robot.create_pos('r22', 500, 500, 385)
print('-> Moving to position (500,500,385)')
robot.move_pos('r2') """
robot.load_current_position()
robot.set_origin()
x=int(input('enter x'))
y=int(input('enter y'))
print(robot.get_z(x,y))
#robot.create_pos('v45', 4500, 1200, 1500)
max_points=5
n_paths=2
pos_vec_array = np.zeros([n_paths,max_points,3])
pos_vec_array[0][0]=[4000, 1000, robot.get_z(4000, 1000)]
pos_vec_array[0][1]=[4500, 1500, robot.get_z(4500, 1500)]
pos_vec_array[0][2]=[4000, 1000, robot.get_z(4000, 1000)]
pos_vec_array[0][3]=[4500, 1500, robot.get_z(4500, 1500)]
pos_vec_array[0][4]=[4000, 1000, robot.get_z(4000, 1000)]
robot.create_pos_vector('vdz', pos_vec_array[0])
robot.move_pos_vec('vdz', pos_vec_array[0])
#robot.create_pos('v44', 4000, 1000, 1300)
#robot.move_pos('v45')
#robot.set_origin()
