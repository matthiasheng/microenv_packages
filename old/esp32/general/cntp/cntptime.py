try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct
import utime
import machine
from machine import reset


# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
# NTP_DELTA = 3155673600

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
#host = "pool.ntp.org"
# host = "192.168.3.3"
# time_diff_in_hour = 8

class CNTP:
    def __init__(self, cntp_config):
        self.ntp_host = cntp_config['ntp_host']
        self.NTP_DELTA = cntp_config['NTP_DELTA']
        self.time_diff_in_hour = cntp_config['time_diff_in_hour']

    def gettime(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo(self.ntp_host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
            val = struct.unpack("!I", msg[40:44])[0]
        except Exception as err:
            val = 0
            pass

        finally:
            s.close()

        return val - self.NTP_DELTA

    # There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
    def settime(self):
        t = self.gettime()
        c = 0
        while t < 0:
            t = self.gettime()
            c += 1
            print('get time from ntp server error, retry {0}: '.format(c))
            utime.sleep(0.5)
            if c >= 10:
                reset()
        tm = utime.gmtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3] + self.time_diff_in_hour, tm[4], tm[5], 0))

    def getdatetime(self):
        rtc = machine.RTC()
        self.settime()
        datetime = rtc.datetime()
        # print('datetime: {0}'.format(datetime))
        return '{0}-{1}-{2} {3}:{4}:{5}'.format(datetime[0], datetime[1], datetime[2], datetime[4], datetime[5], datetime[6])

    def showtime(self):
        datetime = self.getdatetime()
        print('Current time --> {0}'.format(datetime))
