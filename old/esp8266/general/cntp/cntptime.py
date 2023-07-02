try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct
import utime
import logging
from machine import reset, RTC


cntp_log = logging.getLogger(__name__)

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
# NTP_DELTA = 3155673600

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
#host = "pool.ntp.org"
# host = "192.168.3.3"
# time_diff_in_hour = 8


class CNTP:
    """
    rtc.datetime(): (2022, 7, 17, 6, 14, 16, 38, 577) -> (year, month, day, weekday, hours, minutes, seconds, subseconds)
    time.gmtime(): (2022, 7, 17, 14, 25, 18, 6, 198) -> (year, month, mday, hour, minute, second, weekday, yearday)
    in micropython, weekday is +1 automatically to convert to a more usual way of represeting weekday (1-7) for (Mon - Sun)
    """
    def __init__(self, cntp_config):
        self.ntp_host = cntp_config['ntp_host']
        self.NTP_DELTA = cntp_config['NTP_DELTA']
        self.time_diff_in_hour = cntp_config['time_diff_in_hour']
        self.rtc = RTC()
        self.tm_mod = None
        self.tm_mod_offline = None

    def gettime(self):
        """
        return time in seconds after 2000 from local ntp server
        Time Epoch: Unix port uses standard for POSIX systems epoch of 1970-01-01 00:00:00 UTC. However, embedded ports use epoch of 2000-01-01 00:00:00 UTC
        """
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo(self.ntp_host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            cntp_log.debug(f'res: {res}')
            msg = s.recv(48)
            val = struct.unpack("!I", msg[40:44])[0]
            cntp_log.debug(f'val: {val}')
        except Exception as err:
            cntp_log.debug(f'err: {err}')
            val = 0

        finally:
            s.close()

        return val - self.NTP_DELTA

    # There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
    def settime(self):
        """
        get time in seconds after 2000 from local ntp server and set time to the RTC
        Time Epoch: Unix port uses standard for POSIX systems epoch of 1970-01-01 00:00:00 UTC. However, embedded ports use epoch of 2000-01-01 00:00:00 UTC
        return: True for success, False for failure
        """
        t = self.gettime()
        if t < 0 and self.tm_mod:
            return False
        c = 0
        while t < 0 and not self.tm_mod:
            t = self.gettime()
            c += 1
            cntp_log.info(f'Unable to reach {self.ntp_host}. Retry {c} time -> t: {t}')
            utime.sleep(1)
            if c >= 10:
                cntp_log.warning(f'Try to reset and reconnect to ntp server!')
                reset()
        tm = utime.gmtime(t)
        self.tm_mod = (tm[0], tm[1], tm[2], tm[6] + 1, tm[3] + self.time_diff_in_hour, tm[4], tm[5], 0)
        self.rtc.datetime(self.tm_mod)
        return True

    def getdatetime(self):
        if not self.settime():
            cntp_log.info(f'{self.tm_mod}: settime unsuccesfully!')
        else:
            cntp_log.info(f'{self.tm_mod}: settime succesfully!')
        return self.getdatetime_offline()
        # datetime = self.rtc.datetime()
        # print('datetime: {0}'.format(datetime))
        # return self.getdatetime_online()

    def getdatetime_offline(self):
        self.tm_mod_offline = self.rtc.datetime()
        return '{0}-{1}-{2} {3}:{4}:{5}'.format(self.tm_mod_offline[0], self.tm_mod_offline[1], self.tm_mod_offline[2], self.tm_mod_offline[4], self.tm_mod_offline[5], self.tm_mod_offline[6])

    # def getdatetime_online(self):
    #     return '{0}-{1}-{2} {3}:{4}:{5}'.format(self.tm_mod[0], self.tm_mod[1], self.tm_mod[2], self.tm_mod[4], self.tm_mod[5], self.tm_mod[6])

    def showtime(self):
        tm_mod = self.getdatetime()
        cntp_log.info('Current time --> {0}'.format(tm_mod))
