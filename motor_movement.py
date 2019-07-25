import serial
import argparse
from time import sleep


class Serial_Wrapper:
	def __init__(self, device, baud=9600):
		self.ser = serial.Serial(device, baud)
	
	def send_data(self, data, expect_confirmation = False, print_confirmation = False):
		self.ser.write(data)
		if expect_confirmation:
			print('\t||| Sent "' + str(data) + '" over serial.')
			rec = self.ser.readline()
			if print_confirmation:
				print('\t||| Received "' + str(rec) + '" over serial. Which "decode().rstrip()"s to \'' + rec.decode('ASCII').rstrip() + '\'')

	def flush_buffer(self):
		self.ser.flushOutput()
		
class Serial_Motor_Control:
	def __init__(self, device='/dev/ttyACM0', baud=9600, cw_x_flag='1', ccw_x_flag='2', cw_y_flag='3', ccw_y_flag='4'):
		self.serial_dev = Serial_Wrapper(device, baud)
		self.cw_x_flag = cw_x_flag
		self.ccw_x_flag = ccw_x_flag
		self.cw_y_flag = cw_y_flag
		self.ccw_y_flag = ccw_y_flag
	
	def move_x_cw(self, num_increments=1):
		self.serial_dev.send_data(self.cw_x_flag.encode())
	def move_x_ccw(self, num_increments=1):
		self.serial_dev.send_data(self.ccw_x_flag.encode())
		
	def move_y_cw(self, num_increments=1):
		self.serial_dev.send_data(self.cw_y_flag.encode())
	def move_y_ccw(self, num_increments=1):
		self.serial_dev.send_data(self.ccw_y_flag.encode())
		
	def flush_buffer(self):
		self.serial_dev.flush_buffer()