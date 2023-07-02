import os
import time
import network
import logging
import ubinascii


wifi_driver_log = logging.getLogger('wifi_driver_sta_mode')


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
            1000: "STAT_IDLE – no connection and no activity(esp32s2)",
            8: "STAT_IDLE – no connection and no activity(esp32c3)"
        }

    def get_network_details(self):
        self.ip, self.subnet_mask, self.gateway, self.DNS_server = self.wlan.ifconfig()
        if self.ip != self.sta_config.get('ip'):
            wifi_driver_log.warning(f'current ip: {self.ip} != wanted ip: {self.sta_config.get("ip")}')
        wifi_driver_log.info('ip: {0}'.format(self.ip))
        wifi_driver_log.info('subnet_mask: {0}'.format(self.subnet_mask))
        wifi_driver_log.info('gateway: {0}'.format(self.gateway))
        wifi_driver_log.info('DNS_server: {0}'.format(self.DNS_server))

    def connect(self):
        timeout = len(self.router_config) * 10
        for ap, password in self.router_config.items():
            t = 0
            wifi_driver_log.info(f'Connecting to AP: "{ap}"...')
            self.wlan.connect(ap, password)
            while t < timeout and not self.wlan.isconnected():
                for i in range(10):
                    wifi_status = self.check_status()
                    wifi_connected = self.wlan.isconnected()
                    wifi_driver_log.info(f'AP: "{ap}" connection status: "{wifi_status}".')
                    wifi_driver_log.info(f'AP: "{ap}" self.wlan.isconnected(): "{wifi_connected}".')
                    if wifi_connected:
                        return True
                    time.sleep(1)
                    t += 1
        wifi_driver_log.error('All ap failed to connect, try again later! status: {0}'.format(self.check_status()))
        return False

    def disconnect(self):
        self.wlan.disconnect()

    def scan(self):
        found_networks = sorted(self.wlan.scan(), key=lambda x: x[3], reverse=True)
        wifi_driver_log.info(f'Found {len(found_networks)} APs.')
        for i, found_network in enumerate(found_networks):
            wifi_driver_log.debug(f'found network {i+1}/{len(found_networks)}:')
            wifi_driver_log.debug(f'found_network_info: {found_network}')
            ap = found_network[0].decode()
            bssid = ubinascii.hexlify(found_network[1]).decode()
            channel = found_network[2]
            rssi = found_network[3]
            authmode = self.authmodes.get(found_network[4]) if self.authmodes.get(found_network[4]) else 'Undefined'
            hidden = self.hidden_codes.get(found_network[5]) if self.hidden_codes.get(found_network[5]) else 'Undefined'
            wifi_driver_log.debug('ap_name: {0}, bssid: {1}, channel: {2}, rssi: {3} %, authmode: {4}, hidden: {5}'.format(ap, bssid, channel, self.get_rssi_percent(rssi), authmode, hidden))

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
        wifi_driver_log.debug(f'raw_rssi: {rssi}, rssi_percent: {rssi_percent} %')
        return rssi_percent
