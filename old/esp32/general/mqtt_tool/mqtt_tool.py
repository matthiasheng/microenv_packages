import time
from machine import reset, Timer
import micropython
import json


def sub_topic_trigger(sub_topic, msg):
	print('sub_topic: {0}, msg: {1}'.format(sub_topic, msg))


def sub_listen_trigger():
	print("i'm ready to do something, just say it")


class MQTTTool:
	
	def __init__(self, MQTTClient, mqtt_config, topics_config, nprgb):
		self.MQTTClient = MQTTClient
		self.mqtt_config = mqtt_config
		self.topics_config = topics_config
		self.nprgb = nprgb
		self.logger = '/mqtt_log.txt'
		self.delay = 3
		self.timeout = 5000
		self.conn = self.get_connection()
		self.trigger_func = sub_topic_trigger
		self.sub_state = False
	
	def restart_and_reconnect(self, delay=3):
		print('Failed to connect to MQTT broker. Reconnecting...')
		time.sleep(self.delay)
		reset()
	
	def timeout_callback(self, timer_obj):
		micropython.schedule(self.restart_and_reconnect, 3)
	
	def get_connection(self):
		try:
			conn = self.MQTTClient(
				self.mqtt_config['id'],
				server=b"%s" % self.mqtt_config['SERVER'],
				user=b"%s" % self.mqtt_config['USERNAME'],
				password=b"%s" % self.mqtt_config['PASSWORD'],
				port=self.mqtt_config['PORT']
			)
			self.nprgb.show_color('blue')
			print("Connected to %s" % self.mqtt_config['SERVER'])
		except Exception as err:
			conn = None
			self.nprgb.show_color('red')
			with open(self.logger, 'a') as log:
				log.write('err: {0}\n'.format(err))
			self.restart_and_reconnect()
		return conn
	
	def connect(self):
		self.conn.connect()
	
	def disconnect(self):
		self.conn.disconnect()
	
	def publish(self, payload):
		if not self.sub_state:
			self.connect()
		for topic in self.topics_config['PUB']:
			self.nprgb.show_color('green')
			self.conn.publish(topic, json.dumps(payload.get(topic)))
		if not self.sub_state:
			self.disconnect()
		self.nprgb.off()
	
	def sub_cb(self, sub_topic, msg):
		timer = Timer(0)
		# print('notify: {0}'.format(notify))
		timer.init(period=self.timeout, mode=Timer.ONE_SHOT, callback=self.timeout_callback)
		self.trigger_func(sub_topic, msg)
		timer.deinit()
	
	def subscribe(self, callback_func=None):
		timer = Timer(0)
		timer.init(period=self.timeout, mode=Timer.ONE_SHOT, callback=self.timeout_callback)
		if callback_func:
			self.trigger_func = callback_func
		self.conn.set_callback(self.sub_cb)
		self.connect()
		for topic in self.topics_config['SUB']:
			self.conn.subscribe(b"%s" % topic)
		self.sub_state = True
		timer.deinit()
	
	def sub_listen(self, delay=0.05, normal_func=sub_listen_trigger):
		notify = self.conn.check_msg()
		# print('notify: {0}, type: {1}'.format(notify, type(notify)))
		if notify:
			print('notify: {0}'.format(notify))
		timer = Timer(0)
		timer.init(period=self.timeout, mode=Timer.ONE_SHOT, callback=self.timeout_callback)
		normal_func()
		timer.deinit()
		time.sleep(delay)
