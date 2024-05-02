from spidersettings import *
from time import sleep
from smbus import SMBus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# =======================================================================================================
class Power:

    def __init__(self, relaypin, on=0, delay=0.3):
        GPIO.setup(relaypin, GPIO.OUT)
        self.pin = relaypin
        self.delay = delay
        GPIO.output(self.pin, on)
        sleep(self.delay)

    def setpower(self, on):
        if on:
            self.poweron()
        else:
            self.poweroff()

    def poweron(self):
        GPIO.output(self.pin, 1)
        sleep(self.delay)
        print("power on")

    def poweroff(self):
        GPIO.output(self.pin, 0)
        sleep(self.delay)
        print("power off")

    def setdelay(self, newdelay):
        self.delay = newdelay

# =======================================================================================================
class Timing:

    def __init__(self, timingpin):
        self.pin = timingpin
        GPIO.setup(timingpin, GPIO.IN)

    def iswriteready(self, override=False):
        return (GPIO.input(self.pin)) or override

# =======================================================================================================
class Pico:

    def __init__(self, spider, address, debug=False):
        self.spider = spider
        self.address = address
        self.i2cactive = True
        self.i2c = SMBus(1)
        try:
            self.i2c.write_byte_data(PICOADDR, 0, 0)
        except Exception as e:
            print(e)
            self.i2cactive = False
        self.debug = debug
        if self.debug:
            print("pico {} present".format(("not", "")[self.i2cactive]))

    def writeallservos(self):
        stimes = []
        for leg in self.spider.servotimes:
            for joint in leg:
                stimes.append(joint & 255)
                stimes.append(joint >> 8)
        if self.i2cactive:
            self.i2c.write_i2c_block_data(self.address, LEG0BASEADDR, stimes[:18])
            self.i2c.write_i2c_block_data(self.address, LEG3BASEADDR, stimes[18:])

    def writelegservos(self, legnumber):
        stimes = []
        leg = self.spider.servotimes[legnumber]
        for joint in leg:
            stimes.append(joint & 255)
            stimes.append(joint >> 8)
        if self.i2cactive:
            self.i2c.write_i2c_block_data(self.address, legnumber*6, stimes)
