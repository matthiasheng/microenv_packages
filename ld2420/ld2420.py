import time
import ubinascii
from machine import UART


class LD2420:

    def __init__(self, uart_channel, uart_kw_parameters):
        self.uart = UART(uart_channel, **uart_kw_parameters)
        self.onstr = 'FD FC FB FA 02 00 FE 00 04 03 02 01'
        self.offstr = 'FD FC FB FA 04 00 FF 00 01 00 04 03 02 01'

    @property
    def raw_data(self):
        return self.uart.read()

    @property
    def last_data(self):
        if self.raw_data:
            return self.raw_data.decode().split('\r\n')[-3:-1]
        else:
            return None

    @property
    def last_data_op(self):
        _ = self.uart.write(ubinascii.unhexlify(self.onstr.replace(' ', '')))
        _ = self.uart.read()
        while not self.uart.any():
            time.sleep(0.001)
        data = self.uart.read()
        _ = self.uart.write(ubinascii.unhexlify(self.offstr.replace(' ', '')))
        _ = self.uart.read()
        return data.decode().split('\r\n')[-3:-1]

    def get_distance(self):
        # if self.get_presence() == 1:
        #     return int(self.last_data[1].split(' ')[1])
        if self.get_presence() == -1:
            return
        return int(self.last_data_op[1].split(' ')[1])

    def get_presence(self):
        # if self.last_data and self.last_data[0] == 'ON':
        #     return 1
        # elif self.last_data and self.last_data[0] == 'OFF':
        #     return 0
        # else:
        #     return -1
        if self.last_data_op:
            if self.last_data_op[0] == 'ON':
                return 1
            if self.last_data_op[0] == 'OFF':
                return 0
            else:
                return -1
        else:
            return -1

    def run(self):

        while True:
            print(f'presence: {self.get_presence()}, distance: {self.get_distance()}')
            time.sleep(0.001)
