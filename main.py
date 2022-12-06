import serial_func
import robotic_arm
import load_image
import time

if __name__ == "__main__":
    print('Starting')
    
    robot = robotic_arm()
    robot.open_coms('/dev/tty.usbserial-AB6YJ9ZL', 9600)
    robot.home()
    print('-----------------------------')
    print('-----------------------------')
    print('HOMING')
    time.sleep(120000)
    print('Done!')
    print('-----------------------------')
    print('-----------------------------')
    print('-> Creating Position')
    robot.create_pos('r2', 500, 500, 385)
    print('-> Moving to position (500,500,385)')
    robot.move_pos('r2')
    