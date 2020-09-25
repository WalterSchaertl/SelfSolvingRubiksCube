from typing import Iterable
from threading import Thread
import time

import Adafruit_BBIO.GPIO as GPIO
from third_party_solver.enums import Color as Side

class Encoders:
	# Maping of a side to the encoder's pins (Channel A, Channel B)
	# Changes to this should also change the env_var.source
	encoder_pins = {Side.R : ("P1_2", "P1_6"),
					Side.U : ("P1_10", "P1_12"),
					Side.F : ("P1_26", "P1_28"),
					Side.D : ("P1_30", "P1_32"),
					Side.L : ("P1_29", "P1_31"),
					Side.B : ("P1_33", "P1_35")
	}
	angle_step = 0.703125
		
	class Encoder(Thread):
		def __init__(self, side: Side, debug: bool):
			self.side = side
			self.debug = debug
			
			self.stop = False
			self.angle = 0
			self.ch_a_pin, self.ch_b_pin = Encoders.encoder_pins[side]
			
			GPIO.setup(self.ch_a_pin, GPIO.IN)
			GPIO.setup(self.ch_b_pin, GPIO.IN)
			super(Encoders.Encoder, self).__init__()
			print("Pins: " + self.ch_a_pin + " " + self.ch_b_pin)
			#TODO invistigate sevent detect and callback
			#GPIO.add_event_detect(ch_a_pin, GPIO.RISING, update_angle)
				
		
		def reset(self) -> None:
			self.angle = 0
		
		def run(self):
			"""
			Channel A leads Channel B if roatating clockwise, B leads A counterclowise.
			"""
			a_st = GPIO.input(self.ch_a_pin)
			while not self.stop:
				# Wait for A rising edge, check B state to determine dirrection.
				a_new = GPIO.input(self.ch_a_pin)
				# GPIO.wait_for_edge would be nice, but way too slow
				# GPIO.wait_for_edge(self.ch_a_pin, GPIO.RISING)
				if a_st == 0 and a_new == 1:
					if GPIO.input(self.ch_b_pin) == 1:
						self.angle -= 0.703125
					else:
						self.angle += 0.703125
				a_st = a_new
				time.sleep(0.000001)
				
		def get_angle(self):
			return self.angle
		
		def stop_encoder(self):
			self.stop = True
	
	# Work it to add option to just init a list of sides?
	def __init__(self, power_saver: bool = True, debug: bool = True, select: list = Side):
		self.encoders = {} # Map of Side face to Encoder object
		self.debug = debug
		
		if debug:
			print("Setting up encoders...", end="", flush=True)
		for side in select:
			self.encoders[side] = self.Encoder(side, debug)
			self.encoders[side].start()
			
		if debug:
			print(" Done.")
	
	def get_encoder_by_pins(self, pins: Iterable[str]) -> Encoder:
		for encoder_face in Side:
			pb_pins = self.encoder_pins[encoder_face]
			if sorted(pins) == sorted(pb_pins):
				return self.encoders[encoder_face]
		return None
		
	def get_encoder_by_side(self, side: Side) -> Encoder:
	    return self.encoders[side]

