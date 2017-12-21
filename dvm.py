import serial
import time
import math
import config

# b'+0.04824E+1 VDC \r\n'

class DVM:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = config.PORT
        self.ser.baudrate = config.BAUD_RATE
        self.ser.timeout = config.TIMEOUT
        self.connected = False

    def connect(self):
        try:
            self.ser.open()
            self.ser.setRTS(False)
            self.ser.setDTR(False)
        except serial.SerialException:
            self.connected = False
            return self.connected
        self.connected = True
        return self.connected

    def disconnect(self):
        self.connected = False
        self.ser.close()

    def readline(self):
        eol = b'\r\n'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.ser.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)

    def send(self, message):
        #print("sending: {}".format(message))
        try:
            self.ser.write(message.encode())
            self.ser.write('\n'.encode())
        except AttributeError:
            print("Not Connected")

    def read(self):
        try:
            inp = str(self.readline())
            return inp
        except EOFError:
            return "EOFError"
        except ValueError:
            return "EMPTY"

    def decode_voltage(self, s):
        #print(s)
        try:
            #assert s[0] == 'b'
            #assert s[11] == '+'
            #print(s[14:17])
            #assert s[14:17] == 'VDC'
            #print(s[3:10])
            mant = float(s[3:10])
            exp = int(s[12])
            val = mant * (exp * 10)
            print(val)
            return val
        except IndexError:
            print('Index Error')
            return 0
        except ValueError:
            print('Value Error')
            return 0

    def get_id(self):
        self.send(config.READ_ID)
        time.sleep(0.1)
        return self.read()

    def read_value(self):
        self.send(config.READ_VOLTAGE)
        return self.decode_voltage(self.read())

    def read_voltage(self):
        self.send(config.READ_VOLTAGE)
        time.sleep(0.1)
        return self.read()

    def read_current(self):
        self.send(config.READ_CURRENT)
        time.sleep(0.1)
        return self.read()

    def is_on(self):
        self.send(config.IS_ON)
        time.sleep(0.1)
        return self.read()

    def set_ohms(self):
        self.send(config.SET_OHMS)

    def set_vdc(self):
        self.send(config.SET_VDC)

    def turn_on(self):
        self.send(config.TURN_ON)

    def turn_off(self):
        self.send(config.TURN_OFF)

    def set_voltage(self, v):
        self.voltage = v
        self.send("{} {:.2f}".format(config.SET_VOLTAGE, v))

    def set_current_limit(self, i):
        self.send("{} {:.2f}".format(config.SET_CURRENT_LIMIT, i))

    def start_ramp(self, a, b, i, t):
        self.turn_on()
        v = a
        while v < b:
            self.set_voltage(v)
            v += i
            time.sleep(t)
            reading = self.read_current()
            if reading == "EMPTY":
                reading = "0A"
            print(reading[:-1])
            measured_current = float(reading[:-1])
            print(measured_current)
            self.results[v] = measured_current
        self.send("{} {:.2f}".format(config.SET_VOLTAGE, v))
