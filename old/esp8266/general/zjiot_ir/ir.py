import time
import ubinascii
from machine import UART


uart = UART(1, baudrate=115200, tx=1, rx=2, bits=8, parity=None, stop=1, timeout=50)
ex_learn_mode_str = '68 07 00 FF 20 1F 16'
exit_ex_learn_mode_str = '68 07 00 FF 21 20 16'
ok_reply_str = '68 08 00 00 01 00 01 16'
timeout_reply_str = '68 08 00 00 22 13 35 16'
# MeiBo aircon
off_code_str = '68 FF 00 00 22 E4 05 A5 07 3E D9 01 3E D9 01 3D D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E 50 3A 50 3B 50 3A 50 3A 50 3A 50 3A 50 3A 50 3A D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E 50 3B 50 3A 50 3D 4D 3A 50 3B 50 3B 50 3D 4D 3D D6 01 41 D6 01 3E D9 01 41 D6 01 41 D6 01 41 D5 01 41 D6 01 41 D6 01 41 4A 41 4D 3E 4D 3E 4D 3E 4A 41 4D 3E 4A 40 4D 3E D6 01 41 D5 01 41 D5 01 41 4D 3E 4D 3E D5 01 41 D5 01 41 D5 01 41 4C 41 4A 41 4A 41 D2 01 45 D2 01 45 49 42 49 42 49 42 D1 01 48 45 45 D1 01 46 45 46 D1 01 46 45 46 D0 01 46 D1 01 46 45 46 D1 01 46 45 46 CE 01 49 45 45 CE 01 48 45 45 45 45 45 45 CE 01 48 46 41 D2 01 45 46 44 D2 01 44 47 43 47 43 D3 01 41 4A 40 D6 01 40 4A 40 D6 01 40 4B 40 D6 01 40 D6 01 40 A1 07 40 47 16'
on_code_str = '68 FF 00 00 22 E4 05 A4 07 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E 50 3A 50 3A 50 3A 50 3B 50 3B 50 3A 50 3A 50 3A D9 01 3E D8 01 3E D9 01 3E D9 01 41 D6 01 3E D9 01 3E D9 01 3E D9 01 3E 50 3A 50 3D 4D 3E 4A 40 4D 3D 4D 3D 4D 3D 4D 3A D9 01 41 D6 01 41 D6 01 41 D6 01 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 4D 3E 4D 3E 4D 3E 4A 41 4D 3E 4D 3E 4D 3E 4D 3E D5 01 41 4D 3E D5 01 41 4D 3E 4A 41 D5 01 41 D5 01 44 D2 01 44 4A 41 D2 01 45 49 41 D2 01 45 D2 01 45 49 42 49 42 48 42 D1 01 49 45 42 D4 01 46 45 46 D1 01 46 44 46 D0 01 46 D0 01 46 45 46 D1 01 46 45 46 CE 01 48 45 46 CE 01 49 45 45 45 45 45 45 CE 01 48 46 42 D2 01 45 46 44 D2 01 44 47 44 47 44 D3 01 43 47 43 D3 01 40 4A 43 D3 01 40 4A 40 D6 01 40 D6 01 40 A1 07 40 43 16'
up_temp = '68 FF 00 00 22 E4 05 A3 07 3E D8 01 3E D8 01 3E D8 01 3E D9 01 41 D5 01 3E D9 01 40 D6 01 3E D8 01 3E 50 3A 50 3E 4D 3B 50 3E 4A 3E 50 3B 50 3E 4D 3E D5 01 3E D8 01 41 D5 01 41 D5 01 41 D5 01 3E D8 01 41 D5 01 3E D9 01 41 4D 3E 4A 41 4A 41 4D 3E 4A 41 4A 41 4A 41 4A 41 D5 01 41 4A 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 4A 41 D5 01 41 4D 3E 4A 41 49 41 49 44 46 44 4A 3E D5 01 41 49 41 D5 01 42 4A 44 D2 01 44 D2 01 45 D2 01 45 D2 01 45 46 44 D2 01 45 49 42 D1 01 45 45 45 49 42 49 42 48 45 CE 01 49 D1 01 46 45 46 44 46 D0 01 46 44 46 D0 01 46 D0 01 46 44 46 45 46 CE 01 48 CE 01 49 45 45 CE 01 49 45 45 45 45 45 45 CF 01 45 49 41 D2 01 45 46 44 D2 01 44 47 43 47 43 D3 01 40 4A 40 D6 01 40 4A 40 D6 01 40 4B 40 D6 01 40 D6 01 40 A0 07 40 36 16'
down_temp = '68 FF 00 00 22 E6 05 A1 07 40 D6 01 40 D6 01 3D D9 01 40 D6 01 40 D6 01 40 D6 01 3D D9 01 40 D6 01 40 4E 3A 50 3A 50 3D 4D 3D 4D 3D 4D 3A 50 3B 50 3A D9 01 3E D9 01 3E D9 01 3E D9 01 3E D8 01 3E D8 01 3E D9 01 3D D9 01 3E 50 3B 50 3A 50 3A 50 3B 50 3A 50 3A 50 3A 50 3B 50 3A 50 3A D9 01 3E D9 01 3D D9 01 3D D9 01 3E D9 01 3E D9 01 40 D6 01 3E D9 01 40 4D 3B 50 3A 50 3D 4D 3D 4D 3D 4D 3B D9 01 41 4D 3D D6 01 41 4D 3D D5 01 41 D5 01 41 D6 01 41 D5 01 41 4D 3E D5 01 41 4D 3E D5 01 41 4D 3E 4D 41 49 42 49 42 49 42 49 42 D4 01 43 48 45 D1 01 46 45 45 D1 01 46 D0 01 46 D1 01 46 D1 01 46 44 46 CE 01 49 45 45 CE 01 49 45 45 45 45 45 42 D1 01 45 49 41 D1 01 45 46 44 D2 01 44 47 43 47 43 D3 01 40 4A 40 D6 01 41 4A 40 D6 01 40 4A 40 D6 01 40 D6 01 40 A1 07 40 30 16'
slider = '68 FF 00 00 22 E4 05 A4 07 3E D9 01 3E D9 01 3E D8 01 3E D8 01 3E D9 01 3E D9 01 3E D9 01 3E D9 01 3E 50 3B 4D 3E 50 3B 50 3B 50 3D 4D 3E 4D 3D 4D 3E D5 01 3E D8 01 3E D8 01 41 D6 01 41 D5 01 41 D5 01 3E D8 01 41 D6 01 3E 50 3E 4A 41 49 41 4D 3E 4A 41 4A 41 4D 3E 4A 41 4A 41 4D 3E 4A 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 D5 01 41 D5 01 42 4D 3E 4A 41 49 41 4D 3E 4A 41 D5 01 45 49 41 D2 01 45 46 41 4A 41 D5 01 42 D5 01 45 D2 01 45 49 41 D2 01 45 49 41 D2 01 45 D1 01 45 49 42 49 42 48 42 49 42 49 42 D1 01 49 45 46 D1 01 46 44 46 D0 01 46 D0 01 46 D1 01 46 D1 01 46 45 46 D1 01 46 44 46 CE 01 49 45 45 45 45 45 45 CE 01 48 45 44 CF 01 48 46 41 D2 01 44 46 44 47 43 D3 01 41 4A 43 D3 01 44 47 43 D3 01 40 4A 40 D6 01 40 D6 01 40 A0 07 40 41 16'

