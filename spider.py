# system parameters
import time
from spidersettings import *
try:
    from spiderpico import *
    print("standard pico interface loaded")
except Exception as e:
    from spiderpico1 import *
    print("dummy pico interface loaded")
from spiderleg import Leg
from spiderwalk import TripodWalk, WaveWalk

# =======================================================================================================
class Spider(object):

    def __init__(self, poweron, spiderdebug=False, walkdebug=False, nudgedebug=False, picodebug=False):
        leg0 = Leg(self, LEG0ACTIVE, 0, HIP0, SERVOOFFSETHIP0, INITFOOT0REL)
        leg1 = Leg(self, LEG1ACTIVE, 1, HIP1, SERVOOFFSETHIP1, INITFOOT1REL)
        leg2 = Leg(self, LEG2ACTIVE, 2, HIP2, SERVOOFFSETHIP2, INITFOOT2REL)
        leg3 = Leg(self, LEG3ACTIVE, 3, HIP3, SERVOOFFSETHIP3, INITFOOT3REL)
        leg4 = Leg(self, LEG4ACTIVE, 4, HIP4, SERVOOFFSETHIP4, INITFOOT4REL)
        leg5 = Leg(self, LEG5ACTIVE, 5, HIP5, SERVOOFFSETHIP5, INITFOOT5REL)
        self.legs = [leg0, leg1, leg2, leg3, leg4, leg5]

        self.debug = spiderdebug
        self.walkdebug = walkdebug
        self.moveonlydebug = True

        self.pico = Pico(self, PICOADDR, picodebug)
        self.power = Power(RELAYPIN, 1)
        self.timing = Timing(TIMINGPIN)

        self.spidermoving = False
        self.movecompleted = False
        self.nudgecount = 0
        self.halt = False
        self.sitting = False
        self.standing = False
        self.centred = False

        self.walkgaits = (TripodWalk(self, walkdebug), WaveWalk(self, walkdebug))
        self.gaitindex = TRIPODWALK
        self.gait = self.walkgaits[self.gaitindex]
        self.heading = 1.57
        self.turn = 0
        self.stepsize = 100
        self.speed = 3
        self.newtravel = True

        self.elapsedtime = time.time()
        self.recentreinterval = RECENTRETIMEOUT
        self.powerdowndelay = POWERDOWNTIMEOUT
        self.poweredoff = False
        self.powerdowntime = time.time() + self.powerdowndelay
        self.recentretime = time.time() + self.recentreinterval

        self.power.setpower(poweron)
        self.servotimes = [[1500, 1200, 1500] for _ in self.legs]
        self.servotimes.append([1500, 1500, 1500])
        if self.debug:
            print("reset all legs to safe position")
        for leg in self.legs:
            leg.printnudges = nudgedebug
            leg.start()
        self.recentre()

    def moveall(self, debug=False):
        self.movedebug = debug
        self.nudgecount = 0
        self.movecompleted = False
        self.spidermoving = True
        self.elapsedtime = time.time()
        while not self.movecompleted:
            pass

    def poweron(self):
        self.power.setpower(True)
        self.poweredoff = False

    def poweroff(self):
        self.power.setpower(False)
        self.poweredoff = True

    def printstatus(self, alllegs):
        for leg in self.legs:
            leg.printstatus(alllegs)

    def shutdown(self, debug=False):
        self.safe(debug)
        self.poweroff()

    def kickwatchdog(self):
        self.powerdowntime = time.time() + self.powerdowndelay

    def testpowerdown(self):
        if (time.time() > self.powerdowntime) and not self.poweredoff:
            if self.debug:
                print("auto-power down")
            self.shutdown()

    def autorecentre(self, debug=False):
        if not self.centred and time.time() > self.recentretime:
            print("auto-recentering legs")
            self.recentre(debug)

    def recentre(self, debug=False):
        debug = debug or self.debug
        if not self.centred:
            for legpair in ((0, 5), (1, 4), (2, 3)):
                if self.legs[legpair[0]].recentreleg() + self.legs[legpair[1]].recentreleg():
                    if debug:
                        print("recentre legs pair", legpair)
                    self.moveall(debug)
            if debug:
                print("recentering complete")
        else:
            if debug:
                print("legs already centred")
        self.centred = True
        self.newtravel = True

    def safe(self, debug=False):
        debug = debug or self.debug
        if self.poweredoff:
            self.poweron()
        if self.standing:
            self.sit()
        if self.sitting:
            for leg in self.legs:
                leg.move([0, 0, 30], 0, 30)
            self.moveall()
        self.sitting = False
        self.standing = False
        self.newtravel = True
        if debug:
            print("legs in safe position")
            self.printstatus(False)

    def sit(self, debug=False):
        debug = debug or self.debug
        if self.poweredoff:
            self.safe()
        if not self.sitting:
            self.recentre(debug)
            for leg in self.legs:
                leg.sit()
            self.moveall(debug)
            if debug:
                print("sitting complete")
        else:
            print("already in sitting")
        self.sitting = True
        self.standing = False
        self.newtravel = True

    def stand(self, debug=False):
        debug = debug or self.debug
        if self.standing:
            self.recentre(debug)
        else:
            if not self.sitting:
                self.sit()
            elif not self.centred:
                self.recentre(debug)
            if debug:
                print("move legs to standing position")
            for leg in self.legs:
                leg.stand()
            self.moveall(debug)
        if debug:
            print("standing complete")
        self.standing = True
        self.sitting = False
        self.newtravel = True

    def setwalk(self, **kwargs):
        print(kwargs)
        if kwargs:
            self.gaitindex = kwargs.get("gait", self.gaitindex)
            self.stepsize = kwargs.get("stepsize", self.stepsize)
            self.speed = kwargs.get("speed", self.speed)
            self.turn = kwargs.get("turn", self.turn)
            self.heading = kwargs.get("heading", self.heading)
            self.gait = self.walkgaits[self.gaitindex]
            self.newtravel = True

    def walk(self, steps=1):
        debug = self.debug or kwargs.get("debug", False)
        print(steps)
        if not self.standing:
            self.stand(debug)
        if self.newtravel:
            self.gait.setstep(self.stepsize, self.speed)
            if self.gait.settravel(self.heading, self.turn):
                self.centred = False
                self.newtravel = False
            else:
                print("walk failed")
                return False
        self.gait.travel(steps)
        self.recentretime = time.time() + self.recentreinterval

# =======================================================================================================
class Command(object):

    def __init__(self):
        self.command = ''
        self.commandpresent = False
        self.spidercommand = False

    def execute(self):
        if self.commandpresent:
            self.commandpresent = False
            if spidercommand:
                exec(self.command)
            else:
                exec(self.command)

    def get(self):
        result = self.command
        self.commandpresent = False
        self.command = ''
        return result

    def set(self, newcommand):
        self.command = newcommand
        self.commandpresent = True
