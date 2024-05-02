from spidersettings import *
import math

# =======================================================================================================
class TripodWalk(object):

    def __init__(self, spider, walkdebug=False):
        self.spider = spider
        self.walkdebug = walkdebug
        legs = self.spider.legs
        self.walkgroups = [(legs[0], legs[2], legs[4]), (legs[1], legs[3], legs[5])]
        self.movetogroup = 1
        self.fwdshiftdelta = [0, 0, 0]
        self.backshiftdelta = [0, 0, 0]
        self.turnangle = 0
        self.heading = 1.57
        self.walknudges = STDWALKNUDGES
        self.stepsize = 100

    def nextstep(self):
        self.movetogroup = 1 - self.movetogroup

    def setstep(self, stepsize, speed):
        self.stepsize = stepsize
        self.walknudges = (100, 80, 60, 40, 20)[speed-1]

    def settravel(self, heading=0, turn=0.0):
        self.heading = heading
        self.turnangle = turn
        if self.walkdebug:
            print("tripod gait, heading {}, step size {}, turn angle {}".format(self.heading, self.stepsize, turn))
        self.fwdshiftdelta = [int(-math.cos(self.heading) * self.stepsize), int(-math.sin(self.heading) * self.stepsize), 0]
        self.backshiftdelta = [-delta for delta in self.fwdshiftdelta]
        for leg in self.spider.legs:
            if not leg.setstartend(self.fwdshiftdelta, self.turnangle):
                return False
        for leg in self.walkgroups[0]:
            leg.moveto(leg.startpos, self.walknudges)
        self.spider.moveall(self.walkdebug)
        for leg in self.walkgroups[1]:
            leg.moveto(leg.endpos, self.walknudges)
        self.spider.moveall(self.walkdebug)
        self.movetogroup = 1
        return True

    # indicate direction with sign of steps
    def travel(self, steps=1):
        if steps > 0:
            while steps and not self.spider.halt:
                if self.walkdebug:
                    print("tripod step {}".format(steps))
                for leg in self.walkgroups[self.movetogroup]:
                    leg.moveto(leg.startpos, self.walknudges)
                for leg in self.walkgroups[1-self.movetogroup]:
                    leg.move(self.fwdshiftdelta, self.turnangle, self.walknudges)
                self.spider.moveall(self.walkdebug)
                self.nextstep()
                steps -= 1
        if steps < 0:
            while steps and not self.spider.halt:
                if self.walkdebug:
                    print("tripod step {}".format(steps))
                self.nextstep()
                for leg in self.walkgroups[self.movetogroup]:
                    leg.moveto(leg.endpos, self.walknudges)
                for leg in self.walkgroups[1-self.movetogroup]:
                    leg.move(self.backshiftdelta, -self.turnangle, self.walknudges)
                self.spider.moveall(self.walkdebug)
                steps += 1
        if self.spider.halt:
            if self.walkdebug:
                print("spider halted with {} steps to run".format(steps))
                self.spider.halt = False

# =======================================================================================================
class WaveWalk(object):

    def __init__(self, spider, walkdebug=False):
        self.spider = spider
        self.walkdebug = walkdebug
        self.shiftdelta = [0, 0, 0]
        self.rotatedelta = 0
        self.stepsize = STEPDISTANCE
        self.stepangle = STEPANGLE
        self.heading = 1.57
        self.turnangle = 0
        self.walknudges = 30
        self.movetoleg = 0

    def nextstep(self, direction):
        self.movetoleg = (self.movetoleg + direction) % 6

    def setstep(self, stepsize, speed):
        self.stepsize = stepsize
        self.walknudges = (100, 80, 60, 40, 20)[speed-1]

    def settravel(self, heading=1.57, turn=0.0):

        # returns initial position based on legnumber
        def returninit(stepleg):
            percentstart = stepleg.legnumber / 5
            return [(stepleg.startpos[i] * percentstart) + (stepleg.endpos[i] * (1 - percentstart)) for i in range(3)]

        self.heading = heading
        if self.walkdebug:
            print("wave gait, heading {}, full wave range {}, turn angle {}".format(self.heading, self.stepsize, turn))
        fulldelta = [round(-math.cos(self.heading) * self.stepsize), round(-math.sin(self.heading) * self.stepsize), 0]
        self.shiftdelta = [delta/5 for delta in fulldelta]
        self.backshiftdelta = [-delta for delta in self.shiftdelta]
        self.turnangle = turn/5
        for group in ((0, 2, 4), (1, 3, 5)):
            for legnumber in group:
                leg = self.spider.legs[legnumber]
                if not leg.setstartend(fulldelta, turn):
                    return False
                leg.moveto(returninit(leg), self.walknudges)
            self.spider.moveall(self.walkdebug)
        self.movetoleg = 0
        return True

    # indicate direction with sign of steps
    def travel(self, steps=1):
        if steps > 0:
            while steps and not self.spider.halt:
                if self.walkdebug:
                    print("wave step {}".format(steps))
                for leg in self.spider.legs:
                    if leg.legnumber == self.movetoleg:
                        leg.moveto(leg.startpos, self.walknudges)
                    else:
                        leg.move(self.shiftdelta, self.turnangle, self.walknudges)
                self.spider.moveall(self.walkdebug)
                self.nextstep(1)
                steps -= 1
        if steps < 0:
            while steps and not self.spider.halt:
                if self.walkdebug:
                    print("wave step {}".format(steps))
                self.nextstep(-1)
                for leg in self.spider.legs:
                    if leg.legnumber == self.movetoleg:
                        leg.moveto(leg.endpos, self.walknudges)
                    else:
                        leg.move(self.backshiftdelta, -self.turnangle, self.walknudges)
                self.spider.moveall(self.walkdebug)
                steps += 1
        if self.spider.halt:
            self.spider.halt = False
            if self.walkdebug:
                print("spider halted with {} steps to run".format(steps))

