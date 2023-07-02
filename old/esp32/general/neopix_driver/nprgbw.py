from .nprgb import NPRGB
from neopixel import NeoPixel
from machine import Pin
import time


class NPRGBW(NPRGB):
	def __init__(self, pin_num, neopix_units, bpp=4):
		super().__init__(pin_num, neopix_units)
		self.pin_num = pin_num
		self.neopix_units = neopix_units
		self.bpp = bpp
		self.pin = Pin(pin_num, Pin.OUT)
		self.neo_pix = NeoPixel(self.pin, self.neopix_units, bpp=self.bpp)
		self.simple_color_collections = {
			'red': (1, 0, 0, 0),
			'green': (0, 1, 0, 0),
			'blue': (0, 0, 1, 0),
			'magenta': (1, 0, 1, 0),
			'yellow': (1, 1, 0, 0),
			'cyan': (0, 1, 1, 0),
			'white': (1, 1, 1, 0),
			'w_white': (0, 0, 0, 1),
			'f_white': (1, 1, 1, 1),
			'off': (0, 0, 0, 0)
		}
		self.advance_color_collections = {
			'purple': (136, 3, 252, 0),
			'orange': (252, 186, 3, 0),
			'midnight_blue': (25, 25, 112, 0)
		}
	
	def set_raw_color(self, color):
		if len(color) == 3:
			color = (color[0], color[1], color[2], 0)
		else:
			color = (color[0], color[1], color[2], color[3])
		for i in range(self.neopix_units):
			self.neo_pix[i] = color
			
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
			self.show_color_intensity('w_white', intensity)
			time.sleep(delay)
			self.show_color_intensity('f_white', intensity)
			time.sleep(delay)
			self.off()
