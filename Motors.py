from typing import Iterable
import time

import Adafruit_BBIO.GPIO as GPIO
from third_party_solver.enums import Color as Side


class Motors:
	# Mapping of a side to the motor's pins
	# Changes to this should also change the env_var.source
	motor_pins = {  Side.R: ("P2_1", "P2_3", "P2_5", "P2_7"),
					Side.U: ("P2_2", "P2_4", "P2_6", "P2_8"),
					Side.F: ("P2_9", "P2_11", "P2_17", "P2_19"),
					Side.D: ("P2_25", "P2_27", "P2_29", "P2_31"),
					Side.L: ("P2_28", "P2_30", "P2_33", "P2_35"),  # pins 32, 34 are burnt on my PB
					Side.B: ("P2_18", "P2_20", "P2_22", "P2_34")
	}
	
	# Mapping of a side to the encoder's pins side: (channel A, channel B)
	# Changes to this should also change the env_var.source
	encoder_pins = {Side.R: ("P1_2", "P1_6"),
					Side.U: ("P1_4", "P1_12"),
					Side.F: ("P1_26", "P1_28"),
					Side.D: ("P1_30", "P1_32"),
					Side.L: ("P1_29", "P1_31"),
					Side.B: ("P1_33", "P1_35")
	}
	
	# Defined by the stepper and encoder used
	encoder_step_size = 0.703125  # 1/512 CPR
	stepper_step_size = 0.087890625
		
	class Motor:
		def __init__(self, side: Side, power_saver: bool, debug: bool, sleep_time: float):
			"""
			Set's up a motor for this side

			:param side: The side the motor turns
			:param power_saver: If to save power by turning off the motor between turns
			:param debug: If to print debug information
			:param sleep_time: How much time to sleep between turns, a lower number will turn the
			motor faster, but too small will stop it entirely as it can't keep up, 0.0005 is a minimum.
			"""
			self.side = side
			self.power_saver = power_saver
			self.sleep_time = sleep_time  # TODO eventually remove
			self.debug = debug
			
			self.phase = 0  # The motors phase
			self.encoder_angle = 0

			# Enable motor and encoder pins
			for pin in Motors.motor_pins[side]:
				GPIO.setup(pin, GPIO.OUT)
			for pin in Motors.encoder_pins[side]:
				GPIO.setup(pin, GPIO.IN)
			
			# Listen on channel A
			GPIO.add_event_detect(Motors.encoder_pins[side][0], GPIO.RISING, self.update_angle)

		def update_angle(self, pin) -> None:
			"""
			Interrupt, called when the motor's coupled encoder's channel A goes low to high.
			Note, if an encoder is going in the reverse direction, switch the channel wires.

			:param pin: The in that generated this interrupt
			:return: Nothing
			"""
			# Check state of channel B
			b_new = GPIO.input(Motors.encoder_pins[self.side][1]) 
			if b_new == 1:
				self.encoder_angle -= Motors.encoder_step_size
			else:
				self.encoder_angle += Motors.encoder_step_size
			
		def reset(self) -> None:
			"""
			Resets the motor's phase and encoder's angle.

			:return: Nothing
			"""
			self.phase = 0
			self.encoder_angle = 0
		
		def turn(self, degrees: float, clockwise: bool) -> None:
			"""
			Turns the motor degrees in the clockwise direction if clockwise else counterclockwise
			:param degrees: The degrees to turn
			:param clockwise: If to turn clockwise or not
			:return: Nothing
			"""
			if self.debug:
				cw_or_ccw = "clockwise" if clockwise else "counter-clockwise"
				print("Turning Side: " + str(self.side) + " " + str(degrees) + " degrees " + cw_or_ccw, flush=True)
			
			steps = abs((int)(degrees / Motors.stepper_step_size))
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
				self.phase += direction
				if self.phase > 7:
					self.phase = 0
				elif self.phase < 0:
					self.phase = 7
			
			if self.power_saver:
				GPIO.output(pin1, GPIO.LOW)
				GPIO.output(pin2, GPIO.LOW)
				GPIO.output(pin3, GPIO.LOW)
				GPIO.output(pin4, GPIO.LOW)
		
		def __str__(self) -> str:
			"""
			Returns the string of this motor, given by the side and the encoder's value

			:return: A string of the motor
			"""
			return str(self.side) + ":" + str(self.encoder_angle)
			
		def get_encoder_angle(self) -> float:
			"""
			Get's just the coupled encoder's angle.

			:return: A float of the encoder's angle
			"""
			return self.encoder_angle

	def __init__(self, power_saver: bool = True, debug: bool = True, sleep_time: float = .0005, select: list = Side):
		"""
		A class that contains all 6 motors, stored in a dictionary with the sides as the keys.

		:param power_saver: If to turn off the motors between turns
		:param debug: If to print extra information
		:param sleep_time: How much time to sleep between phase updates
		:param select: A list if only to enable a subselection of the motors
		"""
		self.motors = {}  # Map of Side face to Motor object
		self.debug = debug
		self.power_saver = power_saver
		
		if debug:
			print("Setting up motors...", end="", flush=True)
		for side in select:
			self.motors[side] = self.Motor(side, power_saver, debug, sleep_time)
		if debug:
			print(" Done.")

	def turn_motor(self, side: Side, degrees, clockwise) -> None:
		"""
		Turns the selected motor.

		:param side: The side to turn
		:param degrees: The amount to turn
		:param clockwise: The direction to turn
		:return: Nothing
		"""
		self.motors[side].turn(degrees, clockwise)

	def demo(self) -> None:
		"""
		Runs a quick demo by turning all motors 360 degrees.

		:return: nothing
		"""
		if self.debug:
			print("Running demo... ")
		for motor in self.motors.values():
			motor.turn(360, True)
		if self.debug:
			print("Finished.")
	
	def get_motor_by_pins(self, pins: Iterable[str]) -> Motor:
		"""
		Returns the motor defined by the selection of pins (must be all pins)

		:param pins: an iterable of strings that are the pins
		:return: the Motor object, None if none found
		"""
		for motor_face in Side:
			pb_pins = self.motor_pins[motor_face]
			if sorted(pins) == sorted(pb_pins):
				return self.motors[motor_face]
		return None
	
	def get_motor_by_side(self, side: Side) -> Motor:
		"""
		Returns the motor defined by the side.

		:param side: the third_party_solver.enums.Color side
		:return: the Motor object
		"""
		return self.motors[side]
				

if __name__ == "__main__":
	motors = Motors()
	motors.demo()
