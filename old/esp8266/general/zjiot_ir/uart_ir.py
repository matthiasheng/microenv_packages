import time
import ubinascii
from machine import UART
from zjiot_ir.codes import functions_map


class ZJIR:

    def __init__(self, uart_channel, uart_kw_parameters):
        self.uart = UART(uart_channel, **uart_kw_parameters)
        self.ex_learn_mode_str = '68 07 00 FF 20 1F 16'
        self.exit_ex_learn_mode_str = '68 07 00 FF 21 20 16'

    @staticmethod
    def encode_ir_str(ir_str, replace=True, sep=' '):
        if replace:
            ir_str = ir_str.replace(sep, '')
        return ubinascii.unhexlify(ir_str)

    @staticmethod
    def decode_ir_bytes(ir_bytes, split=True, sep=' '):
        if split:
            return ubinascii.hexlify(ir_bytes, sep).decode()
        return ubinascii.hexlify(ir_bytes).decode()

    def send_ir(self, ir_str):
        if self.uart.any():
            print(f'received: {self.decode_ir_bytes(self.uart.read())}')
        ir_bytes = self.encode_ir_str(ir_str)
        sent_bytes_count = self.uart.write(ir_bytes)
        print(f'sent {sent_bytes_count} bytes: \n{ir_bytes}')
        t = 0
        while not self.uart.any():
            time.sleep(0.01)
            t += 0.01
            print(f'waited {t} s...')
        print(f'received: {self.decode_ir_bytes(self.uart.read())}')

    def copy_ir_str(self, timeout=60):
        self.send_ir(self.ex_learn_mode_str)
        t = 0
        while not self.uart.any():
            time.sleep(0.01)
            t += 0.01
            print(f'waited {t} s...')
            if t >= timeout:
                self.send_ir(self.exit_ex_learn_mode_str)
                print(f'Timeout!')
                return
        ir_str = self.decode_ir_bytes(self.uart.read())
        print(f'received: {ir_str}')
        return ir_str

    def run(self):
        head = f'{"*"*100}'
        key_map = {str(i): key for i, key in enumerate(functions_map)}
        content = f'Choose one of the appliances below:\n{key_map}'
        end = f'{"*"*100}'
        msg = '\n'.join([head, content, end])
        print(msg)
        option = input(f'Please enter your choice, Q/q to exit:')
        if option in ['Q', 'q']:
            return
        if option not in key_map:
            print(f'Invalid choice, exit!')
        key_map_sub = {str(i): key for i, key in enumerate(functions_map.get(key_map.get(option)).keys())}
        content_sub = f'Choose one of the appliances below:\n{key_map_sub}'
        msg_sub = '\n'.join([head, content_sub, end])
        print(msg_sub)
        option_sub = input(f'Please enter your choice, Q/q to exit:')
        if option_sub in ['Q', 'q']:
            return
        if option_sub not in key_map_sub:
            print(f'Invalid choice, exit!')
        option_ir_str = functions_map.get(key_map.get(option)).get(key_map_sub.get(option_sub))
        print(f'option_ir_str: {option_ir_str}')
        self.send_ir(option_ir_str)
