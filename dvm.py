import serial
import time
import math
import config

class DVM:
    def __init__(self):
        self.tel = telnetlib.Telnet()
        self.results = {}
        self.voltage = 0
        self.connected = False

    def connect(self):
        try:
            self.tel.open(config.HOST, config.PORT, timeout=config.TIMEOUT)
        except socket.timeout:
            self.connected = False
            return self.connected
        self.connected = True
        return self.connected

    def disconnect(self):
        self.connected = False
        self.tel.close()

    def send(self, message):
        print("sending: {}".format(message))
        try:
            self.tel.write(message.encode())
        except AttributeError:
            print("Not Connected")

    def read(self):
        try:
            inp = self.tel.read_eager().decode("utf-8").strip()
            print(inp)
            return inp
        except EOFError:
            return "EOFError"
        except ValueError:
            return "EMPTY"

    def get_id(self):
        self.send(config.READ_ID)
        time.sleep(0.1)
        return self.read()

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
