import os
import sys
import time
import json
import logging
import micropython
from machine import reset, Timer


mqtt_tool_log = logging.getLogger('mqtt_tool')


def sub_topic_trigger(sub_topic, msg):
    mqtt_tool_log.info('sub_topic: {0}, msg: {1}'.format(sub_topic, msg))


def sub_listen_trigger():
    mqtt_tool_log.info("i'm ready to do something, just say it")


class MQTTTool:

    def __init__(self, MQTTClient, mqtt_config, topics_config, nprgb):
        self.MQTTClient = MQTTClient
        self.mqtt_config = mqtt_config
        self.topics_config = topics_config
        self.nprgb = nprgb
        self.logger = '/mqtt_log.txt'
        self.delay = 3
        self.timeout = mqtt_config.get('timeout')
        self.conn = self.get_connection()
        self.trigger_func = sub_topic_trigger
        self.sub_state = False

    def restart_and_reconnect(self, delay=3):
        mqtt_tool_log.error('Failed to connect to MQTT broker. Reconnecting...')
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
                port=self.mqtt_config['PORT'],
                keepalive=30
            )
            self.nprgb.show_color('blue')
            mqtt_tool_log.info(f'mqtt_config: {self.mqtt_config}')
        except KeyboardInterrupt:
            mqtt_tool_log.error(f'keyboard interrupt! Program exit now!')
            sys.exit()
        except Exception as err:
            conn = None
            self.nprgb.show_color('red')
            with open(self.logger, 'a') as log:
                log.write('err: {0}\n'.format(err))
            mqtt_tool_log.error(f'err: {err}')
            self.restart_and_reconnect()
        return conn

    def connect(self):
        self.conn.connect()
        mqtt_tool_log.info("Connected to %s" % self.mqtt_config['SERVER'])

    def disconnect(self):
        self.conn.disconnect()
        mqtt_tool_log.info("Disconnected from %s" % self.mqtt_config['SERVER'])

    def publish(self, payload):
        if not self.sub_state:
            self.connect()
        for topic in self.topics_config['PUB']:
            self.nprgb.show_color('green')
            self.conn.publish(topic, json.dumps(payload.get(topic)))
            mqtt_tool_log.info(f'published to topic: {topic}')
        if not self.sub_state:
            self.disconnect()
        self.nprgb.off()

    def sub_cb(self, sub_topic, msg):
        timer = Timer(0)
        # print('notify: {0}'.format(notify))
        timer.init(period=self.timeout, mode=Timer.ONE_SHOT, callback=self.timeout_callback)
        self.trigger_func(sub_topic, msg)
        mqtt_tool_log.info(f'sub_topic: {sub_topic} triggered!')
        timer.deinit()

    def subscribe(self, callback_func=None):
        timer = Timer(0)
        timer.init(period=self.timeout, mode=Timer.ONE_SHOT, callback=self.timeout_callback)
        if callback_func:
            self.trigger_func = callback_func
            mqtt_tool_log.info(f'self.trigger_func: {self.trigger_func}')
        self.conn.set_callback(self.sub_cb)
        self.connect()
        for topic in self.topics_config['SUB']:
            self.conn.subscribe(b"%s" % topic)
            mqtt_tool_log.info(f'topic: {topic} subscribed!')
        self.sub_state = True
        timer.deinit()

    def sub_listen(self, delay=0.05, normal_func=sub_listen_trigger):
        try:
            notify = self.conn.check_msg()
            # print('notify: {0}, type: {1}'.format(notify, type(notify)))
            if notify:
                mqtt_tool_log.info('notify: {0}'.format(notify))
            timer = Timer(0)
            timer.init(period=self.timeout, mode=Timer.ONE_SHOT, callback=self.timeout_callback)
            normal_func()
            mqtt_tool_log.info(f'func: {normal_func} is running!')
            timer.deinit()
            time.sleep(delay)
        except Exception as err:
            mqtt_tool_log.error(f'err: {err}')
            self.restart_and_reconnect(3)