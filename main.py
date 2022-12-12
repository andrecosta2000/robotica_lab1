from robotic_arm import RoboticArm
from load_image import PATH
import time

if __name__ == "__main__":
    print('Starting')
    
    drawing = PATH()
    drawing.load_paths_png("images/test_draw_1.png")
    positions,n_paths =drawing.generate_arm_positions()

    robot = RoboticArm()
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
