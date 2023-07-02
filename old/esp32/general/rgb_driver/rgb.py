from machine import Pin
from machine import PWM
import time
from collections import OrderedDict


class RGB:
	def __init__(self, r_pin, g_pin, b_pin, freqs=(100, 100, 100), duties=(0, 0, 0)):
		self.r_pin = r_pin
		self.g_pin = g_pin
		self.b_pin = b_pin
		self.R = PWM(Pin(self.r_pin, Pin.OUT, value=0))
		self.G = PWM(Pin(self.g_pin, Pin.OUT, value=0))
		self.B = PWM(Pin(self.b_pin, Pin.OUT, value=0))
		self.R.freq(freqs[0]), self.G.freq(freqs[1]), self.B.freq(freqs[2])
		self.R.duty(duties[0]), self.G.duty(duties[1]), self.B.duty(duties[2])
		self.simple_color_collections = OrderedDict({
			'red': (1, 0, 0),
			'green': (0, 1, 0),
			'blue': (0, 0, 1),
			'magenta': (1, 0, 1),
			'yellow': (1, 1, 0),
			'cyan': (0, 1, 1),
			'white': (1, 1, 1),
			'off': (0, 0, 0)
		})
		self.advance_color_collections = {
			'purple': (136, 3, 252),
			'orange': (252, 186, 3),
			'midnight_blue': (25, 25, 112)
		}
	
	def set_rgb_color(self, rgb_color):
		r, g, b = rgb_color
		self.R.duty(int(r*4-1 if r >= 1 else 0))
		self.G.duty(int(g*4-1 if g >= 1 else 0))
		self.B.duty(int(b*4-1 if b >= 1 else 0))
	
	def set_advance_color(self, color):
		self.set_rgb_color(self.advance_color_collections[color])
	
	def set_color(self, color):
		self.set_rgb_color(self.simple_color_collections[color])
	
	def set_color_intensity(self, color, intensity):
		if intensity > 255:
			intensity = 255
		if intensity < 1:
			intensity = 0
		self.set_rgb_color(tuple([channel * intensity for channel in self.simple_color_collections[color]]))
	
	def show_raw_color(self, color):
		self.set_rgb_color(color)
	
	def show_advance_color(self, color):
		self.set_advance_color(color)
	
	def show_color(self, color):
		self.set_color(color)
	
	def show_color_intensity(self, color, intensity):
		self.set_color_intensity(color, intensity)
	
	def off(self):
		self.set_color('off')
	
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
