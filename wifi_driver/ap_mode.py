import network
import time
import ubinascii


class APMode:
	def __init__(self, ap_config):
		self.ap_config = ap_config
		self.ap = network.WLAN(network.AP_IF)
		self.mac = ubinascii.hexlify(self.ap.config('mac')).decode()
		self.hidden_codes = {
			0: False,
			1: True
		}
	
	def ap_configure(self, ap_name=''):
		# parameter for ap.config
		self.ap_config['credential']['essid'] = self.ap_config['credential']['essid'] + self.mac + ap_name
		self.ap.active(True)
		self.ap.config(**self.ap_config['credential'])
		# parameter for ap.ifconfig
		ap_config_keys = (
			self.ap_config['ip'], self.ap_config['subnet'], self.ap_config['gateway'],
			self.ap_config['dns'])
		self.ap.ifconfig(ap_config_keys)
		print('AP is up refer to below:')
		print(
			'essid:{0},channel:{1},authmode:{2},hidden:{3},ifconfig:{4}'.format(
				self.ap_config['credential']['essid'],
				self.ap_config['credential']['channel'],
				self.ap_config['credential']['authmode'],
				self.hidden_codes[self.ap_config['credential']['hidden']],
				self.ap.ifconfig()
			)
		)
		
	def ap_on(self):
		self.ap.active(True)
		
	def ap_off(self):
		self.ap.active(False)