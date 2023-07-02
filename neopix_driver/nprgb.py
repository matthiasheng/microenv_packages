import time
from machine import Pin
from neopixel import NeoPixel


class NPRGB:
	def __init__(self, pin_num, neopix_units):
		self.pin_num = pin_num
		self.neopix_units = neopix_units
		self.pin = Pin(pin_num, Pin.OUT)
		self.neo_pix = NeoPixel(self.pin, self.neopix_units)
		self.simple_color_collections = {
			'red': (1, 0, 0),
			'green': (0, 1, 0),
			'blue': (0, 0, 1),
			'magenta': (1, 0, 1),
			'yellow': (1, 1, 0),
			'cyan': (0, 1, 1),
			'white': (1, 1, 1),
			'off': (0, 0, 0)
		}
		self.advance_color_collections = {
			'purple': (136, 3, 252),
			'orange': (252, 186, 3),
			'midnight_blue': (25, 25, 112)
		}
	
	def set_raw_color(self, color):
		for i in range(self.neopix_units):
			self.neo_pix[i] = color
	
	def set_advance_color(self, color):
		for i in range(self.neopix_units):
			self.neo_pix[i] = self.advance_color_collections[color]
	
	def set_color(self, color):
		for i in range(self.neopix_units):
			self.neo_pix[i] = self.simple_color_collections[color]
	
	def set_color_intensity(self, color, intensity):
		if intensity > 255:
			intensity = 255
		if intensity < 1:
			intensity = 0
		for i in range(self.neopix_units):
			self.neo_pix[i] = tuple([channel * intensity for channel in self.simple_color_collections[color]])
	
	def show_raw_color(self, color):
		self.set_raw_color(color)
		self.neo_pix.write()
	
	def show_advance_color(self, color):
		self.set_advance_color(color)
		self.neo_pix.write()
	
	def show_color(self, color):
		self.set_color(color)
		self.neo_pix.write()
	
	def show_color_intensity(self, color, intensity):
		self.set_color_intensity(color, intensity)
		self.neo_pix.write()
	
	def off(self):
		self.set_color('off')
		self.neo_pix.write()
	
	def initialize(self, delay):
		for intensity in range(1, 100, 50):
			self.show_color_intensity('red', intensity)
			time.sleep(delay)
			self.off()
			self.show_color_intensity('green', intensity)
			time.sleep(delay)
			self.off()
			self.show_color_intensity('blue', intensity)
			time.sleep(delay)
			self.off()
			self.show_color_intensity('white', intensity)
			time.sleep(delay)
			self.off()
