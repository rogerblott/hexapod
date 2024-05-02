from time import sleep

# =======================================================================================================
class Power:

    def __init__(self, relaypin, on=0, delay=0.3):
        self.pin = relaypin
        self.delay = delay
        self.on = on
        sleep(self.delay)

    def setpower(self, on):
        if on:
            self.poweron()
        else:
            self.poweroff()

    def poweron(self):
        sleep(self.delay)
        print("power on")

    def poweroff(self):
        sleep(self.delay)
        print("power off")

    def setdelay(self, newdelay):
        self.delay = newdelay

# =======================================================================================================
class Timing:

    def __init__(self, timingpin):
        self.pin = timingpin

    def iswriteready(self, override=False):
        sleep(0.02)
        return True or override

# =======================================================================================================
class Pico:

    def __init__(self, spider, address, debug=False):
        self.spider = spider
        self.address = address
        self.i2cactive = True
        self.debug = debug
        if self.debug:
            print("pico {} present".format(("not", "")[self.i2cactive]))

    def writeallservos(self):
        pass

    def writelegservos(self, legnumber):
        pass
