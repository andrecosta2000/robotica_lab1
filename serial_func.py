import serial
import time
# This function listens the serial port for wait_time seconds
# waiting for ASCII characters to be sent by the robot
# It returns the string of characters

class SerialPort:
    def __init__(self, serial_device: str, baud_rate: int) -> None:
        self.port = serial.Serial(serial_device, baud_rate)#, stopbits)
        print("COM port in use: {0}".format(self.port.name))

    def read_and_wait(self, wait_time):
        output = ""
        flag = True
        start_time = time.time()

        while flag:
            # Wait until there is data waiting in the serial buffer
            if self.port.in_waiting > 0:
                # Read data out of the buffer until a carriage return / new line is found
                serString = self.port.readline()
                # Print the contents of the serial data
                try:
                    output = serString.decode("Ascii")
                    print(serString.decode("Ascii"))
                except:
                    pass
            else:
                deltat = time.time() - start_time
                if deltat>wait_time:
                    flag = False
        return output
    
    def write(self, str: str):
        self.port.write(bytearray(str, 'ascii'))
