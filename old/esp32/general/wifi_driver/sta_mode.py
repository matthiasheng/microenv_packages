import network
import time
import ubinascii


class StaMode:
	def __init__(self, router_config, sta_config):
		self.router_config = router_config
		self.sta_config = sta_config
		self.wlan = network.WLAN(network.STA_IF)
		self.wlan.active(True)
		self.mac = ubinascii.hexlify(self.wlan.config('mac')).decode()
		self.ip = None
		self.gateway = None
		self.subnet_mask = None
		self.DNS_server = None
		self.authmodes = {
			0: "open",
			1: "WEP",
			2: "WPA - PSK",
			3: "WPA2 - PSK",
			4: "WPA / WPA2 - PSK"
		}
		self.hidden_codes = {
			0: False,
			1: True
		}
		self.status_codes = {
			0: "STAT_IDLE – no connection and no activity",
			1: "STAT_CONNECTING – connecting in progress",
			2: "STAT_WRONG_PASSWORD – failed due to incorrect password",
			3: "STAT_NO_AP_FOUND – failed because no access point replied",
			4: "STAT_CONNECT_FAIL – failed due to other problems",
			5: "STAT_GOT_IP – connection successful",
			1010: "STAT_GOT_IP – connection successful(esp32c3)",
			8: "STAT_IDLE – no connection and no activity(esp32c3)"
		}
		
	def get_network_details(self):
		self.ip, self.subnet_mask, self.gateway, self.DNS_server = self.wlan.ifconfig()
		print('ip: {0}'.format(self.ip))
		print('subnet_mask: {0}'.format(self.subnet_mask))
		print('gateway: {0}'.format(self.gateway))
		print('DNS_server: {0}'.format(self.DNS_server))
	
	def connect(self):
		timeout = len(self.router_config) * 10
		t = 0
		while not self.wlan.isconnected() and t < timeout:
			for ap, password in self.router_config.items():
				print('Connecting to {0}...'.format(ap))
				self.wlan.connect(ap, password)
				time.sleep(10)
				if self.wlan.isconnected():
					print(
						'{0} connected! status: {1}, time elapsed:{2}'.format(
							ap,
							self.check_status(),
							t,
						)
					)
					# set ip level config
					# DONE: TypeError: object 'dict' isn't a tuple or list
					self.wlan.ifconfig([i[1] for i in self.sta_config.items()])
					# get ip level config
					self.get_network_details()
					break
				print(
					'{0} not connected! status: {1}, time elapsed:{2}'.format(
						ap,
						self.check_status(),
						t,
					)
				)
				t += 10
		if self.wlan.isconnected():
			self.get_network_details()
		else:
			print('All ap failed to connect, try again later! status: {0}'.format(self.check_status()))
			
	def disconnect(self):
		self.wlan.disconnect()
	
	def scan(self):
		print('Scanned ap listed below:')
		found_networks = sorted(self.wlan.scan(), key=lambda x: x[3], reverse=True)
		for i, found_network in enumerate(found_networks):
			print('found network {0}:'.format(i))
			ap = found_network[0].decode()
			bssid = ubinascii.hexlify(found_network[1]).decode()
			channel = found_network[2]
			rssi = found_network[3]
			authmode = self.authmodes[found_network[4]]
			hidden = self.hidden_codes[found_network[5]]
			print('ap_name: {0}, bssid: {1}, channel: {2}, rssi: {3} %, authmode: {4}, hidden: {5}'.format(ap, bssid, channel, self.get_rssi_percent(rssi), authmode, hidden))
			
	def check_status(self):
		return self.status_codes.get(self.wlan.status())
	
	def check_rssi(self):
		return self.wlan.status('rssi')
	
	def get_rssi_percent(self, rssi=None):
		if not rssi:
			rssi = self.check_rssi()
		if rssi <= -100:
			rssi_percent = 0
		elif rssi >= -50:
			rssi_percent = 100
		else:
			rssi_percent = 2*(100 + rssi)
		return rssi_percent
