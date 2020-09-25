from typing import Iterable
import time

import Adafruit_BBIO.GPIO as GPIO
from third_party_solver.enums import Color as Side

class Motors:
	# Maping of a side to the motor's pins
	# Changes to this should also change the env_var.source
	motor_pins = {  Side.U : ("P2_2", "P2_4", "P2_6", "P2_8"),
					Side.R : ("P2_1", "P2_3", "P2_5", "P2_7"),
					Side.F : ("P2_9", "P2_11", "P2_17", "P2_19"),
					Side.D : ("P2_25", "P2_27", "P2_29", "P2_31"),
					Side.L : ("P2_28", "P2_30", "P2_33", "P2_35"), # pins 32, 34 are bad
					Side.B : ("P2_18", "P2_20", "P2_22", "P2_34")
	}
		
	class Motor:
		def __init__(self, side: Side, power_saver: bool, debug: bool, sleep_time):
			self.side = side
			self.power_saver = power_saver
			self.sleep_time = sleep_time # TODO eventually remove
			self.debug = debug
			
			self.phase = 0
			self.encoder = 0 # Currently, the encoder's reading. TODO switch to the coupled encoder
			self.angle = 0
			for pin in Motors.motor_pins[side]:
				GPIO.setup(pin, GPIO.OUT)
		
		def reset(self) -> None:
			self.phase = 0
			self.encoder = 0
			self.angle = 0
		
		def turn(self, degrees: float, clockwise: bool) -> None:
			if self.debug:
				cw_or_ccw = "clockwise" if clockwise else "count-clcokwise"
				print("Turning Side: " + str(self.side) + " " + str(degrees) + " degrees " + cw_or_ccw)
			
			steps = abs((int)(degrees / 0.087890625))
			pin1, pin2, pin3, pin4 = Motors.motor_pins[self.side]
			direction = 1 if clockwise else -1
			for i in range(steps):
				if self.phase == 0:   # 1 0 0 0
					GPIO.output(pin1, GPIO.HIGH)
					GPIO.output(pin2, GPIO.LOW)
					GPIO.output(pin3, GPIO.LOW)
					GPIO.output(pin4, GPIO.LOW)
				elif self.phase == 1: # 1 1 0 0
					GPIO.output(pin1, GPIO.HIGH)
					GPIO.output(pin2, GPIO.HIGH)
					GPIO.output(pin3, GPIO.LOW)
					GPIO.output(pin4, GPIO.LOW)		
				elif self.phase == 2: # 0 1 0 0
					GPIO.output(pin1, GPIO.LOW)
					GPIO.output(pin2, GPIO.HIGH)
					GPIO.output(pin3, GPIO.LOW)
					GPIO.output(pin4, GPIO.LOW)
				elif self.phase == 3: # 0 1 1 0
					GPIO.output(pin1, GPIO.LOW)
					GPIO.output(pin2, GPIO.HIGH)
					GPIO.output(pin3, GPIO.HIGH)
					GPIO.output(pin4, GPIO.LOW)
				elif self.phase == 4: # 0 0 1 0
					GPIO.output(pin1, GPIO.LOW)
					GPIO.output(pin2, GPIO.LOW)
					GPIO.output(pin3, GPIO.HIGH)
					GPIO.output(pin4, GPIO.LOW)
				elif self.phase == 5: # 0 0 1 1
					GPIO.output(pin1, GPIO.LOW)
					GPIO.output(pin2, GPIO.LOW)
					GPIO.output(pin3, GPIO.HIGH)
					GPIO.output(pin4, GPIO.HIGH)
				elif self.phase == 6: # 0 0 0 1
					GPIO.output(pin1, GPIO.LOW)
					GPIO.output(pin2, GPIO.LOW)
					GPIO.output(pin3, GPIO.LOW)
					GPIO.output(pin4, GPIO.HIGH)
				elif self.phase == 7: # 1 0 0 1
					GPIO.output(pin1, GPIO.HIGH)
					GPIO.output(pin2, GPIO.LOW)
					GPIO.output(pin3, GPIO.LOW)
					GPIO.output(pin4, GPIO.HIGH)
				time.sleep(self.sleep_time)
				# Advance to next phase
				self.phase += direction;
				if self.phase > 7:
					self.phase = 0
				elif self.phase < 0:
					self.phase = 7
				# TODO read the encoder, apply corrections for small differnces (friction)
				# but raise error for large issues (manual stop)
			
			if self.power_saver:
				GPIO.output(pin1, GPIO.LOW)
				GPIO.output(pin2, GPIO.LOW)
				GPIO.output(pin3, GPIO.LOW)
				GPIO.output(pin4, GPIO.LOW)
		
		def __str__(self) -> str:
			return str(self.side) + ":" + str(self.angle) + ":" + str(self.encoder)
			
			
	def __init__(self, power_saver: bool = True, debug: bool = True, sleep_time: float = .0005, select: list = Side):
		self.motors = {} # Map of Side face to Motor object
		self.debug = debug
		self.power_saver = power_saver
		
		if debug:
			print("Setting up motors...", end="", flush=True)
		for side in select:
			self.motors[side] = self.Motor(side, power_saver, debug, sleep_time)
		if debug:
			print(" Done.")


	def turn_motor(self, side: Side, degrees, clockwise) -> None:
		self.motors[side].turn(degrees, clockwise)

	def demo(self) -> None:
		if self.debug:
			print("Running demo... ")
		for motor in self.motors.values():
			motor.turn(360, True)
		if self.debug:
			print("Finished.")
	
	def get_motor_by_pins(self, pins: Iterable[str]) -> Motor:
		for motor_face in Side:
			pb_pins = self.motor_pins[motor_face]
			if sorted(pins) == sorted(pb_pins):
				return self.motors[motor_face]
		return None
	
	def get_motor_by_side(self, side: Side) -> Motor:
		return self.motors[side]
				

if __name__ == "__main__":
	motors = Motors()
	motors.demo()