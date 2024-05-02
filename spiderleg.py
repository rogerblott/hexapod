from spidersettings import *
import math
import time

OVERRIDE = False

# =======================================================================================================
class Leg(object):

    def __init__(self, spider, active, legnumber, hipposition, hipoffset, startpositionrelative):
        # fixed physical
        self.femurlen = FEMURLENGTH
        self.tibialen = TIBIALENGTH
        self.footlen = FOOTLENGTH
        self.servomax = SERVOMAX
        self.servomin = SERVOMIN
        self.t2f2 = self.tibialen * self.tibialen + self.footlen * self.footlen
        self.tfx2 = 2 * self.tibialen * self.footlen

        # orientation
        self.spider = spider
        self.legactive = active
        self.legnumber = legnumber
        self.hipposition = hipposition
        self.jointoffset = (hipoffset, SERVOOFFSETKNEE, SERVOOFFSETANKLE)
        self.startposition = [self.hipposition[i] + startpositionrelative[i] for i in range(3)]
        self.upr = [USECPERRAD, -USECPERRAD, USECPERRAD]
        self.servocentre = CENTRES[legnumber]

        # movement constants (but can be altered)
        self.zsit = ZSIT
        self.zstand = ZSTAND
        self.liftincrement = LIFTDISTANCE/LIFTNUDGES
        self.sitnudges = SITNUDGES
        self.standnudges = STANDNUDGES

        # computed values
        self.jointangles = [0] * 3
        self.foottarget = self.startposition
        self.walkcentre = self.foottarget

        # dynamic move parameters
        self.nudges = 0
        self.nudge = 0
        self.moveincrement = [0, 0, 0]
        self.rotatematrix = [[0, 0], [0, 0]]
        self.lift = False
        self.legmoved = False
        self.startpos = []
        self.endpos = []

        # control
        self.printnudges = False
        self.error = False

    def start(self, delay=0.2):
        self.foottarget = self.startposition
        self.error = self.computeservos(self.foottarget)
        self.spider.pico.writelegservos(self.legnumber)
        time.sleep(delay)

    def makerotatematrix(self, deltatheta):
        cos = math.cos(deltatheta)
        sin = math.sin(deltatheta)
        self.rotatematrix = [[cos, -sin], [sin, cos]]

    def rotatefoot(self, footvector):
        footvector[0] = self.rotatematrix[0][0] * footvector[0] + self.rotatematrix[0][1] * footvector[1]
        footvector[1] = self.rotatematrix[1][0] * footvector[0] + self.rotatematrix[1][1] * footvector[1]
        return footvector

    def setstartend(self, fulldelta, turnangle):
        startpos = [(self.walkcentre[i] - fulldelta[i] / 2) for i in range(2)] + [self.foottarget[2]]
        endpos = [startpos[i] + fulldelta[i] for i in range(2)] + [self.foottarget[2]]
        self.makerotatematrix(turnangle/2)
        self.startpos = self.rotatefoot(startpos)
        if self.computeservos(self.startpos):
            print("start pos {} outside range of servos".format(self.startpos))
            return False
        self.makerotatematrix(-turnangle/2)
        self.endpos = self.rotatefoot(endpos)
        if self.computeservos(self.endpos):
            print("end pos {} outside range of servos".format(self.endpos))
            return False
        if self.spider.walkdebug:
            print("{} startpos {}, endpos {}".format(self.legnumber, intvec(self.startpos), intvec(self.endpos)))
        return True

    def computeservos(self, targetfoot):
        leg = [targetfoot[i] - self.hipposition[i] for i in range(3)]
        lenxy = math.sqrt(leg[0]*leg[0] + leg[1]*leg[1]) - self.femurlen
        arg0 = (lenxy * lenxy + leg[2]*leg[2] - self.t2f2) / self.tfx2
        self.error = 0
        q0, q1, q2 = 0, 0, 0
        try:
            q2 = -math.acos(arg0)
            try:
                q1 = math.atan2(leg[2], lenxy) - math.atan2(self.footlen * math.sin(q2), self.tibialen + self.footlen * arg0)
                try:
                    q0 = math.atan2(leg[1], leg[0])
                except:
                    self.error = 10
            except:
                self.error = 20
        except:
            self.error = 30
        if not self.error:
            self.jointangles = [q0, q1, q2]
            servotimes = [0] * 3
            servoangles = []
            for joint in range(3):
                servoangle = self.jointangles[joint] - self.jointoffset[joint]
                if abs(servoangle) > 3.14:
                    servoangle = self.jointangles[joint] + self.jointoffset[joint]
                servotimes[joint] = int(servoangle * self.upr[joint] + self.servocentre[joint])
                servoangles.append(servoangle)
                if servotimes[joint] > self.servomax:
                    self.error = 40+joint
                if servotimes[joint] < self.servomin:
                    self.error = 50+joint

            if not self.error:
                self.spider.servotimes[self.legnumber] = servotimes
            else:
                print("*** servotimes", servotimes, end='')
                print(", joint angles [{:.2f}, {:.2f}, {:.2f}], servoangles [{:.2f}, {:.2f}, {:.2f}]".format(q0, q1, q2, servoangles[0], servoangles[1], servoangles[2]))
        return self.error

    # set up a foot move ready to be nudged, default no lift
    def move(self, footlateraldelta, footrotatedelta, nudges, lift=NOLIFT):
        self.lift = lift
        self.nudges = max(nudges, MINNUDGES)
        self.moveincrement = [footlateraldelta[i]/nudges for i in range(3)]
        self.makerotatematrix(-footrotatedelta/nudges)
        self.nudge = self.nudges
        if self.spider.walkdebug:
            mode = ("no lift", "lifting")[lift]
            print("{} move by delta {} from {}, turn delta {}, {} nudges, {}".format(self.legnumber,
                                                                                     intvec(footlateraldelta), intvec(self.foottarget), footrotatedelta, self.nudges, mode))
        self.legmoved = True

    # set up a foot move absolute ready to be nudged, default lift
    def moveto(self, footposition, nudges=STDNUDGES, lift=LIFT):
        self.lift = lift
        self.nudges = max(nudges, MINNUDGES)
        delta = [footposition[i] - self.foottarget[i] for i in range(3)]
        self.moveincrement = [delta[i]/nudges for i in range(3)]
        self.makerotatematrix(NOROTATE)
        self.nudge = self.nudges
        if self.spider.walkdebug:
            mode = ("no lift", "lifting")[lift]
            print("{} move to {} from {} in {} nudges, {}".format(self.legnumber,
                                                                  intvec(footposition), intvec(self.foottarget), self.nudges, mode))
        self.legmoved = True

    # do one nudge of a leg, returns 0 when finished
    def nudgeleg(self):
        if not self.legactive:
            return 0
        if self.nudge:
            self.foottarget = [self.foottarget[i] + self.moveincrement[i] for i in range(3)]
            self.foottarget = self.rotatefoot(self.foottarget)
            if self.lift:
                if self.nudge > self.nudges-LIFTNUDGES:
                    self.foottarget[2] += self.liftincrement
                if self.nudge < (LIFTNUDGES+1):
                    self.foottarget[2] -= self.liftincrement
            self.computeservos(self.foottarget)
            if self.printnudges:
                self.printstatus()
            self.nudge -= 1
        return self.nudge

    def recentreleg(self):
        distance = int(max([abs(self.walkcentre[i] - self.foottarget[i]) for i in range(2)]))
        if distance > 2:
            self.moveto(self.walkcentre[:2] + [self.foottarget[2]], MINNUDGES)
            return distance
        return 0

    def stand(self):
        standtarget = self.foottarget[:2] + [self.zstand]
        self.moveto(standtarget, self.standnudges, NOLIFT)

    def sit(self):
        sittarget = self.foottarget[:2] + [self.zsit]
        self.moveto(sittarget, self.sitnudges, NOLIFT)

    def printstatus(self, alllegs=True):
        if self.legmoved or alllegs or self.error:
            legvec = [self.foottarget[i] - self.hipposition[i] for i in range(3)]
            output = "{} ".format(self.legnumber)
            if self.error:
                output += '*'
            tab = 8
            if self.printnudges:
                output += " "*(tab - len(output))
                output += "{}/{}  ".format(self.nudges-self.nudge, self.nudges)
                tab += 10
            output += " "*(tab - len(output))
            tab += 20
            output += "hip {}".format(str(intvec(self.hipposition)))
            output += " "*(tab - len(output))
            tab += 28
            output += "foot {}".format(str(intvec(self.foottarget)))
            output += " "*(tab - len(output))
            tab += 27
            output += "leg {}".format(str(intvec(legvec)))
            output += " "*(tab - len(output))
            output += "servo times {}".format(str(intvec(self.spider.servotimes[self.legnumber])))
            if self.error:
                output += " *** {}".format(self.error)
            print(output)
            self.legmoved = False