# Midea Fan
on_code_str1 = '68 84 00 00 22 D3 08 B0 04 43 D1 01 43 46 43 4A 40 46 43 46 43 46 43 46 43 47 43 4A 40 D1 01 43 D1 01 43 D1 01 43 D1 01 44 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 49 40 46 43 46 43 47 43 46 43 46 43 46 43 46 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 4A 40 46 43 46 43 46 43 47 43 46 43 4A 40 46 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 CC 16'
fan_speed_str = '68 84 00 00 22 D3 08 B0 04 43 D0 01 40 4A 40 4C 3D 4A 40 4C 3D 4C 3D 49 43 49 3D 4C 3D D3 01 41 D3 01 44 D0 01 41 D3 01 43 D1 01 44 D0 01 44 D0 01 44 D0 01 43 D1 01 43 D0 01 40 49 42 48 43 46 43 4A 3D 4D 3D 4D 3D 4A 40 4D 3D D4 01 40 D4 01 40 D4 01 3F D7 01 3A DA 01 3A DA 01 3D D7 01 3D D7 01 3D 4C 3E 4C 3E 4C 41 48 41 48 42 48 41 48 42 48 42 CF 01 45 CF 01 45 CF 01 45 CF 01 44 D0 01 44 CD 16'
fan_rotate_str = '68 84 00 00 22 D6 08 AD 04 44 D1 01 43 46 43 46 44 46 43 3A 50 46 43 46 43 3A 50 46 43 D1 01 43 D1 01 43 D1 01 44 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 D1 01 43 46 43 46 43 D1 01 43 46 44 46 43 46 43 46 43 46 44 D1 01 44 D1 01 44 46 44 D1 01 43 D1 01 43 D1 01 44 D1 01 43 D1 01 43 46 43 46 44 D1 01 43 46 44 46 44 46 43 46 43 46 43 D1 01 43 D1 01 43 46 43 D1 01 43 D1 01 43 D1 01 40 CF 16'
functions_map = {
    'aircon': {
        'on': on_code_str,
        'off': off_code_str,
        'up': up_temp,
        'down': down_temp,
        'rotate': slider
    },
    'fan': {
        'power': on_code_str1,
        'speed': fan_speed_str,
        'rotate': fan_rotate_str
    }
}


def code_str2int_list(code_str):
    return [int(x, 16) for x in code_str.split(' ')]


def int_list2bytearray(int_list):
    return bytearray(int_list)


def encode_ir_str(ir_str, replace=True, sep=' '):
    if replace:
        ir_str = ir_str.replace(sep, '')
    return ubinascii.unhexlify(ir_str)


def decode_ir_bytes(ir_bytes, split=True, sep=' '):
    if split:
        return ubinascii.hexlify(ir_bytes, sep).decode()
    return ubinascii.hexlify(ir_bytes).decode()


def send_ir(ir_str):
    if uart.any():
        print(f'received: {decode_ir_bytes(uart.read())}')
    ir_bytes = encode_ir_str(ir_str)
    sent_bytes_count = uart.write(ir_bytes)
    print(f'sent {sent_bytes_count} bytes: \n{ir_bytes}')
    t = 0
    while not uart.any():
        time.sleep(0.01)
        t += 0.01
        print(f'waited {t} s...')
    print(f'received: {decode_ir_bytes(uart.read())}')


def copy_ir_str(timeout=60):
    send_ir(ex_learn_mode_str)
    t = 0
    while not uart.any():
        time.sleep(0.01)
        t += 0.01
        print(f'waited {t} s...')
        if t >= timeout:
            send_ir(exit_ex_learn_mode_str)
            print(f'Timeout!')
            return
    ir_str = decode_ir_bytes(uart.read())
    print(f'received: {ir_str}')
    return ir_str


def run():
    t = 0
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
    send_ir(option_ir_str)


if __name__ == '__main__':
    run()
